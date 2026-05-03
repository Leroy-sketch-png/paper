# Manuscript: Label Realism, Data Governance, and Representation Shift

**File:** `paper_manuscript.tex`  
**Generated from:** `paper_skeleton.md`  
**Last updated:** May 3, 2026  
**Status:** Submission-ready draft

---

## Quick Start

### Compile to PDF (requires LaTeX installation)

```bash
pdflatex paper_manuscript.tex
# or
xelatex paper_manuscript.tex
```

Repeat compile twice to resolve cross-references:
```bash
pdflatex paper_manuscript.tex
pdflatex paper_manuscript.tex
```

### Online Compilation

If LaTeX is not installed locally, use **Overleaf** (free):
1. Go to https://www.overleaf.com/
2. Create new project → Upload project from file
3. Upload `paper_manuscript.tex`
4. Click "Recompile"

---

## Document Structure

```
1. Introduction
   1.1 Problem Setting and Opportunity
   1.2 Realism Gaps That Motivate This Paper
   1.3 Research Objective
   1.4 Contributions
   1.5 Paper Roadmap

2. Background and Related Work
   2.1 TCP in Continuous Integration
   2.2 Flaky Tests in CI
   2.3 Transfer Learning and Privacy in ML-TCP
   2.4 Representations for TCP
   2.5 Mobile and Android CI

3. Study Design
   3.1 Research Questions
   3.2 Datasets
   3.3 Baselines (Six-Tier Grid)
   3.4 Metrics

4. Direction A: Flaky-Test-Aware TCP
   4.1 Motivation
   4.2 Approach
   4.3 Expected Findings
   4.4 Tables and Figures

5. Direction B: Federated Pretraining
   5.1 Motivation
   5.2 Approach
   5.3 Expected Findings
   5.4 Tables and Figures

6. Direction C: LLM-Augmented Representations
   6.1 Motivation
   6.2 Approach
   6.3 Results (Proxy Representation Experiment)
      - Table C1: APFD by subject and ranker
      - Table C2: Ranking correlation (Spearman ρ)
   6.4 Tables and Figures

7. Direction D: Android/Mobile CI Replication
   7.1 Motivation
   7.2 Approach
   7.3 Expected Findings
   7.4 Tables and Figures

8. Discussion
   8.1 The Label-Realism Problem
   8.2 Transfer Beyond Open Source
   8.3 Are Method Rankings Feature-Era Artifacts?
   8.4 External Validity: Mobile CI as the Hard Case
   8.5 Threats to Validity

9. Conclusion
```

---

## Key Results Included

**Section 6.3 — Direction C Results (Executed)**
- Table C1: APFD comparison (Centroid, Linear, MLP rankers vs FAST-pw) across 5 SIR subjects
- Table C2: Spearman ρ ranking correlation between BPE embeddings and FAST-pw orderings
- Statistical summary: Mean ΔAPFD = −0.3283 (95% CI [−0.4866, −0.1699]), Cohen's d = −1.94

**Other sections (Sections 4-5, 7):**
- Expected Findings, hypotheses, and experiment protocols
- Not yet executed (marked as placeholders in text)

---

## To Update or Regenerate

If you modify `paper_skeleton.md`:

```bash
python generate_latex_manuscript.py
```

This overwrites `paper_manuscript.tex` with updated content.

---

## Submission Preparation Checklist

- [ ] Review compiled PDF for formatting and page breaks
- [ ] Fill in author/affiliation block (currently blank)
- [ ] Add venue-specific references formatting (IEEE/ACM/Springer)
- [ ] Replace placeholder `[TBD]` references with actual citations
- [ ] Verify all table and figure captions are present
- [ ] Check for widow/orphan lines and manual breaks if needed
- [ ] Proof-read for typos and consistency

---

## Known Limitations

- LaTeX must be installed locally or compiled via Overleaf
- Requires `pdflatex` or `xelatex` engine
- Default uses Times Roman font via `times` package (portable)
- No external figures included (table-only document currently)
- References section is a stub (add BibTeX `.bib` file if needed)

---

## File Organization

```
research/
├── paper_manuscript.tex          ← Main submission file
├── generate_latex_manuscript.py  ← Regenerator (if you edit paper_skeleton.md)
├── paper_skeleton.md             ← Source markdown (do not edit after .tex generation unless you regenerate)
├── MANUSCRIPT_README.md          ← This file
└── phase4_results/
    ├── phase4_correlation.json   ← Direction C results (Table C1/C2 data source)
    └── section_5_3_draft.md      ← Direction C synthesis (incorporated into Section 6.3)
```

---

**For questions or edits:** Modify `paper_skeleton.md`, then regenerate with `python generate_latex_manuscript.py`.
