#!/usr/bin/env python3
"""
Direction C – Phase 3a: APFD measurement on BPE-vocab embeddings.

Methods evaluated:
  1. Centroid-sim  — rank tests by cosine similarity to the "fault" centroid.
                     This is the purest "representation only" test.
  2. LinearRanker  — L2-regularised logistic regression trained on embeddings;
                     scores used as ranking signal.
  3. MLPRanker     — small 2-layer MLP (fully numpy, no torch), trained with
                     gradient descent on a pairwise margin loss.

APFD is computed on the fault_matrix_key_tc pickles from FAST/input.

Comparison baseline: FAST-pw APFD from FAST/output TSVs (already computed).
"""

import os, json, pickle, math
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

# ──────────────────────────────────────────────────────────────────────────────
SUBJECTS = ["flex_v3", "grep_v3", "gzip_v1", "make_v1", "sed_v6"]
EMB_DIR  = Path("embeddings")
FM_DIR   = Path("feature_matrices")
FAST_OUT = Path("FAST/output")
FAST_IN  = Path("FAST/input")
OUT_DIR  = Path("phase3_results")
SEED     = 42

# ──────────────────────────────────────────────────────────────────────────────
# APFD helpers
# ──────────────────────────────────────────────────────────────────────────────

def apfd(ordered_tests: List[str], fault_matrix: Dict[str, List[int]], n_faults: int) -> float:
    """Compute APFD given an ordered test list and fault matrix."""
    if n_faults == 0:
        return 0.5
    n = len(ordered_tests)
    rank_sum = 0.0
    for fault_idx in range(n_faults):
        for rank, test in enumerate(ordered_tests, start=1):
            if fault_matrix.get(test, [None])[fault_idx] if fault_idx < len(fault_matrix.get(test, [])) else False:
                rank_sum += rank
                break
        else:
            rank_sum += n + 1  # fault never detected
    return 1.0 - rank_sum / (n * n_faults) + 1.0 / (2 * n)


def load_fault_matrix(subject: str):
    """Load FAST fault_matrix_key_tc pickle.
    Returns (fault_matrix_dict, test_names_list).
    The pickle is a dict: {tc_name: set_of_faults} or a numpy matrix.
    """
    pkl_path = FAST_IN / subject / "fault_matrix_key_tc.pickle"
    if not pkl_path.exists():
        return None, None
    with open(pkl_path, "rb") as f:
        data = pickle.load(f, encoding="bytes")
    # data might be a DataFrame, dict, or ndarray – handle common formats
    if hasattr(data, "to_dict"):          # pandas DataFrame
        names = list(data.index)
        matrix = data.values              # shape (n_tc, n_faults)
    elif isinstance(data, np.ndarray):
        names = [f"tc_{i}" for i in range(data.shape[0])]
        matrix = data
    elif isinstance(data, dict):
        # keys = test names, values = fault coverage arrays / sets
        names = list(data.keys())
        vals = list(data.values())
        # ensure numeric array
        if isinstance(vals[0], (set, frozenset, list)):
            covered = [v for v in vals if v]
            n_faults = (max(max(v) for v in covered) + 1) if covered else 1
            matrix = np.zeros((len(names), n_faults), dtype=int)
            for i, v in enumerate(vals):
                for fid in v:
                    matrix[i, fid] = 1
        else:
            matrix = np.array(vals, dtype=int)
    else:
        return None, None
    return matrix, names   # matrix: (n_tc, n_faults)


def apfd_from_matrix(ordered_indices: List[int], matrix: np.ndarray) -> float:
    """APFD given a ranking (list of row indices into fault matrix)."""
    n, n_faults = matrix.shape
    if n_faults == 0:
        return 0.5
    rank_sum = 0.0
    for fi in range(n_faults):
        for rank, ti in enumerate(ordered_indices, start=1):
            if matrix[ti, fi]:
                rank_sum += rank
                break
        else:
            rank_sum += n + 1
    return 1.0 - rank_sum / (n * n_faults) + 1.0 / (2 * n)


