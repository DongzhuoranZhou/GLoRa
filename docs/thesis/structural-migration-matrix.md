# Thesis Structural Migration Matrix

## Purpose and Source Identifiers

This matrix accounts for the structural disposition of every paragraph block in the baseline kappa before prose revision.
The machine-generated inventory at `artifacts/structural-revision/baseline/paragraph-inventory.tsv` records each block's stable identifier, source file, source lines, and opening content.
This document assigns the structural action, destination, reason, and preservation constraints.

Actions have the meanings fixed in the approved design:

- `KEEP`: retain in the current chapter because it has a unique local function;
- `MOVE`: transfer intact to the named chapter responsibility before editing;
- `MERGE`: combine with the named retained paragraph while preserving unique claims and citations;
- `DELETE AS REPETITION`: remove only after confirming that the named destination carries the same substantive claim;
- `ADD/REWRITE`: replace the block because the approved structure requires a different function;
- `STRUCTURE`: preserve or revise a LaTeX structural command rather than treating it as prose.

`KEEP` describes content allocation, not permission to skip the later paragraph-level clarity pass.
No `DELETE AS REPETITION` action is complete until the retained destination has passed citation and claim comparison.

The thesis contains one included paper: GLoRa.
All contribution and evidence mappings in this matrix therefore use the form `RQ -> kappa chapter -> GLoRa definition, construction, experiment, or diagnostic`, never a multi-paper portfolio map.

## Frozen Final Section Skeleton and Ownership

The following section skeleton is the binding structure for prose revision.
Each chapter writer owns exactly one final chapter file and may read, but not edit, material assigned to another writer.
Material that changes chapter is incorporated by the destination writer and removed by the source-file writer according to the paragraph actions below.
This keeps cross-file migration and prose revision in one traceable pass while preserving disjoint write ownership.

### Chapter 1: Introduction

1. `Long-Range Graph Learning as an Evaluation Problem`
2. `Scope and Research Questions`
3. `Contributions and Paper I`
4. `Research Questions, Chapters, and Evidence`
5. `Thesis Structure`

### Chapter 2: Technical Foundations

1. `Graphs, Features, and Learning Tasks`
2. `Message-Passing Graph Neural Networks`
3. `Locality and Receptive Fields`
4. `Symmetry and Expressivity`
5. `From Reachability to Use`

### Chapter 3: Long-Range Dependency as an Evaluation Target

1. `From Distant Information to Demonstrated Dependence`
2. `Path-Aware Dependencies`
3. `Distance and Dependency Length`
4. `Scope of the Definition`
5. `Access Is Not Demonstrated Use`
6. `Evaluation Contract`

### Chapter 4: Why Long-Range Learning Fails and How Models Address It

1. `Evidence for a Failure Explanation`
2. `Over-Smoothing`
3. `Over-Squashing`
4. `Optimisation and Vanishing Gradients`
5. `Interactions Among the Mechanisms`
6. `From Candidate Mechanisms to Diagnostic Tests`

Within each of Sections 2--4, the order is definition, predicted trace, model-response families, what an intervention can establish, and remaining uncertainty.
GLoRa's observed diagnostic outcomes do not appear in this chapter.

### Chapter 5: Evaluating Long-Range Graph Learning

1. `What Benchmark Evidence Must Establish`
2. `Real-World and Synthetic Evidence`
3. `Specified Dependencies and Controlled Length`
4. `Shortcut Resistance`
5. `Target Expressibility and Fair Comparison`
6. `Existing Benchmark Families Under the Evaluation Criteria`
7. `Requirements Left Open`

### Chapter 6: The GLoRa Contribution

1. `From Evaluation Threats to Design Requirements`
2. `Task and Construction`
3. `Guarantees and Controls`
4. `Experimental Evidence`
5. `Diagnostic Evidence`
   - `Over-Smoothing`
   - `Over-Squashing`
   - `Vanishing Gradients`
6. `Answers Contributed to RQ 2 and RQ 3`
7. `Paper Contribution and Thesis Synthesis`

The internal logic is `threat -> design response -> guarantee or control -> evidence -> bounded interpretation`.
Exact witness-path length remains distinct from the generator parameter throughout.

### Chapter 7: Discussion and Conclusion

1. `Answer to Research Question 1`
2. `Answer to Research Question 2`
3. `Answer to Research Question 3`
4. `Cumulative Contribution`
5. `Significance for Evaluation Practice`
6. `Limitations`
7. `Future Work`
8. `Conclusion`

Chapter 7 is revised only after Chapters 1--6 have passed their chapter-level reviews.

## Front Matter (`FM-P001`--`FM-P024`)

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `FM-P001`--`FM-P005` | `STRUCTURE` | `main.tex` preamble and title | Preserve document class, packages, metadata, title, author, and title-page fields. |
| `FM-P006` | `ADD/REWRITE` | English abstract: context and evaluation gap | State the local-message-passing problem and why accuracy alone does not identify learned dependence or failure mechanism. |
| `FM-P007`--`FM-P008` | `KEEP` | English abstract: method and evidence | Preserve GLoRa's task type, dependency-length parameterisation, performance trend, and diagnostic qualification. |
| `FM-P009` | `ADD/REWRITE` | English abstract: significance and boundary | Replace the general shortcut warning with a bounded statement of the standard of evidence and synthetic scope. |
| `FM-P010` | `ADD/REWRITE` | Norwegian abstract: context and evaluation gap | Match the English factual content without strengthening it. |
| `FM-P011` | `KEEP` | Norwegian abstract: method | Preserve the controlled node-classification and intended-dependency claims. |
| `FM-P012` | `ADD/REWRITE` | Norwegian abstract: evidence, significance, and boundary | Remove the chapter/literature tour; add the performance decline and bounded diagnostic result omitted by the baseline. |
| `FM-P013`--`FM-P014` | `KEEP` | Preface | Preserve acknowledgements and article-based format. |
| `FM-P015`--`FM-P016` | `STRUCTURE` | Front-matter lists | Preserve the table of contents and paper-list heading; add lists of figures and tables after the final figure inventory is fixed. |
| `FM-P017` | `KEEP` | List of Papers | Preserve Paper I authors, title, venue, and year exactly. |
| `FM-P018`--`FM-P024` | `STRUCTURE` | Main matter, back matter, bibliography, and Paper I | Preserve chapter input order until the skeleton task, all paper metadata, and the included PDF command. |

