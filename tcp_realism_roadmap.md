# TCP Realism Project – Hands-on Roadmap

This is a standalone roadmap for pushing your paper further **as a broke student with an office laptop**, without needing to come back to the chat.

It assumes you already know the basics of:
- Continuous integration (CI)
- Test case prioritization (TCP)
- The original ML-based TCP benchmark (MART / ACER-PA regime story)
- Your own paper’s idea of **realism gaps** and a **conditional-validity map**

Use this file as a working doc: edit, check off tasks, and take notes directly in here.

---

## 0. North Star

**Thesis you are aiming for**

> The original TCP benchmark is “benchmark-true”: it tells us what wins under its own assumptions. Your paper asks when that advice stays reliable once you add four realism gaps: noisy labels, non-shareable data, representation shifts, and harder deployment environments.

Your goal is to become the **“realism cartographer”** for ML-based TCP:

- You do **not** try to out-compute big labs.
- You **do** design sharp, small, honest experiments that stress-test the benchmark’s assumptions.
- You end with a **conditional-validity map**: when can a CI team safely copy the benchmark’s recommendation, and when must they add caveats or switch methods.

Keep repeating this to yourself when you feel lost.

---

## 1. Constraints and Superpowers

Write your own quick notes here so you keep reality in view.

```markdown
### My constraints
- Hardware: (e.g., 4 CPU cores, 16GB RAM office laptop)
- Time per week: (e.g., 10–15 hours)
- Datasets I can actually access: (...)
- Code I can actually run: (...)

### My superpowers
- I deeply understand the original benchmark setup and findings.
- I have the realism-gap framework (labels, governance, representation, external validity).
- I already distinguish executed vs proxy vs framework vs staged evidence.
- I can write clearly and explain things out loud.
```

Fill this block properly before you touch experiments.

---

## 2. Big Structure: Phases

Think in **three execution phases**. You can stretch or compress timelines, but keep the order.

1. **Phase 1 – Deep internalization (7–10 days)**  
   Get both papers and the realism framework into your bones so you can improvise.

2. **Phase 2 – Micro-experiments (10–20+ days)**  
   Run 2–3 small but sharp experiments that each attack a realism gap.

3. **Phase 3 – Synthesis and writing (7–14 days)**  
   Turn your understanding + experiments into a compelling story and conditional-validity map.

You can loop these phases (e.g., add another micro-experiment later), but always make sure each phase is *completed* at least once.

---

## 3. Phase 1 – Deep Internalization (7–10 days)

Goal: you should be able to explain **both papers and your realism agenda** in under 60–90 seconds, without notes.

Use your existing 12-loop learning system, but point it at your research:

### 3.1 Loops to actually run

Focus on these loops first:

- Loop 5 – Method Families (heuristics, FAST, ML/RL, semantic)
- Loop 6 – Original Paper Setup (11 projects, 11 techniques, 800 commits, metrics and overhead)
- Loop 7 – Original Paper Findings (regime story: ACER-PA vs MART, practical MART default, pretraining)
- Loop 8 – Pretrained MART and Transfer (50% vs 80% optimal sequences; centralized pretraining assumptions)
- Loop 9 – Why Our Paper Exists (benchmark validity vs deployment validity)
- Loop 10 – The Four Realism Gaps (labels, governance, representation, external validity)
- Loop 11 – Executed vs Staged Evidence (Direction C executed proxy; Direction A/B frameworks; Direction D staged)
- Loop 12 – Final Synthesis (how both papers fit together)

For each loop, follow your own rules:

- No more than **45–60 minutes** per loop before producing output.
- Always do **recall** and **application**, not just reading.

### 3.2 Per-loop output template

For each loop, add a section like this to this file:

```markdown
#### Loop X – [Topic]

1. My 3–5 sentence explanation from memory:
   - ...

2. One thing that surprised me or I misunderstood at first:
   - ...

3. One question this raises for *our* research:
   - ...

4. One possible micro-experiment idea this suggests:
   - ...
```

By the end of Phase 1, you should have 6–8 of these filled.

### 3.3 Phase 1 completion checklist

You are done with Phase 1 when you can:

- Explain both papers in 60 seconds: problem → original answer → why that’s not enough → what your paper adds.
- Recite the **regime story** without hesitation.
- List the **four realism gaps** and give a one-sentence example for each.
- List which parts of your own paper are executed vs proxy vs framework vs staged.

Write a short reflection here when you hit that point:

