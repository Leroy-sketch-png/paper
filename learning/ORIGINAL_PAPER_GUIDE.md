# Original Paper Guide: What The Benchmark Actually Says

Source anchor in this workspace:

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