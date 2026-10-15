"""
Demo 3 - Quantization: making AMPLITUDE discrete.   (Section 2.4)

Sampling handled time, and Nyquist promised we could lose nothing. Amplitude
gets no such promise: a real number has infinitely many possible values and
N bits give exactly 2^N levels, so every stored sample is the true value plus
a small unavoidable error - bounded by half a step, q/2.

Run:  python demo_03_quantization.py
"""

import numpy as np
import sslab

# --- Part 1: a 3-bit quantizer, sample by sample ---------------------------
N_BITS = 3
AMPLITUDE = 0.9

t, exact = sslab.sine(1.0, 1.0, fs_hz=8, amplitude=AMPLITUDE)
quantized, q = sslab.quantize(exact, N_BITS)
error = quantized - exact

print(f"A {N_BITS}-bit quantizer over the range -1 .. +1")
print(f"step size q = 2 / 2^{N_BITS} = {q:.4f}   ->   worst-case error q/2 = {q/2:.4f}\n")
print(f"{'t':>7} {'exact':>10} {'quantized':>11} {'error':>10}")
print("-" * 41)
for i in range(len(t)):
    print(f"{t[i]:>7.3f} {exact[i]:>+10.4f} {quantized[i]:>+11.4f} {error[i]:>+10.4f}")

worst = float(np.max(np.abs(error)))
print(f"\nlargest error seen: {worst:.4f}   bound q/2: {q/2:.4f}   within bound: {worst <= q/2 + 1e-12}")

# --- Part 2: more bits = finer steps = better SNR --------------------------
print("\nMore bits, measured against the theory  SNR ~ 6.02*N + 1.76 dB:\n")
print(f"{'bits':>5} {'levels':>12} {'step over +/-1V':>17} {'measured SNR':>14} {'theory':>9}")
print("-" * 62)

# a long, full-scale sine so the measurement is fair
t_long, x_long = sslab.sine(440.0, 1.0, fs_hz=44100, amplitude=1.0)
for n in (4, 8, 12, 16, 24):
    xq, step = sslab.quantize(x_long, n)
    measured = sslab.snr_db(x_long, xq)
    print(f"{n:>5} {2**n:>12,} {step:>16.3e}V {measured:>13.1f} dB {sslab.theoretical_snr_db(n):>8.1f}")

print("""
Each extra bit halves the step and buys about 6 dB. That is why CD audio uses
16 bits (~98 dB spans a quiet room to painful loudness), why cheap 8-bit audio
audibly hisses, and why studios record at 24 bits - not to hear 146 dB, but so
an engineer can set levels conservatively and still have resolution to spare.
""")

# --- Part 3: the two practical traps ---------------------------------------
loud = 1.4 * np.sin(2 * np.pi * np.arange(8) / 8)     # too loud for the range
clipped, _ = sslab.quantize(loud, 8)
print("Trap 1 - CLIPPING. Input beyond the range is flattened at the maximum:")
print("  input :", np.array2string(loud, precision=2, suppress_small=True))
print("  stored:", np.array2string(clipped, precision=2, suppress_small=True))
print("  Clipping is far uglier than quantization noise - hence conservative levels.")

# A signal quieter than half a step disappears completely... unless we add noise.
q8 = 2 / 2 ** 8
_, whisper = sslab.sine(100.0, 0.2, fs_hz=44100, amplitude=0.3 * q8)
plain, _ = sslab.quantize(whisper, 8)
dithered, _ = sslab.quantize(sslab.dither(whisper, q8), 8)
smoothed = sslab.moving_average(dithered, 201)   # what your ear/eye does anyway
edge = 300                                       # ignore the filter's edges
print("")
print("Trap 2 - DITHER. A whisper (amplitude 0.3 x q) into an 8-bit quantizer:")
print(f"  true amplitude                    : {0.3 * q8:.6f}")
print(f"  quantized plainly, peak stored    : {np.max(np.abs(plain)):.6f}   <- the signal VANISHED")
print(f"  dithered then smoothed, peak      : {np.max(np.abs(smoothed[edge:-edge])):.6f}")
print(f"  ...and its correlation with truth : {np.corrcoef(whisper[edge:-edge], smoothed[edge:-edge])[0, 1]:.3f}")
print("  Adding random noise BEFORE quantizing rescued information that rounding")
print("  alone destroyed. One of engineering's genuinely counter-intuitive moves.")

# ---- optional picture -----------------------------------------------------
plt = sslab.get_pyplot()
if plt:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    t_fine = np.linspace(0, 1, 1000)
    ax1.plot(t_fine, AMPLITUDE * np.sin(2 * np.pi * t_fine), linewidth=1,
             label="true amplitude")
    ax1.step(np.append(t, 1.0), np.append(quantized, quantized[-1]), where="post",
             linewidth=1.5, label=f"{N_BITS}-bit quantized")
    ax1.plot(t, exact, "o", markersize=5, label="samples")
    for level in np.arange(-1, 1.01, q):
        ax1.axhline(level, color="0.85", linewidth=0.5, zorder=0)
    ax1.set_xlabel("time (s)"); ax1.set_ylabel("amplitude")
    ax1.set_title(f"{N_BITS} bits: every value forced onto a grid line")
    ax1.legend(fontsize=8)

    bits = np.arange(2, 25)
    measured = [sslab.snr_db(x_long, sslab.quantize(x_long, int(n))[0]) for n in bits]
    ax2.plot(bits, [sslab.theoretical_snr_db(n) for n in bits], linewidth=1.5,
             label="6.02N + 1.76 dB")
    ax2.plot(bits, measured, "o", markersize=4, label="measured")
    ax2.set_xlabel("bits per sample"); ax2.set_ylabel("SNR (dB)")
    ax2.set_title("About 6 dB per bit")
    ax2.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig("assets/demo_03_quantization.png", dpi=120)
    print("\n[saved] assets/demo_03_quantization.png")