## Chapter 1 (`C1-P001`--`C1-P066`)

### Opening and Motivation

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C1-P001` | `STRUCTURE` | Chapter title | Retain *Introduction*. |
| `C1-P002` | `KEEP` | Chapter opening | Retain the local-computation versus distant-information problem. |
| `C1-P003` | `MERGE` | `C1-P010` | Consolidate the graph-learning motivation rather than previewing all later topics. |
| `C1-P004` | `MERGE` | `C1-P005` | Preserve `\cite{scarselli2008graph}` while shortening the architectural history. |
| `C1-P005` | `KEEP` | Opening problem statement | Retain the graph-structured input and prediction setting. |
| `C1-P006` | `MERGE` | `C1-P030` | Move the evaluation ambiguity to the evaluation-gap argument. |
| `C1-P007` | `ADD/REWRITE` | Bounded thesis preview | Preview the thesis contribution without giving Chapter 6's empirical detail. |
| `C1-P008` | `DELETE AS REPETITION` | Final Chapter 1 outline | The formal outline later in the chapter owns the chapter sequence. |
| `C1-P009` | `STRUCTURE` | Motivation section | Keep only if the final section hierarchy needs a distinct general motivation section. |
| `C1-P010`--`C1-P011` | `KEEP` | Importance and task breadth | Retain as the main graph-learning motivation. |
| `C1-P012` | `MERGE` | `C1-P010` | Compress repeated motivation. |
| `C1-P013` | `DELETE AS REPETITION` | Chapters 2 and 4 | Architecture background has a technical and mechanism-oriented home later. |
| `C1-P014` | `MERGE` | `C1-P011` | Preserve every application citation; these citations are at unique risk during compression. |
| `C1-P015` | `KEEP` | Transition to long-range dependence | Retain the reason distance matters across applications. |

### Long-Range Problem and Running Example

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C1-P016` | `STRUCTURE` | Long-range problem section | Retain or retitle to serve the motivating problem rather than the formal definition. |
| `C1-P017` | `KEEP` | Informal dependency motivation | Formal definition remains in Chapter 3. |
| `C1-P018` | `MERGE` | `C1-P017` | Remove parallel informal definitions. |
| `C1-P019` | `KEEP` | Locality versus required evidence | Retain the immediate problem statement. |
| `C1-P020` | `ADD/REWRITE` | Running positive/negative GLoRa example | Introduce the central visual example in plain language; Chapter 3 later formalises it. |
| `C1-P021` | `KEEP` | Transition from example to evaluation problem | Preserve its argumentative role. |
| `C1-P022` | `STRUCTURE` | Difficulty section | Reduce or retitle as a short statement of candidate explanations. |
| `C1-P023` | `KEEP` | Need for adequate depth and training | Retain as the concise modelling-side challenge. |
| `C1-P024`--`C1-P027` | `DELETE AS REPETITION` | Chapter 4 mechanism sections | The full mechanism definitions and interventions belong in Chapter 4. |
| `C1-P028` | `KEEP` | Accuracy is not a diagnosis | Retain as the one-sentence bridge to the evaluation gap. |

### Evaluation Gap and Scope

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C1-P029` | `STRUCTURE` | Evaluation-gap section | This section becomes the centre of the introduction. |
| `C1-P030`--`C1-P031` | `KEEP` | Model capability versus benchmark evidence | Retain the principal thesis gap. |
| `C1-P032` | `MOVE/MERGE` | Chapter 5, real-world benchmark limitations | Preserve the unique `\cite{tonshoff2023gap}` citation and critique. |
| `C1-P033`--`C1-P034` | `KEEP` | Shortcut and expressibility requirements | State only at motivating depth; Chapter 5 supplies the full criteria. |
| `C1-P035` | `DELETE AS REPETITION` | Chapter 5 synthetic benchmark comparison | Avoid listing benchmark families in the introduction. |
| `C1-P036` | `STRUCTURE` | Thesis response section | Retitle if needed to introduce rather than explain GLoRa. |
| `C1-P037` | `KEEP` | GLoRa as response to the gap | Retain the one-paragraph thesis response. |
| `C1-P038` | `DELETE AS REPETITION` | Chapter 6 construction | Positive/negative construction detail belongs in Chapter 6. |
| `C1-P039` | `KEEP` | Expressibility and evidential purpose | Retain at contribution-preview depth. |
| `C1-P040`--`C1-P041` | `DELETE AS REPETITION` | Chapter 6 protocol and findings | Results appear only after the construction is established. |
| `C1-P042`--`C1-P043` | `KEEP` | Scope and thesis-level significance | Preserve the benchmark-not-leaderboard and bounded-scope claims. |

### Research Questions and Contributions

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C1-P044` | `STRUCTURE` | Research Questions | Preserve the explicit section. |
| `C1-P045`--`C1-P048` | `ADD/REWRITE` | Approved RQ 1--RQ 3 | Replace broad causal wording with the evidence-bounded questions in the design. |
| `C1-P049` | `ADD/REWRITE` | RQ-to-kappa-chapter-to-GLoRa-evidence map | Make the closure path explicit for the sole included paper. |
| `C1-P050` | `STRUCTURE` | Contributions | Preserve the explicit section. |
| `C1-P051` | `KEEP` | Paper anchoring statement | Retain the article-based scope. |
| `C1-P052`--`C1-P055` | `ADD/REWRITE` | Paper I and contributions aligned to RQ 1 and RQ 2 | Preserve paper metadata. Add author role only if independently verified. |
| `C1-P056` | `MERGE` | Revised RQ 2 contribution | Combine shortcut and expressibility controls as one benchmark-validity contribution. |
| `C1-P057`--`C1-P058` | `ADD/REWRITE` | Bounded RQ 3 contribution and scope | Preserve the tested-setting qualification and distinguish exact witness-path length from the generator parameter. |

