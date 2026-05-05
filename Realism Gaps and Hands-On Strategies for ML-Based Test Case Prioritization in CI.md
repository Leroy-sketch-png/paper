# Realism Gaps and Hands-On Strategies for ML-Based Test Case Prioritization in CI

## Executive Summary

Machine-learning-based test case prioritization (ML-TCP) for continuous integration (CI) has a strong benchmark story but a much weaker deployment story. The ICSME 2023 benchmark by Zhao et al. compares 11 ML-based TCP techniques across 11 projects and finds a regime-dependent recommendation: ACER-PA for high-failure subjects, MART for low-failure subjects, with pretrained MART achieving optimal sequences on about 80% of subjects versus 50% for original MART. However, this benchmark assumes clean labels, centralized data for pretraining, a fixed representation pipeline, and relatively controlled environments, which rarely all hold in practice.[^1][^2][^3]

Recent work on flaky tests, federated learning, and semantic test representations shows how each of these assumptions can break. Flaky tests systematically distort labels and metrics, centralized pretraining conflicts with data governance, semantic embeddings can be brittle or misaligned with failure behavior, and mobile/Android CI introduces extreme flakiness and duration variance that affect time-based metrics.[^4][^5][^6][^7][^8][^9][^10][^11]

This report synthesizes external literature into a concrete strategy along four "realism gaps" (labels, governance, representation, external validity) and maps them to specific, small-scale experiments a resource-constrained researcher can run. The goal is a conditional-validity map for ML-TCP: when the benchmark recommendation survives, when it weakens, and where it might invert, along with pragmatic experiment designs that fit in an office-laptop budget.

***

## 1. Benchmark Baseline: What the ICSME Paper Actually Says

The arXiv/ICSME 2023 paper "Revisiting Machine Learning based Test Case Prioritization for Continuous Integration" provides the central benchmark baseline. It evaluates 11 representative ML-based TCP techniques on 11 open-source projects with 800 commits per project under a unified CI-like setup, using rAPFD and timing metrics to compare techniques.[^3][^1]

Key findings include:

- There is no universal winner; the best method depends on the failure-rate regime, with ACER-PA recommended for high-failure subjects and MART for low-failure subjects.[^2][^1]
- Pretraining MART with cross-subject data followed by within-subject fine-tuning dramatically improves performance, raising optimal sequence attainment from around 50% to 80% of subjects.[^1][^2]
- Performance varies across CI cycles mainly due to available training data volume, more than code evolution or test addition/removal, highlighting data imbalance and history length as key drivers.[^2][^1]

Other ML-TCP work, such as DeepOrder, emphasizes similar themes: leveraging long test histories, including duration and execution status, to rank tests and improve APFD and time-effectiveness over both industrial heuristics and state-of-the-art baselines. Complementary work like Test2Vec focuses on embedding execution traces into vectors for downstream tasks including TCP, again under relatively clean, research-constructed conditions.[^12][^13][^8]

This benchmark baseline is valuable, but its conclusions rest on several implicit assumptions that do not always hold in real CI systems: labels reflect real regressions, cross-project data can be pooled, representation pipelines are stable and aligned with failure behavior, and environments behave like the benchmark subjects.

***

## 2. Realism Gap A: Label Realism and Flaky Tests

### 2.1 What the literature says about flakiness

Flaky tests are tests that pass or fail nondeterministically under the same code and expected behavior, often due to timing, concurrency, environment, or order dependencies. A systematic survey of flaky tests finds that asynchronous timing issues and concurrency are leading causes, while platform dependencies can account for roughly a third of flaky-test-related bug reports in some datasets.[^7][^10]

Large-scale empirical studies on CI platforms show the scale of the problem. For instance, an analysis of Travis CI failures reported that about 47% of failing builds that were manually restarted eventually passed without code changes, indicating widespread flakiness. Industrial approaches such as Facebook's Probabilistic Flakiness Score (PFS) quantify flakiness per test based on normal CI runs, without extra reruns, and use that signal to drive repair and reliability goals.[^5][^6][^10][^7]

Recent ML work focuses on predicting flakiness. A 2024 master's thesis from Oulu evaluates ML models for distinguishing flaky from genuine failures using virtual machine data, finding that boosted tree models (XGBoost, RandomForest, GradientBoosting) can achieve accuracy in the 96–98% range with high precision and recall, and with prediction times low enough for high-traffic CI environments. Feature-set innovations such as FLAKE16 encode execution features and system calls to improve ML-based flaky-test detection beyond earlier approaches.[^4][^5]

