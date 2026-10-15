"""
wavtools.py - read and write .wav files with nothing but the Python standard
library.  A .wav file really is just a 44-byte header followed by the samples.

Used by Lab 1A.  No numpy tricks here; the point is to see the bytes.
"""

import wave
import numpy as np


def read_wav(path):
    """Return (samples as float in -1..+1, info dict).

    Handles 16-bit mono/stereo files, which is what this course provides.
    """
    with wave.open(str(path), "rb") as w:
        info = {
            "channels": w.getnchannels(),
            "sample_width_bytes": w.getsampwidth(),
            "bit_depth": w.getsampwidth() * 8,
            "sample_rate": w.getframerate(),
            "n_frames": w.getnframes(),
            "duration_s": w.getnframes() / w.getframerate(),
        }
        raw = w.readframes(w.getnframes())

    if info["sample_width_bytes"] != 2:
        raise ValueError("this helper only reads 16-bit WAV files")

    ints = np.frombuffer(raw, dtype="<i2")          # signed 16-bit, little-endian
    if info["channels"] > 1:
        ints = ints.reshape(-1, info["channels"])
    return ints.astype(np.float64) / 32768.0, info


def write_wav(path, samples, sample_rate=44100):
    """Write float samples (-1..+1) as a 16-bit mono WAV file.

    Anything outside -1..+1 is CLIPPED, exactly as a real converter would.
    """
    clipped = np.clip(np.asarray(samples), -1.0, 1.0)
    ints = np.round(clipped * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)      # 2 bytes = 16 bits
        w.setframerate(sample_rate)
        w.writeframes(ints.tobytes())
    return path


def expected_size_bytes(sample_rate, bit_depth, channels, duration_s, header_bytes=44):
    """What the file SHOULD weigh: rate x bytes-per-sample x channels x seconds."""
    return sample_rate * (bit_depth // 8) * channels * duration_s + header_bytes
