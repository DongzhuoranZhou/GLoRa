# Thesis Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the thesis prose so the argument is clearer, less repetitive, and more thesis-like while preserving all technical claims, LaTeX structure, math, citations, labels, and bibliography.

**Architecture:** Work is split by disjoint TeX files so subagents can edit in parallel without conflicts. Each worker rewrites every paragraph in its assigned file using the plain technical prose rules, then performs a local self-review against the notation file and the review memo. The main agent integrates the resulting patches, runs LaTeX verification, and performs a final consistency pass.

**Tech Stack:** LaTeX thesis source, `uiophdthesis` class, chapter files in `chapters/`, bibliography embedded in `references.tex`, and the included GLoRa PDF under `papers/`.

---

## Shared Rewrite Rules

Every worker must read these files before editing:

- `docs/thesis/rewrite-review.md`
- `notes/notation-and-terminology.md`
- The assigned TeX file

Every worker must follow these constraints:

- Preserve citation keys, labels, references, equations, display math, tables, and LaTeX commands unless fixing a compile error.
- Preserve scientific claims and empirical numbers.
- Do not add new claims, new citations, or new terminology.
- Keep one sentence per source line.
- Remove most repeated scaffold openings such as "This section explains..." by turning them into direct topic sentences.
- Keep terms consistent with `notes/notation-and-terminology.md`.
- Do not edit files outside the assigned write scope.
- Do not revert or overwrite changes made by other workers.
- Return a summary that lists changed files, main rewrite choices, and any concerns.

## Task 1: Front Matter and Main Thesis Frame

**Files:**
- Modify: `main.tex`

- [ ] **Step 1: Review `main.tex` against the thesis claim**

Read the English abstract, Norwegian abstract, preface, List of Papers, and chapter inputs.
Identify sentences that can be made more direct without changing content.

- [ ] **Step 2: Rewrite the English abstract**

Make the abstract state three things plainly:

1. The problem: message-passing GNNs can fail when target labels depend on information at large graph distance.
2. The thesis angle: the problem is also an evaluation problem because benchmarks can reward shortcut functions.
3. The contribution: GLoRa controls dependency length and is designed so fitting requires the intended path-aware dependency.

- [ ] **Step 3: Lightly review the Norwegian abstract**

Only make edits that clearly improve grammar or alignment with the English abstract.
Do not make speculative language changes.

- [ ] **Step 4: Preserve front-matter commands**

Do not change `\title`, `\subtitle`, `\author`, `\uiopaper`, `\uioincludepdf`, or input order.

- [ ] **Step 5: Self-review**

Run:

```bash
git diff -- main.tex
```

Check that only prose changed and that all LaTeX commands remain intact.

## Task 2: Chapter 1, Introduction

**Files:**
- Modify: `chapters/chapter01-introduction.tex`

- [ ] **Step 1: Rewrite the chapter opening**

Make the opening lead with the thesis problem rather than describing the chapter.
Keep GLoRa, benchmark design, and long-range dependency learning in the first page.

- [ ] **Step 2: Rewrite section openings**

Replace the repeated "This section..." openings with direct topic sentences.
Keep reader orientation but remove outline-like phrasing.

- [ ] **Step 3: Tighten repeated evaluation claims**

The introduction should introduce the shortcut problem once, return to it in the evaluation section, and use GLoRa as the concrete answer.
Avoid repeating the same claim in nearly identical words.

- [ ] **Step 4: Preserve research questions and contributions**

Keep RQ 1, RQ 2, RQ 3 and the four contributions.
Improve flow into and out of them, but do not change their substantive meaning.

- [ ] **Step 5: Self-review**

Run:

```bash
git diff -- chapters/chapter01-introduction.tex
```

Check that citation keys and section headings are preserved.

## Task 3: Chapter 2, Graph Learning and Message Passing

**Files:**
- Modify: `chapters/chapter02-graph-learning-message-passing.tex`

- [ ] **Step 1: Preserve notation**

