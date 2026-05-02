# Second-Loop Brutal Research Memo on *Revisiting Machine Learning based Test Case Prioritization for Continuous Integration*

This memo is a second-loop research companion built from the updated critical window and external evidence on flaky-test-heavy CI and newer LLM-oriented TCP directions.[cite:2][cite:23][cite:31] It is written for offline paper revision and assumes the goal is not just to understand the source paper, but to pressure-test it until its strongest surviving claims and most exploitable weaknesses become obvious.[cite:2]

## What survives after a harsher reading

The source paper still deserves to be taken seriously for three reasons.[cite:2] First, it brings 11 ML-based TCP techniques into one controlled evaluation setup across 11 open-source subjects, which is more useful than cross-paper leaderboard reading based on incompatible datasets and metrics.[cite:2] Second, it makes a strong case that there is no universal winner: ACER-PA performs best on more-failure subjects, MART performs best on less-failure subjects, and pretrained MART is the strongest practical default under the study's conditions.[cite:2]

Third, the paper is right to place operational overhead inside the main evaluation frame.[cite:2] Its finding that PPO1-LI can become inapplicable because prediction time may exceed total test execution time is not just an implementation annoyance; it is a reminder that CI optimization is a deployment problem, not a ranking contest.[cite:2] These are real contributions and should not be downplayed in a follow-on paper.[cite:2]

## What becomes weaker on second inspection

The paper's comparative strength does not automatically translate into deployment strength.[cite:2] It solved a comparability problem under one benchmark design, but many of its most practical-sounding recommendations still rest on narrow assumptions about project type, label quality, feature pipeline, and runtime environment.[cite:2] The updated window is correct to say that the paper standardized the battlefield, but the harsher version is this: the battlefield may have been too clean, too open-source-centric, and too historically stable to support strong deployment-level prescriptions.[file:18][cite:2]

The failure-rate regime claim is especially vulnerable.[file:18][cite:2] The paper presents the ACER-PA versus MART split as mainly caused by data imbalance, but that explanation competes with other possibilities: benchmark composition, implementation choices, default hyperparameters, subject maturity, and feature representation may all help create the apparent split.[file:18][cite:2] Unless those factors are disentangled more aggressively, the claim should be treated as a robust observed pattern in this benchmark, not a settled explanation of method superiority.[file:18][cite:2]

The training-data claim is also shakier than it first appears.[file:18][cite:2] Saying that performance changes across CI cycles are caused mainly by training-data volume rather than code evolution or test churn sounds causal, but the evidence described in the window is closer to comparative correlation under a shared setup.[file:18][cite:2] A tougher version of the critique is that training-data growth may be entangled with temporal stabilization, project maturity, changing failure prevalence, and feature drift, none of which are trivial nuisances in CI.[file:18][cite:2]

## The flaky-test escalation

The biggest realism challenge now is not just that the benchmark lacks flaky-test analysis, but that flaky failures can fundamentally distort historical TCP evaluation.[file:18][cite:23] A study on Chrome's historical test prioritization reports that 99.58 percent of test failures in its setting were flaky and argues that earlier effectiveness claims were substantially inflated by this phenomenon.[cite:23] If that kind of label contamination appears in other large CI ecosystems, then any history-based prioritization method may be learning from a mixture of true regression signal and infrastructure or nondeterministic noise.[cite:23]

This matters because the source paper treats failing tests largely as meaningful training and evaluation signals.[file:18][cite:2] Once flaky behavior is introduced, the meaning of both effectiveness and transfer changes: a model may appear strong not because it predicts regressions well, but because it exploits recurring noise patterns.[cite:23] That is a far harsher critique than simply saying flaky tests are a missing future-work item.[cite:23]

