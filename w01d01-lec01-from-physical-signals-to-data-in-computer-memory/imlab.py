"""
imlab.py - the same lecture, one dimension further: images.

A sound is a list of numbers, sampled in TIME.
An image is a grid of numbers, sampled in SPACE.

Every function here has a twin in sslab.py, and that is the point:

    sslab.sine / sslab.quantize   ->  imlab.load_image / imlab.quantize_image
    sslab.moving_average          ->  imlab.box_blur       (an average, but 2-D)
    sslab.reconstruct             ->  imlab.upsample_bilinear
    sslab.alias_frequency         ->  moire, which you will see rather than compute
    sslab.snr_db                  ->  imlab.psnr

Images are stored as numpy arrays of floats between 0.0 (black) and 1.0 (white),
with shape (height, width) for grey or (height, width, 3) for colour.

Needs numpy and Pillow:  pip install numpy pillow
"""

import os

import numpy as np

try:
    from PIL import Image
    HAVE_PILLOW = True
except ImportError:                                   # keep the import optional
    HAVE_PILLOW = False


def _require_pillow():
    if not HAVE_PILLOW:
        raise ImportError("this needs Pillow - install it with:  pip install pillow")


# ---------------------------------------------------------------------------
# 1. Getting a photo in and out
# ---------------------------------------------------------------------------

def load_image(path, max_side=None, grey=False):
    """Read an image file into an array of floats between 0 and 1.

    max_side : shrink the picture so its longest side is at most this many
               pixels. Phone photos are 12 megapixels or more, which makes
               every experiment slow for no extra insight. The shrink uses an
               anti-aliasing filter (section 2.3) - as it must.
    """
    _require_pillow()
    img = Image.open(path)
    img = img.convert("L" if grey else "RGB")

    if max_side and max(img.size) > max_side:
        factor = max(img.size) / max_side
        new_size = (max(1, round(img.width / factor)), max(1, round(img.height / factor)))
        img = img.resize(new_size, Image.LANCZOS)     # a proper low-pass filter

    return np.asarray(img, dtype=np.float64) / 255.0


def save_image(path, img):
    """Write an array of floats (0..1) back to an image file."""
    _require_pillow()
    clipped = np.clip(img, 0.0, 1.0)
    Image.fromarray(np.round(clipped * 255).astype(np.uint8)).save(path)
    return path


def image_info(path):
    """What the camera decided, and what it cost. Section 5, on your own photo."""
    _require_pillow()
    img = Image.open(path)
    width, height = img.size
    channels = len(img.getbands())
    raw = width * height * channels          # 8 bits per channel, uncompressed
    on_disk = os.path.getsize(path)

    return {
        "path": path,
        "width": width,
        "height": height,
        "channels": channels,
        "megapixels": width * height / 1e6,
        "raw_bytes": raw,
        "file_bytes": on_disk,
        "compression_ratio": raw / on_disk if on_disk else float("nan"),
        "format": img.format,
    }


def camera_details(path):
    """A few EXIF fields, if the phone left any. Returns a plain dict.

    Note for the report: EXIF often also carries GPS coordinates - where the
    photo was taken, to a few metres. That is a privacy question you will meet
    properly in the security lecture; for now, just notice that a photo is
    never only pixels.
    """
    _require_pillow()
    try:
        exif = Image.open(path).getexif() or {}
    except Exception:                                  # noqa: BLE001
        return {}

    wanted = {271: "camera_make", 272: "camera_model", 306: "taken_at",
              33434: "exposure_time", 33437: "f_number", 34855: "iso"}
    found = {name: exif[tag] for tag, name in wanted.items() if tag in exif}
    if found or 34853 in exif:
        found["has_gps_data"] = 34853 in exif
    return found          # empty dict = the file carries no EXIF at all


# ---------------------------------------------------------------------------
# 2. Sampling in SPACE - the pixel grid
# ---------------------------------------------------------------------------

def downsample(img, factor, prefilter=False):
    """Keep every factor-th pixel: sampling, with the pixel grid as the clock.

    prefilter=False : take the pixels as they come. This is sampling with no
                      anti-aliasing filter, and fine detail will fold down into
                      false patterns - moire, the spatial twin of section 2.3.
    prefilter=True  : average the neighbourhood FIRST, then sample. That
                      average is the anti-aliasing filter, and it must happen
                      before the sampler, never after.

    The filter here is a box average applied TWICE. One pass is a crude
    low-pass filter that lets a lot of fine detail through; two passes suppress
    it far better. Even this is worse than a properly designed filter (compare
    reference_downsample) - which is exactly why a real converter has a
    carefully designed analog filter in front of it, and why the CD's sampling
    rate leaves a 2 kHz guard band for that filter to work in.
    """
    if prefilter:
        k = factor + 1 if factor % 2 == 0 else factor
        img = box_blur(box_blur(img, k), k)
    return img[::factor, ::factor]


