"""
Demo 7 - The same loop, in pictures.

    the world -> sample (pixels) -> quantize (levels) -> process -> reconstruct

Sound is sampled in time. An image is sampled in SPACE, on a grid of pixels.
Every idea from the lecture survives the move, and two of them become things
you can simply look at:

    aliasing     -> moire, the false pattern on a striped shirt on television
    quantization -> banding, the stripes across a smooth sky

Run on the built-in test pictures:

    python demo_07_image_pipeline.py

Run on YOUR OWN phone photo (this is the interesting version):

    python demo_07_image_pipeline.py my_photo.jpg

Every output picture is written into assets/ - open them and look. The numbers
matter, but this is the one demo where your eyes are the instrument.
"""

import os
import sys

import numpy as np
import sslab
import imlab

os.makedirs("assets", exist_ok=True)

FACTOR = 4          # we will sample every 4th pixel
BITS = 3            # and squeeze each pixel down to 8 levels


def report(label, value):
    print(f"  {label:<50}{value}")


# ===========================================================================
# 0. Where the picture comes from
# ===========================================================================
photo_path = sys.argv[1] if len(sys.argv) > 1 else None

print("=" * 72)
print("STEP 0 - the picture, and what the camera already decided")
print("=" * 72)

if photo_path:
    info = imlab.image_info(photo_path)
    print(f"\n  your photo: {photo_path}\n")
    report("pixels", f"{info['width']} x {info['height']}")
    report("that is", f"{info['megapixels']:.1f} megapixels")
    report("raw, uncompressed (w x h x 3 channels x 8 bits)", f"{info['raw_bytes']/1e6:.2f} MB")
    report(f"actually on disk as {info['format']}", f"{info['file_bytes']/1e6:.2f} MB")
    report("compression ratio", f"{info['compression_ratio']:.1f}x smaller")

    details = imlab.camera_details(photo_path)
    if details:
        print()
        for key, value in details.items():
            report(key, value)
        if details.get("has_gps_data"):
            print("\n  Note: this file carries GPS data - the place it was taken is")
            print("  inside the picture file. A photo is never only pixels.")

    original = imlab.load_image(photo_path, max_side=512, grey=True)
    print(f"\n  (shrunk to {original.shape[1]} x {original.shape[0]} greyscale so the "
          f"experiment runs fast;")
    print("   that shrink used an anti-aliasing filter, as it must)")
else:
    original = imlab.photo_like(512)
    print("\n  no photo given, so using a synthetic stand-in.")
    print("  Re-run with your own:  python demo_07_image_pipeline.py my_photo.jpg")
    raw = imlab.raw_bytes(512, 512, channels=1)
    print()
    report("pixels", f"{original.shape[1]} x {original.shape[0]} greyscale")
    report("raw, uncompressed", f"{raw/1e6:.2f} MB")

height, width = original.shape