### 2.2 Why this threatens ML-TCP benchmark conclusions

ML-TCP techniques like MART, DeepOrder, and Test2Vec-driven methods typically treat past failures as ground truth labels or rely on execution histories that implicitly encode labels. If a substantial fraction of observed failures are flaky rather than genuine regressions, the training signal for supervised or reinforcement learning methods is systematically distorted.[^8][^12][^1]

This can manifest in multiple ways:

- Tests with high flakiness may be treated as "high-value" because they fail often, leading methods to over-prioritize noisy tests that do not indicate real regressions.
- APFD/rAPFD metrics computed on mixed genuine and flaky failures no longer strictly measure fault detection speed, but rather "failure-event" detection speed, which may over-reward strategies that surface noisy tests early.[^10][^7]
- Data-imbalance strategies tuned on genuine-failure distributions may behave differently when flakes dominate rare-failure regimes.

Because the benchmark by Zhao et al. does not explicitly model or correct for flakiness in its datasets, its regime-dependent recommendations may be over-optimistic for systems where flakiness is common.[^3][^1]

### 2.3 Concrete experiment designs for a resource-constrained researcher

The literature suggests several small-scale experiments that can be run without large clusters:

1. **Synthetic flakiness injection on an existing subject**  
   - Take one of the open-source subjects from the benchmark or a similar CI dataset and treat its observed failures as genuine for a baseline.[^1]
   - Inject synthetic flakiness by randomly flipping a percentage of pass/fail outcomes on tests that were originally passing or failing, at levels such as 5%, 10%, 20%.[^10]
   - Re-train or re-evaluate at least one ML-TCP method (e.g., MART-like) and one non-ML baseline (e.g., FAST or heuristic) under each noise level, and compare rAPFD and time-to-first-failure.

2. **Flakiness-aware metric analysis**  
   - Borrow ideas from PFS: compute a simple flakiness score per test based on CI history (e.g., frequency of outcome change).[^6][^7]
   - Re-compute APFD/rAPFD on a subset of failures filtered by low predicted flakiness versus the full set, to see how the perceived ranking performance of each method changes.

3. **Toy analytical model**  
   - Build a simple probabilistic model: with flakiness rate \(p\), a history-based method that prioritizes frequently failing tests will see its reward inflated by a factor dependent on \(p\), whereas methods that diversify or rely less on history may be more robust. This does not require heavy compute but can be tied directly back to empirical patterns in the literature.[^7][^10]

These experiments do not require new datasets of flaky tests; they reuse existing benchmark data and inject controlled noise, aligning them with current flakiness research while staying within a laptop budget.

***

## 3. Realism Gap B: Governance Realism and Federated/Constrained Pretraining

### 3.1 Centralized pretraining in the benchmark

The ICSME benchmark recommends cross-subject pretraining of MART followed by within-subject fine-tuning, showing that this transfer learning approach boosts optimal-sequence performance from about 50% to 80% of subjects. This implicitly assumes that CI execution data from multiple projects can be pooled into a single centralized dataset.[^2][^1]

Industrial practice and privacy regulations often contradict this assumption. Enterprises dealing with sensitive data and strict governance (e.g., financial, healthcare, or highly regulated software contexts) may not be allowed to share raw test logs across projects or organizational boundaries, even internally. Federated learning and federated analytics have emerged precisely to enable learning from distributed, privacy-sensitive data without centralizing it.[^14][^15][^16][^17]

### 3.2 Lessons from federated learning literature

Federated learning frameworks describe training a global model across many clients while keeping data local, with challenges around heterogeneity, data imbalance, and evaluation of local contributions. Edge-oriented FL frameworks emphasize containerized deployments, client/server orchestration, and monitoring in distributed setups, highlighting both the feasibility and complexity of such approaches.[^15][^16]

This literature suggests that applying pretraining in a CI context under governance constraints would likely require federation-style setups, where models are trained across projects without sharing raw execution logs. It also implies that the effectiveness of pretraining may degrade when data is non-IID, imbalanced, or restricted to smaller subsets.[^16][^17][^15]

### 3.3 Concrete degraded-pretraining experiments

