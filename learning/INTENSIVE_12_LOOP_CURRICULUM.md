# Intensive 12-Loop Curriculum

This is the extreme version of the learning path.

It applies the Universal Learning OS more than 10 times on the exact material in this workspace.

Use it when you do not want a light overview. Use it when you want repeated structure until the ideas stick.

## How To Use This File

- Do one loop at a time.
- Do not skip recall.
- Do not skip application.
- Do not spend more than 45-60 minutes on one loop before producing output.
- After three passes on a loop, move to speech, writing, or problem-solving.

## The 12 Loops

### Loop 1: Continuous Integration

#### 1. Define the core

Continuous integration is the practice of repeatedly integrating code changes and re-running automated checks after each change.

#### 2. Rules / principles

- Code changes happen often.
- Each change creates uncertainty.
- Automated testing reduces that uncertainty.
- Fast feedback matters because developers need answers while the change is still fresh.

#### 3. Map the structure

- Input: commit.
- Trigger: CI pipeline starts.
- Process: build, test, report.
- Output: pass, fail, or warning signal.

#### 4. Edge cases and mistakes

- Mistake: thinking CI is just “run all tests.”
- Mistake: ignoring time cost.
- Edge case: a pipeline may pass while still being too slow to be useful.

#### 5. Test recall

1. What problem does CI solve?
2. Why does speed matter in CI?
3. What is the difference between a commit and a CI cycle?
4. Why is repeated automation better than occasional manual checking?
5. What kind of uncertainty is CI trying to reduce?

#### 6. Apply once

Write a 5-sentence explanation of CI to a freshman who has only written local programs on their own laptop.

#### 7. Review with spacing

- Day 1: define CI from memory.
- Day 3: draw the CI pipeline.
- Day 7: explain why slow feedback weakens CI.

### Loop 2: Regression Testing

#### 1. Define the core

Regression testing checks whether new code changes broke behavior that used to work.

#### 2. Rules / principles

- Old behavior matters.
- New code can introduce unintended damage.
- Tests act as memory for the system.
- Regressions are costly because they often surprise developers late.

#### 3. Map the structure

- Old system state.
- New code change.
- Re-run tests.
- Compare expected and actual behavior.

#### 4. Edge cases and mistakes

- Mistake: thinking every failure is a regression.
- Mistake: forgetting flaky tests.
- Edge case: the test is wrong, not the product code.

#### 5. Test recall

1. What is a regression?
2. Why can a test fail without a real regression?
3. Why is regression testing central to CI?
4. What does a test suite remember for a team?
5. Why is regression testing never fully free?

#### 6. Apply once

Give one example of a code change that fixes one bug but accidentally creates a regression somewhere else.

#### 7. Review with spacing

- Day 1: define regression from memory.
- Day 3: explain one false-positive scenario.
- Day 7: explain why regressions matter in team development.

### Loop 3: Test Case Prioritization

#### 1. Define the core

Test case prioritization means ordering tests so the most useful failures appear earlier.

#### 2. Rules / principles

- Test order changes feedback timing.
- TCP does not remove tests; it reorders them.
- Earlier useful failures improve developer response.
- Good ordering is more valuable when time is limited.

#### 3. Map the structure

- Full test suite exists.
- Method assigns a priority score or ranking.
- Tests run in that order.
- Team observes how quickly informative failures surface.

#### 4. Edge cases and mistakes

- Mistake: confusing prioritization with test reduction.
- Mistake: assuming any early failure is useful.
- Edge case: a flaky test is prioritized early and wastes time.

#### 5. Test recall

1. What does TCP change?
2. What does TCP not change?
3. Why can early failure discovery matter more than total test count?
4. Why might a bad priority order still eventually run all tests?
5. Why is TCP especially relevant in CI?

#### 6. Apply once

Imagine 10 tests and only time for 4 before a developer must decide whether to merge. Explain why order matters.

#### 7. Review with spacing

- Day 1: define TCP from memory.
- Day 3: compare TCP with test selection.
- Day 7: explain one realistic reason order matters more than raw suite size.

### Loop 4: Metrics And Overhead

#### 1. Define the core

