# Thesis Structural Revision Implementation Plan

> **Execution rule:** This plan begins only after user approval. Use `superpowers:subagent-driven-development` for chapter execution, `plain-technical-prose` for all prose revisions, and `superpowers:verification-before-completion` before publication.

**Goal:** Restructure the complete PhD thesis so that its abstracts, research questions, chapter responsibilities, evidence, and conclusion form an explicit closed argument, while preserving the verified scientific content of commit `2b78c0a`.

**Architecture:** The main agent first records a mechanical baseline, locks the research questions, creates a paragraph-level migration matrix, and performs the cross-file moves. Only then do disjoint chapter agents revise every paragraph inside stable boundaries. Two independent reviewers check thesis architecture and technical preservation before compilation and publication.

**Single-paper constraint:** GLoRa is the only included paper. The kappa must map each RQ to the relevant kappa chapter and to GLoRa's definitions, construction, experiments, or diagnostics; it must not imitate a multi-paper thesis structure.

**Source files:** `main.tex`, `chapters/chapter01-introduction.tex` through `chapters/chapter07-discussion-conclusion.tex`, `references.tex`, `notes/notation-and-terminology.md`, and `papers/glora-iclr-2025.pdf`.

**Publication targets:** Overleaf `origin/main` and GitHub `github/thesis-overleaf`.

---

## Phase A: Freeze the Evidence and Structure

### Task 1: Record the Baseline Manifest

**Create:**
- `docs/thesis/structural-baseline-2026-07-16.md`
- `artifacts/structural-revision/baseline/`

**Read:**
- `main.tex`
- `chapters/*.tex`
- `references.tex`
- `notes/notation-and-terminology.md`
- `papers/glora-iclr-2025.pdf`

- [ ] Confirm that execution starts from commit `2b78c0a`, or record and review any later user changes without reverting them.
- [ ] Record `git status`, branch, remotes, thesis word and line counts, compiled kappa page count, and included-paper checksum.
- [ ] Extract sorted baseline inventories of citation keys, labels, references, chapter and section headings, equations, tables, figures, and included-paper commands.
- [ ] Record all numerical claims in Chapters 4, 6, and 7 that describe GLoRa results or diagnostics.
- [ ] Compile the untouched baseline twice and preserve the logs and PDF metadata.
- [ ] Mark pre-existing warnings separately so later review detects only regressions.

**Verification:**