A resource-constrained researcher can meaningfully approximate governance limits without building a full FL framework:

1. **Upper vs lower bound pretraining experiment**  
   - Centralized upper bound: mimic the ICSME approach by pretraining MART-like models on all available subjects, then fine-tune per subject and measure rAPFD and optimal-sequence percentages.[^1][^2]
   - Restricted pretraining: repeat the process but remove subsets of projects from the pretraining pool—e.g., pretrain on half the subjects, on only those in a similar domain, or on only small projects.[^1]
   - Compare performance across scenarios to estimate how sensitive the pretraining gains are to reduced cross-project data. This provides a practical "governance penalty" curve.

2. **Pseudo-federated training on a single machine**  
   - Simulate federated training by alternating local updates on project-specific subsets and aggregating parameters centrally, using a simple FedAvg-like loop.[^15][^16]
   - Compare this pseudo-federated model to the fully centralized pretraining baseline on a subset of subjects to see how much performance is lost when only model parameters, not raw data, move.

3. **Representation of governance in the recommendation**  
   - Use results to explicitly frame centralized pretrained MART as an upper bound for organizations that cannot or will not centralize test logs, and provide guidance on when local-only or weakly shared training may push teams back toward FAST/heuristics.

These experiments require only reusing the existing benchmark pipeline with different data splits and training protocols, making them feasible on modest hardware.

***

## 4. Realism Gap C: Representation Realism and Semantic Embeddings

### 4.1 Existing semantic and history-based representations

Beyond handcrafted feature pipelines, several works propose richer representations for tests:

- DeepOrder uses deep neural networks over historical test execution data, including duration and status, to rank tests, demonstrating improved APFD and time-effectiveness compared to industrial baselines and history-based techniques constrained to the last few cycles.[^13][^12]
- Test2Vec embeds execution traces (sequences of method calls, inputs, and outputs) into fixed-length vectors, and uses similarity/diversity in this latent space for TCP and related tasks, showing benefits over static code-based methods in large-scale experiments.[^8]
- Other ML-driven TCP approaches operate on metadata, natural language descriptions, or black-box system tests, again under relatively idealized data conditions.[^18][^19]

These representations show that semantic or behavioral embeddings can be powerful, but they also assume that the representation pipeline is well-aligned with failure behavior and that training data is sufficient.

### 4.2 Risks highlighted by flakiness and Android testing literature

Flakiness surveys and Android testing work show that real-world test behavior is heavily influenced by asynchronous events, device state, platform differences, and UI timing, all of which may be poorly captured by naive code-level tokenization or static representations.[^9][^11][^7][^10]

In Android and UI-centric testing, flakiness is amplified by device variability, emulator vs real-device discrepancies, and concurrency in event handling, requiring specialized techniques to detect and manage flaky tests. Execution-trace-based embeddings like Test2Vec explicitly aim to capture dynamic behavior, but they are evaluated in controlled environments and may still be sensitive to noise and platform-specific artifacts.[^20][^11][^9][^8]

### 4.3 Concrete representation ablations with office-laptop constraints

Assuming a simple BPE-style proxy embedding pipeline over test code or metadata, there are several cheap ablations that can be run to probe representation realism:

1. **Tokenization and vocabulary size ablations**  
   - Vary tokenization granularity (e.g., character-level vs subword vs identifier-based) and vocabulary size, and re-evaluate a fixed TCP model on a small set of subjects.[^8]
   - Track changes in mean delta APFD relative to FAST-pw and in ranking correlations. If all cheap variants remain substantially worse than FAST, this supports a conclusion that naive semantic signals are fragile.

2. **Adding simple structural metadata**  
   - Enrich the embedding inputs with trivial structural features such as file-type tags, directory path buckets, or test-category labels (unit vs UI vs integration), which flakiness surveys identify as correlated with different behaviors.[^7][^10]
   - Evaluate whether this low-cost metadata closes any of the gap to FAST-pw.

3. **Error analysis on disagreements with FAST**  
   - For test-order pairs where the proxy embedding strongly disagrees with FAST and leads to later detection of genuine failures, characterize those tests: file type, typical duration, historical flakiness, platform-specific issues, etc.[^10][^7]
   - Use these patterns to articulate hypotheses about where representation pipelines must be more behavior- or environment-aware.

