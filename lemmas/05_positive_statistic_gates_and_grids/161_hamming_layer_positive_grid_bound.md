# Hamming-Layer Positive Grid Bound

## Statement

Let $z\in\{0,1\}^{k}$ and $y\in\{0,1\}^{m}$. Suppose

$$
f(z,y)=F(\lvert z\rvert,t(y)),
\qquad
t(y)=\sum_{i=1}^{m}\lambda_i y_i,
\qquad
\lambda_i>0.
$$

For each Hamming layer $r\in\{0,\ldots,k\}$, let $C_r$ be the sign-change count of

$$
\tau\mapsto F(r,\tau)
$$

along the ordered image of $t$. Let

$$
J_{\mathrm{Ham}}
:=
\left\lvert
\left\{
r\in\{0,\ldots,k-1\}:
F(r,\tau_{M-1})\neq F(r+1,\tau_0)
\right\}
\right\rvert.
$$

Then

$$
\max_{0\leq r\leq k}H^{*}\bigl(F(r,t(y))\bigr)
\leq
H^{*}(f)
\leq
\sum_{r=0}^{k}C_r+J_{\mathrm{Ham}}.
$$

If each Hamming-layer slice has a univariate sign polynomial in $t$ of degree at most $d_r$, then

$$
H^{*}(f)\leq\sum_{r=0}^{k}d_r+J_{\mathrm{Ham}}.
$$

If $d_r\leq d$ for all $r$, then

$$
H^{*}(f)\leq(k+1)d+J_{\mathrm{Ham}}.
$$

> **Interpretation.** A raw block that appears only through Hamming weight costs $k+1$ raw layers, not $2^k$ raw assignments.

## Proof

Apply the positive grid slice sandwich [159_positive_grid_slice_sandwich.md](159_positive_grid_slice_sandwich.md) with

$$
u(z)=\lvert z\rvert.
$$

The image of $u$ is $0,1,\ldots,k$, so the grid boundary term is exactly $J_{\mathrm{Ham}}$. This gives the first bracket.

The degree bounds follow from [160_positive_grid_degree_exactness.md](160_positive_grid_degree_exactness.md), again with $u(z)=\lvert z\rvert$. $\blacksquare$

## Consequence

This theorem gives a dimension-free upper bound for functions depending on a raw block only through Hamming weight and on the remaining variables through one positive statistic.
