# Any Function of an Integer Comparison Is Cheap

## Statement

Let $I(x)=\sum_{i=1}^n 2^{i-1}x_i$ be the integer value of $x\in\{0,1\}^n$ (the weights $2^{i-1}$ have distinct subset sums, so $I$ is a bijection onto $\{0,\dots,2^n-1\}$). For any $G:\{-(2^n-1),\dots,2^n-1\}\to\{0,1\}$, the **integer-comparison predicate** $f(x,y)=G\big(I(x)-I(y)\big)$ on $2n$ bits satisfies
$$
H^{*}(f)\le C(G),\qquad \mathrm{sr}_{x|y}(f)\le (C(G)+1)2^{C(G)}+1,
$$
where $C(G)$ is the number of sign changes of $G$ along the integer order of its domain.

> **The easy side of head complexity, delineated.** Whatever the model needs to do, if it only depends on *comparing the two strings as integers* it is cheap — with cost exactly the number of sign changes of $G$, and **bounded** sign-rank whenever $C(G)$ is bounded. This is the upper-bound counterpart of the shatter-rectangle lower-bound certificate (L37): it explains why such predicates can never separate $H^{*}$ from threshold degree (bounded $H^{*}$ forces bounded sign-rank, so flattening gives nothing), and it unifies the constant-head catalog — greater-than ($H^{*}=1$), equality ($H^{*}=2$, L46), integer/approximate-equality bands ($\le2$, L44). The hard predicates are exactly the ones that are *not* functions of the integer comparison: the bilinear ones (intersection, subset, interior Hamming), where the matrix has growing sign-rank.

## Proof

**Flip $y$ to positive weights (L15, [015](../04_closure_and_structure/015_negation_permutation_closure.md)).** $H^{*}(f)=H^{*}(g)$ where $g(x,z)=f(x,\overline z)$ substitutes $z_i=1-y_i$. Then
$$
I(x)-I(y)=\sum_i 2^{i-1}x_i-\sum_i 2^{i-1}(1-z_i)=t-(2^n-1),\quad t=\sum_i 2^{i-1}(x_i+z_i),
$$
a positive weighted sum. So $g=F(t)$ with $F(s)=G(s-(2^n-1))$.

**$\mathrm{Im}(t)$ is a full interval.** Each $x_i+z_i\in\{0,1,2\}$, so $t$ is a base-$2$ number with digits in $\{0,1,2\}$. By induction on $n$ every integer in $[0,2(2^n-1)]$ is representable: the top digit contributes $\{0,2^{n-1},2^n\}$ and the lower $n-1$ digits cover $[0,2(2^{n-1}-1)]$; the three shifted copies $[0,2(2^{n-1}-1)]$, $2^{n-1}+[\cdot]$, $2^n+[\cdot]$ overlap and union to $[0,2(2^n-1)]$. Since $I(x),I(y)$ independently realize $\{0,\dots,2^n-1\}$, $d=I(x)-I(y)$ realizes every integer in $\{-(2^n-1),\dots,2^n-1\}$, so $G$'s whole domain is used.

**Sign changes preserved.** $t\mapsto t-(2^n-1)$ is an order isomorphism of integers, so $C(F)=C(G)$.

**Conclude (L25, [025](025_weighted_score_upper.md); L22, [022](../03_lower_bounds/022_flattening_lower_bound.md)).** $H^{*}(g)\le C(F)=C(G)$, hence $H^{*}(f)\le C(G)$; the sign-rank bound is flattening. $\blacksquare$

## Consequences

| predicate | $G(d)$ | $C(G)$ | bound |
|---|---|---|---|
| $\mathrm{GT}$: $x>y$ | $\mathbf 1[d>0]$ | $1$ | $H^{*}\le 1$ |
| $\mathrm{EQ}$: $x=y$ | $\mathbf 1[d=0]$ | $2$ | $H^{*}\le 2$ ([046](046_equality_exact.md)) |
| integer band $a\le d\le b$ | $\mathbf 1[a\le d\le b]$ | $\le 2$ | $H^{*}\le 2$ |
| approximate equality $\lvert d\rvert\le k$ | $\mathbf 1[-k\le d\le k]$ | $2$ | $H^{*}\le 2$ |

Any super-increasing positive weight sequence works in place of $2^{i-1}$; the base-$2$ choice only makes $\mathrm{Im}(t)$ a clean interval. The dividing line of the pair-predicate taxonomy is exactly this: *functions of the linear integer comparison* are cheap (this lemma); the *bilinear* predicates $\mathrm{INT}_n=\mathbf 1[\langle x,y\rangle\ge1]$ (L35/L45), subset, and interior Hamming are $\widetilde\Theta(n)$.
