# The Minimized Positive-Order Alternation Number

## Statement

A positive weight $w$ ($w_i > 0$) is **generic** if $t_w(x) = \sum_i w_i x_i$ takes $2^n$ distinct values on the cube (e.g. $w_i = 2^{i-1}$). A generic positive $w$ totally orders the cube as $x^{(1)},\dots,x^{(2^n)}$ by increasing $t_w$. Define the **alternation count** and the **minimized positive-order alternation number**

$$
A_w(f) = \#\lbrace j : f(x^{(j)}) \neq f(x^{(j+1)})\rbrace,
\qquad
A_{+}(f) = \min_{w>0\ \text{generic}} A_w(f).
$$

**Theorem.**

**(a)** $H^{*}(f) \leq A_{+}(f)$ for every $f$.

**(b)** If $f$ is symmetric, $f(x) = F(|x|)$, then $A_{+}(f) = C(F) = H^{*}(f)$.

> **A simple, L12-style invariant.** $A_{+}(f)$ is the minimum number of times $f$ alternates along a positive linear ordering of the cube. It is computable, upper-bounds head complexity in general, and **equals it for symmetric functions**, recovering [012_symmetric_sign_changes.md](../01_foundations_and_normal_form/012_symmetric_sign_changes.md) in elementary terms. It is **not** exact in general (see the remark): the gap is the head's free numerator.

## Proof

**Part (a).** Fix a generic positive $w$ attaining $A_w(f) = A_+(f)$. Since $t_w$ has $2^n$ distinct values, $f = G \circ t_w$ for the table $G(t_w(x^{(j)})) = f(x^{(j)})$, and the number of sign changes of $G$ along the increasing values of $t_w$ is exactly $A_w(f)$. By the weighted-score upper bound [025_weighted_score_upper.md](025_weighted_score_upper.md), $H^{*}(f) \leq A_w(f) = A_{+}(f)$.

**Part (b), $A_{+}(f) \leq C(F)$.** Take $w_i = 1 + i\eta$ with $\eta > 0$ small enough that the $t_w$-order refines Hamming weight ( $|x| < |y| \Rightarrow t_w(x) < t_w(y)$, since for small $\eta$ the weight perturbations cannot overcome a unit gap in $|\cdot|$). Then in the $t_w$-order the points appear in blocks of constant Hamming weight $0,1,\dots,n$; $f$ is constant on each block, so an alternation occurs only at a block boundary $k\to k+1$, exactly when $F(k)\neq F(k+1)$. Hence $A_w(f) = C(F)$, so $A_{+}(f) \leq C(F)$.

**Part (b), $A_{+}(f) \geq C(F)$.** Let $w$ be any generic positive weight. The Hamming chain $z^{(0)},\dots,z^{(n)}$ (adding one coordinate at a time, $|z^{(k)}| = k$) is $t_w$-increasing (each step adds a positive $w_i$), so it is an increasing subsequence of the $t_w$-order with $f(z^{(k)}) = F(k)$. Its alternation count is $C(F)$, and the alternation count of a sequence is at least that of any subsequence, so $A_w(f) \geq C(F)$. As $w$ was arbitrary, $A_{+}(f) \geq C(F)$.

Thus $A_{+}(f) = C(F)$, and by L12 this equals $H^{*}(f)$. $\blacksquare$

## Remark: not exact in general

$A_{+}$ over-counts for some nonsymmetric $f$, because a single head's *numerator* may be any (mixed-sign) affine form while a single monotone score cannot mimic it:

- **Linear threshold.** $f = \mathbf{1}[x_1 \geq x_2]$ is an LTF, so $H^{*}(f) = 1$ [011_one_head_characterization.md](../01_foundations_and_normal_form/011_one_head_characterization.md). But every positive order puts $00$ first, $11$ last, and $10, 01$ in the middle, giving $f$-values $1,1,0,1$ or $1,0,1,1$, so $A_w(f) = 2$ for all generic positive $w$ and $A_{+}(f) = 2 > 1$.
- **Dictator via superincreasing weights.** With $t(x) = \sum_i 2^{i-1}x_i$ and $F(k) = (-1)^k$, $f = (-1)^{x_1}$ has $H^{*}(f) = 1$ while $C(F) = 2^n - 1$ along that particular order (the minimization over $w$ is what repairs this).

So $A_{+}$ is the right *simple upper-bound* invariant and is exact on symmetric functions, but an exact closed form for general nonsymmetric $f$ is not given by alternation counting; the exact value is the tangential-Chow rank [016_cleared_denominator_invariant.md](../01_foundations_and_normal_form/016_cleared_denominator_invariant.md), reflecting that $H^{*}$ is a genuinely new measure.

## Corollary: an exact characterization where the bounds meet

Since $\deg_{\pm}(f) \leq H^{*}(f)$ [006_threshold_degree_head_complexity_bound.md](../01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md) and $H^{*}(f) \leq A_{+}(f)$ (part (a)),

$$
\deg_{\pm}(f) \;\leq\; H^{*}(f) \;\leq\; A_{+}(f).
$$

Hence **whenever $\deg_{\pm}(f) = A_{+}(f)$, all three coincide:** $H^{*}(f) = A_{+}(f) = \deg_{\pm}(f)$. This holds for all symmetric $f$ (where $\deg_{\pm} = C(F) = A_{+}$), and more generally for any $f$ whose threshold degree already meets its minimum positive-order alternation count. It is the broadest class on which the *simple* invariant $A_{+}$ is provably exact with the current tools.

## Why no simple alternation invariant captures head complexity in general

The positive-order count $A_{+}$ over-counts (free numerator, above). The natural fix, allowing *signed* affine orderings $L$ (define $B(f) = \min_{L\ \text{affine generic}}$ alternations of $f$ along the $L$-order), instead under-counts: a degree-$B$ univariate polynomial $q(L(x))$ sign-represents $f$, so $B(f) \geq \deg_{\pm}(f)$ and $B$ tracks threshold degree, not $H^{*}$ (its degree-$B$ representer uses mixed-slope factors, which are inadmissible, so it does not yield an $H^{*}$ construction). Since $H^{*}$ is strictly finer than $\deg_{\pm}$ [023_counting_separation.md](../03_lower_bounds/023_counting_separation.md), neither alternation count equals $H^{*}$. This is structural evidence that $H^{*}$ has no simple closed form by linear-order alternations alone; the exact invariant is the (positivity-restricted) tangential-Chow rank.
