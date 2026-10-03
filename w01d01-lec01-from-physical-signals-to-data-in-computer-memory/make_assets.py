"""
make_assets.py - build the sound files the labs use.

Run this once before Lab 1A:   python make_assets.py
It writes into assets/ and prints exactly how big each file should be, so you
can check the arithmetic of "data volume is decided at digitization".
"""

import os
import numpy as np
import sslab
import wavtools

os.makedirs("assets", exist_ok=True)

SAMPLE_RATE = 44100        # CD rate
BIT_DEPTH = 16
DURATION = 2.0

files = {}

# 1. A plain 440 Hz tone (the "A" an orchestra tunes to).
_, tone = sslab.sine(440.0, DURATION, SAMPLE_RATE, amplitude=0.4)
files["tone_a440.wav"] = tone

# 2. A three-note chord - richer, so filtering it is audible.
_, c = sslab.sine(261.63, DURATION, SAMPLE_RATE, amplitude=0.3)
_, e = sslab.sine(329.63, DURATION, SAMPLE_RATE, amplitude=0.3)
_, g = sslab.sine(392.00, DURATION, SAMPLE_RATE, amplitude=0.3)
files["chord_cmaj.wav"] = c + e + g

# 3. A wanted tone spoiled by a high whine - raw material for Lab 1C.
_, wanted = sslab.sine(220.0, DURATION, SAMPLE_RATE, amplitude=0.6)
_, whine = sslab.sine(8000.0, DURATION, SAMPLE_RATE, amplitude=0.2)
files["noisy_tone.wav"] = wanted + whine

print(f"{'file':>20} {'on disk':>12} {'predicted':>12}   rate x depth x channels")
print("-" * 76)
for name, samples in files.items():
    path = os.path.join("assets", name)
    wavtools.write_wav(path, samples, SAMPLE_RATE)
    on_disk = os.path.getsize(path)
    predicted = wavtools.expected_size_bytes(SAMPLE_RATE, BIT_DEPTH, 1, DURATION)
    print(f"{name:>20} {on_disk:>12,} {int(predicted):>12,}   "
          f"{SAMPLE_RATE} Hz x {BIT_DEPTH} bit x 1 ch x {DURATION:.0f}s + 44-byte header")

rate = sslab.data_rate_bits_per_s(SAMPLE_RATE, BIT_DEPTH, 1)
print(f"\nRaw data rate of these files: {rate/1000:,.1f} kbit/s "
      f"({sslab.human_bytes(rate/8)} per second).")
print("Nothing here is compressed - a .wav file is the samples, almost naked.")