These ablations help justify a nuanced claim: simple diversity-based baselines like FAST remain strong and robust under representation shifts, and naive "LLM-flavored" or code-token embeddings may underperform or even mislead unless carefully grounded in dynamic behavior.

***

## 5. Realism Gap D: External Validity and Harder Deployment Environments

### 5.1 Evidence from Android and mobile CI

Mobile and Android instrumentation testing in CI is particularly challenging due to flaky tests, emulator vs device differences, and long, variable test durations. Research on Android instrumentation tests in CI highlights cost, brittleness, and configuration drift as recurring obstacles, with headless CI environments exacerbating nondeterminism and flakiness.[^21][^11][^9][^20]

FlakeScanner and related tools for Android focus on concurrency-related flakiness by exploring event orderings on emulators and devices, indicating that UI and event-driven behavior is a major source of nondeterministic outcomes. Practitioner guidelines for Android UI testing emphasize flakiness protection practices like waiting for content, isolating environments, and sorting tests based on duration to reduce cross-device scheduling artifacts.[^22][^9][^20]

Performance benchmarking in Android CI, such as using Jetpack Macrobenchmark with Firebase Test Lab, further shows that long-running benchmarks must contend with limited device timeouts (e.g., 45-minute limits) and the need to run on real devices rather than emulators to avoid inconsistent results. These factors highlight that time-based metrics such as APFD and rAPFD must be interpreted differently when test durations and platform behavior differ drastically from the benchmark environment.[^21]

### 5.2 Implications for ML-TCP recommendations

The ICSME benchmark subjects are open-source projects with relatively stable, code-based tests and CI environments that do not capture the extremes of mobile/UI flakiness, device heterogeneity, or long, macro-benchmark-style tests. In such settings, the regime-dependent recommendation (ACER-PA vs MART) and the pretraining gains for MART are meaningful, but they may not transfer directly to Android/mobile CI where:[^11][^3][^21][^1]

- Test durations vary widely, and timeouts become a primary failure mode.
- Platform dependencies and environment drift contribute heavily to flakiness.
- Device/emulator behavior is non-deterministic across runs and infrastructure providers.

In these environments, time-to-first-useful-failure and cost-effective coverage may depend more on duration-aware strategies, flakiness-aware ordering, and resource-constrained scheduling than on the exact ranking learned on traditional benchmark subjects.

### 5.3 Synthetic external-validity stress tests

Without access to large Android datasets, a resource-constrained researcher can still perform informative stress tests:

1. **Duration skew injection**  
   - Take a project with relatively uniform test durations and inject a small number of synthetic "very long" tests, or assign longer durations to tests covering certain components.[^12][^21]
   - Re-compute time-to-first-failure and rAPFD for ML-TCP methods vs FAST/heuristics under the new duration distribution. Investigate whether methods that excelled under uniform durations still dominate when long tests are present.

2. **Timeout-aware evaluation**  
   - Introduce a global suite-level timeout and measure how often each prioritization strategy encounters timeouts before executing key failure-detecting tests.[^11][^10]
   - This approximates mobile CI conditions where device time is limited and tests compete for fixed slots.

3. **Platform-sensitivity scenarios**  
   - Use practitioner reports and flakiness surveys to construct qualitative scenarios where platform dependency is a major cause, then reason about how ML-TCP methods trained under one platform’s behavior might mis-rank tests when ported to another.[^11][^7][^10]
   - This can be presented as a thought experiment backed by empirical patterns rather than as a full dataset-driven study.

These stress tests do not require new Android apps but allow the paper to argue more concretely about external validity limits of benchmark recommendations.

***

## 6. Cross-Cutting Themes and a Conditional-Validity Map

### 6.1 Flakiness and label quality as first-order concerns

Across flakiness detection, ML prediction of flakiness, and multivocal reviews of causes and impacts, there is strong evidence that label quality in CI is a first-order concern, not a minor nuisance. When ML-TCP methods build on historical failures to learn rankings, uncorrected flakiness can mislead both training and evaluation.[^23][^4][^7][^10]

Consequently, any deployment-oriented recommendation of ML-TCP should:

- Treat flakiness detection or mitigation (reruns, flakiness scores, test quarantining) as a precondition for trusting ML-based rankings.
- Consider reweighting, down-weighting, or excluding highly flaky tests from training sets.
- Evaluate rAPFD both on all failures and on a subset filtered for low predicted flakiness.

