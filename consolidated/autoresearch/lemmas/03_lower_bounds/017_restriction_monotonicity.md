# Restriction Monotonicity for Head Complexity

## Statement

For every $f : \lbrace 0,1\rbrace ^n \to \lbrace 0,1\rbrace $, every coordinate $k \in \lbrace 1,\dots,n\rbrace $, and every value $c_0 \in \lbrace 0,1\rbrace $,

$$
H^{*}\big(f|_{x_k=c_0}\big) \leq H^{*}(f).
$$

By iteration, every sub-cube restriction $g$ of $f$ (fixing any set of coordinates to any values) satisfies $H^{*}(g) \leq H^{*}(f)$.

> **Lower bounds by restriction.** If a restriction of $f$ equals (a relabeling of) $g$, then $H^{*}(f) \geq H^{*}(g)$. Since $H^{*}(\mathrm{XOR}_m) = m$ [008_exact_parity_complexity.md](../01_foundations_and_normal_form/008_exact_parity_complexity.md), any $f$ with a sub-cube restriction equal to $\mathrm{XOR}_m$ has $H^{*}(f) \geq m$; the $2$-bit checkerboard obstruction [003_checkerboard_obstruction.md](../01_foundations_and_normal_form/003_checkerboard_obstruction.md) is the case $m = 2$.

## Proof

Write $[n] = \lbrace 1,\dots,n\rbrace $, $I = [n]\setminus\lbrace k\rbrace $. For $y \in \lbrace 0,1\rbrace ^I$ let $E(y) \in \lbrace 0,1\rbrace ^n$ be the point with $E(y)_k = c_0$ and $E(y)_i = y_i$ for $i \in I$, and set $r(y) := f(E(y)) = f|_{x_k=c_0}(y)$. We use the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md).

### Restricting one atom yields an atom

Let $\phi$ be a one-head atom on $\lbrace 0,1\rbrace ^n$ with parameters $\gamma,\rho_i,\alpha,\eta,\delta,m_i$. Split the numerator and denominator sums over $[n] = I \cup \lbrace k\rbrace $ and substitute $x_k = c_0$, $x_i = y_i$ ($i \in I$). The $k$-th terms become the constants $\rho_k\alpha^{c_0}(m_k + \delta c_0)$ and $\rho_k\alpha^{c_0}$. Setting

$$
\gamma' := \gamma + \rho_k\alpha^{c_0}, \qquad \eta' := \eta + \rho_k\alpha^{c_0}(m_k + \delta c_0),
$$

and keeping $\alpha,\delta$ and the $\rho_i, m_i$ for $i \in I$, gives

$$
\phi(E(y)) = \frac{\eta' + \sum_{i\in I}\rho_i\alpha^{y_i}(m_i + \delta y_i)}{\gamma' + \sum_{i\in I}\rho_i\alpha^{y_i}}.
$$

Since $c_0 \in \lbrace 0,1\rbrace $ and $\alpha > 0$, we have $\alpha^{c_0} > 0$, so $\rho_k\alpha^{c_0} > 0$ and $\gamma' = \gamma + \rho_k\alpha^{c_0} > 0$; the remaining $\rho_i > 0$ and $\alpha > 0$ are unchanged. So $y \mapsto \phi(E(y))$ is a one-head atom on $\lbrace 0,1\rbrace ^I$.

### Restricting a representation

Let $H = H^{*}(f)$, witnessed by atoms $\phi_1,\dots,\phi_H$ and constant $\lambda$ with $f(x) = 1 \iff \lambda + \sum_h \phi_h(x) > 0$. By the previous step, each $\phi_h' (y) := \phi_h(E(y))$ is a one-head atom on $\lbrace 0,1\rbrace ^I$. For every $y \in \lbrace 0,1\rbrace ^I$,

$$
r(y) = 1 \iff f(E(y)) = 1 \iff \lambda + \sum_{h=1}^{H}\phi_h(E(y)) > 0 \iff \lambda + \sum_{h=1}^{H}\phi_h'(y) > 0 .
$$

By the normal form, $H^{*}(r) \leq H = H^{*}(f)$. $\blacksquare$

### Iteration and lower bounds

Fixing coordinates one at a time and chaining the inequality gives $H^{*}(g) \leq H^{*}(f)$ for any sub-cube restriction $g$. Coordinate relabeling preserves $H^{*}$ (reindex $\rho_i, m_i$; this is the permutation half of [015_negation_permutation_closure.md](../04_closure_and_structure/015_negation_permutation_closure.md)). Hence if a restriction of $f$ equals a relabeled copy of $g$, then $H^{*}(g) = H^{*}(\text{that restriction}) \leq H^{*}(f)$. Applying this with $g = \mathrm{XOR}_m$ (using $H^{*}(\mathrm{XOR}_m) = m$) and with $m = 2$ for the checkerboard recovers the stated lower bounds.

## Consequence

Restriction monotonicity is the first general lower-bound *transfer* tool for nonsymmetric $f$: any planted parity sub-cube forces head complexity to grow, independent of the rest of $f$. It complements the threshold-degree lower bound [006_threshold_degree_head_complexity_bound.md](../01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md) and is the structural generalization of the checkerboard obstruction.
