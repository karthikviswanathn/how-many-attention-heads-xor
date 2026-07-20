# How many attention heads does it take to compute a Boolean function?

A single attention head can linearly realize $\mathrm{AND}$ or $\mathrm{OR}$ on two bits,
but it cannot realize $\mathrm{XOR}$. Two heads can. This small gap is the seed of the
whole project: it suggests that the **number of attention heads** is itself a complexity
measure for Boolean functions, sitting somewhere alongside the classical measures
(threshold degree, circuit depth, Fourier complexity) but native to the transformer.

We make that precise, prove what we can, and measure the rest empirically.

## The question

Fix a **single-layer, attention-only transformer**: $n$ input bits plus one query token,
one self-attention layer with $H$ parallel heads, no MLP, no layer norm, and a linear
readout from the query token. A Boolean function $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$ is
*computable with* $H$ *heads* if some choice of embeddings, attention parameters, and
readout reproduces $f$ on every input. Define

$$H^{\ast}(f) := \min\lbrace H : f \text{ is computable with } H \text{ heads} \rbrace.$$

The central problem: **understand $H^{\ast}(f)$** as a function of $f$. Prove lower and upper
bounds, compute it for natural families, and ask whether it equals a known invariant.

The precise model (embeddings, softmax head, residual readout, masking convention) is in
[`model.md`](model.md); the formal problem statement and the list of core questions is in
[`problem_statement.md`](problem_statement.md).

## What we know so far

The results below are written up in full under [`theorems/`](theorems/). The core stack
is indexed in [`theorems.md`](theorems.md); the full consolidated ledger (entries 001-197,
with the dependency order between them) is [`lemmas.md`](lemmas.md), and
[`CONSOLIDATION.md`](CONSOLIDATION.md) maps where every piece came from.

**Lower bounds (a function needs many heads).**
- *Checkerboard obstruction.* If $f$ has a 2-bit "checkerboard" restriction (one diagonal
  of some 2-cube slice disagrees with the other, the way $\mathrm{XOR}$ does), then
  $H^{\ast}(f) \geq 2$. One head can never separate the two diagonals.
- *Threshold-degree bound.* Head complexity dominates threshold degree:
  $\deg_{\pm}(f) \leq H^{\ast}(f)$.
- *General slice obstruction.* For every candidate count $H\geq2$, a homogeneous cleared
  $H$-head score has polynomial slice rank at most two:
  $P = L _1 Q _1 + L _2 Q _2$. Its zero hypersurface contains a real
  codimension-at-most-two linear space, and one slice generator can be chosen as an
  admissible denominator. This gives a Grassmannian lower-bound relaxation with only
  $2(n-1)$ nonlinear dimensions. On the Boolean cube it adds information beyond
  threshold degree only below the middle-level rank collapse, and should be screened
  before use. See
  [`190_slice_rank_two_obstruction.md`](theorems/02_complexity_measure_upper_bounds/190_slice_rank_two_obstruction.md),
  [`191_boolean_cube_slice_relaxation_ceiling.md`](theorems/02_complexity_measure_upper_bounds/191_boolean_cube_slice_relaxation_ceiling.md), and the
  [`general methodology`](artifacts/calculations/general_hstar_scalable_research_program.md).

**The threshold-degree bound is strictly loose.**
- [Theorem 13](theorems/02_separations_and_counterexamples/013_strict_threshold_degree_separation.md)
  gives an explicit ten-bit function $f_{10}$ with
  $\deg_{\pm}(f_{10})=2 \lt 3\leq H^{\ast}(f_{10})$, machine-checked in Lean
  (`f10_strict_separation`). Thus threshold degree is a genuine lower bound, not an
  exact characterization of head complexity.
- The smallest known separation is eight bits: for $x,y\in\lbrace 0,1\rbrace^4$, the
  Hamming threshold $f_8(x,y)=\mathbf{1}[\Delta(x,y)\geq2]$ has
  $\deg_{\pm}(f_8)=2$ but $H^{\ast}(f_8)=3$. Its shell transitions force a
  four-dimensional column-max spectral inequality that no cleared two-head score can
  satisfy. See
  [`189_eight_bit_hamming_threshold_strict_separation.md`](theorems/06_strict_separations/189_eight_bit_hamming_threshold_strict_separation.md).
  An earlier $12$-bit example is the Hamming threshold
  $\mathbf{1}[\Delta(x,y)\geq3]$ from
  [`182_hamming_threshold_strict_separation.md`](theorems/06_strict_separations/182_hamming_threshold_strict_separation.md).
