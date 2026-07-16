# Literature Update: Long-Range Failure Mechanisms and Evaluation

## Scope

This memo records the literature check completed before restructuring the thesis.
It covers work available through 16 July 2026 on over-smoothing, over-squashing, optimisation and gradient failure, and evaluation of long-range graph learning.
Three independent searches examined over-smoothing, over-squashing, and the relation among performance symptoms, mechanisms, diagnostics, and benchmarks.

The purpose is not to turn the kappa into an exhaustive survey.
The update identifies literature that changes a definition, corrects the interpretation of a diagnostic, or materially changes how GLoRa should be positioned.
Primary papers support technical claims; surveys and position papers are used only for discovery or to identify debates.

## Accepted Taxonomy

The revised thesis will separate four levels that the literature often mixes:

1. **Performance symptom:** accuracy declines as dependency length increases.
2. **Candidate mechanism:** a proposed reason for failure, such as representation contraction, inadequate communication capacity, or weak backward signal.
3. **Diagnostic:** a measurement predicted by a mechanism, such as within-graph representation convergence, source-to-target sensitivity, or task-aligned layerwise gradients.
4. **Intervention:** an architectural or optimisation change motivated by a mechanism.

An intervention that improves accuracy establishes practical usefulness under its tested conditions.
It does not by itself show that its motivating mechanism caused the baseline failure because the intervention may also change depth, topology, optimisation, model capacity, effective dependency length, or the hypothesis class.

Accuracy against dependency length is therefore a symptom curve.
When the benchmark controls shortcuts and target expressibility, the curve can locate where a system stops learning the intended dependency.
It cannot identify the failure mechanism without additional measurements.

## Over-Smoothing

### Bounded Definition

Graph propagation often contracts node-varying components of the representation towards an operator-dependent invariant or low-dimensional subspace.
This contraction becomes harmful over-smoothing when it erases task-relevant distinctions before the model has completed the computation required for prediction.

This definition avoids four overstatements:

- the limiting subspace need not be a single constant vector;
- finite smoothing may be useful denoising before it becomes harmful;
- low rank, low norm, weak class separation, and over-smoothing are related but not identical;
- an accuracy decrease with depth is not itself evidence of over-smoothing.

### Theory to Add

The revised Chapter 4 should add a compact progression rather than a long catalogue:

- Li, Han, and Wu establish the graph-smoothing interpretation of GCN propagation.
- Oono and Suzuki give sufficient spectral and weight-norm conditions for exponential convergence towards an invariant subspace.
- Cai and Wang connect over-smoothing to contraction of raw Dirichlet energy under spectral and weight-norm conditions; this workshop result is useful only if the thesis discusses energy-based diagnostics because raw energy is scale-sensitive and can vanish through norm collapse.
- Keriven gives two model-specific examples in which finitely many mean-aggregation steps improve regression or classification before further smoothing becomes harmful.
- Wu et al. show that broad attention systems can also contract under explicit assumptions, so attention is not a general anti-smoothing guarantee.
- Roth and Liebig show that rank collapse is broader than over-smoothing and produces over-smoothing only for particular aggregation operators.
- Scholkemper et al. analyse linearised GNNs: initial residuals constrain the attainable subspace, while batch normalisation prevents one-dimensional collapse and can yield a top-$k$ eigenspace.

### Diagnostics and Limits

The chapter should distinguish pairwise distances, cosine or MAD measures, Dirichlet energy, projection distance to a predicted invariant subspace, effective rank, and task-conditioned probes.
Each measures a different trace and depends on choices about scale, graph operator, directionality, node roles, and task relevance.

Paper I examines the one-dimensional final target representation across examples at two generator settings and observes that the values do not collapse to one point.
The thesis may safely report that observation and state that it does not support complete collapse of the measured scalar.
It should not present the experiment as a general test of within-graph, layerwise, task-relevant over-smoothing.

