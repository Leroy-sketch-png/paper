# Flashcard Deck

Use this deck with the exact format from the Universal Learning OS:

- Question
- Reasoning
- Answer

Do not just read the answers. Cover them and answer first.

## Foundations

### Card 1

Question:

What is continuous integration?

Reasoning:

Think about repeated code changes, repeated automated checks, and the need for fast feedback.

Answer:

Continuous integration is the practice of repeatedly integrating code changes and automatically rerunning checks so developers quickly learn whether the new code broke something.

### Card 2

Question:

What is regression testing?

Reasoning:

Focus on old behavior breaking after new changes.

Answer:

Regression testing checks whether newly changed code caused previously working behavior to fail.

### Card 3

Question:

What is test case prioritization?

Reasoning:

Separate changing order from changing suite membership.

Answer:

Test case prioritization means reordering tests so useful failures are revealed earlier, without removing tests from the suite.

### Card 4

Question:

Why does test order matter in CI?

Reasoning:

Think about limited time and fast developer decisions.

Answer:

Test order matters because CI is time-sensitive, so earlier useful failures give developers faster and better feedback than the same failures found later.

### Card 5

Question:

What is a flaky test?

Reasoning:

Think about a test changing outcome without a true regression.

Answer:

A flaky test is a test that sometimes passes and sometimes fails under the same code state, so its failure does not reliably indicate a real defect.

### Card 6

Question:

Why can a good TCP method still be a bad CI choice?

Reasoning:

Include runtime cost, not only ranking quality.

Answer:

A TCP method can be a bad CI choice if its own training or prediction overhead is so high that it erases the benefit of better ordering.

## Metrics And Method Families

### Card 7

Question:

What is the intuition behind APFD?

Reasoning:

Think “how early are faults found on average?”

Answer:

APFD measures how quickly faults are revealed in an ordered test run, rewarding methods that surface faults earlier.

### Card 8

Question:

Why does the original paper use rAPFD?

Reasoning:

Think fairness in CI comparison.

Answer:

The original paper uses rAPFD because it argues older metrics can distort cross-cycle CI comparisons, and rAPFD is meant to be fairer for that setting.

### Card 9

Question:

What is FAST in this workspace?

Reasoning:

Think non-ML similarity baseline.

Answer:

FAST is a similarity-based, non-ML TCP baseline that prioritizes by diversity rather than by training a learned model.

### Card 10

Question:

What is one strength of heuristics compared with ML-based TCP?

Reasoning:

Think simplicity and cost.

Answer:

Heuristics are usually simpler, cheaper to run, and easier to understand than ML-based TCP methods.

### Card 11

Question:

What is one risk of ML-based TCP compared with simpler baselines?

Reasoning:

Think cost, brittleness, and label quality.

Answer:

ML-based TCP can be more expensive and more sensitive to poor labels or shifting conditions than simpler baselines.

### Card 12

Question:

Why are semantic methods interesting?

Reasoning:

Think richer code representation.

Answer:

Semantic methods are interesting because they can use code embeddings to capture deeper structural or semantic signal than simpler handcrafted features.

## Original Paper Setup

### Card 13

Question:

How many projects did the original paper study?

Reasoning:

This is one of the anchor numbers.

Answer:

The original paper studied 11 projects.

### Card 14

Question:

How many ML-based TCP techniques did the original paper compare?

Reasoning:

Match this with the number of studied projects.

Answer:

It compared 11 ML-based TCP techniques.

### Card 15

Question:

How many commits per project were used in the original paper?

Reasoning:

This is another anchor number.

Answer:

The original paper used 800 commits per project.

### Card 16

Question:

Why is a unified benchmark setup important?

Reasoning:

Think fair cross-method comparison.

Answer:

A unified setup matters because it compares methods under the same data, metrics, and evaluation logic, making the differences between methods more meaningful.

## Original Paper Findings

### Card 17

Question:

What is the original paper's regime story for more-failure subjects?

Reasoning:

This is the high-risk reversal card.

Answer:

On more-failure subjects, ACER-PA is the best recommendation.

### Card 18

Question:

What is the original paper's regime story for less-failure subjects?

Reasoning:

Pair this with the previous card carefully.

Answer:

On less-failure subjects, MART is the best recommendation.

### Card 19

Question:

What is the strongest practical overall recommendation in the original paper?

Reasoning:

Separate practical default from regime-specific winner.

Answer:

MART is the strongest practical overall recommendation in the original paper.

### Card 20

Question:

Why does data imbalance matter in the original paper?

Reasoning:

Connect failure rate, scarce failures, and method behavior.

Answer:

Data imbalance matters because different methods respond differently when failures are common versus rare, which helps explain the regime split between ACER-PA and MART.

### Card 21

Question:

What does the original paper say about RL methods and cost?

Reasoning:

Think strong but often expensive.

