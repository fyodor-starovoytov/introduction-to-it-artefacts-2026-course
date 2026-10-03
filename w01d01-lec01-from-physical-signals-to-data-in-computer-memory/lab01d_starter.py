"""
LAB 1D - "Your own photo, through the whole loop"   (optional; 1-2 hours)

    your phone -> sample -> quantize -> process -> reconstruct -> your screen

Everything you did to a sound in Labs 1A-1C, done to a picture you took
yourself. It is the same theorem; only the axis changed, from cycles per
second to cycles per pixel.

HOW TO GET A PHOTO ONTO YOUR COMPUTER
  - email or message it to yourself, or
  - plug the phone in with a cable and copy it, or
  - use your cloud photo library and download one file.
  Then save it next to this script and put its name in PHOTO below.

  Take a photo with FINE REPEATING DETAIL in it: a brick wall, a striped
  shirt, a radiator, a keyboard, a distant fence, a tiled floor. That detail
  is what will misbehave, which is the whole point.

  Your photo never leaves your computer. Nothing here uploads anything.

Run:  python lab01d_starter.py

Deliverables: this file completed, lab01d_report.md with your pictures, AI-log.md
"""

import os

import numpy as np
import imlab

# TODO 0: put your own photo's filename here. Leave it as None to use the
#         built-in test picture (fine for a first run, but do use your own).
PHOTO = None                    # e.g. "my_photo.jpg"

os.makedirs("assets/lab01d", exist_ok=True)


def out(name):
    return os.path.join("assets", "lab01d", name)


# ===========================================================================
# TASK 1 - what your camera already decided
# ===========================================================================
print("=" * 70)
print("TASK 1 - your photo, before you touch it")
print("=" * 70)

if PHOTO:
    info = imlab.image_info(PHOTO)
    print(f"\n  {info['width']} x {info['height']} pixels = {info['megapixels']:.1f} megapixels")
    print(f"  raw (w x h x {info['channels']} channels x 8 bits) : {info['raw_bytes']/1e6:>8.2f} MB")
    print(f"  actually on disk as {info['format']:<16}: {info['file_bytes']/1e6:>8.2f} MB")
    print(f"  compression ratio                    : {info['compression_ratio']:>8.1f}x")

    details = imlab.camera_details(PHOTO)
    if details:
        print(f"\n  the file also remembers: {details}")

    original = imlab.load_image(PHOTO, max_side=512, grey=True)
else:
    print("\n  (no photo set - using the built-in test picture)")
    print("  Set PHOTO at the top of this file to your own photo.")
    original = imlab.photo_like(512)

imlab.save_image(out("00_original.png"), original)
print(f"\n  working with {original.shape[1]} x {original.shape[0]} greyscale pixels")

# TODO 1: compute, by hand in your report, how many bytes your photo would take
#         with NOTHING thrown away, and how many it actually takes on disk.
#         Where did the difference go, and what was traded away to get it?

# ===========================================================================
# TASK 2 - sampling in space, with and without the filter
# ===========================================================================
print("\n" + "=" * 70)
print("TASK 2 - throw pixels away, two different ways")
print("=" * 70)

# TODO 2a: choose how much coarser to sample. Start with 4, then try 8.
FACTOR = 0                      # <-- e.g. 4

if FACTOR > 1:
    naive = imlab.downsample(original, FACTOR, prefilter=False)
    filtered = imlab.downsample(original, FACTOR, prefilter=True)
    truth = imlab.reference_downsample(original, FACTOR)

    imlab.save_image(out("01_no_filter.png"), imlab.upsample_nearest(naive, FACTOR))
    imlab.save_image(out("01_with_filter.png"), imlab.upsample_nearest(filtered, FACTOR))

    print(f"\n  {original.shape[1]} x {original.shape[0]}  ->  {naive.shape[1]} x {naive.shape[0]} pixels")
    print(f"  both versions kept 1 pixel in {FACTOR*FACTOR}. Only the ORDER of filter")
    print("  and sampler differed.\n")
    print(f"  straight to the sampler, no filter : {imlab.psnr(truth, naive):>6.1f} dB")
    print(f"  filter first, then sample          : {imlab.psnr(truth, filtered):>6.1f} dB")

    # TODO 2b: OPEN both saved pictures and look at the fine detail (the bricks,
    #          the stripes, the fence). Describe in your report what appeared in
    #          the unfiltered one that was never in the scene.
    # TODO 2c: why can this not be repaired afterwards? Answer in the report,
    #          referring to the three identical cosines of demo_02.
