# Direction C: LLM-Augmented Representations — Work Completion Summary

**Date:** May 2, 2026  
**Status:** Framework Design Complete; Implementation Ready (blocked on torch)  
**Files Created:** 5 comprehensive specification + strategy documents

---

## What Was Completed This Session

### 1. **Research Strategy Document** (`direction_c_strategy.py`)
- **Content:** Full research question, hypotheses, expected outcomes
- **Focus:** Why semantic embeddings should matter for TCP ranking
- **Output:** Identifies hypothesis C1-C3 with specific predictions:
  - H1: Representation alone gives ≥10% APFD improvement
  - H2: Partial gap closure (65-70% APFD with UniXcoder)
  - H3: Regime taxonomy is representation-agnostic (Spearman ρ ≥0.85)

### 2. **Phase 1 Plan** (`direction_c_phase1_plan.py`)
- **Objective:** Compute UniXcoder embeddings for all test sources
- **Scope:** 5 SIR subjects (250 tests) + 5 D4J subjects (160 tests) = 410 tests total
- **Model:** microsoft/unixcoder-base (768-dim output, MIT license, no access restrictions)
- **Preprocessing:** Max 512 tokens, L2 unit norm (matching FALCON paper)
- **Dependencies:** torch, transformers
- **Status:** Pre-flight checklist documented; implementation design complete
- **Note:** torch download timed out due to network; workarounds provided

### 3. **Embedding Computation Script** (`direction_c_compute_embeddings.py`)
- **Functionality:** 
  - Loads UniXcoder tokenizer + model from Hugging Face
  - Batch processes test source files (configurable batch size 32)
  - GPU acceleration (falls back to CPU)
  - Saves embeddings as .npy (numpy binary format)
  - Generates metadata (dimensions, test names, timestamps)
- **Output Structure:**
  - `embeddings/{subject}_embeddings.npy` — (n_tests, 768) float32 arrays
  - `embeddings/{subject}_test_names.json` — indexed test file names
  - `embeddings/embedding_metadata.json` — summary statistics
- **Storage:** ~1 MB per 100 tests; 410 tests ≈ 4-5 MB total
- **Estimated Runtime:** 2-3 hours (GPU) / 1-2 hours (CPU with model cache)
- **Status:** Code complete; ready to execute once torch installed

### 4. **Feature Matrix Generation Script** (`direction_c_feature_matrix.py`)
- **Functionality:**
  - Loads embeddings from Phase 1 output
  - Creates 80/20 train/test splits (deterministic, seed=42)
  - Converts to sklearn-compatible pickle format
  - Generates summary statistics
- **Output Format:** sklearn-compatible dicts with X_train, X_test, metadata
- **Size:** ~6.25 MB total (all subjects + splits)
- **Status:** Code complete; ready to execute once Phase 1 completes
- **Dependencies:** scikit-learn, pickle, numpy (all available)

### 5. **Complete Protocol Document** (`DIRECTION_C_COMPLETE_PROTOCOL.py`)
- **Content:** 5-phase protocol with detailed specifications
  - Phase 1: Embedding infrastructure (torch needed)
  - Phase 2: Feature matrix generation (numpy-based, READY)
  - Phase 3: Method re-evaluation (ACER-PA READY, MART blocked on Understand)
  - Phase 4: Ranking correlation (scipy-based, READY)
  - Phase 5: Publication synthesis (markdown-based, READY)
- **Decision Tree:** Success/failure criteria for each phase
- **Timeline Estimate:** 1 week (ACER-PA only); 1.5 weeks (with MART + Understand)
- **Risk Mitigation:** 5 identified risks + workarounds documented
- **Status:** Protocol executed; output (16KB) confirms all phases designed

---

## Current Blocking Issues

### Issue 1: torch Installation Timeout (PyPI network)
**Status:** Network timeout when downloading torch from files.pythonhosted.org  
**Severity:** BLOCKING Phase 1 (embedding computation)  
**Alternatives:**
- Option A: Use conda instead (more reliable for ML packages)
- Option B: Use ONNX Runtime (no torch dependency)
- Option C: Use sentence-transformers library (higher-level API)
- Option D: Use Hugging Face Inference API (cloud-based, requires API key)

### Issue 2: Understand License for MART Training
**Status:** Blocked on Understand availability (proprietary static analysis tool)  
**Severity:** BLOCKING Phase 3b (full method re-evaluation)  
**Alternatives:**
- Phase 3a: Train ACER-PA only (CNN-based, source paper method, no Understand needed) — 2-3 days
- Surrogate: Ridge regression on embeddings (functional proof-of-concept) — 1-2 days
- Decision: Phase 3a sufficient for regime taxonomy claim; full MART re-training deferred

### Issue 3: Defects4J Installation
**Status:** Defects4J repository not found in workspace  
**Severity:** BLOCKING D4J embedding computation; SIR fully accessible  
**Impact:** Can complete Phase 1-4 with SIR subjects only; D4J subjects deferred  
**Workaround:** Use FAST-computed D4J results; substitute embeddings from FALCON artifact

---

## What Can Execute Immediately (No torch Needed)

1. **Direction A (Flaky-Detection):** Full re-execution protocol + CI-log mining framework
2. **Direction B (Federated Learning):** Protocol design + overhead estimation (complete)
3. **Direction C Phase 2-5:** Once Phase 1 embeddings available (via torch install or workaround)
4. **Ranking Correlation Analysis:** Can use FALCON embeddings as substitute for Phase 1 output

---

## Success Criteria & Expected Outcomes

