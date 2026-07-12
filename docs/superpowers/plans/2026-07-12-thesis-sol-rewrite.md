# Thesis Sol Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task by task, with chapter-level workers and independent review.

**Goal:** Produce a complete GPT-5.6-sol second pass of the PhD thesis that improves argument and prose without changing its scientific content.

**Architecture:** Use one non-overlapping worker for `main.tex` and each chapter file.
Each worker performs a paragraph-by-paragraph pass under a chapter-specific brief, while the main agent owns cross-chapter integration, technical verification, compilation, and publication.

**Tech Stack:** LaTeX, `uiophdthesis`, BibTeX references in `references.tex`, `latexmk`, Git, and the `plain-technical-prose` writing standard.

---

## Shared Worker Contract

Every worker must read the full text of its assigned file, the relevant task below, `docs/thesis/rewrite-review-sol.md`, and `notes/notation-and-terminology.md`.
Chapter 6 and any worker touching GLoRa results must verify claims against `papers/glora-iclr-2025.pdf`.

Every worker must:

- edit only its assigned file;
- review every paragraph, including paragraphs that ultimately remain unchanged;
- preserve all LaTeX commands, equations, citations, labels, numbers, and supported claims;
- keep one sentence per source line;
- avoid em dashes, inflated language, synonym cycling, and formulaic section openings;
- avoid rewriting solely to create a diff;
- run `git diff --check -- <assigned-file>` and inspect `git diff -- <assigned-file>`;
- report `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED` with a concise summary.

Workers do not commit or push.

### Task 1: Front Matter and Abstract

**Files:**
- Modify: `main.tex`

- [ ] Read both abstracts, preface, paper list, and inclusion metadata.
- [ ] Rewrite the English abstract so problem, benchmark design, empirical result, and thesis significance each have a distinct role.
- [ ] Make only clearly safe Norwegian edits and preserve all factual metadata.
- [ ] Verify that commands, inputs, paper inclusion, and citation keys are unchanged.
- [ ] Run `git diff --check -- main.tex` and self-review the diff.

### Task 2: Introduction

**Files:**
- Modify: `chapters/chapter01-introduction.tex`

- [ ] Review each paragraph for whether it motivates graph learning, defines the long-range problem, introduces the evaluation gap, or states the thesis response.
- [ ] Remove repeated versions of the benchmark claim while preserving the modelling/evaluation distinction.
- [ ] Make RQ1--RQ3 arise directly from the unresolved problems and keep the contribution list factual.
- [ ] Preserve all citations, description environments, labels, and chapter references.
- [ ] Run `git diff --check -- chapters/chapter01-introduction.tex` and self-review the diff.

### Task 3: Graph Learning and Message Passing

**Files:**
- Modify: `chapters/chapter02-graph-learning-message-passing.tex`

- [ ] Preserve every graph and message-passing definition and equation exactly in meaning.
- [ ] Improve the progression from graph objects and tasks to locality, symmetry, standard architectures, expressivity, and benchmark target functions.
- [ ] Shorten thesis-level repetition where the local formal point already carries the argument.
- [ ] Check all uses of $G=(V,E,\lambda)$, $N(v)$, $h_v^{(\ell)}$, $L$, and $d$ against the notation guide.
- [ ] Run `git diff --check -- chapters/chapter02-graph-learning-message-passing.tex` and self-review the diff.

### Task 4: Long-Range Dependencies

**Files:**
- Modify: `chapters/chapter03-long-range-dependencies.tex`

- [ ] Make the informal definition, path-aware formalization, and evaluation meaning cumulative.
- [ ] Preserve intervention and duplicate-segment explanations, node-level and graph-level distinctions, and domain breadth.
- [ ] Clarify graph distance, path length, and dependency length without adding new notation.
- [ ] Tighten the access-versus-use argument and remove circular restatement.
- [ ] Run `git diff --check -- chapters/chapter03-long-range-dependencies.tex` and self-review the diff.

### Task 5: Failure Explanations

**Files:**
- Modify: `chapters/chapter04-failure-explanations.tex`

- [ ] Use predicted internal traces as the chapter's organizing principle.
- [ ] Give over-smoothing, over-squashing, and vanishing gradients distinct mechanisms, evidence standards, and GLoRa interpretations.
- [ ] Consolidate generic warnings that an accuracy drop is not itself a diagnosis.
- [ ] Preserve the directedness qualification and the narrow scope of the diagnostic conclusions.
- [ ] Run `git diff --check -- chapters/chapter04-failure-explanations.tex` and self-review the diff.

