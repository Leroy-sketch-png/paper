# Copilot Instructions

## Workspace Identity

This repository is a research workspace for a manuscript on ML-based test case prioritization in continuous integration. It combines:

- manuscript drafting and LaTeX generation
- experiment orchestration and result aggregation
- research planning memos for Directions A-D
- artifact verification and baseline computation

Treat the workspace as an evidence-preserving research artifact, not as a generic software project.

## Primary Objectives

- Preserve numerical and textual consistency across manuscript, memos, summaries, and scripts.
- Prefer reproducible, script-backed updates over hand-edited claims.
- Keep experimental claims tied to verified artifacts already present in the workspace.
- Avoid broad refactors that obscure provenance or invalidate prior notes.

## Source Of Truth Order

When facts conflict, use this order unless the user says otherwise:

1. Executed data files and direct script outputs.
2. The current filesystem state in this workspace.
3. Aggregation scripts such as `heuristic_baselines.py`, `print_results.py`, `bootstrap_ci.py`, and `comprehensive_results.py`.
4. Execution summaries such as `EXECUTION_SUMMARY.md` and `WORK_PRODUCT_INDEX.md`.
5. Planning documents and expected-findings memos.
6. Narrative manuscript text.

Do not introduce new numbers into narrative files unless they can be traced to a script, artifact, or an already verified summary in the workspace.

Historical summaries may describe a larger research directory than the current checked-out workspace. If a document says an artifact or subtree exists, verify the file is actually present before treating it as available.

## Evidence Labels

Use the strongest accurate label for every claim:

- `verified` for values backed by existing artifacts, checked files, or executed outputs present in the workspace
- `artifact-verified` for values imported from an external artifact already downloaded or extracted into the workspace
- `simulated` for protocol demonstrations such as `direction_a/flaky_detection_protocol.py`
- `framework` or `protocol` for design documents that specify how work should run but do not prove that the underlying experiment ran
- `blocked` or `staged` where a dependency or dataset is still unavailable

Do not collapse `framework complete`, `ready to execute`, `simulated`, and `executed on real data` into the same status language.

Planning documents may be more ambitious than the currently checked-in execution scripts. When Direction C documents and `direction_c/direction_c_phase3_ranker.py` or `direction_c/direction_c_phase4_correlation.py` disagree, describe both accurately instead of forcing a false single story.

## Editing Rules

- Prefer minimal, local edits.
- Preserve the current naming of the four research directions: A flaky labels, B federated pretraining, C LLM representations, D mobile or Android CI.
- Keep the six-tier baseline framing intact unless the user explicitly requests a conceptual rewrite.
- Do not silently remove caveats about unavailable artifacts, Understand-license constraints, sparse IDoFT overlap, or staged Direction D scope.
- Keep historical status statements internally consistent: if a file says `ready`, `blocked`, `executed`, or `simulated`, do not upgrade or downgrade that state without evidence.

## Path And Environment Safety

Some historical or maintenance files still contain an older machine-specific research path.

- Do not add new hardcoded user-specific paths.
- When changing scripts, prefer paths derived from `Path(__file__).parent`, the current workspace root, or clearly declared config variables.
- If a path-sensitive script is edited, preserve Windows compatibility.
- Assume this repository may be moved between machines; portability is better than convenience.
- Before referencing FAST outputs, Defects4J trees, or downloaded artifacts, check whether they are inside the current workspace or only mentioned in historical notes.

## Generated Artifacts

Generated experiment outputs are intentionally ignored by Git. Expect these directories to be absent until the corresponding scripts are run:

- `embeddings/`
- `feature_matrices/`
- `phase3_results/`
- `phase4_results/`
- `FAST/output/`

Do not describe these outputs as present unless you have verified them in the current workspace.

Prefer regenerating derived artifacts over hand-editing them. This especially applies to `manuscript/paper_manuscript.tex`, `artifacts/heuristic_baselines.csv`, and any future `phase3_results/` or `phase4_results/` JSON outputs.

## Manuscript Workflow

- `manuscript/paper_skeleton.md` is the main narrative source.
- `manuscript/generate_latex_manuscript.py` regenerates `manuscript/paper_manuscript.tex` from `manuscript/paper_skeleton.md`.
- `manuscript/MANUSCRIPT_README.md` describes the intended manuscript flow and compilation steps.

If you change the manuscript structure or claims:

1. Update the markdown source first.
2. Regenerate LaTeX when needed.
3. Keep manuscript-facing summaries aligned with the changed claim.

If a summary claims `zero placeholders`, verify that against `manuscript/paper_skeleton.md` before repeating it. The repository history shows manuscript-status summaries can lag behind the actual text.

## Citation And Baseline Hygiene

- Use `references/2311.13413v1.notes.md` as a working interpretation aid, not as the final authority for exact citations.
- For source-paper numbers that matter to the manuscript, prefer `references/2311.13413v1.pdf` or the cleaned extraction in `references/2311.13413v1.md`, with extra caution around figure-heavy or table-heavy claims.
- Preserve the difference between source-paper claims, artifact-verified numbers, and locally reproduced numbers.
- For FALCON specifically, keep paper-level and project-level aggregation distinct.

## Document Roles

Use these files intentionally:

