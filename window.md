# Research Window 001 — Fourth Loop

## Standalone Brief

This document is a standalone upward-facing research briefing, now through four adversarial loops.
Loop 1 introduced vulnerabilities per claim. Loop 2 escalated: flaky-test label contamination as a first-class attack on the paper's core learning assumptions, transfer hardness distinguished from transfer promise, LLM-augmented representations reframed as a winner-landscape shift. Loop 3 grounded the research: source paper replication package located, FAST non-ML baseline ported and verified, FALCON (ICST 2025) and LRTS (ISSTA 2024) registered as adjacent artifacts. Loop 4 integrates the full artifact ecosystem: DeepOrder registered, Extension Tracks given empirical thresholds, experimental grid codified, and the career-risk framing introduced — winning only ML-vs-ML is no longer sufficient when FALCON and heuristics are in the comparison pool.
Designed to be forwarded without local workspace context.

## Source

- Paper title: Revisiting Machine Learning based Test Case Prioritization for Continuous Integration
- Source identifier: 2311.13413v1
- Research topic: machine-learning-based test case prioritization for continuous integration
- **Replication package: Zenodo record 7036507** (`https://zenodo.org/records/7036507`). Contains full code (RL algorithms: ACER-PA, PPO2-PO, PPO1-LI, COLEMAN; SL algorithms: MART, RankNet, RankBoost, CA, L-MART, DeepOrder), data (11 projects, original + SMOTE-preprocessed), and results (RQ1–RQ3 + threats to validity). Adoption note: uses Understand tool for dependency analysis — requires separate license.
- **Live artifact: FAST repo (icse18-FAST/FAST) — cloned locally at `FAST/`, ported to Python 3.10.** Implements 12 TCP algorithms: FAST-pw, FAST-one, FAST-log, FAST-sqrt, FAST-all (similarity-based, black-box and white-box), plus GT, GA, GA-S, ART-F, ART-D (white-box), STR, I-TSD (black-box). ICSE 2018. These are non-ML, similarity-based baselines — directly relevant as the pre-ML TCP landscape that the source paper's 11 ML techniques are competing against. **Verified output: `python py/prioritize.py flex_v3 bbox FAST-pw 3` → APFD ~0.878–0.948.**
- **Adjacent artifact: FALCON** (ICST 2025, Zenodo 18897073). Submodular optimization + UniXcoder embeddings for TCP. 16.4% higher median APFD over similarity-based methods (0.731 vs 0.628) on Defects4J. Directly relevant to Direction C (LLM-augmented representations). FALCON establishes that semantic code embeddings + diversity optimization outperform FAST-style similarity in the same benchmark space.
- **Adjacent artifact: LRTS** (ISSTA 2024, Zenodo 12662090, GitHub: lrtsuser/LRTS). Long-Running Test Suites dataset: **21,255 CI builds, 57,437 test-suite runs, average 6.5 hours per run**, 10 large-scale Java projects, explicitly analyzing flaky tests and long-running suites. Key finding: simple policies (prioritize faster tests that recently failed) can outperform sophisticated ML in some contexts — a direct challenge to any narrative that ML complexity yields reliable gains. Directly relevant to Directions A (flaky-test-aware TCP) and D (Android/mobile CI replication as contrast case).
- **Adjacent artifact: DeepOrder** (ICSME 2021, GitHub: AizazSharif/DeepOrder-ICSME21). Deep learning TCP for CI: regression-style neural model consuming historical test execution records. Already outperforms some prior approaches on efficiency and detection. Jointly with FALCON, establishes that the representation-learning space for TCP is **not underexplored** — the interesting question is no longer whether deep/semantic models beat classic heuristics but how they behave under flaky labels, federated constraints, and long-running suites.

## Lab Status (as of May 2, 2026)