```markdown
### Phase 1 Reflection
- What I understand clearly now:
- What still feels fuzzy:
- Which realism gap I want to attack first:
```

---

## 4. Phase 2 – Micro-Experiments (10–20+ days)

Goal: run **2–3 tight experiments** that each stress-test one assumption in the benchmark. Each one should be small enough to run on your laptop, but sharp enough to say something non-trivial.

Pick **two or three** of the following. It’s better to finish two properly than start five.

---

### 4.1 Experiment A – Label Realism Micro-Lab (Direction A)

**Question:** How does flaky label noise change the relative ranking of a history-based ML TCP method vs a simple non-ML baseline like FAST or a heuristic?

**High-level plan:**

1. Take one benchmark subject (or a synthetic version if needed).
2. Introduce artificial flakiness into failure labels at different rates (e.g., 0%, 5%, 10%, 20%).
3. Compare rAPFD (or similar) for:
   - a history-based ML/TCP method
   - a non-ML baseline (FAST-pw or a simple heuristic)
4. Observe at what noise levels the ML method’s advantage shrinks, disappears, or inverts.

**Steps checklist:**

- [ ] Choose the subject or synthetic dataset.
- [ ] Implement a simple label-noise injection function.
- [ ] Select one ML/TCP method and one non-ML baseline.
- [ ] Run for several noise levels and log metrics.
- [ ] Plot or tabulate results.
- [ ] Write a half-page interpretation.

**Notes / results:**

```markdown
### Experiment A Notes
- Dataset:
- Methods compared:
- Noise levels tested:
- Main pattern I see:
- How this affects the original benchmark advice:
```

---

### 4.2 Experiment B – Governance Realism via Degraded Pretraining (Direction B)

**Question:** How sensitive is the pretraining benefit (e.g., MART’s jump from 50% to 80% optimal sequences) to losing access to some projects due to governance constraints?

**High-level plan:**

1. Start from whatever version of MART or similar model you can realistically train.
2. Define several pretraining conditions:
   - Centralized: pretrain on “all available projects”.
   - Restricted 1: pretrain on half the projects.
   - Restricted 2: pretrain on a different half, or only on similar projects.
3. For each, fine-tune on the target project(s) and measure the same metrics the benchmark cares about.
4. Look at how much benefit you lose as pretraining data shrinks.

**Steps checklist:**

- [ ] Identify which projects you can actually include.
- [ ] Implement pretraining + fine-tuning pipeline at small scale.
- [ ] Define centralized vs restricted scenarios.
- [ ] Run and log metrics for each scenario.
- [ ] Write a half-page interpretation focusing on “centralized as upper bound”.

**Notes / results:**

```markdown
### Experiment B Notes
- Projects used:
- Pretraining scenarios compared:
- Performance differences observed:
- How this reframes pretraining in governance-constrained CI:
```

---

### 4.3 Experiment C – Representation Realism Ablation (Direction C)

**Question:** Why did a plausible BPE-style proxy representation underperform FAST-pw, and can cheap tweaks make it competitive?

**High-level plan:**

1. Start from your existing BPE-style proxy embedding pipeline on 5 subjects.
2. Change only **cheap knobs** (no giant new models):
   - Tokenization granularity (e.g., character vs word-piece).
   - Vocabulary size.
   - Adding simple metadata (file-type tags, path buckets).
3. Re-run the same TCP method using these variants.
4. Compare against FAST-pw in terms of:
   - mean delta APFD
   - rank correlation of test ordering
5. Identify whether any cheap variant meaningfully closes the gap.

**Steps checklist:**

- [ ] Document the current proxy pipeline clearly.
- [ ] Define 2–4 cheap variants to try.
- [ ] Run all variants on the same subjects.
- [ ] Compare each variant to FAST-pw.
- [ ] Do a small error analysis: where do the worst disagreements occur?

**Notes / results:**

```markdown
### Experiment C Notes
- Variants tried:
- Performance vs FAST-pw:
- Patterns in where proxy fails:
- Final takeaway on naive “semantic” signals vs FAST:
```

---

### 4.4 Experiment D – External Validity via Synthetic Stress (Direction D)

**Question:** How do longer, more variable test durations and platform-specific behaviors (like in mobile or long-running suites) affect the benchmark’s story?

**High-level plan (synthetic):**

1. Take an existing subject where test durations are moderate.
2. Inject a small number of **very long** tests and/or artificially skew the duration distribution.
3. Evaluate a few prioritization strategies (MART-like, FAST, simple heuristics) on:
   - time-to-first-useful-failure
   - overall rAPFD
