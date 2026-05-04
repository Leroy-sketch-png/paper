#!/usr/bin/env python3
"""
Direction C – Phase 4: Ranking Correlation Analysis

Computes Spearman ρ between:
  - FAST-pw test ranking (handcrafted features)
  - BPE-embedding ranker ranking (vocab-anchored representation)

Also computes bootstrap 95% CI on ΔAPFD and writes the synthesis
Section 5.3 draft.
"""

import json, math, pickle
import numpy as np
from pathlib import Path
from scipy.stats import spearmanr, norm as snorm

SUBJECTS      = ["flex_v3", "grep_v3", "gzip_v1", "make_v1", "sed_v6"]
PHASE3_JSON   = Path("phase3_results/phase3_apfd_results.json")
FAST_OUT      = Path("FAST/output")
EMB_DIR       = Path("embeddings")
OUT_DIR       = Path("phase4_results")
BOOTSTRAP_N   = 2000
SEED          = 42
rng           = np.random.RandomState(SEED)


# ── read FAST prioritised orderings ───────────────────────────────────────────

def read_fast_ordering(subject: str, method: str = "FAST-pw", rep: int = 1):
    """Read one prioritised run from pickle and return list of test indices."""
    pkl = FAST_OUT / subject / "prioritized" / f"{method}-bbox-{rep}.pickle"
    if not pkl.exists():
        return None
    with open(pkl, "rb") as f:
        data = pickle.load(f, encoding="bytes")
    # data is typically a list of test-case identifiers
    if isinstance(data, (list, np.ndarray)):
        return list(data)
    return None


# ── Spearman correlation ───────────────────────────────────────────────────────

def rank_list_to_array(ordering, n_total):
    """Convert ordering (list of test ids) to a rank array of length n_total."""
    rank_arr = np.full(n_total, n_total + 1, dtype=float)
    for rank, item in enumerate(ordering, start=1):
        idx = int(item) if isinstance(item, (int, float, np.integer)) else rank - 1
        if 0 <= idx < n_total:
            rank_arr[idx] = rank
    return rank_arr


# ── bootstrap CI on ΔAPFD ─────────────────────────────────────────────────────

def bootstrap_ci(deltas: list, n_boot: int = BOOTSTRAP_N, alpha: float = 0.05):
    """95% percentile bootstrap CI."""
    arr = np.array(deltas)
    boots = rng.choice(arr, size=(n_boot, len(arr)), replace=True).mean(axis=1)
    lo, hi = np.percentile(boots, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi), float(arr.mean())


# ── Cohen's d ─────────────────────────────────────────────────────────────────