Answer:

The original paper finds that RL-based methods can be effective but are generally much more expensive to train, and some can even become impractical in CI.

## Pretraining

### Card 22

Question:

Why is pretrained MART a high-leverage result?

Reasoning:

Think cross-project training and strong practical gain.

Answer:

Pretrained MART is high leverage because it shows that cross-subject data can dramatically improve a strong practical method before much local project history is available.

### Card 23

Question:

What percentage of subjects does original MART produce the optimal sequence on?

Reasoning:

This is the lower of the two pretraining anchor numbers.

Answer:

Original MART produces the optimal sequence on 50% of subjects.

### Card 24

Question:

What percentage of subjects does pretrained MART produce the optimal sequence on?

Reasoning:

This is the higher pretraining anchor number.

Answer:

Pretrained MART produces the optimal sequence on 80% of subjects.

### Card 25

Question:

What hidden assumption sits under centralized pretraining?

Reasoning:

Think raw data sharing.

Answer:

Centralized pretraining assumes raw CI histories from multiple projects can be pooled together.

## Our Paper

### Card 26

Question:

What is our paper trying to add to the original benchmark?

Reasoning:

Think qualification under realism.

Answer:

Our paper adds a realism-based qualification layer that asks when the original benchmark's recommendations remain trustworthy in deployment.

### Card 27

Question:

What is a conditional-validity map?

Reasoning:

Think “when does the recommendation hold, weaken, or invert?”

Answer:

A conditional-validity map shows the conditions under which a benchmark recommendation remains reliable, weakens, or reverses.

### Card 28

Question:

What are the four realism gaps?

Reasoning:

You must recall the exact set.

Answer:

The four realism gaps are label realism, governance realism, representation realism, and external validity.

### Card 29

Question:

Why is our paper not simply a rejection of the original paper?

Reasoning:

Think benchmark-valid versus deployment-conditional.

Answer:

Our paper is not a rejection because it accepts that the benchmark can be valid inside its own setup and instead asks whether those recommendations survive realistic deployment constraints.

### Card 30

Question:

What is the paper's six-tier baseline idea trying to prevent?

Reasoning:

Think narrow or flattering comparisons.

Answer:

The six-tier baseline grid prevents claims that look strong only because they were compared against too few or too weak baselines.

## Directions A-D

### Card 31

Question:

What does Direction A study?

Reasoning:

Think label noise and flaky tests.

Answer:

Direction A studies how flaky-test contamination may distort TCP effectiveness results and recommendations.

### Card 32

Question:

What does Direction B study?

Reasoning:

Think federation and pretraining.

Answer:

Direction B studies whether federated pretraining can preserve the benefit of centralized pretraining without sharing raw CI logs.

### Card 33

Question:

What does Direction C study?

Reasoning:

Think representation shift.

Answer:

Direction C studies whether method rankings change when handcrafted features are replaced with LLM-derived code representations.

### Card 34

Question:

What does Direction D study?

Reasoning:

Think harder deployment environments.

Answer:

Direction D studies whether the benchmark's conclusions survive in harder settings such as Android or mobile CI.

## Evidence Discipline

### Card 35

Question:

Which direction currently has the clearest executed manuscript result?

Reasoning:

Think current repo state, not the full research ambition.

Answer:

Direction C has the clearest executed manuscript result in the current repo.

### Card 36

Question:

What is the Direction C proxy result at a high level?

Reasoning:

Think BPE proxy, not full contextual UniXcoder.

Answer:

The Direction C proxy result shows that the vocabulary-anchored BPE-style representation path underperformed FAST-pw on the tested SIR subjects.

### Card 37

Question:

Why does that negative proxy result still matter?

Reasoning:

Think lower bound, not final refutation.

Answer:

It still matters because it shows that not every semantic-looking representation helps, which sharpens the difference between weak proxies and stronger contextual embedding approaches.

### Card 38

Question:

Why must you separate executed findings from framework or staged work in this repo?

Reasoning:

Think research integrity and honest evidence labeling.

Answer:

You must separate them because the repo contains both verified findings and planned or staged work, and confusing those levels would misstate the evidence.

## Synthesis

### Card 39

Question:

What is the cleanest one-sentence relationship between the two papers?

Reasoning:

Compress benchmark answer plus realism qualification.

Answer:

The original paper tells us what wins under benchmark conditions, and our paper tests when those wins remain trustworthy under realism constraints.

### Card 40

Question:

What is the mature lesson a student should leave with?

Reasoning:

Think beyond “which paper wins?”

Answer:

The mature lesson is not to ask which paper wins, but to ask which recommendation holds under which conditions.

## Deck Usage Rule

Use this cadence:

- Day 1: Cards 1-10
- Day 3: Cards 11-20
- Day 7: Cards 21-30
- Day 14: Cards 31-40
- Day 30: Full-deck recall without notes