| Item | Status | Location / Notes |
|---|---|---|
| Source paper | In hand | `2311.13413v1.pdf`, converted to `.md` |
| Source paper replication package | Located | Zenodo 7036507 — not yet downloaded |
| FAST (ICSE 2018) non-ML baseline | **Running** | `FAST/` — Python 3.10 port complete; FAST-pw APFD ~0.878–0.948 on flex\_v3 |
| FALCON (ICST 2025) artifact | Located | Zenodo 18897073 — not yet downloaded |
| LRTS (ISSTA 2024) dataset | Located | Zenodo 12662090 / GitHub lrtsuser/LRTS — not yet downloaded |
| DeepOrder (ICSME 2021) artifact | Located | GitHub AizazSharif/DeepOrder-ICSME21 — not yet cloned |
| TCP-CI dataset | Located (reference) | Cited in federated pretraining track; exact Zenodo/GitHub not yet confirmed |
| IDoFT flaky-test dataset | Not yet found | Needed for Direction A (flaky-test-aware TCP) |
| Android open-source CI data | Not yet found | Needed for Direction D |
| Full FAST baseline table | Not yet run | All 10 subjects × bbox + wbox — ~5 min automated |
| Paper skeleton / draft | Not started | All four directions confirmed active |

**Highest-readiness direction:** Direction B (federated pretraining) — source paper's strongest clue, replication package in hand, concept grounded. **Highest-urgency gap:** Direction A flaky-test dataset (IDoFT) — the label-realism attack needs empirical grounding before it can anchor a motivation section.

## Scope In Plain Terms

- TCP = test case prioritization.
- CI = continuous integration.
- SL = supervised learning.
- RL = reinforcement learning.
- rAPFD = rectified Average Percentage of Faults Detected — the paper's proposed replacement for prior evaluation metrics.
- APFD = Average Percentage of Faults Detected — original metric; known fairness and discernment problems in CI.
- MART = SL-based technique. Best on less-failure subjects. Lowest overhead. Safest practical default.
- ACER-PA = RL-based technique. Best on more-failure subjects. High effectiveness, high runtime cost.
- PPO1-LI = RL-based technique. Can become inapplicable when prediction time exceeds total test execution time.
- FAST = similarity-based non-ML TCP framework (ICSE 2018). 12 algorithms. Strong APFD at minimal cost. The pre-ML baseline tier.
- FALCON = submodular + UniXcoder embedding TCP (ICST 2025). Currently the highest-bar semantic baseline: 0.731 median APFD on Defects4J.
- DeepOrder = deep learning TCP for CI (ICSME 2021). Historical test execution records → regression-style neural ranking.
- LRTS = Long-Running Test Suites dataset (ISSTA 2024). 21,255 CI builds, 57,437 runs, avg 6.5 h/run. Explicit flaky-test analysis.
- The paper compares 11 ML-based TCP methods under one controlled setup on 11 open-source GitHub projects.
- It evaluates three dimensions: effectiveness, efficiency, and practical applicability.

## Executive Window

- This paper's core contribution is not a single best method — it demonstrates the **absence of a universal winner** under one controlled experimental setup.
- The strongest method depends on the project's failure-rate regime, training data availability, and runtime budget.
- ACER-PA is strongest on more-failure subjects. MART is strongest on less-failure subjects and is the safest practical default overall.
- Cross-subject pretraining is one of the strongest improvement levers: pretrained MART reaches optimal sequences on 80% of subjects vs. 50% for original MART.
- Metric choice matters: APFD, NAPFD, and NRPA have known fairness and discernment problems in CI; rAPFD is proposed as a replacement but is itself still contestable.
- Runtime overhead belongs in the main evaluation frame. PPO1-LI demonstrates that high effectiveness can still mean practical inapplicability.
- **Critical posture**: The paper solved the comparability problem better than prior work. It did not solve the realism problem. It standardized the battlefield — but the battlefield was too clean, too open-source-centric, and too historically stable to support strong deployment-level prescriptions.
- **Flaky escalation**: A study on Chrome's CI history reports 99.58% of test failures were flaky. If that kind of label contamination appears broadly, history-based TCP methods may be learning from noise, not regression signal. This is not a future-work footnote — it attacks the paper's learning and evaluation logic at the root.
- **LLM shift**: Richer semantic representations may change which methods are robust, which transfer, and which justify overhead. Old method rankings may be feature-era artifacts, not durable truths.
- **Non-ML baseline risk**: FAST already achieves high APFD cheaply. FALCON beats FAST by 16.4% using semantic embeddings. LRTS shows simple heuristics outperform ML in some large-scale real contexts. A new paper that wins only against other ML methods while losing to FALCON or well-tuned heuristics has not contributed to the right battle — this is the primary career risk for any TCP paper in 2026.

