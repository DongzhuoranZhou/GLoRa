# Thesis Rewrite Review: Sol Second Pass

## Scope and Baseline

This review covers `main.tex`, all seven files under `chapters/`, the notation guide, and the included GLoRa paper.
The baseline is commit `a15da39`, which was produced by GPT-5.5 with the `plain-technical-prose` skill.
The baseline compiles and already removes the most obvious generated-writing patterns.
The Sol pass should therefore improve argument and paragraph function rather than rewrite merely to create a larger diff.

## Overall Assessment

The thesis has a coherent central claim: long-range graph learning is both a modelling problem and an evaluation problem.
The chapter order supports that claim, and the technical content is generally careful.
The strongest parts are the distinction between access and use, the path-aware account of dependency length, the separation of symptoms from diagnoses, and the controlled interpretation of GLoRa.

The remaining weakness is cumulative repetition.
The same claim about benchmark scores, shortcut functions, and expressibility appears in Chapters 1, 2, 3, 5, 6, and 7 with only small changes in purpose.
Each occurrence is defensible in isolation, but together they reduce momentum.
The second pass should keep the claim where it advances the argument and shorten it where it only reminds the reader.

## Priority Findings

### 1. Give repeated claims a chapter-specific job

The benchmark claim should evolve across the thesis.
Chapter 1 should motivate it, Chapter 2 should connect it to model expressivity, Chapter 3 should define the dependency being certified, Chapter 5 should use it as a criterion for comparing prior work, Chapter 6 should show how the construction satisfies it, and Chapter 7 should state the resulting contribution and limits.
Paragraphs that only repeat the general claim should be compressed or redirected to the chapter's local question.

### 2. Reduce front-loaded GLoRa framing

Several early sections explain their topic through GLoRa before establishing the topic in its own right.
This keeps the thesis focused, but it can make background chapters read as commentary on one paper rather than a scholarly account of the research problem.
Open with the concept or scientific issue, then connect it to GLoRa once the reader knows what is at stake.

### 3. Tighten the diagnostic chapter around predicted traces

Chapter 4 has the right organizing idea: an explanation should predict an internal trace.
The chapter nevertheless repeats after each phenomenon that low accuracy alone is not a diagnosis and that the phenomenon remains relevant in general.
Keep the qualification, but state it once at full length and let later sections concentrate on the distinct trace: representation convergence, structural compression, or weak backward signal.

### 4. Turn the state of the art from a catalogue into an argument

Chapter 5 is comprehensive and well sourced, but many subsections still follow the same sequence: mechanism, possible benefit, and a final sentence saying that the method does not certify the intended dependency.
The Sol pass should give each family a distinct conclusion.
Standard GNNs establish local reach, depth methods establish usable depth, rewiring changes graph semantics, transformers separate visibility from structural use, real benchmarks establish practical utility, and synthetic benchmarks establish control only when shortcuts and expressibility are handled.
The tables should carry compact mechanism summaries so that the body can compare assumptions and evidence.

### 5. Remove duplication inside the GLoRa chapter

Chapter 6 repeats the benchmark motivation in its opening, Motivation, Why Expressibility Matters, and Thesis-Level Interpretation sections.
The chapter should read as a construction in which every design choice answers a named threat to interpretation.
Keep all formal properties, parameters, protocol details, results, and qualifications, but shorten repeated statements of the general problem.

### 6. Separate the functions of the final chapter

In Chapter 7, Summary should state what was established, Significance should explain why that changes evaluation practice, Limitations should bound the evidence, Future Directions should follow directly from those bounds, and Concluding Remarks should close without restating the entire abstract.
The five existing limitations must remain distinct.

### 7. Preserve narrow technical claims

The included paper supports the following precise empirical statements: most systems drop before $d=9$, even the stronger systems perform poorly after $d=11$, and the tested diagnostics do not support the three standard explanations in the reported setting.
Do not strengthen these into universal claims.
Preserve the distinction between exact witness-path length and the implemented generator parameter $d$.
Preserve Properties (P1)--(P3), the directedness qualification, and the bounded number of additional chains.

## File-Specific Rewrite Direction

`main.tex`: sharpen the English abstract by separating problem, method, result, and significance.
Edit the Norwegian abstract only when the change is clearly safe.

`chapters/chapter01-introduction.tex`: reduce early repetition and make the research questions arise directly from the unresolved modelling, evaluation, and diagnostic problems.

`chapters/chapter02-graph-learning-message-passing.tex`: keep the formalism stable and improve the progression from local computation to receptive fields, symmetry, expressivity, and benchmark validity.

`chapters/chapter03-long-range-dependencies.tex`: make the informal, formal, and evaluative meanings of dependency length cumulative rather than parallel restatements.

`chapters/chapter04-failure-explanations.tex`: organize each mechanism around its predicted trace and consolidate generic caveats.

`chapters/chapter05-state-of-the-art.tex`: preserve every method and citation while replacing repeated evaluative endings with family-specific synthesis.

`chapters/chapter06-glora-contribution.tex`: make the generator read as a sequence of design responses to shortcut, fairness, expressibility, and diagnostic threats.

`chapters/chapter07-discussion-conclusion.tex`: separate established findings, significance, limits, research directions, and final conclusion.

## Hard Constraints

- Preserve LaTeX commands, citation keys, labels, equations, notation, experimental values, and technical claims.
- Do not add citations or scientific claims that are not supported by the included paper or existing references.
- Use British English where natural.
- Keep one sentence per source line.
- Use one term per referent, following `notes/notation-and-terminology.md`.
- Do not edit the included paper PDF.
- Do not shorten the kappa by deleting substantive literature coverage or technical explanation.

## Success Criteria

The final thesis should read as one cumulative argument rather than seven restatements of the same thesis claim.
Every section should have a clear local purpose, and every paragraph should advance that purpose.
No paragraph should be changed solely to make the Sol version look different from the GPT-5.5 baseline.
The complete LaTeX document must compile without errors, and the final diff must contain prose changes only in the intended thesis sources and new review/plan documentation.
