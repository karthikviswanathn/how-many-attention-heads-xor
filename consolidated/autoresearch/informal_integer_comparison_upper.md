# Problem: Any function of an integer comparison has head complexity at most its sign-change count

## Background and definitions (self-contained)

Fix $n$ and the **integer value map** $I(x)=\sum_{i=1}^n 2^{i-1}x_i$ on $\{0,1\}^n$ (so $I$ is a bijection $\{0,1\}^n\to\{0,1,\dots,2^n-1\}$: the weights $2^{i-1}$ have **distinct subset sums**). For a function $G:\{-(2^n-1),\dots,2^n-1\}\to\{0,1\}$ define the **integer-comparison predicate** on $2n$ bits
$$
f(x,y) = G\big(I(x)-I(y)\big).
$$

**Established results (cite as given).**
- **(L25, weighted-score sign changes.)** If $h(u)=F(t(u))$ for a positive weighted sum $t(u)=\sum_k c_k u_k$ ($c_k>0$) and $F:\mathrm{Im}(t)\to\{0,1\}$, then $H^{*}(h)\le C(F)$, the number of sign changes of $F$ along the increasing order of $\mathrm{Im}(t)$.
- **(L15, negation/permutation closure.)** Flipping any input variable $u_k\mapsto 1-u_k$ leaves $H^{*}$ unchanged.
- **(L22, flattening.)** $\mathrm{sr}_{x|y}(h)\le (H^{*}(h)+1)2^{H^{*}(h)}+1$ for the $x|y$ sign-rank.

Write $C(G)$ for the number of sign changes of $G$ along the increasing integer order of its domain.

## Claim to prove

$$
H^{*}(f) \;\le\; C(G), \qquad\text{and consequently}\qquad \mathrm{sr}_{x|y}(f)\le (C(G)+1)2^{C(G)}+1 .
$$
In particular, if $C(G)$ is bounded (independent of $n$) then $f$ has constant head complexity and bounded sign-rank.

## Guidance (prove every step rigorously)

1. **Flip $y$ to positive weights.** By L15, $H^{*}(f)=H^{*}(g)$ where $g(x,z)=f(x,\overline z)$ replaces each $y_i$ by $z_i=1-y_i$. Then
$$
I(x)-I(y)=\sum_i 2^{i-1}x_i-\sum_i 2^{i-1}(1-z_i)=\Big(\sum_i 2^{i-1}x_i+\sum_i 2^{i-1}z_i\Big)-(2^n-1)=t-(2^n-1),
$$
with $t(x,z)=\sum_i 2^{i-1}x_i+\sum_i 2^{i-1}z_i$ a **positive** weighted sum (all weights $2^{i-1}>0$). So $g(x,z)=G\big(t-(2^n-1)\big)=F(t)$ with $F(s):=G(s-(2^n-1))$.

2. **The image of $t$ is a full integer interval.** Each $x_i+z_i\in\{0,1,2\}$, so $t=\sum_i 2^{i-1}(x_i+z_i)$ is a base-$2$ number with digits in $\{0,1,2\}$ (redundant binary). Show $\mathrm{Im}(t)=\{0,1,\dots,2(2^n-1)\}$ (every integer in $[0,2(2^n-1)]$ is representable with digits $0,1,2$ — e.g. greedily, or induct on $n$: $[0,2(2^{n}-1)]$ is covered because the top digit contributes $\{0,2^{n-1},2^{\,n}\}$ and the lower $n-1$ digits already cover $[0,2(2^{n-1}-1)]$, and these shifted copies overlap). Hence as $s=I(x)-I(y)=t-(2^n-1)$ ranges over $\{-(2^n-1),\dots,2^n-1\}$ (all integers, since $I(x),I(y)$ independently realize $\{0,\dots,2^n-1\}$), every value of $G$'s domain is hit.

3. **Sign changes are preserved by the shift.** $F(s)=G(s-(2^n-1))$ is $G$ composed with a translation of the integer line; the increasing order of $\mathrm{Im}(t)$ maps order-isomorphically to the increasing order of $G$'s domain, so $C(F)=C(G)$.

4. **Apply L25 and L22.** By L25, $H^{*}(g)\le C(F)=C(G)$; with step 1, $H^{*}(f)\le C(G)$. The sign-rank bound is then immediate from L22.

## Consequences (state briefly)

| predicate | $G(d)$ | $C(G)$ | bound |
|---|---|---|---|
| $\mathrm{GT}$: $x>y$ | $\mathbf 1[d>0]$ | $1$ | $H^{*}\le 1$ (an LTF) |
| $\mathrm{EQ}$: $x=y$ | $\mathbf 1[d=0]$ | $2$ | $H^{*}\le 2$ |
| integer band $a\le d\le b$ | $\mathbf 1[a\le d\le b]$ | $\le 2$ | $H^{*}\le 2$ |
| approximate equality $\lvert d\rvert\le k$ | $\mathbf 1[-k\le d\le k]$ | $2$ | $H^{*}\le 2$ |

So **every** predicate that depends only on the comparison of the two strings as integers is cheap, with cost equal to the number of sign changes of $G$ and **bounded sign-rank**. This delineates the "easy" side of head complexity: it is the upper-bound counterpart to the shatter-rectangle lower-bound certificate (L37), and it explains why these predicates can never separate $H^{*}$ from threshold degree (bounded $H^{*}$ forces bounded sign-rank, hence no flattening lower bound).

## Pitfalls

- The $y$-flip (L15) is what makes all weights positive; without it the score $\sum 2^{i-1}x_i-\sum 2^{i-1}y_i$ has mixed-sign weights and L25 does not apply. State it.
- Any **super-increasing** positive weight sequence works in place of $2^{i-1}$ (distinct subset sums is all that is used); the specific base-$2$ choice is only to make $\mathrm{Im}(t)$ a clean full interval.
- $C(F)=C(G)$ because the map $t\mapsto t-(2^n-1)$ is an order isomorphism on integers; do not miscount by conflating the value $0$ of $d$ with an endpoint (it is interior whenever both $d<0$ and $d>0$ occur, which holds for $n\ge1$).
