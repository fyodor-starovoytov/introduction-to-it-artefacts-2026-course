"""
relay.py - the network in the middle of Lecture 1's loop.

Run this on the SOURCE computer. It does three jobs at once:

  1. serves the three web pages (sender, receiver, packet monitor)
  2. relays every voice packet from the sender to every receiver and monitor
  3. prints each packet as it passes, so the terminal itself is a demo

Python standard library only - no pip install, no framework. The WebSocket
handshake and framing below are about eighty lines, and they are worth reading:
this is what "a protocol" actually looks like.

    python relay.py                       # normal
    python relay.py --loss 5              # drop 5% of packets, on purpose
    python relay.py --delay 120           # add 120 ms of delay to every packet
    python relay.py --port 8000

Then, on the SOURCE computer:        http://localhost:8000/sender.html
and on the DESTINATION computer:     http://<this computer's IP>:8000/receiver.html
and anywhere at all:                 http://<this computer's IP>:8000/monitor.html
"""

import argparse
import base64
import hashlib
import os
import random
import socket
import struct
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"     # fixed by RFC 6455
HERE = os.path.dirname(os.path.abspath(__file__))

clients = {}            # socket -> role ("sender" / "receiver" / "monitor")
clients_lock = threading.Lock()
stats = {"packets": 0, "bytes": 0, "dropped": 0, "started": time.time()}
OPTS = {"loss": 0.0, "delay": 0.0, "quiet": False}


# ---------------------------------------------------------------------------
# WebSocket frames, by hand
# ---------------------------------------------------------------------------
def ws_send(sock, payload, opcode=0x2):
    """Send one frame. opcode 0x2 = binary, 0x1 = text."""
    header = bytearray([0x80 | opcode])          # FIN + opcode, never fragmented
    n = len(payload)
    if n < 126:
        header.append(n)                          # small payloads: length fits in 7 bits
    elif n < 65536:
        header.append(126)
        header += struct.pack("!H", n)            # 126 means "the next 2 bytes are the length"
    else:
        header.append(127)
        header += struct.pack("!Q", n)
    sock.sendall(bytes(header) + payload)         # server->client frames are never masked


def ws_recv(sock):
    """Read one frame. Returns (opcode, payload) or None when the peer goes away."""
    def read(n):
        buf = b""
        while len(buf) < n:
            chunk = sock.recv(n - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf

    head = read(2)
    if not head:
        return None
    opcode = head[0] & 0x0F
    masked = head[1] & 0x80
    length = head[1] & 0x7F

    if length == 126:
        length = struct.unpack("!H", read(2))[0]
    elif length == 127:
        length = struct.unpack("!Q", read(8))[0]

    mask = read(4) if masked else None
    payload = read(length) if length else b""
    if payload is None:
        return None
    if mask:                                       # browser->server frames ARE masked
        payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    return opcode, payload


# ---------------------------------------------------------------------------
# The packet format - defined identically in wire.js
#
#   byte 0     magic 0xA5
#   byte 1     bits per sample (8 or 16)
#   bytes 2-3  sequence number
#   bytes 4-5  sampling rate in Hz
#   bytes 6-7  how many samples follow
#   then       the samples themselves
# ---------------------------------------------------------------------------
def describe(packet):
    if len(packet) < 8 or packet[0] != 0xA5:
        return None
    bits, seq, fs, count = packet[1], *struct.unpack("!HHH", packet[2:8])
    return {"bits": bits, "seq": seq, "fs": fs, "count": count, "bytes": len(packet)}


def broadcast(packet, sender_sock):
    """Pass the packet on to everyone who is listening - with the impairments
    the lecturer asked for, so a lossy link can be demonstrated on purpose."""
    if OPTS["loss"] and random.random() < OPTS["loss"]:
        stats["dropped"] += 1
        return

    def deliver():
        with clients_lock:
            targets = [s for s, role in clients.items() if role != "sender" or s is not sender_sock]
        for sock in targets:
            try:
                ws_send(sock, packet)
            except OSError:
                pass

    if OPTS["delay"]:
        threading.Timer(OPTS["delay"], deliver).start()
    else:
        deliver()


# ---------------------------------------------------------------------------
# HTTP + WebSocket in one server
# ---------------------------------------------------------------------------
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=HERE, **kw)

    def log_message(self, *a):
        pass                                        # the packet log is the interesting one

    def do_GET(self):
        if self.headers.get("Upgrade", "").lower() != "websocket":
            return super().do_GET()

        key = self.headers.get("Sec-WebSocket-Key", "")
        accept = base64.b64encode(hashlib.sha1((key + WS_GUID).encode()).digest()).decode()
        self.wfile.write(("HTTP/1.1 101 Switching Protocols\r\n"
                          "Upgrade: websocket\r\nConnection: Upgrade\r\n"
                          f"Sec-WebSocket-Accept: {accept}\r\n\r\n").encode())

        role = "monitor"
        if "role=" in self.path:
            role = self.path.split("role=")[1].split("&")[0]
        sock = self.connection
        with clients_lock:
            clients[sock] = role
        announce(f"+ {role} connected from {self.client_address[0]}")

        try:
            while True:
                frame = ws_recv(sock)
                if frame is None:
                    break
                opcode, payload = frame
                if opcode == 0x8:                   # close
                    break
                if opcode == 0x9:                   # ping -> pong
                    ws_send(sock, payload, opcode=0xA)
                    continue
                if opcode == 0x2 and payload:
                    info = describe(payload)
                    if info:
                        stats["packets"] += 1
                        stats["bytes"] += len(payload)
                        if not OPTS["quiet"] and stats["packets"] % 25 == 1:
                            print(f"  seq {info['seq']:>5}  {info['count']:>4} samples  "
                                  f"{info['bits']:>2}-bit  {info['fs']:>6} Hz  "
                                  f"{info['bytes']:>5} bytes   first bytes: "
                                  f"{payload[8:16].hex(' ')}")
                    broadcast(payload, sock)
        except OSError:
            pass
        finally:
            with clients_lock:
                clients.pop(sock, None)
            announce(f"- {role} disconnected")


