# checks.py — one check per behaviour. Run them all with:  python checks.py
# A check calls a function with a known input and states the expected answer with assert.
# If every assert is true, the last line prints; if one is false, Python stops there and tells you.

import logic
import numpy as np

result = logic.heart_size(4)
x = np.linspace(-(4/3+2), 4/3+2, 400)
y = np.linspace(-(4/3+2), 4/3+2, 400)
x, y = np.meshgrid(x, y)
assert np.all(result == (x**2 + y**2 - int(4))**3 - x**2 * y**3), "got " + str(result)

result = logic.heart_size(1)
x = np.linspace(-(1/3+2), 1/3+2, 400)
y = np.linspace(-(1/3+2), 1/3+2, 400)
x, y = np.meshgrid(x, y)
assert np.all(result == (x**2 + y**2 - int(1))**3 - x**2 * y**3), "got " + str(result)

result = logic.heart_size(100)
x = np.linspace(-(100/3+2), 100/3+2, 400)
y = np.linspace(-(100/3+2), 100/3+2, 400)
x, y = np.meshgrid(x, y)
assert np.all(result == (x**2 + y**2 - int(100))**3 - x**2 * y**3), "got " + str(result)

print("all checks passed")
