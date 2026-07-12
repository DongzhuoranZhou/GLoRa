# Thesis Sol Rewrite Design

## Objective

Run a second, higher-judgment prose pass over the complete thesis using GPT-5.6-sol and the `plain-technical-prose` rules.
The pass must improve argument, paragraph function, and cross-chapter progression while preserving every supported technical claim.

## Chosen Approach

The rewrite uses commit `a15da39` as the technical baseline.
Eight workers receive non-overlapping write scopes: `main.tex` and one file for each of the seven chapters.
Within each file, the worker reads every paragraph and changes it only when the change improves clarity, logic, rhythm, or its role in the thesis argument.

This approach is preferred to a fresh redraft because the current version already compiles, follows the required structure, and contains careful technical qualifications.
It is preferred to a selective patch because the user requested an end-to-end Sol review of the complete thesis.

## Coordination

All workers use the same notation guide, Sol review, and included paper as shared evidence.
Each worker owns one file and may not edit any other file.
The main agent reviews all diffs after integration, resolves cross-chapter repetition, runs consistency scans, and compiles the complete thesis.

Writing tasks are independent at the file level, so workers may run in parallel.
Quality review is performed after their drafts are visible in the shared workspace.
Review first checks compliance with the chapter brief and technical constraints, then checks prose quality and cross-chapter coherence.

## Evidence Boundaries

The rewrite may clarify or narrow existing claims but may not introduce a new empirical or theoretical result.
The included GLoRa paper is the source of truth for generator details, Properties (P1)--(P3), evaluated systems, dependency-length findings, and diagnostics.
The notation guide is the source of truth for symbols and terminology.

## Verification

The main agent will compare citations, labels, equations, and section structure before and after the rewrite.
It will scan for terminology drift, repeated scaffold phrases, em dashes, and source-line violations.
It will run `git diff --check` and a fresh `latexmk` build.
Only after those checks pass will the changes be committed and synchronized to the Overleaf main branch and the GitHub `thesis-overleaf` branch.
