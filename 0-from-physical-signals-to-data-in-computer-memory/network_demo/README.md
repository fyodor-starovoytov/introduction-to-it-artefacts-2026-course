# Two computers, one voice — the network demo

A voice goes into a microphone on **one** computer, crosses the room as packets
over WiFi, and comes out of the loudspeaker on **another**. Three screens show
the three things students should see at once:

| Screen | Runs on | Shows |
|---|---|---|
| **sender** | the source computer | the analog waveform being captured, and what is leaving as packets |
| **receiver** | the destination computer | the sound being rebuilt from integers, and how the delivery went |
| **monitor** | any computer, projector by choice | the packets themselves — headers, bytes, rate, losses |

Nothing to install. Python standard library plus a browser.

---

## Setup, in three commands

**On the SOURCE computer** (this one holds the microphone and runs the relay):

```bash
python relay.py
```

It prints the exact addresses to open, including this machine's IP on the WiFi.

**On the SOURCE computer**, open:

```
http://localhost:8000/sender.html
```

> It must be `localhost`, not the IP address. Browsers only grant microphone
> access to pages served from `localhost` or `https` — that restriction is a
> security feature, not a bug, and it is the reason the relay runs on the source
> machine.

**On the DESTINATION computer**, open the address the relay printed:

```
http://<source computer's IP>:8000/receiver.html
```

Playing sound needs no permission, so the destination has no such restriction.

**Optionally, on either computer**, open `monitor.html` at the same address —
this is the one to put on the projector.

Press **Start** on the sender, press **Start listening** on the receiver, and
talk.

### If the destination cannot connect

Almost always the firewall on the source computer. On Windows, the first run
pops up a dialog — allow Python on **private networks**. Otherwise check that
both machines really are on the same WiFi (some campus and guest networks
isolate clients from each other; a phone hotspot is a reliable fallback).

---

## What the demo actually shows

### 1. Your voice becomes a number, and only a number

The sender captures continuous air pressure, samples it 8000 times a second,
rounds each sample to 8 bits, and packs 20 milliseconds of them into a packet
with an 8-byte header. Point at the receiver's screen: those integers are the
**entire** message. No sound crossed the room — only numbers did.

### 2. Where the 64 kbit/s comes from

The sender shows `8000 × 8 = 64.0 kbit/s`, and the monitor shows the real total
including headers (about 67 kbit/s). That is a telephone call, exactly:
this demo's default settings *are* G.711, the standard that carried the world's
voice traffic for forty years.

Drag **packet length** on the sender from 20 ms up to 100 ms and watch the
header overhead fall from 4.8% to under 1% — then explain why nobody does it:
longer packets mean more delay before the first sample can be sent, and a
conversation with lag is worse than a conversation with overhead.

### 3. Quality is a dial, and the class can hear every notch

On the sender, drag **bits per sample** down from 8 to 4 while the destination
is playing. The data rate halves; the voice gets grainy. Drag **sampling rate**
down to 4000 Hz and consonants start to disappear — Nyquist, audible across the
room.

### 4. What a bad network sounds like

Stop the relay and start it again with impairments:

```bash
python relay.py --loss 10
```

Ten percent of packets are now thrown away on purpose. The receiver's **lost**
counter climbs, the monitor's flow strip fills with red gaps, and the voice at
the destination acquires exactly the choppy, robotic quality of a bad video
call. Students have heard this a thousand times; now they can see the cause.

```bash
python relay.py --delay 300
```

Every packet is held back 300 ms. Nothing is lost, everything is late, and the
conversation becomes impossible — the failure mode of a satellite link.

### 5. The jitter buffer, and why your call is always slightly delayed

On the receiver, drag the **jitter buffer** slider to 0 and listen: gaps appear,
the "gaps in playback" counter climbs. Packets that arrive a few milliseconds
late are useless — you cannot play sound whose moment has passed. Drag it up to
300 ms and the audio is smooth, but the destination is now a third of a second
behind the speaker.

Every phone call, every video conference, every game voice chat sits somewhere
on that trade, chosen by an engineer. There is no setting that wins.

---

## The packet, byte by byte

The monitor's middle panel decodes the last packet live. This is the whole
protocol — it is defined once in `wire.js` and parsed again in `relay.py`:

```
byte 0     0xA5     magic number, so we know it is ours
byte 1     bits     8 or 16 bits per sample
bytes 2-3  seq      sequence number — how the receiver detects a loss
bytes 4-5  fs       sampling rate in Hz
bytes 6-7  count    how many samples follow
bytes 8..  samples  the voice itself
```

A real VoIP call adds RTP, UDP and IP headers — 40 more bytes per packet, which
at 50 packets per second is another 16 kbit/s of pure overhead. Worth mentioning
when a student asks why the measured rate never matches the arithmetic exactly.

---

## Files

| File | What it is |
|---|---|
| `relay.py` | The server: serves the pages, relays packets, prints them, and can damage them on request |
| `wire.js` | The packet format and the WebSocket connection, shared by all three pages |
| `sender.html` | Source station — capture, sample, quantize, packetize, send |
| `receiver.html` | Destination station — receive, buffer, reconstruct, play |
| `monitor.html` | The packet inspector |
| `station.css` | Shared styling. Warm = the physical world, cool = numbers on a wire |

`relay.py` implements the WebSocket handshake and framing by hand in about
eighty lines of standard library. That is deliberate: a student who wants to
know what "a protocol" means can read it in one sitting.

---

## Practical notes for the lecture room

- **Use headphones on the source computer**, or mute it. Microphone plus
  loudspeaker in one room is a feedback howl.
- **Keep both browser windows visible.** Browsers throttle background tabs, and
  a minimised receiver will let its buffer drift (measured: the buffer pins at
  its maximum and the delay grows). Side-by-side windows also make the better
  demo.
- **Two computers is the point, but one works.** Open the sender and receiver in
  two windows on the same machine if a second laptop falls through — everything
  still runs, and the packets still cross the loopback network.
- **The relay prints every packet.** Putting that terminal on the projector next
  to the monitor page is a strong pairing: the same packets, in two very
  different views.
- Verified end to end before publishing: 50 packets/s, 168 bytes each,
  67 kbit/s on the wire, 0 lost over a clean link, ~12% lost with `--loss 10`,
  and a jitter buffer that holds steady at about 135 ms.