### Outline

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C1-P059` | `STRUCTURE` | Outline | Preserve the section. |
| `C1-P060`--`C1-P066` | `ADD/REWRITE` | Argumentative chapter handoffs | Describe what each chapter establishes and which RQ it advances, not merely its topic list. |

## Chapter 2 (`C2-P001`--`C2-P074`)

### Foundations and Graph Learning Scope

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C2-P001` | `STRUCTURE` | Rename to *Technical Foundations* | Match the narrowed chapter responsibility. |
| `C2-P002`--`C2-P004` | `KEEP` | Chapter purpose and progression | Retain only claims used later. |
| `C2-P005` | `MERGE` | `C2-P007` | Preserve notation and the neighbourhood equation; do not conflate graph distance, path length, dependency length, and the generator parameter. |
| `C2-P006` | `STRUCTURE` | Graphs and Features | Preserve the section. |
| `C2-P007` | `KEEP` | Graph definition and notation | Preserve exactly in meaning. |
| `C2-P008` | `DELETE AS REPETITION` | Chapters 1 and 3 | Remove repeated motivation. |
| `C2-P009`--`C2-P011` | `KEEP` | Features, directed edges, and neighbourhoods | Preserve definitions. |
| `C2-P012` | `MERGE` | `C2-P011` | Consolidate the neighbourhood convention. |
| `C2-P013` | `KEEP` | Feature and structure distinction | Retain for later path-aware reasoning. |
| `C2-P014` | `STRUCTURE` | Graph Learning Tasks | Preserve the section. |
| `C2-P015`--`C2-P017` | `KEEP` | Node-, graph-, and edge-level tasks | Retain the minimum task taxonomy. |
| `C2-P018`--`C2-P019` | `MERGE` | `C2-P016` | Keep only the scope distinction needed later. |
| `C2-P020` | `MERGE` | `C2-P021` | Consolidate inductive/transductive scope. |
| `C2-P021` | `KEEP` | GLoRa's inductive node-classification scope | Preserve the exact task type. |
| `C2-P022` | `MERGE` | `C2-P021` | Avoid repeating the thesis scope. |

### Message Passing, Locality, and Symmetry

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C2-P023` | `STRUCTURE` | Message-Passing Graph Neural Networks | Preserve the section. |
| `C2-P024` | `KEEP` | Informal message-passing definition | Retain. |
| `C2-P025` | `MERGE` | `C2-P026` | Introduce the formal update without duplicating it. |
| `C2-P026`--`C2-P029` | `KEEP` | Message-passing and classification equations | Move or merge atomically; preserve symbols and mathematical meaning. |
| `C2-P030` | `MERGE` | `C2-P028` | Keep the self-information convention once. |
| `C2-P031` | `STRUCTURE` | Locality and Receptive Fields | Preserve the section. |
| `C2-P032`--`C2-P036` | `KEEP` | Receptive-field progression and access-versus-use distinction | Preserve equations and the core RQ 1 foundation. |
| `C2-P037` | `MOVE/MERGE` | Chapter 3, dependency length as evaluation parameter | The evaluative consequence belongs with the target definition. |
| `C2-P038` | `STRUCTURE` | Permutation Equivariance and Invariance | Preserve only as required by expressivity. |
| `C2-P039`--`C2-P041` | `KEEP` | Equivariance definition and equation | Preserve. |
| `C2-P042` | `MERGE` | `C2-P041` | Preserve the invariance equation while consolidating prose. |
| `C2-P043` | `KEEP` | Symmetry and graph learning | Retain its later expressivity use. |
| `C2-P044` | `MERGE` | `C2-P043` | Consolidate repeated interpretation. |
| `C2-P045` | `KEEP` | Transition to expressivity | Retain if needed after architecture removal. |

### Architecture Material and Expressivity

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C2-P046` | `STRUCTURE` | Remove the standard-architecture section from Chapter 2 | Its content belongs with intervention families in Chapter 4. |
| `C2-P047` | `MOVE` | Chapter 4, intervention families and evidential limits | Retain the family-level orientation. |
| `C2-P048`--`C2-P055` | `DELETE AS REPETITION` | Retained counterparts in current Chapter 5, moved to Chapter 4 | Compare citations before deletion; preserve unique conceptual distinctions. |
| `C2-P056` | `STRUCTURE` | Expressivity | Preserve the section. |
| `C2-P057`--`C2-P062` | `KEEP` | Minimum expressivity foundation | Retain the distinction between representability, learnability, and evaluation. |
| `C2-P063` | `STRUCTURE` | Remove detailed benchmark-validity section from Chapter 2 | Chapter 5 owns the criteria. |
| `C2-P064`--`C2-P068` | `MOVE` | Chapter 5, shortcut functions and target-function expressibility | Preserve all formal and cited claims. |
| `C2-P069` | `MOVE` | Chapter 5, fair comparison and dependency-length control | Retain as a distinct criterion. |
| `C2-P070` | `DELETE AS REPETITION` | Chapter 6 design and expressibility properties | Preserve the exact witness-path versus generator-parameter distinction in Chapter 6. |

