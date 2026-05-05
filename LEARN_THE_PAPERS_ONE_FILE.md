# Learn The Papers: One-File Master Manual

This is the single-file version of the learning system.

It exists for one reason: if you dislike juggling multiple files, you should be able to learn the original paper and our paper from one place without losing the structure, recall, application, or spaced-review logic.

This manual combines the logic of the entire `learning/` folder into one study surface.

## Start Here

If you want the shortest usable path through this manual, do only these four things first:

1. Read `1. Foundations`.
2. Read `2. Original Paper Guide`.
3. Read `3. Our Paper Guide`.
4. Jump to `4. Synthesis Workbook` and do the 60-second teach-back.

If that works, come back for the flashcards, oral exam, intensive loops, and 30-day plan.

---

## What This File Covers

This one file gives you:

- the foundations you need before either paper makes sense
- the original paper explained simply and accurately
- our paper explained simply and accurately
- a comparison framework for both papers together
- note templates and self-tracking tools
- an intensive 12-loop curriculum
- an oral exam mode
- a flashcard deck
- a 30-day execution plan

---

## The Only Rule That Matters

If you understand enough to predict outcomes, and you have tested yourself, you must apply the idea within 24 hours. Further refinement comes after use.

---

## How To Use This Manual

If you want the simplest path, use this order:

1. Foundations
2. Original paper guide
3. Our paper guide
4. Synthesis
5. Flashcards or oral exam
6. 30-day plan

If you want the extreme path, do this:

1. Foundations
2. Original paper guide
3. Our paper guide
4. Intensive 12 loops
5. Oral exam mode
6. Flashcard deck
7. 30-day execution plan

---

## Hard Constraints From The Learning OS

- Three-pass cutoff: no endless rereading. After three passes, produce output.
- One note format: topic -> principles -> mistakes -> application.
- One flashcard format: question -> reasoning -> answer.
- One review cadence: 1, 3, 7, 14, 30 days.
- Completion before perfection: if you can explain, predict, or apply it, ship the understanding and move on.

---

## Navigation Map

1. Foundations
2. Original Paper Guide
3. Our Paper Guide
4. Synthesis Workbook
5. Student Tracker Templates
6. Intensive 12-Loop Curriculum
7. Intensive Loop Tracker
8. Oral Exam Mode
9. Flashcard Deck
10. 30-Day Execution Plan

---

# 1. Foundations

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

---

# 2. Original Paper Guide

Source anchors in this workspace:

- `references/2311.13413v1.notes.md`
- `references/2311.13413v1.md`

## Pass 1 - Simple Essence

### One-sentence core

The original paper compares 11 ML-based TCP techniques under one unified CI setup and argues that the best method depends on the failure regime, while pretrained MART becomes the strongest practical overall recommendation.

### Top 5 core ideas in plain language

1. The paper compares 11 ML-based TCP techniques across 11 projects and 800 commits per project.
2. It argues older evaluation habits can be misleading, so it uses rAPFD for fairer comparison.
3. There is no single winner for every condition.
4. On more-failure subjects, ACER-PA is the best-performing recommendation.
5. On less-failure subjects, MART is the best-performing recommendation, and pretrained MART is even stronger.

### Numbers worth remembering

- 11 projects.
- 11 ML-based TCP techniques.
- 800 commits per project.
- Pretrained MART reaches the optimal sequence on 80% of subjects.
- Original MART reaches the optimal sequence on 50% of subjects.
- MART saves more than 95% of time-to-first-failure in most subjects.

## Pass 2 - System Map

### What the paper is trying to answer

The paper asks four practical questions:

1. Which ML-based TCP techniques are most effective?
2. Which ones are efficient enough for CI?
3. Which ones are actually applicable in real CI time windows?
4. How should we interpret results when failure rates differ across projects?

### The paper's structure in one map

#### A. Setup

- Gather 11 open-source subjects.
- Collect 800 commits per subject.
- Recreate CI-like prioritization conditions.
- Compare supervised-learning and reinforcement-learning methods under one pipeline.

#### B. Evaluation lens

- Use rAPFD for fairness across CI cycles.
- Measure training time and prediction time too.
- Check not just “who wins,” but “who is usable.”

