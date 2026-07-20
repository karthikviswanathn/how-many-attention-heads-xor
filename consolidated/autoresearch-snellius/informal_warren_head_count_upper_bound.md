# Warren Counting Bound for Low Head Complexity

For integers $n\geq 1$ and $H\geq 1$, let\n\n$$\n\mathcal{F}_{n,H}:=\{f:\{0,1\}^{n}\to\{0,1\}: H^{\ast}(f)\leq H\}.\n$$\n\nHere $H^{\ast}(f)$ is the least number of heads in the one-layer attention model of `model.md` that computes $f$ by a strict final threshold. Then there is an absolute constant $C>0$ such that\n\n$$\n\log_2 |\mathcal{F}_{n,H}| \leq C H n\bigl(n+\log(H+1)\bigr).\n$$\n\nEquivalently, the class of Boolean functions computable with at most $H$ heads has at most\n\n$$\n2^{C H n(n+\log(H+1))}\n$$\n\npossible sign patterns on the Boolean cube.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Cite Goldberg–Jerrum (1995) / Warren (1968)** as the black box: $\#\{\text{sign patterns of }m\text{ degree-}d\text{ polys in }\ell\text{ vars}\}\le(4edm/\ell)^\ell$ for $m\ge\ell$ — this is the entire engine.
2. **Build the polynomial from Lemmas 13 + 14**: each $f$ with $H^\ast(f)\le H$ is $\mathbf 1[P(x;\Theta)>0]$ with $\deg_\Theta P\le H+1=O(H)$ and $\ell=O(Hn)$ parameters; verify these two constants explicitly — they are the only quantitative risk.
3. **Count directly, not via VC dimension**: the direct sign-pattern count gives $O(Hn^2)\le CHn(n+\log(H{+}1))$; the VC+Sauer–Shelah route gives $O(Hn^2\log H)$ and fails to prove the stated bound.
4. **Use the sign-*condition* count (Basu–Pollack–Roy) to absorb $P=0$**, and **split off the $\ell>m=2^n$ regime** with the trivial $2^{2^n}$ bound.
5. **Sanity-check at $H=1$** against $\#\mathrm{LTF}_n=2^{n^2(1-o(1))}$ (Cover 1965; Zuev 1989) to confirm the leading $Hn^2$ order is correct.