This is a thesis-level clarification of the evidence, not a criticism inserted into the prose.
Chapter 6 will describe the measurement, observation, and bounded implication neutrally.

## Over-Squashing

### Bounded Definition

Over-squashing is a model- and task-relative failure in which relevant information is reachable through the message-passing computation but exerts too little usable influence on the target because the available computational channels are inadequate.

The literature now supports at least three related accounts:

- **computational or capacity bottleneck:** finite-width aggregation cannot retain or select the required information;
- **topological bottleneck:** cuts, curvature, commute time, or effective resistance limit communication between relevant regions;
- **dynamical or sensitivity bottleneck:** source-to-target influence contracts through normalisation, depth, or learned dynamics.

The thesis should keep strict under-reaching separate: when the source lies outside the receptive field, its influence is structurally zero rather than merely too weak.
It should also keep input-output sensitivity separate from parameter-gradient magnitude.

### Theory to Add

- Alon and Yahav motivate the finite-capacity account using branching and chain controls.
- Topping et al. relate message-passing sensitivity bounds to graph structure and curvature under stated derivative assumptions.
- Di Giovanni et al. analyse the effects of width, depth, and topology and later define task-relative mixing.
- Black et al. connect over-squashing to effective resistance for undirected graphs.
- Recent work on width-aware message passing, virtual nodes, and graph dynamics shows that rewiring is not the only possible intervention.

Curvature, spectral gap, effective resistance, path counts, and cuts are structural proxies rather than universal diagnoses.
Many central theorems concern undirected graphs and must not be transferred to GLoRa's directed construction without qualification.

### Diagnostics and Limits

Useful tests include distance-versus-branching controls, task-conditioned input-output Jacobians, perturbation sensitivity, width sweeps, and matched rewiring interventions.
Topology-only measures omit learned weights, direction, source relevance, and task semantics.
Rewiring changes the task's communication graph and can shorten the effective dependency, so an accuracy gain alone does not identify the cause.

In GLoRa's main directed construction, the number of directed source-to-target paths is bounded independently of the generator parameter.
This excludes exponential directed path proliferation as a complete explanation of the observed degradation.
It does not exclude sensitivity decay along a small number of paths, finite-width capacity limits, task-relative mixing limits, or optimisation effects.

## Optimisation and Gradient Evidence

The revised thesis will distinguish parameter-gradient magnitudes from task-aligned information transport.
Nonzero first-layer weight gradients show that the inspected aggregate gradients have not numerically vanished.
They do not establish that useful source-conditioned signals reach every required parameter or that the optimisation direction supports the intended dependency.

Recent joint analyses of recurrent and graph learning provide a better theoretical frame for the interaction among forward contraction, over-squashing, and backward gradients.
Chapter 4 should explain that interaction at a conceptual level; Chapter 6 should report only the exact gradients Paper I measured.

## Long-Range Evaluation After GLoRa

The post-2024 literature strengthens the thesis's central evaluation argument:

- Tönshoff et al. show that the reported performance gap between selected message-passing and GPS baselines on the Long Range Graph Benchmark depends substantially on the tested tuning and protocol choices.
- Bamberger et al. introduce distance-weighted input-output derivatives for measuring model and task range and report dataset- and architecture-specific differences in the ranges they measure.

Chapter 5 should compare benchmarks using the following criteria:

- necessity of the claimed dependency;
- resistance to shortcut functions;
- model-class and realised expressivity;
- class-distribution and system-protocol fairness;
- controlled dependency length and graph scale;
- in-range interpolation versus distance-held-out extrapolation;
- protocol sensitivity;
- available mechanism diagnostics.

GLoRa's strongest position remains the joint control of a length-parameterised path-aware dependency, shortcut resistance, expressibility, and class fairness.
The thesis should separately acknowledge finite-sample behaviour, realised expressivity of each trained configuration, mechanism identification, and distance extrapolation as limitations or future directions.

## Inclusion Decisions

