# Oral Exam Mode

This file turns the learning path into a spoken, pressure-tested learning experience.

Use it after reading the standard guides or during the intensive 12-loop curriculum.

## Purpose

The goal is not passive recognition.

The goal is to make you:

- explain clearly
- avoid common reversals
- recover from mistakes
- speak in structured, accurate language under pressure

## Rules

- Answer out loud before looking at the answer check.
- Keep each first answer under 60 seconds.
- If your answer is weak, repair it immediately in one second attempt.
- If you can predict, explain, and apply the idea, move on.
- Do not reread indefinitely. Speak, fail, repair, continue.

## Grading Scale

- `0`: I froze or guessed.
- `1`: I recognized the topic but explained it badly.
- `2`: I explained it mostly right with some gaps.
- `3`: I explained it clearly and accurately.

If you score:

- `0` or `1`: repeat the same question later that day.
- `2`: revisit on Day 3.
- `3`: teach it to someone else within 24 hours.

## Round 1: Foundations

### Q1

Explain continuous integration to a freshman who has only written solo code.

#### Answer check

A strong answer includes:

- code changes happen often
- automated checks run after changes
- the purpose is fast feedback
- CI reduces uncertainty about whether the new code broke something

### Q2

What is regression testing, and why is it central to CI?

#### Answer check

A strong answer includes:

- regressions are old behaviors breaking after new changes
- tests are rerun to catch that damage
- CI relies on regression testing as repeated memory of expected behavior

### Q3

What is test case prioritization, and what does it not do?

#### Answer check

A strong answer includes:

- TCP changes order, not suite membership
- the purpose is earlier discovery of useful failures
- it is different from test selection or test reduction

### Q4

Why can a prioritization method be scientifically interesting but practically useless?

#### Answer check

A strong answer includes:

- overhead can be too high
- prediction time can erase the benefit
- CI is time-sensitive, so applicability matters

## Round 2: Original Paper

### Q5

What was the original paper trying to do?

#### Answer check

A strong answer includes:

- unified benchmark
- 11 ML-based TCP techniques
- 11 projects
- effectiveness, efficiency, and applicability in CI

### Q6

State the original paper's regime story correctly.

#### Answer check

This must come out correctly:

- more-failure subjects: ACER-PA
- less-failure subjects: MART

If you reverse those, the answer is wrong even if everything else sounds good.

### Q7

Why is pretrained MART one of the most important findings in the original paper?

#### Answer check

A strong answer includes:

- cross-subject pretraining materially improves results
- original MART optimal on 50% of subjects
- pretrained MART optimal on 80% of subjects
- this is highly actionable for CI practice

### Q8

Why does the original paper care so much about metrics and runtime cost?

#### Answer check

A strong answer includes:

- evaluation can be distorted by weak metrics
- rAPFD was proposed for fairer comparison
- runtime and prediction cost matter for deployment

## Round 3: Our Paper

### Q9

What is our paper trying to do that the original paper did not try to do?

#### Answer check

A strong answer includes:

- qualify benchmark recommendations under realism constraints
- focus on deployment-conditional validity
- produce a conditional-validity map

### Q10

Name and explain the four realism gaps.

#### Answer check

You need all four:

- label realism
- governance realism
- representation realism
- external validity

### Q11

Why is our paper not just “the old paper was wrong”?

#### Answer check

A strong answer includes:

- the benchmark can still be valid inside its own setup
- the issue is whether recommendations survive real deployment constraints
- our paper qualifies rather than casually rejects

### Q12

Which direction currently has the clearest executed result in the manuscript, and what is that result?

#### Answer check

A strong answer includes:

- Direction C
- proxy vocabulary-anchored embedding path
- underperformed FAST-pw on the tested SIR subjects
- negative result is still informative

## Round 4: Stress Questions

### Q13

Why can flaky tests distort the original benchmark's recommendations?

#### Answer check

A strong answer includes:

- failures may be noise rather than regressions
- history-based methods may amplify noisy labels
- APFD-like results can be inflated or misinterpreted

### Q14

Why is federated pretraining a big deal even though it is not fully executed here?

#### Answer check

A strong answer includes:

- centralized pooling may be unrealistic in real organizations
- federated learning addresses governance constraints
- it tests whether the transfer benefit can survive without raw log sharing

### Q15

Why does a weak Direction C proxy result not kill the idea of semantic representations?

#### Answer check

A strong answer includes:

- the proxy is not full UniXcoder contextual encoding
- one weak representation path does not invalidate the whole representation family
- FALCON remains the stronger external semantic reference point

### Q16

What is the most mature one-sentence relationship between the two papers?

#### Answer check

Target idea:

The original paper tells us what wins under benchmark conditions, and our paper tests when those wins remain trustworthy under realism constraints.

## Final Oral Tasks

### Task A: 60-second explanation

Explain both papers in this order:

1. the problem
2. the original benchmark answer
3. why that answer may need qualification
4. what our paper adds

### Task B: One-minute defense

Defend this statement:

“A benchmark can be correct and still be incomplete for deployment.”

### Task C: Freshman teach-back

Teach the whole topic in plain language with no jargon except these five words:

- CI
- regression
- TCP
- MART
- flaky

## Oral Exam Repair Rule

If you miss a question, immediately do three things:

1. Say what you got wrong.
2. Say the corrected answer in one sentence.
3. Give one example that makes the corrected answer concrete.