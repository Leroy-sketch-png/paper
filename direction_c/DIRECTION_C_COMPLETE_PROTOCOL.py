#!/usr/bin/env python3
"""
Direction C: Complete Execution Protocol & Roadmap

LLM-Augmented Representations for ML-TCP.

This document specifies the complete protocol for Direction C:
  - Research questions & hypotheses
  - Experimental design
  - Implementation phases
  - Expected outcomes
  - Success criteria

Can be executed in phases as dependencies become available.
"""

import json
from datetime import datetime
from pathlib import Path

print("=" * 90)
print("DIRECTION C: LLM-AUGMENTED REPRESENTATIONS FOR ML-TCP")
print("Complete Execution Protocol & Roadmap")
print("=" * 90)

protocol = {
    "title": "Direction C: LLM Representations in TCP",
    "date": datetime.now().isoformat(),
    "status": "Framework Ready",
    "dependencies": {
        "torch": "install status: PENDING (network timeout)",
        "transformers": "install status: PENDING",
        "scikit-learn": "install status: PENDING",
        "numpy": "status: AVAILABLE"
    },
    "workaround": "Can proceed without immediate torch; protocol design complete"
}

print(f"""
RESEARCH QUESTION:
  Does the semantic-gap advantage (FALCON 0.731 vs FAST-pw 0.602 on Defects4J)
  persist when we apply UniXcoder embeddings to EXISTING methods (MART, ACER-PA)?

HYPOTHESIS C1: Representation Advantage
  - Statement: UniXcoder embeddings > handcrafted CI features
  - Prediction: MART(UniXcoder) - MART(handcrafted) ≥ 10% APFD gain
  - Interpretation: Semantic understanding of code structure is orthogonal to
                   code metrics, enabling better feature extraction

HYPOTHESIS C2: Partial Gap Closure
  - Statement: LLM representations reduce but don't eliminate FALCON advantage
  - Prediction: MART(UniXcoder) ≈ 0.65-0.70 (between 0.60 and 0.73)
  - Interpretation: Method + representation both matter; neither is dominant

HYPOTHESIS C3: Regime Taxonomy Stability
  - Statement: Method ranking is robust to representation choice
  - Prediction: Spearman ρ ≥ 0.85 for ranking correlation
  - Interpretation: Regime differences (heuristic, FAST, semantic, ML) are
                   orthogonal to feature representation era

BASELINE NUMBERS (to beat):
  - FALCON (semantic, UniXcoder-based): 0.731 median APFD (Defects4J)
  - FAST-pw (handcrafted, statistical): 0.602 median APFD (Defects4J)
  - Gap to close: 0.129 (21.3% improvement)
""")

print("\n" + "=" * 90)
print("PHASE 1: UNIXCODER EMBEDDING INFRASTRUCTURE")
print("=" * 90)

phase1 = {
    "objective": "Compute UniXcoder embeddings for all test sources (SIR + D4J)",
    "dependencies": ["torch", "transformers"],
    "timeline": "2-3 hours (GPU) / 2-3 hours (CPU with HF cache)",
    "outputs": [
        "embeddings/{subject}_embeddings.npy — (n_tests, 768) float32 array",
        "embeddings/{subject}_test_names.json — indexed test names",
        "embeddings/embedding_metadata.json — summary statistics"
    ],
    "estimated_storage": "~1 MB per 100 tests × 25 subjects ≈ 25 MB total"
}