### Add to the Thesis

An independent citation review approved the following minimal set:

- Oono and Suzuki, ICLR 2020, invariant-subspace convergence under explicit assumptions;
- Keriven, NeurIPS 2022, two model-specific finite-depth smoothing analyses;
- Wu et al., NeurIPS 2023, over-smoothing in attention-based GNNs under stated conditions;
- Scholkemper et al., ICLR 2025, residuals, normalisation, and limiting subspaces in linearised GNNs;
- Di Giovanni et al., TMLR 2024, task-relative mixing and expressive power;
- Arroyo et al., NeurIPS 2025, a joint analysis connecting gradients to particular contractive smoothing and squashing mechanisms;
- Bamberger et al., ICML 2025, distance-weighted derivative measures of long-range interaction;
- Tönshoff et al., TMLR 2024, protocol sensitivity in the reported message-passing versus GPS gap on LRGB.

Cai and Wang, Roth and Liebig, or Black et al. will be added only if the final prose retains raw Dirichlet energy, effective rank, or effective resistance as a named diagnostic.

### Use Selectively or Only as Future Work

PANDA, virtual-node theory, recent dynamical systems, causal rewiring studies, City-Networks, ECHO, and distance-generalisation preprints are useful for the current frontier.
They should appear only when a concise paragraph or table row materially supports an argument already required by the thesis.
Preprints and position papers must be labelled as such and will not carry foundational claims when a peer-reviewed source is available.

### Do Not Add Merely for Breadth

The thesis will not enumerate every mitigation method published through 2026.
A method is included only if it represents a distinct mechanism, diagnostic, intervention family, or evaluation criterion.

## Verified Source Locations

- Oono and Suzuki: <https://openreview.net/forum?id=S1ldO2EFPr>
- Cai and Wang: <https://arxiv.org/abs/2006.13318>
- Keriven: <https://proceedings.neurips.cc/paper_files/paper/2022/hash/0f956ca6f667c62e0f71511773c86a59-Abstract-Conference.html>
- Wu et al.: <https://proceedings.neurips.cc/paper_files/paper/2023/hash/6e4cdfdd909ea4e34bfc85a12774cba0-Abstract-Conference.html>
- Black et al.: <https://proceedings.mlr.press/v202/black23a.html>
- Di Giovanni et al.: <https://openreview.net/forum?id=KJRoQvRWNs>
- Scholkemper et al.: <https://openreview.net/forum?id=i8vPRlsrYu>
- Bamberger et al.: <https://proceedings.mlr.press/v267/bamberger25a.html>
- Arroyo et al.: <https://proceedings.neurips.cc/paper_files/paper/2025/hash/6ba7ebba4d54408b00a2b0275629f625-Abstract-Conference.html>
- Tönshoff et al.: <https://openreview.net/forum?id=Nm0WX86sKv>
- GLoRa: <https://openreview.net/forum?id=60i0zFqawO>

Metadata notes:

- Tönshoff et al. is a TMLR 2024 paper; the baseline bibliography incorrectly gives 2023.
- Arroyo et al. is cited as NeurIPS 2025 even though the official proceedings page was posted in 2026.
- Cai and Wang is an ICML 2020 workshop paper, not an archival ICML proceedings paper.
- Roth and Liebig appears in the Proceedings of the Second Learning on Graphs Conference, PMLR 231, published in 2024 for the 2023 conference.

## Writing Constraints Derived from the Review

- State what each diagnostic measures before stating its implication.
- Use “does not support” rather than “rules out” unless the tested account and assumptions are named.
- Keep Paper I's reported measurements unchanged while narrowing only thesis-level interpretation where necessary.
- Attribute critiques of existing benchmarks to GLoRa or the relevant primary source.
- Keep post-GLoRa literature in Chapters 4 and 5; do not retroactively present it as part of Paper I.
- Present GLoRa as the sole included paper and distinguish its original contribution from the kappa's later synthesis.
