# Direction C: Expected Findings & Impact Analysis

**Document Purpose:** Pre-specify expected findings and their implications for the TCP field.  
**Audience:** Conference reviewers, research community  
**Date:** May 2, 2026

---

## Research Question (Precise Formulation)

**Primary:** Is the 21% APFD advantage of FALCON (0.731 vs FAST-pw 0.602 on Defects4J) primarily attributable to:
  1. **Representation:** UniXcoder embeddings encode better semantics than handcrafted features?
  2. **Method:** FALCON's learning strategy (semantic-aware objectives) better optimizes test ranking?
  3. **Both:** Representation and method are complementary; neither alone closes the gap?

**Secondary:** Does the regime taxonomy (heuristic, FAST, semantic, ML, RL) reflect:
  - **Hypothesis A:** Inherent method categories that are representation-agnostic (robust taxonomy)?
  - **Hypothesis B:** Feature-generation eras that will shift as embeddings mature (era-specific)?

---

## Expected Findings Across Outcome Scenarios

### Scenario 1: Strong Representation Effect (Representation > Method)
**Prediction:** ACER-PA(UniXcoder) ≈ 0.68-0.70 (closes 40-60% of FALCON gap)

**Evidence:**
- ΔAPFD_ACER-PA ≥ 10% improvement from handcrafted to UniXcoder
- Bootstrap CIs for improvement don't cross zero
- Spearman ρ ≈ 0.90 (ranking stable; representation orthogonal to method)

**Interpretation:**
- UniXcoder embeddings are ~10% more informative than code metrics for test ranking
- The regime difference (FAST ≈ 0.60 vs semantic ≈ 0.70) is primarily representation-driven
- **Implication for field:** Investment in better embeddings > investment in complex methods
- **Implication for taxonomy:** Heuristic/FAST/semantic categories are era-dependent; will shift with embeddings

**Publication Frame:**
> "Semantic code embeddings provide orthogonal information to traditional metrics, improving TCP APFD by ~10% when integrated into existing methods. This suggests the primary advantage of semantic-based approaches is representation quality, not learning algorithm sophistication."

### Scenario 2: Moderate Representation Effect (Balanced)
**Prediction:** ACER-PA(UniXcoder) ≈ 0.64-0.66 (closes 20-30% of FALCON gap)

**Evidence:**
- ΔAPFD_ACER-PA ≈ 5-7% improvement (modest but significant)
- Ranking reordering occurs for some methods (Spearman ρ ≈ 0.75-0.85)
- FALCON still dominates despite representation upgrade

**Interpretation:**
- Representation improvement is measurable but non-dominant
- Method design (how embeddings are integrated) matters nearly as much as embeddings themselves
- FALCON's advantage is partly representation (UniXcoder), partly method (semantic optimization objectives)
- **Implication for field:** Both embeddings and learning strategy are critical; neither is sufficient alone
- **Implication for taxonomy:** Semantic methods form a distinct regime, not just an era-specific improvement

**Publication Frame:**
> "While semantic embeddings improve upon handcrafted features (+5-7% APFD), they account for only ~30% of FALCON's 21% advantage over FAST. This suggests that TCP progress requires both better representations (embeddings) and methods adapted to leverage them (semantic learning objectives)."

### Scenario 3: Weak Representation Effect (Method Dominates)
**Prediction:** ACER-PA(UniXcoder) ≈ 0.60-0.62 (closes <10% of FALCON gap)

**Evidence:**
- ΔAPFD_ACER-PA ≈ 0-2% improvement (negligible or absent)
- No significant ranking reordering (Spearman ρ ≥ 0.95)
- FALCON advantage remains despite embedding upgrade

**Interpretation:**
- UniXcoder vs handcrafted features is not the primary differentiator
- FALCON's advantage is algorithmic, not representational
- Regime differences (heuristic, FAST, semantic) are method-era, not feature-era dependent
- **Implication for field:** Focus on better learning algorithms, not just embeddings
- **Implication for taxonomy:** Semantic methods (FALCON, ACER-PA) form distinct regime regardless of representations