### Chapter Handoff

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C2-P071` | `STRUCTURE` | Chapter conclusion or handoff | A short closing section may remain. |
| `C2-P072` | `ADD/REWRITE` | Foundations-to-target handoff | State what Chapter 3 can now define. |
| `C2-P073`--`C2-P074` | `MERGE` | `C2-P072` | Preserve locality, notation, symmetry, and expressivity without previewing all benchmark controls. |

## Unverified Author-Contribution Constraint

The inspected thesis and Paper I establish authorship but not a formal contribution taxonomy.
No author-role statement will be added from inference.
The revision will preserve a marked documentation requirement until a verifiable contribution statement, institutional record, or user-supplied description is available.

## Chapter 3 (`C3-P001`--`C3-P065`)

### Definition and Formalisation

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C3-P001` | `STRUCTURE` | Rename to *Long-Range Dependency as an Evaluation Target* | The title states the chapter's evidential role. |
| `C3-P002` | `STRUCTURE` | Opening definition section | Preserve a staged informal-to-formal progression. |
| `C3-P003` | `ADD/REWRITE` | Evidence-bounded opening definition | Do not define dependency by distance alone. |
| `C3-P004` | `MERGE` | Chapter 2 graph notation, `C2-P005` | Keep the graph definition in one technical home. |
| `C3-P005` | `MERGE` | `C3-P023`--`C3-P024` | Place the distance distinction in its dedicated section. |
| `C3-P006`--`C3-P007` | `KEEP` | Informal target and scope | Retain the distinction between distant information and demonstrated dependence. |
| `C3-P008` | `STRUCTURE` | Informal view | Preserve as the bridge to the running example. |
| `C3-P009` | `ADD/REWRITE` | Running paired or intervention example | Reuse the Chapter 1 figure and explain what changes between the examples. |
| `C3-P010` | `MERGE` | `C3-P049` | Consolidate access-versus-use reasoning. |
| `C3-P011` | `DELETE AS REPETITION` | `C3-P049` and Chapter 4 | Remove repeated architecture and mechanism preview. |
| `C3-P012` | `MERGE` | `C3-P045` | Keep only the minimum cross-domain motivation. |
| `C3-P013` | `STRUCTURE` | Formal path-aware view | Preserve the section. |
| `C3-P014`--`C3-P021` | `KEEP` | Path-aware formalisation | Preserve all three intervention conditions and the qualification that this is one possible formalisation. |

### Distance, Scope, and Evidence

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C3-P022` | `STRUCTURE` | Graph Distance, Path Length, and Dependency Length | Preserve the explicit distinction. |
| `C3-P023`--`C3-P027` | `KEEP` | Distance and length definitions | Keep `G=(V,E,\lambda)` and `p=(v_0,\ldots,v_d)` at their assigned homes and distinguish exact witness length from the generator parameter. |
| `C3-P028` | `MERGE` | `C3-P026` | Consolidate repeated parameter interpretation. |
| `C3-P029` | `STRUCTURE` | Why Path-Aware Dependencies Matter | Preserve the section's evidential role. |
| `C3-P030` | `KEEP` | Path awareness and internal-node sensitivity | Retain. |
| `C3-P031` | `MERGE` | Running example `C3-P009` | Avoid a second example explanation. |
| `C3-P032` | `KEEP` | Need for all intervention conditions | Internal-node sensitivity alone is insufficient. |
| `C3-P033` | `MOVE/MERGE` | Chapter 6, shortcut examples | GLoRa-specific construction belongs with its design response. |
| `C3-P034` | `KEEP` | Evidential implication | Retain at definition level. |
| `C3-P035` | `MERGE` | `C3-P049` | Consolidate access-versus-use interpretation. |
| `C3-P036` | `STRUCTURE` | Node-Level and Graph-Level Dependencies | Preserve the scope section. |
| `C3-P037`--`C3-P041` | `KEEP` | Node- and graph-level distinctions | Preserve that Paper I's formal guarantee concerns inductive binary node classification. |
| `C3-P042` | `MERGE` | `C3-P043` | Consolidate the conceptual graph-level extension. |
| `C3-P043` | `KEEP` | Thesis scope | Retain. |
| `C3-P044` | `STRUCTURE` | Remove standalone domain catalogue | Domain breadth is motivation, not a separate contribution. |
| `C3-P045` | `KEEP` | Compressed domain motivation | Preserve unique citations. |
| `C3-P046`--`C3-P047` | `MERGE` | `C3-P045` | Avoid an applications survey. |

### Access, Dependency Length, and Evaluation Contract

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C3-P048` | `STRUCTURE` | Retitle to *Access Is Not Demonstrated Use* | State the central RQ 1 distinction directly. |
| `C3-P049` | `KEEP` | Reachability versus use | Retain as the primary explanation site. |
| `C3-P050` | `MERGE` | `C3-P049` | Remove restatement. |
| `C3-P051` | `MERGE` | `C3-P054` | Keep benchmark implication once. |
| `C3-P052` | `KEEP` | Correlation versus dependence | Retain. |
| `C3-P053` | `MERGE` | `C3-P052` | Consolidate the distinction. |
| `C3-P054` | `KEEP` | What evidence must establish | Retain. |
| `C3-P055` | `STRUCTURE` | Dependency Length as an Evaluation Parameter | Preserve the section. |
| `C3-P056`--`C3-P057` | `KEEP` | Controlled dependency length | Preserve. |
| `C3-P058` | `ADD/REWRITE` | General parameter interpretation | Remove Chapter 6 construction and result detail. |
| `C3-P059` | `ADD/REWRITE` | Concise evaluation contract | State the criteria that later chapters operationalise. |
| `C3-P060` | `ADD/REWRITE` | Handoff to failure mechanisms | Do not give the GLoRa empirical verdict here. |
| `C3-P061` | `KEEP` | Scope qualification | Retain if not redundant after the contract. |
| `C3-P062` | `STRUCTURE` | Retitle to *Evaluation Contract* | End the chapter with the evidence requirement. |
| `C3-P063`--`C3-P064` | `KEEP` | Consequences for benchmark evidence | Preserve. |
| `C3-P065` | `ADD/REWRITE` | Handoff to Chapters 4--6 | Do not repeat GLoRa construction. |

