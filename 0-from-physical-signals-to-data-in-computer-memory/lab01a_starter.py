"""
LAB 1A - "Watch the world become numbers"   (familiarize; <= 1 hour)

Nothing to build from scratch. Run it, read the numbers, and write down what
you saw. Three tiny TODOs are marked below; each is one or two lines.

Run:  python lab01a_starter.py
Then answer the questions in lab01a_report.md (template in templates/).

Before you start:  python make_assets.py
"""

import os
import numpy as np
import sslab
import wavtools

print("=" * 70)
print("PART 1 - a sine wave, measured at three different rates")
print("=" * 70)

TONE_HZ = 1.0
t_true, x_true = sslab.sine(TONE_HZ, 2.0, fs_hz=1000)      # the "analog" truth

for fs in (4, 8, 50):
    t_s, x_s = sslab.sine(TONE_HZ, 2.0, fs_hz=fs)
    print(f"\n  fs = {fs} Hz  ->  {len(t_s)} samples in 2 seconds, "
          f"one every {1/fs:.3f} s")
    print(f"  first four stored values: "
          f"{np.array2string(x_s[:4], precision=3, suppress_small=True)}")

# TODO 1: The Nyquist rule says fs must be greater than 2 x the highest
#         frequency present. Our tone is 1 Hz. Which of 4, 8, 50 Hz satisfy it?
#         Set the variable below to a list of the rates that DO satisfy it.
rates_that_satisfy_nyquist = []          # <-- fill this in, e.g. [8, 50]

print(f"\n  your answer - rates satisfying Nyquist for a {TONE_HZ:.0f} Hz tone: "
      f"{rates_that_satisfy_nyquist}")

print("""
  Q1 (for your report): in one sentence, what does "too few samples" look
  like when you plot the dots over the true curve? Run demo_01_sampling.py
  with matplotlib installed to see the picture.
""")

print("=" * 70)
print("PART 2 - a real file: where does its size come from?")
print("=" * 70)

path = os.path.join("assets", "tone_a440.wav")
samples, info = wavtools.read_wav(path)

print(f"\n  file            : {path}")
print(f"  sample rate     : {info['sample_rate']} Hz")
print(f"  bit depth       : {info['bit_depth']} bits per sample")
print(f"  channels        : {info['channels']}")
print(f"  duration        : {info['duration_s']:.2f} s")
print(f"  samples stored  : {info['n_frames']:,}")

# TODO 2: predict the file size BEFORE looking. The formula is
#         rate x (bits/8) x channels x seconds, plus a 44-byte WAV header.
predicted_bytes = 0                       # <-- fill in your calculation

actual_bytes = os.path.getsize(path)
print(f"\n  you predicted   : {predicted_bytes:,} bytes")
print(f"  actually on disk: {actual_bytes:,} bytes")
print(f"  difference      : {actual_bytes - predicted_bytes:,} bytes")
print("""
  Q2 (for your report): if your prediction was 44 bytes short, what is that
  header for? If it was wildly off, which of the four numbers above did you
  forget to multiply by?
""")

print("=" * 70)
print("PART 3 - processing is just arithmetic")
print("=" * 70)

# Louder = multiply. Quieter = multiply by less than one. That is the whole
# trick; there is no hidden audio library doing something clever.
loud = sslab.amplify(samples, 2.0)
quiet = sslab.amplify(samples, 0.5)

wavtools.write_wav(os.path.join("assets", "tone_a440_loud.wav"), loud, info["sample_rate"])
wavtools.write_wav(os.path.join("assets", "tone_a440_quiet.wav"), quiet, info["sample_rate"])

print(f"\n  original peak amplitude : {np.max(np.abs(samples)):.3f}")
print(f"  x 2.0  peak amplitude   : {np.max(np.abs(loud)):.3f}")
print(f"  x 0.5  peak amplitude   : {np.max(np.abs(quiet)):.3f}")
print("  wrote assets/tone_a440_loud.wav and assets/tone_a440_quiet.wav")

# TODO 3: multiply by 4.0 instead. Peak amplitude cannot exceed 1.0 in a WAV
#         file, so what must happen to the samples? Write the file, listen to
#         it, and name the effect in your report (hint: section 2.4).
too_loud = sslab.amplify(samples, 4.0)
wavtools.write_wav(os.path.join("assets", "tone_a440_too_loud.wav"), too_loud,
                   info["sample_rate"])
print(f"\n  x 4.0  peak amplitude before writing : {np.max(np.abs(too_loud)):.3f}")
print(f"  fraction of samples beyond +/-1.0    : "
      f"{np.mean(np.abs(too_loud) > 1.0) * 100:.1f}%  (these get flattened)")

print("""
  Q3 (for your report): listen to all three files. Name the effect that
  appears in the x4.0 version, and say why more bits would NOT fix it.

Done. Now fill in templates/lab01a_report.md and templates/AI-log.md.
""")