def upsample_nearest(img, factor):
    """Repeat each pixel factor times: the staircase a DAC makes (section 4.1)."""
    return np.repeat(np.repeat(img, factor, axis=0), factor, axis=1)


def upsample_bilinear(img, factor):
    """Join the dots in 2-D: linear interpolation along x, then along y.

    This is exactly sslab.reconstruct() - the reconstruction filter - applied
    once per axis. Compare it with upsample_nearest to see what the filter
    after the DAC is actually for.
    """
    out = _interp_axis(img, factor, axis=0)
    return _interp_axis(out, factor, axis=1)


def _interp_axis(a, factor, axis):
    """Linear interpolation along one axis, by an integer factor."""
    n = a.shape[axis]
    # where each new sample sits in old-pixel coordinates (pixel centres)
    src = (np.arange(n * factor) + 0.5) / factor - 0.5
    src = np.clip(src, 0, n - 1)
    lo = np.floor(src).astype(int)
    hi = np.minimum(lo + 1, n - 1)

    shape = [1] * a.ndim
    shape[axis] = n * factor
    w = (src - lo).reshape(shape)                     # how far between lo and hi

    return (1 - w) * np.take(a, lo, axis=axis) + w * np.take(a, hi, axis=axis)


# ---------------------------------------------------------------------------
# 3. Quantization - fewer levels per pixel
# ---------------------------------------------------------------------------

def quantize_image(img, n_bits):
    """Round every pixel onto one of 2**n_bits levels between 0 and 1.

    A normal photo already is quantized: 8 bits per channel, 256 levels. Drop
    to 4 or 3 and you will see BANDING - smooth skies breaking into stripes.
    That is section 2.4, visible instead of audible.
    """
    levels = 2 ** n_bits
    step = 1.0 / (levels - 1)
    return np.round(img / step) * step


def dither_image(img, n_bits, rng=None):
    """Add a little noise BEFORE quantizing, then quantize.

    Same counter-intuitive trick as in audio: it trades hard-edged bands for
    fine grain, which the eye finds far less objectionable.
    """
    rng = rng or np.random.default_rng(0)
    step = 1.0 / (2 ** n_bits - 1)
    noisy = img + rng.uniform(-step / 2, step / 2, size=img.shape)
    return quantize_image(np.clip(noisy, 0, 1), n_bits)


# ---------------------------------------------------------------------------
# 4. Processing = arithmetic, still
# ---------------------------------------------------------------------------

def box_blur(img, k):
    """Replace each pixel by the average of the k x k block around it.

    The 2-D twin of sslab.moving_average: same idea, one more dimension. Use an
    odd k so the result does not shift.
    """
    if k <= 1:
        return img.copy()
    if k % 2 == 0:
        k += 1
    pad = k // 2
    widths = [(pad, pad), (pad, pad)] + [(0, 0)] * (img.ndim - 2)
    padded = np.pad(img, widths, mode="edge")

    total = np.zeros_like(img, dtype=np.float64)
    for dy in range(k):
        for dx in range(k):
            total += padded[dy:dy + img.shape[0], dx:dx + img.shape[1]]
    return total / (k * k)


def sharpen(img, amount=1.0, k=5):
    """Unsharp mask: original + amount x (original - blurred).

    Three operations - a blur, a subtraction, a multiplication. No lens, no
    hardware, and it can be undone by editing a number.
    """
    return np.clip(img + amount * (img - box_blur(img, k)), 0.0, 1.0)


