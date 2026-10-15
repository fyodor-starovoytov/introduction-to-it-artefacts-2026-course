"""
Demo 6 - The cost: data volume is decided at digitization.   (Part 5)

Every byte your software will ever store, move or pay for was fixed back at
the sensor by two choices: how often to sample, and how many bits per sample.
This script recomputes the lecture's table from first principles.

Run:  python demo_06_data_rates.py
"""

import sslab

# name, sampling rate (Hz), bits per sample, channels
SOURCES = [
    ("Telephone (G.711)", 8_000, 8, 1),
    ("CD audio", 44_100, 16, 2),
    ("Studio audio", 48_000, 24, 2),
    ("12-lead ECG", 500, 12, 12),
]

print("Audio-style sources - rate x bit depth x channels:\n")
print(f"{'source':>20} {'kbit/s':>10} {'per minute':>14} {'per hour':>12}")
print("-" * 60)
for name, fs, bits, ch in SOURCES:
    rate = sslab.data_rate_bits_per_s(fs, bits, ch)
    print(f"{name:>20} {rate/1000:>10,.1f} "
          f"{sslab.human_bytes(rate * 60 / 8):>14} {sslab.human_bytes(rate * 3600 / 8):>12}")

# --- images and video: sampling in SPACE as well as time -------------------
print("\nImages and video - the same arithmetic, with pixels as the samples:\n")

photo_bytes = 4000 * 3000 * 3          # width x height x 3 colours x 8 bits
print(f"  photo 4000 x 3000, 3 x 8-bit colour : {sslab.human_bytes(photo_bytes)} uncompressed")
print(f"                                        (JPEG typically stores a few MB)")

video_rate_bits = 1920 * 1080 * 3 * 8 * 30
print(f"  1080p video, 30 frames per second   : {video_rate_bits/1e9:.2f} Gbit/s raw")
print(f"  a 2-hour film at that raw rate      : {sslab.human_bytes(video_rate_bits * 7200 / 8)}")

# --- one concrete song ------------------------------------------------------
song_s = 180
cd_bits = sslab.data_rate_bits_per_s(44_100, 16, 2)
mp3_bits = 128_000
print(f"\nA 3-minute song:")
print(f"  as raw CD audio : {sslab.human_bytes(cd_bits * song_s / 8)}")
print(f"  as a 128 kbit/s MP3 : {sslab.human_bytes(mp3_bits * song_s / 8)} "
      f"- about {cd_bits/mp3_bits:.0f}x smaller")

print("""
Every row is a trade. More bits and faster sampling mean better data and a
higher bill in storage, bandwidth and energy. Raw 1080p is never sent to your
home because 1.49 Gbit/s dwarfs a home connection - and that number was not
decided by the network. It was decided at the sensor.
""")
