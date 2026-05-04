# Research Workspace Layout

This repository is an evidence-preserving workspace for the ML-based test case prioritization manuscript and its supporting analyses.

## Top-Level Structure

- `manuscript/` contains the paper source, generated LaTeX, PDF, and manuscript workflow notes.
- `artifacts/` contains verified downloaded artifacts and regenerated result summaries.
- `references/` contains the source-paper bundle and reading aids.
- `direction_a/`, `direction_b/`, and `direction_c/` contain active direction-specific framework and execution material.
- `scripts/analysis/` contains active analysis implementations.
- `archive/` contains historical plans, status snapshots, and older memos kept for provenance.
- `FAST/` contains the benchmark implementation subtree used for reproduced baseline runs.

## Root Entry Points

The root keeps a small set of intentional entry points for common workflows:

- `bootstrap_ci.py`
- `heuristic_baselines.py`
- `print_results.py`
- `comprehensive_results.py`
- `EXECUTION_SUMMARY.md`
- `window.md`
- `WORK_PRODUCT_INDEX.md`

## Common Commands

Run these from the workspace root:

```bash
python manuscript/generate_latex_manuscript.py
python print_results.py
python comprehensive_results.py
python direction_a/flaky_detection_protocol.py
python direction_b/federated_pretraining_framework.py
```

## Working Rules

- Update `manuscript/paper_skeleton.md` first for manuscript changes, then regenerate LaTeX.
- Prefer scripts and checked artifacts over narrative files when facts conflict.
- Treat `archive/` as historical context, not the source of current workspace state.