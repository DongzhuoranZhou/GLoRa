# Thesis Structural Revision Baseline

## Source State

- Baseline commit: `2b78c0a59c55f790b81d24ffeab5b2a44e1ab613`
- Commit date: 2026-07-12
- Commit subject: `Rewrite thesis prose with GPT-5.6 Sol`
- Execution branch: `codex/thesis-structural-revision`
- Included Paper I checksum: `dfe3c3b1ffb9145436e9b0c7bc090bb7479c95328cbc2bf5083b66cdf3f9e10a`
- Paper file: `papers/glora-iclr-2025.pdf`

The baseline is the published Sol prose pass.
This revision therefore measures structural and argumentative changes against an already edited language baseline.

## Source Size

| Source | Lines | Words |
|---|---:|---:|
| `main.tex` | 114 | 607 |
| Chapter 1 | 274 | 3,269 |
| Chapter 2 | 390 | 4,353 |
| Chapter 3 | 306 | 4,200 |
| Chapter 4 | 232 | 3,264 |
| Chapter 5 | 511 | 6,174 |
| Chapter 6 | 368 | 4,669 |
| Chapter 7 | 140 | 1,918 |
| **Total** | **2,335** | **28,454** |

## Structural Inventory

- Chapters: 7
- Chapter and section headings: 78
- Citation keys used in the kappa: 62
- `\bibitem` entries: 62
- Citation keys without a matching `\bibitem`: 0
- Labels: 25
- Explicit reference commands: 0
- Displayed equation environments recorded by the baseline scan: 0
- Tables: 6, all in Chapter 5
- Figures: 0
- Included papers: 1

The source contains inline display mathematics but no named `equation`, `align`, `gather`, or `multline` environments.

## Compiled Baseline

The untouched thesis source was compiled with a clean `latexmk` build and then a second stability build:

```bash
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Both commands exited successfully.
The second command reported that all targets were up to date.

- Total PDF pages: 113
- Bibliography ends on PDF page 90
- Paper I divider: PDF page 91
- Blank separator: PDF page 92
- Published Paper I PDF begins: PDF page 93
- PDF title: *Long-Range Dependency Learning in Graph Neural Networks: Benchmarks, Explanations, and Limits*

The final LaTeX log contains four pre-existing `Underfull \vbox` warnings and no unresolved citation or cross-reference warning.
These warnings are the comparison baseline for the final build.

## Preserved Mechanical Inventories

The directory `artifacts/structural-revision/baseline/` contains:

- source line and word counts;
- Paper I checksum;
- sorted citation keys;
- sorted labels;
- explicit reference targets;
- chapter and section headings;
- mathematical, table, and figure environment locations;
- candidate numerical and diagnostic claims from Chapters 4, 6, and 7;
- clean and stability build logs;
- compiled PDF metadata.

The final technical-preservation review will compare the revised thesis with these inventories and investigate every difference rather than assuming that a changed count is harmless.
