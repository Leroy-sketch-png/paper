#!/usr/bin/env python3
"""
Compute bootstrap 95% confidence intervals for SIR FAST-pw and FAST-log results.
Reads the 30-repetition TSV files and resamples with replacement.
"""

import os
import csv
import statistics
import random
from pathlib import Path

SIR_SUBJECTS = ["flex_v3", "grep_v3", "gzip_v1", "make_v1", "sed_v6"]
FAST_METHODS = [("FAST-pw", "FAST-pw-bbox.tsv"), ("FAST-log", "FAST-log-bbox.tsv")]
FAST_BASE = r"c:\Users\YOGA\Downloads\research\FAST\output"
N_BOOTSTRAP = 1000
ALPHA = 0.05  # 95% CI

def read_tsv(fpath):
    """Read APFD values from TSV file (all rows)."""
    apfds = []
    try:
        with open(fpath, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    apfd = float(row['APFD'])
                    apfds.append(apfd)
                except (ValueError, KeyError):
                    pass
    except FileNotFoundError:
        pass
    return apfds

def bootstrap_ci(data, n_resamples=1000, alpha=0.05):
    """Compute bootstrap percentile CI."""
    if len(data) < 2:
        return None, None
    resampled_means = []
    for _ in range(n_resamples):
        sample = [random.choice(data) for _ in range(len(data))]
        resampled_means.append(statistics.mean(sample))
    resampled_means.sort()
    lower_idx = int(n_resamples * (alpha / 2))
    upper_idx = int(n_resamples * (1 - alpha / 2))
    return resampled_means[lower_idx], resampled_means[upper_idx]

print("Bootstrap 95% CIs for SIR FAST results (1000 resamples)")
print("=" * 80)

for subject in SIR_SUBJECTS:
    print(f"\n{subject}:")
    for method_name, tsv_name in FAST_METHODS:
        tsv_file = Path(FAST_BASE) / subject / tsv_name
        data = read_tsv(str(tsv_file))
        if data:
            mean = statistics.mean(data)
            stdev = statistics.stdev(data) if len(data) > 1 else 0
            lower, upper = bootstrap_ci(data, N_BOOTSTRAP, ALPHA)
            print(f"  {method_name:10} n={len(data):2d}  mean={mean:.4f} stdev={stdev:.4f} CI95=[{lower:.4f}, {upper:.4f}]")
        else:
            print(f"  {method_name:10} — no data")

print("\n" + "=" * 80)
print("Note: Bootstrap CIs are percentile-based, using 1000 resamples with replacement.")
print("CI95 = 2.5th to 97.5th percentile of resampled means.")