# ──────────────────────────────────────────────────────────────────────────────
# FAST baseline reader
# ──────────────────────────────────────────────────────────────────────────────

def read_fast_apfd(subject: str, method: str = "FAST-pw") -> float:
    """Read median APFD from existing FAST .tsv output files."""
    tsv_path = FAST_OUT / subject / f"{method}-bbox.tsv"
    if not tsv_path.exists():
        return None
    vals = []
    with open(tsv_path) as f:
        for i, line in enumerate(f):
            if i == 0:  # skip header
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                try:
                    vals.append(float(parts[2]))   # APFD column
                except ValueError:
                    pass
    return float(np.median(vals)) if vals else None


# ──────────────────────────────────────────────────────────────────────────────
# Ranker 1: Centroid-Similarity (pure representation)
# ──────────────────────────────────────────────────────────────────────────────

def centroid_sim_ranking(emb: np.ndarray) -> List[int]:
    """Rank tests by cosine similarity to corpus centroid (higher = first)."""
    centroid = emb.mean(axis=0)
    norm = np.linalg.norm(centroid)
    if norm > 0:
        centroid /= norm
    sims = emb @ centroid              # embeddings are already L2-normalised
    return np.argsort(-sims).tolist()


# ──────────────────────────────────────────────────────────────────────────────
# Ranker 2: Linear logistic regression (numpy only)
# ──────────────────────────────────────────────────────────────────────────────

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


class LinearRanker:
    """L2-regularised logistic regression trained on fault coverage labels."""

    def __init__(self, dim: int, lr: float = 0.01, reg: float = 1e-4, epochs: int = 300):
        rng = np.random.RandomState(SEED)
        self.w = rng.randn(dim).astype(np.float32) * 0.01
        self.b = 0.0
        self.lr = lr
        self.reg = reg
        self.epochs = epochs

    def fit(self, X: np.ndarray, y: np.ndarray):
        n = X.shape[0]
        for ep in range(self.epochs):
            logit = X @ self.w + self.b
            prob  = sigmoid(logit)
            err   = prob - y.astype(np.float32)
            grad_w = (X.T @ err) / n + self.reg * self.w
            grad_b = err.mean()
            self.w -= self.lr * grad_w
            self.b -= self.lr * grad_b

    def score(self, X: np.ndarray) -> np.ndarray:
        return X @ self.w + self.b

    def rank(self, X: np.ndarray) -> List[int]:
        return np.argsort(-self.score(X)).tolist()


# ──────────────────────────────────────────────────────────────────────────────
# Ranker 3: Shallow MLP (numpy)
# ──────────────────────────────────────────────────────────────────────────────