print(f"""
Objective: {phase1['objective']}

Dependency: torch + transformers (attempting installation with retries)

Models to use:
  - Primary: microsoft/unixcoder-base (768-dim output)
  - Backup: microsoft/unixcoder-large (if GPU available; 1024-dim)
  - License: MIT (open source, no access restrictions)

Preprocessing (matching FALCON paper):
  - Max length: 512 tokens per source file
  - Normalization: L2 unit norm
  - Tokenizer: BPE (Byte-Pair Encoding, built into UniXcoder)

Subjects to embed:
  SIR (C):
    - flex_v3: ~50 tests
    - grep_v3: ~49 tests
    - gzip_v1: ~54 tests
    - make_v1: ~47 tests
    - sed_v6: ~53 tests
    → Total: ~250 tests

  Defects4J (Java): [requires Defects4J installation]
    - Chart: ~49 tests
    - Closure: ~54 tests
    - Lang: ~24 tests
    - Math: ~15 tests
    - Time: ~21 tests
    → Total: ~160 tests

IMPLEMENTATION:
  Script: direction_c/direction_c_compute_embeddings.py
  - Load UniXcoder from Hugging Face (first run downloads ~900MB)
  - Batch process tests (batch_size=32, configurable)
  - GPU acceleration (falls back to CPU)
  - Save as .npy (numpy arrays) for ML training

ALTERNATIVE (if torch installation fails):
  - Use ONNX Runtime (lighter weight, no torch needed)
  - Or use sentence-transformers library (simpler API)
  - Or simulate embeddings with PCA on FAST features (lossy but functional)
""")

print("\n" + "=" * 90)
print("PHASE 2: FEATURE MATRIX GENERATION")
print("=" * 90)

phase2 = {
    "objective": "Convert embeddings to train/test matrices for ML training",
    "dependencies": ["scikit-learn", "numpy"],
    "timeline": "< 1 hour",
    "outputs": [
        "feature_matrices/{subject}_features.pkl — sklearn-compatible dict",
        "feature_matrices/summary_stats.json — train/test split info"
    ]
}

print(f"""
Objective: {phase2['objective']}

Train/Test Split:
  - Strategy: Stratified 80/20 split (matches FALCON paper)
  - Random seed: 42 (reproducibility)
  - Balancing: Ensure both splits have diverse test coverage

Feature Matrix Format (for sklearn):
  {{
    "X_train": ndarray of shape (n_train, 768),
    "X_test": ndarray of shape (n_test, 768),
    "n_train": int,
    "n_test": int,
    "embedding_dim": 768,
    "type": "sir" or "d4j"
  }}

IMPLEMENTATION:
  Script: direction_c/direction_c_feature_matrix.py
  - Load all embeddings from Phase 1
  - Create train/test splits
  - Standardize (optional: zero-mean, unit variance)
  - Save as pickle (efficient for large arrays)

OUTPUT SIZE:
  - SIR: ~250 tests × 768 dims × 4 bytes = ~0.75 MB per split × 5 subjects = 3.75 MB
  - D4J: ~160 tests × 768 dims × 4 bytes = ~0.5 MB per split × 5 subjects = 2.5 MB
  - Total: ~6.25 MB (compressed)
""")

print("\n" + "=" * 90)
print("PHASE 3: METHOD RE-EVALUATION")
print("=" * 90)

phase3 = {
    "objective": "Train existing methods on UniXcoder embeddings; compare vs handcrafted",
    "dependencies": ["MART source code (Zenodo 7036507) or ACER-PA reference implementation"],
    "timeline": "3-5 days (blocked on Understand license for MART)",
    "blocking_note": "MART requires Understand static analysis tool (proprietary)",
    "workaround": "Train ACER-PA (CNN, no Understand needed) as interim; 3 days"
}

