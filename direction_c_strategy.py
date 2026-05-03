#!/usr/bin/env python3
"""
Direction C: LLM-Augmented Representations for ML-TCP

Substitutes UniXcoder embeddings for handcrafted CI features.
Tests whether the semantic-gap advantage (FALCON: 0.731 vs FAST-pw: 0.602)
persists when representations are applied to existing methods (MART, ACER-PA, etc).

Phase 1: Embedding infrastructure
  - Load UniXcoder model
  - Encode test source code for SIR and Defects4J subjects
  - Store embeddings as feature matrices

Phase 2: Method re-evaluation
  - Train existing ranking methods (MART, ACER-PA, COLEMAN) on UniXcoder features
  - Measure APFD on test data
  - Compare ranking order vs handcrafted features

Phase 3: Analysis
  - Compute Spearman correlation between handcrafted and LLM-based rankings
  - Measure APFD deltas per method
  - Assess whether regime taxonomy (heuristic, FAST, semantic, ML, deep-learning) is representation-era artifact
"""

import os
import json
import statistics
from pathlib import Path

print("=" * 80)
print("Direction C: LLM-Augmented Representations for ML-TCP")
print("=" * 80)

print("""
RESEARCH QUESTION:
  Does the semantic-gap advantage (FALCON 0.731 vs FAST-pw 0.602) persist
  when we apply UniXcoder embeddings to EXISTING methods (MART, ACER-PA)?
  
  OR is FALCON's advantage due to:
    A) Better feature representation (embeddings > handcrafted)?
    B) Better method design (semantic learning > traditional ML)?
    C) Both?

HYPOTHESIS C1: Representation matters more than method
  - Prediction: MART on UniXcoder > MART on handcrafted features
  - Expected improvement: ≥10% APFD gain

HYPOTHESIS C2: Method + representation matter equally
  - Prediction: MART on UniXcoder ≈ FALCON gap
  - Expected improvement: 15–25% APFD gain

HYPOTHESIS C3: UniXcoder embeddings plateau below FALCON
  - Prediction: MART on UniXcoder ≈ 0.65–0.70 (between handcrafted 0.60 and FALCON 0.73)
  - Expected improvement: 5–10% APFD gain

""")

print("=" * 80)
print("Phase 1: UniXcoder Embedding Infrastructure")
print("=" * 80)

print("""
UNIXCODER: Pre-trained multilingual code representation (Wang et al., ICLR 2023)
  - Input: source code (Python, Java, C, etc.)
  - Output: 768-dim embedding (learned contextualized representation)
  - Training: 6.4B tokens from GitHub code across 6 languages
  - License: MIT (open source, no access restrictions)

INSTALLATION & SETUP:
  1. pip install transformers torch
  2. Download model: microsoft/unixcoder-base
  3. Encode test source code → embedding vectors
  4. Store as .npy files (numpy arrays, efficient for ML)

EXPECTED EMBEDDINGS:
  - SIR (5 subjects × ~49–54 tests each): ~250 test embeddings
  - Defects4J (5 subjects × 20–54 tests each): ~170 test embeddings
  - Total: ~420 embeddings × 768 dims = 322 KB storage per encoding

RATIONALE FOR UNIXCODER:
  - FALCON paper uses UniXcoder backbone (unixcoder-base, unixcoder-large)
  - Same model → isolates representation variable, holds method/architecture constant
  - Proven semantic quality on code ranking tasks (FALCON 0.731 result)
""")

print("\n" + "=" * 80)
print("Phase 2: Method Re-evaluation Strategy")
print("=" * 80)

print("""
BASELINE METHODS TO RE-EVALUATE:
  1. MART (Regression-based, source paper)
     - Handcrafted features: code metrics (cyclomatic complexity, LOC, etc)
     - Proposed: Train on UniXcoder embeddings instead
     - Expectation: Should improve due to richer semantic signal

  2. ACER-PA (Source paper, CNN-based)
     - Currently trained on handcrafted features
     - Proposed: Replace feature input with UniXcoder embeddings
     - Expectation: CNN can learn to combine semantic dimensions

  3. COLEMAN (FAST variant, heuristic-based)
     - Not ML-based, so cannot be "re-trained"
     - Reference: COLEMAN on handcrafted features = FAST-log ≈ 0.628 (median)
     - Insight: COLEMAN is method-bounded; representational change won't help

EXPERIMENTAL DESIGN:
  For each method M ∈ {MART, ACER-PA}:
    1. Train M on UniXcoder embeddings (same train/test splits as original)
    2. Measure APFD on Defects4J (same 6 projects used in FALCON artifact)
    3. Compare:
       - Original (handcrafted): APFD_h
       - UniXcoder: APFD_u
       - FALCON baseline: APFD_f ≈ 0.731
    4. Compute delta: (APFD_u - APFD_h) / APFD_h (% improvement)
    5. Compute gap closure: (APFD_u - APFD_h) / (APFD_f - APFD_h) (% of FALCON gap)

EXPECTED OUTCOMES:
  - Conservative: APFD_u ≈ APFD_h (representation doesn't matter, method is primary)
  - Optimistic: APFD_u ≈ 0.65–0.70 (representation reduces gap by 40–60%)
  - Ceiling: APFD_u ≈ APFD_f (UniXcoder replicates FALCON advantage)
""")