## What The Paper Genuinely Establishes

Three real contributions:

1. **No universal winner.** The paper reframes method selection as conditional on failure behavior, training data, and overhead budget. This pushes back against leaderboard-style reading in prior TCP literature.
2. **Methodological unification.** 11 techniques evaluated under one pipeline removes incompatible cross-paper claims from different datasets, metrics, and feature setups.
3. **Overhead as first-class variable.** PPO1-LI's prediction cost can exceed total test execution time in some subjects — a point more practically valuable than most effectiveness-only comparisons because CI is time-budgeted.

## Decision-Relevant Claims

### Claim 1. Best method depends on failure-rate regime

- More-failure subjects: ACER-PA performs best.
- Less-failure subjects: MART performs best.
- The paper attributes this split mainly to data imbalance.

**Why this matters:** Any claim of a single globally best ML-TCP method is weak unless conditioned on subject failure behavior.

**Vulnerability:** The failure-rate regime itself may be unstable or endogenous to dataset construction. If failure prevalence changes with project maturity, bug-fix bursts, or release cadence, then the ACER-PA / MART split may reflect transient benchmark conditions rather than a durable taxonomy. More aggressively: benchmark composition, implementation choices, default hyperparameters, subject maturity, and feature representation may all independently contribute to the apparent split. Unless those factors are disentangled, the claim should be treated as a robust observed pattern in this benchmark — not a settled explanation of method superiority. A reviewer will ask: is failure-rate an explanatory variable, a descriptive artifact, or both?

### Claim 2. More training data matters more than code evolution

- Performance changes across CI cycles are attributed mainly to training data volume, not code evolution or test churn.
- RL methods may improve later because they adapt online. SL methods may stagnate.

**Why this matters:** Transfer learning and pretraining are central practical levers, not side experiments.

**Vulnerability:** The experiment does not fully isolate training-data volume from feature drift, distribution shift, test-suite restructuring, and evolving fault patterns. The harsher version: training-data growth may be entangled with temporal stabilization, project maturity, changing failure prevalence, and feature drift simultaneously. None of these are trivial nuisances in CI. The claim reads causally; the evidence is closer to controlled comparative observation under a shared setup.

### Claim 3. Pretraining is a major improvement path

- Pretrained MART reaches optimal sequence on 80% of subjects.
- Original MART reaches optimal sequence on 50% of subjects.

**Why this matters:** Cross-subject data is operationally valuable and should be treated as a serious asset for future ML-TCP systems.

**Vulnerability:** The paper established **transfer promise** without measuring **transfer hardness** — it did not map when transfer breaks, degrades, or becomes misleading. Transfer gains can come from genuine signal reuse, benchmark affinity, hidden subject similarity, or feature leakage through broadly shared development patterns. Whether pretraining helps when source and target projects are intentionally dissimilar is untested. Cross-project data also raises governance constraints: in industrial settings, test execution histories may be sensitive, siloed, or legally constrained. A federated baseline would not just modernize the design — it would test whether the paper's strongest clue survives realistic organizational constraints.

### Claim 4. High effectiveness does not guarantee practical usability

- RL methods require much longer training time than SL methods.
- PPO1-LI can become inapplicable: prediction cost can exceed total test execution time.
- MART combines strong effectiveness with low overhead.