**Publication Frame:**
> "Despite upgrading features to semantic embeddings, ACER-PA shows minimal improvement over handcrafted baselines. This indicates that FALCON's advantage over FAST-style methods arises from algorithmic sophistication (semantic-aware learning objectives), not representational improvements. The TCP regime taxonomy is robust to representation choice."

---

## Per-Project Variation Analysis

**Expected Pattern:** Even if overall median shows weak representation effect, individual projects may vary.

Example findings:
- **Closure (102 bugs, sparse faults):** Embeddings may help (signals from few failing tests; semantics bridges noise)
- **Chart (27 bugs, dense faults):** Embeddings may not help (clear failure signals from code metrics alone)
- **Math (8 bugs, dense faults):** Minimal representation benefit

**Publication Use:**
- Table: ΔAPFD per project (handcrafted vs UniXcoder)
- Figure: Density plot of ΔAPFD across projects
- Text: "Representation benefit is heterogeneous; sparse-label projects benefit from semantic embeddings (Closure +8%), while dense-label projects show minimal improvement (Math +1%)."

---

## Statistical Rigor Expected

### Confidence Intervals (Required)
- 95% bootstrap CIs on ΔAPFD per method per subject
- Report as [lower, upper] range
- Success: CIs don't cross zero (improvement is robust)
- Failure: CIs cross zero (improvement is noise)

### Ranking Correlation Test (Required)
- Spearman rank correlation (ρ) between handcrafted and UniXcoder method rankings
- Significance test: p < 0.05
- Effect interpretation:
  - ρ ≥ 0.90: Ranking extremely stable
  - 0.70 < ρ < 0.90: Moderate reordering
  - ρ ≤ 0.70: Substantial reordering

### Effect Sizes (Recommended)
- Cohen's d: (APFD_uni - APFD_hand) / σ
- Interpretation: d < 0.2 (negligible), 0.2-0.5 (small), 0.5-0.8 (medium), > 0.8 (large)

---

## Implications for Regime Taxonomy

**Current Taxonomy (Literature-Based):**
```
Regime      Method Type       APFD Range (SIR)    APFD Range (D4J)   Feature Era
──────────  ────────────      ────────────────    ────────────────   ────────────
Heuristic   Heuristic rules   0.50-0.70           0.45-0.55          N/A
FAST        Static features   0.70-0.85           0.55-0.65          Handcrafted (2010s)
Semantic    Code embeddings   0.80-0.95           0.65-0.75          Pretrained (2020s)
Deep-L      Learned reps      0.75-0.90           0.60-0.70          Learned (2020s)
ML/RL       Domain-adaptive   TBD                 TBD                TBD
```

**Direction C Test:** Are regime differences orthogonal to representation choice?

**If Representation Effect is Strong (Scenario 1):**
- Add new row: "Semantic Embeddings" as distinct feature tier
- Revised taxonomy: Heuristic → FAST → Semantic-Handcrafted → Semantic-Embeddings → Deep-L
- Implication: Regime taxonomy is feature-era dependent; maturation curve applies

**If Representation Effect is Weak (Scenario 3):**
- Regime taxonomy unchanged; orthogonal to representation
- Revised interpretation: Semantic methods form distinct learning-algorithm category
- Implication: Regime taxonomy is method-era dependent; robust to representations

---

## Threat-to-Validity Considerations

**Threat 1: Embedding Quality**
- Risk: UniXcoder embeddings may not be optimal for test ranking
- Mitigation: Use FALCON paper's same model; verify with dimensionality analysis
- Residual Risk: Unknown (would need comparison to other embeddings)

**Threat 2: Method Implementation**
- Risk: ACER-PA re-implementation may not match source paper
- Mitigation: Use source-paper code or reference implementation; verify on handcrafted baseline
- Residual Risk: Implementation artifacts could confound representation effect

**Threat 3: Train/Test Leakage**
- Risk: Embeddings computed globally (not per-split); potential information leak
- Mitigation: Use same 80/20 splits as original experiments; verify no train/test overlap
- Residual Risk: Embedding model (pre-trained on GitHub code) could contain project-specific knowledge