- An exact integer certificate also proves equality $H^{\ast}(f)=\deg_{\pm}(f)$ for every
  function on at most four bits. See
  [`183_small_dimension_exact_classification.md`](theorems/06_strict_separations/183_small_dimension_exact_classification.md).
  An exhaustive cocircuit and tangent-tope certificate proves that every five-bit
  function of threshold degree two has head complexity exactly two. See
  [`187_five_bit_degree_two_exact.md`](theorems/06_strict_separations/187_five_bit_degree_two_exact.md).
  A second exact classification eliminates all five-bit functions of threshold degree four:
  each has exactly four-head complexity. See
  [`186_five_bit_degree_four_exact.md`](theorems/06_strict_separations/186_five_bit_degree_four_exact.md).
  Thus the least separation dimension is currently between $5$ and $8$, and any
  five-bit separation must have threshold degree three.

**Upper bounds (a function needs few heads).**
- *Symmetric thresholds need one head.* Every $T_{n,t}(x) = \mathbf{1}[|x| \geq t]$ is
  computable with a single head, so $H^{\ast}(\mathrm{AND}_n) = H^{\ast}(\mathrm{OR}_n) = H^{\ast}(\mathrm{MAJORITY}_n) = 1$.
- *Weighted-sum interpolation.* If $f(x) = F\left(\sum_i \lambda_i x_i\right)$ for
  positive weights $\lambda_i$ and the weighted sum takes $M$ distinct values, then
  $H^{\ast}(f) \leq M - 1$. Consequently every symmetric function needs at most $n$ heads and
  every Boolean function at most $2^n - 1$.
- *Fourier-sparse construction.* If a Walsh polynomial $\sum_S c_S\chi_S$ strictly
  sign-represents $f$, its constant and singleton-character part costs at most one head,
  while every active character of size at least two costs its support size. Thus a degree $d$
  Walsh PTF with $m _{\geq2}$ active nonsingleton terms needs at most
  $\mathbf{1}[m _1 > 0] + d m _{\geq2}$ heads.
  See [`045_fourier_support_upper_bound.md`](theorems/02_complexity_measure_upper_bounds/045_fourier_support_upper_bound.md).

**Certified concrete interval.**

- *Six-bit parity triple flip.* For parity with vertices $21$, $38$, and $41$ flipped,
  exact integer certificates prove $\deg_{\pm}(f_6)=4$ and
  $4\leq H^{\ast}(f_6)\leq6$. The upper endpoint is a verified six-head
  representation. See
  [`n6_parity_midlayer_triple_rigidity.md`](artifacts/calculations/n6_parity_midlayer_triple_rigidity.md).

**Exact answers.**
- *Parity is the extremal case.* $H^{\ast}(\mathrm{XOR}_n) = n$: in this model, parity needs
  exactly one head per input bit. The lower bound comes from
  $\deg _{\pm}(\mathrm{PARITY}_n) = n$, the upper bound from an explicit $n$-head construction.
- A first split inside the symmetric functions: monotone thresholds have complexity $1$,
  while parity and the internal exact-count predicates $\mathrm{EXACT}_{n,k}$ need at
  least $2$.
- *A geometric non-equivalence.* The affine cut-cell formulation is already different
  for $\mathrm{XOR} _3$: it needs four plane cuts, while $H^{\ast}(\mathrm{XOR} _3)=3$.
  See [`artifacts/calculations/cut_cell_counterexample.md`](artifacts/calculations/cut_cell_counterexample.md).

Taken together this is a *partial* characterization, not yet a single invariant
$I(f)$ with $H^{\ast}(f) \asymp I(f)$. Closing that gap is the main open problem.

## Open directions

- Find an invariant that pins down $H^{\ast}(f)$ on broad classes, or a family where head
  complexity behaves qualitatively unlike the classical measures.
- Determine the exact value of $H^{\ast}(f_{10})$, and find scalable families with a
  growing gap between threshold degree and head complexity.
- Close the remaining gap for the smallest strict-separation dimension, currently known
  to lie between $5$ and $8$.
- Push the formalization in [`formalization/`](formalization/) to cover more of the
  theorem stack.