**Why this matters:** Runtime cost must be a first-class selection criterion.

**Vulnerability:** Practicality is assessed against average commit intervals and test execution times in these 11 subjects, not against industrial diversity. A method that clears this bar may still fail in high-frequency repos, mobile pipelines with emulator overhead, or CI with stricter latency SLOs. For Android/mobile CI specifically: emulator instability, asynchronous timing, hardware heterogeneity, and UI synchronization problems increase the chance that historical outcomes are fundamentally dirtier than the benchmark assumes. MART's relative advantage may also partly reflect the benchmark and implementation stack favoring its cost structure — if batching, hardware acceleration, or async scheduling change, the RL vs. SL practicality gap may narrow.

## Metric Critique

The paper proposes rAPFD to replace APFD, NAPFD, and NRPA, arguing prior metrics have fairness and discernment problems in CI.

**The key critical question:** Does rAPFD improve scientific comparability, operational fidelity, or both?

- If mainly comparability across CI cycles with varying failure counts: the paper should be framed more modestly.
- If a better proxy for engineering value in deployment: needs a direct tie to downstream developer outcomes (debugging delay, failure triage speed).
- Without that tie, the paper risks replacing one benchmark convenience metric with a refined benchmark convenience metric.

**Second-loop deepening:** rAPFD is valuable as a comparability repair inside CI-style evaluation when failure counts vary across cycles. But the stronger question is whether rAPFD remains meaningful when failure labels are noisy, failures are dependent, or downstream developer value is the real objective. A metric can be scientifically cleaner while still being operationally incomplete. If a follow-on paper introduces flaky-test-aware evaluation or developer-centered outcomes, rAPFD should be positioned as a useful benchmark repair rather than the final metric answer for CI TCP.

**Remaining edge cases:** CI with many passing cycles, flaky failures, dependent failures, or partially redundant failing tests may still complicate rank-based evaluation in ways rAPFD does not settle.

## Hard Numbers To Carry Upward

- 11 GitHub projects.
- 11 ML-based TCP techniques evaluated.
- 800 commits collected per project.
- Pretrained MART: optimal sequence on 80% of subjects.
- Original MART: optimal sequence on 50% of subjects.
- MART can save more than 95% of time-to-first-failure in most subjects.
- PPO1-LI: prediction overhead can exceed total test execution time in some subjects — practically inapplicable.
- **External signal — Chrome CI study: 99.58% of observed test failures were flaky.** If that rate applies broadly, the paper's learned failure signals may substantially reflect nondeterministic noise rather than true regressions.
- **LRTS dataset scale:** 21,255 CI builds, 57,437 test-suite runs, average 6.5 hours per run. Simple "recent-failure + fast-test" heuristics outperform sophisticated ML in some LRTS contexts — directly challenging the assumption that ML complexity yields reliable gains on realistic datasets.
- **FALCON competitive bar:** 0.731 median APFD vs. 0.628 for similarity-based methods on Defects4J. Any new LLM/embedding method must clear FALCON, not just the source paper's 11 ML methods.

## Canonical Evidence Snips

### Abstract Signal

> To alleviate the cost of regression testing in continuous integration (CI), a large number of machine learning-based (ML-based) test case prioritization techniques have been proposed. However, it is yet unknown how they perform under the same experimental setup, because they are evaluated on different datasets with different metrics.

> We investigate the performance of 11 representative ML-based prioritization techniques for CI on 11 open-source subjects and obtain a series of findings.

> In particular, the pretrained MART achieves state-of-the-art performance, producing the optimal sequence on 80% subjects, while the existing best technique, the original MART, only produces the optimal sequence on 50% subjects.

### Metric Correction Signal

> Through the systematic analysis, we find that the metrics (i.e., APFD, NAPFD, and NRPA) used by the existing work have problems in fair comparison and discernment. Therefore, we propose the rectified APFD (rAPFD), with which we evaluate 11 representative ML-based TCP techniques.