#### C. Main findings

- The best method changes with failure rate.
- Data imbalance matters a lot.
- RL methods are often more expensive.
- PPO1-LI can become impractical.
- MART is the strongest practical overall choice.
- Pretraining greatly improves MART.

#### D. Main recommendations

- Split thinking by failure regime.
- Use imbalance-aware ideas such as SMOTE-style handling when failures are rare.
- Use cross-subject pretraining when possible.
- Always check overhead, not only ranking score.

### The key regime story

This is the part students most easily reverse.

- More-failure subjects: ACER-PA is the best recommendation.
- Less-failure subjects: MART is the best recommendation.
- Overall practical recommendation: MART, especially when pretraining is available.

### Common mistakes and edge cases

1. Reversing the failure-regime recommendation.
2. Treating pretrained MART and original MART as if they are the same result.
3. Looking only at average performance and forgetting applicability.
4. Thinking DeepOrder being strong in one aggregate view means it replaces MART as the practical recommendation.
5. Forgetting that the paper's conclusions are tied to its feature pipeline and benchmark conditions.

### The easiest way to remember the paper

Use this sentence:

“ACER-PA is the high-failure specialist, MART is the low-failure practical default, and pretraining makes MART much stronger.”

## Pass 3 - Transfer And Testing

### 5 recall questions

1. Why does the original paper say there is no universal winner?
2. What is the recommendation for more-failure subjects?
3. What is the recommendation for less-failure subjects?
4. Why is pretrained MART such an important result?
5. Why does the paper care about training time and prediction time in addition to rAPFD?

### One concrete application task

You are advising a CI team with these properties:

- failures are rare
- the team cannot afford long model runtime
- they do have some cross-project historical data

Write a 6-8 sentence recommendation using the paper's logic. Name the method you would start from and explain why.

### Compressed study note

1. The original paper is a unified benchmark of 11 ML-based TCP methods.
2. It studies effectiveness, efficiency, and applicability together.
3. rAPFD is the paper's key fairness-oriented metric.
4. Failure-rate regime changes the best method.
5. ACER-PA is best on more-failure subjects.
6. MART is best on less-failure subjects.
7. MART is the strongest overall practical recommendation.
8. Pretrained MART improves optimal-sequence performance from 50% to 80% of subjects.
9. RL methods can be powerful but expensive.
10. Practical TCP advice must consider overhead, not just ranking quality.

### Spaced review plan

- Day 1: Recite the regime story correctly.
- Day 3: Rebuild the setup: 11 projects, 11 techniques, 800 commits.
- Day 7: Explain pretrained MART in 90 seconds.
- Day 14: Redo the recommendation task from memory.
- Day 30: Compare MART, ACER-PA, and PPO1-LI without notes.

---

# 3. Our Paper Guide

Source anchors in this workspace:

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

---

# 4. Synthesis Workbook

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

---

# 5. Student Tracker Templates

## Session Log

### Session 1

Topic:

What I understood clearly:

What still feels confusing:

Three key terms I can now define from memory:

One thing I can already explain out loud:

### Session 2

Topic:

What I understood clearly:

What still feels confusing:

Three key terms I can now define from memory:

One thing I can already explain out loud:

### Session 3

Topic:

What I understood clearly:

What still feels confusing:

Three key terms I can now define from memory:

One thing I can already explain out loud:

### Session 4

Topic:

What I understood clearly:

What still feels confusing:

Three key terms I can now define from memory:

One thing I can already explain out loud:

### Session 5

Topic:

What I understood clearly:

What still feels confusing:

Three key terms I can now define from memory:

One thing I can already explain out loud:

## One Note Format

```markdown
Topic:

Core:

Rules / principles:

Structure / map:

Mistakes / edge cases:

Recall from memory:

One concrete application:
```

## Flashcard Format

```markdown
Question:

Reasoning:

Answer:
```

## Review Tracker

### Day 1

- [ ] Re-answer the recall questions.
- [ ] Explain the topic in 60 seconds.

### Day 3

- [ ] Rebuild the system map from memory.
- [ ] Correct one misunderstanding.

### Day 7

- [ ] Teach the topic without notes.
- [ ] Re-do one application task.

### Day 14

