# Thesis Structural Revision Design

**Status:** Implemented and independently reviewed on 2026-07-16

**Baseline:** commit `2b78c0a`

**Scope:** kappa structure, argument, content allocation, abstracts, front matter, and thesis-level figures

## 1. Purpose

This revision will make the thesis read as one cumulative argument rather than a collection of individually sound chapters that repeatedly return to GLoRa, shortcuts, expressibility, and the standard failure mechanisms.

Commit `2b78c0a` has already received a GPT-5.6-sol prose pass under the `plain-technical-prose` standard.
The new work is therefore not another blanket rewrite.
It is a structural migration: decide what each part of the thesis must establish, move existing material to the chapter where it performs that role, remove repetition, add only genuinely missing connective or evidential material, and then revise the prose paragraph by paragraph inside the new structure.

The public reference thesis by Huiling You, *Event Extraction from News: Resources, Methods, Applications*, is used as a model of thesis architecture, not as a source of technical content or wording.
Its relevant strengths are explicit research-question closure, distinct chapter responsibilities, a clear map from papers to contributions, and a conclusion that answers the research questions before discussing significance and limitations.

This thesis is a single-paper thesis.
Paper I, GLoRa, is the only included paper and the sole empirical contribution around which the kappa is organised.
The reference thesis's multi-paper mapping will therefore not be copied.
Its closure principle will be adapted as `RQ -> kappa chapter -> definition, construction, experiment, or diagnostic evidence in GLoRa`.

## 2. Baseline Diagnosis

The current kappa has seven chapters, approximately 28,500 words, and 69 pages.
It contains the technical substance needed for the revision, but the substance is not yet allocated optimally.

The main structural problems are:

- the current RQ 1 asks broadly what makes long-range learning difficult, while the included evidence can support a narrower claim about controlled evaluation and selected diagnostics;
- the research questions do not close explicitly through the contribution statement, chapter structure, and final conclusion;
- Chapters 2--5 often read as textbook or survey chapters rather than steps in the thesis argument;
- Chapters 2 and 5 both catalogue standard architectures;
- shortcut functions, expressibility, and benchmark validity recur in Chapters 2, 3, 5, 6, and 7;
- the three failure mechanisms and the interpretation of their diagnostics recur in Chapters 4, 6, and 7;
- Chapter 6 risks reproducing the included paper instead of synthesising its thesis-level contribution;
- Chapter 7 summarises the topic but does not answer RQ 1--RQ 3 one by one;
- the Norwegian abstract omits the principal empirical and diagnostic result stated in the English abstract;
- the kappa has six tables but no list of tables, no figures, and no explicit author-contribution statement.

The working assumption is that roughly 85 percent of the required content already exists.
The revision should move and consolidate that material before writing new prose.

The mechanism review also needs a literature-freshness check.
Before structural migration, independent searches will update the treatment of over-smoothing, over-squashing, and optimisation or gradient failure through July 2026.
The review will distinguish a mechanism from its predicted trace, a diagnostic measurement, and a method that merely improves performance.
Only verified primary sources that change or materially support the thesis argument will be added.

## 3. Governing Argument

The revised kappa will develop the following argument:

> A result about long-range graph learning is interpretable only when the evaluation defines the intended path-aware dependency, rules out easier shortcut functions, keeps the target expressible by the evaluated systems, and varies dependency length under controlled conditions. GLoRa implements these requirements and thereby reveals a performance decline that the reported diagnostics for over-smoothing, over-squashing, and vanishing gradients do not fully explain in the tested setting.

Each chapter must earn one part of this claim and hand the reader a specific unresolved question that the next chapter answers.

## 4. Revised Research Questions

The wording below was verified against the included paper and is frozen for the structural revision.

**RQ 1.** What evidence is required to conclude that a graph learning system has learned a path-aware dependency of a specified length?

**RQ 2.** How can a benchmark isolate a path-aware dependency of a specified length while ruling out shortcut functions, retaining target expressibility, and comparing systems fairly?

**RQ 3.** Under controlled evaluation, how does performance change with dependency length, and to what extent do the diagnostics support common failure explanations?

These questions deliberately replace the unbounded causal wording of the current RQ 1.
They match the evidence available from the definitions, benchmark construction, comparative literature review, GLoRa experiments, and reported diagnostics.

### RQ-to-Evidence Closure