TCP metrics try to measure how quickly faults are found, while overhead measures whether the method is worth the cost of running.

#### 2. Rules / principles

- A ranking method must help enough to justify its own runtime.
- Good science needs a fair metric.
- A metric can distort conclusions if it does not match the CI setting.
- Practicality matters as much as raw score.

#### 3. Map the structure

- APFD: fault-detection speed idea.
- rAPFD: corrected fairness-oriented metric used in the original paper.
- Overhead: training time plus prediction time.
- Applicability: whether CI can actually tolerate that overhead.

#### 4. Edge cases and mistakes

- Mistake: ranking methods only by accuracy-like numbers.
- Mistake: ignoring prediction cost.
- Edge case: the method is good on paper but too slow in practice.

#### 5. Test recall

1. Why does overhead matter in TCP?
2. What is the intuition behind APFD?
3. Why did the original paper care about rAPFD?
4. How can a method be effective but inapplicable?
5. Why is metric choice not a minor detail?

#### 6. Apply once

Describe a situation where Method A finds failures earlier than Method B, but Method A still should not be deployed.

#### 7. Review with spacing

- Day 1: explain APFD and overhead at a high level.
- Day 3: explain why metric choice can reverse conclusions.
- Day 7: produce one example of effective-but-inapplicable.

### Loop 5: The Method Families

#### 1. Define the core

The workspace compares several families of TCP methods: heuristics, similarity methods, ML/RL methods, and semantic or embedding-based methods.

#### 2. Rules / principles

- Simpler methods are cheaper and often more robust.
- Learned methods can exploit richer historical patterns.
- Semantic methods depend heavily on representation quality.
- No family wins automatically under every condition.

#### 3. Map the structure

- Heuristics: simple rules.
- FAST: non-ML similarity/diversity baseline.
- ML and RL: data-driven ranking policies.
- FALCON-style semantic methods: code embeddings plus stronger selection logic.

#### 4. Edge cases and mistakes

- Mistake: assuming ML is always superior.
- Mistake: treating FAST as a trivial baseline.
- Edge case: a strong representation can still fail if the downstream method is weak.

#### 5. Test recall

1. What is the benefit of heuristics?
2. Why is FAST important in this repo?
3. What extra risks do ML and RL methods add?
4. Why are semantic methods exciting?
5. Why should you compare across families instead of only within one family?

#### 6. Apply once

Write a short ranking of the method families by expected complexity of deployment, from easiest to hardest, and explain your reasoning.

#### 7. Review with spacing

- Day 1: list the four families.
- Day 3: compare FAST and ML-based TCP.
- Day 7: explain why semantic methods are not automatically superior.

### Loop 6: The Original Paper Setup

#### 1. Define the core

The original paper is a unified benchmark that compares 11 ML-based TCP techniques under one controlled CI-oriented setup.

#### 2. Rules / principles

- Fair comparison needs one shared setup.
- Different techniques must be tested under the same evaluation logic.
- Subject-level differences matter.
- Practical recommendations should come from both effectiveness and applicability.

#### 3. Map the structure

- 11 projects.
- 800 commits per project.
- 11 ML-based techniques.
- rAPFD, runtime, and applicability analysis.

#### 4. Edge cases and mistakes

- Mistake: remembering only the winners and forgetting the setup.
- Mistake: assuming one aggregate chart tells the whole story.
- Edge case: a technique looks strongest in one aggregate view but not as the practical subject-level choice.

#### 5. Test recall

1. How many projects were studied?
2. How many techniques were compared?
3. Why does a unified setup matter?
4. What kinds of outputs did the benchmark examine besides effectiveness?
5. Why is this paper stronger than a narrow one-method comparison?

#### 6. Apply once

Write a short paragraph explaining why benchmarking many methods under one setup is more persuasive than reading several isolated papers that each test only one method.

#### 7. Review with spacing

- Day 1: memorize 11 projects, 11 techniques, 800 commits.
- Day 3: explain why unified setup matters.
- Day 7: explain benchmark scope without notes.

### Loop 7: The Original Paper Findings

#### 1. Define the core

The original paper's most important message is that the best ML-based TCP method depends on the failure-rate regime, while MART is the strongest practical overall choice.

