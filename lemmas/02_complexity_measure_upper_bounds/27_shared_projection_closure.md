# Shared Projection Boolean Closure

## Statement

Let

$$
t(x)=\sum_{i=1}^{n}\lambda_i x_i,
\qquad
\lambda_i>0,
$$

and write its image in increasing order as

$$
\tau_0<\tau_1<\cdots<\tau_{M-1}.
$$

Suppose Boolean functions $f_1,\ldots,f_m$ all factor through this same statistic:

$$
f_j(x)=F_j(t(x)),
\qquad
F_j:\operatorname{Im}(t)\to\{0,1\}.
$$

Let

$$
G:\{0,1\}^m\to\{0,1\}
$$

be any Boolean operation, and define

$$
g(x):=G(f_1(x),\ldots,f_m(x)).
$$

Then

$$
H^{*}(g)
\leq
C_t(g)
\leq
\sum_{j=1}^{m}C_t(f_j),
$$

where $C_t(h)$ denotes the number of sign changes of $h$ along the ordered image of $t$.

In particular,

$$
H^{*}(g)\leq M-1.
$$

> **Interpretation.** Once several functions are functions of the same positive weighted sum, arbitrary Boolean combinations stay in the same one-dimensional world. The cost is controlled by the number of new label changes along that shared statistic, not by recomputing the inputs separately.

## Proof

Define

$$
G_t(\tau):=G(F_1(\tau),\ldots,F_m(\tau))
$$

for $\tau\in\operatorname{Im}(t)$. Then

$$
g(x)=G_t(t(x)),
$$

so $g$ also factors through $t$.

By the positive-projection sign-change theorem [07_positive_projection_sign_changes.md](07_positive_projection_sign_changes.md),

$$
H^{*}(g)\leq C_t(g).
$$

It remains to compare sign-change counts. If $G_t$ changes between adjacent levels $\tau_{\ell-1}$ and $\tau_{\ell}$, then the vector

$$
\bigl(F_1(\tau),\ldots,F_m(\tau)\bigr)
$$

must change between those two levels. Therefore at least one of the component functions $F_j$ changes between $\tau_{\ell-1}$ and $\tau_{\ell}$.

Thus the set of adjacent cuts where $G_t$ changes is contained in the union of the adjacent cuts where some $F_j$ changes. Hence

$$
C_t(g)
\leq
\sum_{j=1}^{m}C_t(f_j).
$$

Since there are only $M$ projection levels, every label sequence has at most $M-1$ sign changes, so

$$
H^{*}(g)\leq C_t(g)\leq M-1.
$$

$\blacksquare$

## Consequence

For two functions $f$ and $g$ sharing the same statistic $t$,

$$
H^{*}(f\wedge g),
\quad
H^{*}(f\vee g),
\quad
H^{*}(f\oplus g)
\leq
C_t(f)+C_t(g).
$$

This explains why Boolean combinations of co-statistical functions should not be treated by a generic sum-of-heads construction. The shared statistic already supplies the basis.
