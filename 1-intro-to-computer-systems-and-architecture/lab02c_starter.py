"""
LAB 2C - "Measure the memory hierarchy"       (challenge; optional; 3-4 h)

You are reproducing the lecture's stride experiment on your own
machine, then predicting and explaining the curve. 

Run:  python lab02c_starter.py
Deliverables: this file completed, report.md, and your table/plot.
"""

import numpy as np

from archlab import machine_info, time_median

print("=" * 70)
print("TASK 1 - the stride experiment, honestly")
print("=" * 70)

# TODO 1a: size the experiment for YOUR machine. The array must be much
#          larger than your L3 cache (find L3 with lscpu, or from
#          machine_info() on Linux). Keep the touched-element count FIXED
#          across strides - same work every row.
N_TOUCH = 1_000_000
STRIDES = (1, 2, 4, 8, 16, 32)
a = np.arange(N_TOUCH * max(STRIDES), dtype=np.int64)

print(f"\n  array: {a.nbytes / 2**20:.0f} MB;  my machine: {machine_info()}\n")
print(f"  {'stride':>6} | {'ns/elem (median of 7)':>22} | {'spread ns':>9}")
print(f"  {'-'*6} | {'-'*22} | {'-'*9}")

results = {}
for stride in STRIDES:
    view = a[: N_TOUCH * stride : stride]
    # TODO 1b: time np.add.reduce(view) with time_median (>= 7 reps).
    #          Store nanoseconds-per-element in `results[stride]` and print
    #          the row, INCLUDING the spread - a result without its noise
    #          estimate is not a measurement.
    ...

print("""
  TODO 1c (report): present time-per-element versus stride and annotate
  where your caches should stop helping, using your own cache sizes.
""")

print("=" * 70)
print("TASK 2 - predict, then compare")
print("=" * 70)
print("""
  In the report, BEFORE looking too hard at your table: from your 64-byte
  cache-line size, predict at which stride every element costs a full line
  (stride >= line/8 for int64) and therefore where the curve saturates.
  Compare prediction to measurement. Name deviations honestly - hardware
  prefetching and TLB effects are allowed to appear as open questions.
""")

print("=" * 70)
print("TASK 3 - a second locality experiment: rows versus columns")
print("=" * 70)

side = 4000
m = np.arange(side * side, dtype=np.int64).reshape(side, side)

# TODO 3: time summing `m` row-by-row versus column-by-column WITHOUT
#         letting numpy pick the fast path for you - e.g. loop over
#         m[i, :].sum() versus m[:, j].sum() - and report the ratio.
#         Then state the layout convention (row-major) that explains it.
row_time, col_time = None, None

print(f"\n  row-by-row: {row_time}   column-by-column: {col_time}")

print("""
  TASK 4 (report only) - transfer: connect ONE measured ratio from above
  to one AI-era fact from lecture Part 5 (e.g. why token generation is
  memory-bandwidth-bound). Be explicit about which number carries the
  argument.
""")
