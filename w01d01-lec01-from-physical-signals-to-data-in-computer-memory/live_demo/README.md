# Live demo — the whole pipeline, running, on a projector

`voice_pipeline.html` is one self-contained page that runs the entire Lecture 1
chain **in real time** and draws every stage as it happens:

```
the air → sample → quantize → the actual integers → down a noisy wire → back to sound
```

Every waveform on the screen is the data that just went through the pipeline a
few milliseconds ago. Nothing is pre-rendered, and there is no video.

## Running it

Open a terminal in this folder and start a tiny web server:

```bash
python -m http.server 8000
```

Then open <http://localhost:8000/voice_pipeline.html> and press **Start**
(browsers only allow audio after a click).

You can also just double-click the file, but serve it from `localhost` if you
want the **microphone** option: browsers only grant microphone access to pages
on `localhost` or `https`.

**No microphone, no problem.** Two of the three sources are synthetic — a voice
and a test tone generated in the page itself. They demonstrate everything, and
the test tone is *better* for teaching aliasing because you control its exact
frequency instead of asking someone to whistle on cue.

## The five-minute lecture choreography

Numbers below are what the page will show you; they line up with the lecture text.

**1 · "This is a voice."** Source *synthetic voice*, sampling rate 8000 Hz,
8 bits. Point at stage 1 (warm — the physical world) and stage 4 (cool — the
numbers). Read the data rate aloud: **64.0 kbit/s**. That is G.711, the number
that carried the world's telephone calls for forty years, and the class just
watched it be created.

**2 · "Watch time become discrete."** Drag the sampling rate down to 2000 Hz.
The dots in stage 2 thin out; the reconstruction in stage 6 gets coarse. Drag it
back up. Nyquist stops being a formula and becomes a picture.

**3 · The moment worth the whole demo.** Switch source to *test tone*. Set it to
1200 Hz — everything is fine. Now drag the tone slider upward while the class
watches stage 2. As you cross 4000 Hz (half of 8000), the dots begin tracing a
**slower** wave than the input, and a red banner appears:

> ⚠ ALIASING — your 6000 Hz tone is above the Nyquist limit. It is being
> recorded as 2000 Hz, and no software downstream can ever tell.

Ask the room: *the input went up, the recording went down — where did the real
frequency go?* Then turn the speaker on (headphones or a quiet hall) and sweep
again: they **hear** the pitch rise, fold, and come back down.

**4 · "Why the filter must come first."** With the tone still above Nyquist,
toggle **anti-alias filter: ON / OFF**. The filter cannot rescue an alias that
has already been recorded — it prevents one. That is exactly why it lives before
the sampler in the block diagram, and why the CD's 44,100 Hz leaves a guard band
for it to work in.

**5 · "Now amplitude."** Back to *synthetic voice*. Drag **bits** from 16 down to
3 and watch stage 3 turn into a visible staircase, `q` grow from 0.00003 to
0.25000, and the data rate fall from 128 kbit/s to 24 kbit/s. With the speaker
on, the class hears the hiss arrive. Then push bits back up and note that past a
point it stops helping — because the bottleneck has moved to the sampling rate.
That is the telephone's thin voice, derived live.

**6 · "Why numbers beat voltages."** Raise **channel noise** slowly and compare
the two lanes in stage 5. The analog lane degrades from the first nudge. The
digital lane is perfect, perfect, perfect — the receiver decides *1 or 0* and
retransmits a clean signal — and then, past about 50%, bits start flipping and
the readout turns red. Digital does not degrade gracefully; it is exact until it
is broken. That cliff is why a call from Jyväskylä to Hawaii sounds like the
room next door, and why it dies abruptly rather than fading.

## What each control actually does

| Control | What it changes in the pipeline |
|---|---|
| **source** | What plays the part of "the physical world": a synthetic voice, a pure test tone, or your microphone |
| **tone** | The test tone's true frequency — drag it past half the sampling rate to force aliasing |
| **sampling rate** | How often the sampler measures. The Nyquist limit is always half of this |
| **bits** | How many levels the quantizer may use: 2^bits, with step q = 2 / 2^bits |
| **channel noise** | Noise added to each bit's voltage on the wire, and to an analog copy for comparison |
| **anti-alias filter** | Whether the signal is low-passed *before* the sampler — the point of §2.3 |
| **reconstruct** | Zero-order hold (the DAC's raw staircase) versus interpolation (the reconstruction filter) |
| **speaker** | Plays the reconstructed output. **Use headphones** — a microphone plus speakers is a feedback howl |

## Notes for whoever maintains this

- One `ScriptProcessorNode` does the whole chain block by block; `processBlock()`
  in the page is the entire lecture in about 60 lines of arithmetic, and it is
  meant to be read by students who want to know how it works.
- The sampling rate you select is snapped to an integer division of the browser's
  hardware rate (usually 48 kHz), so the readout shows the rate actually used.
- Colour is information here: **warm = the continuous physical world**,
  **cool = discrete numbers**. Red means something is genuinely broken.
- `ScriptProcessorNode` is deprecated but works in every current browser and
  keeps the code readable. If it is ever removed, the same 60 lines move into an
  `AudioWorklet` unchanged.