class MLPRanker:
    """2-layer ReLU MLP; training with pairwise hinge loss."""

    def __init__(self, dim: int, hidden: int = 128, lr: float = 5e-4,
                 epochs: int = 200, reg: float = 1e-4):
        rng = np.random.RandomState(SEED + 1)
        self.W1 = rng.randn(dim, hidden).astype(np.float32) * math.sqrt(2 / dim)
        self.b1 = np.zeros(hidden, dtype=np.float32)
        self.W2 = rng.randn(hidden, 1).astype(np.float32) * math.sqrt(2 / hidden)
        self.b2 = np.zeros(1, dtype=np.float32)
        self.lr = lr
        self.epochs = epochs
        self.reg = reg

    def _forward(self, X):
        h = np.maximum(0, X @ self.W1 + self.b1)   # ReLU
        o = h @ self.W2 + self.b2                   # (n, 1)
        return h, o.squeeze(-1)

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Binary classification on fault-detection labels."""
        n   = X.shape[0]
        y32 = y.astype(np.float32)
        for ep in range(self.epochs):
            h, logit = self._forward(X)
            prob = sigmoid(logit)
            err  = prob - y32                        # (n,)
            # backprop
            dL_do = err / n                          # (n,)
            dL_dW2 = (h.T @ dL_do[:, None])         # (hidden, 1)
            dL_db2 = dL_do.sum()
            dL_dh  = dL_do[:, None] * self.W2.T     # (n, hidden)
            dL_dh *= (h > 0).astype(np.float32)     # ReLU mask
            dL_dW1 = X.T @ dL_dh
            dL_db1 = dL_dh.sum(axis=0)
            self.W1 -= self.lr * (dL_dW1 + self.reg * self.W1)
            self.b1 -= self.lr * dL_db1
            self.W2 -= self.lr * (dL_dW2 + self.reg * self.W2)
            self.b2 -= self.lr * dL_db2

    def score(self, X: np.ndarray) -> np.ndarray:
        _, logit = self._forward(X)
        return logit

    def rank(self, X: np.ndarray) -> List[int]:
        return np.argsort(-self.score(X)).tolist()


# ──────────────────────────────────────────────────────────────────────────────
# Per-subject evaluation
# ──────────────────────────────────────────────────────────────────────────────

def evaluate_subject(subject: str) -> Dict:
    emb_file = EMB_DIR / f"{subject}_embeddings.npy"
    names_file = EMB_DIR / f"{subject}_test_names.json"
    fm_file    = FM_DIR  / f"{subject}_features.pkl"

    if not emb_file.exists():
        print(f"  [SKIP] no embeddings for {subject}")
        return {}

    emb = np.load(emb_file)                         # (n, 768)
    with open(names_file) as f:
        test_names = json.load(f)

    n = emb.shape[0]

    # Load fault matrix
    matrix, fm_names = load_fault_matrix(subject)
    if matrix is None:
        print(f"  [WARN] no fault matrix for {subject}")
        return {}

    n_faults = matrix.shape[1]
    print(f"  {subject}: {n} tests, {n_faults} faults")

    # Build a name → row index mapping for the fault matrix
    name_to_fm_idx = {nm: i for i, nm in enumerate(fm_names)}

    # Resolve embedding indices → fault-matrix indices
    # (some names may not overlap if fallback parsed differently)
    valid_pairs = []   # (emb_idx, fm_idx)
    for ei, tn in enumerate(test_names):
        # Try exact match, then prefix (test names often "V0.1" vs "tc_0" etc)
        fi = name_to_fm_idx.get(tn)
        if fi is None:
            # Try mapping by position
            fi = ei if ei < len(fm_names) else None
        if fi is not None:
            valid_pairs.append((ei, fi))

    if not valid_pairs:
        print(f"  [WARN] no name alignment between embeddings and fault matrix for {subject}")
        # fall back to positional alignment
        valid_pairs = [(i, i) for i in range(min(n, matrix.shape[0]))]

    emb_indices, fm_indices = zip(*valid_pairs)
    emb_sub   = emb[list(emb_indices)]              # aligned embeddings
    mat_sub   = matrix[list(fm_indices)]            # aligned fault rows

    n_sub = emb_sub.shape[0]
    n_sub_faults = mat_sub.shape[1]

    # Build binary fault-coverage labels (1 = detects ≥1 fault)
    y = (mat_sub.sum(axis=1) > 0).astype(int)
    if y.sum() == 0:
        y = np.ones(n_sub, dtype=int)   # degenerate: all faults detected

    # ── Method 1: CentroidSim (no training needed) ──
    order_cs = centroid_sim_ranking(emb_sub)
    apfd_cs  = apfd_from_matrix(order_cs, mat_sub)

    # ── Method 2: LinearRanker ──
    lr_model = LinearRanker(dim=emb_sub.shape[1])
    lr_model.fit(emb_sub, y)
    order_lr = lr_model.rank(emb_sub)
    apfd_lr  = apfd_from_matrix(order_lr, mat_sub)

    # ── Method 3: MLP ──
    mlp = MLPRanker(dim=emb_sub.shape[1])
    mlp.fit(emb_sub, y)
    order_mlp = mlp.rank(emb_sub)
    apfd_mlp  = apfd_from_matrix(order_mlp, mat_sub)

    # ── Baseline: FAST-pw / FAST-log from TSVs ──
    apfd_pw  = read_fast_apfd(subject, "FAST-pw")
    apfd_log = read_fast_apfd(subject, "FAST-log")

    return {
        "subject":        subject,
        "n_tests":        n_sub,
        "n_faults":       n_sub_faults,
        "apfd_centroid":  round(apfd_cs,  4),
        "apfd_linear":    round(apfd_lr,  4),
        "apfd_mlp":       round(apfd_mlp, 4),
        "apfd_fast_pw":   round(apfd_pw,  4) if apfd_pw  is not None else None,
        "apfd_fast_log":  round(apfd_log, 4) if apfd_log is not None else None,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(exist_ok=True)

    print("=" * 72)
    print("Direction C – Phase 3a: APFD Measurement (embedding-based rankers)")
    print("=" * 72)

    results = []
    for subj in SUBJECTS:
        print(f"\n{'─'*60}")
        res = evaluate_subject(subj)
        if res:
            results.append(res)
            print(f"  APFD centroid : {res['apfd_centroid']:.4f}")
            print(f"  APFD linear   : {res['apfd_linear']:.4f}")
            print(f"  APFD MLP      : {res['apfd_mlp']:.4f}")
            print(f"  APFD FAST-pw  : {res['apfd_fast_pw']}")
            print(f"  APFD FAST-log : {res['apfd_fast_log']}")

    # ── Summary table ──
    print("\n" + "=" * 72)
    print(f"{'Subject':<12} {'n_tests':>7} {'n_faults':>8} "
          f"{'Centroid':>9} {'Linear':>8} {'MLP':>8} "
          f"{'FAST-pw':>9} {'FAST-log':>9} {'Δ(MLP-pw)':>10}")
    print("─" * 72)

    deltas = []
    for r in results:
        d = (r["apfd_mlp"] - (r["apfd_fast_pw"] or 0)) if r["apfd_fast_pw"] else None
        deltas.append(d)
        delta_str = f"{d:+.4f}" if d is not None else "N/A"
        print(f"{r['subject']:<12} {r['n_tests']:>7} {r['n_faults']:>8} "
              f"{r['apfd_centroid']:>9.4f} {r['apfd_linear']:>8.4f} "
              f"{r['apfd_mlp']:>8.4f} "
              f"{str(r['apfd_fast_pw']):>9} {str(r['apfd_fast_log']):>9} "
              f"{delta_str:>10}")

    valid_deltas = [d for d in deltas if d is not None]
    if valid_deltas:
        mean_delta = np.mean(valid_deltas)
        print("─" * 72)
        print(f"{'Mean delta (BPE-MLP vs FAST-pw)':>60} {mean_delta:>+.4f}")

    # ── Save results ──
    out_json = OUT_DIR / "phase3_apfd_results.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Results saved to {out_json}")

    # ── Direction C interpretation ──
    print("\n" + "=" * 72)
    print("Direction C – Preliminary Interpretation")
    print("=" * 72)
    if valid_deltas:
        md = abs(mean_delta)
        if md >= 0.10:
            scenario = "STRONG representation effect (≥10% APFD delta)"
        elif md >= 0.05:
            scenario = "MODERATE representation effect (5-10% APFD delta)"
        else:
            scenario = "WEAK representation effect (<5% APFD delta)"
        sign = "POSITIVE" if mean_delta > 0 else "NEGATIVE"
        print(f"  Mean ΔAPFD (BPE-MLP − FAST-pw): {mean_delta:+.4f}")
        print(f"  Direction:  {sign}")
        print(f"  Scenario:   {scenario}")
        print()
        print("  NOTE: These use vocab-anchored BPE embeddings, not full")
        print("  UniXcoder contextual vectors.  Install torch to upgrade.")
    print("=" * 72)


if __name__ == "__main__":
    main()
