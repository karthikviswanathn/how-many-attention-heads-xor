# Bitwise Equality Has Head Complexity Exactly Two

## Statement

For $\mathrm{EQ}_n(x,y) = \mathbf 1[x = y] = \bigwedge_{i=1}^n \overline{(x_i\oplus y_i)}$ on $2n$ bits (the AND of $n$ disjoint XNORs),
$$
H^{*}(\mathrm{EQ}_n) = 2 \qquad\text{for all } n\ge 1 .
$$

> **Equality is constant-head because string equality linearizes.** Despite being an AND of $n$ checkerboards — each XNOR alone forces $H^{*}=2$ (L3) — the whole conjunction still needs only two heads. With super-increasing weights $w_i=2^{i-1}$ the integers $I(x)=\sum w_i x_i$ have **distinct subset sums**, so $x=y \iff I(x)=I(y)$, a single comparison: after flipping the $y$-inputs (free, L15) $\mathrm{EQ}_n$ becomes the degenerate single-value weighted band $\mathbf 1[t = 2^n-1]$ of one *positive* weighted sum $t$, hence $H^{*}\le 2$ (L25/L44); the XNOR-checkerboard restriction gives $\ge 2$ (L3). This is the sharp foil to set intersection $\mathrm{INT}_n$ on the same $2n$ bits, which is $\widetilde\Theta(n)$ (L35/L45): "all pairs equal" is one linear comparison, "some pair both-$1$" is irreducibly multiplicative.

## Proof

**Upper bound.** By negation/permutation closure ([015](../04_closure_and_structure/015_negation_permutation_closure.md)), $H^{*}(\mathrm{EQ}_n)=H^{*}(g)$ where $g(x,z)=\mathrm{EQ}_n(x,\overline z)$ replaces each $y_i$ by $z_i=1-y_i$; since $x_i=y_i\iff x_i+z_i=1$, $g(x,z)=\mathbf 1[x_i+z_i=1\ \forall i]$. Put $w_i=2^{i-1}>0$, the positive weighted sum $t(x,z)=\sum_i w_i x_i+\sum_i w_i z_i$, and $W=\sum_i w_i=2^n-1$.

*Claim $g=\mathbf 1[t=W]$.* If every $x_i+z_i=1$ then $t=\sum_i w_i=W$. Conversely $t=W$ gives $\sum_i w_i\big((x_i+z_i)-1\big)=0$ with each coefficient in $\lbrace-1,0,1\rbrace$; the weights $2^{i-1}$ have distinct subset sums over $\lbrace-1,0,1\rbrace$ coefficients ($|\sum_{i<n}\epsilon_i 2^{i-1}|\le 2^{n-1}-1<2^{n-1}$ forces $\epsilon_n=0$, then induct), so every $x_i+z_i=1$.

$W=2^n-1$ is strictly interior to $\mathrm{Im}(t)=\lbrace0,\dots,2(2^n-1)\rbrace$, so $F(s)=\mathbf 1[s=W]$ has exactly $C(F)=2$ sign changes; by the weighted-score bound ([025](025_weighted_score_upper.md), the degenerate $\theta_1=\theta_2$ band of [044](044_weighted_band.md)), $H^{*}(g)\le 2$. Hence $H^{*}(\mathrm{EQ}_n)\le 2$.

**Lower bound.** Fix $x_k=y_k=0$ for $k\ge 2$; then $\mathrm{EQ}_n$ restricts to $\mathbf 1[x_1=y_1]$, which is $1$ on $\lbrace(0,0),(1,1)\rbrace$ and $0$ on $\lbrace(0,1),(1,0)\rbrace$ — a 2-bit checkerboard. By the checkerboard obstruction ([003](../01_foundations_and_normal_form/003_checkerboard_obstruction.md)), $H^{*}(\mathrm{EQ}_n)\ge 2$. $\blacksquare$

## Consequence: a taxonomy of pair-predicates

The upper bound is one instance of a general principle: **any Boolean function of the integer difference** $d=I(x)-I(y)$ (super-increasing weights, so $d$ ranges over a contiguous integer interval) has $H^{*}\le C(G)$ where $f=G(d)$ — because $d$ is, after flipping $y$, a positive weighted sum (L25). So all "integer-comparison" predicates are cheap:

| predicate | as a function of $d=I(x)-I(y)$ | $H^{*}$ |
|---|---|---|
| $\mathrm{GT}$: $x>y$ | $\mathbf 1[d>0]$ | $1$ |
| $\mathrm{EQ}$: $x=y$ | $\mathbf 1[d=0]$ | $2$ |
| integer band $a\le d\le b$ | $\mathbf 1[a\le d\le b]$ | $\le 2$ |
| approx. equality $\lvert d\rvert\le k$ | $\mathbf 1[-k\le d\le k]$ | $2$ |

By contrast the **set-theoretic** pair-predicates are irreducibly multiplicative, $\widetilde\Theta(n)$: set intersection $\mathrm{INT}_n=\bigvee_i(x_i\wedge y_i)$ (L35/L45), and subset $x\subseteq y=\neg\,\mathrm{INT}_n(x,\overline y)$ (so $H^{*}(\subseteq)=H^{*}(\mathrm{INT}_n)=\widetilde\Theta(n)$ by L15). The dividing line is exactly whether the predicate collapses to a single linear comparison of the two strings or requires detecting a coordinate-wise conjunction across an OR (which a positive linear order interleaves $2^n$ times: $A_{+}(\mathrm{INT}_n)=2^n-1$).

## Remarks

- The $y$-flip (L15) is essential: in the original $(x,y)$ the natural score $\sum w_i x_i-\sum w_i y_i$ has mixed-sign weights, which the weighted-score bound forbids; flipping $y$ makes all weights positive.
- The distinct-subset-sum property is needed over $\lbrace-1,0,1\rbrace$ coefficients (not just $\lbrace0,1\rbrace$); any super-increasing positive sequence works in place of $2^{i-1}$.
- $\mathrm{EQ}_n$ joins the exact-value catalog of nonsymmetric (cut-)functions: $\mathrm{INT}_2,\mathrm{INT}_3$ ($=2$, L27/L39), products ($\le2$, L41/L42), weighted bands ($=2$, L44), now equality ($=2$). It is the cheapest natural $2n$-bit pair-predicate that is not a single threshold.