Keep `G=(V,E,\lambda)`, `N(v)`, `h_v^{(\ell)}`, `L`, `d`, and all equations aligned with `notes/notation-and-terminology.md`.

- [ ] **Step 2: Rewrite scaffolding**

Reduce repeated "This section..." and "It matters because..." wording.
Turn these into direct statements about why the definitions matter.

- [ ] **Step 3: Improve transitions**

Make the chapter flow from graph objects to tasks, message passing, locality, permutation symmetry, standard architectures, expressivity, and benchmark target functions.

- [ ] **Step 4: Preserve formal content**

Do not alter equations, multiset notation, receptive field definitions, or the expressivity argument.

- [ ] **Step 5: Self-review**

Run:

```bash
git diff -- chapters/chapter02-graph-learning-message-passing.tex
```

Check that every symbol still has the same meaning and that `d` is used only for distance or dependency length.

## Task 4: Chapter 3, Long-Range Dependencies

**Files:**
- Modify: `chapters/chapter03-long-range-dependencies.tex`

- [ ] **Step 1: Sharpen the concept sequence**

Make the chapter move cleanly from informal dependency, to path-aware definition, to the distinction among graph distance, path length, and dependency length.

- [ ] **Step 2: Compress repeated examples**

Keep social, traffic, biochemical, web, and financial examples only where they add distinct intuition.
Remove repetitive sentences that merely restate that paths matter.

- [ ] **Step 3: Preserve path-aware definition details**

Keep the intervention, duplicate segment, and damaged-original-path explanation.
Make the prose simpler, but do not weaken the definition.

- [ ] **Step 4: Strengthen the access-versus-use section**

Make the distinction between large receptive field and learned dependency one of the chapter's central takeaways.

- [ ] **Step 5: Self-review**

Run:

```bash
git diff -- chapters/chapter03-long-range-dependencies.tex
```

Check that all uses of \(d\), \(p=(v_0,\ldots,v_d)\), source node, and target node remain consistent.

## Task 5: Chapter 4, Explanations of Long-Range Failure

**Files:**
- Modify: `chapters/chapter04-failure-explanations.tex`

- [ ] **Step 1: Make "internal trace" the organizing thread**

Every explanation should answer: what internal trace would make this diagnosis credible?

- [ ] **Step 2: Tighten each phenomenon**

For over-smoothing, focus on representation collapse.
For over-squashing, focus on compression through bottlenecks.
For vanishing gradients, focus on weak backward signal in early layers.

- [ ] **Step 3: Reduce repeated caveats**

Preserve the narrow claim that GLoRa does not rule out these phenomena generally.
Avoid restating the same caveat after every paragraph.

- [ ] **Step 4: Preserve diagnostic findings**

Keep all claims about target-node representations, bounded directed paths, and stable gradients.

- [ ] **Step 5: Self-review**

Run:

```bash
git diff -- chapters/chapter04-failure-explanations.tex
```

Check that each explanation still has a predicted trace and that the GLoRa conclusion remains restrained.

## Task 6: Chapter 5, State of the Art

**Files:**
- Modify: `chapters/chapter05-state-of-the-art.tex`

- [ ] **Step 1: Rewrite subsection openings**

Reduce formulaic openings across the 12 subsections.
Each opening should say what the method family contributes and what specific evaluation risk remains.

- [ ] **Step 2: Make method-family conclusions specific**

Avoid using the same "helps access but does not certify dependency" sentence repeatedly.
For each family, state the local issue:

- Standard GNNs: local reach and depth.
- Depth methods: usable depth versus certified use.
- Rewiring: changed graph semantics and possible shortcuts.
- Transformers: visibility without graph relation learning.
- Real-world benchmarks: practical usefulness without controlled target functions.
- Synthetic benchmarks: control without automatic shortcut or expressibility guarantees.

- [ ] **Step 3: Tighten tables and captions**

Keep all tables and labels.
Make captions explain how to read the table, not restate the whole result.