## Chapter 4 (`C4-P001`--`C4-P051`)

### Mechanism and Evidence Standard

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C4-P001` | `STRUCTURE` | Rename to *Why Long-Range Learning Fails and How Models Address It* | The chapter pairs mechanisms with interventions and evidence limits. |
| `C4-P002` | `MERGE` | `C4-P003` | Consolidate the opening. |
| `C4-P003`--`C4-P004` | `KEEP` | Three candidate mechanisms and trace distinction | Retain as the chapter frame. |
| `C4-P005` | `ADD/REWRITE` | Mechanism, trace, intervention, and limit organisation | Remove GLoRa-specific findings from the opening. |
| `C4-P006` | `STRUCTURE` | What a Candidate Explanation Must Explain | Preserve the evidence-standard section. |
| `C4-P007`--`C4-P009` | `KEEP` | Symptom versus causal explanation | Retain. |
| `C4-P010` | `MOVE/MERGE` | Chapter 6 diagnostic findings | GLoRa's actual diagnostic procedure and verdict belong with its evidence. |

### Over-Smoothing

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C4-P011` | `STRUCTURE` | Over-Smoothing | Preserve the mechanism section. |
| `C4-P012` | `ADD/REWRITE` | General mechanism and predicted trace | Remove the GLoRa-specific question. |
| `C4-P013`--`C4-P016` | `KEEP` | Representation convergence and diagnostic standard | Preserve while updating against verified literature. |
| Current `C5-P019`--`C5-P035` | `MOVE/MERGE` | After `C4-P016` | Compress depth, normalisation, stochastic regularisation, layer selection, residual, and implicit methods by what trace or limitation they address. |
| `C4-P017`--`C4-P018` | `MOVE/MERGE` | Chapter 6 over-smoothing diagnostic | Preserve the tested systems, measurement, and non-collapse qualification. |

### Over-Squashing

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C4-P019` | `STRUCTURE` | Over-Squashing | Preserve the mechanism section. |
| `C4-P020` | `ADD/REWRITE` | General bottleneck mechanism and predicted trace | Remove the GLoRa-specific question and update against verified literature. |
| `C4-P021`--`C4-P024` | `KEEP` | Compression, topology, and distinction from over-smoothing | Preserve, subject to the literature update. |
| Current `C5-P036`--`C5-P053` | `MOVE/MERGE` | After `C4-P024` | Compress diffusion, shortest-path, dynamic, curvature, and spectral methods by mechanism and evidential consequence. |
| `C4-P025`--`C4-P027` | `MOVE/MERGE` | Chapter 6 over-squashing diagnostic | Preserve directedness, bounded additional chains, exact path-count claim, and the undirected-walk caveat. |

### Optimisation and Interaction

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C4-P028` | `STRUCTURE` | Optimisation and Vanishing Gradients | Preserve the section with appropriately bounded terminology. |
| `C4-P029` | `ADD/REWRITE` | General optimisation mechanism and trace | Remove the GLoRa-specific question. |
| `C4-P030`--`C4-P032` | `KEEP` | Backward signal and diagnostic standard | Preserve. |
| `C4-P033`--`C4-P034` | `MOVE/MERGE` | Chapter 6 gradient diagnostic | Preserve which layers, weights, and epochs were inspected. |
| `C4-P035` | `ADD/REWRITE` | General diagnostic limitation | Nonzero weight gradients need not be useful gradients. |
| `C4-P036` | `STRUCTURE` | How the Explanations Interact | Preserve after the separate mechanisms. |
| `C4-P037` | `ADD/REWRITE` | General interaction statement | Remove GLoRa interpretation. |
| `C4-P038`--`C4-P039` | `KEEP` | Mechanism interactions | Retain. |
| Current `C5-P055`--`C5-P068` | `MOVE/MERGE` | After `C4-P041` | Place global attention and structural encodings as responses to visibility and structural-use limits, not as proof of a named mechanism. |
| `C4-P040` | `ADD/REWRITE` | Intervention interaction | Leave the gated-system empirical observation in Chapter 6. |
| `C4-P041` | `ADD/REWRITE` | Causal-identification warning | An intervention gain may reflect depth, optimisation, connectivity, or shorter effective dependency length. |

