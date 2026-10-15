"""
check_setup.py - run this FIRST, before the lab.   python check_setup.py

It answers one question: can this computer run Lecture 2's code?
Nothing here is graded. If a line says FAIL, fix that line and run it again.
"""

import shutil
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


print("Lecture 2 - environment check\n")

check(f"Python {sys.version.split()[0]} (3.10 or newer)",
      sys.version_info >= (3, 10),
      "install a newer Python from python.org")

try:
    import numpy
    check(f"numpy {numpy.__version__}", True)
except ImportError:
    check("numpy", False, "pip install numpy")

import dis  # noqa: F401  (stdlib - always present; imported to be explicit)
check("dis module (Python bytecode disassembler, stdlib)", True)

check("lscpu (Linux only - nicer machine info for Lab 2A)",
      shutil.which("lscpu") is not None,
      "not on this OS - lab02a_starter.py falls back to Python's own view",
      optional=True)

check("gcc (only for the lecture's nine-byte aside; nothing in the lab needs it)",
      shutil.which("gcc") is not None,
      "skip, or use the course environment",
      optional=True)

print()
print("All good - start with demo_01_bits_and_bases.py" if ok
      else "Fix the FAIL lines above, then run me again.")
sys.exit(0 if ok else 1)
