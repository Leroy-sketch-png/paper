"""
Heuristic baselines for TCP:
1. Failure-Frequency-First (FFF): sort tests by number of faults/versions they detect (desc)
   - SIR: fault_matrix key=tcID, val=[fault_IDs]  → count faults per test
   - D4J: fault_matrix key=version, val=[faulty_tcs] → count versions per test (javaFlag=True)
2. Random-30: mean APFD over 30 random orderings (fixed seeds for reproducibility)

Note: FFF is oracle-based (requires ground-truth failure knowledge). It is an informed
upper-bound baseline, not a realistic deployment heuristic.
"""
import os, sys, pathlib, pickle, random, statistics, csv


def workspace_root() -> pathlib.Path:
    current = pathlib.Path(__file__).resolve()
    for candidate in (current.parent, *current.parents):
        if (candidate / ".github" / "copilot-instructions.md").exists():
            return candidate
    raise FileNotFoundError("Could not locate workspace root from script path")


ROOT = workspace_root()
FAST = ROOT / "FAST"
ARTIFACTS = ROOT / "artifacts"
os.chdir(FAST)
sys.path.insert(0, str(FAST / "py"))
import metric as m

SIR_SUBJECTS = ["flex_v3", "grep_v3", "gzip_v1", "make_v1", "sed_v6"]
D4J_SUBJECTS = ["chart_v0", "closure_v0", "lang_v0", "math_v0", "time_v0"]

BBOX_FILES = {
    "flex_v3":    "input/flex_v3/flex-bbox.txt",
    "grep_v3":    "input/grep_v3/grep-bbox.txt",
    "gzip_v1":    "input/gzip_v1/gzip-bbox.txt",
    "make_v1":    "input/make_v1/make-bbox.txt",
    "sed_v6":     "input/sed_v6/sed-bbox.txt",
    "chart_v0":   "input/chart_v0/chart-bbox.txt",
    "closure_v0": "input/closure_v0/closure-bbox.txt",
    "lang_v0":    "input/lang_v0/lang-bbox.txt",
    "math_v0":    "input/math_v0/math-bbox.txt",
    "time_v0":    "input/time_v0/time-bbox.txt",
}

FM_FILES = {
    "flex_v3":    "input/flex_v3/fault_matrix_key_tc.pickle",
    "grep_v3":    "input/grep_v3/fault_matrix_key_tc.pickle",
    "gzip_v1":    "input/gzip_v1/fault_matrix_key_tc.pickle",
    "make_v1":    "input/make_v1/fault_matrix_key_tc.pickle",
    "sed_v6":     "input/sed_v6/fault_matrix_key_tc.pickle",
    "chart_v0":   "input/chart_v0/fault_matrix.pickle",
    "closure_v0": "input/closure_v0/fault_matrix.pickle",
    "lang_v0":    "input/lang_v0/fault_matrix.pickle",
    "math_v0":    "input/math_v0/fault_matrix.pickle",
    "time_v0":    "input/time_v0/fault_matrix.pickle",
}


def load_fm(subj):
    with open(FM_FILES[subj], "rb") as f:
        return pickle.load(f)


def count_tests(subj):
    with open(BBOX_FILES[subj]) as f:
        return len(f.readlines())


def fff_order_sir(fm, tc_ids):
    """SIR: fm[tcID] = [fault_IDs]. Sort by count of detected faults desc."""
    fault_counts = {tc: len(fm.get(tc, [])) for tc in tc_ids}
    return sorted(tc_ids, key=lambda t: fault_counts[t], reverse=True)


def fff_order_d4j(fm, tc_ids):
    """D4J: fm[version] = [faulty_tcs]. Sort tests by # versions they appear in desc."""
    version_counts = {tc: 0 for tc in tc_ids}
    for faulty_tcs in fm.values():
        for tc in faulty_tcs:
            if tc in version_counts:
                version_counts[tc] += 1
    return sorted(tc_ids, key=lambda t: version_counts[t], reverse=True)


def compute_apfd_sir(order, fm_path):
    return m.apfd(order, fm_path, False)


def compute_apfd_d4j(order, fm_path):
    """D4J javaFlag=True returns list of APFDs (one per version). Return mean."""
    apfds = m.apfd(order, fm_path, True)
    return statistics.mean(apfds)


def run_all():
    ARTIFACTS.mkdir(exist_ok=True)
    results = {}

    for subj in SIR_SUBJECTS + D4J_SUBJECTS:
        is_d4j = subj in D4J_SUBJECTS
        print(f"\n=== {subj} {'(D4J)' if is_d4j else '(SIR)'} ===")

        n = count_tests(subj)
        fm_path = FM_FILES[subj]
        fm = load_fm(subj)
        tc_ids = list(range(1, n + 1))

        # FFF ordering
        fff = fff_order_d4j(fm, tc_ids) if is_d4j else fff_order_sir(fm, tc_ids)
        fff_apfd = compute_apfd_d4j(fff, fm_path) if is_d4j else compute_apfd_sir(fff, fm_path)
        print(f"  Failure-Freq-First APFD: {fff_apfd:.4f}")

        # Random-30 (fixed seeds)
        rand_apfds = []
        for seed in range(30):
            random.seed(seed)
            order = tc_ids[:]
            random.shuffle(order)
            a = compute_apfd_d4j(order, fm_path) if is_d4j else compute_apfd_sir(order, fm_path)
            rand_apfds.append(a)
        rand_mean = statistics.mean(rand_apfds)
        rand_std = statistics.stdev(rand_apfds)
        print(f"  Random-30 APFD: mean={rand_mean:.4f} stdev={rand_std:.4f}")

        results[subj] = {
            "n_tests": n,
            "fff_apfd": fff_apfd,
            "rand_mean": rand_mean,
            "rand_std": rand_std,
        }

    # Summary table
    print("\n" + "="*80)
    print(f"{'Subject':<15} {'N':>6} {'FFF':>8} {'Rand(mean)':>12} {'Rand(std)':>10}")
    print("-"*80)
    for subj in SIR_SUBJECTS + D4J_SUBJECTS:
        r = results[subj]
        print(f"{subj:<15} {r['n_tests']:>6} {r['fff_apfd']:>8.4f} {r['rand_mean']:>12.4f} {r['rand_std']:>10.4f}")

    # Write CSV
    out_path = ARTIFACTS / "heuristic_baselines.csv"
    with open(out_path, "w", newline="") as csvf:
        writer = csv.writer(csvf)
        writer.writerow(["subject", "suite", "n_tests", "fff_apfd", "rand30_mean", "rand30_stdev"])
        for subj in SIR_SUBJECTS + D4J_SUBJECTS:
            r = results[subj]
            suite = "D4J" if subj in D4J_SUBJECTS else "SIR"
            writer.writerow([subj, suite, r["n_tests"],
                             f"{r['fff_apfd']:.4f}", f"{r['rand_mean']:.4f}", f"{r['rand_std']:.4f}"])
    print(f"\nWritten to {out_path}")


if __name__ == "__main__":
    run_all()