```bash
git status --short --branch
git rev-parse HEAD
sha256sum papers/glora-iclr-2025.pdf
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

**Gate:** No structural edit begins until the baseline manifest is complete and reproducible.

### Task 2: Update the Literature on Long-Range Failure Mechanisms

**Create:**
- `docs/thesis/literature-update-2026-07-16.md`

**Read:**
- `chapters/chapter03-long-range-dependencies.tex`
- `chapters/chapter04-failure-explanations.tex`
- `chapters/chapter05-state-of-the-art.tex`
- `chapters/chapter06-glora-contribution.tex`
- `references.tex`

- [ ] Conduct independent searches for over-smoothing, over-squashing, and empirical diagnosis of long-range graph-learning failures through July 2026.
- [ ] Use primary papers for technical claims and surveys only to discover or cross-check primary sources.
- [ ] Verify every candidate paper programmatically through at least one bibliographic API and, where possible, a publisher, proceedings, DOI, or arXiv source.
- [ ] Separate mechanism definitions, predicted traces, empirical diagnostics, and mitigation methods; do not treat improved accuracy as proof that a named mechanism caused the original failure.
- [ ] Record which relevant works are already cited, which are missing, and which do not change the thesis argument enough to include.
- [ ] Add only verified bibliography entries and document their DOI, proceedings, or arXiv source.
- [ ] Revise the Chapter 4 and Chapter 5 content contracts if the current literature requires a different distinction or stronger qualification.
- [ ] Have one independent agent review the literature memo for citation accuracy and unsupported synthesis.

**Gate:** No chapter prose is rewritten until the main agent has accepted a verified mechanism/diagnostic taxonomy and a bounded list of new citations.

### Task 3: Build the Paragraph-Level Migration Matrix

**Create:**
- `docs/thesis/structural-migration-matrix.md`

**Read:**
- `docs/superpowers/specs/2026-07-16-thesis-structural-revision-design.md`
- `main.tex`
- `chapters/*.tex`

- [ ] Assign every source paragraph a stable identifier such as `C3-S2-P04`.
- [ ] Record its current location, principal claim, local function, citations, equations or labels, and whether the claim appears elsewhere.
- [ ] Assign exactly one action: `KEEP`, `MOVE`, `MERGE`, `DELETE AS REPETITION`, or `ADD`.
- [ ] For `MOVE` and `MERGE`, record the destination chapter and section.
- [ ] For every deletion, identify the retained paragraph that carries the claim and citations.
- [ ] Add rows for genuinely missing material: scope, RQ/evidence map, author role, direct RQ answers, and figure captions.
- [ ] Produce a chapter-level count of kept, moved, merged, deleted, and added paragraphs.
- [ ] Check that every current section and every substantive paragraph is accounted for.

**Gate:** The main agent reviews and freezes the matrix before any chapter subagent edits prose.

### Task 4: Lock the Research Questions and Evidence Map

**Modify only after plan approval:**
- `docs/thesis/structural-migration-matrix.md`
- `chapters/chapter01-introduction.tex`

**Verify against:**
- `papers/glora-iclr-2025.pdf`
- `docs/thesis/structural-baseline-2026-07-16.md`

- [ ] Verify that each proposed RQ is answerable by existing definitions, construction, experiments, or diagnostics.
- [ ] Narrow any wording that would require unsupported causal or universal claims.
- [ ] Lock one term for each concept: graph distance, path length, dependency length, path-aware dependency, shortcut function, expressibility, and diagnostic trace.
- [ ] Create a provisional RQ-to-kappa-chapter-to-GLoRa-evidence-to-contribution table.
- [ ] Check that every contribution corresponds to at least one RQ and every RQ corresponds to reported evidence.

**Gate:** RQ wording does not change during chapter drafting unless the main agent reopens the evidence map and updates all dependent chapters.

### Task 5: Install the New Chapter Skeleton

**Modify:**
- `chapters/chapter01-introduction.tex`
- `chapters/chapter02-graph-learning-message-passing.tex`
- `chapters/chapter03-long-range-dependencies.tex`
- `chapters/chapter04-failure-explanations.tex`
- `chapters/chapter05-state-of-the-art.tex`
- `chapters/chapter06-glora-contribution.tex`
- `chapters/chapter07-discussion-conclusion.tex`

- [ ] Apply the approved chapter titles and section hierarchy from the design document.
- [ ] Preserve existing labels where their referents remain valid; add or rename labels only with a documented cross-reference update.
- [ ] Physically move paragraphs according to the frozen matrix without polishing them yet.
- [ ] Move citations, footnotes, equations, tables, and labels with the claims they support.
- [ ] Insert explicit placeholders only in the migration matrix, not in thesis prose, for missing transitions or evidence.
- [ ] Compare source and destination counts after every move to prevent silent content loss.
- [ ] Compile once to catch broken labels, environments, or references caused by migration.

**Gate:** The thesis must compile and the migration matrix must show every move completed before paragraph-level rewriting starts.

---

## Phase B: Rebuild the Front Matter and Chapters

### Task 6: Align the Abstracts and Front Matter

**Modify:**
- `main.tex`

**Agent:** dedicated front-matter agent

- [ ] Rewrite the English abstract using the five-part content contract: problem, evaluation gap, method, principal evidence, significance and boundary.
- [ ] Revise the Norwegian abstract to make the same claims in the same order, including the main empirical and diagnostic result.
- [ ] Back-translate or independently check every technical Norwegian sentence against the English factual content.
- [ ] Add `\listoffigures` and `\listoftables` once the final figure set is known.
- [ ] Add a concise author-contribution statement based only on verified authorship information.
- [ ] Preserve title metadata, paper metadata, input order, and paper inclusion commands.
- [ ] Have a second agent compare both abstracts claim by claim.

**Acceptance:** A five-row bilingual content table shows no omitted or stronger claim in either abstract.

### Task 7: Rebuild Chapter 1, Introduction

**Modify:**
- `chapters/chapter01-introduction.tex`

**Agent brief:** establish the full thesis contract without teaching later chapters in advance.

- [ ] Open with the concrete running example and the inference that current evaluation evidence can be ambiguous.
- [ ] Establish motivation, problem, evaluation gap, scope, and boundaries in that order.
- [ ] State the locked RQs exactly.
- [ ] Rewrite the contribution list so each item identifies an output and the evidence supporting it.
- [ ] Present Paper I and the verified author role without duplication from the front matter.
- [ ] Add the RQ-to-kappa-chapter-to-GLoRa-evidence map, treating GLoRa as the sole included paper.
- [ ] Rewrite the outline as a sequence of argumentative handoffs.
- [ ] Remove detailed mechanism, benchmark-construction, and result material now owned by Chapters 3--6.
- [ ] Review every paragraph against one named Chapter 1 function in the migration matrix.

**Acceptance:** A reader can predict what each RQ asks, where it is answered, what the thesis contributes, and where its claims stop.

### Task 8: Narrow Chapter 2, Technical Foundations

**Modify:**
- `chapters/chapter02-graph-learning-message-passing.tex`

**Agent brief:** retain only the formal tools used by the thesis argument.

- [ ] Keep graph, feature, node-classification, and message-passing definitions and notation technically unchanged.
- [ ] Build one progression from local updates to depth, receptive fields, and the distinction between reachability and use.
- [ ] Retain symmetry and expressivity only where later chapters rely on them.
- [ ] Move mechanism-oriented architecture material to Chapter 4 and benchmark-validity material to Chapter 5 according to the matrix.
- [ ] Remove generic application or architecture survey prose that has no later use, preserving any unique supported claim in its proper destination.
- [ ] End with the exact technical premise Chapter 3 needs.
- [ ] Check notation against `notes/notation-and-terminology.md`.

**Acceptance:** Every definition or subsection is cited by, or explicitly prepares, a later thesis claim.

### Task 9: Refocus Chapter 3 on the Evaluation Target

**Modify:**
- `chapters/chapter03-long-range-dependencies.tex`

**Agent brief:** define what must be learned before discussing why learning fails or how to benchmark it.

- [ ] Merge the informal and formal accounts into one cumulative explanation.
- [ ] Define graph distance, path length, dependency length, and path-aware dependency without synonym drift.
- [ ] Use the running example to distinguish reachability, correlation, and dependence.
- [ ] Explain the intervention or paired-example logic that makes dependence observable.
- [ ] State node-level and graph-level scope, then delimit the thesis to GLoRa's inductive binary node-classification setting where appropriate.
- [ ] Compress broad domain examples to the minimum needed for motivation.
- [ ] End with an evaluation contract that supplies Chapter 5's criteria.
- [ ] Remove repeated generator construction and shortcut analysis whose primary home is later.

**Acceptance:** RQ 1 can be answered from Chapters 2 and 3 without relying on GLoRa's empirical result.

### Task 10: Integrate Mechanisms and Model Responses in Chapter 4

**Modify:**
- `chapters/chapter04-failure-explanations.tex`

**Sources migrated from:**
- `chapters/chapter05-state-of-the-art.tex`

**Agent brief:** pair each candidate failure mechanism with its predicted trace, intervention family, and unresolved evidential question.

- [ ] Give over-smoothing, over-squashing, and optimisation or vanishing-gradient failure separate definitions and predicted traces.
- [ ] Place depth, residual, normalisation, rewiring, diffusion, global-attention, and structural-encoding methods under the mechanism or limitation they address.
- [ ] Preserve method citations and qualifications while replacing catalogue rhythm with comparisons.
- [ ] Add or revise one synthesis table: mechanism, trace, intervention family, what success would show, and what remains unproven.
- [ ] Explain interactions once, after the separate mechanisms.
- [ ] Consolidate the warning that low accuracy alone is not a diagnosis.
- [ ] Move all GLoRa-specific diagnostic outcomes to Chapter 6.

**Acceptance:** Every method family has a reason for appearing, and every causal explanation has a testable trace rather than only an accuracy prediction.

### Task 11: Rebuild Chapter 5 Around Benchmark Validity

**Modify:**
- `chapters/chapter05-state-of-the-art.tex`

**Sources migrated from:**
- `chapters/chapter02-graph-learning-message-passing.tex`
- `chapters/chapter03-long-range-dependencies.tex`

**Agent brief:** compare evaluations by what their results can establish.

- [ ] State explicit criteria: specified dependency, controlled length, shortcut resistance, target expressibility, fair comparison, and diagnostic interpretability.
- [ ] Separate the complementary purposes of real-world and synthetic benchmarks.
- [ ] Reorganise existing benchmark families under the criteria rather than publication chronology.
- [ ] Preserve all benchmark citations and table facts.
- [ ] Move method-family surveys out to Chapter 4, retaining only model details necessary to understand benchmark fairness.
- [ ] Treat shortcuts and expressibility once at full depth in this chapter.
- [ ] End with a numbered or clearly parallel prose statement of the unresolved requirements inherited by GLoRa.
- [ ] Verify that no sentence pre-announces GLoRa's empirical conclusion.

**Acceptance:** The final gap statement leads directly and without repetition into Chapter 6's design goals.

### Task 12: Rebuild Chapter 6 as Thesis-Level Synthesis

**Modify:**
- `chapters/chapter06-glora-contribution.tex`

**Verify every technical statement against:**
- `papers/glora-iclr-2025.pdf`

**Agent brief:** explain how evidence is produced, not reproduce the included paper section by section.

- [ ] Start from Chapter 5's unresolved evaluation threats.
- [ ] For each GLoRa element, state the threat, design response, guarantee or control, and evidential consequence.
- [ ] Preserve Properties (P1)--(P3), parameter meanings, feature ranges, chain bounds, splits, protocol, and all result qualifications.
- [ ] Preserve the distinction between exact witness-path length and the generator parameter.
- [ ] Keep only enough protocol detail to interpret the results; refer readers to Paper I for exhaustive implementation detail.
- [ ] Present the main performance result once, using the verified paper figure or underlying data.
- [ ] Present each diagnostic as prediction, measurement, observation, and bounded conclusion.
- [ ] State explicitly which evidence answers RQ 2 and RQ 3.
- [ ] Add the verified author contribution and distinguish paper contribution from thesis synthesis.
- [ ] Remove repeated general motivation, definitions already owned by Chapter 3, and benchmark criteria already owned by Chapter 5.

**Acceptance:** The chapter can be outlined as `threat -> design -> guarantee -> result -> interpretation`, and every numerical or diagnostic statement matches Paper I.

### Task 13: Rebuild Chapter 7 Around Direct RQ Answers

**Modify:**
- `chapters/chapter07-discussion-conclusion.tex`

**Dependency:** Chapters 1--6 must be structurally stable.

**Agent brief:** close the exact contract made in Chapter 1.

- [ ] Answer RQ 1, RQ 2, and RQ 3 in separate, explicitly labelled subsections and in the original order.
- [ ] For each answer, distinguish established evidence from interpretation and limitation.
- [ ] State the cumulative contribution after the answers rather than repeating the abstract.
- [ ] Explain significance as a change in evaluation practice.
- [ ] Preserve the five distinct limitations: synthetic control, dependency family, feature simplicity, empirical scope, and causal incompleteness.
- [ ] Pair each future direction with a named limitation or empirical finding.
- [ ] End with a bounded conclusion and no fresh generator explanation.
- [ ] Check vocabulary against the exact RQ wording in Chapter 1.

**Acceptance:** A reviewer can locate a direct, evidence-bounded answer to every RQ without reconstructing it from the chapter summary.

---

## Phase C: Figures, Integration, and Independent Review

### Task 14: Add Evidence-Bearing Figures

**Modify:**
- `main.tex`
- `chapters/chapter01-introduction.tex`
- `chapters/chapter03-long-range-dependencies.tex`
- `chapters/chapter06-glora-contribution.tex`
- figure assets under the repository's established asset location

**Read:**
- `papers/glora-iclr-2025.pdf`
- figure captions and permissions or attribution requirements from Paper I

- [ ] Inventory figures in Paper I and identify exact source figure numbers and captions.
- [ ] Adapt or reuse a running path-aware positive/negative example with attribution.
- [ ] Adapt or reuse the main accuracy-versus-dependency-length result with all axes, legends, and tested-setting qualifications intact.
- [ ] Add a diagnostic summary only if it is directly supported by a paper figure or verified data.
- [ ] Reuse the running example by cross-reference instead of drawing near-duplicates in Chapters 1 and 3.
- [ ] Verify legibility in the compiled PDF at normal page scale and in greyscale.
- [ ] Add list of figures and list of tables to the front matter.

**Acceptance:** Every figure advances an RQ, has a self-contained caption and source attribution, and reproduces no unsupported data.

### Task 15: Run the Cross-Chapter Repetition and Terminology Audit

**Review and modify only where necessary:**
- `main.tex`
- `chapters/*.tex`

- [ ] Read the abstract, all chapter openings and endings, RQs, contribution statements, Chapter 6 interpretation, and Chapter 7 answers as one continuous argument.
- [ ] Search every occurrence of `GLoRa`, `shortcut`, `expressib`, `over-smooth`, `over-squash`, `vanishing gradient`, `dependency length`, and related variants.
- [ ] Assign one primary explanation site for each recurring concept and reduce later occurrences to purposeful callbacks.
- [ ] Check that chapter endings pose the next chapter's problem rather than summarising the whole thesis.
- [ ] Check that no chapter opening repeats the abstract.
- [ ] Audit one term per referent, notation, British English, one sentence per source line, paragraph flow, and unsupported rhetoric.
- [ ] Update migration-matrix status for every paragraph and explain any deviation from the frozen action.

**Acceptance:** Repeated concepts evolve by chapter function; they do not restart from the same general claim.

### Task 16: Independent Thesis-Architecture Review

**Reviewer:** independent agent that did not draft a chapter

**Review:**
- `main.tex`
- `chapters/*.tex`
- `docs/superpowers/specs/2026-07-16-thesis-structural-revision-design.md`
- `docs/thesis/structural-migration-matrix.md`

- [ ] Check the five-part abstract contract in both languages.
- [ ] Check RQ wording, contribution alignment, chapter ownership, and direct conclusion answers.
- [ ] Check that the structure consistently presents GLoRa as the sole included paper rather than implying a multi-paper portfolio.
- [ ] Check every chapter against its `must contain` and `must not contain` contract.
- [ ] Compare the architecture with the relevant strengths of Huiling You's thesis: explicit problem, RQs, contribution/paper map, distinct chapter dimensions, and question-by-question conclusion.
- [ ] Report findings by severity and exact file or section.
- [ ] Return actionable findings to the responsible chapter agent and re-review corrections.

**Gate:** No unresolved high- or medium-severity architecture finding.

### Task 17: Independent Technical-Preservation Review

**Reviewer:** independent agent that did not draft Chapter 6

**Compare:**
- baseline inventories under `artifacts/structural-revision/baseline/`
- revised `main.tex` and `chapters/*.tex`
- `papers/glora-iclr-2025.pdf`

- [ ] Compare citation keys, labels, references, equations, tables, numerical claims, and included-paper metadata with the baseline.
- [ ] Investigate every difference; restore accidental losses and document intentional structural changes.
- [ ] Verify GLoRa construction details, Properties (P1)--(P3), protocol, findings, and diagnostic qualifications against Paper I.
- [ ] Check that model-family descriptions remain accurate after moving from Chapter 5 to Chapter 4.
- [ ] Check that no abstract, introduction, or conclusion claim is stronger than Chapter 6's evidence.
- [ ] Report findings by severity and exact file or section, then re-review corrections.

**Gate:** No unresolved technical, citation, notation, or evidence-preservation finding.

---

## Phase D: Mechanical Verification and Publication

### Task 18: Compile and Inspect the Complete Thesis

**Verify:** all changed files

- [ ] Run `git diff --check`.
- [ ] Search for unresolved placeholders such as `TODO`, `TBD`, `FIXME`, and draft notes.
- [ ] Run a clean `latexmk` build followed by a second stability build.
- [ ] Confirm that citation and cross-reference warnings are resolved.
- [ ] Compare chapter order, paper inclusion, page counts, figure/table lists, and PDF metadata with expectations.
- [ ] Inspect the complete PDF at chapter openings, page breaks, tables, figures, captions, lists, and the transition into Paper I.
- [ ] Distinguish pre-existing layout warnings from new regressions and fix all new regressions.
- [ ] Confirm that the working tree contains no generated or unrelated files intended to remain uncommitted.

**Verification:**

```bash
git diff --check
rg -n 'TODO|TBD|FIXME|PLACEHOLDER' main.tex chapters docs/thesis
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

**Gate:** Both builds succeed, references are stable, and visual inspection reports no blocking defect.

### Task 19: Final Diff Review and Publish Identical Commits

**Commit:** intended thesis sources, figure assets, migration and review records, and the approved design and plan documents

- [ ] Review `git diff --stat`, then inspect every changed file and all deletions.
- [ ] Confirm that no unsupported claim, accidental citation loss, unrelated edit, or generated build file is staged.
- [ ] Stage intended files explicitly and inspect the staged diff.
- [ ] Create one structural-revision commit with a precise message.
- [ ] Push the commit to Overleaf `origin/main`.
- [ ] Push the identical commit to GitHub `github/thesis-overleaf` without modifying GitHub `main`.
- [ ] Verify that local `HEAD`, `origin/main`, and `github/thesis-overleaf` resolve to the same hash.
- [ ] Report the final commit, build result, principal structural changes, figure inventory, and any residual non-blocking warnings.

**Verification:**

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/main
git ls-remote github refs/heads/thesis-overleaf
```

**Done condition:** The approved structure is present in the compiled thesis, all review gates pass, and the same verified commit is available on both Overleaf and GitHub.