### 6.2 Pretraining as an upper bound under governance

Federated learning literature and governance-focused cloud analytics show that unified, centralized training datasets are increasingly incompatible with strict privacy and compliance regimes. Thus the cross-subject pretraining gains demonstrated in the benchmark should be framed as an upper bound achievable only when organizations can centralize CI histories.[^17][^14][^16][^15]

A conditional-validity map should distinguish between:

- Organizations able to centralize CI logs internally, where pretrained MART-like approaches are realistic.
- Organizations restricted to per-project or per-domain training, where pretraining benefits are degraded.
- Organizations that require full FL-style federation, where bandwidth, non-IID data, and orchestration overhead further complicate pretraining.

### 6.3 Representation and external validity as intertwined issues

Representation choices (static code tokens, execution traces, environment features) interact strongly with external validity. Execution-trace embeddings like Test2Vec can better capture behavioral nuances but may still fail to generalize to environments with heavy platform dependencies and complex UI/interaction patterns.[^9][^8][^11]

Mobile and Android CI examples show that environment and platform features are often as important as code-level behavior in determining failures and flakiness. For deployment guidance, representation realism must therefore be considered jointly with environment realism: a representation that ignores device state, timing, or concurrency may be systematically fragile in those settings.[^20][^21][^9][^11]

### 6.4 Example conditional-validity table

A conceptual conditional-validity table grounded in the literature might look like this:

```markdown
| CI condition                                      | Benchmark assumption status          | Trust in MART/ACER-PA advice       | Recommended stance                           |
|--------------------------------------------------|--------------------------------------|------------------------------------|----------------------------------------------|
| Low flakiness, centralized data, code-based tests| Mostly satisfied                     | High                               | Use benchmark recommendation with minor checks. |
| High flakiness, centralized data                 | Label assumption violated            | Medium                             | Apply flakiness-aware filtering; compare to FAST. |
| Low flakiness, no cross-project data sharing     | Governance assumption violated       | Medium                             | Treat pretrained MART as upper bound; test local-only models. |
| High flakiness, no data sharing                  | Labels & governance violated         | Low                                | Favor robust baselines; require local experiments. |
| Mobile/Android, long/variable durations          | Representation & environment differ  | Unknown/Low                        | Require stress tests and external-validity experiments. |
```

This table is illustrative; concrete thresholds and guidance should be refined based on the small-scale experiments described earlier.

***

## 7. Practical Guidance for a Resource-Constrained Researcher

Based on the literature, a student with limited hardware but strong understanding can still make a substantial contribution by:

- Selecting 2–3 realism gaps and running targeted, low-cost experiments (e.g., synthetic flakiness injection, degraded pretraining, representation ablations, duration skew stress tests) on subsets of existing benchmark data.[^12][^8][^1]
- Explicitly labeling evidence status (verified benchmark vs executed proxy vs framework vs staged), a practice encouraged by the diversity of evidence levels observed in flakiness, FL, and Android CI research.[^4][^7][^10][^11]
- Framing findings in terms of conditional validity: when exactly the benchmark recommendation can be trusted and when practitioners should be cautious or prefer simpler baselines.

This strategy aligns with current research directions on flaky tests, federated learning, and semantic embeddings, while remaining feasible on an office laptop.

---

## References

