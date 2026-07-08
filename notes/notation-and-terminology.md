# Notation and Terminology

This file is the source of truth for notation in the thesis.
The purpose is to avoid symbol drift across chapters.

## Graphs

- Graph: $G=(V,E,\lambda)$.
- Nodes: $u,v,w\in V$.
- Directed edge: $(u,v)\in E$ means that information can be aggregated from $u$ into $v$ under the paper's convention.
- Node feature map: $\lambda:V\to\mathbb{R}^{n}$.
- Input feature of node $v$: $\lambda(v)$.
- Neighbourhood: $N(v)=\{u\in V\mid (u,v)\in E\}$.
- Use `neighbour` and `neighbourhood` consistently.

## Message Passing

- Layer index: $\ell$.
- Number of message-passing layers: $L$.
- Hidden state or node representation at layer $\ell$: $h_v^{(\ell)}$.
- Initial representation: $h_v^{(0)}=\lambda(v)$.
- Aggregation function: $\operatorname{Agg}^{(\ell)}$.
- Update function: $\operatorname{Upd}^{(\ell)}$.
- Classification function: $\operatorname{Cls}$.

Do not use both $v_\ell$ and $h_v^{(\ell)}$ for the same node representation.
Use $h_v^{(\ell)}$ in the thesis text.
If quoting or paraphrasing the GLoRa paper's equation, explain that the thesis uses $h_v^{(\ell)}$ for the same object.

## Paths and Dependency Length

- Dependency length: $d$.
- Path of length $d$: $p=(v_0,\ldots,v_d)$.
- Source node on the path: $v_0$.
- Target node on the path: $v_d$.
- Intermediate node: $v_i$ for $0<i<d$.
- Graph distance in graph $G$: $\operatorname{dist}_G(u,v)$.
- Use $\operatorname{dist}(u,v)$ only when the graph is clear and the subscript would add clutter.

Do not use $d$ for hidden dimension, degree, or dataset.
Use $n$ for input feature dimension and $m$ only for local counts when needed.

## GLoRa

- Method name: GLoRa.
- Long form: Graph Long-Range dependency benchmark.
- Task type: inductive binary node classification.
- Label values: True and False in prose; use mathematical labels only when needed.
- A positive example contains a complete source-to-target path with the required feature pattern.
- A negative example contains a hole on the corresponding path.

## Terms

- Use `long-range dependency`, not `long dependency`, except when quoting a title or paper phrase.
- Use `dependency length`, not `range length`.
- Use `target node`, not `prediction node`.
- Use `source node`, not `starting node`, except in informal explanation.
- Use `shortcut function` for a function that fits the generated data without using the intended dependency.
- Use `expressible` for functions representable by the evaluated architecture.
- Use `over-smoothing` with a hyphen.
- Use `over-squashing` with a hyphen.
- Use `vanishing gradients` for the phenomenon in prose; singular only inside compound phrases.

## Claims To Preserve

- Long-range graph learning is partly an architectural problem and partly an evaluation problem.
- Good benchmark performance does not by itself prove that a graph learning system learned a dependency of a specified length.
- A controlled benchmark should rule out shortcut functions and keep the target function expressible by the evaluated model family.
- GLoRa shows that many evaluated systems fail as dependency length grows.
- The GLoRa diagnostics show that over-smoothing, over-squashing, and vanishing gradients do not fully explain the observed drop in the tested setting.