**Threat 4: Limited Project Coverage**
- Risk: D4J unavailable; SIR only
- Mitigation: Use FALCON-reported project results; substitute where embedding computation blocks
- Residual Risk: SIR results may not generalize to Java projects

---

## Success Criteria for Publication

**Minimum (Acceptable):**
1. Phase 1-2: Embeddings computed for ≥3 subjects; shapes verified
2. Phase 3: ACER-PA trained on UniXcoder; APFD measured
3. Phase 4: Spearman correlation computed; p-value reported
4. Finding: Any of Scenarios 1-3 above with statistical rigor

**Strong (Preferred):**
1. Embeddings computed for all 10 subjects
2. Both ACER-PA and MART trained (requires Understand)
3. Per-project heterogeneity documented
4. Bootstrap CIs on all findings; no CI crossing zero

**Exceptional (Publication + Impact):**
1. All above
2. Ranking correlation tested for statistical significance
3. Regime taxonomy updated with new figure/table
4. Mechanism analysis: why does representation help for sparse-label projects?

---

## Decision Logic for Publication

**Publication IF:**
- Phase 1 succeeds (embeddings computed)
- Phase 3 & 4 complete with statistical rigor (CIs, p-values)
- Finding matches one of Scenarios 1-3 with clear interpretation

**Conditional Publication IF:**
- Phase 1 succeeds on SIR only (D4J unavailable)
- Phase 3-4 complete on SIR subset
- Include caveat: "Results on C subjects; Java generalization deferred"

**Defer IF:**
- Phase 1 fails (torch unavailable; ONNX/fallback exhausted)
- Phase 3 incomplete (ACER-PA unavailable; MART blocked on Understand)
- Insufficient statistical evidence for any scenario

---

## Word Budget for Paper

**Target:** Section 5.3 (LLM Representations)

| Subsection | Content | Words |
|---|---|---|
| 5.3.1 | Research question + hypotheses | 150 |
| 5.3.2 | UniXcoder infrastructure + dataset | 150 |
| 5.3.3 | Results (APFD, ranking correlation) | 200 |
| 5.3.4 | Interpretation (which scenario?) | 150 |
| 5.3.5 | Regime taxonomy implications | 150 |
| 5.3.6 | Threats to validity | 100 |
| **Total** | | **900** |

---

## Example Figure: Expected Results

```
ACER-PA Performance: Handcrafted vs UniXcoder Embeddings
(Defects4J, 6 projects, 95% CI)

                  Handcrafted    UniXcoder    Δ APFD    % Gap Closed
────────────────  ───────────    ──────────   ────────  ──────────────
Chart             0.48 ± 0.15    0.52 ± 0.12  +0.04     12%
Closure           0.51 ± 0.18    0.59 ± 0.15  +0.08     40%
Lang              0.43 ± 0.14    0.48 ± 0.13  +0.05     18%
Math              0.55 ± 0.16    0.56 ± 0.14  +0.01     3%
Mockito           0.62 ± 0.12    0.65 ± 0.11  +0.03     11%
Time              0.50 ± 0.17    0.54 ± 0.14  +0.04     14%
────────────────  ───────────    ──────────   ────────  ──────────────
Median            0.50           0.54         +0.04     18%
FALCON            (baseline)     (baseline)   (goal)    (Scenario 2)

Interpretation:
- Representation provides modest 5-7% improvement overall
- Heterogeneous per-project (Closure 40%, Math 3%)
- Sparse-label projects (Closure) benefit more from embeddings
- Total gap closure: 18% of FALCON advantage (from 60→64 APFD)
- Implication: Both representation AND method matter (Scenario 2)
```

---

## Next Steps

1. **Installation (ongoing):** sentence-transformers install
2. **Phase 1 (2-3h):** Compute embeddings
3. **Phase 2 (<1h):** Generate feature matrices
4. **Phase 3a (2-3d):** Train ACER-PA
5. **Phase 4 (1d):** Ranking correlation
6. **Synthesis (1d):** Update manuscript/paper_skeleton.md

**Expected publication date:** May 10, 2026 (pending Understand access for full MART evaluation).

