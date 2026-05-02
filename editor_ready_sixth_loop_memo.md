# Editor-Ready Sixth-Loop Memo on *Revisiting Machine Learning based Test Case Prioritization for Continuous Integration*

This memo assumes the fifth-loop window as context and pushes it one level further: from demolition map to **paper-ready synthesis**.[cite:1] It is designed for discussion with an editor, supervisor, or coauthor who needs to see a clear thesis, contribution set, and experimental plan rather than another round of critique.[cite:1] The goal is to lock in *what this new paper is actually about* and *what it must empirically clear* to be worth publishing.

---

## 1. Core thesis (what this new paper claims)

A compact, editor-facing thesis:

> **This paper reconciles unified ML-based TCP benchmarks with modern CI realism** by showing how label noise (flaky tests), data-governance constraints (federated pretraining), semantic representation shift (LLM-era embeddings), and external validity (desktop/server vs. mobile/Android CI) jointly reshape which test case prioritization methods are genuinely deployable.

In plainer terms:

- The 2023 source paper solved *comparability* for 11 ML-based TCP methods across 11 projects but under clean-label, open-data, pre-LLM assumptions.[cite:2]
- The surrounding ecosystem (FAST, FALCON, DeepOrder, LRTS, IDoFT, TCP-CI) now exposes mismatches between that benchmark and actual CI realities.[cite:3][cite:4][cite:5][cite:6]
- This new paper does not "revisit again"; it **tests which of the original conclusions survive when those realism constraints are enforced and where the method rankings break or invert**.

This is the sentence your editor cares about.

---

## 2. Concrete contribution set (what readers can quote)

Proposed contributions, written in publication-ready language and grounded in the artifact ecosystem:

1. **Label-realism analysis for ML-based TCP.**
   - Quantifies how flaky and confounding failures (identified via re-execution, CI-log mining, or DeFlaker/NonDex-style tools) change effectiveness metrics for history-based TCP, using a subset of the 11 source-paper subjects plus LRTS-style long-running suites.[cite:4][cite:6]
   - Shows that APFD/rAPFD values computed on raw CI histories can substantially overstate true regression-detection performance when flaky labels dominate.

2. **Federated pretraining versus centralized pretraining.**
   - Reuses the source paper's MART-style cross-project pretraining pipeline (via Zenodo 7036507) but constrains data flow to simulate organization-level data silos.[cite:2]
   - Demonstrates how much of the original 80% vs. 50% optimal-sequence gain survives when only model parameters or gradients are shared, not raw test histories.[cite:2]

3. **Representation-shift robustness study.**
   - Benchmarks classic feature-based ML TCP, non-ML similarity (FAST), semantic TCP (FALCON), and an LLM-augmented variant on the same subjects.[cite:3][cite:5]
   - Shows that upgrading representation from handcrafted features to semantic embeddings can reorder the winner landscape (e.g., MART vs. ACER-PA vs. FALCON vs. LLM variant), especially under noisy labels.

4. **Baseline-complete evaluation grid across five tiers.**
   - Places heuristics, similarity-based, semantic, deep-learning, and ML/RL methods on the same board using the FAST, FALCON, DeepOrder, LRTS, and source-paper artifacts.[cite:3][cite:4][cite:5]
   - Provides the first evaluation where a new method must beat or match **FALCON plus simple heuristics** under long-running, flaky-prone suites, not just other ML methods.

Even if one of these contributions weakens during implementation, the others are independently valuable.

---

## 3. Datasets and artifacts (the experimental universe)

Your work is anchored in a specific artifact graph, not in abstract talk. The key nodes:

- **Source paper dataset (11 GitHub projects).**
  - Includes more-failure subjects (bcel, jedis, jsprit, nfe, spring-data-redis) and less-failure subjects (csv, dbcp, text, java-faker, jsoup, maxwell).[cite:1]
  - Available via Zenodo 7036507 replication package, albeit with some access and tooling constraints (Understand, RankLib). Central for reproducing MART/ACER-PA results and the failure-regime split.[cite:2]

- **FAST benchmark subjects (SIR + Defects4J).**
  - Ten projects: flex_v3, grep_v3, gzip_v1, make_v1, sed_v6 (C); chart_v0, closure_v0, lang_v0, math_v0, time_v0 (Java).[cite:1]
  - Non-ML similarity baselines (FAST-pw, FAST-log) already profiled: strong on SIR, weaker and higher-variance on Defects4J.

- **FALCON semantic TCP (Defects4J).**
  - Covers Defects4J projects Chart, Closure, Lang, Math, Mockito, Time.[cite:5]
  - Provides FAST and semantic baselines plus comprehensive CSV results; 16.4% median APFD improvement (0.731 vs. 0.628) over similarity-based methods.[cite:5]

- **LRTS long-running suites.**
  - 21k+ CI builds, 57k+ suite runs, ≈6.5 hours per run, 10 large Java projects.[cite:4]
  - Already shows cases where very simple heuristics beat ML TCP under realistic, flaky, long-running conditions.

- **IDoFT flaky-tests dataset.**
  - Rich classification of flaky tests by root cause, but **almost no overlap** with the 11 source-paper subjects (only small coverage for jedis and spring-data-redis).[cite:6]
  - Forces Direction A to adopt alternative flaky-label acquisition strategies on those 11 projects.

- **DeepOrder artifact.**
  - Deep-learning TCP for CI that consumes historical execution records; shows the learning-based representation space is already populated.[cite:3]

This list is what makes your design grounded rather than speculative.

---

## 4. Baseline and method grid (what you must beat or match)

Editors and reviewers have a simple question: *"Against what?"* This is the grid you should commit to:

1. **Heuristic baselines**
   - Shortest-tests-first.
   - Most-recent-failure-first.
   - LRTS-style "fast + recently failing" policy.[cite:4]

2. **Non-ML similarity baselines**
   - FAST-pw and FAST-log on SIR and Defects4J.[cite:3]

3. **Semantic / embedding baselines**
   - FALCON (UniXcoder + submodular optimization) on Defects4J.[cite:5]

4. **Deep learning TCP**
   - DeepOrder on at least one shared dataset.

5. **Original ML/RL methods**
   - MART, ACER-PA, and at least one reinforcement-learning variant from the replication package.[cite:2]

6. **Your new method(s)**
   - Federated MART (and/or other SL models) with constrained data sharing.
   - Flaky-label-aware variant(s) and/or LLM-augmented variant(s).

The **career-risk warning** from the fifth-loop window stands: winning only battle 5 vs. 6 (ML vs. ML) while losing to FALCON or heuristics is not a contribution that the 2026 TCP community cares about.[cite:1]

---

## 5. Direction prioritization (what to actually implement first)

Given current lab status and external constraints, the directions rank as follows:

1. **Direction B – Federated pretraining (highest readiness).**
   - Replication package exists; MART-style pretraining is already established.[cite:2]
   - You can simulate federated setups by partitioning subjects and restricting what crosses partitions (gradients/parameters vs. raw histories).
   - Low additional artifact risk, high conceptual leverage.

2. **Direction C – Representation shift (LLM/semantic).**
   - FALCON and DeepOrder provide immediate semantic and deep baselines.[cite:3][cite:5]
   - Implementing a new LLM-augmented model is work, but the pathway is clear (e.g., replacing or enriching FALCON's embeddings).

3. **Direction A – Flaky-test-aware TCP (blocked by label source).**
   - IDoFT coverage gap for the 11 subjects is confirmed; you must choose between DeFlaker/NonDex, CI-log mining, or heavy re-execution.[cite:6]
   - High conceptual payoff but high engineering and compute cost.

4. **Direction D – Android/mobile CI (data missing).**
   - Requires identifying or mining an Android CI dataset with sufficiently rich history and flaky behavior.
   - Likely multi-month, separate project unless a suitable dataset surfaces.

A realistic near-term plan for a single paper is to fully deliver B and C, and to use A as the main *motivation plus partial evidence* section (e.g., small-scale flaky-label study), while clearly flagging D as future work.

---

## 6. Threats to validity (already weaponized, now structured)

Your threats-to-validity section should explicitly mirror the earlier critique loops but with a constructive tone:

- **Label validity.**
  - Threat: conflating true regressions with flaky or infrastructure-induced failures.
  - Mitigation: LRTS-style re-execution for a subset; Chrome-style evidence; explicit separation of flaky vs. non-flaky labels where available.[cite:4]

- **Dataset and domain coverage.**
  - Threat: 11 GitHub projects and Defects4J do not cover mobile, microservices, or large polyglot systems.
  - Mitigation: making all claims conditional on dataset families; using LRTS as a contrasting large-scale long-running suite; being explicit that Android/mobile CI is out of scope.

- **Representation bias.**
  - Threat: older handcrafted features may bias in favor of certain models.
  - Mitigation: adding semantic and LLM-based representations; reporting how rankings change when representation changes.

- **Hyperparameter and implementation sensitivity.**
  - Threat: MART vs. ACER-PA split might be an artifact of one configuration.
  - Mitigation: limited sensitivity analysis on key hyperparameters and seeds; explicit reporting of where rankings are unstable.

This is where you turn earlier brutalities into a controlled, self-aware narrative.

---

## 7. How to talk about the source paper (editor-safe wording)

Recommended language for positioning the original work:

- "The original study provided the first unified benchmark of 11 ML-based TCP techniques across 11 CI projects, demonstrating that there is no universal winner and that method choice depends on failure regime and runtime budget."[cite:2]
- "However, its conclusions were drawn under assumptions that predate modern CI realism: labels were treated as clean, cross-project data sharing as unproblematic, and feature representations as fixed."[cite:1]
- "This paper reconciles those benchmark conclusions with contemporary evidence on flaky tests, federated data constraints, and semantic representations by re-evaluating the original methods alongside non-ML, heuristic, and semantic baselines on both classic and long-running CI datasets."[cite:3][cite:4][cite:5]

This phrasing is respectful, accurate, and clearly opens room for your contribution.

---

## 8. Editor checklist: when is this paper "done"?

You can give your editor a short checklist derived from this memo:

1. **Replication:** Key MART/ACER-PA results reproduced on at least a subset of the 11 subjects (or documented access limitations) with rAPFD metrics reported.
2. **Baselines:** FAST, heuristics, FALCON, DeepOrder, and at least MART/ACER-PA included in all main experiments.
3. **Federated pretraining:** At least one federated variant evaluated that retains a meaningful fraction of centralized pretraining gains.
4. **Representation shift:** At least one semantic or LLM-based variant evaluated that either beats FALCON on shared benchmarks or shows clear robustness under noisy labels.
5. **Flaky evidence:** Some empirical demonstration (e.g., via LRTS or small-scale re-execution) that label noise materially affects TCP metrics.
6. **Threats-to-validity section:** Explicitly covers label validity, dataset scope, representation bias, and hyperparameter sensitivity.

If you can check off items 1–4 and offer credible progress on 5–6, the paper is more than "yet another ML TCP benchmark"; it is a realism-correction paper for an entire line of work.

---

## 9. One-line internal summary

> The project is no longer about finding the next best TCP algorithm; it is about **testing which of the original unified-benchmark conclusions survive when confronted with flaky labels, federated data, semantic representations, and harder CI datasets — and reporting those survivals and failures with baseline-complete honesty.**

