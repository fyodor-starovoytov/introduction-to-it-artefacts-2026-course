# Lab 1C report: Build the whole digitization loop


**Name:**
**Date of the report:**
**How long it took:**
**Name of collaboration partners:**


## 1. Pipeline

- Wanted tone: ____ Hz   Interference: ____ Hz
- Sampling rate: ____ Hz   Bit depth: ____   Filter taps: ____
- Why the null at fs/taps lands on the interference:

| stage | SNR |
|---|---|
| at the "microphone" | |
| after filtering | |
| after reconstruction | |

Figure: original, contaminated and recovered signals. *(figures/pipeline.png)*

## 2. Nyquist experiment

Range of sampling rates swept: ____ to ____ Hz, tone at ____ Hz.

Figure: apparent vs true frequency, with the fold marked.
*(figures/nyquist_fold.png)*

- Where does reconstruction stop being faithful, exactly?
- What happens at fs = 2B exactly, and why is "greater than" not pedantry?
- Sanity check: 6 kHz sampled at 8 kHz → ____ kHz (must be 2 kHz)

## 3. Quantization analysis

| bits | measured SNR | theory | gap | with dither | gap |
|---|---|---|---|---|---|

Figure: SNR vs bit depth with 6.02N+1.76 overlaid. *(figures/snr_vs_bits.png)*

### Where my results deviate from theory and why

*(Be specific. Candidates: the signal is not exactly full scale; at
low N the error is correlated with the signal and is distortion rather than
noise; FFT windowing; the dither trade — what it costs and what it buys.)*

## 4. Transfer — aliasing in a monitoring system

- Highest frequency that matters, and why:
- Maximum safe sampling interval, justified with Nyquist:
- Simulated dashboard values at several intervals:
- The mitigation I would deploy, and what it costs:

## Reflection

What is the one claim in this lab you would still defend if a senior engineer pushed back on it, and what evidence would you show them?