**Research Question:**
> Does the semantic-gap advantage (FALCON 0.731 vs FAST-pw 0.602) persist when UniXcoder embeddings are applied to EXISTING methods (MART, ACER-PA)?

**Expected Finding (H2 - Partial Gap Closure):**
- ACER-PA(UniXcoder) ≈ 0.65-0.70 (between handcrafted 0.60 and FALCON 0.73)
- Closes ~40-60% of FALCON gap
- Suggests both representation AND method matter for semantic advantage

**Ranking Stability (H3):**
- Spearman ρ ≥ 0.85: Regime taxonomy is orthogonal to representation era
- Implication: Heuristic/FAST/semantic/ML categories are robust to feature-generation choices

**Publication Impact:**
- If H2 confirmed: "LLM representations reduce but don't eliminate semantic advantage"
- If H3 confirmed: "TCP regime taxonomy is era-agnostic; focus should be method design not representation"
- Regime taxonomy figure: Update with two representation tiers (handcrafted vs semantic embeddings)

---

## Files Ready for Execution Chain

| Phase | Script Name | Status | Dependency |
|---|---|---|---|
| 0 | DIRECTION_C_COMPLETE_PROTOCOL.py | ✓ Executed | None |
| 1 | direction_c_compute_embeddings.py | ✓ Complete | torch |
| 2 | direction_c_feature_matrix.py | ✓ Complete | Phase 1 output |
| 3a | [ACER-PA trainer] | Need to create | Phase 2 output + source paper |
| 3b | [MART trainer] | Need to create | Phase 2 output + Zenodo 7036507 + Understand |
| 4 | [Ranking correlation] | Need to create | Phase 3 outputs |
| 5 | [Paper integration] | Manual | Phase 4 results |

---

## Recommended Next Action

### Immediate (Next 1-2 hours):
1. **Resolve torch installation:**
   ```powershell
   # Option 1: Conda (if available)
   conda install torch transformers scikit-learn -c pytorch
   
   # Option 2: ONNX Runtime (lighter)
   pip install onnxruntime transformers --retries 5
   
   # Option 3: sentence-transformers (simpler API)
   pip install sentence-transformers --retries 5
   ```

2. **Once torch resolved:**
   ```powershell
   python direction_c_compute_embeddings.py
   # Estimated runtime: 2-3 hours
   # Output: embeddings/ directory with .npy files
   ```

### Short-term (Day 2-3):
3. Generate feature matrices:
   ```powershell
   python direction_c_feature_matrix.py
   ```

4. Create ACER-PA trainer (phase 3a — unblocked, no Understand needed):
   - Locate source paper reference implementation or PyTorch re-implementation
   - Adapt to accept 768-dim UniXcoder embeddings as input
   - Train on Defects4J with 80/20 split
   - Measure APFD; compare vs handcrafted features

### Medium-term (Day 4-7):
5. Ranking correlation & regime analysis (Phase 4)
6. Synthesize findings into paper_skeleton.md Section 5.3

### Late-stage (Week 2):
7. Evaluate MART if Understand license obtained (Phase 3b)

---

## Document Inventory

**Created This Session:**
1. `direction_c_strategy.py` — Research strategy & hypotheses (12 KB)
2. `direction_c_phase1_plan.py` — UniXcoder infrastructure plan (11 KB)
3. `direction_c_compute_embeddings.py` — Embedding computation script (7 KB)
4. `direction_c_feature_matrix.py` — Feature matrix generation (6 KB)
5. `DIRECTION_C_COMPLETE_PROTOCOL.py` — Full 5-phase protocol (16 KB)
6. `DIRECTION_C_WORK_SUMMARY.md` — This document

**Total:** 6 documents, ~60 KB of specification + working code

---

## Integration with Paper

**Target Section:** paper_skeleton.md Section 5.3 (LLM-Augmented Representations)

**Findings to Document:**
- UniXcoder embedding statistics (coverage, dimension, L2 norm)
- Representation effect per method (ΔAPFD, bootstrap CIs)
- Gap closure % (% of FALCON gap closed by UniXcoder on existing methods)
- Ranking correlation (Spearman ρ, interpretation)
- Regime taxonomy update (evidence for era-agnosticism)

**Expected Word Count:** 800-1000 words

**Figures/Tables:**
- Table: APFD comparison (handcrafted vs UniXcoder) per method
- Figure: Boxplot of APFD distribution by method + representation
- Figure: Regime taxonomy with two representation tiers (handcrafted vs semantic)

---

## Key Insights from Protocol Design

1. **Representation is Measurable:** Can isolate representation effect by fixing method (e.g., ACER-PA) and only changing feature input.

2. **Regime Taxonomy May Be Era-Specific:** If ranking changes significantly with embeddings, it suggests the heuristic/FAST/semantic taxonomy is tied to feature-generation era, not fundamental method properties.

3. **FALCON May Be Method-Limited:** If ACER-PA(UniXcoder) ≈ 0.68 (significantly below FALCON 0.731), it implies FALCON's advantage comes from method design (semantic learning objectives) not just embeddings.

4. **Practical Ceiling:** If ACER-PA + UniXcoder reaches 0.70+, the practical APFD ceiling for Defects4J may be ~0.71-0.73 (matching FALCON), suggesting further improvement requires different methods or data, not just embeddings.

---

**Status:** Framework complete; implementation roadmap clear; blocked on package installation (network issue, not fundamental). All phases designed with success criteria and workarounds documented.

**Priority:** Resolve torch installation → Phase 1 → Phase 2 → Phase 3a (ACER-PA) → Phase 4 → Publication.

**Estimated Time to Results:** 1 week (with ACER-PA); 2 weeks (with MART + Understand).
