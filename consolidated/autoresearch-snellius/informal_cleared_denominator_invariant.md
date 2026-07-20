# Cleared-Denominator Polynomial Invariant

Let $f : \{0,1\}^{n} \to \{0,1\}$ and let $H^{*}(f)$ be the least number of attention heads needed in the one-layer model of `model.md`, with a final strict threshold at the query token.\n\nCall an affine pair $(N,D)$ admissible if it is exactly one of the affine one-head pairs from Lemma 13: $D>0$ on the cube, $D$ is either constant positive, has all nonzero coordinate coefficients positive, or has all nonzero coordinate coefficients negative with positive value at $\mathbf 1$; if $D$ is nonconstant then $N$ is arbitrary affine, while if $D$ is constant then the coordinate coefficients of $N$ are sign-uniform as in Lemma 13.\n\nDefine $\mathrm{MFdeg}_{\pm}(f)$ to be the least $H \geq 0$ for which there exist admissible affine pairs $(N_h,D_h)$, $1 \leq h \leq H$, and a real constant $\theta$ such that the polynomial\n\n$$\nP(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x)\n$$\nstrictly sign-represents $f$ on $\{0,1\}^{n}$, meaning $P(x)>0$ when $f(x)=1$ and $P(x)<0$ when $f(x)=0$. For $H=0$, the empty product is $1$ and the sum is $0$.\n\nThen\n\n$$\nH^{*}(f)=\mathrm{MFdeg}_{\pm}(f).\n$$

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Prove as a corollary, not afresh:** chain $H^*(f)\overset{\text{L10}}{=}L_{\mathrm{frac}}(f)\overset{\text{clear}}{=}\mathrm{MFdeg}_\pm(f)$, reusing the clearing identity already written in Lemma 13's *Consequence*.
2. **Positivity engine:** $\prod_h D_h(x)>0$ via `Finset.prod_pos` (each $D_h>0$ from Lemma 13); multiplication/division by it preserves the sign pattern on $\{0,1\}^n$.
3. **Strictness:** upgrade Lemma 10's one-sided `iff` to strict two-sided by perturbing the global constant $c\to c-\epsilon$, $0<\epsilon<$ (min positive margin over the finite cube); leaves all $(N_h,D_h)$ and the shape of $P$ unchanged.
4. **Pin the definition:** read "admissible" as Lemma 13's *exact* three denominator classes (all-zero / all-positive / all-negative coordinate coeffs), not the looser prose — the reverse direction depends on it.
5. **Free consistency check + downstream payoff:** $\deg P\le H$ re-derives Lemma 6 ($\deg_\pm\le H^*$); and via rational degree (Iyer et al. 2023) any $\mathrm{rdeg}_\pm$ lower bound becomes an $H^*$ lower bound.
