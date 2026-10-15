"""
Demo 1 - Sampling: making TIME discrete.   (Lecture 1, sections 2.1-2.2)

A 1 Hz sine wave is a smooth, continuous thing. We measure it 4, 8 and 50
times per second and keep ONLY those measurements. Nyquist says we need more
than 2 x 1 Hz = 2 Hz. Watch what "more than twice" actually buys you.

Run:  python demo_01_sampling.py
"""

import numpy as np
import sslab

TONE_HZ = 1.0
DURATION_S = 2.0
RATES = [4, 8, 50]

# The "analog" world is faked by a very dense grid of points (1000 Hz).
t_analog, x_analog = sslab.sine(TONE_HZ, DURATION_S, fs_hz=1000)

print(f"A {TONE_HZ:.0f} Hz sine wave, {DURATION_S:.0f} s long.")
print(f"Nyquist says: sample faster than {2 * TONE_HZ:.0f} Hz.\n")

print(f"{'fs (Hz)':>8} {'samples':>8} {'gap T=1/fs':>12} {'reconstruction error':>22}")
print("-" * 54)

results = {}
for fs in RATES:
    t_s, x_s = sslab.sine(TONE_HZ, DURATION_S, fs_hz=fs)
    # Join the dots back up and see how far off we are from the true curve.
    x_back = sslab.reconstruct(t_s, x_s, t_analog)
    # Only judge the stretch actually covered by samples (no guessing past the end).
    inside = t_analog <= t_s[-1]
    max_error = float(np.max(np.abs(x_back[inside] - x_analog[inside])))
    results[fs] = (t_s, x_s, x_back)
    print(f"{fs:>8} {len(t_s):>8} {1/fs:>11.4f}s {max_error:>21.3f}")

print("""
Read it: at 4 Hz the Nyquist condition holds, so the frequency survives - but
the shape is crude. At 50 Hz the samples describe the curve so well that the
error nearly vanishes. Nothing was lost by throwing away the instants between
samples; only by taking too few of them.
""")

# ---- optional picture -----------------------------------------------------
plt = sslab.get_pyplot()
if plt:
    fig, axes = plt.subplots(len(RATES), 1, figsize=(9, 7), sharex=True)
    for ax, fs in zip(axes, RATES):
        t_s, x_s, x_back = results[fs]
        ax.plot(t_analog, x_analog, linewidth=1, label="true (analog) signal")
        shown = t_analog <= t_s[-1]   # do not draw past the last sample
        ax.plot(t_analog[shown], x_back[shown], "--", linewidth=1, label="reconstructed")
        ax.plot(t_s, x_s, "o", markersize=5, label=f"samples @ {fs} Hz")
        ax.set_ylabel("amplitude")
        ax.legend(loc="upper right", fontsize=8)
    axes[-1].set_xlabel("time (s)")
    axes[0].set_title(f"Sampling a {TONE_HZ:.0f} Hz sine at different rates")
    fig.tight_layout()
    fig.savefig("assets/demo_01_sampling.png", dpi=120)
    print("[saved] assets/demo_01_sampling.png")