### Task 6: State of the Art

**Files:**
- Modify: `chapters/chapter05-state-of-the-art.tex`

- [ ] Preserve every named method, benchmark, citation, table, caption, and label.
- [ ] Replace catalogue rhythm with comparisons based on assumptions, mechanisms, and evidence.
- [ ] Give each family its own synthesis: local reach, usable depth, changed graph semantics, visibility plus structural encoding, practical usefulness, or controlled target functions.
- [ ] Let tables carry compact summaries and keep captions focused on how to read them.
- [ ] Run citation, label, and named-method checks before self-reviewing the diff.
- [ ] Run `git diff --check -- chapters/chapter05-state-of-the-art.tex`.

### Task 7: The GLoRa Contribution

**Files:**
- Modify: `chapters/chapter06-glora-contribution.tex`

- [ ] Verify the file against the included paper before editing.
- [ ] Make each design element answer a named evaluation threat: path dependence, hole-count shortcuts, graph statistics, fairness, expressibility, or diagnostic ambiguity.
- [ ] Preserve Properties (P1)--(P3), feature ranges, chain counts, splits, training protocol, dependency-length findings, and all qualifications.
- [ ] Preserve the distinction between an exact witness path of length $d$ and the implemented generator parameter.
- [ ] Reduce duplication among the opening, Motivation, Expressibility, and Thesis-Level Interpretation sections.
- [ ] Run `git diff --check -- chapters/chapter06-glora-contribution.tex` and self-review the diff against the paper.

### Task 8: Discussion and Conclusion

**Files:**
- Modify: `chapters/chapter07-discussion-conclusion.tex`

- [ ] Make Summary state established findings without reproducing the abstract.
- [ ] Make Significance explain the change in evaluation practice.
- [ ] Preserve all five limitations: synthetic control, dependency family, feature simplicity, empirical scope, and causal incompleteness.
- [ ] Tie each future direction to one of those limitations or to the empirical result.
- [ ] End with a bounded cumulative contribution rather than another chapter summary.
- [ ] Run `git diff --check -- chapters/chapter07-discussion-conclusion.tex` and self-review the diff.

### Task 9: Chapter-Level Compliance Review

**Files:**
- Review: `main.tex`
- Review: `chapters/*.tex`

- [ ] For each file, compare the diff with its task brief and shared worker contract.
- [ ] Check that no technical content, citations, labels, equations, methods, limitations, or results were lost.
- [ ] Send any concrete gaps back to a correction worker with the exact file and paragraph.
- [ ] Re-review corrected files until no compliance issue remains.

### Task 10: Thesis-Level Prose Review

**Files:**
- Review and, only where needed, modify: `main.tex`, `chapters/*.tex`

- [ ] Read the abstract, chapter openings, chapter endings, RQs, contributions, GLoRa interpretation, and final conclusion as one argument.
- [ ] Remove cross-chapter repetition that chapter-level workers could not see.
- [ ] Check terminology against `notes/notation-and-terminology.md`.
- [ ] Scan for scaffold openings, overloaded sentences, repeated caveats, em dashes, and one-sentence paragraphs that break flow.
- [ ] Confirm that the second pass improved purpose or clarity rather than merely changing wording.

### Task 11: Mechanical and LaTeX Verification

**Files:**
- Verify: all changed files

- [ ] Run `git diff --check` and fix any whitespace errors.
- [ ] Compare counts and names of citations, labels, equations, tables, and section headings with commit `a15da39`.
- [ ] Run a fresh build with `latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex`.
- [ ] Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` again to confirm references are stable.
- [ ] Inspect warnings and distinguish existing layout warnings from new errors.
- [ ] Confirm that the working tree contains only intended thesis prose and documentation changes.

### Task 12: Publish the Sol Rewrite

**Files:**
- Commit: intended thesis sources and Sol review/design/plan documents

- [ ] Stage files explicitly and inspect the staged diff summary.
- [ ] Commit with a message that identifies the Sol second pass.
- [ ] Push the current thesis branch to Overleaf `origin/main`.
- [ ] Push the same commit to GitHub `github/thesis-overleaf` without touching GitHub `main`.
- [ ] Verify that local `HEAD`, `origin/main`, and `github/thesis-overleaf` resolve to the same commit.
