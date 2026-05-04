# Foundations: What You Need Before Either Paper Makes Sense

## Pass 1 - Simple Essence

### One-sentence core

Test case prioritization in continuous integration means ordering tests so the most useful failures are found as early as possible after each code change.

### Top 5 ideas in plain language

1. Continuous integration, or CI, means developers keep pushing code and the system keeps re-running tests.
2. Regression testing means checking whether new code broke something that used to work.
3. A test suite can be expensive, so the order of tests matters when time is limited.
4. Test case prioritization, or TCP, does not remove tests; it changes their order.
5. A method is only useful in CI if it helps enough and is fast enough to be worth running.

### Tiny glossary

- Commit: a recorded code change.
- CI cycle: one run of the pipeline after a change.
- Test suite: the collection of tests.
- Failure: a test reports something went wrong.
- Fault: the underlying bug or defect.
- TCP: deciding the order of tests.
- Heuristic: a simple rule.
- ML-based TCP: a model learns from previous CI history.
- RL-based TCP: a model learns by reward and repeated interaction.
- Flaky test: a test that sometimes fails without a real code regression.

## Pass 2 - System Map

### The basic pipeline

1. A developer pushes a commit.
2. CI decides which tests to run.
3. A prioritization method orders those tests.
4. Tests run in that order.
5. Developers care how quickly the first useful failure is revealed.

### The main idea families

#### A. Simple heuristics

- Example idea: run tests that failed recently first.
- Strength: simple, cheap, understandable.
- Weakness: may miss deeper patterns.

#### B. Similarity-based methods

- Example idea: choose tests that cover diverse parts of the code.
- Strength: no heavy learning step.
- Weakness: may miss failure-history signal.

#### C. ML and RL methods

- Example idea: learn from old CI data which tests are likely to fail.
- Strength: can exploit patterns humans would not manually encode.
- Weakness: can be expensive, brittle, and sensitive to bad labels.

#### D. Semantic methods

- Example idea: use code embeddings to understand test content more deeply.
- Strength: richer representation.
- Weakness: can add complexity, model cost, and new failure modes.

### The three most important metrics in this workspace

- APFD: how quickly faults are found on average.
- rAPFD: a rectified version used by the original paper for fairer CI comparison.
- Overhead: how much time the prioritization method itself costs.

### What makes TCP hard

- Failures are rare in many projects.
- Some failures are flaky rather than real regressions.
- The best method may change from one project type to another.
- A highly accurate method can still be useless if it is too slow.

### Common mistakes and edge cases

1. Confusing prioritization with test selection or test reduction.
2. Thinking “best average score” means “best for every project.”
3. Forgetting that a failing test may be flaky rather than meaningful.
4. Ignoring method runtime and only looking at ranking quality.
5. Assuming all CI projects have the same failure patterns.

## Pass 3 - Transfer And Testing

### 5 recall questions

1. What problem is TCP trying to solve inside a CI pipeline?
2. Why is changing test order different from removing tests?
3. Why can a model with good ranking quality still be a bad CI choice?
4. What is a flaky test, and why does it matter for ML-based TCP?
5. Why might one method work well on one project but poorly on another?

### One concrete application task

Imagine a project has 5 tests. Two tests often fail early when bugs are real, one test is flaky, and two tests almost never fail.

Write a short answer to this question:

Which tests would you want near the front of the run, and what extra information would you need before trusting that order?

### Compressed study note

1. CI reruns tests after code changes.
2. Regression testing checks whether new code broke old behavior.
3. TCP changes test order, not the membership of the suite.
4. The goal is earlier discovery of useful failures.
5. Methods include heuristics, similarity-based, ML/RL, and semantic approaches.
6. APFD and rAPFD measure how early faults are found.
7. Overhead matters because CI is time-sensitive.
8. Failure rate and label quality change which method works best.
9. Flaky tests can poison the learning signal.
10. Practical TCP is always a balance between effectiveness and cost.

### Spaced review plan

- Day 1: Define TCP, CI, APFD, and flaky test from memory.
- Day 3: Redraw the four method families.
- Day 7: Explain the whole pipeline in 60 seconds.
- Day 14: Re-do the application task with no notes.
- Day 30: Teach the topic to a classmate or imaginary student.