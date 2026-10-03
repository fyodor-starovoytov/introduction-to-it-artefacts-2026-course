"""
Demo 4 - The whole loop, live: cleaning a signal with arithmetic. (Section 3.3)

This is the entire lecture in one runnable experiment:

    analog in -> [anti-alias] -> sample -> quantize -> PROCESS -> DAC -> analog out

A wanted 50 Hz tone is contaminated by a 3 kHz whine. We digitize it, delete
the whine with nothing but arithmetic - a 5-tap moving average - and rebuild
an analog-style output. No hardware. No soldering iron. Five lines of code.

Reproduces the numbers printed in the lecture (section 3.3).
Run:  python demo_04_full_chain.py
"""

import numpy as np
import sslab

# --- parameters ------------------------------------------------------------
WANTED_HZ, WANTED_AMP = 50.0, 0.8        # the signal we care about
NOISE_HZ, NOISE_AMP = 3000.0, 0.15       # the interference we do not
FS = 15000                               # sampling rate of our ADC
N_BITS = 8                               # quantizer resolution
TAPS = 5                                 # moving-average length
DURATION = 0.1
FS_ANALOG = 120000                       # dense grid standing in for "analog"

# --- 1. the analog world ---------------------------------------------------
t_analog = np.arange(0, DURATION, 1 / FS_ANALOG)
clean_analog = WANTED_AMP * np.sin(2 * np.pi * WANTED_HZ * t_analog)

t = np.arange(0, DURATION, 1 / FS)
clean = WANTED_AMP * np.sin(2 * np.pi * WANTED_HZ * t)
microphone = clean + NOISE_AMP * np.sin(2 * np.pi * NOISE_HZ * t)

print(f"[analog in]  wanted {WANTED_HZ:.0f} Hz (amp {WANTED_AMP}) + "
      f"interference {NOISE_HZ/1000:.0f} kHz (amp {NOISE_AMP})")
snr_in = sslab.snr_db(clean, microphone)
print(f"[analog in]  SNR at the microphone: {snr_in:.1f} dB")

# --- 2. into the digital world: sample, then quantize ----------------------
stored, q = sslab.quantize(microphone, N_BITS)
print(f"[ADC]        fs = {FS} Hz, {N_BITS}-bit quantizer, step q = {q:.6f}")
print(f"[ADC]        first five stored values: "
      f"{np.array2string(stored[:5], precision=4, suppress_small=True)}")
max_q_error = float(np.max(np.abs(stored - microphone)))
print(f"[ADC]        max quantization error: {max_q_error:.6f}  (bound q/2 = {q/2:.6f})")

# --- 3. processing is arithmetic -------------------------------------------
processed = sslab.moving_average(stored, TAPS)
print(f"[DSP]        {TAPS}-tap moving average; frequency response has a null "
      f"at fs/{TAPS} = {FS//TAPS} Hz")

# --- 4. back to the analog world -------------------------------------------
edge = 3                                       # skip the filter's edge samples
out_analog = sslab.reconstruct(t[edge:-edge], processed[edge:-edge], t_analog)
inside = (t_analog >= t[edge]) & (t_analog <= t[-edge - 1])

snr_out = sslab.snr_db(clean_analog[inside], out_analog[inside])
residual = float(np.max(np.abs(out_analog[inside] - clean_analog[inside])))
print(f"[out]        SNR after the whole chain (vs the clean {WANTED_HZ:.0f} Hz tone): {snr_out:.1f} dB")
print(f"[out]        improvement over the analog input: {snr_out - snr_in:.1f} dB")
print(f"[out]        max residual error: {residual:.4f}")

print(f"""
Read what happened. The microphone heard a signal only {snr_in:.1f} dB above its
interference. After sampling, quantizing to {N_BITS} bits (measured error inside the
theoretical bound q/2), a five-line averaging computation, and reconstruction,
the output is {snr_out:.1f} dB clean - an improvement of {snr_out - snr_in:.0f} dB, meaning the
interference power was cut by a factor of about {10 ** ((snr_out - snr_in) / 10):,.0f}.

That is why we digitize.
""")

# ---- optional picture -----------------------------------------------------
plt = sslab.get_pyplot()
if plt:
    show = t_analog <= 0.04
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t[t <= 0.04], microphone[t <= 0.04], linewidth=0.8, label="contaminated input")
    ax.plot(t_analog[show], clean_analog[show], linewidth=1.5, label="wanted 50 Hz tone")
    ax.plot(t_analog[show], out_analog[show], "--", linewidth=1.2, label="recovered output")
    ax.set_xlabel("time (s)"); ax.set_ylabel("amplitude")
    ax.set_title("Interference removed by arithmetic alone")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("assets/demo_04_full_chain.png", dpi=120)
    print("[saved] assets/demo_04_full_chain.png")
