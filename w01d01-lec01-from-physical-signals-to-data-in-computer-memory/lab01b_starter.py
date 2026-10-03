"""
LAB 1B - "Make aliasing and quantization happen"   (core; graded; 2-3 hours)

You produce the phenomena yourself and explain them. Fill in every TODO, then
run the file: the self-checks at the bottom tell you whether the numbers are
right. They do NOT grade your explanations - that is what the report is for.

Run:  python lab01b_starter.py

Deliverables: this file completed, lab01b_report.md, AI-log.md  (see templates/)
"""

import numpy as np
import sslab

# ===========================================================================
# TASK 1 - Alias on purpose
# ===========================================================================
# Choose a sampling rate and TWO tone frequencies - one below the Nyquist
# frequency, one above it - whose samples come out numerically IDENTICAL.
#
# Hint: the folding rule says a tone at f appears at |f - k*fs|. So pick any
# f_low below fs/2, then push it up by one whole fs.
#
# TODO 1a: choose your three numbers.
FS = 0.0            # <-- sampling rate in Hz, e.g. 8.0
F_LOW = 0.0         # <-- a tone BELOW fs/2
F_HIGH = 0.0        # <-- a tone ABOVE fs/2 that will masquerade as F_LOW

N_SAMPLES = 8

print("=" * 70)
print("TASK 1 - two different tones, one set of numbers")
print("=" * 70)

if FS > 0:
    t = np.arange(N_SAMPLES) / FS
    low = np.cos(2 * np.pi * F_LOW * t)
    high = np.cos(2 * np.pi * F_HIGH * t)

    print(f"\n  fs = {FS} Hz, Nyquist frequency = {sslab.nyquist_frequency(FS)} Hz")
    print(f"  samples of {F_LOW} Hz : {np.array2string(low, precision=4, suppress_small=True)}")
    print(f"  samples of {F_HIGH} Hz : {np.array2string(high, precision=4, suppress_small=True)}")
    print(f"  identical? {np.allclose(low, high)}")

    # TODO 1b: predict, using the folding rule, where F_HIGH will appear.
    #          Compute it BY HAND first, then check with sslab.alias_frequency.
    my_prediction_hz = 0.0        # <-- your hand calculation
    print(f"\n  your predicted alias of {F_HIGH} Hz: {my_prediction_hz} Hz")
    print(f"  sslab.alias_frequency says          : {sslab.alias_frequency(F_HIGH, FS)} Hz")
else:
    print("\n  (fill in TODO 1a first)")

# Q1 for your report: no algorithm can recover which tone produced these
# numbers. Explain in 3-4 sentences WHY, and say at which exact moment in the
# chain the information was lost.

# ===========================================================================
# TASK 2 - Quantize and measure
# ===========================================================================
# Write your own quantizer. Do not call sslab.quantize here - the point is to
# build it. Then measure the SNR and compare it with 6.02*N + 1.76 dB.

def my_quantize(x, n_bits, v_min=-1.0, v_max=1.0):
    """Round each sample onto one of 2**n_bits levels between v_min and v_max.

    Returns (quantized_signal, step_size).

    TODO 2a: implement this in three lines.
      1. step size q = (v_max - v_min) / 2**n_bits
      2. round each sample to the nearest multiple of q
      3. clip anything outside [v_min, v_max]
    """
    raise NotImplementedError("TODO 2a")


print("\n" + "=" * 70)
print("TASK 2 - more bits, better numbers")
print("=" * 70)

t_audio, x_audio = sslab.sine(440.0, 1.0, fs_hz=44100, amplitude=1.0)

try:
    print(f"\n{'bits':>6} {'levels':>10} {'step q':>12} {'max |error|':>13} "
          f"{'measured SNR':>14} {'6.02N+1.76':>12}")
    print("-" * 72)
    for n_bits in (4, 8, 12, 16):
        xq, q = my_quantize(x_audio, n_bits)
        measured = sslab.snr_db(x_audio, xq)
        print(f"{n_bits:>6} {2**n_bits:>10,} {q:>12.6f} "
              f"{np.max(np.abs(xq - x_audio)):>13.6f} {measured:>13.1f} dB "
              f"{sslab.theoretical_snr_db(n_bits):>11.1f}")