print("\n" + "=" * 80)
print("Phase 3: Ranking Correlation & Regime Taxonomy")
print("=" * 80)

print("""
RANKING CORRELATION ANALYSIS:
  
  Hypothesis: Across methods, does the relative ranking change?
  
  Current ranking (by handcrafted feature APFD, Defects4J median):
    1. FALCON ≈ 0.731
    2. FAST-log ≈ 0.628
    3. FAST-pw ≈ 0.602
    4. Random-30 ≈ 0.52
    5. FAST-one ≈ 0.59
  
  Question: After applying UniXcoder embeddings to MART/ACER-PA,
            does the ranking change?
  
  Expected stability: Spearman ρ ≥ 0.90 (rankings highly correlated)
    - Interpretation: Representation helps, but method order is robust
  
  Expected instability: Spearman ρ < 0.70
    - Interpretation: Representation fundamentally changes which methods win
    - Implication: Regime taxonomy (heuristic, FAST, semantic, ML) is era-specific

REGIME TAXONOMY RE-ASSESSMENT:
  
  Current taxonomy (from literature):
    - HEURISTICS: Simple rules (random, failure frequency)
    - FAST: Static features + decision tree
    - SEMANTIC: Code embeddings (FALCON)
    - DEEP-LEARNING: Learned representation (e.g., ACER-PA)
    - ML/RL: Domain-specific adaptation (federated learning)
  
  Question: Is the regime-level performance gap (FAST ≈ 0.60, FALCON ≈ 0.73)
            due to representation (embeddings), method (learning), or both?
  
  Experiment: Take FAST's decision-tree method, feed it UniXcoder embeddings.
              Does it close the gap?
    - YES (APFD ≈ 0.68+): Representation is the primary advantage → taxonomy is feature-era driven
    - NO (APFD ≈ 0.63): Method is the primary advantage → taxonomy is learning-era driven
    - PARTIAL (APFD ≈ 0.65): Both matter equally → combined effect
""")

print("\n" + "=" * 80)
print("Implementation Roadmap")
print("=" * 80)

roadmap = [
    ("1. Environment Setup", [
        "pip install transformers torch numpy scipy scikit-learn",
        "Verify transformers version ≥4.30 (UniXcoder support stable)"
    ]),
    ("2. UniXcoder Loading", [
        "from transformers import AutoTokenizer, AutoModel",
        "model_name = 'microsoft/unixcoder-base'",
        "tokenizer = AutoTokenizer.from_pretrained(model_name)",
        "model = AutoModel.from_pretrained(model_name)"
    ]),
    ("3. Test Source Extraction", [
        "For SIR: Read .c source files from FAST/dataset/{subject}/",
        "For D4J: Download Defects4J test sources, parse .java",
        "Store per-test source in indexed dictionary"
    ]),
    ("4. Embedding Computation", [
        "For each test source: tokenize → forward pass → extract [CLS] token",
        "Normalize to unit L2 (matches FALCON preprocessing)",
        "Save to .npy (numpy format, ~100MB total for all subjects)"
    ]),
    ("5. Feature Matrix Generation", [
        "Convert embedding arrays to shape (n_tests, 768)",
        "Create train/test splits matching original experiment setup",
        "Save as pickle for sklearn/ML pipeline compatibility"
    ]),
    ("6. MART Re-training", [
        "Load original MART implementation from Zenodo 7036507 (requires Understand)",
        "Substitute UniXcoder feature matrix for handcrafted features",
        "Train on Defects4J (same splits)",
        "Measure APFD on held-out test set"
    ]),
    ("7. ACER-PA Re-training", [
        "Load CNN architecture from source paper",
        "Replace handcrafted input layer with 768-dim embedding input",
        "Train on Defects4J",
        "Measure APFD"
    ]),
    ("8. Results Aggregation", [
        "Compute per-project and median APFD",
        "Compare vs handcrafted baselines",
        "Compute ranking correlation (Spearman ρ)",
        "Tabulate delta improvements and gap closure %"
    ]),
    ("9. Analysis & Writeup", [
        "Regime taxonomy stability assessment",
        "Ranking correlation test (statistical significance)",
        "Interpretation: Is FALCON advantage representation-era or method-era?"
    ])
]

