"""
archlab.py - tiny helpers for Lecture 2. Read me; I am short on purpose.
"""

import os
import platform
import shutil
import statistics
import subprocess
import time


def time_median(fn, reps=7):
    """Run fn() `reps` times; return (median_seconds, spread_seconds).

    Median, not mean: one background hiccup should not pollute the number.
    The spread (max - min) tells you how noisy the measurement was.
    """
    times = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return statistics.median(times), max(times) - min(times)


def machine_info():
    """Best-effort machine description, portable across OSes.

    On Linux, `lscpu` and /proc/meminfo give the real numbers (use those in
    your report). Elsewhere we fall back to what Python itself can see.
    """
    info = {
        "python": platform.python_version(),
        "os": f"{platform.system()} {platform.release()}",
        "machine": platform.machine(),
        "logical_cores": os.cpu_count(),
    }
    if shutil.which("lscpu"):
        out = subprocess.run(["lscpu"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            for key in ("Model name", "L1d", "L2", "L3"):
                if line.startswith(key):
                    info[key] = line.split(":", 1)[1].strip()
    return info
