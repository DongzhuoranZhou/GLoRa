# Thesis Rewrite Review

## Scope

Reviewed `main.tex`, `notes/notation-and-terminology.md`, and all seven chapter files under `chapters/`.
The thesis is an article-based PhD thesis centered on GLoRa, a benchmark generator for testing whether graph learning systems learn path-aware long-range dependencies of specified length.

## Current Strengths

The thesis already has a clear spine: long-range graph learning is both a modelling problem and an evaluation problem.
GLoRa is positioned as the methodological contribution because it controls dependency length, shortcut functions, and expressibility.
The notation file is useful and should remain the source of truth for terms such as `source node`, `target node`, `dependency length`, `shortcut function`, `over-smoothing`, and `over-squashing`.

The chapter order is sound.
Chapters 2 and 3 establish the computational and task-level meaning of dependency length.
Chapter 4 separates accuracy drops from mechanistic diagnoses.
Chapter 5 surveys architecture and benchmark work.
Chapter 6 presents the GLoRa contribution.
Chapter 7 closes with limitations and future work.

The prose is already readable and technically careful.
The rewrite should therefore be a thesis-level clarity pass, not a change in scientific content.
The goal is to make the argument feel less scaffolded, less repetitive, and more like one sustained account.

## Global Issues To Fix

1. Many sections open with explicit metadiscourse such as "This section explains..." or "This subsection reviews...".
   These sentences are safe, but they repeat across the thesis and make the text feel like an outline.
   Replace most of them with direct topic sentences that still orient the reader.

2. The main claim repeats in almost the same form across chapters: high accuracy does not certify long-range dependency learning unless shortcut functions are ruled out and the intended function is expressible.
   Keep the claim, but make each occurrence do new work.
   In early chapters it should motivate the problem; in Chapter 5 it should evaluate the literature; in Chapter 6 it should explain the construction; in Chapter 7 it should become the final thesis contribution.

3. The prose often uses defensive connectors: "does not by itself", "not enough", "therefore", "however", and "This does not mean".
   These are often correct, but repeated use weakens rhythm.
   Keep the logic while varying sentence shape and cutting redundant caveats.

4. Chapter 5 is useful but repetitive.
   Many subsections have the same structure: method family, what it helps, then why it does not certify dependency length.
   Keep that evaluation standard, but give each method family a more specific local conclusion.
   Let the tables carry compact summary material, and keep body text for interpretation.

5. Chapter 3 has several domain examples that repeat the same path-aware pattern.
   Keep enough examples to show breadth, but compress where the examples only restate the definition.
   The chapter should move from intuition to formal path-aware dependency to evaluation parameter without feeling circular.

6. Chapter 4 is conceptually strong.
   The main rewrite should tighten it around one diagnostic standard: a candidate explanation must predict an internal trace.
   Avoid repeating the same limitation after every phenomenon unless the limitation is specific.

7. Chapter 6 is the technical core.
   Preserve all details of the generator, path-aware definition, properties P1-P3, protocol, results, and diagnostics.
   Improve transitions so the chapter reads as a construction whose pieces solve specific evaluation hazards.

8. The abstract and conclusion should mirror each other more cleanly.
   The abstract should state the thesis in plain terms.
   The conclusion should not merely repeat the abstract; it should state what is now known, what remains open, and why GLoRa gives the field a sharper test.

9. Captions in Chapter 5 are generally within scope, but they can be slightly more "how to read the table" and less like body-text summaries.
   Do not add new results in captions.

10. Preserve technical content.
    Do not alter equations, citation keys, labels, section references, or the included-paper statement unless a compile issue requires it.
    Do not add new unsupported scientific claims.

## Rewrite Standard

Use the plain technical prose rules:

- Name the concrete thing behind abstractions.
- State the point directly, with jargon second when needed.
- Split overloaded sentences, but avoid choppy runs of identical sentence openings.
- Test causal connectives.
- Use one name per concept.
- Keep one sentence per source line.
- Keep notation where it has an immediate job.
- Preserve all math, citations, labels, and claims.

## File-Specific Notes

`main.tex`
The abstract is clear but can be sharper.
The English abstract can be tightened around the evaluation claim.
The Norwegian abstract should receive only light editing unless the worker is confident in the language.
The preface and List of Papers should stay factual.

`chapters/chapter01-introduction.tex`
Reduce section-scaffold openings.
Make the research questions and contributions feel like the natural result of the preceding motivation.
Avoid repeating the same benchmark-design claim in three neighbouring sections.

`chapters/chapter02-graph-learning-message-passing.tex`
Keep definitions precise.
Rewrite section openings to reduce "It matters because" repetition.
Preserve equations and notation exactly unless grammar requires surrounding prose changes.

`chapters/chapter03-long-range-dependencies.tex`
Compress repeated domain examples.
Make the distinction among graph distance, path length, and dependency length crisp.
Keep the path-aware formalization plain and readable.

`chapters/chapter04-failure-explanations.tex`
Use "internal trace" as the organizing thread.
Avoid over-restating that over-smoothing, over-squashing, and vanishing gradients are not ruled out in general.
Preserve the narrow interpretation of the GLoRa diagnostics.

`chapters/chapter05-state-of-the-art.tex`
This chapter needs the most rhythm work.
Vary the subsection openings.
Make each literature family's evaluation risk specific.
Keep tables concise and aligned with the body.

`chapters/chapter06-glora-contribution.tex`
Preserve technical detail.
Strengthen transitions from motivation to path-aware definition, generator design, shortcut analysis, expressibility, protocol, findings, diagnostics, and interpretation.

`chapters/chapter07-discussion-conclusion.tex`
Make the conclusion cumulative rather than repetitive.
Keep limitations concrete.
Make future directions read as a research agenda that follows from the GLoRa result.