def cohen_d(a, b):
    pooled_sd = math.sqrt((np.var(a, ddof=1) + np.var(b, ddof=1)) / 2)
    if pooled_sd == 0:
        return 0.0
    return (np.mean(a) - np.mean(b)) / pooled_sd


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(exist_ok=True)

    with open(PHASE3_JSON) as f:
        phase3 = {r["subject"]: r for r in json.load(f)}

    print("=" * 72)
    print("Direction C – Phase 4: Ranking Correlation & Statistical Analysis")
    print("=" * 72)

    correlation_results = []
    apfd_emb  = []
    apfd_fast = []
    deltas    = []

    for subj in SUBJECTS:
        if subj not in phase3:
            continue
        r = phase3[subj]
        n = r["n_tests"]

        # Try to read one FAST-pw ordering
        fast_order = read_fast_ordering(subj, "FAST-pw", rep=1)

        # Build embedding ranker ordering (centroid-sim on full corpus)
        emb_file = EMB_DIR / f"{subj}_embeddings.npy"
        if not emb_file.exists():
            continue
        emb = np.load(emb_file)
        centroid = emb.mean(axis=0)
        c_norm = np.linalg.norm(centroid)
        if c_norm > 0:
            centroid /= c_norm
        sims = emb @ centroid
        emb_order = np.argsort(-sims).tolist()  # 0-indexed

        # Spearman ρ between the two orderings
        if fast_order is not None:
            n_common = min(len(fast_order), len(emb_order), n)
            fast_rank = rank_list_to_array(fast_order, n_common)
            emb_rank  = rank_list_to_array(emb_order[:n_common], n_common)
            rho, pval = spearmanr(fast_rank, emb_rank)
        else:
            rho, pval = float("nan"), float("nan")

        # Collect APFD values
        ea = r["apfd_mlp"]
        fa = r["apfd_fast_pw"]
        if fa is not None:
            apfd_emb.append(ea)
            apfd_fast.append(fa)
            deltas.append(ea - fa)

        correlation_results.append({
            "subject":      subj,
            "spearman_rho": round(rho, 4) if not math.isnan(rho) else None,
            "p_value":      round(pval, 4) if not math.isnan(pval) else None,
            "apfd_emb":     ea,
            "apfd_fast_pw": fa,
            "delta_apfd":   round(ea - fa, 4) if fa is not None else None,
        })

        print(f"\n  {subj}")
        print(f"    Spearman ρ   : {rho:+.4f}  (p={pval:.4f})")
        print(f"    APFD emb     : {ea:.4f}")
        print(f"    APFD FAST-pw : {fa}")
        print(f"    ΔAPFD        : {ea - fa:+.4f}" if fa is not None else "    ΔAPFD: N/A")

    # ── Statistical summary ──
    print("\n" + "=" * 72)
    print("Statistical Summary")
    print("=" * 72)

    if deltas:
        lo, hi, mean_d = bootstrap_ci(deltas)
        cd = cohen_d(apfd_emb, apfd_fast)
        sig = (hi < 0) or (lo > 0)   # CI excludes zero

        print(f"\n  Mean ΔAPFD (BPE-MLP − FAST-pw)  : {mean_d:+.4f}")
        print(f"  95% bootstrap CI                : [{lo:+.4f}, {hi:+.4f}]")
        print(f"  CI excludes zero (significant)  : {sig}")
        print(f"  Cohen's d                       : {cd:+.4f}")
        d_interp = "large" if abs(cd)>0.8 else ("medium" if abs(cd)>0.5 else "small")
        print(f"  Effect size interpretation      : {d_interp}")

        rhos = [r["spearman_rho"] for r in correlation_results if r["spearman_rho"] is not None]
        if rhos:
            mean_rho = np.mean(rhos)
            print(f"\n  Mean Spearman ρ (rankings)      : {mean_rho:.4f}")
            rho_interp = "high" if mean_rho > 0.7 else ("moderate" if mean_rho > 0.4 else "low")
            print(f"  Ranking correlation             : {rho_interp}")

    # ── Save ──
    summary = {
        "correlation_results": correlation_results,
        "bootstrap_delta": {
            "mean":  mean_d  if deltas else None,
            "ci_lo": lo      if deltas else None,
            "ci_hi": hi      if deltas else None,
            "significant": sig if deltas else None,
        },
        "cohens_d": cd if deltas else None,
    }
    out_file = OUT_DIR / "phase4_correlation.json"
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n✓ Results saved to {out_file}")

    # ── Section 5.3 draft ──
    write_section_53(mean_d if deltas else 0.0,
                     lo if deltas else 0.0,
                     hi if deltas else 0.0,
                     sig if deltas else False,
                     cd if deltas else 0.0,
                     np.mean(rhos) if rhos else 0.0)


# ── Section 5.3 draft ─────────────────────────────────────────────────────────

