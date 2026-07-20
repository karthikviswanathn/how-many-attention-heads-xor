# Quadratic threshold functions can require linearly large unrestricted tangential-Chow complexity

Let $\mathrm{tChow}_{\pm}(f)$ denote the least integer $H$ such that $f : \{0,1\}^{n} \to \{0,1\}$ is strictly sign-represented on the Boolean cube by a polynomial of the unrestricted tangential-Chow form

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x),
$$

where $\theta\in\mathbb R$ and $N_h,D_h$ are arbitrary affine real functions of $x_1,\ldots,x_n$. Let $\deg_{\pm}(f)$ be the threshold degree of $f$.

There are absolute constants $c>0$ and $n_0$ such that for every $n\geq n_0$ there exists a Boolean function $f_n : \{0,1\}^{n}\to\{0,1\}$ with

$$
\deg_{\pm}(f_n)=2
$$

and

$$
\mathrm{tChow}_{\pm}(f_n)\geq c n.
$$

Equivalently, even after dropping all attention positivity and admissibility restrictions, unrestricted tangential-Chow complexity can be linearly larger than ordinary threshold degree.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Transcribe Lemmas 20/22, swapping Lemma 19 → Lemma 21 and $\mathcal F_{n,H},H^\ast\to\mathcal T_{n,H},\mathrm{tChow}_\pm$.** Their "Lemma 1" ($2^{m^2/9}$ LTFs) and "Lemma 2" ($2^{n^3/243}$ degree-$2$ PTFs) are about $\deg_\pm$ only and carry over verbatim; the pigeonhole constant $c=\min\{1,a/4C\}$, $a=1/243$ is unchanged. This is the whole proof.
2. **Do the "$\deg_\pm=2$ exactly" upgrade directly in tChow language:** show $\mathrm{tChow}_\pm(f)\le 1\iff\deg_\pm(f)\le 1$ — order $K{=}1$ gives $P=\theta L_1+M_1$, an arbitrary affine form (all LTFs + constants), and order $0$ gives constants. Then $\mathrm{tChow}_\pm(f_n)>H_n\ge1$ forces $\deg_\pm(f_n)\ge2$. (Equivalently route through Lemma 16 + Lemma 11.)
3. **Or upgrade by cardinality, avoiding any characterization:** $\#\{\deg_\pm\le1\}\le 2^{O(n^2)}\ll 2^{n^3/243}$ (Warren/Zuev), so $\{\deg_\pm=2\}$ alone still beats $|\mathcal T_{n,H_n}|$; run the pigeonhole on that subset. Most robust option.
4. **Cite the counting black box as Warren (1968)** (or Milnor–Thom / Basu–Pollack–Roy), exactly as Lemma 21 already does — do not attempt a Mathlib lemma; the multivariate sign-condition bound is not in Mathlib (the `signVariations` hits are univariate Descartes, a false friend).
5. **State the result as the canonical separation** (it implies Lemmas 20/22 via the sandwich $\mathrm{tChow}_\pm\le H^\ast$); the geometric "tangential Chow" naming is descriptive only — the proof needs just degree $\le H$ in $x$ and $\le H+1$ in the parameters.