### Finding 1

> On more-failure subjects and less-failure subjects, the performance of ML-based TCP techniques is different. On more-failure subjects, the RL-based technique ACER-PA performs the best, while on less-failure subjects, the SL-based technique MART performs the best. This phenomenon is caused by data imbalance.

> Actionable suggestions: Techniques dealing with data imbalance well may perform better for TCP in CI, therefore, cost-sensitive, ensemble algorithms or other robust techniques are promising in this scenario. Besides, pre-processing approaches alleviating data imbalance like SMOTE can boost the existing TCP techniques.

### Finding 2

> The performance of the TCP techniques changes across CI cycles mainly caused by the changing amount of training data, rather than code evolution and test removal/addition. The RL-based technique may perform well on later CI cycles, because they continuously get trained using the coming data, while SL-based techniques cannot. Therefore, more training data lead to better effectiveness for TCP in CI.

> Actionable suggestions: Cross-subject data can be used to pretrain TCP techniques. With more training data available, TCP techniques get fully trained and perform better.

### Finding 3

> RL-based techniques generally have much longer training time than SL-based techniques. In particular, ACER-PA is among the least efficient techniques although achieves high effectiveness, while SL-based techniques are all relatively efficient.

### Finding 4

> The average training and prediction time of all techniques is shorter than the average commit intervals in all subjects. However, PPO1-LI's prediction time exceeds the total test execution time in some subjects, which makes it inapplicable. Except for PPO1-LI, other techniques are generally applicable to the CI context. A good TCP technique (e.g., MART) can help developers save more than 95% time cost in most subjects.

> Actionable suggestions: Test duration should be estimated to assess the necessity of applying any TCP techniques. The overhead of TCP techniques deserves more attention and may become the bottleneck of application in practice.

### Discussion-Level Use Guidance

> When facing more-failure subjects, we suggest using ACER-PA as the TCP technique. Conversely, when facing less-failure subjects, we suggest using MART.

> If a subject has a high CI cycle frequency and, consequently, a low average commit interval, we suggest using SL-based techniques such as MART. This is because RL-based techniques tend to be more time-consuming for training and predicting.

> If the subject is newly-created and has few commits which cannot support sufficient training, or the developers want to improve the performance of TCP techniques, we suggest collecting test execution data from other high-quality subjects. These data can then be used to train the ML models and improve their effectiveness.

### Conclusion Signal

> To learn how ML-based TCP techniques perform in CI, we present the first comprehensive study on 11 GitHub projects, including 11 state-of-the-art ML-based TCP techniques. In our study, we systematically analyze the effectiveness, efficiency, and applicability of existing TCP techniques and get a series of findings and actionable suggestions.

## External Evidence Snips

These are not from the source paper. They are the external findings that most directly challenge or bound the source paper's claims.

### LRTS: Simple Heuristics vs. ML on Realistic CI

> Simple policies such as prioritizing faster tests that recently failed can outperform more sophisticated techniques in some contexts.
— *Revisiting Test-Case Prioritization on Long-Running Test Suites*, ISSTA 2024 (lrtsuser/LRTS, Zenodo 12662090)

**Why this snip matters:** LRTS's test suites average 6.5 hours per run across 21,255 CI builds. When ML methods lose to heuristics at that scale and duration, no paper can safely skip heuristic baselines.

### FALCON: Semantic + Submodular TCP Bar

> FALCON achieves 16.4% higher median APFD than state-of-the-art similarity-based methods (0.731 vs. 0.628) while requiring only 4.45s median runtime. Among five embedding models, UniXcoder with cosine similarity provides the best effectiveness-efficiency trade-off.
— *FALCON: Efficient Test Case Prioritization via Submodular Optimization*, ICST 2025 (Zenodo 18897073)

**Why this snip matters:** This is the current semantic baseline ceiling. An LLM-augmented method must beat 0.731 median APFD on Defects4J or justify itself by robustness, not raw score.