- `manuscript/MANUSCRIPT_README.md` for manuscript status and regeneration workflow
- `manuscript/paper_skeleton.md` for the primary paper narrative
- `manuscript/paper_manuscript.tex` as generated output, not the preferred hand-edit target
- `EXECUTION_SUMMARY.md` for verified baseline and blocker framing
- `window.md` for upward-facing research synthesis and argument framing
- `WORK_PRODUCT_INDEX.md` plus archived status/planning documents under `archive/status/` and `archive/plans/` for historical context
- `references/2311.13413v1.notes.md` for source-paper interpretation shortcuts

Prefer updating the source document that owns the fact instead of only changing downstream summaries.

Session summaries and roadmap files often capture an optimistic point-in-time execution snapshot. Treat ETAs, readiness percentages, and `ready within minutes` language as historical unless the current filesystem and dependencies confirm them.

## Direction Status Guardrails

Respect the current asymmetry across the four directions:

- Direction A is a flaky-label protocol and simulation track unless real re-execution outputs or mined CI histories are present.
- Direction B is a federated-design track unless source-paper code and license-dependent tooling become available.
- Direction C is the only direction with manuscript-integrated executed findings in the current repo, but those findings are a BPE or lexical proxy path, not full UniXcoder contextual replication.
- Direction D is a staged extension and should stay explicitly conditional on dataset discovery.

Do not rewrite the paper or summaries as if all four directions have been executed equivalently.

## Direction C Specific Rules

- Distinguish between the planning stack (`direction_c/direction_c_strategy.py`, `direction_c/direction_c_phase1_plan.py`, `direction_c/DIRECTION_C_COMPLETE_PROTOCOL.py`, `direction_c/DIRECTION_C_EXPECTED_FINDINGS.md`) and the currently implemented surrogate execution stack (`direction_c/direction_c_compute_embeddings.py`, `direction_c/direction_c_feature_matrix.py`, `direction_c/direction_c_phase3_ranker.py`, `direction_c/direction_c_phase4_correlation.py`).
- If discussing current executed Direction C results, say they are based on a vocabulary-anchored or fallback embedding path on SIR subjects unless you have verified new full-contextual outputs.
- Do not imply MART or ACER-PA retraining happened unless output artifacts prove it.
- Keep the manuscript's negative BPE-proxy result separate from the open question about full UniXcoder or FALCON-level representations.

## Tables And Placeholders

- `manuscript/paper_skeleton.md` still contains placeholder sections for Direction A, B, and D tables or figures.
- Direction C tables cite `phase3_results/` and `phase4_results/` JSON outputs; verify those files exist before claiming the tables were script-generated in the current checkout.
- If you add or remove a placeholder, synchronize the surrounding summaries so status language stays honest.

## Research Integrity Constraints

- No hallucinated results, citations, datasets, or execution status.
- Separate executed findings from planned work and expected findings.
- Preserve explicit uncertainty when a result is partial, blocked, staged, or hypothetical.
- If a script uses a fallback approximation, label it clearly in code or documentation rather than implying it is a full replication.
- Treat simulation frameworks for Directions A and B as method specifications unless there is separate evidence that they were run on real subject data.

## Workspace Boundary Awareness

This workspace mixes three categories of material:

- primary manuscript and summary documents
- executable helper scripts and protocol code
- historical memos that reference tools, datasets, and folders outside the current checkout

Archived memo loops, stale session snapshots, and one-off utilities may be moved under `archive/` or `scripts/maintenance/` to reduce root clutter without deleting provenance.

Active analysis helpers may be grouped under `scripts/analysis/` as long as established root entry points are preserved as thin wrappers.

Active direction-specific framework material may live under `direction_a/`, `direction_b/`, and `direction_c/` when that keeps the workspace root focused on manuscript files and primary entry points.

Always distinguish between `documented somewhere`, `implemented in code`, and `present and runnable here`.

## Preferred Working Style

- Read nearby summaries before rewriting a research-facing document.
- Check for existing memos before creating new planning text.
- Favor deterministic scripts and fixed-seed behavior when adding analyses.
- When summarizing Direction C, respect the distinction between paper-level and artifact-level FALCON aggregation.
- When a historical summary conflicts with the current repo state, prefer the current repo state and explicitly note the mismatch.

## High-Risk Files

Treat edits in these files as high impact and verify carefully afterward:

- `manuscript/paper_skeleton.md`
- `manuscript/paper_manuscript.tex`
- `EXECUTION_SUMMARY.md`
- `window.md`
- `heuristic_baselines.py`
- `print_results.py`
- `direction_c/direction_c_compute_embeddings.py`
- `direction_c/direction_c_phase3_ranker.py`
- `direction_c/direction_c_phase4_correlation.py`

## Default Agent Behavior For This Repo

- Be conservative with claims.
- Be explicit about provenance.
- Prefer reproducibility over polish.
- Prefer consistency across documents over isolated local improvements.

## Review Checklist

Before finalizing any substantial repo change, verify these points when relevant:

1. Numbers match a checked artifact, script, or already-verified summary.
2. Status language still distinguishes executed, simulated, ready, blocked, and staged work.
3. Hardcoded paths were not added or silently preserved in new code.
4. Manuscript-source changes were mirrored into the right summaries, not only one downstream file.
5. Generated-output references still match files that actually exist in the workspace.