- [ ] Compare the original and newer paper in writing.
- [ ] Check whether I reversed any recommendation.

### Day 30

- [ ] Write a one-page summary from memory.
- [ ] Mark what I still cannot explain clearly.

## Final Self-Test

1. What is TCP in CI?
2. Why does test order matter?
3. What does the original paper recommend for more-failure subjects?
4. What does it recommend for less-failure subjects?
5. Why is pretrained MART important?
6. What is a conditional-validity map?
7. What are the four realism gaps?
8. Why does our paper qualify the benchmark instead of simply rejecting it?
9. What is the clearest executed result in our manuscript right now?
10. In one sentence, how do the two papers relate?

---

# 6. Intensive 12-Loop Curriculum

Use this section when you want the same learning engine applied again and again on smaller conceptual targets.

## Loop Rules

- Do one loop at a time.
- Do not skip recall.
- Do not skip application.
- Do not spend more than 45-60 minutes on one loop before producing output.
- After three passes on a loop, move to speech, writing, or problem-solving.

## The 12 Loops

### Loop 1: Continuous Integration

Core: Continuous integration is the practice of repeatedly integrating code changes and re-running automated checks after each change.

Rules:

- Code changes happen often.
- Each change creates uncertainty.
- Automated testing reduces that uncertainty.
- Fast feedback matters because developers need answers while the change is still fresh.

Map:

- Input: commit.
- Trigger: CI pipeline starts.
- Process: build, test, report.
- Output: pass, fail, or warning signal.

Mistakes and edge cases:

- Thinking CI is just “run all tests.”
- Ignoring time cost.
- A pipeline may pass while still being too slow to be useful.

Recall:

1. What problem does CI solve?
2. Why does speed matter in CI?
3. What is the difference between a commit and a CI cycle?
4. Why is repeated automation better than occasional manual checking?
5. What kind of uncertainty is CI trying to reduce?

Application:

Write a 5-sentence explanation of CI to a freshman who has only written local programs on their own laptop.

Review:

- Day 1: define CI from memory.
- Day 3: draw the CI pipeline.
- Day 7: explain why slow feedback weakens CI.

### Loop 2: Regression Testing

Core: Regression testing checks whether new code changes broke behavior that used to work.

Rules:

- Old behavior matters.
- New code can introduce unintended damage.
- Tests act as memory for the system.
- Regressions are costly because they often surprise developers late.

Map:

- Old system state.
- New code change.
- Re-run tests.
- Compare expected and actual behavior.

Mistakes and edge cases:

- Thinking every failure is a regression.
- Forgetting flaky tests.
- The test may be wrong, not the product code.

Recall:

1. What is a regression?
2. Why can a test fail without a real regression?
3. Why is regression testing central to CI?
4. What does a test suite remember for a team?
5. Why is regression testing never fully free?

Application:

Give one example of a code change that fixes one bug but accidentally creates a regression somewhere else.

Review:

- Day 1: define regression from memory.
- Day 3: explain one false-positive scenario.
- Day 7: explain why regressions matter in team development.

### Loop 3: Test Case Prioritization

Core: Test case prioritization means ordering tests so the most useful failures appear earlier.

Rules:

- Test order changes feedback timing.
- TCP does not remove tests; it reorders them.
- Earlier useful failures improve developer response.
- Good ordering is more valuable when time is limited.

Map:

- Full test suite exists.
- Method assigns a priority score or ranking.
- Tests run in that order.
- Team observes how quickly informative failures surface.

Mistakes and edge cases:

- Confusing prioritization with test reduction.
- Assuming any early failure is useful.
- A flaky test may be prioritized early and waste time.

Recall:

1. What does TCP change?
2. What does TCP not change?
3. Why can early failure discovery matter more than total test count?
4. Why might a bad priority order still eventually run all tests?
5. Why is TCP especially relevant in CI?

Application:

Imagine 10 tests and only time for 4 before a developer must decide whether to merge. Explain why order matters.

Review:

- Day 1: define TCP from memory.
- Day 3: compare TCP with test selection.
- Day 7: explain one realistic reason order matters more than raw suite size.

### Loop 4: Metrics And Overhead