### Chrome CI: Flaky Failure Prevalence

> 99.58% of test failures observed in Chrome's CI history were flaky.
— External citation (Chrome CI study; referenced in third-loop memo)

**Why this snip matters:** If this rate generalizes even partially, history-based TCP methods are training and evaluating on contaminated labels. Every APFD number in the source paper is conditionally valid at best.

## Operational Implications

- Use MART as the safest practical baseline when failure-rate regime is unknown or when operational overhead matters.
- Use ACER-PA when the subject is clearly more-failure and the runtime budget can tolerate heavier RL cost.
- Treat cross-project pretraining as a serious design axis, not a cosmetic enhancement — but audit source/target similarity before trusting transfer gains.
- Do not trust cross-paper comparisons that rely on NRPA-style evaluation without metric validity checks.
- Measure prediction latency against actual selected-test execution time before calling a method deployable in CI.
- Separate effectiveness, efficiency, and deployability in any analysis — they do not naturally align.
- **FAST baseline is runnable locally** (`python py/prioritize.py <subject> bbox FAST-pw 50`). Subjects available: flex_v3, grep_v3, gzip_v1, make_v1, sed_v6, chart_v0, closure_v0, lang_v0, math_v0, time_v0. Verified: flex_v3 FAST-pw APFD ~0.878–0.948. Use FAST-pw as the non-ML similarity baseline when benchmarking any new TCP contribution.
- **Source paper replication package (Zenodo 7036507) is available** — code, data, and results for all 11 ML-TCP methods. Download before constructing baselines to avoid reimplementing existing infrastructure. Note the Understand tool dependency for feature extraction.
- **FALCON (Zenodo 18897073)** demonstrates that UniXcoder embeddings + submodular optimization already outperform similarity-based TCP by 16.4% median APFD in Defects4J. This sets the minimum bar for any LLM representation argument in Direction C — "better than FAST" is not enough; "better than FALCON" is the live threshold.
- **LRTS (Zenodo 12662090 / GitHub lrtsuser/LRTS)** provides 21,255 CI builds / 57,437 runs of long-running Java suites — highest-quality publicly available dataset for flaky-test interaction, multi-method comparison, and mobile CI contrast work.

## Hidden Assumptions To Surface

These are implicit in the paper's design and should be made explicit in any follow-on work:

- **Failure labels are meaningful signals.** The paper does not systematically separate true failures, flaky failures, infrastructure noise, and environment-dependent breakage. This is not a minor omission — if a significant share of failures are flaky, learning and evaluation logic are both contaminated.
- Historical execution outcomes are informative enough for learning-based prioritization over time.
- The chosen feature representation is expressive enough across all 11 techniques — but feature quality can dominate model quality in SE prediction tasks, and LLM-era representations may change which methods appear competitive.
- Open-source CI histories are an adequate proxy for broader deployment conditions.
- Implementation cost is part of technique identity — but engineering optimization could shift the apparent practicality ranking.

## Flaky-Test Escalation

This is the deepest structural attack on the source paper. It is not a future-work gap — it is a challenge to the paper's core learning and evaluation logic.

**The problem:** The source paper treats failing tests largely as meaningful training and evaluation signals. But CI failure labels can be heavily contaminated by flaky, nondeterministic, or infrastructure-dependent failures. A study of Chrome's historical CI reports 99.58% of test failures were flaky. If similar contamination exists in other large CI ecosystems, a history-based prioritization model may be learning to exploit recurring noise patterns rather than predict regressions.

**Why this is more than a missing variable:**
- Effectiveness numbers computed on contaminated labels may be substantially inflated.
- Transfer gains from pretraining may partly reflect shared noise patterns across similar open-source projects, not genuine reusable regression signal.
- rAPFD, while a better comparability metric than its predecessors, does not resolve the question of whether the failures being ranked are informationally valid.

