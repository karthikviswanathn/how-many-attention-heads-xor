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
readout from the query token. A Boolean function $f : \{0,1\}^n \to \{0,1\}$ is
*computable with $H$ heads* if some choice of embeddings, attention parameters, and
readout reproduces $f$ on every input. Define

$$
H^{*}(f) \;:=\; \min\{\, H : f \text{ is computable with } H \text{ heads} \,\}.
$$

The central problem: **understand $H^{*}(f)$** as a function of $f$. Prove lower and upper
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
  $H^{*}(f) \geq 2$. One head can never separate the two diagonals.
- *Threshold-degree bound.* Head complexity dominates threshold degree:
  $\deg_{\pm}(f) \leq H^{*}(f)$.

**Upper bounds (a function needs few heads).**
- *Symmetric thresholds need one head.* Every $T_{n,t}(x) = \mathbf{1}[\,|x| \geq t\,]$ is
  computable with a single head, so $H^{*}(\mathrm{AND}_n) = H^{*}(\mathrm{OR}_n) =
  H^{*}(\mathrm{MAJORITY}_n) = 1$.
- *Weighted-sum interpolation.* If $f(x) = F\!\left(\sum_i \lambda_i x_i\right)$ for
  positive weights $\lambda_i$ and the weighted sum takes $M$ distinct values, then
  $H^{*}(f) \leq M - 1$. Consequently every symmetric function needs at most $n$ heads and
  every Boolean function at most $2^n - 1$.

**Exact answers.**
- *Parity is the extremal case.* $H^{*}(\mathrm{XOR}_n) = n$: in this model, parity needs
  exactly one head per input bit. The lower bound comes from $\deg_{\pm}(\mathrm{PARITY}_n)
  = n$, the upper bound from an explicit $n$-head construction.
- A first split inside the symmetric functions: monotone thresholds have complexity $1$,
  while parity and the internal exact-count predicates $\mathrm{EXACT}_{n,k}$ need at
  least $2$.

Taken together this is a *partial* characterization, not yet a single invariant
$I(f)$ with $H^{*}(f) \asymp I(f)$. Closing that gap is the main open problem.

## Open directions

- Find an invariant that pins down $H^{*}(f)$ on broad classes, or a family where head
  complexity behaves qualitatively unlike the classical measures.
- Tighten the gap between the threshold-degree lower bound and the weighted-sum upper
  bound.
- Push the formalization in [`head-complexity/`](head-complexity/) to cover more of the
  lemma stack.
- Extend the empirical search to larger $n$ and reconcile it with the proofs. The current
  run flags four provisional $H^{*}(f) = 3$ functions at $n = 3$ (see
  [`three_head_functions_n3.md`](three_head_functions_n3.md)); these are estimates
  awaiting proof.

## Repository map

| Path | What it is |
| --- | --- |
| [`problem_statement.md`](problem_statement.md) | The question and the core open problems. |
| [`model.md`](model.md) | The precise attention model and the definition of $H^{*}(f)$. |
| [`lemmas.md`](lemmas.md) | Ledger of the main lemmas, their status, and how they fit together. |
| [`lemmas/`](lemmas/) | Full writeups: checkerboard lower bound, threshold upper bounds, the $n$-bit XOR analysis, weighted-sum upper bound. |
| [`writeup.md`](writeup.md) | Longer narrative tying the results together. |
| [`literature_survey.md`](literature_survey.md) | Related work across transformers and Boolean complexity. |
| [`three_head_functions_n3.md`](three_head_functions_n3.md) | Provisional empirical $H^{*}=3$ functions at $n=3$. |
| [`head-complexity/`](head-complexity/) | Lean 4 formalization of the results (depends on mathlib). |
| [`src/hstar/`](src/hstar/) | Python package that empirically estimates $H^{*}(f)$ by training small attention models. |
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
attention models with increasing head counts to estimate $H^{*}(f)$.

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