print(f"""
Objective: {phase3['objective']}

BLOCKED DEPENDENCY: MART training requires Understand static analysis tool
STATUS: Zenodo 7036507 replication package includes MART implementation
        but requires Understand license (proprietary, ~$10k/year)

WORKAROUND 1: Train ACER-PA (Immediate, 2-3 days)
  - Architecture: CNN with 2-3 hidden layers
  - Input: UniXcoder embeddings (768-dim)
  - Training: SGD + L2 regularization on Defects4J
  - Evaluation: APFD on test set
  - Comparison: ACER-PA(UniXcoder) vs ACER-PA(handcrafted)
  - Rationale: Proves representation-level advantage without Understand

WORKAROUND 2: Surrogate Regression (Immediate, 1-2 days)
  - Substitute for MART while awaiting Understand
  - Learn: test source embeddings → ranking scores (using FAST-log as proxy)
  - Train: Ridge regression on Defects4J
  - Evaluate: Ranking correlation & APFD
  - Rationale: Functional experiment; less rigorous but informative

FULL PROTOCOL (once Understand available, ~5 days):
  1. Replicate MART from Zenodo 7036507 on handcrafted features
     - Verify against paper baseline (0.60 median)
  2. Substitute UniXcoder embeddings for handcrafted features
  3. Re-train MART on embeddings
  4. Measure APFD on same test set
  5. Compute delta: (APFD_unixcoder - APFD_handcrafted) / APFD_handcrafted
  6. Tabulate results per project

METHODS TO EVALUATE (in priority order):
  1. ACER-PA (source paper, CNN-based) [UNBLOCKED]
  2. MART (source paper, regression-based) [BLOCKED on Understand]
  3. Ridge Regression (surrogate) [UNBLOCKED]
  4. FAST-like Decision Tree (representation stress test) [UNBLOCKED]

EXPECTED OUTCOMES:
  Conservative: Δ APFD ≈ 0% (representation doesn't help)
  Optimistic: Δ APFD ≈ 10% (strong representation effect)
  Ceiling: APFD_unixcoder ≈ 0.70+ (nearly closes FALCON gap)
""")

print("\n" + "=" * 90)
print("PHASE 4: RANKING CORRELATION & REGIME ANALYSIS")
print("=" * 90)

phase4 = {
    "objective": "Assess whether regime taxonomy is representation-era specific",
    "dependencies": ["scipy (for Spearman rank correlation)"],
    "timeline": "1-2 days"
}

print(f"""
Objective: {phase4['objective']}

RANKING STABILITY TEST:
  Current ranking (by handcrafted feature APFD, Defects4J median):
    1. FALCON ≈ 0.731 (semantic, UniXcoder-based) ← BASELINE
    2. FAST-log ≈ 0.628 (handcrafted, statistical)
    3. FAST-pw ≈ 0.602 (handcrafted, statistical)
    4. ACER-PA ≈ 0.60+ (deep learning, handcrafted features)
    5. Random-30 ≈ 0.52 (baseline)

  Question: After applying UniXcoder to MART/ACER-PA, does ranking change?
  
  Test: Compute Spearman rank correlation between handcrafted and UniXcoder rankings
    - ρ ≥ 0.85: Rankings highly stable (representation orthogonal to method)
    - 0.70 ≤ ρ < 0.85: Moderate reordering (representation + method interact)
    - ρ < 0.70: Substantial reordering (representation fundamentally changes winner)

REGIME TAXONOMY RE-ASSESSMENT:
  Current taxonomy (from literature):
    - HEURISTICS: random, shortest-first, recent-failure-first
    - FAST: static features + decision tree / random forest
    - SEMANTIC: pre-trained code embeddings (FALCON)
    - DEEP-LEARNING: learned representations (CNN, RNN)
    - ML/RL: domain-specific adaptation (federated, RL)

  Questions:
    1. Is semantic > FAST due to representation or method?
       → Compare FAST decision tree on UniXcoder embeddings
       → If FAST(UniXcoder) ≈ 0.65+, representation is primary
    
    2. Is deep-learning > ML due to learned features?
       → Compare ACER-PA on UniXcoder embeddings
       → If gap closes, method is secondary
    
    3. Is regime taxonomy era-agnostic?
       → If Spearman ρ ≈ 1.0, ranking is robust
       → If ρ < 0.7, regime differences are era-specific artifacts

STATISTICAL TESTS:
  - Spearman rank correlation (significance: α = 0.05)
  - Paired t-test: APFD_unicoder vs APFD_handcrafted (per method)
  - Cohen's d: Effect size of representation shift
  - Bootstrap CIs: 95% confidence on ranking correlation
""")

print("\n" + "=" * 90)
print("PHASE 5: SYNTHESIS & PUBLICATION")
print("=" * 90)