1. [Revisiting Machine Learning based Test Case Prioritization for ...](https://arxiv.org/abs/2311.13413) - Abstract page for arXiv paper 2311.13413: Revisiting Machine Learning based Test Case Prioritization...

2. [ML Test Case Prioritization in CI | PDF | Machine Learning - Scribd](https://www.scribd.com/document/971103224/2023-Revisiting-Machine-Learning-Based-Test-Case-Prioritization-for-Continuous-Integration) - This paper presents a comprehensive study on machine learning-based test case prioritization (TCP) t...

3. [Revisiting Machine Learning based Test Case Prioritization for Continuous Integration](http://arxiv.org/abs/2311.13413) - To alleviate the cost of regression testing in continuous integration (CI), a large number of machin...

4. [[PDF] EVALUATION OF MACHINE LEARNING MODELS IN PREDICTING ...](https://oulurepo.oulu.fi/bitstream/handle/10024/51068/nbnfioulu-202406285038.pdf;jsessionid=E581A01B889D81175D4C0434360EE041?sequence=1)

5. [[PDF] Evaluating features for machine learning detection of order](https://eprints.whiterose.ac.uk/id/eprint/230092/1/parry2022b.pdf) - Abstract—Flaky tests are test cases that can pass or fail without code changes. They often waste the...

6. [How Are We Using Pfs?](https://engineering.fb.com/2020/12/10/developer-tools/probabilistic-flakiness/) - Facebook’s codebase changes each day as engineers develop new features and optimizations for our app...

7. [Test flakiness' causes, detection, impact and responses](https://www.sciencedirect.com/science/article/pii/S0164121223002327) - This paper presents a multivocal review that investigates how flaky tests, as a topic, have been add...

8. [[PDF] Test2Vec: An Execution Trace Embedding for Test Case Prioritization](https://arxiv.org/pdf/2206.15428.pdf) - Most automated software testing tasks, such as test case generation, selection, and prioritization, ...

9. [[PDF] Flaky Test Detection in Android via Event Order Exploration](https://abhikrc.com/pdf/FSE21.pdf) - Due to the lack of a test- ing benchmark for flaky tests, we created the first subject-suite. FlakyA...

10. [A Survey of Flaky Tests - ACM Digital Library](https://dl.acm.org/doi/fullHtml/10.1145/3476105) - Tests that fail inconsistently, without changes to the code under test, are described as flaky. Flak...

11. [Android Instrumentation Testing in Continuous Integration - arXiv](https://arxiv.org/html/2604.03438v1) - We study how open-source Android apps run instrumentation tests in CI by analyzing 4,518 repositorie...

12. [[2110.07443] DeepOrder: Deep Learning for Test Case Prioritization ...](https://arxiv.org/abs/2110.07443) - DeepOrder learns failed test cases based on multiple factors including the duration and execution st...

13. [[PDF] DeepOrder: Deep Learning for Test Case Prioritization in ... - arXiv](https://arxiv.org/pdf/2110.07443.pdf)

14. [fbloc-2022-893747 1..9](https://www.frontiersin.org/journals/blockchain/articles/10.3389/fbloc.2022.893747/pdf)

15. [A Framework for testing Federated Learning algorithms using an edge-like environment](https://ar5iv.labs.arxiv.org/html/2407.12980) - Federated Learning (FL) is a machine learning paradigm in which many clients cooperatively train a s...

16. [[論文評述] A Framework for testing Federated Learning algorithms ...](https://www.themoonlight.io/tw/review/a-framework-for-testing-federated-learning-algorithms-using-an-edge-like-environment) - The paper titled "A Framework for Testing Federated Learning Algorithms Using an Edge-like Environme...

17. [Federated learning: what it is and how it works | Google Cloud](https://cloud.google.com/discover/what-is-federated-learning) - Federated learning is a privacy-preserving AI and machine learning technique. Learn about its model,...

18. [[PDF] Prioritization of Regression Test Cases Based on Machine Learning ...](https://dergipark.org.tr/en/download/article-file/3769500) - This study confirms ML techniques can prioritize regression test scenarios effectively. • RF model e...

19. [[PDF] Machine Learning-Driven Test Case Prioritization Approaches for ...](https://www.ama-science.org/proceedings/download/ZwtmZt==) - We designed our approach to prioritize manually executed test cases, i.e., it analyzes meta-data and...

20. [Flakiness - Proper Android UI Testing](https://android-ui-testing.github.io/Cookbook/practices/flakiness/) - Flakiness protection · 1. Wait for the content appearing · 2. Use isolated environment for each test...

21. [Benchmarking Android applications in CI/CD pipelines - CircleCI](https://circleci.com/blog/benchmarking-android/) - In this tutorial you will get started with the Jetpack benchmarking libraries, and learn how to impl...

22. [100% Flakiness-free UI test automation with Kaspresso and Allure ...](https://blog.codemagic.io/100-flakiness-free-ui-test-automation-with-kaspresso-and-alluretestops/) - Learn about new Android UI test framework and integration to your CI/CD pipeline. ... CI/CD Build Sp...

23. [[PDF] Understanding the Lifecycle of Flaky Tests and Identifying Flaky ...](https://spectrum.library.concordia.ca/id/eprint/993837/1/Malmir_MCompSc_F2024.pdf) - Flaky tests are tests that pass and fail on different executions of the same version of a code under...

