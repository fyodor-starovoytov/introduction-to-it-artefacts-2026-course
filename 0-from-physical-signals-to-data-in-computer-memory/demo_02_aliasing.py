"""
Demo 2 - Aliasing: what happens when you sample too slowly.  (Section 2.3)

Sample three DIFFERENT cosine waves - 1 Hz, 7 Hz and 9 Hz - at fs = 8 Hz and
look at the numbers you actually stored. They are not similar. They are
identical. The information that told them apart was destroyed at the instant
of sampling, so no later software - and no AI - can bring it back.

Run:  python demo_02_aliasing.py
"""

import numpy as np
import sslab

FS = 8.0          # samples per second
TONES = [1.0, 7.0, 9.0]
N = 8             # look at one second's worth

print(f"Sampling at fs = {FS:.0f} Hz  ->  Nyquist frequency = {sslab.nyquist_frequency(FS):.0f} Hz\n")

t = np.arange(N) / FS
columns = {f: np.cos(2 * np.pi * f * t) for f in TONES}

print(f"{'n':>2} {'t (s)':>7} " + " ".join(f"{'cos %g Hz' % f:>10}" for f in TONES))
print("-" * 44)
for n in range(N):
    row = " ".join(f"{columns[f][n]:>+10.4f}" for f in TONES)
    print(f"{n:>2} {t[n]:>7.3f} {row}")

same = all(np.allclose(columns[TONES[0]], columns[f]) for f in TONES)
print(f"\nAre the three sample vectors identical?  {same}")
print("Three different sounds. One set of numbers. The difference is gone.\n")

# --- the folding rule: where does a too-high tone end up? ------------------
print("Folding rule  |f - k*fs|  at telephone rate fs = 8 kHz (Nyquist 4 kHz):\n")
print(f"{'true frequency':>16} {'appears as':>12}   verdict")
print("-" * 46)
for f in [1000, 3000, 5000, 7000, 10000]:
    apparent = sslab.alias_frequency(f, 8000)
    verdict = "correct" if apparent == f else "ALIASED - a lie"
    print(f"{f/1000:>13.0f} kHz {apparent/1000:>9.0f} kHz   {verdict}")

print("""
The fix must come BEFORE the sampler: an analog anti-aliasing (low-pass)
filter that removes everything above the Nyquist frequency while the signal
is still continuous. Filtering afterwards is useless - by then the impostor
is indistinguishable from a genuine low frequency.
""")

# --- the wagon wheel, in numbers -------------------------------------------
print("Bonus - the wagon wheel. Film samples the world 24 times per second:")
for rev_per_s in [12.0, 23.8, 24.0, 25.0]:
    apparent = rev_per_s - 24.0 * round(rev_per_s / 24.0)
    if apparent == 0:
        look = "frozen"
    elif apparent < 0:
        look = f"rolling BACKWARD at {abs(apparent):.1f} rev/s"
    else:
        look = f"forward at {apparent:.1f} rev/s"
    print(f"  wheel truly at {rev_per_s:>5.1f} rev/s  ->  looks {look}")

# ---- optional picture -----------------------------------------------------
plt = sslab.get_pyplot()
if plt:
    t_dense = np.linspace(0, 1, 2000)
    fig, ax = plt.subplots(figsize=(10, 4))
    for f in TONES:
        ax.plot(t_dense, np.cos(2 * np.pi * f * t_dense), linewidth=1, label=f"{f:.0f} Hz")
    ax.plot(t, columns[TONES[0]], "ko", markersize=7,
            label=f"the samples (fs = {FS:.0f} Hz)", zorder=5)
    ax.set_xlabel("time (s)"); ax.set_ylabel("amplitude")
    ax.set_title("Three different waves. One identical set of samples.")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig("assets/demo_02_aliasing.png", dpi=120)
    print("\n[saved] assets/demo_02_aliasing.png")