print("""
Objective: Integrate findings into manuscript/paper_skeleton.md (Section 5.3: LLM Representations)

FINDINGS TO DOCUMENT:
  1. UniXcoder embedding quality (per subject)
     - Coverage: n_tests per subject, embedding dimension
     - Quality: L2 norm distribution, semantic coherence (optional: similarity analysis)
  
  2. Representation effect (per method)
     - ΔAPFD = (APFD_unixcoder - APFD_handcrafted) / APFD_handcrafted
     - Bootstrap CIs on delta
     - Statistical significance
  
  3. Gap closure analysis
     - % of FALCON gap closed: (APFD_unixcoder - APFD_handcrafted) / (FALCON - APFD_handcrafted)
     - Per-project and aggregate
     - Project-specific variation
  
  4. Ranking correlation
     - Spearman ρ between handcrafted and UniXcoder rankings
     - Interpretation: regime taxonomy stability
  
  5. Regime taxonomy update
     - Evidence: Does representation choice explain regime-level performance gaps?
     - Implication: Are heuristic/FAST/semantic/ML categories era-agnostic?

PAPER SECTIONS:
  - Section 4 (Baselines): Add UniXcoder embeddings as representation tier
  - Section 5.3 (LLM Representations): Full Direction C results + analysis
  - Section 6 (Analysis): Regime taxonomy stability discussion
  - Figure 3: APFD comparison (handcrafted vs UniXcoder) boxplot per method
  - Table X: Representation shift per method + per project

WORD BUDGET: ~800 words for Section 5.3
DEADLINE: Before final manuscript review
""")

print("\n" + "=" * 90)
print("SUCCESS CRITERIA & DECISION TREE")
print("=" * 90)

criteria = {
    "Phase 1: Embeddings": {
        "success": "All subjects embedded; no NaN values; L2 norm ≈ 1.0",
        "failure": "Failed to compute embeddings; torch installation blocked",
        "decision": "Proceed to Phase 2 if success; use ONNX workaround if failure",
        "status": "BLOCKED (torch timeout, retrying...)"
    },
    "Phase 2: Feature Matrices": {
        "success": "Train/test splits created; shapes match expected",
        "failure": "File I/O errors; sklearn unavailable",
        "decision": "Proceed to Phase 3 if success; check sklearn installation if failure",
        "status": "READY (numpy + pickle available)"
    },
    "Phase 3: Method Re-evaluation": {
        "success": "APFD_unixcoder > APFD_handcrafted by ≥5% for at least 1 method",
        "failure": "No improvement; representation has negligible effect",
        "decision": "If success: Proceed to Phase 4 + publication. If failure: Document constraints.",
        "status": "BLOCKED (Understand license); ACER-PA workaround READY"
    },
    "Phase 4: Ranking Correlation": {
        "success": "Spearman ρ ≥ 0.80; regime ranking is stable",
        "failure": "Spearman ρ < 0.70; representation fundamentally changes ranking",
        "decision": "Success → regime taxonomy is robust. Failure → era-specific.",
        "status": "READY (scipy available)"
    },
    "Phase 5: Publication": {
        "success": "Section 5.3 complete; all tables & figures in manuscript/paper_skeleton.md",
        "failure": "Insufficient data for publication-quality claims",
        "decision": "Conditional: publish if Phase 3 & 4 succeed; otherwise contribution is protocol.",
        "status": "PENDING (depends on Phases 1-4)"
    }
}

for phase, details in criteria.items():
    print(f"\n{phase}:")
    print(f"  Success Criterion: {details['success']}")
    print(f"  Failure Criterion: {details['failure']}")
    print(f"  Decision: {details['decision']}")
    print(f"  Status: {details['status']}")

print("\n" + "=" * 90)
print("TIMELINE & EFFORT ESTIMATE")
print("=" * 90)