| Research question | Primary chapters | Required evidence | Final closure |
|---|---|---|---|
| RQ 1 | Chapters 2 and 3 | Locality and expressivity foundations; path-aware dependency; distinction among graph distance, path length, and dependency length; criteria separating access from demonstrated use | Chapter 7 gives a direct answer and states the limits of that evidence |
| RQ 2 | Chapters 5 and 6 | Benchmark comparison; shortcut analysis; expressibility and fairness requirements; GLoRa design choices and Properties (P1)--(P3) | Chapter 7 states which controls GLoRa supplies and what remains outside its scope |
| RQ 3 | Chapters 4 and 6 | Predicted traces of the three mechanisms; performance by dependency length; representation, structural, and gradient diagnostics | Chapter 7 reports the bounded empirical answer without universalising it |

Chapter 1 will state this map explicitly.
Chapter 6 will identify which result answers which RQ.
Chapter 7 will answer every RQ in the same order and vocabulary used in Chapter 1.

## 5. Abstract Content Contract

The English and Norwegian abstracts must contain the same five content units in the same logical order:

1. **Context and problem:** message passing is local, while some node labels depend on distant information.
2. **Evaluation gap:** declining accuracy does not by itself show which dependency was attempted or why learning failed; benchmarks may permit shortcuts.
3. **Method and contribution:** GLoRa generates controlled node-classification tasks parameterised by dependency length and designed to require a path-aware dependency.
4. **Main evidence:** performance declines as dependency length increases in the tested systems, and the reported diagnostics do not fully support the three standard explanations in the tested setting.
5. **Significance and boundary:** the contribution is a controlled standard of evidence for one class of long-range dependencies, not a universal account of all long-range graph learning.

The abstracts will not contain a chapter tour, detailed generator mechanics, a literature catalogue, or claims stronger than the paper supports.

## 6. Target Chapter Architecture

### Chapter 1: Introduction

**Question answered:** Why is controlled evidence about long-range dependency learning needed, and what exactly does this thesis contribute?

**Must contain:**

- one concrete running GLoRa example that distinguishes a positive example from a plausible shortcut-bearing negative example;
- the practical and scientific motivation for long-range graph learning;
- the gap between model capability claims and what existing evaluations demonstrate;
- explicit scope and boundaries;
- the revised RQs;
- contributions aligned one-to-one with the RQs and evidence;
- Paper I, a verified author-role statement if evidence is available, and a map from each RQ to the kappa chapter and the corresponding definition, construction, experiment, or diagnostic evidence in GLoRa;
- a short chapter outline that describes argumentative roles rather than listing topics.

**Must not contain:** full definitions, a survey of failure mechanisms, generator details, or empirical results that belong to Chapters 3, 4, or 6.

### Chapter 2: Technical Foundations

**Question answered:** What graph-learning concepts are necessary to define and evaluate long-range dependency learning?

**Must contain:**

- graph, feature, node-classification, and message-passing notation used later;
- locality, depth, receptive fields, and the access-versus-use distinction;
- permutation equivariance or invariance only to the extent required by the later expressivity argument;
- the minimum expressivity foundation needed to understand why an impossible target is an invalid test of learnability.

**Must not contain:** a generic applications survey, a second state-of-the-art catalogue, or detailed benchmark criteria that belong to Chapter 5.

### Chapter 3: Long-Range Dependency as an Evaluation Target

**Question answered:** What does it mean to learn a dependency of a specified length, and what observation would count as evidence?

**Must contain:**

- an informal dependency concept followed by the path-aware formalisation;
- the distinction among graph distance, path length, and dependency length;
- node-level and graph-level scope, with GLoRa's node-classification scope made explicit;
- the difference between information being reachable and the prediction depending on it;
- intervention or paired-example reasoning that shows what evidence the benchmark must create;
- a running visual example reused from Chapter 1 and formalised here;
- a concise evaluation contract that leads into the failure and benchmark chapters.

**Must not contain:** repeated GLoRa construction details, a long applications catalogue, or claims that distance alone proves dependence.

### Chapter 4: Why Long-Range Learning Fails and How Models Address It

**Question answered:** What mechanisms may prevent long-range learning, what internal traces should they produce, and which model families target them?

**Must contain:**

- over-smoothing, over-squashing, and optimisation or gradient failure as distinct candidate mechanisms;
- the observable prediction and evidence standard for each mechanism;
- interactions among the mechanisms without collapsing them into one explanation;
- corresponding intervention families moved from current Chapter 5: depth methods, residual and normalisation methods, rewiring or diffusion methods, and global-attention or structural-encoding methods;
- a synthesis table relating mechanism, predicted trace, intervention, and remaining evidential limitation.

**Must not contain:** GLoRa's empirical verdict, repeated benchmark construction, or a method-by-method catalogue detached from the mechanisms.

### Chapter 5: Evaluating Long-Range Graph Learning