4. See whether methods that look similar in the benchmark start to diverge when durations become more extreme.

**Steps checklist:**

- [ ] Choose subject and define synthetic duration perturbation.
- [ ] Implement perturbed duration profiles.
- [ ] Re-evaluate methods under the new durations.
- [ ] Write up how the regime story shifts (or holds) under this stress.

**Notes / results:**

```markdown
### Experiment D Notes
- Perturbation used:
- Methods compared:
- Changes in time-to-first-failure:
- What this suggests about external validity:
```

---

### 4.5 Per-experiment mini-report template

When you finish an experiment, immediately write **1–2 pages** using this template (still inside this file or a new one):

```markdown
# Experiment [A/B/C/D] – [Title]

## Question

## Why this matters for the benchmark

## Setup
- Data / subjects:
- Methods compared:
- Metrics:

## Results (short)

## Interpretation
- What stays consistent with the benchmark story:
- What weakens:
- Any inversion or surprising behavior:

## Threats to validity / limitations

## One sentence that could go into the main paper
```

These mini-reports will later turn into sections or subsections in your manuscript.

---

## 5. Phase 3 – Synthesis and Writing (7–14 days)

Goal: glue everything into a **compelling narrative** that sounds like a serious, opinionated, realistic follow-up to the benchmark.

### 5.1 Core story skeleton

Draft your paper around this skeleton:

1. **Problem:** CI teams want earlier useful failures but face real-world messiness.
2. **Original answer:** the benchmark compares 11 ML-based TCP methods on 11 projects and recommends ACER-PA for high-failure subjects, MART (especially pretrained) for low-failure subjects.
3. **Why that’s not enough:** those recommendations assume clean labels, centralized data, fixed representations, and relatively friendly deployment environments.
4. **What you add:** you stress-test the benchmark along four realism gaps and build a conditional-validity map: when the original advice survives, weakens, or inverts.
5. **Your concrete findings:** short bullets summarizing your 2–3 experiments.
6. **Actionable guidance:** a simple decision surface for practitioners.

Write this skeleton as 1–2 pages of prose first, before worrying about LaTeX or formatting.

### 5.2 Conditional-validity map for practitioners

Design a table or flowchart like this:

```markdown
| Condition in CI system                             | Trust level in MART/ACER-PA benchmark advice | Recommended attitude                    |
|---------------------------------------------------|-----------------------------------------------|-----------------------------------------|
| Failures rare, flaky tests low, centralized data  | High                                          | Follow benchmark (MART) with minor checks. |
| Failures rare, flaky tests high                   | Medium                                        | Re-check label realism; consider robust baselines. |
| No cross-project data sharing allowed             | Medium                                        | Treat centralized pretraining gains as an upper bound. |
| Representation pipeline heavily changed           | Low–Medium                                    | Re-evaluate vs FAST/heuristics locally. |
| Long, highly variable test durations (e.g., mobile) | Unknown/Low                                 | Require local stress tests before adoption. |
```

Adapt the wording once you have actual results.

### 5.3 Evidence status as a contribution

Make “evidence status” explicit in the paper, not just internally:

- Mark which claims are **verified benchmark**, **executed proxy experiment**, **framework/protocol**, or **staged**.
- Emphasize that honest status labeling is part of the contribution: it tells practitioners what they can rely on now vs where they should expect future work.

Add a small table in the paper summarizing this; you already have the conceptual structure.

### 5.4 Final reflection

At the end of this file, keep a running log of what you’ve actually done and learned.

```markdown
## Execution Log

- [Date] Finished Phase 1, loops done: ...
- [Date] Completed Experiment A runs, key pattern: ...
- [Date] Completed Experiment C, main surprise: ...
- [Date] Drafted synthesis skeleton, current gaps: ...
```

This is mostly for you, but it will also help when you write the paper’s “Threats to validity” and “Future work” sections.

---

## 6. How to Use This File

1. **Clone it into your repo** as `tcp_realism_roadmap.md` or similar.
2. Treat it as a **living notebook**, not a static plan.
3. Every time you sit down to work, open this file first and:
   - Check what phase and experiment you’re in.
   - Write down what you’ll do in the next 45–60 minutes.
   - After the block, write what you actually did and learned.
4. When in doubt, return to the North Star (Section 0).

If you follow this with discipline, you’ll end up with:
- A much deeper personal understanding of both papers.
- 2–3 small but real experiments.
- A clear, ambitious story that’s honest about constraints and still intellectually strong.