Core: TCP metrics try to measure how quickly faults are found, while overhead measures whether the method is worth the cost of running.

Rules:

- A ranking method must help enough to justify its own runtime.
- Good science needs a fair metric.
- A metric can distort conclusions if it does not match the CI setting.
- Practicality matters as much as raw score.

Map:

- APFD: fault-detection speed idea.
- rAPFD: corrected fairness-oriented metric used in the original paper.
- Overhead: training time plus prediction time.
- Applicability: whether CI can actually tolerate that overhead.

Mistakes and edge cases:

- Ranking methods only by accuracy-like numbers.
- Ignoring prediction cost.
- The method may be good on paper but too slow in practice.

Recall:

1. Why does overhead matter in TCP?
2. What is the intuition behind APFD?
3. Why did the original paper care about rAPFD?
4. How can a method be effective but inapplicable?
5. Why is metric choice not a minor detail?

Application:

Describe a situation where Method A finds failures earlier than Method B, but Method A still should not be deployed.

Review:

- Day 1: explain APFD and overhead at a high level.
- Day 3: explain why metric choice can reverse conclusions.
- Day 7: produce one example of effective-but-inapplicable.

### Loop 5: The Method Families

Core: The workspace compares several families of TCP methods: heuristics, similarity methods, ML/RL methods, and semantic or embedding-based methods.

Rules:

- Simpler methods are cheaper and often more robust.
- Learned methods can exploit richer historical patterns.
- Semantic methods depend heavily on representation quality.
- No family wins automatically under every condition.

Map:

- Heuristics: simple rules.
- FAST: non-ML similarity/diversity baseline.
- ML and RL: data-driven ranking policies.
- FALCON-style semantic methods: code embeddings plus stronger selection logic.

Mistakes and edge cases:

- Assuming ML is always superior.
- Treating FAST as a trivial baseline.
- A strong representation can still fail if the downstream method is weak.

Recall:

1. What is the benefit of heuristics?
2. Why is FAST important in this repo?
3. What extra risks do ML and RL methods add?
4. Why are semantic methods exciting?
5. Why should you compare across families instead of only within one family?

Application:

Write a short ranking of the method families by expected complexity of deployment, from easiest to hardest, and explain your reasoning.

Review:

- Day 1: list the four families.
- Day 3: compare FAST and ML-based TCP.
- Day 7: explain why semantic methods are not automatically superior.

### Loop 6: The Original Paper Setup

Core: The original paper is a unified benchmark that compares 11 ML-based TCP techniques under one controlled CI-oriented setup.

Rules:

- Fair comparison needs one shared setup.
- Different techniques must be tested under the same evaluation logic.
- Subject-level differences matter.
- Practical recommendations should come from both effectiveness and applicability.

Map:

- 11 projects.
- 800 commits per project.
- 11 ML-based techniques.
- rAPFD, runtime, and applicability analysis.

Mistakes and edge cases:

- Remembering only the winners and forgetting the setup.
- Assuming one aggregate chart tells the whole story.
- A technique may look strongest in one aggregate view but not as the practical subject-level choice.

Recall:

1. How many projects were studied?
2. How many techniques were compared?
3. Why does a unified setup matter?
4. What kinds of outputs did the benchmark examine besides effectiveness?
5. Why is this paper stronger than a narrow one-method comparison?

Application:

Write a short paragraph explaining why benchmarking many methods under one setup is more persuasive than reading several isolated papers that each test only one method.

Review:

- Day 1: memorize 11 projects, 11 techniques, 800 commits.
- Day 3: explain why unified setup matters.
- Day 7: explain benchmark scope without notes.

### Loop 7: The Original Paper Findings

Core: The original paper's most important message is that the best ML-based TCP method depends on the failure-rate regime, while MART is the strongest practical overall choice.

Rules:

- Failure-rate regime changes the best method.
- Data imbalance is a major explanatory factor.
- Practicality matters, not only raw ranking quality.
- Pretraining can materially improve outcomes.

Map:

- More-failure subjects: ACER-PA best.
- Less-failure subjects: MART best.
- Overall practical default: MART.
- Pretrained MART: stronger than original MART.

Mistakes and edge cases:

- Reversing ACER-PA and MART.
- Collapsing “best in one regime” into “best everywhere.”
- A technique can dominate in one regime and collapse in another.

Recall:

1. Which method is best on more-failure subjects?
2. Which method is best on less-failure subjects?
3. Why is MART still the practical overall recommendation?
4. What role does data imbalance play?
5. Why must you not reverse the regime story?

Application:

Write the regime story as a one-line memory hook you can repeat without hesitation.

Review:

- Day 1: recite the regime story correctly.
- Day 3: explain why data imbalance matters.
- Day 7: explain the difference between local winner and practical default.

### Loop 8: Pretrained MART And Transfer

Core: One of the original paper's highest-leverage findings is that cross-subject pretraining makes MART much stronger.

Rules:

- More training data can improve ranking quality.
- Cross-subject signal can be valuable.
- Finetuning on the target project matters.
- Transfer learning changes what a new project can do before it has much local history.

Map:

- Original MART optimal sequence on 50% of subjects.
- Pretrained MART optimal sequence on 80% of subjects.
- Interpretation: better initialization from outside-project data.

Mistakes and edge cases:

- Treating pretraining as a minor detail.
- Assuming transfer is always free or always allowed.
- Transfer may help less when source and target differ too much.

Recall:

1. Why is pretrained MART such a big deal?
2. What are the 50% and 80% numbers about?
3. Why is transfer learning high leverage in CI?
4. What practical problem does pretraining solve for a new project?
5. What hidden assumption is built into centralized pretraining?

Application:

Write a short product pitch for why a CI team should care about pretrained MART.

Review:

- Day 1: memorize 50% and 80% correctly.
- Day 3: explain transfer in plain language.
- Day 7: explain one limit of cross-subject pretraining.

### Loop 9: Why Our Paper Exists

Core: Our paper exists because a benchmark recommendation can be valid inside the benchmark and still become fragile in deployment.

Rules:

- Benchmark validity is not identical to deployment validity.
- Real systems add noise, policy, and representation changes.
- Good follow-up research does not only ask “what wins?” but also “when is that advice trustworthy?”
- Qualification is intellectually stronger than blind acceptance or blind rejection.

Map:

- Keep the benchmark as baseline.
- Stress its assumptions.
- Identify robustness, fragility, and possible inversion.
- Produce a conditional-validity map.

Mistakes and edge cases:

- Saying our paper disproves the old paper.
- Saying the new paper is only a summary.
- A benchmark can still be very useful even if some conclusions are conditional.

Recall:

1. Why did we revisit the benchmark?
2. What does “deployment-conditional” mean?
3. What is a conditional-validity map?
4. Why is our paper not just a replacement leaderboard?
5. Why is qualification better than casual disagreement?

Application:

Write a 6-sentence explanation of why a benchmark result may need qualification before deployment.

Review:

- Day 1: define conditional validity.
- Day 3: contrast benchmark validity and deployment validity.
- Day 7: explain why our paper depends on the original one.

### Loop 10: The Four Realism Gaps

Core: The new paper organizes its challenge to the benchmark into four realism gaps: label realism, governance realism, representation realism, and external validity.

Rules:

- Labels can be noisy.
- Data sharing can be restricted.
- Representations can change what methods see.
- Harder deployment environments can weaken old conclusions.

Map:

- Direction A: flaky labels.
- Direction B: federated pretraining.
- Direction C: LLM representations.
- Direction D: Android or mobile CI extension.

Mistakes and edge cases:

- Memorizing the directions without understanding the realism problem.
- Assuming all four directions were executed equally.
- One realism gap may matter much more than another in a given deployment.

Recall:

1. What does label realism ask?
2. What does governance realism ask?
3. What does representation realism ask?
4. What does external validity ask?
5. Why are these four gaps enough to reshape how we read the benchmark?

Application:

For a company with strict privacy rules and lots of intermittent failures, say which two realism gaps matter first and why.

Review:

- Day 1: list the four gaps from memory.
- Day 3: pair each gap with its direction letter.
- Day 7: explain which gap worries you most in practice and why.

### Loop 11: Executed Evidence Versus Staged Work

Core: Not every part of the new paper is at the same evidence level, so learning it correctly means separating executed findings from protocols and staged extensions.