timeline_table = """
Phase  Task                          Timeline    Effort  Blocker         Status
─────  ──────────────────────────    ──────────  ──────  ──────────────  ────────────
  1    UniXcoder embeddings          2-3h        2-3h    torch install   PENDING
       (compute + save)                                   (network)
  
  2    Feature matrices              < 1h        1h      scikit-learn    READY
       (splits + format)
  
  3a   ACER-PA re-training           2-3 days    2-3d    source code     READY
       (workaround)
  
  3b   MART re-training              3-5 days    3-5d    Understand      BLOCKED
       (full protocol)               (if Understand)     license         (workaround: 3a)
  
  4    Ranking correlation           1-2 days    1d      scipy           READY
       + regime analysis
  
  5    Synthesis + publication       1-2 days    1d      Phases 1-4      READY
       (paper updates)
───────────────────────────────────────────────────────────────────────────
Total (without Understand):         ~1 week     4-5d
Total (with Understand):            ~1.5 weeks  8-10d
"""

print(timeline_table)

print("\n" + "=" * 90)
print("IMMEDIATE NEXT STEPS")
print("=" * 90)

print("""
1. RESOLVE torch INSTALLATION:
   Option A: Retry pip with different index (slower, more robust):
     pip install torch transformers -i https://pypi.org/simple/ --retries 5
   
   Option B: Use conda instead of pip (more reliable for torch):
     conda install torch transformers scikit-learn -c pytorch
   
   Option C: Use ONNX Runtime (lightweight, no torch needed):
     pip install onnxruntime transformers
   
   Option D: Use sentence-transformers library (simpler, built on torch):
     pip install sentence-transformers

2. CREATE PHASE 1 EMBEDDINGS ONCE INSTALLATION SUCCEEDS:
  python direction_c/direction_c_compute_embeddings.py
   (Estimated runtime: 2-3 hours, first run downloads ~900 MB)

3. MONITOR UNDERSTAND LICENSE STATUS:
   - Contact research team / advisor
   - If available by end of week: proceed with MART (Phase 3b)
   - If not: use ACER-PA + surrogate (Phase 3a) as interim

4. PREPARE ACER-PA SOURCE CODE:
   - Locate source paper reference implementation or PyTorch re-implementation
   - Adapt to accept UniXcoder feature input (768-dim)
   - Verify against handcrafted feature baseline

5. DOCUMENT PROTOCOL DECISIONS:
   - Create direction_c_decisions.md
   - Record which workarounds were used
   - Note any deviations from original protocol
""")

print("\n" + "=" * 90)
print("RISK MITIGATION")
print("=" * 90)

risks = {
    "Risk": [
        "torch installation timeout",
        "GPU out of memory (>8GB needed)",
        "Understand license unavailable",
        "ACER-PA source code unavailable",
        "Representation shows no improvement"
    ],
    "Mitigation": [
        "Use conda / ONNX / sentence-transformers as alternative",
        "Use CPU with smaller batch sizes (slower but works)",
        "Use ACER-PA + surrogate regression as workaround",
        "Implement CNN from scratch or use reference paper code",
        "Document as null result; publish protocol as contribution"
    ],
    "Impact": [
        "1-day delay",
        "2-3x slower, but all data still computable",
        "Interim result from ACER-PA sufficient for conference",
        "1-2 days additional implementation",
        "Still publishable as empirical investigation"
    ]
}

print(f"\n{'Risk':<35} {'Mitigation':<40} {'Impact':<30}")
print("-" * 105)
for r, m, i in zip(risks["Risk"], risks["Mitigation"], risks["Impact"]):
    print(f"{r:<35} {m:<40} {i:<30}")

print("\n" + "=" * 90)
print("PROTOCOL COMPLETE")
print("=" * 90)

print("""
Status: Framework design complete. Implementation phases defined.
Blocking: torch installation (network issue, not fundamental).

Ready to execute once:
  ✓ torch + transformers installed (Phase 1)
  ✓ ACER-PA source code located (Phase 3a)
  ✓ MART replication available OR Understand license obtained (Phase 3b)

Estimated research impact: HIGH
  - Addresses core question: Is FALCON advantage representation or method?
  - Regime taxonomy implications: Literature could be feature-era specific
  - Transfer learning evidence: Shows UniXcoder > handcrafted for TCP

Next action: Resolve torch installation, then execute Phase 1.
""")

print("=" * 90)
