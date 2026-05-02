# Third-Loop Brutal Research Memo on *Revisiting Machine Learning based Test Case Prioritization for Continuous Integration*

This memo is built on the third-loop window plus external artifacts: the official replication package, non-ML FAST baselines, modern semantic TCP (FALCON), and the LRTS dataset on long-running CI test suites.[cite:35][cite:39][cite:45][cite:37] It is meant to be handed to an editor or coauthor as a demolition map and construction guide: what the source paper nailed, what later work and real datasets do to its core claims, and where a new contribution can credibly hit above that bar.

## New empirical grounding: artifacts that anchor your story

The third-loop window already records that the source paper has a full replication package on Zenodo (7036507), with code for all 11 ML/RL techniques and datasets for 11 projects, including SMOTE-processed variants.[cite:35][cite:45] That package is not just a convenience; it removes the usual excuse for reimplementing fragile baselines. For your paper, it means that any deviation from those baselines must be a conscious design choice, not a missing resource.

The window also logs that FAST, a 2018 ICSE non-ML similarity-based TCP framework, is already running locally, with FAST-pw achieving APFD in the 0.878–0.948 range on flex_v3.[cite:35] This matters because it re-centers the baseline discussion: the original paper positions its 11 ML techniques largely against each other, but the real choice space in 2026 includes non-ML methods that are cheap, interpretable, and already very strong.

FALCON, from ICST 2025, then raises the bar even further: using UniXcoder embeddings and submodular facility-location optimization, it achieves a 16.4 percent higher median APFD than state-of-the-art similarity-based methods (0.731 vs 0.628) on Defects4J while keeping runtime modest.[cite:39] This baseline makes it clear that any LLM- or embedding-based contribution in your work must do better than both FAST-style similarity and FALCON-style submodular diversity, not just better than the original paper's 11 ML methods.

Finally, LRTS, from ISSTA 2024, introduces a dataset with 21,255 CI builds and 57,437 test-suite runs from 10 large-scale projects, explicitly studying flaky tests and long-running suites.[cite:37][cite:40] LRTS shows that simple policies such as prioritizing faster tests that recently failed can outperform more sophisticated techniques in some contexts.[cite:21] That is a direct challenge to any narrative that sophisticated ML should be assumed superior once datasets become realistic.

## How these artifacts change the interpretation of the source paper

The source paper still delivers a valuable unified benchmark and the key insight that no single ML method wins universally; MART and ACER-PA occupy different failure-rate regimes, and pretraining MART substantially improves optimal-sequence frequency.[cite:35][cite:2] But the existence of FAST, FALCON, DeepOrder, and LRTS means that the paper's implicit baseline universe is now clearly incomplete.

Compared with FAST, the source paper's ML techniques need to justify their extra complexity and overhead in terms of real gains over strong similarity-based baselines, not just over weaker or ad hoc prior ML methods.[cite:35][cite:24] The third-loop window notes that FAST is already hitting high APFD on classic Defects4J-style subjects; this suggests that any future benchmark must put ML and non-ML baselines on the same board.

Compared with FALCON, the source paper's feature and representation assumptions look dated.[cite:35][cite:39] FALCON demonstrates that submodular optimization over semantic embeddings can outdo similarity-based baselines with relatively low runtime, which in turn implies that some of the "winner" methods in the source paper might lose once representation quality and diversity-aware selection are upgraded.[cite:39]

Compared with LRTS, the source paper's assumptions about CI scale, duration, and label behavior look narrow.[cite:35][cite:37] LRTS test suites last an average of 6.5 hours per run and explicitly analyze flaky tests and frequently failing tests; in that space, many traditional TCP techniques perform differently from what smaller, cleaner benchmarks would suggest.[cite:21][cite:37]

## Deepening the flaky-test attack

The third-loop window already escalates flaky tests from a footnote to a core attack: a Chrome CI study reports that 99.58 percent of observed failures were flaky, which implies that historical labels can be dominated by nondeterministic noise.[cite:35][cite:23] LRTS reinforces this by explicitly accounting for confounding test failures and showing that frequently failing tests are often flaky and not strongly correlated with code changes.[cite:40]

Taken together, these sources support a harsher statement: in realistic CI ecosystems, naive history-based TCP can achieve strong measured APFD while being only weakly predictive of true regressions, because it is partially learning noise patterns and infrastructure idiosyncrasies.[cite:23][cite:40]

For your paper, the move is to connect the Chrome flaky statistic, LRTS's confounding-failure handling, and the source paper's clean-label assumption into a single narrative: the original unified benchmark is valuable but label-naive.[cite:35][cite:23][cite:40] It treats failures as ground truth events when, in many CI histories, they are mixtures of regressions and flakiness.

## Reframing transfer: promise versus hardness under modern datasets

The original paper's strongest forward-looking clue is that pretraining MART on cross-subject data yields a clear performance boost (80 percent versus 50 percent optimal sequences under its evaluation).[cite:2][cite:35] The third-loop window correctly distinguishes transfer promise from transfer hardness, and the new artifacts sharpen that distinction.

The replication package reveals that the dataset is limited to 11 open-source subjects with specific languages and build systems, plus SMOTE-enhanced versions.[cite:45] This makes it easier for source and target projects to share structural and behavioral similarities that might not exist in more diverse or industrial settings.

LRTS, by contrast, spans 10 large-scale projects with long-running suites and explicitly studies tests that fail with no prior failure history.[cite:21][cite:37] It provides a natural environment to stress-test transfer hardness: does a model pretrained on one cluster of long-running suites help on another, or do project-specific behaviors dominate?

Your paper can leverage this by explicitly structuring experiments around two axes:

- Source-paper replication-plus-transfer: replicate pretraining results using Zenodo 7036507, possibly adding federated or privacy-preserving variants.[cite:45]
- LRTS-based transfer hardness: test whether architectures that win on the original dataset still transfer on LRTS when faced with long-running, flaky-influenced suites.

That way, the new work does not just repeat "pretraining helps" but quantifies when transfer breaks, how flakiness and long-duration tests interact with transfer, and whether federated constraints change the calculus.

## LLM and representation-shift arguments in the presence of FALCON and DeepOrder

DeepOrder (ICSME 2021) already introduced deep learning for TCP in CI with a regression-style neural model that consumes historical test execution records and outperforms some prior approaches on efficiency and detection.[cite:36] FALCON (ICST 2025) demonstrates that UniXcoder-based semantic embeddings combined with submodular optimization significantly outperform similarity baselines.[cite:39]

These two works jointly undermine any claim that the space of representation learning for TCP is underexplored.[cite:36][cite:39] The interesting question is no longer whether deep or semantic models can beat classic heuristics; it is how those models behave under flaky labels, federated constraints, and long-running suites.

For your LLM-oriented direction, this leads to a tougher but more honest bar:

- An LLM-enhanced method should be evaluated against FALCON, DeepOrder, and FAST, not just against the original 11 ML techniques.
- Representation arguments should be framed as representation-shift questions: which comparative results from the original paper survive when representation moves from handcrafted CI features to LLM-derived semantics?
- Attack the stability of the original ranking: show that when feature space changes, the method order (e.g., MART versus ACER-PA versus RL baselines) can change as well.

This framing makes the LLM component more than a superficial add-on; it becomes central to revisiting the paper's most visible leaderboard claims.[cite:35][cite:36][cite:39]

## Non-ML baselines and the risk of overfitting on ML-only battles

FAST and other similarity-based or greedy methods remind reviewers that simple, non-ML approaches can still perform extremely well, especially when calibrated with real project history and lightweight features.[cite:35][cite:24][cite:32] Recent industrial case studies continue to report substantial APFD gains and test suite reductions from heuristic or greedy algorithms alone.[cite:43]

The risk for any new ML-heavy paper is to win a battle the community no longer cares about: outcompeting narrow ML baselines while losing to well-tuned heuristic or semantic methods on realistic datasets.[cite:32][cite:39] The third-loop window partly addresses this by anchoring FAST, but your paper should go further: treat non-ML, semantic, and ML/RL methods as peers in experimental design.

A strong experimental grid for your work would therefore include:

- FAST-style similarity baselines (FAST-pw and others).
- Traditional heuristic/greedy baselines (e.g., shortest-tests-first, most-recent-failure-first, or industry-style heuristics).
- Semantic baselines like FALCON.
- The original 11 ML methods, including MART, ACER-PA, and DeepOrder.
- Any new federated, flaky-aware, or LLM-based variants you introduce.

This makes your contribution harder to deliver but much more convincing when it succeeds.

## Updated extension tracks with explicit thresholds

The third-loop window already lists four main extension tracks; the artifacts let you refine each with explicit empirical thresholds.

| Track | External artifact(s) | Minimum threshold for a credible claim |
|---|---|---|
| Flaky-test-aware TCP | Chrome flaky study, LRTS | Must show where historical TCP performance drops or changes when flaky and frequently failing tests are separated out; should at least match simple "recent failures + fast tests" heuristics on LRTS.[cite:23][cite:21][cite:40] |
| Federated / privacy-preserving pretraining | Zenodo 7036507, TCP-CI dataset | Must demonstrate that federated or restricted-data variants of MART-style pretraining retain a substantial portion of the original transfer gains without pooling raw test histories.[cite:45][cite:41] |
| LLM / semantic representations | FALCON, DeepOrder | Must outperform FALCON on shared benchmarks or show robustness advantages (e.g., under flaky labels or cross-project transfer) that justify higher costs.[cite:36][cite:39] |
| Android / mobile CI replication | LRTS as contrast, plus any mobile CI dataset you introduce | Must show that conclusions drawn from the original 11 subjects weaken or flip under mobile conditions; especially, overhead and flakiness should change the perceived winners.[cite:37][cite:42] |

By hard-coding these thresholds into your internal planning, you preempt reviewer feedback that says "but what about FALCON" or "but why not use LRTS".

## Concrete guidance for your editor-facing draft

When you bring this to an editor or advisor, the most helpful structural shift is to stop treating the source paper as the center of the universe and start treating it as one node in a now-dense TCP research graph.

Rewrite the positioning roughly as follows:

- The original paper provided the first unified ML benchmark for TCP in CI with a clear message: no universal winner, conditional on failure regimes and overhead.
- Subsequent work (DeepOrder, FALCON, LRTS, TCP-CI) has expanded the space along representation, optimization, dataset scale, and label realism.
- The most important open questions now concern label quality (flakiness), data-governance constraints (federated vs centralized pretraining), representation shift (classic features vs LLM embeddings), and external validity (desktop/server vs mobile/Android CI).

Then define your paper not as "revisiting again" but as "reconciling benchmark conclusions with realism constraints" using those four axes.

## Blunt third-loop verdict

The third-loop window plus external artifacts confirms that the source paper is a strong benchmark but a narrow one.[cite:35][cite:45] It is strongest when read as a carefully executed experiment within a particular era of features and datasets and weakest when its method rankings are treated as broadly deployable truths.

The surrounding ecosystem—non-ML baselines, semantic methods, long-running and flaky-aware datasets—now supplies both higher baselines and harder questions.[cite:24][cite:36][cite:39][cite:37] That is good news for your project: there is real headroom for a paper that confronts those realities directly rather than extending the original benchmark in a straight line.