### Diagnostic Limits and Synthesis

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C4-P042` | `STRUCTURE` | What the Diagnostics Leave Open | Preserve the limitations section. |
| `C4-P043`--`C4-P044` | `KEEP` | Mechanism-specific evidence requirements | Retain. |
| `C4-P045` | `MOVE/MERGE` | Chapter 6 diagnostic findings | Keep the actual GLoRa measurements out of the general chapter. |
| `C4-P046` | `KEEP` | No diagnosis from accuracy alone | Retain once. |
| `C4-P047` | `STRUCTURE` | Retitle to *Synthesis: Mechanisms, Traces, and Interventions* | Replace the GLoRa-centred ending. |
| `C4-P048` | `MOVE/MERGE` | Chapter 6 diagnostic interpretation | Preserve the tested-setting qualification. |
| `C4-P049` | `MERGE` | `C4-P043` | Consolidate the general diagnostic principle. |
| `C4-P050` | `MOVE/MERGE` | Chapter 6 thesis-level interpretation | Preserve the bounded empirical conclusion. |
| `C4-P051` | `ADD/REWRITE` | Synthesis table and Chapter 5 handoff | Relate mechanism, predicted trace, intervention, what success shows, and what remains unproven. |

## Chapter 4 Claims at Particular Risk

- The over-squashing conclusion must remain limited to the bounded directed-path account inspected by Paper I.
- Directedness, at most ten additional chains, and the undirected-walk caveat are necessary to that conclusion.
- Non-collapsed final representations do not identify the true mechanism or rule out every over-smoothing measure.
- Nonzero inspected weight gradients do not prove that useful gradients reach all required parameters.
- Better performance from a mechanism-motivated intervention does not establish that the named mechanism caused the baseline failure.
- Every GLoRa diagnostic claim remains bounded to the inspected systems, layers, measurements, and directed construction.

## Chapter 5 (`C5-P001`--`C5-P101`)

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C5-P001` | `STRUCTURE` | Rename to *Evaluating Long-Range Graph Learning* | Chapter 5 owns benchmark validity rather than all state of the art. |
| `C5-P002` | `ADD/REWRITE` | Opening validity criteria | Introduce specified dependence, controlled length, shortcut resistance, expressibility, class fairness, system fairness, and diagnostic interpretability. |
| `C5-P003` | `MERGE` | Chapter 4 opening, `C4-P004` | Preserve the mechanism citations. |
| `C5-P004`, `C5-P006` | `STRUCTURE` | Chapter 4 architecture headings | Remove architecture ownership from Chapter 5. |
| `C5-P005` | `MERGE` | Chapter 4 opening, `C4-P002` | Preserve the family-level orientation. |
| `C5-P007`--`C5-P017` | `MOVE` | Chapter 4 after `C4-P004` | Move standard GNN descriptions and `tab:sota-standard-gnns` atomically. |
| `C5-P018` | `MERGE` | Chapter 4, `C4-P003` | Consolidate modelling-versus-evaluation framing. |
| `C5-P019` | `STRUCTURE` | Chapter 4 over-smoothing heading | Remove from Chapter 5. |
| `C5-P020`--`C5-P034` | `MOVE` | Chapter 4 after `C4-P016` | Move depth methods and `tab:sota-oversmoothing` atomically. |
| `C5-P035` | `ADD/REWRITE` | Chapter 4 intervention synthesis | Keep the empirical verdict only in Chapter 6. |
| `C5-P036` | `STRUCTURE` | Chapter 4 over-squashing heading | Remove from Chapter 5. |
| `C5-P037`--`C5-P053` | `MOVE` | Chapter 4 after `C4-P024` | Move rewiring families and `tab:sota-rewiring` atomically. |
| `C5-P054` | `MOVE/MERGE` | Chapter 6 over-squashing diagnostic, `C6-P054`--`C6-P055` | Preserve the bounded directed-path and directedness qualifications. |
| `C5-P055` | `STRUCTURE` | Chapter 4 global-attention heading | Remove from Chapter 5. |
| `C5-P056`--`C5-P068` | `MOVE` | Chapter 4 after the rewiring material | Move graph transformers, encodings, and `tab:sota-transformers` atomically. |
| `C5-P069` | `MOVE/MERGE` | Chapter 6 main evidence, `C6-P046` | Keep the GLoRa result with GLoRa evidence. |
| `C5-P070` | `STRUCTURE` | Real-World Graph Benchmarks | Preserve the benchmark section. |
| `C5-P071`--`C5-P077` | `KEEP` | Real-world benchmark comparison | Preserve `tab:sota-real-benchmarks` and all citations. |
| `C5-P078` | `STRUCTURE` | Synthetic Long-Range Benchmarks | Preserve the section. |
| `C5-P079` | `KEEP` | Role of synthetic control | Retain. |
| `C5-P080` | `ADD/REWRITE` | Shortcut and expressibility criterion | State the criterion without pre-empting GLoRa's response. |
| `C5-P081` | `STRUCTURE` | Chain and transfer benchmarks | Preserve the subsection. |
| `C5-P082`--`C5-P085` | `KEEP` | Chain and transfer comparison | Preserve attribution of shortcut critiques to GLoRa. |
| `C5-P086` | `STRUCTURE` | Tree and proximity benchmarks | Preserve the subsection. |
| `C5-P087`--`C5-P090` | `KEEP` | Tree and proximity comparison | Preserve citations and qualifications. |
| `C5-P091` | `STRUCTURE` | Connectivity benchmarks | Preserve the subsection. |
| `C5-P092`--`C5-P095` | `KEEP` | Connectivity and synthetic benchmark comparison | Preserve `tab:sota-synthetic-benchmarks` and attribution. |
| `C5-P096` | `STRUCTURE` | Retitle as *Unmet Evaluation Requirements* | End with a direct handoff to Chapter 6. |
| `C5-P097`--`C5-P098` | `ADD/REWRITE` | Benchmark-only synthesis | Remove architecture-family conclusions. |
| `C5-P099` | `DELETE AS REPETITION` | Chapter 6 Properties (P1)--(P3) | Do not explain GLoRa's guarantees before Chapter 6. |
| `C5-P100` | `KEEP` | Controlled evaluation gap | Retain. |
| `C5-P101` | `ADD/REWRITE` | Explicit unmet-requirements list | Name path necessity, shortcut resistance, expressibility, separate fairness notions, and controlled dependency length. |

