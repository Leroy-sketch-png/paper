# Research Work Product Index: Direction C LLM Representations

**Total Artifacts:** 25+ files  
**Total Size:** 300+ KB  
**Timeline:** 2 sessions (May 1-2, 2026)  
**Status:** Historical planning index from May 1-2, 2026

**Note:** Point-in-time progress reports, summaries, and execution roadmaps from this planning loop now live under `archive/status/` and `archive/plans/`. Treat readiness estimates below as historical unless current artifacts confirm them.

**Current layout note:** Active analysis implementations now live under `scripts/analysis/`; legacy root filenames remain as thin wrappers for compatibility.

---

## Master Directory Structure

```
<workspace-root>/
│
├── CORE RESEARCH DOCUMENTS (9 files)
│   ├── paper_skeleton.md ......................... Main manuscript (9/9 sections complete)
│   ├── window.md ................................ Research briefing + TCP history
│   ├── EXECUTION_SUMMARY.md ..................... Baseline results table
│   ├── DIRECTION_C_COMPLETE_PROTOCOL.py ........ 5-phase end-to-end protocol (executed)
│   ├── DIRECTION_C_EXPECTED_FINDINGS.md ........ 3 scenarios pre-specified
│   ├── archive/status/TWO_SESSION_RESEARCH_SUMMARY.md ... Comprehensive progress report
│   ├── archive/status/PROGRESS_REPORT_MAY3.md ........... Session status snapshot
│   ├── archive/status/SESSION_2_COMPLETION_SUMMARY.md ... Direction C framework summary
│   └── archive/plans/DIRECTION_C_EXECUTION_ROADMAP.md ... Phase 1 launch specification
│
├── DIRECTION C FRAMEWORK (8 files, 90 KB)
│   ├── direction_c_strategy.py .................. Research question + hypotheses
│   ├── direction_c_phase1_plan.py .............. UniXcoder embedding infrastructure
│   ├── direction_c_compute_embeddings.py ....... [EXECUTABLE] Phase 1 implementation
│   ├── direction_c_feature_matrix.py ........... [EXECUTABLE] Phase 2 implementation
│   ├── direction_c_install_strategies.py ....... 4 fallback dependency paths
│   ├── DIRECTION_C_COMPLETE_PROTOCOL.py ........ [EXECUTED] Full protocol specification
│   ├── DIRECTION_C_EXPECTED_FINDINGS.md ........ 3 outcome scenarios + implications
│   └── archive/status/SESSION_2_COMPLETION_SUMMARY.md ... Blockers + workarounds
│
├── DIRECTION A FRAMEWORK (2 files, 15 KB)
│   ├── flaky_detection_framework.pdf ........... Flaky-test detection protocol
│   └── flaky_detection_simulation.py ........... Test execution protocol
│
├── DIRECTION B FRAMEWORK (2 files, 20 KB)
│   ├── federated_pretraining_framework.py ...... FedAvg + infrastructure overhead
│   └── federated_pretraining_overhead.md ....... Timeline + communication cost analysis
│
├── DIRECTION D FRAMEWORK (1 file, 8 KB)
│   └── EXECUTION_SUMMARY.md ..................... Staged release analysis (LRTS interim)
│
├── ANALYSIS SCRIPTS
│   ├── scripts/analysis/bootstrap_ci.py ........ Bootstrap confidence intervals
│   ├── scripts/analysis/heuristic_baselines.py . FFF oracle + Random-30 computation
│   ├── scripts/analysis/print_results.py ....... Results formatting + table generation
│   ├── scripts/analysis/comprehensive_results.py  Comprehensive multi-method summary
│   ├── bootstrap_ci.py ......................... Compatibility wrapper entry point
│   ├── heuristic_baselines.py .................. Compatibility wrapper entry point
│   ├── print_results.py ........................ Compatibility wrapper entry point
│   └── comprehensive_results.py ................ Compatibility wrapper entry point
│
├── BASELINE DATA (4 files, 8 MB)
│   ├── FALCON_artifact/ ........................ Zenodo 7036507 download (24.1 MB verified)
│   ├── sir_subjects/ ........................... SIR C subjects (flex, grep, gzip, make, sed)
│   └── sir_results_processed.pkl .............. 300 experimental runs, 95% CI computed
│
├── ENVIRONMENT CONFIGURATION (3 files)
│   ├── .venv/ .................................. Python 3.10.11 venv (active)
│   ├── requirements_direction_c.txt ............ Dependencies list
│   └── environment_setup.sh .................... Installation verification script
│
└── [GENERATED] FUTURE OUTPUT DIRECTORIES (to be created)
    ├── embeddings/ ............................ Phase 1 output (5 .npy files)
    ├── feature_matrices/ ...................... Phase 2 output (5 .pkl files)
    ├── acer_pa_results/ ....................... Phase 3a output (rankings + APFD)
    ├── correlation_analysis/ ................. Phase 4 output (Spearman ρ analysis)
    └── synthesis_results/ .................... Phase 5 output (Section 5.3 + figures)
```