def announce(text):
    print(text, flush=True)


def local_ip():
    """The address the other computer should type. Works without internet."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))            # nothing is actually sent
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def report():
    """Once a second, say what is actually crossing the wire."""
    last = dict(stats)
    while True:
        time.sleep(1.0)
        packets = stats["packets"] - last["packets"]
        byts = stats["bytes"] - last["bytes"]
        if packets:
            with clients_lock:
                roles = list(clients.values())
            print(f"[{packets:>3} packets/s  {byts * 8 / 1000:>6.1f} kbit/s  "
                  f"dropped {stats['dropped']:>4}]  "
                  f"connected: {roles.count('sender')} sender, "
                  f"{roles.count('receiver')} receiver, {roles.count('monitor')} monitor",
                  flush=True)
        last = dict(stats)


def main():
    ap = argparse.ArgumentParser(description="Voice packet relay for Lecture 1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--loss", type=float, default=0, help="percent of packets to drop on purpose")
    ap.add_argument("--delay", type=float, default=0, help="extra delay in milliseconds")
    ap.add_argument("--quiet", action="store_true", help="only the per-second summary")
    args = ap.parse_args()

    OPTS["loss"] = args.loss / 100.0
    OPTS["delay"] = args.delay / 1000.0
    OPTS["quiet"] = args.quiet

    ip = local_ip()
    print("=" * 72)
    print("  Voice over the network - Lecture 1")
    print("=" * 72)
    print(f"\n  On THIS computer (the source), open:")
    print(f"      http://localhost:{args.port}/sender.html")
    print(f"        ^ must be 'localhost' - browsers only allow the microphone there\n")
    print(f"  On the OTHER computer (the destination), open:")
    print(f"      http://{ip}:{args.port}/receiver.html\n")
    print(f"  On either computer, to watch the packets:")
    print(f"      http://{ip}:{args.port}/monitor.html\n")
    if args.loss or args.delay:
        print(f"  Impairments active: {args.loss}% loss, {args.delay} ms extra delay\n")
    print("  If the other computer cannot connect, it is almost always the")
    print("  firewall on this machine - allow Python on private networks.\n")
    print("-" * 72)

    threading.Thread(target=report, daemon=True).start()
    server = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")


if __name__ == "__main__":
    main()