**Android / mobile CI escalation:** Emulator instability, asynchronous timing, hardware heterogeneity, and UI synchronization problems in mobile CI make historical outcomes dirtier than the benchmark assumes. A paper that introduces flaky-test-aware TCP in Android CI would not just be extending the benchmark — it would be attacking one of its deepest hidden assumptions with the hardest available test environment.

**For your paper:** Move flaky-test analysis out of threats-to-validity into the main motivation section. Frame it as a label-realism problem that qualifies every effectiveness number in the source paper.

## Hard Reviewer Questions

- Why should a failure-rate split from 11 subjects be treated as a general selection rule rather than a benchmark-specific pattern?
- How robust are the reported winners to hyperparameter tuning, feature substitutions, seed variation, and implementation-level optimization?
- Does rAPFD correlate better than prior metrics with actual developer value — reduced debugging delay, faster failure triage?
- Are pretraining gains still present when source projects are intentionally dissimilar from the target?
- How would results change under flaky-test-heavy CI, mobile CI, or industrial pipelines with heterogeneous hardware?
- Is the RL vs. SL trade-off intrinsic to learning paradigm, or partly an artifact of specific implementations and compute budgets?
- Does the new contribution beat FALCON (0.731 median APFD, Defects4J) — not just the source paper's 11 ML methods? If not, what robustness or realism advantage justifies it?
- Are simple heuristics (shortest-tests-first, recent-failure-first) included as baselines? Omitting them is a reviewer red flag given LRTS's findings.

## Extension Tracks (Where A New Paper Beats This One)

The strongest move is not to claim this paper is wrong. The stronger move: argue its benchmark exposed the right problem structure but stopped before the most important realism variables were introduced.

| Direction | Extension track | Strongest claim | Why it can beat the source paper | Minimum threshold (artifact-grounded) |
|---|---|---|---|---|
| **A** | Flaky-test-aware TCP | Historical TCP effectiveness is overstated when failure labels are noisy. | Attacks the label-quality assumption under the benchmark's learning and evaluation logic directly. | Show where performance drops when flaky and confounding failures are separated; must at least match simple "recent-failure + fast-test" heuristics on LRTS (Chrome study + LRTS). |
| **B** | Federated / privacy-preserving pretraining | Transfer remains valuable even when projects cannot share raw CI histories. | Preserves the paper's strongest clue while adding a realistic organizational constraint the paper never tested. | Federated / restricted-data MART variants must retain a substantial share of the original 80%-vs-50% optimal-sequence gain without pooling raw test histories (Zenodo 7036507 + TCP-CI dataset). |
| **C** | LLM-augmented representations | Semantic representations can **reopen the winner landscape** — not just boost scores, but change which methods are robust, which transfer, and which justify overhead. | Challenges whether old method rankings are method properties or feature-era artifacts. | Must outperform FALCON (0.731 median APFD on Defects4J) or demonstrate robustness advantages (under flaky labels or cross-project transfer) that justify higher cost. Beating only the source paper's 11 methods is insufficient (FALCON + DeepOrder). |
| **D** | Android / mobile CI replication | Benchmark conclusions weaken when CI labels, runtimes, and scheduling differ materially from open-source desktop/server projects. | Attacks external validity directly and brings the study into modern applied settings with harder label noise. | Show that at least one source-paper conclusion (winner identity, overhead ranking, or transfer gain) changes or reverses under mobile conditions; use LRTS as the long-running contrast case. |
| **E** | Hyperparameter-robust benchmarking | Fair benchmarks separate technique quality from default settings. | Challenges whether current rankings reflect method design or setup decisions. | Demonstrate ranking instability under varied hyperparameter configurations; show that the MART vs. ACER-PA split is configuration-sensitive. |

**Highest-yield combination:** Flaky-test-aware federated pretraining with semantic representations, evaluated in Android or mobile CI. Aggressive but coherent — targets label realism, data-sharing realism, and feature realism simultaneously.

### Required Experimental Grid

Any new paper must put all baseline tiers on the same board or reviewers will ask. The minimum grid:

1. **Non-ML similarity baselines** — FAST-pw and FAST-log (already running locally)
2. **Heuristic / greedy baselines** — shortest-tests-first, most-recent-failure-first (industry-standard)
3. **Semantic / embedding baselines** — FALCON (UniXcoder + submodular)
4. **Deep learning TCP** — DeepOrder
5. **Original ML/RL methods** — MART, ACER-PA, and at minimum the top-3 from Zenodo 7036507
6. **New contribution** — federated, flaky-aware, or LLM-augmented variants

Winning only battle 5 vs. 6 is the career risk: the community no longer cares if a new ML method beats other ML methods while losing to FALCON or well-tuned heuristics on realistic datasets.

## Concrete Rewrite Instructions

For any paper that builds on this source, these five edits separate a credible follow-on from a summary paper:

1. **Claim format.** Rewrite every major source-paper claim as: *claim → evidence → confounders → why confounders matter → what a stronger benchmark needs to rule them out.*
2. **Flaky tests in motivation, not threats.** Move flaky-test analysis into the main motivation or background section. They directly contaminate historical labels and qualify every effectiveness number.
3. **Pretraining as a constrained systems question.** Foreground cross-project governance and privacy barriers. Federated learning, privacy-preserving transfer, or parameter-sharing baselines are the natural next design space.
4. **LLMs as representation-shift argument.** Do not frame LLM integration as "we also tried embeddings." Argue that richer features may change which methods are robust, which transfer, and which justify overhead — reopening old comparative conclusions rather than just topping leaderboards.
5. **Downgrade deployment language.** Remove or qualify any sentence that implies the source benchmark's recommendations survive noisy labels, heterogeneous CI conditions, or modern feature pipelines without further validation.
6. **Experimental grid discipline.** Include all five baseline tiers: non-ML similarity (FAST), heuristic/greedy, semantic (FALCON), deep learning TCP (DeepOrder), and original ML/RL methods. A paper that only wins against other ML methods while losing to FALCON or heuristics on realistic datasets has not contributed to the right battle.

## Cautions

- This window is source-grounded, but some table and figure areas in the Markdown extraction are noisier than plain text sections.
- Exact numeric claims taken from tables should be verified against the source PDF before formal external citation.
- The paper's recommendations are strong within this study design but depend on project failure profile and feature pipeline.
- The paper's conclusions are controlled benchmark conclusions, not deployment conclusions. That gap is exactly where follow-on work should strike.

## One-Line Carry-Upward Summary

The source paper is a strong unified benchmark but a narrow one: carefully executed within a particular era of features and datasets, strongest when read as a within-study conclusion, weakest when its method rankings are treated as broadly deployable truths; the surrounding ecosystem — non-ML baselines (FAST), semantic methods (FALCON, DeepOrder), and long-running flaky-aware datasets (LRTS) — now supplies both higher baselines and harder questions, and the most credible follow-on move is not to revisit again but to **reconcile benchmark conclusions with realism constraints** along four axes: label quality (flakiness), data-governance (federated pretraining), representation shift (LLM embeddings), and external validity (mobile/Android CI).

## Research Clue Tags

- ml-based-tcp
- continuous-integration
- metric-validity
- data-imbalance
- transfer-learning
- pretraining
- transfer-hardness
- runtime-overhead
- mart
- acer-pa
- flaky-test-aware-tcp
- label-noise
- label-contamination
- federated-pretraining
- llm-augmented-representations
- representation-shift
- external-validity
- android-mobile-ci
- replication-package-zenodo-7036507
- falcon-icst2025
- lrts-issta2024
- submodular-tcp
- unixcoder-embeddings
- deeporder-icsme2021
- tcp-ci-dataset
- non-ml-baseline-risk
- transfer-hardness-lrts
- experimental-grid
- reconcile-benchmark-realism
- fast
- fast-pw
- similarity-based-tcp
- non-ml-baseline
- icse18