#### 2. Rules / principles

- Failure-rate regime changes the best method.
- Data imbalance is a major explanatory factor.
- Practicality matters, not only raw ranking quality.
- Pretraining can materially improve outcomes.

#### 3. Map the structure

- More-failure subjects: ACER-PA best.
- Less-failure subjects: MART best.
- Overall practical default: MART.
- Pretrained MART: stronger than original MART.

#### 4. Edge cases and mistakes

- Mistake: reversing ACER-PA and MART.
- Mistake: collapsing “best in one regime” into “best everywhere.”
- Edge case: a technique can dominate in one regime and collapse in another.

#### 5. Test recall

1. Which method is best on more-failure subjects?
2. Which method is best on less-failure subjects?
3. Why is MART still the practical overall recommendation?
4. What role does data imbalance play?
5. Why must you not reverse the regime story?

#### 6. Apply once

Write the regime story as a one-line memory hook you can repeat without hesitation.

#### 7. Review with spacing

- Day 1: recite the regime story correctly.
- Day 3: explain why data imbalance matters.
- Day 7: explain the difference between local winner and practical default.

### Loop 8: Pretrained MART And Transfer

#### 1. Define the core

One of the original paper's highest-leverage findings is that cross-subject pretraining makes MART much stronger.

#### 2. Rules / principles

- More training data can improve ranking quality.
- Cross-subject signal can be valuable.
- Finetuning on the target project matters.
- Transfer learning changes what a new project can do before it has much local history.

#### 3. Map the structure

- Original MART optimal sequence on 50% of subjects.
- Pretrained MART optimal sequence on 80% of subjects.
- Interpretation: better initialization from outside-project data.

#### 4. Edge cases and mistakes

- Mistake: treating pretraining as a minor detail.
- Mistake: assuming transfer is always free or always allowed.
- Edge case: transfer may help less when source and target differ too much.

#### 5. Test recall

1. Why is pretrained MART such a big deal?
2. What are the 50% and 80% numbers about?
3. Why is transfer learning high leverage in CI?
4. What practical problem does pretraining solve for a new project?
5. What hidden assumption is built into centralized pretraining?

#### 6. Apply once

Write a short product pitch for why a CI team should care about pretrained MART.

#### 7. Review with spacing

- Day 1: memorize 50% and 80% correctly.
- Day 3: explain transfer in plain language.
- Day 7: explain one limit of cross-subject pretraining.

### Loop 9: Why Our Paper Exists

#### 1. Define the core

Our paper exists because a benchmark recommendation can be valid inside the benchmark and still become fragile in deployment.

#### 2. Rules / principles

- Benchmark validity is not identical to deployment validity.
- Real systems add noise, policy, and representation changes.
- Good follow-up research does not only ask “what wins?” but also “when is that advice trustworthy?”
- Qualification is intellectually stronger than blind acceptance or blind rejection.

#### 3. Map the structure

- Keep the benchmark as baseline.
- Stress its assumptions.
- Identify robustness, fragility, and possible inversion.
- Produce a conditional-validity map.

#### 4. Edge cases and mistakes

- Mistake: saying our paper disproves the old paper.
- Mistake: saying the new paper is only a summary.
- Edge case: a benchmark can still be very useful even if some conclusions are conditional.

#### 5. Test recall

1. Why did we revisit the benchmark?
2. What does “deployment-conditional” mean?
3. What is a conditional-validity map?
4. Why is our paper not just a replacement leaderboard?
5. Why is qualification better than casual disagreement?

#### 6. Apply once

Write a 6-sentence explanation of why a benchmark result may need qualification before deployment.

#### 7. Review with spacing

- Day 1: define conditional validity.
- Day 3: contrast benchmark validity and deployment validity.
- Day 7: explain why our paper depends on the original one.

### Loop 10: The Four Realism Gaps

#### 1. Define the core

The new paper organizes its challenge to the benchmark into four realism gaps: label realism, governance realism, representation realism, and external validity.

#### 2. Rules / principles

- Labels can be noisy.
- Data sharing can be restricted.
- Representations can change what methods see.
- Harder deployment environments can weaken old conclusions.

#### 3. Map the structure

