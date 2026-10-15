"""
Demo 5 - Back to the analog world: when reconstruction is faithful, and when
it confidently lies.   (Section 4.2)

One 3 Hz tone. Three sampling rates. Sample it, then join the dots back up
(linear interpolation is a crude stand-in for the DAC's reconstruction filter)
and ask two questions of the result: what frequency does it have now, and how
far is it from the truth?

Reproduces the numbers printed in the lecture (section 4.2).
Run:  python demo_05_reconstruction.py
"""

import numpy as np
import sslab

TONE_HZ = 3.0
DURATION = 10.0
FS_ANALOG = 1000          # dense grid standing in for the continuous world
RATES = [50, 10, 5]       # well above Nyquist / just above / below

t_analog, x_analog = sslab.sine(TONE_HZ, DURATION, FS_ANALOG)

print(f"{TONE_HZ:.0f} Hz tone, sampled then reconstructed by linear interpolation:")
print(f"(Nyquist requires fs > {2 * TONE_HZ:.0f} Hz)\n")

for fs in RATES:
    t_s, x_s = sslab.sine(TONE_HZ, DURATION, fs)
    recovered = sslab.reconstruct(t_s, x_s, t_analog)
    inside = t_analog <= t_s[-1]

    found = sslab.dominant_frequency(recovered[inside], FS_ANALOG)
    max_error = float(np.max(np.abs(recovered[inside] - x_analog[inside])))

    if abs(found - TONE_HZ) > 0.5:
        verdict = "[ALIASED]"
    elif max_error < 0.05:
        verdict = "[faithful]"
    else:
        verdict = "[frequency kept, shape rough]"

    print(f"  fs = {fs:>2} Hz -> dominant frequency {found:.1f} Hz, "
          f"max error {max_error:.3f}   {verdict}")

print(f"""
Three lessons in three lines.

  fs = 50 Hz  comfortably above Nyquist: reconstruction is faithful.
  fs = 10 Hz  Nyquist still satisfied, so the FREQUENCY survives - but our
              crude interpolation leaves the SHAPE rough. The theorem promises
              perfect recovery only with a proper reconstruction filter.
  fs =  5 Hz  below Nyquist: the output is a clean, confident, WRONG {sslab.alias_frequency(TONE_HZ, 5):.0f} Hz tone
              - exactly |3 - 5| from the folding rule - and no downstream
              stage can ever know.
""")