**Question answered:** Which benchmark properties make claims about dependency length valid, and what gap remains before GLoRa?

**Must contain:**

- the roles and limits of real-world and synthetic benchmarks;
- shortcut functions and why accuracy can fail to demonstrate the intended dependency;
- target-function expressibility;
- fairness across systems and control of dependency length;
- a comparison of existing benchmark families under explicit evaluation criteria;
- a final gap statement listing the requirements that no reviewed benchmark jointly establishes and that Chapter 6 will address.

**Must not contain:** another architecture survey, GLoRa's results, or a conclusion that synthetic control alone guarantees validity.

### Chapter 6: The GLoRa Contribution

**Question answered:** How does GLoRa answer the evaluation gap, and what does the resulting evidence establish?

**Internal sequence:** evaluation threat, design response, formal or constructional guarantee, empirical evidence, bounded interpretation.

**Must contain:**

- the design goals inherited explicitly from Chapter 5;
- the path-aware task, positive and negative examples, chains, holes, and controls needed to understand the construction;
- Properties (P1)--(P3), expressibility, and fairness claims exactly as supported by Paper I;
- an appropriately concise experimental protocol, referring to the included paper for reproducibility detail;
- the main performance result as a figure indexed by dependency length;
- diagnostic results for the three candidate mechanisms;
- explicit answers contributed to RQ 2 and RQ 3 by the single included GLoRa paper;
- verified author contribution and a thesis-level interpretation that does not repeat the paper abstract.

**Must not contain:** long protocol repetition, generic literature review, or universal causal claims.

### Chapter 7: Discussion and Conclusion

**Question answered:** What has the thesis established, why does it matter, where does the evidence stop, and what follows?

**Must contain, in order:**

1. direct answer to RQ 1;
2. direct answer to RQ 2;
3. direct answer to RQ 3;
4. cumulative contribution and significance for evaluation practice;
5. limitations of synthetic control, dependency family, feature simplicity, empirical scope, and causal diagnosis;
6. future work tied explicitly to those limitations;
7. a bounded final conclusion.

**Must not contain:** a fresh explanation of the generator, a repeated literature review, or claims broader than the tested setting.

## 7. Content Migration Map

The implementation will create a paragraph-level matrix before any paragraph is rewritten.
At chapter level, the intended migration is:

| Current source | Primary action | Target responsibility |
|---|---|---|
| Chapter 1 motivation and evaluation sections | Keep and consolidate | Chapter 1 problem, gap, scope, and running example |
| Chapter 1 broad RQ 1 and current contribution list | Replace and remap | Chapter 1 evidence-bounded RQs, contributions, and closure map |
| Chapter 2 graph notation, message passing, locality, symmetry | Keep and tighten | Chapter 2 foundations |
| Chapter 2 standard architecture catalogue | Reduce; move only mechanism-relevant material | Chapter 4 intervention families |
| Chapter 2 benchmark expressibility discussion | Split | Minimal formal basis in Chapter 2; evaluation criterion in Chapter 5 |
| Chapter 3 informal and formal dependency accounts | Merge into one progression | Chapter 3 evaluation target |
| Chapter 3 domain examples | Compress to motivation only | Chapter 3, with excess breadth removed if it adds no evidence |
| Chapter 3 evaluation implications | Consolidate | End of Chapter 3 and criteria in Chapter 5 |
| Chapter 4 mechanism explanations | Keep and reorganise by predicted trace | Chapter 4 |
| Chapter 4 GLoRa interpretation | Move | Chapter 6 diagnostics and Chapter 7 RQ 3 answer |
| Chapter 5 depth, rewiring, and transformer methods | Move and compare by addressed mechanism | Chapter 4 |
| Chapter 5 real and synthetic benchmark review | Keep and reorganise by validity criterion | Chapter 5 |
| Chapter 5 synthesis | Rewrite as an explicit unmet-requirements handoff | End of Chapter 5 |
| Chapter 6 repeated motivation and path-aware definition | Remove or reduce to short callbacks | Chapters 3 and 5 own the concepts; Chapter 6 applies them |
| Chapter 6 design, guarantees, protocol, and findings | Keep, verify, and reorder | Chapter 6 threat-to-evidence sequence |
| Chapter 7 summary of mechanisms and generator | Replace with references back | Chapter 7 direct RQ answers |
| Chapter 7 limitations and future directions | Keep, pair, and sharpen | Chapter 7 evidence boundaries and next steps |

No substantive paragraph will be deleted until its claim, citation, and role have either been assigned to a destination or explicitly marked as duplicate in the migration matrix.