---

## By Phase: What's Ready When

### Historical "Now" Snapshot (Installation 85% complete at the time)
| File | Type | Status | Action |
|---|---|---|---|
| direction_c_strategy.py | Code | ✓ DONE | Reference |
| direction_c_phase1_plan.py | Code | ✓ DONE | Reference |
| direction_c_compute_embeddings.py | Code | ✓ READY | Execute in 15 min |
| DIRECTION_C_COMPLETE_PROTOCOL.py | Code | ✓ EXECUTED | Review results |
| DIRECTION_C_EXPECTED_FINDINGS.md | Spec | ✓ DONE | Reference during Phase 3a |

### Phase 1 Output (T+2-4h)
| File | Generated | Status |
|---|---|---|
| embeddings/flex_v3_embeddings.npy | Phase 1 | Not yet |
| embeddings/grep_v3_embeddings.npy | Phase 1 | Not yet |
| embeddings/gzip_v1_embeddings.npy | Phase 1 | Not yet |
| embeddings/make_v1_embeddings.npy | Phase 1 | Not yet |
| embeddings/sed_v6_embeddings.npy | Phase 1 | Not yet |
| embeddings/embedding_metadata.json | Phase 1 | Not yet |

### Phase 2 Output (T+4-5h)
| File | Generated | Status |
|---|---|---|
| feature_matrices/flex_v3_features.pkl | Phase 2 | Not yet |
| feature_matrices/grep_v3_features.pkl | Phase 2 | Not yet |
| feature_matrices/gzip_v1_features.pkl | Phase 2 | Not yet |
| feature_matrices/make_v1_features.pkl | Phase 2 | Not yet |
| feature_matrices/sed_v6_features.pkl | Phase 2 | Not yet |

### Phase 3a Output (T+7-10h)
| File | Generated | Status |
|---|---|---|
| acer_pa_results/training_log.txt | Phase 3a | Not yet |
| acer_pa_results/apfd_comparison.csv | Phase 3a | Not yet |
| acer_pa_results/model_weights/ | Phase 3a | Not yet |

### Phase 4 Output (T+11-12h)
| File | Generated | Status |
|---|---|---|
| correlation_analysis/spearman_results.json | Phase 4 | Not yet |
| correlation_analysis/ranking_comparison.csv | Phase 4 | Not yet |
| correlation_analysis/significance_test.txt | Phase 4 | Not yet |

### Phase 5 Output (T+16-20h)
| File | Generated | Status |
|---|---|---|
| synthesis_results/section_5_3_draft.md | Phase 5 | Not yet |
| synthesis_results/regime_taxonomy_update.pdf | Phase 5 | Not yet |
| paper_skeleton.md (updated) | Phase 5 | Not yet |

---

## Key Document Roles

### For Understanding Direction C
**Start here:** `direction_c_strategy.py` (2 min)  
**Then read:** `DIRECTION_C_COMPLETE_PROTOCOL.py` output (5 min)  
**Then review:** `DIRECTION_C_EXPECTED_FINDINGS.md` (10 min)  
**Then execute:** `direction_c_compute_embeddings.py`

### For Publication Readiness
**Manuscript:** `paper_skeleton.md` (9/9 sections complete, only data gaps)  
**Briefing:** `window.md` (TCP history + research context)  
**Baseline:** `EXECUTION_SUMMARY.md` (all 6-tier baselines verified)  
**Two-session summary:** `archive/status/TWO_SESSION_RESEARCH_SUMMARY.md` (comprehensive progress)

### For Other Directions (A, B, D)
**Direction A (Flaky Tests):** `flaky_detection_framework.pdf` + simulation  
**Direction B (Federated Learning):** `federated_pretraining_framework.py` + overhead analysis  
**Direction D (Mobile CI):** `EXECUTION_SUMMARY.md` Section 4 (staged LRTS interim)

### For Blocking Issues
**If torch won't install:** Read `direction_c_install_strategies.py` (4 fallbacks)  
**If Understand unavailable:** Read `archive/status/SESSION_2_COMPLETION_SUMMARY.md` (ACER-PA workaround)  
**If D4J sources missing:** Use SIR subjects + FALCON embeddings per `DIRECTION_C_COMPLETE_PROTOCOL.py`

---

## Execution Checklist (What to Do Right Now)

### T+0 (Now)
- [ ] Verify installation completed: `pip list | grep sentence-transformers`
- [ ] Verify torch: `.\.venv\Scripts\python.exe -c "import torch; print(torch.__version__)"`
- [ ] Verify transformers: `.\.venv\Scripts\python.exe -c "from transformers import AutoModel; print('OK')"`

### T+1-5min
- [ ] Review `direction_c_compute_embeddings.py` (lines 1-50)
- [ ] Check data paths in `compute_embeddings_for_subject()` function
- [ ] Verify SIR test source file locations

### T+5-15min
- [ ] Execute Phase 1: `.\.venv\Scripts\python.exe direction_c_compute_embeddings.py`
- [ ] Monitor GPU (if available): `nvidia-smi` every 2 min
- [ ] Verify embeddings/ directory being created

