# Manuscript: Label Realism, Data Governance, and Representation Shift

**File:** `manuscript/paper_manuscript.tex`  
**Generated from:** `manuscript/paper_skeleton.md`  
**Last updated:** May 5, 2026  
**Status:** Submission-ready draft with formal references
**Target venue:** ISSTA

---

## Quick Start

### Preferred one-command build

From the workspace root:

```bash
python manuscript/build_submission_pdf.py
```

This regenerates `manuscript/paper_manuscript.tex` from `manuscript/paper_skeleton.md` and then rebuilds `manuscript/paper_manuscript.pdf`.

If no local LaTeX engine is installed, the script can only reuse an already up-to-date `manuscript/paper_manuscript.pdf`; otherwise it stops and you must compile with a local TeX installation or Overleaf.

### Compile to PDF (requires LaTeX installation)

```bash
cd manuscript
pdflatex paper_manuscript.tex
# or
xelatex paper_manuscript.tex
```

Repeat compile twice to resolve cross-references:
```bash
cd manuscript
pdflatex paper_manuscript.tex
pdflatex paper_manuscript.tex
```

### Online Compilation

If LaTeX is not installed locally, use **Overleaf** (free):
1. Go to https://www.overleaf.com/
2. Create new project → Upload project from file
3. Upload `paper_manuscript.tex` from the `manuscript/` folder
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
   4.3 Evidence Status and Publication Role

5. Direction B: Federated Pretraining
   5.1 Motivation
   5.2 Approach
   5.3 Evidence Status and Publication Role

6. Direction C: LLM-Augmented Representations
   6.1 Motivation
   6.2 Approach
   6.3 Results (Proxy Representation Experiment)
      - Table C1: APFD by subject and ranker
      - Table C2: Ranking correlation (Spearman ρ)
   6.4 Result Notes and Follow-up

7. Direction D: Android/Mobile CI Replication
   7.1 Motivation
   7.2 Approach
   7.3 Evidence Status and Publication Role

8. Discussion
   8.1 The Label-Realism Problem
   8.2 Transfer Beyond Open Source
   8.3 Are Method Rankings Feature-Era Artifacts?
   8.4 External Validity: Mobile CI as the Hard Case
   8.5 Deployment-Facing Conditional-Validity Matrix
   8.6 Threats to Validity

9. Conclusion
```

---

## Key Results Included

**Section 6.3 — Direction C Results (Executed)**
- Table C1: APFD comparison (Centroid, Linear, MLP rankers vs FAST-pw) across 5 SIR subjects
- Table C2: Spearman ρ ranking correlation between BPE embeddings and FAST-pw orderings
- Statistical summary: Mean ΔAPFD = −0.3283 (95% CI [−0.4866, −0.1699]), Cohen's d = −1.94

**Section 8.5 — Deployment-Facing Conditional-Validity Matrix**
- A practitioner-facing decision surface translating the four realism gaps into adoption guidance
- Explicit conditions under which the source-paper recommendation should be treated as trustworthy, qualified, or provisional

**Abstract / Conclusion refresh**
- The abstract now foregrounds the executed Direction C proxy result instead of implying four fully executed tracks
- The conclusion now ends with a lightweight adoption protocol for practitioners

**References / final-page state**
- The inline references section is now formalized in `manuscript/paper_skeleton.md` and emits a real bibliography in the generated LaTeX
- The generated PDF currently builds to 11 pages, and the final bibliography page has been stabilized under the IEEE-style output pipeline

**Other sections (Sections 4-5, 7):**
- Evidence-status framing and execution protocols for the unexecuted realism tracks
- Written to qualify benchmark recommendations without overstating current execution status

---

## Evidence Status Snapshot

- Executed in the current draft: FAST baselines on 10 subjects, artifact-verified FALCON summary extraction, IDoFT overlap analysis, and Direction C BPE-proxy results on 5 SIR subjects
- Protocol-backed but not fully executed: Direction A flaky-label cleaning measurements and Direction B federated pretraining retention study
- Staged extension: Direction D Android/mobile CI replication after dataset admission criteria are met

---

## To Update or Regenerate

If you modify `manuscript/paper_skeleton.md` from the workspace root:

```bash
python manuscript/build_submission_pdf.py
```

This overwrites `manuscript/paper_manuscript.tex` with updated content and rebuilds `manuscript/paper_manuscript.pdf`.

If you only want to regenerate LaTeX without compiling the PDF:

```bash
python manuscript/generate_latex_manuscript.py
```

---

## Research Expansion Checklist

- [ ] Reproduce MART and ACER-PA on at least a subset of source-paper subjects, or add an explicit access-limitation note with fallback protocol
- [ ] Implement heuristic baselines in the main experiment table (shortest-first, recent-failure-first, fast-plus-recent-failure)
- [ ] Run one federated pretraining variant and report retention versus centralized pretraining
- [ ] Run one stronger semantic/LLM representation variant and compare against FALCON on shared subjects
- [ ] Produce flaky-label impact evidence on a feasible subset via re-execution and/or CI-log mining
- [x] Finalize the threat-to-validity mapping in the manuscript discussion and conclusion

---

## Submission Preparation Checklist

- [x] Rebuild and review the compiled PDF for formatting and page breaks
- [ ] Replace the three-author placeholder block with actual names, affiliations, locations, and emails
- [x] Formalize references directly in the manuscript source
- [ ] Replace any remaining unresolved metadata or dataset placeholders once the missing source inputs exist
- [ ] Verify all table and figure captions are present
- [ ] Optionally tighten long URLs and remaining box warnings if a stricter final typography pass is needed
- [ ] Proof-read for typos and consistency

---

## Known Limitations

- LaTeX must be installed locally or compiled via Overleaf
- Requires `pdflatex` or `xelatex` engine
- Default uses Times Roman font via `times` package (portable)
- No external figures included (table-only document currently)
- Author names and affiliations are still placeholders
- References are maintained inline in `manuscript/paper_skeleton.md` rather than via a separate `.bib` file
- The build is stable, but the LaTeX log still reports non-fatal underfull/overfull box warnings on dense prose and long URLs

---

## File Organization

```
paper/
├── manuscript/
│   ├── paper_manuscript.tex          ← Main submission file
│   ├── generate_latex_manuscript.py  ← Regenerator
│   ├── paper_skeleton.md             ← Source markdown
│   └── MANUSCRIPT_README.md          ← This file
└── direction_c/
   └── DIRECTION_C_COMPLETE_PROTOCOL.py  ← Active Direction C protocol context
```

---

**For questions or edits:** Modify `manuscript/paper_skeleton.md`, then rebuild with `python manuscript/build_submission_pdf.py`.
