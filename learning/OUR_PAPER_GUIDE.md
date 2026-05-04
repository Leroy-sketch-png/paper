# Our Paper Guide: Why We Revisited The Benchmark

Source anchor in this workspace:

- `manuscript/paper_skeleton.md`
- `EXECUTION_SUMMARY.md`

## Pass 1 - Simple Essence

### One-sentence core

Our paper asks when the original benchmark's recommendations remain trustworthy once realistic constraints such as flaky labels, data-sharing limits, representation shift, and harder deployment environments are taken seriously.

### Top 5 core ideas in plain language

1. Our paper does not say the original benchmark is useless.
2. It says benchmark-valid results may still be deployment-conditional.
3. We organize that challenge into four realism gaps: labels, governance, representation, and external validity.
4. We require a six-tier comparison grid so claims are judged against a wide baseline set.
5. Our goal is a conditional-validity map: when does the original advice hold, weaken, or invert?

### The four realism gaps

#### A. Label realism

Are observed failures real regressions, or are some of them flaky noise?

#### B. Governance realism

Can organizations really pool raw CI data for pretraining, or do privacy and policy block that?

#### C. Representation realism

Do method rankings change when we move from handcrafted CI features to semantic code embeddings?

#### D. External-validity realism

Do results from benchmark-friendly Java and C projects still hold in noisier settings such as long-running suites or mobile CI?

## Pass 2 - System Map

### The structure of our paper

#### A. Keep the baseline, then stress it

- We preserve the benchmark as the starting point.
- We do not throw away the original problem setup.
- We ask whether its recommendations survive real constraints.

#### B. Four directions

- Direction A: flaky-test-aware TCP.
- Direction B: federated pretraining.
- Direction C: LLM-augmented representations.
- Direction D: Android or mobile CI extension.

#### C. Six-tier baseline grid

- Heuristics.
- FAST similarity methods.
- FALCON semantic baseline.
- DeepOrder.
- Source-paper ML/RL methods.
- New constrained variants.

#### D. The central output

The paper's main output is not “here is one new winner.”

It is:

“Here is when the older recommendation is still safe, and here is when you need a caveat or a replacement.”

### What is executed versus staged

This matters a lot in this repo.

- Direction C has executed manuscript-integrated findings through a proxy embedding path.
- Direction A is a protocol plus feasibility analysis, not a full real-data rerun.
- Direction B is a framework and protocol, not a completed federated retraining result.
- Direction D is staged and conditional on dataset availability.

### The most concrete executed finding right now

The strongest executed new result in the manuscript is from Direction C:

- a vocabulary-anchored BPE proxy embedding path was tested on 5 SIR subjects
- it underperformed FAST-pw
- mean delta APFD was negative
- the ranking correlation with FAST-pw orderings was very low

This is important because it shows:

- not every “LLM-flavored” representation is automatically better
- richer representation claims need careful validation
- a negative result can still be highly informative

### Common mistakes and edge cases

1. Thinking our paper completely refutes the original paper.
2. Thinking all four directions were executed equally. They were not.
3. Thinking a weak BPE proxy result means semantic methods in general are useless. It does not.
4. Confusing a paper-level FALCON claim with artifact-level aggregation details.
5. Forgetting that our paper is about recommendation reliability, not only leaderboard replacement.

### The easiest way to remember our paper

Use this sentence:

“The original benchmark may be right inside the benchmark, but our paper checks whether it is still right under realism constraints.”

## Pass 3 - Transfer And Testing

### 5 recall questions

1. What is a conditional-validity map?
2. What are the four realism gaps?
3. Why does our paper keep the original benchmark instead of discarding it?
4. Which direction currently has the clearest executed manuscript result?
5. Why is a negative Direction C result still valuable?

### One concrete application task

Imagine you are advising a company with these properties:

- they have strict data-governance rules
- they suspect flaky tests are common
- they are curious about LLM embeddings
- they cannot wait for an Android-specific dataset

Write a short memo saying which parts of the original benchmark you would trust immediately, which parts you would qualify, and which new experiments from our paper matter most first.

### Compressed study note

1. Our paper revisits the benchmark under realism constraints.
2. It does not discard the original benchmark.
3. Its goal is conditional validity, not blind contradiction.
4. The four realism gaps are flaky labels, governance, representation, and external validity.
5. The paper requires a six-tier baseline grid.
6. Direction A asks whether flaky labels distort recommendations.
7. Direction B asks whether pretraining survives under federation.
8. Direction C asks whether rankings survive representation shift.
9. Direction D asks whether harder deployment settings break the benchmark story.
10. Current executed evidence is strongest for Direction C, and it is a useful negative proxy result.

### Spaced review plan

- Day 1: List the four realism gaps from memory.
- Day 3: Explain what “deployment-conditional” means.
- Day 7: Reconstruct the six-tier baseline grid.
- Day 14: Re-do the recommendation memo from memory.
- Day 30: Explain the paper in one minute to a non-expert.