def brighten(img, gain):
    """Louder, for light. Values above 1.0 clip exactly as loud audio does."""
    return np.clip(img * gain, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 5. Measuring what happened
# ---------------------------------------------------------------------------

def mse(a, b):
    """Mean squared error between two images of the same shape."""
    return float(np.mean((np.asarray(a) - np.asarray(b)) ** 2))


def psnr(original, processed):
    """Peak signal-to-noise ratio in dB - the standard image quality number.

    Same idea as sslab.snr_db: how far the picture stands above the error.
    Rules of thumb: above 40 dB is hard to see, below 25 dB is obvious damage.
    """
    error = mse(original, processed)
    if error == 0:
        return float("inf")
    return 10.0 * np.log10(1.0 / error)               # peak value is 1.0 here


def psnr_text(original, processed):
    """PSNR as a printable string, honest about the boring case.

    A photo loaded from a file is ALREADY quantized to 8 bits, so quantizing it
    to 8 bits again changes nothing at all and the PSNR shoots off to a silly
    number. That is not a triumph, it is a no-op, and it should say so.
    """
    value = psnr(original, processed)
    return "unchanged" if value > 100 else f"{value:.1f} dB"


def raw_bytes(width, height, channels=3, bits_per_channel=8):
    """What the picture would weigh with nothing thrown away."""
    return width * height * channels * bits_per_channel / 8


# ---------------------------------------------------------------------------
# 6. Test pictures, for when you have no photo yet
# ---------------------------------------------------------------------------

def zone_plate(size=720, strength=0.00055):
    """Rings that get finer towards the edges: a moire machine.

    Detail grows finer the further out you look, so any sampling rate is fine
    in the middle and too slow further out. Downsample this without a
    prefilter and the false patterns are unmissable.
    """
    y, x = np.mgrid[-size // 2:size // 2, -size // 2:size // 2]
    return 0.5 + 0.5 * np.cos(strength * (x ** 2 + y ** 2) * np.pi)


def stripe_chart(size=512, periods=(16, 10, 8, 6, 5)):
    """Bands of vertical stripes, each band finer than the one above it.

    This is the clearest aliasing demonstration in the whole course. Sample it
    every 4th pixel with no filter and the fine bands do not merely blur - they
    come back as WIDE stripes that were never there, at exactly the spacing the
    folding rule predicts. Sample it with a filter first, and the too-fine
    bands honestly become flat grey: nothing, rather than something false.

    periods are in pixels per stripe cycle.
    """
    _, x = np.mgrid[0:size, 0:size]
    img = np.zeros((size, size))
    band = size // len(periods)
    for i, period in enumerate(periods):
        top = i * band
        bottom = size if i == len(periods) - 1 else (i + 1) * band
        img[top:bottom] = 0.5 + 0.5 * np.cos(2 * np.pi * x[top:bottom] / period)
    return img


def dominant_period(row):
    """The strongest stripe spacing in a 1-D slice, in pixels per cycle.

    The image twin of sslab.dominant_frequency: same FFT, same idea, except
    the axis is space rather than time.
    """
    row = np.asarray(row, dtype=float)
    spectrum = np.abs(np.fft.rfft(row - row.mean()))
    cycles = int(np.argmax(spectrum))
    return len(row) / cycles if cycles else float("inf")


def gradient_ramp(width=720, height=240):
    """A perfectly smooth ramp from black to white: a banding detector."""
    return np.tile(np.linspace(0, 1, width), (height, 1))


def photo_like(size=512, seed=1):
    """A synthetic stand-in for a photograph, for when you have none to hand.

    Real photographs have most of their energy at coarse scales and less at
    fine ones, plus a few hard edges. This fakes that, and adds one patch of
    very fine stripes - the shirt that shimmers on television.
    """
    rng = np.random.default_rng(seed)
    freqs = np.fft.fftfreq(size)
    fx, fy = np.meshgrid(freqs, freqs)
    radius = np.sqrt(fx ** 2 + fy ** 2)
    radius[0, 0] = 1e-6
    spectrum = (rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))) / radius ** 1.2

    img = np.real(np.fft.ifft2(spectrum))
    img = (img - img.min()) / np.ptp(img)
    img = 0.7 * img + 0.3 * np.tile(np.linspace(0, 1, size), (size, 1))   # a smooth sky
    img[size // 5:size // 5 + 100, size // 5:size // 5 + 100] = 0.9       # a flat wall

    _, x = np.mgrid[0:size, 0:size]
    patch = (slice(3 * size // 5, 3 * size // 5 + 120), slice(3 * size // 5, 3 * size // 5 + 160))
    img[patch] = 0.5 + 0.5 * np.cos(1.2 * x[patch])                       # the fine shirt
    return np.clip(img, 0.0, 1.0)


def reference_downsample(img, factor):
    """A careful shrink, used as the truth to measure your own shrink against.

    Pillow's LANCZOS filter low-passes properly before it samples. It is what a
    good tool does, and comparing your own downsampling to it is how you put a
    number on aliasing instead of arguing about pictures.
    """
    _require_pillow()
    grey = img.ndim == 2
    pil = Image.fromarray(np.round(np.clip(img, 0, 1) * 255).astype(np.uint8))
    small = pil.resize((img.shape[1] // factor, img.shape[0] // factor), Image.LANCZOS)
    out = np.asarray(small, dtype=np.float64) / 255.0
    return out if grey else out.reshape(small.size[1], small.size[0], -1)
