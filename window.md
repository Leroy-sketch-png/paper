# Research Window 001

## Standalone Brief

This document is a standalone upward-facing research briefing for the first research iteration.
It is designed to be readable without access to the source workspace, notes, or extraction files.

## Source

- Paper title: Revisiting Machine Learning based Test Case Prioritization for Continuous Integration
- Source identifier: 2311.13413v1
- Research topic: machine-learning-based test case prioritization for continuous integration

## Scope In Plain Terms

- TCP = test case prioritization.
- CI = continuous integration.
- SL = supervised learning.
- RL = reinforcement learning.
- The paper compares 11 ML-based TCP methods under one controlled setup.
- It evaluates three things: effectiveness, efficiency, and practical applicability.

## Executive Window

- This paper argues that ML-based TCP in CI does not have one universal winner.
- The strongest method depends on the project’s failure-rate regime.
- ACER-PA is strongest on more-failure subjects.
- MART is strongest on less-failure subjects and is the strongest overall practical default.
- Cross-subject pretraining is one of the strongest improvement levers in the paper.
- Metric choice matters: the paper argues earlier comparisons were distorted by problematic metrics and proposes rAPFD as a corrected comparison metric.
- Runtime overhead is not secondary. A technically strong method can still be operationally poor if prediction time is too high.

## Decision-Relevant Claims

### Claim 1. Best method depends on failure-rate regime

- More-failure subjects: ACER-PA performs best.
- Less-failure subjects: MART performs best.
- The paper attributes this split mainly to data imbalance.

Why this matters:
- Any claim of a single globally best ML-TCP method is weak unless it is conditioned on subject failure behavior.

### Claim 2. More training data matters more than code evolution

- Performance changes across CI cycles are attributed mainly to the amount of training data, not primarily to code evolution or test churn.
- RL methods may improve later because they keep adapting online.
- SL methods may stagnate because they train early and then freeze.

Why this matters:
- Transfer learning and pretraining are not side ideas here. They are central practical levers.

### Claim 3. Pretraining is a major improvement path

- Pretrained MART reaches the optimal sequence on 80% of subjects.
- The original MART reaches the optimal sequence on 50% of subjects.

Why this matters:
- Cross-subject data is operationally valuable and should be treated as a serious asset for future ML-TCP systems.

### Claim 4. High effectiveness does not guarantee practical usability

- RL methods generally require much longer training time than SL methods.
- PPO1-LI can become inapplicable in practice because prediction cost can exceed just running the tests.
- MART combines strong effectiveness with low enough overhead to remain attractive in practice.

Why this matters:
- Runtime cost must be treated as a first-class selection criterion, not a secondary benchmark detail.

## Hard Numbers To Carry Upward

- 11 GitHub projects.
- 11 ML-based TCP techniques.
- 800 commits collected per project.
- Pretrained MART: optimal sequence on 80% of subjects.
- Original MART: optimal sequence on 50% of subjects.
- MART can save more than 95% of time-to-first-failure in most subjects.
- PPO1-LI can be inapplicable because prediction overhead can exceed total test execution time in some subjects.

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

> The average training and prediction time of all techniques is shorter than the average commit intervals in all subjects. However, PPO1-LI’s prediction time exceeds the total test execution time in some subjects, which makes it inapplicable. Except for PPO1-LI, other techniques are generally applicable to the CI context. A good TCP technique (e.g., MART) can help developers save more than 95% time cost in most subjects.

> Actionable suggestions: Test duration should be estimated to assess the necessity of applying any TCP techniques. The overhead of TCP techniques deserves more attention and may become the bottleneck of application in practice.

### Discussion-Level Use Guidance

> When facing more-failure subjects, we suggest using ACER-PA as the TCP technique. Conversely, when facing less-failure subjects, we suggest using MART.

> If a subject has a high CI cycle frequency and, consequently, a low average commit interval, we suggest using SL-based techniques such as MART. This is because RL-based techniques tend to be more time-consuming for training and predicting.

> If the subject is newly-created and has few commits which cannot support sufficient training, or the developers want to improve the performance of TCP techniques, we suggest collecting test execution data from other high-quality subjects. These data can then be used to train the ML models and improve their effectiveness.

### Conclusion Signal

> To learn how ML-based TCP techniques perform in CI, we present the first comprehensive study on 11 GitHub projects, including 11 state-of-the-art ML-based TCP techniques. In our study, we systematically analyze the effectiveness, efficiency, and applicability of existing TCP techniques and get a series of findings and actionable suggestions.

## Operational Implications

- Use MART as the safest practical baseline when failure-rate regime is unknown or when operational overhead matters.
- Use ACER-PA when the subject is clearly more-failure and the runtime budget can tolerate heavier RL cost.
- Treat cross-project pretraining as a serious design axis, not a cosmetic enhancement.
- Do not trust cross-paper comparisons that rely heavily on NRPA-style evaluation without checking metric validity.
- Measure prediction latency against actual selected-test execution time before calling a method deployable in CI.

## Cautions

- This window is source-grounded, but some table and figure areas in the Markdown extraction are noisier than plain text sections.
- Exact numeric claims taken from tables should be verified against the source PDF before formal external citation.
- The paper’s recommendations are strong within this study design, but they still depend on the project’s failure profile and feature pipeline.

## One-Line Carry-Upward Summary

This paper’s core clue is that ML-based TCP in CI should be selected by failure-rate regime and runtime budget, not by one global leaderboard, and that cross-subject pretraining is one of the strongest practical paths to materially better results.

## Research Clue Tags

- ml-based-tcp
- continuous-integration
- metric-validity
- data-imbalance
- transfer-learning
- pretraining
- runtime-overhead
- mart
- acer-pa