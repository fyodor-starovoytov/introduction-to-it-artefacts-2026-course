# Lab 1D report — My own photo through the whole loop


**Name:**
**Date of the report:**
**How long it took:**
**Name of collaboration partners:**
**Photo I used:** *(what is in it, and why you chose it? where is the fine repeating detail? Do not submit any photo that has personally identifiable information, meaning selfie, or photos of other people)*

> Attach the pictures you produced. This lab is judged on what you saw and how
> well you explain it, not on getting a high number.

## Task 1 — What my camera already decided

| | value |
|---|---|
| pixels (width × height) | |
| megapixels | |
| raw size, computed by hand (w × h × channels × bits ÷ 8) | |
| actual size on disk | |
| compression ratio | |
| file format | |

Show the hand calculation, not just the number the script printed.

**Where did the missing bytes go, and what was traded away to save them?**

## Task 2 — Sampling, with and without the filter

- Sampling factor used:
- PSNR, no anti-aliasing filter:
- PSNR, filter applied first:

*(images: `01_no_filter.png` and `01_with_filter.png`)*

**What appeared in the unfiltered picture that was never in the scene?** Point
at the exact region — the bricks, the fence, the fabric.

**Why can this not be repaired afterwards?** Answer with reference to the three
cosines of `demo_02_aliasing.py` that produce identical samples.

**Both versions kept the same number of pixels. So what exactly was different?**

## Task 3 — Quantization

| bits | levels | PSNR | did I see banding? |
|---|---|---|---|
| 8 | 256 | | |
| 6 | 64 | | |
| 5 | 32 | | |
| 4 | 16 | | |
| 3 | 8 | | |
| 2 | 4 | | |

- The bit depth where **I** first saw banding:
- Where in the picture it appeared first (and why there rather than elsewhere):

**Dither, at that bit depth:** plain ___ dB, dithered ___ dB.

**One of them has the better number and the other looks better. Explain the
conflict, and say which one you would ship.**

## Task 4 — Processing is arithmetic

| filter | PSNR |
|---|---|
| noisy input | |
| 3×3 average | |
| 5×5 average | |
| 7×7 average | |
| 9×9 average | |

**Why does a wider filter stop helping?** (What does it start removing?)

## Task 5 — Reconstruction

- Repeat each pixel (the DAC staircase): ___ dB
- Interpolate between them (the reconstruction filter): ___ dB

*(images: `05_reconstructed_nearest.png` and `05_reconstructed_bilinear.png`)*

**The two numbers are close. Are the two pictures close? What does that tell
you about judging work by a single metric?**

## Reflection

1. Which loss in this lab was **irreversible**, and at which exact step was it committed?
2. Which loss was merely **unpleasant** but recoverable?
3. Your phone made all of these choices for you, before you ever saw the photo.
   Name one choice you would now make differently, and what it would cost.