else:
    print("\n  (set FACTOR first - TODO 2a)")

# ===========================================================================
# TASK 3 - quantization: how few levels can your eye tolerate?
# ===========================================================================
print("\n" + "=" * 70)
print("TASK 3 - fewer levels per pixel")
print("=" * 70)
print()
print(f"{'bits':>6} {'levels':>8} {'PSNR':>10}   file")
print("-" * 56)
for bits in (8, 6, 5, 4, 3, 2):
    q = imlab.quantize_image(original, bits)
    imlab.save_image(out(f"02_quantized_{bits}bit.png"), q)
    print(f"{bits:>6} {2**bits:>8} {imlab.psnr_text(original, q):>12}   "
          f"02_quantized_{bits}bit.png")

# TODO 3a: open those six files in order. At which bit depth do YOU first see
#          banding - stripes across smooth areas that should be smooth?
first_banding_bits = 0          # <-- your answer

# TODO 3b: at that same bit depth, compare plain quantizing with dithering.
#          Which has the better PSNR? Which looks better? Explain the conflict.
if first_banding_bits:
    plain = imlab.quantize_image(original, first_banding_bits)
    dithered = imlab.dither_image(original, first_banding_bits)
    imlab.save_image(out(f"03_plain_{first_banding_bits}bit.png"), plain)
    imlab.save_image(out(f"03_dithered_{first_banding_bits}bit.png"), dithered)
    print(f"\n  at {first_banding_bits} bits:")
    print(f"    plain    : {imlab.psnr(original, plain):>6.1f} dB")
    print(f"    dithered : {imlab.psnr(original, dithered):>6.1f} dB")
else:
    print("\n  (fill in first_banding_bits - TODO 3a)")

# ===========================================================================
# TASK 4 - processing: repair something with arithmetic
# ===========================================================================
print("\n" + "=" * 70)
print("TASK 4 - clean up a grainy picture with nothing but averaging")
print("=" * 70)

noisy = np.clip(original + np.random.default_rng(0).normal(0, 0.10, original.shape), 0, 1)
imlab.save_image(out("04_noisy.png"), noisy)

print(f"\n  noisy input : {imlab.psnr(original, noisy):>6.1f} dB\n")
print(f"{'filter':>16} {'PSNR':>10}")
print("-" * 30)
for k in (3, 5, 7, 9):
    cleaned = imlab.box_blur(noisy, k)
    imlab.save_image(out(f"04_cleaned_{k}x{k}.png"), cleaned)
    print(f"{f'{k}x{k} average':>16} {imlab.psnr(original, cleaned):>9.1f} dB")

# TODO 4: which filter width wins on the number? Which wins when you LOOK at
#         the pictures? Say in your report why a wider filter stops helping.

# ===========================================================================
# TASK 5 - reconstruction: back to something you can look at
# ===========================================================================
print("\n" + "=" * 70)
print("TASK 5 - from the small grid back to a full-size picture")
print("=" * 70)

if FACTOR > 1:
    stair = imlab.upsample_nearest(filtered, FACTOR)
    smooth = imlab.upsample_bilinear(filtered, FACTOR)
    imlab.save_image(out("05_reconstructed_nearest.png"), stair)
    imlab.save_image(out("05_reconstructed_bilinear.png"), smooth)

    print(f"\n  repeat each pixel (the DAC staircase)   : {imlab.psnr(original, stair):>6.1f} dB")
    print(f"  interpolate (the reconstruction filter) : {imlab.psnr(original, smooth):>6.1f} dB")

    # TODO 5: the two numbers are close. Open the two pictures - are they close?
    #         What does that tell you about trusting a single number?
else:
    print("\n  (needs FACTOR from TASK 2)")

# ===========================================================================
# SELF-CHECK
# ===========================================================================
print("\n" + "=" * 70)
print("SELF-CHECK")
print("=" * 70)

checks = [("a photo of your own is set (not the built-in picture)", PHOTO is not None),
          ("TASK 2: a sampling factor is chosen", FACTOR > 1)]
if FACTOR > 1:
    checks.append(("TASK 2: filtering first really did score higher",
                   imlab.psnr(truth, filtered) > imlab.psnr(truth, naive)))
checks.append(("TASK 3: you decided where banding starts", first_banding_bits > 0))

for label, passed in checks:
    print(f"  [{'PASS' if passed else 'TODO'}] {label}")
print(f"\n{sum(p for _, p in checks)}/{len(checks)} checks passing.")
print(f"\nAll your pictures are in {out('')} - they belong in your report.")
