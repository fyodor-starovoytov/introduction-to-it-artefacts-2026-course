"""
LAB 1C - "Build the whole loop"   (challenge; optional; 3-4 hours)

    analog -> sample -> quantize -> process -> reconstruct -> analog

Four parts. The scaffolding below gives you the structure, the measurement
helpers, and the printing; the engineering decisions and the honest error
analysis are yours. Rigor of method and honesty about deviations matter more
here than a pretty result.

Run:  python lab01c_starter.py

Deliverables: this file completed, lab01c_report.md (with plots), AI-log.md
"""

import numpy as np
import sslab

# ===========================================================================
# PART 1 - The pipeline
# ===========================================================================
# Build the full chain for a WANTED low tone contaminated by an UNWANTED high
# tone. Remove the unwanted one with a moving average, reconstruct, and report
# the SNR before and after. demos/demo_04_full_chain.py is the worked example -
# use it as a reference, not as a copy: change the frequencies and the rate,
# and make the filter null land on YOUR interference.

WANTED_HZ = 0.0        # TODO: the tone you want to keep
NOISE_HZ = 0.0         # TODO: the tone you want to delete
FS = 0                 # TODO: sampling rate (respect Nyquist for BOTH tones)
N_BITS = 0             # TODO: quantizer resolution
TAPS = 0               # TODO: odd number; the null sits at fs / TAPS


def run_pipeline(wanted_hz, noise_hz, fs, n_bits, taps, duration=0.1,
                 noise_amp=0.15, wanted_amp=0.8):
    """Return a dict of everything the report needs. TODO: fill in the gaps."""
    t = np.arange(0, duration, 1 / fs)
    clean = wanted_amp * np.sin(2 * np.pi * wanted_hz * t)
    contaminated = clean + noise_amp * np.sin(2 * np.pi * noise_hz * t)

    # TODO 1a: quantize the contaminated signal (sslab.quantize).
    stored, q = None, None

    # TODO 1b: filter it with a moving average (sslab.moving_average).
    processed = None

    # TODO 1c: measure SNR before and after (sslab.snr_db, ignoring the first
    #          and last few samples where the filter runs off the edge).
    edge = taps
    snr_before = None
    snr_after = None

    return {"t": t, "clean": clean, "contaminated": contaminated,
            "stored": stored, "q": q, "processed": processed,
            "snr_before": snr_before, "snr_after": snr_after, "edge": edge}


print("=" * 70)
print("PART 1 - the pipeline")
print("=" * 70)
if FS > 0:
    r = run_pipeline(WANTED_HZ, NOISE_HZ, FS, N_BITS, TAPS)
    print(f"  filter null lands at fs/TAPS = {FS/TAPS:,.0f} Hz "
          f"(your interference is at {NOISE_HZ:,.0f} Hz)")
    print(f"  SNR before : {r['snr_before']} dB")
    print(f"  SNR after  : {r['snr_after']} dB")
else:
    print("  (fill in the parameters and the TODOs in run_pipeline)")

# Report: plot original, contaminated and recovered signals on one figure.

# ===========================================================================
# PART 2 - The Nyquist experiment
# ===========================================================================
# Sweep the sampling rate from well below 2B to well above it. For each rate,
# sample a fixed tone, measure the recovered frequency with an FFT
# (sslab.dominant_frequency), and plot apparent vs true. Show the fold.

TONE_HZ = 3000.0                      # the tone we keep fixed
SWEEP_RATES = []                      # TODO: e.g. range(2000, 12001, 500)

print("\n" + "=" * 70)
print("PART 2 - where reconstruction stops being faithful")
print("=" * 70)

if SWEEP_RATES:
    print(f"\n{'fs (Hz)':>10} {'Nyquist':>10} {'apparent (FFT)':>16} "
          f"{'folding rule':>14} {'faithful?':>10}")
    print("-" * 66)
    for fs in SWEEP_RATES:
        # TODO 2a: sample TONE_HZ at fs for a sensible duration.
        # TODO 2b: measure the dominant frequency of those samples.
        # TODO 2c: compare against sslab.alias_frequency(TONE_HZ, fs).
        pass
else:
    print("  (choose your sweep of sampling rates)")

# Sanity check you can rely on: a 6 kHz tone sampled at 8 kHz must show an FFT
# peak at 2 kHz. If your code disagrees, your code is wrong - not the theory.
print(f"\n  sanity check: alias_frequency(6000, 8000) = "
      f"{sslab.alias_frequency(6000, 8000):.0f} Hz  (must be 2000)")

# ===========================================================================
# PART 3 - Quantization analysis, honestly
# ===========================================================================
# Measure SNR against bit depth for N = 2..16, overlay 6.02N + 1.76, and
# discuss deviations HONESTLY: is the signal truly full scale? Is the error
# correlated with the signal at low N? Does windowing matter? Then add dither
# at low N (sslab.dither) and report what changes.

print("\n" + "=" * 70)
print("PART 3 - SNR against bit depth")
print("=" * 70)

BIT_DEPTHS = []                        # TODO: e.g. range(2, 17)

if BIT_DEPTHS:
    print(f"\n{'bits':>6} {'measured':>12} {'theory':>10} {'gap':>8} {'with dither':>13}")
    print("-" * 54)
    for n in BIT_DEPTHS:
        # TODO 3a: quantize a full-scale sine, measure SNR, compare to theory.
        # TODO 3b: repeat with dither applied before quantizing.
        pass
else:
    print("  (choose your range of bit depths)")

# ===========================================================================
# PART 4 - Transfer: the same theorem, in software
# ===========================================================================
# A service spikes for 30 seconds every 5 minutes. Your monitoring samples CPU
# every SAMPLE_INTERVAL seconds. Treat the spike train as the signal.

SPIKE_PERIOD_S = 300
SPIKE_WIDTH_S = 30

print("\n" + "=" * 70)
print("PART 4 - aliasing in a monitoring system")
print("=" * 70)

# TODO 4a: what is the highest frequency you must capture to see the spike,
#          and what sampling interval does Nyquist therefore demand?
highest_frequency_hz = 0.0             # <-- your reasoning here
max_safe_interval_s = 0.0              # <-- your answer

print(f"\n  spike: {SPIKE_WIDTH_S}s long, every {SPIKE_PERIOD_S}s")
print(f"  highest frequency to capture : {highest_frequency_hz} Hz")
print(f"  maximum safe sample interval : {max_safe_interval_s} s")

# TODO 4b: simulate it. Build the spike train on a 1-second grid, sample it at
#          several intervals (say 10s, 60s, 150s, 300s) and print the peak the
#          dashboard would show. Watch a real outage become invisible.

print("""
  For the report: justify max_safe_interval_s with Nyquist, show the simulated
  dashboard values, and name ONE practical mitigation an engineer would deploy
  (hint: what if each stored point carried the min and max seen since the last
  point, instead of a single instantaneous reading?).
""")