Rules:

- Verified findings are stronger than planned work.
- Protocols matter, but they are not the same as executed results.
- Honest status labeling protects research integrity.
- Students learn faster when they know what is proven versus what is proposed.

Map:

- Executed manuscript-integrated result: Direction C proxy representation finding.
- Protocol or framework: Direction A and Direction B.
- Staged extension: Direction D.
- Verified supporting baselines: FAST, heuristic summaries, FALCON artifact references.

Mistakes and edge cases:

- Speaking as if all directions were completed equally.
- Treating a proxy result as the final word on all LLM representations.
- A negative executed result can still be very valuable.

Recall:

1. Which direction currently has the clearest executed manuscript result?
2. Why is Direction B not the same kind of evidence as Direction C?
3. Why is Direction D explicitly staged?
4. Why is evidence labeling essential in this repo?
5. Why can a proxy negative result still matter scientifically?

Application:

Sort these into buckets: verified, executed proxy, protocol/framework, staged.

- pretrained MART result from the source paper
- Direction C BPE proxy result
- federated pretraining framework
- Android extension

Review:

- Day 1: name the executed direction.
- Day 3: re-sort the evidence buckets.
- Day 7: explain why honesty about status improves trust.

### Loop 12: Final Synthesis And Teach-Back

Core: The final lesson is that the original paper tells us what wins in the benchmark, and our paper tells us when that answer remains trustworthy outside the benchmark.

Rules:

- Do not collapse benchmark truth into deployment truth.
- Do not throw away a good benchmark because it has limits.
- Do not accept a recommendation without checking realism constraints.
- Mature understanding means keeping both papers in one mental model.

Map:

- Problem: CI needs useful failures early.
- Original answer: benchmark the ML-based TCP methods.
- Key result: regime-dependent recommendations plus pretrained MART.
- New challenge: realism can weaken those recommendations.
- New output: conditional-validity map.

Mistakes and edge cases:

- Asking “which paper wins?” instead of “what does each paper contribute?”
- Forgetting the role of evidence status.
- A deployment can still use the original recommendation if the realism gaps are small.

Recall:

1. In one sentence, what is the original paper about?
2. In one sentence, what is our paper about?
3. What is the regime story in the original paper?
4. What is the central organizing idea in our paper?
5. What should an engineer ask before trusting the benchmark recommendation?

Application:

1. Explain both papers in 60 seconds.
2. Write a one-page memo to an engineering manager about whether to trust the benchmark recommendation.
3. Teach the topic to a fictional freshman version of yourself using only plain language.

Review:

- Day 1: do the 60-second talk.
- Day 3: write the memo from memory.
- Day 7: teach both papers without notes.
- Day 14: revisit the loops you found hardest.
- Day 30: write a final summary and compare it with the docs.

## Master Compression

1. CI needs fast feedback.
2. TCP changes test order so useful failures appear earlier.
3. The original paper benchmarked 11 ML-based TCP methods on 11 subjects.
4. ACER-PA wins on more-failure subjects.
5. MART wins on less-failure subjects.
6. MART is the strongest practical overall recommendation.
7. Pretrained MART is one of the original paper's biggest results.
8. Our paper asks whether those recommendations survive realism.
9. The four realism gaps are labels, governance, representation, and external validity.
10. Our paper's output is a conditional-validity map.
11. Direction C has the clearest executed new result in the current manuscript.
12. The mature lesson is not “which paper is right,” but “which recommendation holds under which conditions.”

---

# 7. Intensive Loop Tracker

Use this with the 12-loop curriculum.

## Loop Progress Table

| Loop | Topic | Read | Recall done | Application done | Teach-back done | Day 1 | Day 3 | Day 7 | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Continuous Integration | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 2 | Regression Testing | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 3 | Test Case Prioritization | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 4 | Metrics And Overhead | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 5 | Method Families | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 6 | Original Paper Setup | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 7 | Original Paper Findings | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 8 | Pretrained MART And Transfer | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 9 | Why Our Paper Exists | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 10 | The Four Realism Gaps | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 11 | Executed Evidence Versus Staged Work | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |
| 12 | Final Synthesis And Teach-Back | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Not started |

## Session Record

Loop number:

Date:

What I can now explain from memory:

What I still cannot explain clearly:

The most common mistake I almost made:

My application output:

My teach-back summary in 3-5 sentences:

## Performance Rule

- 0 = I mostly copied the notes.
- 1 = I roughly understand but cannot explain clearly.
- 2 = I can explain clearly with minor gaps.
- 3 = I can explain, predict, and apply without notes.

If you score:

- `0` or `1`: repeat the same loop tomorrow.
- `2`: move forward, but revisit on Day 3.
- `3`: move forward and teach it within 24 hours.

---

# 8. Oral Exam Mode

This section turns the learning path into a spoken, pressure-tested learning experience.

## Rules

- Answer out loud before looking at the answer check.
- Keep each first answer under 60 seconds.
- If your answer is weak, repair it immediately in one second attempt.
- If you can predict, explain, and apply the idea, move on.

## Grading Scale

- `0`: I froze or guessed.
- `1`: I recognized the topic but explained it badly.
- `2`: I explained it mostly right with some gaps.
- `3`: I explained it clearly and accurately.

## Questions

### Q1

Explain continuous integration to a freshman who has only written solo code.

Answer check: include repeated code changes, repeated automated checks, fast feedback, and uncertainty reduction.

### Q2

What is regression testing, and why is it central to CI?

Answer check: regressions are old behaviors breaking after new changes, tests are rerun to catch that damage, and CI relies on that repeated check.

### Q3

What is test case prioritization, and what does it not do?

Answer check: it changes order, not suite membership; it is different from test selection or reduction.

### Q4

Why can a prioritization method be scientifically interesting but practically useless?

Answer check: overhead can erase benefit; CI is time-sensitive.

### Q5

What was the original paper trying to do?

Answer check: unified benchmark, 11 techniques, 11 projects, effectiveness plus efficiency plus applicability.

### Q6

State the original paper's regime story correctly.

Answer check: more-failure -> ACER-PA; less-failure -> MART.

### Q7

Why is pretrained MART one of the most important findings in the original paper?

Answer check: strong transfer improvement, 50% to 80%, practical leverage.

### Q8

Why does the original paper care so much about metrics and runtime cost?

Answer check: fair evaluation and CI applicability.

### Q9

What is our paper trying to do that the original paper did not try to do?

Answer check: realism qualification and conditional validity.

### Q10

Name and explain the four realism gaps.

Answer check: label, governance, representation, external validity.

### Q11

Why is our paper not just “the old paper was wrong”?

Answer check: benchmark-valid can still need deployment qualification.

### Q12

Which direction currently has the clearest executed result in the manuscript, and what is that result?

Answer check: Direction C, proxy representation path underperformed FAST-pw, still informative.

### Q13

Why can flaky tests distort the original benchmark's recommendations?

Answer check: noisy labels, false failure signal, history-based amplification.

### Q14

Why is federated pretraining a big deal even though it is not fully executed here?

Answer check: governance realism, raw-log sharing constraints, tests whether transfer survives under federation.

### Q15

Why does a weak Direction C proxy result not kill the idea of semantic representations?

Answer check: proxy is weaker than full contextual encoding; one path failing is not the whole family failing.

### Q16

What is the most mature one-sentence relationship between the two papers?

Answer check: the original paper tells us what wins under benchmark conditions, and our paper tests when those wins remain trustworthy under realism constraints.

## Final Oral Tasks

1. Explain both papers in 60 seconds.
2. Defend this statement: “A benchmark can be correct and still be incomplete for deployment.”
3. Teach the whole topic in plain language using only these five bits of jargon: CI, regression, TCP, MART, flaky.

---

# 9. Flashcard Deck

Use the exact format: question -> reasoning -> answer.

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

- Day 1: Cards 1-10
- Day 3: Cards 11-20
- Day 7: Cards 21-30
- Day 14: Cards 31-40
- Day 30: Full-deck recall without notes

---

# 10. 30-Day Execution Plan

## Core Rule

Every study block must include all four:

1. structure
2. retrieval
3. application
4. review scheduling

If a block contains only reading, it does not count.

## Week 1: Build The Core

### Day 1