For Android or mobile CI, this issue becomes even more dangerous.[file:18][cite:23] Emulator instability, asynchronous timing behavior, hardware heterogeneity, UI synchronization problems, and environment-dependent failures all increase the chance that historical outcomes are dirtier than the benchmark assumes.[cite:23] A paper that brings flaky-test-aware TCP into Android CI would therefore not just be extending the benchmark, but attacking one of its deepest hidden assumptions.[file:18][cite:23]

## Transfer is both the strongest clue and the most fragile claim

Pretrained MART is one of the most important findings in the source paper, because it suggests that cross-subject data is not a side benefit but a major path to materially better TCP performance.[cite:2] The reported result that pretrained MART achieves optimal sequences on 80 percent of subjects, versus 50 percent for original MART, is exactly the kind of number that can motivate a next paper.[cite:2] But that result is still under-interpreted if it is treated as straightforward evidence that more shared data simply solves the problem.[cite:2]

Transfer gains can arise from reusable signal, but also from benchmark affinity, hidden similarity between source and target projects, or representation choices that favor some projects over others.[file:18][cite:2] A more brutal reading says that the source paper established transfer promise without fully measuring transfer hardness.[file:18][cite:2] In other words, it showed that pretraining helps under available source-target relationships, but it did not map when transfer breaks, degrades, or becomes misleading.[cite:2]

This is exactly why federated pretraining is more than a fashionable systems add-on.[file:18][cite:2] The source paper creates the motivation for shared learning, while real organizations create the constraint that raw CI histories may be siloed, sensitive, or legally unshareable.[file:18][cite:2] A federated baseline would therefore not just modernize the design, but test whether the paper's strongest practical clue survives under realistic governance constraints.[file:18][cite:2]

## LLMs change the target, not just the toolset

The updated window is right to list LLM-augmented representations as an extension track.[file:18] The deeper point is that LLM features may destabilize the paper's entire winner landscape, because many benchmarked methods are being compared under older feature assumptions rather than richer semantic representations of code, tests, changes, and execution context.[file:18][cite:31] Newer work is explicitly exploring LLM-enhanced test case prioritization for complex systems, which means future comparisons may be less about whether RL beats SL and more about how representation quality changes separability and transferability.[cite:31]

That creates an opportunity and a risk.[cite:31] The opportunity is obvious: semantic embeddings may capture relations between tests and code changes that classic handcrafted features miss.[cite:31] The risk is that a paper that simply bolts LLMs onto the old benchmark without rethinking confounders could look like feature inflation rather than scientific progress.[cite:31][cite:2]

A stronger framing is to argue that richer representations reopen old comparative conclusions.[file:18][cite:31] If MART or ACER-PA wins mainly under a given feature pipeline, then the introduction of LLM-derived semantic signals could change which methods are robust, which methods transfer, and which methods justify their overhead.[file:18][cite:31][cite:2] That is a more ambitious and more defendable claim than saying LLMs merely improve accuracy.[cite:31]

## Metric critique after the second loop

The source paper's critique of APFD, NAPFD, and NRPA may still be right, but the proposed remedy should be described more carefully than the source paper does.[cite:2] rAPFD appears valuable as a comparability repair inside CI-style evaluation, especially when failure counts vary across cycles.[cite:2] But the stronger reviewer question is no longer merely whether rAPFD fixes fairness and discernment; it is whether rAPFD remains meaningful when failure labels are noisy, failures are dependent, or downstream developer value is the real objective.[file:18][cite:2][cite:23]

That distinction matters because a metric can be scientifically cleaner while still being operationally incomplete.[cite:2] If a new paper introduces flaky-test-aware evaluation or developer-centered outcomes, then rAPFD should be positioned as a useful benchmark repair rather than the final metric answer for CI TCP.[cite:2][cite:23] This lets a follow-on paper acknowledge the source contribution while still opening room for a stronger evaluation frame.[cite:2]

## The hardest reviewer attacks to prepare for

A serious software-engineering reviewer could attack the source paper and any follow-on paper through the following lines.