- Direction A: flaky labels.
- Direction B: federated pretraining.
- Direction C: LLM representations.
- Direction D: Android or mobile CI extension.

#### 4. Edge cases and mistakes

- Mistake: memorizing the directions without understanding the underlying realism problem.
- Mistake: assuming all four directions were executed equally.
- Edge case: one realism gap may matter much more than another in a given deployment.

#### 5. Test recall

1. What does label realism ask?
2. What does governance realism ask?
3. What does representation realism ask?
4. What does external validity ask?
5. Why are these four gaps enough to reshape how we read the benchmark?

#### 6. Apply once

For a company with strict privacy rules and lots of intermittent failures, say which two realism gaps matter first and why.

#### 7. Review with spacing

- Day 1: list the four gaps from memory.
- Day 3: pair each gap with its direction letter.
- Day 7: explain which gap worries you most in practice and why.

### Loop 11: Executed Evidence Versus Staged Work

#### 1. Define the core

Not every part of the new paper is at the same evidence level, so learning it correctly means separating executed findings from protocols and staged extensions.

#### 2. Rules / principles

- Verified findings are stronger than planned work.
- Protocols matter, but they are not the same as executed results.
- Honest status labeling protects research integrity.
- Students learn faster when they know what is proven versus what is proposed.

#### 3. Map the structure

- Executed manuscript-integrated result: Direction C proxy representation finding.
- Protocol or framework: Direction A and Direction B.
- Staged extension: Direction D.
- Verified supporting baselines: FAST, heuristic summaries, FALCON artifact references.

#### 4. Edge cases and mistakes

- Mistake: speaking as if all directions were completed equally.
- Mistake: treating a proxy result as the final word on all LLM representations.
- Edge case: a negative executed result can still be very valuable.

#### 5. Test recall

1. Which direction currently has the clearest executed manuscript result?
2. Why is Direction B not the same kind of evidence as Direction C?
3. Why is Direction D explicitly staged?
4. Why is evidence labeling essential in this repo?
5. Why can a proxy negative result still matter scientifically?

#### 6. Apply once

Sort these into buckets: verified, executed proxy, protocol/framework, staged.

- pretrained MART result from the source paper
- Direction C BPE proxy result
- federated pretraining framework
- Android extension

#### 7. Review with spacing

- Day 1: name the executed direction.
- Day 3: re-sort the evidence buckets.
- Day 7: explain why honesty about status improves trust.

### Loop 12: Final Synthesis And Teach-Back

#### 1. Define the core

The final lesson is that the original paper tells us what wins in the benchmark, and our paper tells us when that answer remains trustworthy outside the benchmark.

#### 2. Rules / principles

- Do not collapse benchmark truth into deployment truth.
- Do not throw away a good benchmark because it has limits.
- Do not accept a recommendation without checking realism constraints.
- Mature understanding means keeping both papers in one mental model.

#### 3. Map the structure

- Problem: CI needs useful failures early.
- Original answer: benchmark the ML-based TCP methods.
- Key result: regime-dependent recommendations plus pretrained MART.
- New challenge: realism can weaken those recommendations.
- New output: conditional-validity map.

#### 4. Edge cases and mistakes

- Mistake: asking “which paper wins?” instead of “what does each paper contribute?”
- Mistake: forgetting the role of evidence status.
- Edge case: a deployment can still use the original recommendation if the realism gaps are small.

#### 5. Test recall

1. In one sentence, what is the original paper about?
2. In one sentence, what is our paper about?
3. What is the regime story in the original paper?
4. What is the central organizing idea in our paper?
5. What should an engineer ask before trusting the benchmark recommendation?

#### 6. Apply once

Do all three of these:

1. Explain both papers in 60 seconds.
2. Write a one-page memo to an engineering manager about whether to trust the benchmark recommendation.
3. Teach the topic to a fictional freshman version of yourself using only plain language.

#### 7. Review with spacing

- Day 1: do the 60-second talk.
- Day 3: write the memo from memory.
- Day 7: teach both papers without notes.
- Day 14: revisit the loops you found hardest.
- Day 30: write a final summary and compare it with the docs.

## Master Compression

If you remember only the bare minimum, remember this:

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