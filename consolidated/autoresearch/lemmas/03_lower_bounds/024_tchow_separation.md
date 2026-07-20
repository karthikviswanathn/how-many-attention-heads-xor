# Positivity Is Not the Source of the Separation

## Statement

Recall $\mathrm{tChow}_{\pm}(f)$ (the cleared tangent form with *arbitrary* affine factors, no positivity), with $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$ [018_tchow_sandwich.md](../01_foundations_and_normal_form/018_tchow_sandwich.md).

**Theorem.**

**(a)** $\#\lbrace f : \mathrm{tChow}_{\pm}(f) \leq H\rbrace \leq 2^{O(Hn^2)}$ for $H \geq 1$ and large $n$.

**(b)** For all large $n$, some $f$ has $\deg_{\pm}(f) \leq 2$ and $\mathrm{tChow}_{\pm}(f) = \Omega(n)$; hence (since $\mathrm{tChow}_{\pm} \leq H^{*}$) the same $f$ has $H^{*}(f) = \Omega(n)$.

> **What this says about the positivity question (F4).** The separation of head complexity from threshold degree is **already present without the attention positivity/one-sided-slope constraints**. So those constraints are *not* the cause of the $\deg_{\pm}$-to-$H^{*}$ gap: the tangent-to-products-of-affine-forms structure alone already forces it. Whether positivity adds any *further* cost (i.e. whether $\mathrm{tChow}_{\pm}(f) < H^{*}(f)$ for some $f$) is the remaining open part of F4.

## External inputs

Warren 1968 (sign-pattern bound) and the degree-2 PTF count $\geq 2^{c_0 n^3}$ (Baldi-Vershynin 2019), exactly as in [023_counting_separation.md](023_counting_separation.md).

## Proof

**Part (a).** A $\mathrm{tChow}_{\pm}$-witness of order $H$ is a parameter vector $w \in \mathbb{R}^p$ holding the coefficients of the $H$ affine pairs $(N_h, D_h)$ and $\theta$, with $p = 2H(n+1)+1 = \Theta(Hn)$ (pad a shorter witness to exactly $H$ pairs by $D_h \equiv 1$, $N_h \equiv 0$, which is affine and leaves $P$ unchanged). For each $x$, $q_x(w) = \theta\prod_h D_h(x) + \sum_h N_h(x)\prod_{g\neq h}D_g(x)$ is degree $\leq H+1$ in $w$, and $f(x) = 1 \iff q_x(w) > 0$; so $f$ is the sign vector $(\mathrm{sgn}\,q_x(w))_x$. By Warren with $m = 2^n$, $d = H+1$, $p = \Theta(Hn)$, the number of realized sign vectors is at most $(C(H+1)2^n/p)^p$, giving $\log_2\#\lbrace f : \mathrm{tChow}_{\pm}(f)\leq H\rbrace \leq O(Hn^2)$.

**Part (b).** If every degree-2 PTF had $\mathrm{tChow}_{\pm} \leq \lfloor\gamma n\rfloor$ ($\gamma = c_0/(2c_1)$), then $2^{c_0 n^3} \leq 2^{c_1\gamma n^3} = 2^{(c_0/2)n^3}$, a contradiction for large $n$. So some $\deg_{\pm}=2$ function has $\mathrm{tChow}_{\pm} = \Omega(n)$, hence $H^{*} = \Omega(n)$. $\blacksquare$

## Consequence

This refines the counting separation [023_counting_separation.md](023_counting_separation.md): the parameter-counting argument never used $D_h > 0$ or one-sided slopes, so the entire $\Omega(n)$ separation survives at the positivity-free level. The map of the first core question is now:

$$
\deg_{\pm}(f) \;\le\; \mathrm{tChow}_{\pm}(f) \;\le\; H^{*}(f),
$$

with the left gap already $\Omega(n)$ for some $\deg_{\pm}=2$ function (tangent structure), and the right gap (the cost of positivity) the open F4 question.