- The failure-rate split may be descriptive rather than explanatory unless hyperparameters, feature pipelines, and subject composition are stress-tested more thoroughly.[file:18][cite:2]
- The pretraining result may be real but benchmark-dependent unless source-target dissimilarity is explicitly manipulated.[file:18][cite:2]
- Practical applicability may be implementation-dependent unless compute assumptions, scheduling policy, and hardware are varied.[file:18][cite:2]
- Historical TCP claims may collapse in noisy CI ecosystems if flaky failures dominate observed labels.[cite:23]
- LLM-based extensions may improve representation quality while worsening reproducibility, cost, or interpretability if not benchmarked with comparable rigor.[cite:31]

A strong future paper should preempt these attacks by design rather than by rhetoric.[cite:2][cite:23][cite:31]

## Best positioning for your own paper

The most credible next-paper move is not to say the source paper was wrong.[cite:2] The better claim is that it identified the right structural axes—failure prevalence, transfer, and runtime overhead—but evaluated them under assumptions that are too clean for modern CI.[file:18][cite:2] That framing preserves the source paper's value while making room for a more realism-oriented contribution.[file:18][cite:2]

The strongest positioning options now look like this.

| Direction | Strongest claim | Why it can beat the source paper |
|---|---|---|
| Flaky-test-aware TCP | Historical TCP effectiveness is overstated when failures are noisy.[cite:23] | It attacks the label-quality assumption under the benchmark's learning and evaluation logic.[cite:23][cite:2] |
| Federated pretraining | Transfer remains valuable even when projects cannot share raw CI histories.[file:18][cite:2] | It preserves the source paper's best clue while adding a realistic organizational constraint.[file:18][cite:2] |
| LLM-augmented TCP | Semantic representations can reopen the winner landscape, not just boost scores.[cite:31] | It challenges whether old method rankings remain meaningful once feature quality changes.[cite:31][cite:2] |
| Android/mobile CI replication | Benchmark conclusions weaken when CI labels, runtimes, and scheduling differ materially from open-source desktop/server projects.[file:18][cite:23] | It attacks external validity directly and brings the study closer to modern applied settings.[file:18][cite:23] |

Among these, the highest-yield combination is flaky-test-aware federated pretraining with semantic representations evaluated in Android or mobile CI.[file:18][cite:23][cite:31] That is aggressive, but it is also coherent: it targets label realism, data-sharing realism, and feature realism at the same time.[file:18][cite:23][cite:31]

## Concrete rewrite instructions for the next draft

Use the following edits in your working paper.

1. Rewrite every major source-paper claim into the format: claim, evidence, confounders, why the confounders matter, and what a stronger benchmark would need to rule them out.[file:18][cite:2]
2. Stop treating flaky tests as an optional extension section; move them into the main threats-to-validity or motivation section because they can directly contaminate historical labels.[cite:23]
3. Reframe pretraining as a constrained systems question, not just an empirical boost, by foregrounding cross-project governance and privacy barriers.[file:18][cite:2]
4. Treat LLMs as a representation-shift argument, not just an accuracy-improvement argument.[cite:31]
5. Downgrade any language suggesting deployment prescriptions from the source benchmark unless those prescriptions survive noisy labels, heterogeneous CI conditions, and modern feature pipelines.[file:18][cite:2][cite:23]

## Blunt final assessment

The updated window is now good enough to support serious argumentation, but the next strong move is to turn it from a critical summary into a claim-by-claim demolition map.[file:18] The source paper remains valuable because it gives a rare unified benchmark and a strong transfer-learning clue.[cite:2] It remains vulnerable because its clean historical assumptions, open-source scope, and feature-era limitations make its practical recommendations easier to overread than the authors fully acknowledge.[file:18][cite:2][cite:23][cite:31]

That combination is exactly what you want in a base paper.[cite:2] It is credible enough to build on, but incomplete enough to beat.[cite:2][cite:23][cite:31]