# Make the image dimensions divisible by the sampling factor.
# This avoids a 1-pixel mismatch when comparing downsampled images.
height = (height // FACTOR) * FACTOR
width = (width // FACTOR) * FACTOR
original = original[:height, :width]

imlab.save_image("assets/img_00_original.png", original)


# ===========================================================================
# 1. SAMPLING in space - and why the filter must come first
# ===========================================================================
print("\n" + "=" * 72)
print(f"STEP 1 - sampling: keep every {FACTOR}th pixel")
print("=" * 72)

naive = imlab.downsample(original, FACTOR, prefilter=False)
filtered = imlab.downsample(original, FACTOR, prefilter=True)
truth = imlab.reference_downsample(original, FACTOR)

print(f"\n  {width} x {height}  ->  {naive.shape[1]} x {naive.shape[0]} pixels\n")
report("no anti-aliasing filter, measured against truth", f"{imlab.psnr(truth, naive):.1f} dB")
report("with the filter applied first", f"{imlab.psnr(truth, filtered):.1f} dB")
report("difference caused purely by the ORDER", f"{imlab.psnr(truth, filtered) - imlab.psnr(truth, naive):.1f} dB")

imlab.save_image("assets/img_01_sampled_no_filter.png", imlab.upsample_nearest(naive, FACTOR))
imlab.save_image("assets/img_01_sampled_with_filter.png", imlab.upsample_nearest(filtered, FACTOR))

print("""
  Both pictures threw away the same 15 out of every 16 pixels. Only the ORDER
  differed: one averaged the neighbourhood before sampling, the other just
  grabbed pixels. Open the two files and compare the fine detail.""")

# ---------------------------------------------------------------------------
# The same thing again, on a pattern where we can PREDICT the damage exactly.
# ---------------------------------------------------------------------------
PERIODS = (16, 10, 8, 6, 5)          # pixels per stripe, coarse to fine
chart = imlab.stripe_chart(512, PERIODS)
chart_naive = imlab.downsample(chart, FACTOR)
chart_filtered = imlab.downsample(chart, FACTOR, prefilter=True)

imlab.save_image("assets/img_02_stripes_original.png", chart)
imlab.save_image("assets/img_02_stripes_no_filter.png",
                 imlab.upsample_nearest(chart_naive, FACTOR))
imlab.save_image("assets/img_02_stripes_with_filter.png",
                 imlab.upsample_nearest(chart_filtered, FACTOR))

print("\n  Now a chart of stripes, from coarse to fine, sampled the same two ways.")
print("  Sampling every 4th pixel is a 'sampling rate' of 1/4 cycle per pixel,")
print(f"  so the Nyquist limit is one cycle every {2*FACTOR} pixels.\n")
print(f"{'stripes':>9} {'folding rule':>14} {'measured':>10} {'left by filter':>16}   verdict")
print("-" * 78)

band = 512 // len(PERIODS)
for i, period in enumerate(PERIODS):
    row = (i * band + band // 2) // FACTOR
    measured = imlab.dominant_period(chart_naive[row]) * FACTOR

    # the SAME folding rule as the audio lecture - frequency is now per pixel
    alias = sslab.alias_frequency(1.0 / period, 1.0 / FACTOR)
    predicted = 1.0 / alias if alias else float("inf")
    survives = float(np.ptp(chart_filtered[row]))     # contrast, 0 = flat grey

    verdict = ("recorded correctly" if period >= 2 * FACTOR
               else f"FALSE {predicted:.0f} px stripes - never there")
    print(f"{period:>6} px {predicted:>11.0f} px {measured:>7.0f} px "
          f"{survives:>15.2f}   {verdict}")

print(f"""
  Look at the last two rows. Stripes {PERIODS[-2]} and {PERIODS[-1]} pixels apart are finer than this
  grid can record, so they do not blur away - they come back as WIDE stripes,
  {1/sslab.alias_frequency(1/PERIODS[-2], 1/FACTOR):.0f} and {1/sslab.alias_frequency(1/PERIODS[-1], 1/FACTOR):.0f} pixels apart, that were never in front of the camera. The
  prediction came from sslab.alias_frequency - the very same folding rule as
  the audio lecture, because it is the very same theorem. Only the axis
  changed: cycles per second became cycles per pixel.

  In the filtered version those same bands fade towards flat grey. That is the
  honest answer: detail too fine to record becomes NOTHING, rather than
  something false. Compare assets/img_02_stripes_no_filter.png with
  assets/img_02_stripes_with_filter.png and you have seen the whole of
  section 2.3 with your own eyes.""")

# ===========================================================================
# 2. QUANTIZATION - fewer levels per pixel
# ===========================================================================
print("\n" + "=" * 72)
print("STEP 2 - quantization: fewer levels per pixel")
print("=" * 72)
print()
print(f"{'bits':>6} {'levels':>8} {'PSNR':>10}   what you will see")
print("-" * 58)
for bits in (8, 5, 4, 3, 2):
    q = imlab.quantize_image(original, bits)
    note = {8: "the original (photos are already 8-bit)",
            5: "still hard to fault",
            4: "banding starts in smooth areas",
            3: "obvious stripes across the gradient",
            2: "a poster, not a photograph"}[bits]
    print(f"{bits:>6} {2**bits:>8} {imlab.psnr_text(original, q):>12}   {note}")
    imlab.save_image(f"assets/img_03_quantized_{bits}bit.png", q)

plain = imlab.quantize_image(original, BITS)
dithered = imlab.dither_image(original, BITS)
imlab.save_image(f"assets/img_04_dithered_{BITS}bit.png", dithered)

print(f"\n  Dither, at {BITS} bits:")
report("plain rounding", f"{imlab.psnr(original, plain):.1f} dB")
report("with dither added before quantizing", f"{imlab.psnr(original, dithered):.1f} dB")
print("""
  Read that carefully: dither scores WORSE on the number and looks BETTER to
  the eye. It replaces hard-edged bands with fine grain. When a metric and a
  human disagree, the engineer's job is to know which one the product is for.""")

# ===========================================================================
# 3. PROCESSING - still just arithmetic
# ===========================================================================
print("\n" + "=" * 72)
print("STEP 3 - processing: arithmetic on the grid of numbers")
print("=" * 72)

noisy = np.clip(original + np.random.default_rng(0).normal(0, 0.10, original.shape), 0, 1)

imlab.save_image("assets/img_05_noisy.png", noisy)
imlab.save_image("assets/img_06_sharpened.png", imlab.sharpen(original, amount=1.0))
imlab.save_image("assets/img_07_brightened.png", imlab.brighten(original, 1.6))

print()
print("  A grainy photo (the kind a phone takes indoors at night), cleaned up by")
print("  averaging neighbouring pixels - the 2-D twin of demo 4's moving average.")
print()
print(f"{'filter':>28} {'PSNR':>10}   verdict")
print("-" * 62)
print(f"{'noisy input':>28} {imlab.psnr(original, noisy):>9.1f} dB   what the sensor gave us")
best_k, best_psnr = None, -1
for k in (3, 5, 7):
    cleaned = imlab.box_blur(noisy, k)
    score = imlab.psnr(original, cleaned)
    if score > best_psnr:
        best_k, best_psnr = k, score
    gain = score - imlab.psnr(original, noisy)
    verdict = ("clearly better" if gain > 1 else
               "barely worth it" if gain > -1 else
               "WORSE - the filter is eating the picture")
    print(f"{f'{k}x{k} average':>28} {score:>9.1f} dB   {verdict}")
    imlab.save_image(f"assets/img_05_denoised_{k}x{k}.png", cleaned)

print(f"""
  The best of these is the {best_k}x{best_k} average: {best_psnr - imlab.psnr(original, noisy):+.1f} dB, from nothing but
  addition and division. But look down the column - a WIDER filter is not a
  better filter. Past a point it removes the picture along with the grain,
  because the detail you want and the noise you do not now live at the same
  scale. Choosing that width is engineering, and no library chooses it for you.

  Brightening is one multiplication; sharpening is a blur, a subtraction and a
  multiplication. No darkroom, no lens, no hardware - and every one of them can
  be undone by editing a number.""")

# ===========================================================================
# 4. RECONSTRUCTION - back out to something you can look at
# ===========================================================================
print("\n" + "=" * 72)
print("STEP 4 - reconstruction: from the small grid back to a picture")
print("=" * 72)

stair = imlab.upsample_nearest(filtered, FACTOR)
smooth = imlab.upsample_bilinear(filtered, FACTOR)
imlab.save_image("assets/img_08_reconstructed_nearest.png", stair)
imlab.save_image("assets/img_08_reconstructed_bilinear.png", smooth)

print()
report("repeat each pixel (the DAC's staircase)", f"{imlab.psnr(original, stair):.1f} dB")
report("interpolate between them (reconstruction filter)", f"{imlab.psnr(original, smooth):.1f} dB")
print("""
  The two numbers are close - and the two pictures are not. Open them: one is
  built from visible blocks, the other is smooth. This is the DAC staircase and
  the reconstruction filter of section 4.1, in a form you can see. It is also a
  warning about metrics: PSNR barely separates these, your eye separates them
  instantly, and only one of those two is the customer.""")

# ===========================================================================
# 5. THE COST
# ===========================================================================
print("\n" + "=" * 72)
print("STEP 5 - the cost, decided at the sensor")
print("=" * 72)
print()
print(f"{'version':>34} {'pixels':>13} {'raw size':>12}")
print("-" * 62)
for label, arr in (("original", original), (f"sampled 1-in-{FACTOR}", filtered)):
    h, w = arr.shape
    print(f"{label:>34} {f'{w} x {h}':>13} {imlab.raw_bytes(w, h, 1)/1e6:>10.2f} MB")

print(f"""
  Sampling {FACTOR}x coarser in BOTH directions divides the data by {FACTOR**2}, because an
  image is sampled in two dimensions at once. That is why a phone photo is
  measured in megapixels and a video in gigabits per second - and why every
  streaming service on earth exists to cope with the number.

  All output pictures are in assets/img_*.png - go and look at them.""")