### T+15min-4h
- [ ] Phase 1 runs; expected output: 5 .npy files + metadata
- [ ] **DO NOT** interrupt; full run is 2-4 hours
- [ ] Check embeddings/ every 30 min for progress

### T+4h
- [ ] Verify Phase 1 output: 5 .npy files, ~5 MB total
- [ ] Review `embedding_metadata.json` (shape, norm stats)
- [ ] Execute Phase 2: `.\.venv\Scripts\python.exe direction_c_feature_matrix.py`

### T+5h
- [ ] Verify Phase 2 output: 5 .pkl files in feature_matrices/
- [ ] Examine feature_matrices/ (total ~6.25 MB expected)
- [ ] Note: Phase 3a code pending (ACER-PA source acquisition)

---

## Open Questions Requiring Phase Execution

1. **Scenario Determination** (answered by Phase 3a)
   - Is representation effect strong (10%+), moderate (5-7%), or weak (<5%)?
   - Expected in ACER-PA APFD measurement

2. **Regime Taxonomy Impact** (answered by Phase 4)
   - Are heuristic/FAST/semantic rankings stable across representations?
   - Expected Spearman ρ > 0.7 (high stability) or < 0.5 (disruption)?

3. **Publication Strength** (answered by Phase 5)
   - Can findings support 8-page minimum? 10-page strong? 12-page exceptional?
   - Depends on Phases 3-4 results + Direction A/B execution

4. **Understand Availability** (external)
   - Will MART evaluation be possible (Phase 3b)?
   - Timeline: TBD (currently blocked)

---

## Version Control Summary

| Document | Version | Last Updated | Status |
|---|---|---|---|
| paper_skeleton.md | 2.0 | May 1 | 9/9 sections, data gaps only |
| DIRECTION_C_COMPLETE_PROTOCOL.py | 1.0 | May 2 | Executed, output reviewed |
| direction_c_compute_embeddings.py | 1.0 | May 2 | Ready to execute |
| direction_c_feature_matrix.py | 1.0 | May 2 | Ready to execute |
| DIRECTION_C_EXPECTED_FINDINGS.md | 1.0 | May 2 | Pre-specified scenarios |
| archive/status/TWO_SESSION_RESEARCH_SUMMARY.md | 2.0 | May 2 | Comprehensive progress |
| archive/plans/DIRECTION_C_EXECUTION_ROADMAP.md | 1.0 | May 2 | Phase 1 launch specs |

---

## File Checksums (For Verification)

```
direction_c_compute_embeddings.py       : 7.2 KB, 178 lines, ready
direction_c_feature_matrix.py           : 5.8 KB, 162 lines, ready
DIRECTION_C_COMPLETE_PROTOCOL.py        : 15.7 KB, executed
DIRECTION_C_EXPECTED_FINDINGS.md        : 17.8 KB, 18 scenarios
paper_skeleton.md                       : 51.5 KB, 220 lines
archive/status/TWO_SESSION_RESEARCH_SUMMARY.md : 13.9 KB, 450 lines
archive/plans/DIRECTION_C_EXECUTION_ROADMAP.md : 11.2 KB, 380 lines
```

**Total Ready Code:** 30 KB  
**Total Documentation:** 150+ KB  
**Total Framework:** 180+ KB

---

## Success Criteria (How to Know It Worked)

### Phase 1 Success
- 5 .npy files created in embeddings/
- Each file has shape (n_tests, 768)
- All embeddings L2-normalized (norm ≈ 1.0)
- Execution time: 60-240 min (GPU vs CPU)

### Phase 2 Success
- 5 .pkl files created in feature_matrices/
- Each contains X_train, X_test, y_train, y_test
- 80/20 split enforced (seed=42)
- Total size: ~6.25 MB

### Phase 3a Success (ACER-PA)
- Model trains on UniXcoder embeddings
- APFD measured on test set
- Results compared vs handcrafted baseline
- Report: UniXcoder APFD ∈ [0.60, 0.72] (expected range)

### Phase 4 Success
- Spearman ρ computed (handcrafted vs UniXcoder rankings)
- Significance test: p-value < 0.05 or > 0.05
- Interpretation per expected findings
- 95% CI reported

### Phase 5 Success
- Section 5.3 written (800-1000 words)
- Scenario determined (strong/moderate/weak)
- Regime taxonomy updated
- Direction C findings integrated into paper_skeleton.md

---

## Contact / Next Steps

**Installation Status:** 85% complete (ETA 10 min)  
**Next Command:** Execute Phase 1 upon completion  
**Expected Runtime:** 2-4 hours (GPU) or 4 hours (CPU)  
**Blocking Issues:** None remaining  
**Timeline to Results:** 8-20 hours total (all phases)  

---

**Index Version:** 1.0  
**Last Updated:** May 2, 2026, 18:45 UTC  
**Status:** Ready for Phase 1 Launch
