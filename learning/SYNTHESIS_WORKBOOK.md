# Synthesis Workbook: Learn Both Papers Together

This is the capstone document. Use it after the foundations and both guides.

## Pass 1 - Simple Essence

### One-sentence core

The original paper tells us what wins under benchmark conditions, while our paper tells us when those benchmark wins remain trustworthy in the real world.

### The 5 biggest contrasts

1. Original paper: benchmark comparison. Our paper: realism qualification.
2. Original paper: who performs best. Our paper: when the recommendation survives.
3. Original paper: unified ML-TCP benchmark. Our paper: conditional-validity map.
4. Original paper: pretraining is powerful. Our paper: can that power survive governance limits?
5. Original paper: method ranking under a feature pipeline. Our paper: does the ranking survive representation shift and label noise?

## Pass 2 - System Map

### Compare the two papers side by side

| Question | Original paper | Our paper |
|---|---|---|
| Main goal | Compare ML-based TCP methods fairly in CI | Test whether those recommendations survive realism constraints |
| Main output | Benchmark conclusions and practical recommendations | Conditional-validity map |
| Core regime story | ACER-PA for more-failure, MART for less-failure | Check whether that story weakens under flaky labels, governance limits, representation shift, and harder environments |
| Strongest practical result | Pretrained MART improves strongly | Some benchmark conclusions may be benchmark-valid but deployment-conditional |
| Evidence status | Original benchmark results | Mixed: some executed results, some frameworks, some staged directions |

### One mental model to keep

Think of the relationship like this:

- The original paper answers: “What works best in the benchmark?”
- Our paper answers: “How much of that answer can you safely carry into deployment?”

### What you should now be able to separate

#### Benchmark validity

The result is correct for the tested setup.

#### Deployment validity

The result is still reliable once messy real constraints are present.

That distinction is the heart of our paper.

### Edge cases and student traps

1. Saying the new paper “proves the old paper wrong.” That is too crude.
2. Forgetting the old paper still provides the baseline and many useful insights.
3. Forgetting that our paper itself contains both executed results and staged research directions.
4. Turning “conditional” into “uncertain about everything.” That is also wrong.
5. Ignoring the difference between a benchmark claim and a deployment recommendation.

## Pass 3 - Transfer And Testing

### 5 recall questions

1. What is the difference between benchmark validity and deployment validity?
2. Why does our paper still depend on the original paper instead of replacing it outright?
3. What is the single most important take-away from the original paper?
4. What is the single most important take-away from our paper?
5. Which realism gap would you investigate first in a CI system full of intermittent failures?

### Final application tasks

#### Task 1: 60-second teach-back

Explain both papers in under 60 seconds using this structure:

- problem
- original answer
- why that answer may not be enough
- what our paper adds

#### Task 2: One-page decision memo

Write a memo for a hypothetical engineering manager answering:

“Can we trust the original benchmark's recommendation for our CI system?”

Your memo must mention:

- failure rate
- flaky labels
- pretraining or governance
- representation choice
- overhead

#### Task 3: Honest evidence labeling

Sort each of these into one bucket: verified, executed proxy, protocol/framework, or staged.

- original benchmark recommendation
- pretrained MART result
- Direction C BPE proxy finding
- federated pretraining framework
- Android extension

### Self-check rubric

You understand the material well if you can do all of these:

- state the original regime story correctly
- explain why pretraining matters
- explain why flaky labels can distort conclusions
- explain why semantic representation changes are not automatically improvements
- explain why our paper is about qualification, not casual contradiction

### Compressed master note

1. TCP in CI is about finding useful failures earlier.
2. The original paper is a unified ML-based benchmark.
3. It recommends ACER-PA for more-failure subjects and MART for less-failure subjects.
4. MART is the strongest practical overall recommendation.
5. Pretrained MART is one of the paper's highest-leverage results.
6. Our paper asks whether those results survive realism.
7. The four realism gaps are labels, governance, representation, and external validity.
8. The new paper's goal is a conditional-validity map.
9. It keeps the original benchmark as the baseline rather than discarding it.
10. Direction C currently provides the clearest executed new evidence in the manuscript.
11. A negative proxy result is still useful evidence.
12. The mature lesson is not “which paper wins,” but “which recommendation survives under which conditions.”

### Final review plan

- Day 1: Teach back both papers in 60 seconds.
- Day 3: Recreate the compare table from memory.
- Day 7: Write the one-page decision memo.
- Day 14: Redo the evidence-labeling task.
- Day 30: Write a full-page summary of both papers and then compare it against this workbook.