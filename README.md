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
readout from the query token. A Boolean function $f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$ is
**computable with** $H$ **heads** if some choice of embeddings, attention parameters, and
readout reproduces $f$ on every input. Define

$$ H^{\ast}(f)  :=  \min\lbrace  H : f \text{ is computable with } H \text{ heads}  \rbrace. $$

The central problem: **understand $H^{\ast}(f)$** as a function of $f$. Prove lower and upper
bounds, compute it for natural families, and ask whether it equals a known invariant.

The precise model (embeddings, softmax head, residual readout, masking convention) is in
[`model.md`](model.md); the formal problem statement and the list of core questions is in
[`problem_statement.md`](problem_statement.md).

## What we know so far

The results below are written up in full under [`lemmas/`](lemmas/) and indexed, with the
dependency order between them, in [`lemmas.md`](lemmas.md).

**Lower bounds (a function needs many heads).**
- *Checkerboard obstruction.* If $f$ has a 2-bit "checkerboard" restriction (one diagonal
  of some 2-cube slice disagrees with the other, the way $\mathrm{XOR}$ does), then
  $H^{\ast}(f) \geq 2$. One head can never separate the two diagonals.
- *Threshold-degree bound.* Head complexity dominates threshold degree:
  $\deg_{\pm}(f) \leq H^{\ast}(f)$.
- *The bound can be strict.* For $x,y\in\lbrace0,1\rbrace^4$, the explicit eight-bit
  Hamming threshold $f_8(x,y)=\mathbf{1}[\Delta(x,y)\geq2]$ has
  $\deg_{\pm}(f_8)=2$ but $H^{\ast}(f_8)=3$. Its shell transitions force a
  four-dimensional column-max spectral inequality that no cleared two-head score can
  satisfy. See
  [`189_eight_bit_hamming_threshold_strict_separation.md`](lemmas/06_strict_separations/189_eight_bit_hamming_threshold_strict_separation.md).
  An earlier $12$-bit example is the Hamming threshold
  $\mathbf{1}[\Delta(x,y)\geq3]$ from
  [`182_hamming_threshold_strict_separation.md`](lemmas/06_strict_separations/182_hamming_threshold_strict_separation.md).
  An exact integer certificate also proves equality $H^{\ast}(f)=\deg_{\pm}(f)$ for every
  function on at most four bits. See
  [`183_small_dimension_exact_classification.md`](lemmas/06_strict_separations/183_small_dimension_exact_classification.md).
  An exhaustive cocircuit and tangent-tope certificate proves that every five-bit
  function of threshold degree two has head complexity exactly two. See
  [`187_five_bit_degree_two_exact.md`](lemmas/06_strict_separations/187_five_bit_degree_two_exact.md).
  A second exact classification eliminates all five-bit functions of threshold degree four:
  each has exactly four-head complexity. See
  [`186_five_bit_degree_four_exact.md`](lemmas/06_strict_separations/186_five_bit_degree_four_exact.md).
  Thus the least separation dimension is currently between $5$ and $8$, and any
  five-bit separation must have threshold degree three.

**Upper bounds (a function needs few heads).**
- *Symmetric thresholds need one head.* Every $T_{n,t}(x) = \mathbf{1}[ |x| \geq t ]$ is
  computable with a single head, so $H^{\ast}(\mathrm{AND}_n) = H^{\ast}(\mathrm{OR}_n) = H^{\ast}(\mathrm{MAJORITY}_n) = 1$.
- *Weighted-sum interpolation.* If $f(x) = F \left(\sum_i \lambda_i x_i\right)$ for
  positive weights $\lambda_i$ and the weighted sum takes $M$ distinct values, then
  $H^{\ast}(f) \leq M - 1$. Consequently every symmetric function needs at most $n$ heads and
  every Boolean function at most $2^n - 1$.

**Exact answers.**
- *Parity is the extremal case.* $H^{\ast}(\mathrm{XOR}_n) = n$: in this model, parity needs
  exactly one head per input bit. The lower bound comes from
  $\deg _{\pm}(\mathrm{PARITY}_n) = n$, the upper bound from an explicit $n$-head construction.
- A first split inside the symmetric functions: monotone thresholds have complexity $1$,
  while parity and the internal exact-count predicates $\mathrm{EXACT}_{n,k}$ need at
  least $2$.
- *A geometric non-equivalence.* The affine cut-cell formulation is already different
  for $\mathrm{XOR}&#95;3$: it needs four plane cuts, while $H^{\ast}(\mathrm{XOR}&#95;3)=3$.
  See [`artifacts/calculations/cut_cell_counterexample.md`](artifacts/calculations/cut_cell_counterexample.md).

Taken together this is a *partial* characterization, not yet a single invariant
$I(f)$ with $H^{\ast}(f) \asymp I(f)$. Closing that gap is the main open problem.

## Open directions

- Find an invariant that pins down $H^{\ast}(f)$ on broad classes, or a family where head
  complexity behaves qualitatively unlike the classical measures.
- Close the remaining gap for the smallest strict-separation dimension, currently known
  to lie between $5$ and $8$.
- Quantify the gap between threshold degree and head complexity beyond the first explicit
  separation.
- Push the formalization in [`head-complexity/`](head-complexity/) to cover more of the
  lemma stack.
- Extend the empirical search to larger $n$ and reconcile it with the proofs. The current
  run flags four provisional $H^{\ast}(f) = 3$ functions at $n = 3$ (see
  [`three_head_functions_n3.md`](three_head_functions_n3.md)); these are estimates
  awaiting proof.

## Repository map

| Path | What it is |
| --- | --- |
| [`problem_statement.md`](problem_statement.md) | The question and the core open problems. |
| [`model.md`](model.md) | The precise attention model and the definition of $H^{\ast}(f)$. |
| [`lemmas.md`](lemmas.md) | Ledger of the main lemmas, their status, and how they fit together. |
| [`lemmas/`](lemmas/) | Full writeups: checkerboard lower bound, threshold upper bounds, the $n$-bit XOR analysis, weighted-sum upper bound. |
| [`writeup.md`](writeup.md) | Longer narrative tying the results together. |
| [`literature_survey.md`](literature_survey.md) | Related work across transformers and Boolean complexity. |
| [`artifacts/calculations/cut_cell_counterexample.md`](artifacts/calculations/cut_cell_counterexample.md) | Short counterexample showing that affine cut cells do not characterize $H^{\ast}$. |
| [`three_head_functions_n3.md`](three_head_functions_n3.md) | Provisional empirical $H^{\ast}=3$ functions at $n=3$. |
| [`head-complexity/`](head-complexity/) | Lean 4 formalization of the results (depends on mathlib). |
| [`src/hstar/`](src/hstar/) | Python package that empirically estimates $H^{\ast}(f)$ by training small attention models. |
| [`proposal.pdf`](proposal.pdf) / [`proposal.tex`](proposal.tex) | Project proposal (build with `./compile_pdf.sh`). |
| [`AGENTS.md`](AGENTS.md) | Markdown conventions used across the writeups. |

New here? Read [`problem_statement.md`](problem_statement.md), then skim
[`lemmas.md`](lemmas.md). The individual files under [`lemmas/`](lemmas/) are self-contained.

## Getting started

**Lean proofs.** Needs [Lean 4 / elan](https://leanprover-community.github.io/get_started.html).

```bash
cd head-complexity
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
./compile_pdf.sh   # runs pdflatex on proposal.tex and cleans up aux files
```
