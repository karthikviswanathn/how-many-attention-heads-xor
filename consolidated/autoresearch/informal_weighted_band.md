# Problem: The head complexity of a weighted band is exactly two

## Background and definitions (self-contained)

Fix positive reals $w_1,\dots,w_n > 0$ and let $t(x) = \sum_i w_i x_i$ on $\lbrace 0,1\rbrace^n$. For reals $\theta_1 \leq \theta_2$, the **weighted band** is
$$
f(x) = \mathbf 1[\,\theta_1 \leq t(x) \leq \theta_2\,].
$$
(This is the positive-weight, nonsymmetric generalization of the symmetric exact-count band $\mathrm{EXACT}_{n,k} = \mathbf 1[\lvert x\rvert = k]$.)

**Established (cite as given).**
- **(L25, weighted-score sign changes.)** If $f(x) = F(t(x))$ for a positive weighted sum $t$ and $F : \mathrm{Im}(t)\to\lbrace0,1\rbrace$, then $H^{*}(f) \leq C(F)$, the number of sign changes of $F$ along the increasing order of $\mathrm{Im}(t)$.
- **(L3, checkerboard obstruction.)** If $f$ has a 2-bit checkerboard restriction — two coordinates $i\neq j$ and a fixed assignment to the others under which $f$ restricted to $(x_i,x_j)$ takes value $a$ on $\lbrace(0,0),(1,1)\rbrace$ and $b\neq a$ on $\lbrace(0,1),(1,0)\rbrace$ — then $H^{*}(f) \geq 2$.
- **(L2, antipode identity.)** For affine $t$ and any restriction to coordinates $i,j$ (others fixed), $t_{00} + t_{11} = t_{01} + t_{10}$, where $t_{bc}$ is $t$ with $x_i=b, x_j=c$.

## Claim to prove

**(a)** Every weighted band $f$ has $H^{*}(f) \leq 2$.

**(b)** If moreover there exist coordinates $i\neq j$ and an assignment to the remaining coordinates such that, with the four restricted values $t_{00} \leq t_{01}, t_{10} \leq t_{11}$ (using $w_i, w_j > 0$),
$$
t_{00} < \theta_1, \qquad \theta_1 \leq t_{01}, t_{10} \leq \theta_2, \qquad t_{11} > \theta_2,
$$
then $H^{*}(f) = 2$.

## Guidance (prove every step rigorously)

**Part (a).** $f(x) = F(t(x))$ with $F(s) = \mathbf 1[\theta_1\leq s\leq\theta_2]$ and $t = \sum_i w_i x_i$ a positive weighted sum. Along the increasing order of $\mathrm{Im}(t)$, $F$ is $0$ for $s<\theta_1$, then $1$ for $\theta_1\leq s\leq\theta_2$, then $0$ for $s>\theta_2$; so $F$ has at most two sign changes, $C(F)\leq 2$. By L25, $H^{*}(f)\leq C(F)\leq 2$. *(If $F$ has fewer than two sign changes — e.g. the band is empty, all of $\mathrm{Im}(t)$, or one-sided — then $H^{*}(f)\leq 1$; part (a) still holds.)*

**Part (b).** Under the stated condition, restrict to coordinates $i, j$ with the others fixed as given. Since $w_i, w_j > 0$, the four values satisfy $t_{00} \leq t_{01}, t_{10} \leq t_{11}$ and (by L2) $t_{00} + t_{11} = t_{01} + t_{10}$. The hypotheses give:
- $t_{00} < \theta_1$, so $f$ at $(x_i,x_j)=(0,0)$ is $0$;
- $\theta_1 \leq t_{01} \leq \theta_2$ and $\theta_1 \leq t_{10} \leq \theta_2$, so $f$ at $(0,1)$ and $(1,0)$ is $1$;
- $t_{11} > \theta_2$, so $f$ at $(1,1)$ is $0$.

Thus the restriction is a 2-bit checkerboard ($0$ on the diagonal $\lbrace(0,0),(1,1)\rbrace$, $1$ on the anti-diagonal $\lbrace(0,1),(1,0)\rbrace$). By L3, $H^{*}(f) \geq 2$. With part (a), $H^{*}(f) = 2$. $\blacksquare$

## Pitfalls

- Part (a) uses only that $t$ is a positive weighted sum and $F$ is an interval indicator (two sign changes); state $C(F)\leq 2$ carefully (handle degenerate bands giving $\leq 1$).
- Part (b)'s checkerboard is the *anti-diagonal-in-band* pattern: the two middle values $t_{01}, t_{10}$ (which lie between $t_{00}$ and $t_{11}$, and whose sum equals $t_{00}+t_{11}$) fall inside $[\theta_1,\theta_2]$ while the extreme values $t_{00}, t_{11}$ fall outside. A band containing the two *extremes* would, being an interval, contain everything between — so only the anti-diagonal pattern can occur, never the diagonal one.
- The condition in (b) is exactly "the band is proper enough to straddle some pair": it holds for any band that excludes a low and a high value while including two incomparable middle values; it is the nonsymmetric analogue of $\mathrm{EXACT}_{n,k}$ being non-monotone.