- Extend the empirical search to larger $n$ and reconcile it with the proofs. The current
  run flags four provisional $H^{\ast}(f) = 3$ functions at $n = 3$ (see
  [`three_head_functions_n3.md`](three_head_functions_n3.md)); these are estimates
  awaiting proof.
- Benchmark the general certificate portfolio: optimized product-margin matrix bounds,
  slice-rank Grassmann incidence, cost-aware sparse PTF search, and direct
  denominator-group boosting.

## Repository map

| Path | What it is |
| --- | --- |
| [`problem_statement.md`](problem_statement.md) | The question and the core open problems. |
| [`CONSOLIDATION.md`](CONSOLIDATION.md) | The all-branches consolidation: source map, proved-material index, consolidated hypotheses. |
| [`model.md`](model.md) | The precise attention model and the definition of $H^{\ast}(f)$. |
| [`theorems.md`](theorems.md) | Ledger of the core theorem stack, its status, and how it fits together. |
| [`lemmas.md`](lemmas.md) | Full consolidated ledger (entries 001-197) with the dependency order between them. |
| [`theorems/`](theorems/) | Full writeups: foundational results, normal forms, upper-bound machinery, and explicit separations. |
| [`artifacts/intro-materials/writeup.md`](artifacts/intro-materials/writeup.md) | Original blog-post writeup of the two-bit XOR result. |
| [`literature_survey.md`](literature_survey.md) | Related work across transformers and Boolean complexity. |
| [`artifacts/calculations/cut_cell_counterexample.md`](artifacts/calculations/cut_cell_counterexample.md) | Short counterexample showing that affine cut cells do not characterize $H^{\ast}$. |
| [`three_head_functions_n3.md`](three_head_functions_n3.md) | The corrected exact three-bit head-complexity hierarchy. |
| [`formalization/`](formalization/) | Lean 4 formalization of the results (depends on mathlib). |
| [`src/hstar/`](src/hstar/) | Python package with both empirical training searches and certified interval estimation for $H^{\ast}(f)$. |
| [`artifacts/calculations/certified_hstar_estimation.md`](artifacts/calculations/certified_hstar_estimation.md) | Guaranteed interval estimator using exact lower bounds, verified upper certificates, and optional real-algebraic decisions. |
| [`artifacts/calculations/general_hstar_scalable_research_program.md`](artifacts/calculations/general_hstar_scalable_research_program.md) | General research program for structural, matrix, coefficient-lift, witness-subset, and parameter-space bounds. |
| [`artifacts/calculations/scalable_hstar_bound_methodology.md`](artifacts/calculations/scalable_hstar_bound_methodology.md) | Anytime certificate architecture and implementation priorities. |
| [`artifacts/calculations/adaptive_general_hstar_estimator.md`](artifacts/calculations/adaptive_general_hstar_estimator.md) | Adaptive proof-portfolio scheduler, exact certificate schemas, cost gates, and research priorities for general $H^{\ast}$. |
| [`artifacts/calculations/high_head_hstar_methodology.md`](artifacts/calculations/high_head_hstar_methodology.md) | Model-aware lower methods that remain nontrivial above the matrix and slice midpoint ceilings. |
| [`artifacts/calculations/weighted_tau_hard_core_scheduler.md`](artifacts/calculations/weighted_tau_hard_core_scheduler.md) | Certified search design for restrictions, hard submatrices, product weights, and exact weighted $\tau$ admission. |
| [`src/hstar/sparse_ptf.py`](src/hstar/sparse_ptf.py) | Exact sparse monomial and Walsh PTF upper certificates, greedy Fourier tails, optimal tail knapsack, and bounded support search. |
| [`artifacts/calculations/verify_sparse_ptf_prototype.py`](artifacts/calculations/verify_sparse_ptf_prototype.py) | Exhaustive small checks and transform-priced column-generation scale tests. |
| [`artifacts/calculations/weighted_tau_partition_pilot.py`](artifacts/calculations/weighted_tau_partition_pilot.py) | Eigenvector-cut weighted $\tau$ discovery with an exact rational Gram-plus-residual verifier. |
| [`artifacts/calculations/boolean_cube_slice_rank_and_n6_cubic_dominance.md`](artifacts/calculations/boolean_cube_slice_rank_and_n6_cubic_dominance.md) | Executable certificate for the Boolean slice-rank formula and six-bit cubic dominance warning. |
| [`theorems/02_complexity_measure_upper_bounds/192_multiway_sign_tensor_rank.md`](theorems/02_complexity_measure_upper_bounds/192_multiway_sign_tensor_rank.md) | Exact multiway tangent rank cap and proof that CP-rank size cannot beat the balanced matrix input-count screen. |
| [`theorems/02_complexity_measure_upper_bounds/193_positive_secant_diagonal_blowup.md`](theorems/02_complexity_measure_upper_bounds/193_positive_secant_diagonal_blowup.md) | Exact replacement of the positive-secant endpoint diagonal by finitely charted tangent directions. |
| [`theorems/02_complexity_measure_upper_bounds/194_signed_secant_diagonal_blowup.md`](theorems/02_complexity_measure_upper_bounds/194_signed_secant_diagonal_blowup.md) | Closed signed-secant compactification with one inequality per truth-table vertex. |
| [`artifacts/calculations/verify_signed_secant_diagonal_blowup.py`](artifacts/calculations/verify_signed_secant_diagonal_blowup.py) | Exact rational identity, chart, boundary, and pair-equivalence checks for Theorem 194. |
| [`artifacts/calculations/signed_secant_mccormick_leaf_format.md`](artifacts/calculations/signed_secant_mccormick_leaf_format.md) | Exact rational McCormick cell-leaf schema, checker, first certificate, and scaling analysis. |
| [`artifacts/calculations/f8_h2_pp_scalar_plus_chart_cover.json`](artifacts/calculations/f8_h2_pp_scalar_plus_chart_cover.json) | Exact five-term dual covering one full two-head chart of the eight-bit separation. |
| [`theorems/02_complexity_measure_upper_bounds/195_atomic_margin_sparsification.md`](theorems/02_complexity_measure_upper_bounds/195_atomic_margin_sparsification.md) | Model-native upper bound from the output-normalized one-head atomic margin. |
| [`theorems/02_complexity_measure_upper_bounds/196_optimal_fourier_tail_knapsack.md`](theorems/02_complexity_measure_upper_bounds/196_optimal_fourier_tail_knapsack.md) | Exact polynomial-time optimization of the absolute Fourier-tail compiler certificate. |
| [`theorems/02_complexity_measure_upper_bounds/197_box_sum_greedy_affine_bounds.md`](theorems/02_complexity_measure_upper_bounds/197_box_sum_greedy_affine_bounds.md) | Exact fractional-knapsack affine bounds used to tighten signed-secant cells. |
| [`artifacts/calculations/six_bit_optimal_fourier_tail_h8_certificate.json`](artifacts/calculations/six_bit_optimal_fourier_tail_h8_certificate.json) | Exact eight-head Walsh certificate from the public budgeted Fourier-tail backend. |
| [`artifacts/calculations/n6_parity_midlayer_triple_h6_certificate.json`](artifacts/calculations/n6_parity_midlayer_triple_h6_certificate.json) | Exact six-head upper certificate for the six-bit parity triple-flip candidate. |
| [`artifacts/intro-materials/proposal.pdf`](artifacts/intro-materials/proposal.pdf) / [`proposal.tex`](artifacts/intro-materials/proposal.tex) | Project proposal (build with `./artifacts/scripts/compile_pdf.sh`). |
| [`AGENTS.md`](AGENTS.md) | Markdown conventions used across the writeups. |

New here? Read [`problem_statement.md`](problem_statement.md), then skim
[`theorems.md`](theorems.md). The individual files under [`theorems/`](theorems/) are self-contained.

## Getting started

**Lean proofs.** Needs [Lean 4 / elan](https://leanprover-community.github.io/get_started.html).

```bash
cd formalization
lake exe cache get   # fetch prebuilt mathlib, first time only
lake build
```

**Python search.** Needs Python with [PyTorch](https://pytorch.org/). The package
enumerates symmetry-class representatives of $n$-bit functions and, for each, trains
attention models with increasing head counts to estimate $H^{\ast}(f)$.

```bash
# Estimate H*(f) over all 3-bit representatives, trying up to 3 heads.
PYTHONPATH=src python -m hstar.cli --n 3 --max-heads 3
```

Useful flags: `--limit` / `--start-index` / `--end-index` to slice the representative
list, `--robust` for a stronger second-pass search, `--device {cpu,cuda,mps}`, and
`--output result.json` to save the payload. Run with `--help` for the full list.

**Proposal PDF.**

```bash
./artifacts/scripts/compile_pdf.sh   # runs pdflatex on proposal.tex and cleans up aux files
```
