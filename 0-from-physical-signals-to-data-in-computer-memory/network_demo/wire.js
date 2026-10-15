/* wire.js — everything the three pages agree on.
 *
 * A protocol is nothing more than two programs agreeing on what the bytes mean.
 * Here is the entire agreement, in one file, used by the sender, the receiver
 * and the monitor — and parsed again in Python by relay.py.
 *
 *   byte 0     0xA5        a magic number, so we can tell our packets apart
 *   byte 1     bits        8 or 16 bits per sample
 *   bytes 2-3  seq         sequence number, so the receiver can spot losses
 *   bytes 4-5  fs          sampling rate in Hz
 *   bytes 6-7  count       how many samples follow
 *   bytes 8..  samples     the voice itself, as plain integers
 *
 * Eight bytes of header. Everything else is the sound.
 */

const MAGIC = 0xA5;
const HEADER = 8;

function encodePacket({ seq, fs, bits, samples }) {
  const wide = bits > 8;
  const buf = new ArrayBuffer(HEADER + samples.length * (wide ? 2 : 1));
  const view = new DataView(buf);
  view.setUint8(0, MAGIC);
  view.setUint8(1, bits);
  view.setUint16(2, seq & 0xffff);
  view.setUint16(4, fs);
  view.setUint16(6, samples.length);
  for (let i = 0; i < samples.length; i++) {
    if (wide) view.setInt16(HEADER + i * 2, samples[i]);
    else view.setInt8(HEADER + i, samples[i]);
  }
  return buf;
}

function decodePacket(buf) {
  const view = new DataView(buf);
  if (view.byteLength < HEADER || view.getUint8(0) !== MAGIC) return null;
  const bits = view.getUint8(1);
  const wide = bits > 8;
  const count = view.getUint16(6);
  const samples = new Int16Array(count);
  for (let i = 0; i < count; i++) {
    samples[i] = wide ? view.getInt16(HEADER + i * 2) : view.getInt8(HEADER + i);
  }
  return {
    bits, count, samples,
    seq: view.getUint16(2),
    fs: view.getUint16(4),
    bytes: view.byteLength,
    hex: hexOf(buf, 16),
  };
}

function hexOf(buf, n) {
  const b = new Uint8Array(buf, 0, Math.min(n, buf.byteLength));
  return Array.from(b, x => x.toString(16).padStart(2, "0")).join(" ");
}

/* The socket back to relay.py. It reconnects on its own, because a lecture is
   no place to be reloading tabs. */
function connect(role, onPacket, onState) {
  let ws = null, retry = null;

  const open = () => {
    const proto = location.protocol === "https:" ? "wss:" : "ws:";
    ws = new WebSocket(`${proto}//${location.host}/ws?role=${role}`);
    ws.binaryType = "arraybuffer";

    ws.onopen = () => { onState && onState("connected"); };
    ws.onclose = () => {
      onState && onState("disconnected");
      clearTimeout(retry);
      retry = setTimeout(open, 1000);
    };
    ws.onerror = () => ws.close();
    ws.onmessage = (e) => {
      if (!(e.data instanceof ArrayBuffer)) return;
      const packet = decodePacket(e.data);
      if (packet) onPacket && onPacket(packet, e.data);
    };
  };
  open();

  return {
    send: (buf) => { if (ws && ws.readyState === 1) ws.send(buf); },
    get ready() { return ws && ws.readyState === 1; },
  };
}

/* A small oscilloscope, so all three pages draw the same way. */
function scope(canvas) {
  const g = canvas.getContext("2d");
  return function draw(data, colour, span) {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (canvas.width !== w * dpr) { canvas.width = w * dpr; canvas.height = h * dpr; }
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, w, h);

    g.strokeStyle = getComputedStyle(canvas).getPropertyValue("--grid") || "#eee";
    g.lineWidth = 1;
    g.beginPath(); g.moveTo(0, h / 2); g.lineTo(w, h / 2); g.stroke();

    const n = span || data.length;
    g.strokeStyle = colour; g.lineWidth = 1.6; g.beginPath();
    for (let i = 0; i < n; i++) {
      const x = (i / n) * w, y = h / 2 - (data[i] || 0) * h * 0.45;
      i ? g.lineTo(x, y) : g.moveTo(x, y);
    }
    g.stroke();
  };
}

window.Wire = { encodePacket, decodePacket, connect, scope, hexOf, HEADER, MAGIC };