## Chapter 6 (`C6-P001`--`C6-P064`)

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C6-P001` | `STRUCTURE` | The GLoRa Contribution | Retain the title and label. |
| `C6-P002` | `KEEP` | Thesis-level opening | Retain. |
| `C6-P003` | `ADD/REWRITE` | Threat-to-evidence roadmap | Organise the single included paper as threat, design, guarantee, evidence, and interpretation. |
| `C6-P004` | `STRUCTURE` | Retitle as *Evaluation Threats and Design Goals* | Inherit the Chapter 5 gap explicitly. |
| `C6-P005` | `DELETE AS REPETITION` | Chapter 4 mechanism frame | Keep mechanisms out of the design motivation. |
| `C6-P006` | `ADD/REWRITE` | Short Chapter 5 callback | State the unmet benchmark requirements once. |
| `C6-P007` | `DELETE AS REPETITION` | Chapter 5 real-world benchmark limits | Avoid a second benchmark review. |
| `C6-P008` | `MERGE` | `C6-P017` | Place the controlled-generation response with the design. |
| `C6-P009` | `ADD/REWRITE` | Inherited design goals | Do not equate generator parameter and exact witness-path length. |
| `C6-P010` | `STRUCTURE` | Collapse path-aware notation into a short callback | Chapter 3 owns the full definition. |
| `C6-P011` | `KEEP` | Minimal path-aware callback | Retain only notation needed for the construction. |
| `C6-P012`--`C6-P014` | `DELETE AS REPETITION` | Chapter 3 formalisation | Remove the repeated graph, path, and intervention definitions. |
| `C6-P015` | `MERGE` | Guarantee statement `C6-P034` | Preserve the approximate-`\delta` qualification. |
| `C6-P016` | `STRUCTURE` | Benchmark Design | Preserve or retitle as the construction section. |
| `C6-P017`--`C6-P018` | `KEEP` | Basic construction | Retain. |
| `C6-P019` | `ADD/REWRITE` | Exact chain bounds and length distinction | Restore rounded `2d/3`-to-`d` chain bounds and distinguish witnesses from generator parameter. |
| `C6-P020`--`C6-P023` | `KEEP` | Holes, additional chains, feature controls, and fairness design | Preserve values and construction details. |
| `C6-P024` | `STRUCTURE` | Fold shortcut examples into the design threats | Avoid a detached second motivation section. |
| `C6-P025`--`C6-P026` | `MERGE` | `C6-P020` | Preserve global-readout, virtual-node, and preprocessing shortcut concerns. |
| `C6-P027` | `MERGE` | `C6-P022` | Place hole-count control with the construction. |
| `C6-P028` | `DELETE AS REPETITION` | Chapter 5 benchmark comparison | Avoid repeating benchmark-by-benchmark critiques. |
| `C6-P029` | `ADD/REWRITE` | Construction versus guarantee distinction | Construction motivates necessity; Property (P1) supplies the guarantee. |
| `C6-P030` | `STRUCTURE` | Retitle as *Formal Guarantees* | Group Properties (P1)--(P3) and theorem qualifications. |
| `C6-P031` | `MERGE` | `C6-P032` | Consolidate the guarantee introduction. |
| `C6-P032`--`C6-P033` | `KEEP` | Properties (P1)--(P3) and expressibility | Preserve exact meaning. |
| `C6-P034` | `ADD/REWRITE` | Theorem 1 quantifiers | Preserve `\forall\delta>0`, `\forall P\in(0,1)`, `\exists K`, sufficient examples, precision/probability, and balanced sampling. |
| `C6-P035` | `KEEP` | Fairness and expressibility interpretation | Keep class-distribution fairness distinct from common-protocol system fairness. |
| `C6-P036` | `STRUCTURE` | Experimental Protocol | Preserve a concise interpretation-focused protocol. |
| `C6-P037`--`C6-P041` | `KEEP` | Protocol | Preserve `d=3,\ldots,15`, 5000 examples per class, 80:10:10, five runs, 300 epochs, `d+2` layers, batch size 32, and the 0.8 threshold. |
| `C6-P042` | `STRUCTURE` | Main Findings | Preserve the section. |
| `C6-P043`--`C6-P047` | `KEEP` | Main performance evidence | Report the observed limits as protocol-bound results. |
| `C6-P048` | `ADD/REWRITE` | Bounded interpretation | Restore Property (P1)'s precision and probability qualifications. |
| `C6-P049`, `C6-P051`, `C6-P053`, `C6-P056` | `STRUCTURE` | Diagnostic findings and three mechanism subsections | Preserve the hierarchy. |
| `C6-P050`, `C6-P052` | `ADD/REWRITE` | Over-smoothing diagnostic | Report only the one-dimensional final target representation measurement at `d=6` and `d=13`; do not claim it rules out all over-smoothing. |
| `C6-P054`--`C6-P055` | `KEEP` | Over-squashing diagnostic | Limit the conclusion to the tested directed many-path account. |
| `C6-P057`--`C6-P058` | `KEEP` | Gradient diagnostic | State that measured weight gradients remain nonzero without claiming useful optimisation direction. |
| `C6-P059` | `STRUCTURE` | Retitle as explicit RQ 2 and RQ 3 closure | State the single paper's thesis-level evidence. |
| `C6-P060` | `KEEP` | Thesis-level benchmark contribution | Retain. |
| `C6-P061` | `MERGE` | `C6-P048` | Consolidate evidence qualification. |
| `C6-P062` | `ADD/REWRITE` | Direct empirical answer | State the performance trend under the reported protocol. |
| `C6-P063` | `ADD/REWRITE` | Bounded diagnostic answer | Separate what each measurement does and does not support. |
| `C6-P064` | `MERGE` | `C6-P060` | End with one thesis-level interpretation. |

## Chapter 6 Claims at Particular Risk

- Property (P2) is expressibility, not learnability.
- Property (P3)'s class-distribution fairness is distinct from common-protocol fairness across systems.
- Preserve feature range `[-12,-2]\cup[3,13]`, binary markers, rounded chain bounds, and five to ten additional chains.
- “Most systems drop before `d=9`” and “stronger systems perform poorly after `d=11`” are protocol-bound observations, not universal limits.
- Existing-benchmark shortcut and inexpressibility analyses remain attributed to GLoRa rather than presented as uncontested general facts.
- Move all tables together with their captions, labels, and citations.
- Do not infer an author-contribution statement without verified evidence.

## Chapter 7 (`C7-P001`--`C7-P028`)

| Paragraphs | Action | Destination or retained content | Reason and preservation constraint |
|---|---|---|---|
| `C7-P001` | `STRUCTURE` | Discussion and Conclusion | Retain the chapter title and label. |
| `C7-P002` | `DELETE AS REPETITION` | Chapters 1 and 6 | Transfer its GLoRa citation to the direct RQ 2 answer. |
| `C7-P003` | `STRUCTURE` | Replace Summary with explicit RQ-answer section | The chapter must close the Chapter 1 contract. |
| `C7-P004` | `ADD/REWRITE` | Direct bounded answer to RQ 1 | Distinguish access from demonstrated use and graph distance/path length from dependency length. Move mechanism citations to RQ 3. |
| `C7-P005` | `ADD/REWRITE` | Direct bounded answer to RQ 2 | Organise the answer as evaluation threats, required controls, and supported conclusion. |
| `C7-P006` | `DELETE AS REPETITION` | Chapter 6 construction | Do not re-explain path notation, labels, chains, or holes. Preserve only guarantees and parameter qualifications in RQ 2. |
| `C7-P007` | `MERGE` | RQ 2 answer | Preserve `\cite{barcelo2020logical,zhou2025glora}` and distinguish expressibility from learnability. |
| `C7-P008` | `ADD/REWRITE` | Direct bounded answer to RQ 3 | State the performance trend, exact diagnostic evidence, and non-causal conclusion. |
| `C7-P009` | `STRUCTURE` | Retitle to *Cumulative Contribution and Significance* | Place synthesis after the direct RQ answers. |
| `C7-P010`--`C7-P012` | `KEEP` | Change to evaluation practice and complementary evidence | Retain. |
| `C7-P013` | `MERGE` | `C7-P010` | Keep the predicted-trace principle once; leave empirical verdict in RQ 3. |
| `C7-P014` | `STRUCTURE` | Limitations | Preserve the section. |
| `C7-P015` | `KEEP` | Synthetic control limitation | Retain. |
| `C7-P016` | `KEEP` | Dependency-family limitation | Retain. |
| `C7-P017` | `KEEP` | Feature-simplicity limitation | Retain. |
| `C7-P018` | `KEEP` | Empirical-scope limitation | Retain. |
| `C7-P019` | `KEEP` | Causal-incompleteness limitation | Retain and align with narrowed diagnostics. |
| `C7-P020` | `STRUCTURE` | Future Directions | Preserve the section. |
| `C7-P023` | `MOVE` | First future direction | Pair with the synthetic-control limitation. |
| `C7-P021` | `KEEP` | Second future direction | Pair with the dependency-family limitation. |
| `C7-P022` | `KEEP` | Third future direction | Pair with the feature-simplicity limitation. |
| `C7-P024` | `KEEP` | Fourth future direction | Pair with empirical scope. |
| `C7-P025` | `KEEP` | Fifth future direction | Pair with causal incompleteness. |
| `C7-P026` | `MERGE` | `C7-P024` | Retain gating as a broader-evaluation hypothesis, not a causal conclusion. |
| `C7-P027` | `STRUCTURE` | Concluding Remarks | Preserve the heading. |
| `C7-P028` | `KEEP` | Bounded cumulative conclusion | Retain as the final claim after vocabulary alignment. |

## Matrix Coverage

The baseline inventory contains 473 paragraph blocks:

- front matter: 24;
- Chapter 1: 66;
- Chapter 2: 74;
- Chapter 3: 65;
- Chapter 4: 51;
- Chapter 5: 101;
- Chapter 6: 64;
- Chapter 7: 28.

The tables above assign every block to a structural action.
The literature memo has passed independent citation review.
All cross-file moves and chapter rewrites were completed against the frozen section skeleton and citation keys, then passed chapter-level and thesis-level review on 2026-07-16.