- [ ] **Step 4: Preserve all method coverage**

Do not delete named methods or citations.
Condense only repeated prose around them.

- [ ] **Step 5: Self-review**

Run:

```bash
git diff -- chapters/chapter05-state-of-the-art.tex
```

Check that all section labels, table labels, and citations remain present.

## Task 7: Chapter 6, The GLoRa Contribution

**Files:**
- Modify: `chapters/chapter06-glora-contribution.tex`

- [ ] **Step 1: Strengthen the chapter arc**

Make the chapter read as a construction:

1. Benchmark scores need a dependency guarantee.
2. Path-aware dependency defines the target.
3. The generator removes shortcuts.
4. Expressibility prevents an impossible-task interpretation.
5. Experiments estimate the length limit.
6. Diagnostics narrow the explanation.

- [ ] **Step 2: Preserve generator details**

Keep node feature forms, the filler range `[-12,-2]\cup[3,13]`, the role of holes, alternative chains, extra holes, and directedness.

- [ ] **Step 3: Preserve properties P1-P3**

Do not weaken P1, P2, or P3.
Make clear how the three properties work together.

- [ ] **Step 4: Preserve protocol and findings**

Keep dataset sizes, split ratio, run count, epoch limit, `d+2` layers, AdamW, batch normalization, gradient clipping, ReLU, batch size, and reported length behaviour.

- [ ] **Step 5: Self-review**

Run:

```bash
git diff -- chapters/chapter06-glora-contribution.tex
```

Check that all empirical details and citation keys are unchanged.

## Task 8: Chapter 7, Discussion and Conclusion

**Files:**
- Modify: `chapters/chapter07-discussion-conclusion.tex`

- [ ] **Step 1: Make the conclusion cumulative**

The conclusion should show what the reader can now say after the thesis, not simply repeat earlier chapter summaries.

- [ ] **Step 2: Tighten the summary**

Keep the modelling/evaluation distinction, GLoRa construction, expressibility point, empirical result, and diagnostics.
Remove repeated phrasing where possible.

- [ ] **Step 3: Keep limitations concrete**

Preserve the five limitations: synthetic control, dependency family, simple features, empirical scope, and causal incompleteness.
Make each limitation read as a precise boundary of the thesis.

- [ ] **Step 4: Strengthen future work**

Make future directions follow directly from the limitations and findings:
new benchmark families, stronger diagnostics, architectures for path-aware memory, semi-synthetic real-graph tests, and better reporting practice.

- [ ] **Step 5: Self-review**

Run:

```bash
git diff -- chapters/chapter07-discussion-conclusion.tex
```

Check that the final paragraphs restate the thesis contribution without adding unsupported claims.

## Task 9: Main-Agent Integration and Verification

**Files:**
- Inspect: `main.tex`
- Inspect: `chapters/*.tex`
- Inspect: `references.tex`
- Inspect: `notes/notation-and-terminology.md`

- [ ] **Step 1: Review worker diffs**

Run:

```bash
git diff -- main.tex chapters/*.tex
```

Check for conflicting terminology, changed citations, changed labels, or accidental LaTeX edits.

- [ ] **Step 2: Check source mechanics**

Run:

```bash
rg -n "This section|This subsection|It matters because|This matters because|---| -- |—|–" main.tex chapters/*.tex
```

Remaining matches must be intentional.

- [ ] **Step 3: Check terminology**

Run:

```bash
rg -n "long dependency|range length|prediction node|starting node|oversmoothing|oversquashing" main.tex chapters/*.tex
```

Expected result: no unintended terminology drift.

- [ ] **Step 4: Build the thesis**

Prefer:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If `latexmk` is unavailable, run:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

- [ ] **Step 5: Final prose pass**

Read the abstract, Chapter 1 opening, Chapter 6 opening, and Chapter 7 conclusion together.
They should state the same thesis arc at different levels of maturity: problem, contribution, evidence, and implication.