except NotImplementedError:
    print("\n  (implement my_quantize first - TODO 2a)")

# Q2 for your report: explain the ~6 dB per bit trend in one paragraph. Why 6?
# (Hint: adding a bit halves q. What does halving the error do to the ratio of
# signal power to error power, expressed in dB?)

# ===========================================================================
# TASK 3 - Reconcile a data rate with a real file
# ===========================================================================
# Pick ONE row of the lecture's Part-5 table, recompute its raw data rate from
# first principles, and reconcile it against a real file you create or download.

print("\n" + "=" * 70)
print("TASK 3 - where does file size come from?")
print("=" * 70)

# TODO 3a: fill in the three numbers for the source you chose.
CHOSEN_SOURCE = "..."          # <-- e.g. "CD audio"
CHOSEN_FS = 0                  # <-- sampling rate in Hz
CHOSEN_BITS = 0                # <-- bits per sample
CHOSEN_CHANNELS = 0            # <-- channels

if CHOSEN_FS > 0:
    rate = sslab.data_rate_bits_per_s(CHOSEN_FS, CHOSEN_BITS, CHOSEN_CHANNELS)
    print(f"\n  {CHOSEN_SOURCE}: {CHOSEN_FS} Hz x {CHOSEN_BITS} bits x "
          f"{CHOSEN_CHANNELS} ch = {rate/1000:,.1f} kbit/s")
    for seconds, label in ((60, "one minute"), (180, "a 3-minute song")):
        print(f"    {label:>16}: {sslab.human_bytes(rate * seconds / 8)}")

    # TODO 3b: measure a REAL file (use assets/tone_a440.wav, or any .wav or
    #          .mp3 on your computer). Put its path and duration here, then
    #          explain any gap between predicted and actual size in the report.
    REAL_FILE = ""             # <-- path to a real audio file
    if REAL_FILE:
        import os
        actual = os.path.getsize(REAL_FILE)
        print(f"\n  real file : {REAL_FILE}")
        print(f"  on disk   : {sslab.human_bytes(actual)}")
else:
    print("\n  (fill in TODO 3a first)")

# Q3 for your report: if your real file is much SMALLER than predicted, what
# happened to the missing bytes, and what was traded away to save them?

# ===========================================================================
# SELF-CHECK - run automatically; these must all pass before you submit
# ===========================================================================
print("\n" + "=" * 70)
print("SELF-CHECK")
print("=" * 70)

checks = []

# Task 1
if FS > 0:
    t = np.arange(N_SAMPLES) / FS
    same = np.allclose(np.cos(2 * np.pi * F_LOW * t), np.cos(2 * np.pi * F_HIGH * t))
    checks.append(("F_LOW is below the Nyquist frequency", F_LOW < FS / 2))
    checks.append(("F_HIGH is above the Nyquist frequency", F_HIGH > FS / 2))
    checks.append(("the two sample vectors are identical", same))
    checks.append(("your folding-rule prediction matches",
                   abs(my_prediction_hz - sslab.alias_frequency(F_HIGH, FS)) < 1e-9))
else:
    checks.append(("task 1 attempted", False))

# Task 2
try:
    xq, q = my_quantize(x_audio, 8)
    checks.append(("my_quantize step size is correct for 8 bits", abs(q - 2 / 256) < 1e-12))
    checks.append(("my_quantize error never exceeds q/2",
                   float(np.max(np.abs(xq - x_audio))) <= q / 2 + 1e-12))
    checks.append(("measured SNR is within 1.5 dB of theory",
                   abs(sslab.snr_db(x_audio, xq) - sslab.theoretical_snr_db(8)) < 1.5))
    clipped, _ = my_quantize(np.array([2.0, -2.0]), 8)
    checks.append(("my_quantize clips out-of-range input",
                   bool(np.all(np.abs(clipped) <= 1.0))))
except NotImplementedError:
    checks.append(("task 2 attempted", False))

# Task 3
checks.append(("task 3 numbers filled in", CHOSEN_FS > 0 and CHOSEN_BITS > 0))

for label, passed in checks:
    print(f"  [{'PASS' if passed else 'TODO'}] {label}")

print(f"\n{sum(p for _, p in checks)}/{len(checks)} checks passing.")