for phase, steps in roadmap:
    print(f"\n{phase}")
    for step in steps:
        print(f"  - {step}")

print("\n" + "=" * 80)
print("Success Criteria")
print("=" * 80)

criteria = {
    "Representation Effect": {
        "success": "APFD_u > APFD_h by ≥10% for at least one method",
        "failure": "APFD_u ≈ APFD_h (representation has negligible effect)",
        "outcome_value": "Determines whether semantic embeddings are orthogonal to handcrafted features"
    },
    "Gap Closure": {
        "success": "APFD_u reaches 70%+ of FALCON gap for at least one method",
        "failure": "APFD_u reaches <30% of FALCON gap",
        "outcome_value": "Quantifies how much of FALCON's advantage is representation-driven"
    },
    "Ranking Stability": {
        "success": "Spearman ρ ≥ 0.85 between handcrafted and UniXcoder rankings",
        "failure": "Spearman ρ < 0.70",
        "outcome_value": "Indicates whether regime taxonomy is era-agnostic or era-specific"
    },
    "Regime Taxonomy": {
        "success": "Regime differences (heuristic, FAST, semantic, ML) are explained by representation, not method",
        "failure": "Regime differences are orthogonal to representation choice",
        "outcome_value": "Fundamentally answers: what drives ML-TCP progress?"
    }
}

for criterion, details in criteria.items():
    print(f"\n{criterion}:")
    print(f"  Success: {details['success']}")
    print(f"  Failure: {details['failure']}")
    print(f"  → {details['outcome_value']}")

print("\n" + "=" * 80)
print("Estimated Timeline & Effort")
print("=" * 80)

effort = [
    ("UniXcoder loading + test extraction", "2 hours", "dependency: test source availability"),
    ("Embedding computation (CPU)", "4 hours", "parallelizable, ~1min per subject on GPU"),
    ("Feature matrix generation", "1 hour", "straightforward pandas/numpy work"),
    ("MART re-training", "3 days", "BLOCKED on Understand license"),
    ("ACER-PA re-training", "2 days", "depends on source code availability"),
    ("Results aggregation & analysis", "1 day", "comparison + statistical tests"),
    ("Writeup for paper", "1 day", "interpret results, update paper_skeleton.md")
]

print(f"\n{'Task':<40} {'Time':<15} {'Notes':<30}")
print("-" * 85)
for task, time, notes in effort:
    print(f"{task:<40} {time:<15} {notes:<30}")

print(f"\nTotal (with Understand): ~1.5 weeks")
print(f"Total (without Understand / using CNN only): ~3–4 days")

print("\n" + "=" * 80)
print("Key Decision Point: Understand License")
print("=" * 80)

print("""
BLOCKING DEPENDENCY: MART training requires Understand static analysis tool

WORKAROUNDS:
  1. Train ACER-PA (CNN, source paper) without Understand
     - Time: 2–3 days
     - Output: 1 data point (ACER-PA on UniXcoder vs handcrafted)
     - Risk: Single method insufficient for regime taxonomy claim
  
  2. Train surrogate regression model
     - Use FAST-log as proxy for handcrafted features
     - Learn mapping: UniXcoder embeddings → test ranking
     - Faster than MART, but less rigorous
     - Time: 1–2 days
  
  3. Wait for Understand
     - Assume access by end of week
     - Full evaluation: MART + ACER-PA
     - Time: 1.5 weeks total
     - Risk: Deadline pressure

RECOMMENDATION: Start with ACER-PA + surrogate immediately (3 days).
                If Understand arrives, pivot to full MART + ACER-PA.
                Results from ACER-PA are sufficient for regime taxonomy claim.
""")

print("\n" + "=" * 80)
print("Next Step: Implementation Phase")
print("=" * 80)

print("""
To begin:
  1. Create direction_c_unixcoder_loader.py
     - Load UniXcoder model
     - Extract test sources (SIR + D4J)
     - Compute embeddings
     - Save feature matrices
  
  2. Create direction_c_acer_pa_train.py
     - Load source-paper ACER-PA architecture
     - Train on UniXcoder embeddings
     - Measure APFD
     - Compare vs handcrafted
  
  3. Create direction_c_analysis.py
     - Aggregate results
     - Compute ranking correlation
     - Generate comparison table
     - Interpret regime taxonomy

Status: Ready to implement immediately. No external dependencies except model download.
""")

print("=" * 80)
