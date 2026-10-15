# Lab 2 — Computer Systems & Architecture


**Setup** (once):

```bash
pip install -r requirements.txt
```

```bash
python check_setup.py
```




## Lab2C: "Measure the memory hierarchy"


Run `python lab02c_starter.py` and complete its TODOs.

1. **Reproduce the stride experiment**: array ≫ your L3, fixed element count,
   strides 1…32, ≥ 7 repetitions, report the **median and the spread**.
2. **Predict, then compare**: from your cache-line size and cache capacities,
   predict where the curve bends and saturates; discuss deviations honestly
   (prefetching and TLB effects may appear — name them as open questions).
3. **A second locality experiment**: sum a large 2-D array row-by-row versus
   column-by-column and report the ratio; state the row-major convention that
   explains it.