- Read Foundations.
- Answer the recall questions from memory.
- Fill one block in the student tracker.
- Explain CI, regression testing, and TCP out loud in 2 minutes total.

### Day 2

- Read the Original Paper Guide.
- Memorize the regime story correctly.
- Write one 6-sentence recommendation for a low-failure CI team.

### Day 3

- Review Day 1 with no notes first.
- Start cards 1-10 from the flashcard deck.
- Do Oral Exam Q1-Q4.

### Day 4

- Re-read only the weakest part of the Original Paper Guide.
- Do Oral Exam Q5-Q8.
- Write the 50% versus 80% pretraining explanation from memory.

### Day 5

- Read Our Paper Guide.
- Memorize the four realism gaps.
- Write a short paragraph explaining “benchmark-valid but deployment-conditional.”

### Day 6

- Review Day 2 and Day 5 from memory.
- Start cards 11-20.
- Do Oral Exam Q9-Q12.

### Day 7

- Read the Synthesis Workbook.
- Give the 60-second explanation of both papers.
- Fill in tracker notes for what is still fuzzy.

## Week 2: Pressure-Test Understanding

### Day 8

- Do Intensive Loops 1-2.
- Complete recall and application for both.

### Day 9

- Do Loops 3-4.
- Re-answer Oral Exam Q1-Q4 without looking.

### Day 10

- Review Day 7 teach-back.
- Start cards 21-30.
- Write one example of effective-but-inapplicable TCP.

### Day 11

- Do Loops 5-6.
- Rebuild the original paper setup from memory.

### Day 12

- Do Loops 7-8.
- Say the regime story and pretraining story back to back without hesitation.

### Day 13

- Do Oral Exam Q13-Q16.
- Start cards 31-40.
- Write one memo about whether to trust the benchmark in a noisy CI system.

### Day 14

- Full review day.
- No reading for the first half.
- Explain everything from memory first.
- Only then check the docs and repair weak spots.

## Week 3: Move From Recall To Transfer

### Day 15

- Do Loops 9-10.
- Explain why our paper is not a rejection of the original paper.

### Day 16

- Do Loops 11-12.
- Sort evidence into verified, proxy-executed, framework, staged.

### Day 17

- Full-deck flashcard recall for cards 1-20.
- Fix the three weakest cards by rewriting them in your own words.

### Day 18

- Full-deck flashcard recall for cards 21-40.
- Redo the hardest five orally.

### Day 19

- Write a one-page comparison of the two papers.
- No notes for the first draft.

### Day 20

- Read your one-page comparison.
- Mark every fuzzy sentence.
- Repair each one using the guides.

### Day 21

- Give a 3-minute teach-back as if tutoring another freshman.
- Record the points where you stall or become vague.

## Week 4: Consolidate And Ship Understanding

### Day 22

- Redo Oral Exam Q1-Q8.
- Target score: mostly `3`.

### Day 23

- Redo Oral Exam Q9-Q16.
- Target score: mostly `3`.

### Day 24

- Revisit the weakest two loops only.
- Do not reread everything.

### Day 25

- Write the engineering manager memo from the Synthesis section.
- Include failure rate, flaky labels, pretraining, representation, and overhead.

### Day 26

- Rewrite the memo in simpler language for a non-expert reader.
- This checks whether you really understand it.

### Day 27

- Full-deck flashcard run.
- Mark any cards that still take longer than 10 seconds to answer.

### Day 28

- Do the 60-second explanation and the 3-minute explanation.
- Compare them: short version should be sharp, long version should be structured.

### Day 29

- Final no-notes review.
- Explain:
  - CI
  - TCP
  - the regime story
  - pretrained MART
  - the four realism gaps
  - the relationship between the two papers

### Day 30

- Write a final one-page summary from memory.
- Compare it with this manual.
- Mark what is now stable knowledge and what still needs repetition.

## Minimum Completion Standard

You are done when you can:

1. explain the original paper without reversing the regime story
2. explain our paper without treating it as a casual contradiction
3. state why pretrained MART matters
4. name and explain the four realism gaps
5. distinguish strong evidence from staged work in this repo

## Anti-Perfectionism Rule

If you can explain, predict, and apply the idea, ship the understanding and move on. Refinement happens after use, not before.