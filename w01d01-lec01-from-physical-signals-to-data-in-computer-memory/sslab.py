"""
sslab.py - the tiny toolkit for Lecture 1: Signals & Systems.

Everything in this file is deliberately small enough to read in one sitting.
Nothing here is magic: a signal is a list of numbers, and every function below
does ordinary arithmetic on that list.

Used by the demo scripts (demos/) and by the lab starters (labs/).
Only dependency: numpy.  Plotting is optional (see get_pyplot()).
"""

import numpy as np

# ---------------------------------------------------------------------------
# 1. Making signals
# ---------------------------------------------------------------------------

def sine(freq_hz, duration_s, fs_hz, amplitude=1.0, phase=0.0):
    """Return (t, x): a sampled sine wave.

    freq_hz     : frequency of the tone, in hertz
    duration_s  : how long the signal lasts, in seconds
    fs_hz       : sampling rate - how many measurements per second
    """
    t = np.arange(0.0, duration_s, 1.0 / fs_hz)
    x = amplitude * np.sin(2 * np.pi * freq_hz * t + phase)
    return t, x


def cosine(freq_hz, duration_s, fs_hz, amplitude=1.0):
    t = np.arange(0.0, duration_s, 1.0 / fs_hz)
    return t, amplitude * np.cos(2 * np.pi * freq_hz * t)


# ---------------------------------------------------------------------------
# 2. Sampling (making TIME discrete) and its consequences
# ---------------------------------------------------------------------------

def nyquist_frequency(fs_hz):
    """The highest frequency a sampling rate fs can faithfully capture."""
    return fs_hz / 2.0


def alias_frequency(f_hz, fs_hz):
    """Where a tone at f_hz *appears* to be after sampling at fs_hz.

    The folding rule from the lecture: |f - k*fs| for the integer k that
    brings the result into 0 .. fs/2.
        alias_frequency(6000, 8000) -> 2000.0   (a 6 kHz tone masquerades as 2 kHz)
        alias_frequency(1000, 8000) -> 1000.0   (below Nyquist: unharmed)
    """
    return abs(f_hz - fs_hz * round(f_hz / fs_hz))


def dominant_frequency(x, fs_hz):
    """Strongest frequency present in signal x, found with an FFT.

    This is our 'measuring instrument': it answers 'what note is this?'
    """
    spectrum = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(len(x), d=1.0 / fs_hz)
    spectrum[0] = 0.0  # ignore the DC (0 Hz) bin
    return float(freqs[int(np.argmax(spectrum))])


# ---------------------------------------------------------------------------
# 3. Quantization (making AMPLITUDE discrete)
# ---------------------------------------------------------------------------

def quantize(x, n_bits, v_min=-1.0, v_max=1.0):
    """Round every sample onto one of a finite set of levels.

    Returns (x_quantized, step_size q).  Worst-case error is q/2 - always.
    Values outside [v_min, v_max] are CLIPPED (flattened), exactly as a real
    ADC would clip them.
    """
    q = (v_max - v_min) / (2 ** n_bits)
    x_q = np.round(x / q) * q
    return np.clip(x_q, v_min, v_max), q


def theoretical_snr_db(n_bits):
    """Ideal signal-to-noise ratio of an N-bit quantizer: ~6 dB per bit."""
    return 6.02 * n_bits + 1.76


def snr_db(clean, measured):
    """How many dB the wanted signal stands above the error, 10*log10(P_s/P_n)."""
    noise = np.asarray(measured) - np.asarray(clean)
    power_signal = float(np.sum(np.asarray(clean) ** 2))
    power_noise = float(np.sum(noise ** 2))
    if power_noise == 0.0:
        return float("inf")
    return 10.0 * np.log10(power_signal / power_noise)


def dither(x, q, rng=None):
    """Add a tiny random noise BEFORE quantizing (one step wide, peak-to-peak).

    Counter-intuitive but real: this trades ugly distortion for benign hiss.
    """
    rng = rng or np.random.default_rng(0)
    return x + rng.uniform(-q / 2, q / 2, size=len(x))


# ---------------------------------------------------------------------------
# 4. Processing = arithmetic on the list of numbers
# ---------------------------------------------------------------------------

def moving_average(x, n_taps):
    """The simplest filter there is: replace each sample by the average of its
    n_taps neighbours.  Use an ODD number of taps so the output is not delayed.

    Its frequency response has a null at fs/n_taps - which is how we delete an
    unwanted tone in demo_04.
    """
    if n_taps % 2 == 0:
        raise ValueError("use an odd number of taps so the output stays aligned")
    kernel = np.ones(n_taps) / n_taps
    return np.convolve(x, kernel, mode="same")


def amplify(x, gain):
    """'Louder' is one multiplication."""
    return x * gain


# ---------------------------------------------------------------------------
# 5. Back to the analog world
# ---------------------------------------------------------------------------

def reconstruct(t_samples, x_samples, t_dense):
    """Stand-in for the DAC + reconstruction filter: join the dots.

    Linear interpolation is a crude reconstruction filter, but it is enough to
    see when reconstruction is faithful and when it confidently lies.
    """
    return np.interp(t_dense, t_samples, x_samples)


# ---------------------------------------------------------------------------
# 6. The cost: how big is this going to be?
# ---------------------------------------------------------------------------

def data_rate_bits_per_s(fs_hz, n_bits, channels=1):
    """Raw data rate = rate x bit depth x channels.  Decided at the sensor."""
    return fs_hz * n_bits * channels


def bytes_for_duration(fs_hz, n_bits, channels, duration_s):
    return data_rate_bits_per_s(fs_hz, n_bits, channels) * duration_s / 8.0


def human_bytes(n):
    """1234567 -> '1.23 MB'.

    Decimal units (1 MB = 1,000,000 bytes), the convention used by storage
    makers and by the lecture's table. Your operating system may instead show
    binary units (1 MiB = 1,048,576 bytes) - which is why a "32 GB" stick
    reports as 29.8 GB.
    """
    for unit in ("B", "kB", "MB", "GB", "TB"):
        if abs(n) < 1000.0 or unit == "TB":
            return f"{n:.2f} {unit}"
        n /= 1000.0


# ---------------------------------------------------------------------------
# 7. Plotting is optional - the numbers are the lesson
# ---------------------------------------------------------------------------

def get_pyplot():
    """Return matplotlib.pyplot, or None with a friendly hint if not installed."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # write PNG files; no window needed
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        print("[note] matplotlib is not installed, so no figure was saved.")
        print("       Install it with:  pip install matplotlib")
        return None