## 8. Figure and Front-Matter Design

The current absence of figures weakens the reader's ability to retain the thesis's central distinction and main result.
The revision should add two or three evidence-bearing figures, preferably adapted from Paper I with accurate attribution rather than redrawn from memory.

1. **Running path-aware example, Chapters 1 and 3.** A positive/negative or intervention-based example showing the intended path, the target node, relevant distant information, and why a shortcut is insufficient.
2. **Main performance result, Chapter 6.** Accuracy against dependency length for the evaluated systems, adapted directly from Paper I with the tested setting visible in the caption.
3. **Optional diagnostic synthesis, Chapter 6.** Include only if the paper provides a figure or the underlying data support an accurate compact comparison of predicted and observed traces.

A separate locality schematic in Chapter 2 will be added only if the running example cannot also explain receptive-field growth.
Decorative figures and unsupported reconstructed plots are out of scope.

Once figures are included, `main.tex` will contain a list of figures and a list of tables in the front matter.
An author-contribution statement will be added only from verified authorship information; no role will be inferred.

## 9. Paragraph Migration Rules

Every existing paragraph will receive one of five actions:

- **KEEP:** already in the right chapter and serving a unique function;
- **MOVE:** correct content, wrong chapter;
- **MERGE:** overlaps another paragraph and should become one stronger unit;
- **DELETE AS REPETITION:** makes no unique claim after migration;
- **ADD:** genuinely missing material required by the RQ and chapter contracts.

Each matrix entry will record current file and section, paragraph identifier, main claim, citations or equations, action, destination, reason, and completion status.
The main agent owns this matrix and the initial structural skeleton.
Subagents may improve paragraph logic and prose after migration, but they may not change chapter ownership, RQ wording, technical claims, or evidence boundaries without returning the issue to the main agent.

## 10. Agent Coordination

The structural skeleton and cross-file migration must be sequential because they determine all later ownership.
After that skeleton is stable, chapter work can be distributed to disjoint subagents.

- **Main agent:** baseline manifest, RQs, chapter contracts, migration matrix, physical content moves, cross-chapter integration, compilation, and publication.
- **Chapter agents:** one owner per final chapter file, or per non-overlapping section when a chapter needs more than one specialist; each reviews every paragraph against its assigned function and uses the `plain-technical-prose` standard.
- **Front-matter agent:** English and Norwegian abstract alignment, lists, paper metadata, and verified contribution statement.
- **Architecture reviewer:** checks RQ closure, chapter responsibility, cumulative argument, and comparison with the structural strengths of the reference thesis.
- **Technical-preservation reviewer:** checks claims, values, equations, notation, citations, labels, and fidelity to Paper I.

Chapter agents will work only on disjoint files after all cross-file moves are complete.
Chapter 7 will be drafted after Chapters 1--6 are stable because it must answer the final form of the argument, not a preliminary outline.
All agents must treat GLoRa as the thesis's one included paper, not as one item in a multi-paper portfolio.

## 11. Hard Constraints

- Preserve all supported technical claims and qualifications.
- Preserve citation keys, labels, equations, table content, and numerical values unless a verified structural reason requires a documented change.
- Do not alter the included Paper I PDF.
- Do not introduce a new scientific result or causal explanation.
- Preserve the distinction between exact witness-path length and the implemented generator parameter.
- Preserve Properties (P1)--(P3), feature ranges, chain bounds, splits, protocols, and diagnostic qualifications from Paper I.
- Use British English and the established notation guide.
- Keep one sentence per LaTeX source line.
- Do not polish a paragraph merely to produce a visible diff.
- Do not publish until structural, technical, and LaTeX verification all pass.

## 12. Acceptance Criteria

The revision is complete only when:

- the English and Norwegian abstracts satisfy the same five-part contract;
- every RQ has a named evidence source, contribution, chapter path, and direct answer in Chapter 7;
- every chapter satisfies its stated responsibility without taking over another chapter's role;
- the migration matrix accounts for every original section and all substantive paragraphs;
- the mechanism and diagnostic taxonomy has been checked against verified primary literature through July 2026;
- repeated explanations of shortcuts, expressibility, failure diagnostics, and GLoRa construction have one primary home;
- at least the running example and main empirical result appear as legible, attributed figures;
- all existing citations, labels, equations, tables, numerical claims, and the included paper are preserved or any intentional difference is documented and verified;
- two clean `latexmk` passes complete and references are stable;
- the independent architecture and technical-preservation reviews report no unresolved blocking issue;
- the same final commit is pushed to Overleaf `origin/main` and GitHub `github/thesis-overleaf`.
