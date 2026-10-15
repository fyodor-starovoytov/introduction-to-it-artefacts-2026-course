"""
check_setup.py - run this FIRST, before the lab.   python check_setup.py

It answers one question: can this computer run Lecture 1's code?
Nothing here is graded. If a line says FAIL, fix that line and run it again.
"""

import sys

ok = True


def check(label, passed, hint="", optional=False):
    global ok
    mark = "PASS" if passed else ("SKIP" if optional else "FAIL")
    print(f"  [{mark}] {label}")
    if not passed:
        if not optional:
            ok = False
        if hint:
            print(f"         -> {hint}")


print("Lecture 1 - environment check\n")

check(f"Python {sys.version.split()[0]} (3.10 or newer)",
      sys.version_info >= (3, 10),
      "install a newer Python from python.org")

try:
    import numpy
    check(f"numpy {numpy.__version__}", True)
except ImportError:
    check("numpy", False, "pip install numpy")

try:
    import PIL
    check(f"pillow {PIL.__version__} (needed for the image demo and Lab 1D)", True)
except ImportError:
    check("pillow", False, "pip install pillow")

try:
    import matplotlib
    check(f"matplotlib {matplotlib.__version__}", True)
except ImportError:
    check("matplotlib (optional - only needed for the plots)", False,
          "pip install matplotlib", optional=True)

try:
    import sslab, wavtools, imlab     # noqa: F401
    check("course toolkit (sslab.py, wavtools.py, imlab.py) importable", True)
except ImportError as e:
    check("course toolkit", False, f"run this script from the lec01 folder ({e})")

# One real calculation, so we know the maths works and not just the imports.
try:
    import numpy as np
    import sslab
    x = sslab.sine(1.0, 1.0, 8)[1]
    xq, q = sslab.quantize(x, 3)
    check("arithmetic sanity: 3-bit step is 0.25 and error stays under q/2",
          abs(q - 0.25) < 1e-12 and np.max(np.abs(xq - x)) <= q / 2 + 1e-12)
    check("folding rule: a 6 kHz tone sampled at 8 kHz appears at 2 kHz",
          sslab.alias_frequency(6000, 8000) == 2000)

    import imlab
    tiny = imlab.stripe_chart(64, (16, 8))
    check("images: a picture can be sampled and rebuilt",
          imlab.upsample_bilinear(imlab.downsample(tiny, 4), 4).shape == tiny.shape)
except Exception as e:      # noqa: BLE001
    check("arithmetic sanity", False, str(e))

import os
check("assets/ contains the lab sound files",
      os.path.exists(os.path.join("assets", "tone_a440.wav")),
      "run: python make_assets.py")

print("\n" + ("All good - start with:  python demo_01_sampling.py"
               if ok else "Fix the FAIL lines above, then run this again."))
sys.exit(0 if ok else 1)
