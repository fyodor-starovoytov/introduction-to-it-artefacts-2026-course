# Lab 1B report: visualizing aliasing and quantization happen


**Name:**
**Date of the report:**
**How long it took:**
**Name of collaboration partners:**
**Self-checks passing:**  __ / __

## Task 1 — Alias on purpose

- Sampling rate chosen: ____ Hz  (Nyquist frequency ____ Hz)
- Tone below Nyquist: ____ Hz
- Tone above Nyquist: ____ Hz
- Folding-rule prediction, computed by hand: |____ − ____ × ____| = ____ Hz

Paste both sample vectors here and state whether they are identical.

**Why can no algorithm recover which tone produced these numbers?** (3–4
sentences. Name the exact moment the information was lost.)

## Task 2 — Quantize and measure

| bits | levels | step q | max error | measured SNR | 6.02N+1.76 |
|---|---|---|---|---|---|
| 4 | | | | | |
| 8 | | | | | |
| 12 | | | | | |
| 16 | | | | | |

**Why about 6 dB per bit?** (one paragraph)

**Did any measured error exceed q/2? Should it be able to?**

## Task 3 — Reconcile a data rate

- Source chosen:
- Rate × bit depth × channels =  ____ kbit/s
- Predicted size of ____ seconds:  ____
- Real file measured:  ____
- Difference, and what explains it:

**What was traded away to save those bytes?**
