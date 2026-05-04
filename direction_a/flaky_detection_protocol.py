#!/usr/bin/env python3
"""
Flaky-test detection framework (Direction A).

This script implements a re-execution-based protocol to identify flaky tests:
1. Run a test suite N times (configurable)
2. Collect pass/fail status per test per run
3. Identify tests that exhibit both pass and fail outcomes
4. Classify by frequency (e.g., consistently flaky vs rarely flaky)

Output: flaky test list and statistics per subject.
"""

import json
import statistics
from pathlib import Path
from collections import defaultdict

SUBJECTS = {
    "SIR": ["flex_v3", "grep_v3", "gzip_v1", "make_v1", "sed_v6"],
    "D4J": ["chart_v0", "closure_v0", "lang_v0", "math_v0", "time_v0"],
}

IDOFT_COVERAGE = {
    "jedis": 2,  # ID-category tests
    "spring-data-redis": 7,  # ID-category tests
    "flex_v3": 0,
    "grep_v3": 0,
    "gzip_v1": 0,
    "make_v1": 0,
    "sed_v6": 0,
    "chart_v0": 0,
    "closure_v0": 0,
    "lang_v0": 0,
    "math_v0": 0,
    "time_v0": 0,
}

def simulate_re_execution_protocol(subject, n_runs=30, flaky_ratio=0.15):
    """
    Simulate re-execution protocol.
    
    In practice, this would run the test suite N times and collect results.
    For simulation, we generate synthetic pass/fail outcomes with configurable flakiness.
    """
    # Estimate test count from FAST metadata
    test_counts = {
        "flex_v3": 670,
        "grep_v3": 809,
        "gzip_v1": 214,
        "make_v1": 875,
        "sed_v6": 370,
        "chart_v0": 355,
        "closure_v0": 217,
        "lang_v0": 110,
        "math_v0": 384,
        "time_v0": 122,
    }
    
    n_tests = test_counts.get(subject, 100)
    n_flaky = int(n_tests * flaky_ratio)
    
    # Simulate: some tests are deterministic (always pass or always fail),
    # others are flaky (randomly pass/fail)
    test_results = defaultdict(list)  # test_id -> [pass (1), pass (1), fail (0), ...]
    
    for test_id in range(n_tests):
        is_flaky = test_id < n_flaky
        for run in range(n_runs):
            if is_flaky:
                # Flaky test: 50-70% pass rate
                outcome = 1 if (run + test_id) % 2 == 0 else 0
            else:
                # Deterministic test: always pass
                outcome = 1
            test_results[test_id].append(outcome)
    
    # Identify flaky tests
    flaky_tests = []
    for test_id, outcomes in test_results.items():
        has_pass = any(outcomes)
        has_fail = any(not o for o in outcomes)
        if has_pass and has_fail:
            pass_rate = sum(outcomes) / len(outcomes)
            flaky_tests.append({
                "test_id": test_id,
                "pass_rate": round(pass_rate, 3),
                "pass_count": sum(outcomes),
                "fail_count": n_runs - sum(outcomes),
            })
    
    return {
        "subject": subject,
        "n_tests": n_tests,
        "n_runs": n_runs,
        "n_flaky_tests": len(flaky_tests),
        "flaky_ratio_detected": round(len(flaky_tests) / n_tests, 3),
        "flaky_tests": flaky_tests[:10],  # Top 10
    }

print("Flaky-Test Detection Protocol — Simulation")
print("=" * 80)
print("\nDirection A: Flaky-Label Contamination Impact\n")

print("IDoFT Coverage Status:")
print("-" * 80)
print("Subject                 IDoFT Labels    Status")
print("-" * 80)
for subject in IDOFT_COVERAGE:
    coverage = IDOFT_COVERAGE[subject]
    status = f"COVERED ({coverage} tests)" if coverage > 0 else "ABSENT"
    print(f"{subject:20} {coverage:3d} tests        {status}")

print("\n" + "=" * 80)
print("\nRe-Execution Protocol Simulation (N=30 runs per subject):")
print("-" * 80)

for subject in SUBJECTS["SIR"] + SUBJECTS["D4J"]:
    result = simulate_re_execution_protocol(subject, n_runs=30, flaky_ratio=0.15)
    print(f"\n{result['subject']}:")
    print(f"  Tests: {result['n_tests']}, Detected flaky: {result['n_flaky_tests']} ({result['flaky_ratio_detected']*100:.1f}%)")
    if result['flaky_tests']:
        print(f"  Sample flaky tests (pass rate):")
        for ft in result['flaky_tests'][:3]:
            print(f"    test_{ft['test_id']:3d}: {ft['pass_rate']:.2%} pass ({ft['pass_count']}/{result['n_runs']} runs)")

print("\n" + "=" * 80)
print("\nProtocol Design Notes:")
print("-" * 80)
print("""
1. IDoFT provides coverage only on jedis (2 tests) and spring-data-redis (7 tests).
   All other subjects must use supplementary detection methods.

2. Re-execution protocol:
   - Run full test suite ≥30 times on each subject
   - Collect per-test pass/fail for each run
   - Identify tests with both pass and fail outcomes
   - Classify flakiness type if possible (OD/ID/etc from re-execution patterns)

3. For subjects where re-execution is infeasible:
   - Use CI-log mining (GitHub Actions / Travis CI history)
   - Look for tests that fail sporadically without code changes
   - Heuristic: test failure on commit X but not on nearby commits with no intervening changes

4. Expected flaky ratio (from literature):
   - Industrial CI: 10-40% of test failures attributable to flakiness
   - Open-source: 5-20% depending on project maturity
   - Simulation assumes 15% for baseline estimation

5. Impact measurement:
   - Compare APFD before and after removing flaky tests from evaluation
   - Quantify delta per method to identify which methods are most sensitive
   - Update method rankings if flaky labels change the winner
""")

print("\nNext Step: Execute on actual test suites (requires test execution environment)")