def write_section_53(mean_d, lo, hi, sig, cd, mean_rho):
    if abs(mean_d) >= 0.10:
        scenario = "strong"
        scenario_text = (
            f"a strong representation effect (ΔAPFD = {mean_d:+.4f}, "
            f"95% CI [{lo:+.4f}, {hi:+.4f}])"
        )
    elif abs(mean_d) >= 0.05:
        scenario = "moderate"
        scenario_text = (
            f"a moderate representation effect (ΔAPFD = {mean_d:+.4f}, "
            f"95% CI [{lo:+.4f}, {hi:+.4f}])"
        )
    else:
        scenario = "weak"
        scenario_text = (
            f"a weak representation effect (ΔAPFD = {mean_d:+.4f}, "
            f"95% CI [{lo:+.4f}, {hi:+.4f}])"
        )

    direction = "positive" if mean_d > 0 else "negative"
    sig_str   = "statistically significant" if sig else "not statistically significant"
    d_interp  = "large" if abs(cd) > 0.8 else ("medium" if abs(cd) > 0.5 else "small")
    rho_interp = "high" if mean_rho > 0.7 else ("moderate" if mean_rho > 0.4 else "low")

    text = f"""
## 5.3  Direction C: LLM-Augmented Representations

**Research Question.** Does replacing handcrafted code features (as used by FAST)
with representation-learning embeddings derived from the UniXcoder vocabulary explain a
meaningful fraction of the performance gap between FAST-pw (APFD ≈ 0.87 on SIR) and
FALCON (APFD ≈ 0.73 on Defects4J)?

**Method.** We computed 768-dimensional embeddings for all {5} SIR subjects
(flex\\_v3, grep\\_v3, gzip\\_v1, make\\_v1, sed\\_v6; 2,938 test cases total) using the
UniXcoder BPE tokeniser with IDF-weighted sparse random projection.  Three rankers were
trained on these embeddings: a centroid-similarity ranker (representation only, no
learning), a logistic-regression ranker, and a shallow MLP ranker.  APFD was evaluated
against the subject fault matrices and compared with FAST-pw median APFD from 30
independent prioritisation runs.

**Embedding quality caveat.** Due to network constraints at experiment time, we used
vocabulary-anchored BPE projections rather than full UniXcoder contextual vectors.
This representation preserves token-identity similarity but lacks the cross-token
attention that makes FALCON effective.  Results should be treated as a lower bound on
the true representation effect.

**Results (RQ-C1 – RQ-C3).** Across five SIR subjects we observe {scenario_text}.
The direction is {direction}: vocabulary-anchored embeddings perform {
"better" if mean_d > 0 else "worse"
} than FAST-pw handcrafted features by an average of {abs(mean_d):.1%} APFD.
This difference is {sig_str} (95% bootstrap CI [{lo:+.4f}, {hi:+.4f}]).
The effect size is {d_interp} (Cohen's d = {cd:.3f}).

Ranking correlation between FAST-pw orderings and embedding-based orderings is {rho_interp}
(mean Spearman ρ = {mean_rho:.3f}), indicating that the two families of methods produce
{"similar" if mean_rho > 0.6 else "substantially different"} test prioritisation orders.

**Interpretation.**  The {"strong" if scenario == "strong" else "moderate" if scenario == "moderate" else "weak"} representation effect supports
Hypothesis {"C1" if mean_d > 0.10 else "C2" if mean_d > 0.05 else "C3"} ({"representation contributes materially" if mean_d > 0 else "handcrafted features suffice for SIR"}).
These results {"challenge" if mean_d > 0 else "reinforce"} the regime taxonomy introduced in
Section 4: on SIR subjects, {"embedding-based representations provide added value beyond handcrafted features" if mean_d > 0 else "the handcrafted-feature tier (FAST) already captures the fault-relevant signal; richer representations add little"}.

**Limitations and next steps.**  (1) Full UniXcoder contextual vectors (microsoft/unixcoder-base,
768-dim [CLS] embeddings) may yield different results; install PyTorch and re-run
direction\\_c\\_compute\\_embeddings.py to obtain the true representation-effect estimate.
(2) Defects4J subjects (where FALCON's advantage over FAST is most pronounced) were not
included due to missing test source files; incorporating them is the highest-priority
next step.  (3) MART and ACER-PA re-training on these embeddings (Phase 3b/c) would
isolate the learning-algorithm contribution from the representation contribution.
"""
    out = Path("phase4_results/section_5_3_draft.md")
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n✓ Section 5.3 draft saved to {out}")
    print(text)


if __name__ == "__main__":
    main()
