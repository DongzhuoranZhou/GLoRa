# Thesis Figure Inventory

## Source and Reuse Rule

All selected figures are extracted from the official PDF of Paper I at `papers/glora-iclr-2025.pdf`.
They reproduce the published visual evidence rather than reconstructing graphs or numerical data from memory.
Thesis captions will use the attribution `Adapted from Paper I` and will state the tested setting and evidential limit.

## Running Path-Aware Example

**Source:** Paper I, Figure 1.

**Extracted assets:**

- `figures/glora-positive-d6.png`
- `figures/glora-negative-d6.png`

**Published caption:** Positive (left) and negative (right) GLoRa examples for $d=6$: green source nodes, blue normal nodes, and orange hole nodes have embeddings of the forms $[1,-]$, $[-,1]$, and $[-,0]$, respectively; $T$ marks the target node; the red-arrow chain is the long-range dependency path.

**Thesis role:** introduce the source, target, intended path, and hole distinction in Chapter 1, then reuse the same figure by cross-reference when Chapter 3 formalises path-aware dependence.

**Interpretive boundary:** the figure illustrates one generated positive/negative pair.
It does not by itself establish shortcut resistance or any of Properties (P1)--(P3); Chapter 6 supplies those arguments.

## Accuracy Against the Generator Parameter

**Source:** Paper I, Figure 2(a)--(c).

**Extracted assets:**

- `figures/glora-accuracy-vanilla.png`
- `figures/glora-accuracy-oversmoothing.png`
- `figures/glora-accuracy-oversquashing.png`

**Published caption:** Test accuracy of GNN-based systems on GLoRa benchmarks for increasing $d$; lines represent mean accuracy over multiple runs and shaded areas indicate standard deviation.

**Panel meanings:**

- Figure 2(a): vanilla GNN-based systems;
- Figure 2(b): systems targeting over-smoothing;
- Figure 2(c): systems targeting over-squashing.

**Thesis role:** present the principal performance evidence once in Chapter 6.
The three panels should appear in a single figure environment so their shared axes and comparison purpose remain clear.

**Interpretive boundary:** the horizontal trend is performance as Paper I's generator parameter $d$ increases.
It is evidence of failure on the controlled benchmark instances, not by itself a diagnosis of over-smoothing, over-squashing, or optimisation failure.

## Diagnostic Figures

Paper I also contains Figure 3, which plots histograms of one-dimensional final target-node values, and Figure 4, which plots first-layer weight gradients over training.
Neither figure has been selected for the kappa at this stage.
The thesis can state the reported measurements and limits in Chapter 6 without adding a third dense figure.
This avoids turning the kappa into a duplicate of Paper I and leaves the visual emphasis on the task construction and main performance pattern.

## Planned Placement

| Thesis location | Figure | Function |
|---|---|---|
| Chapter 1 | Paper I Figure 1, positive and negative panels | Establish the running example and evaluation problem |
| Chapter 3 | Cross-reference to the Chapter 1 figure | Formalise the same example without duplication |
| Chapter 6 | Paper I Figure 2(a)--(c) | Present the principal performance result and its variance |

No decorative figure and no unsupported diagnostic synthesis will be added.
