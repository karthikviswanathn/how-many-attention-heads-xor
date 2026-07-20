# Monotone-Term DNF Upper Bound

## Statement

A **monotone term** is the indicator of a subcube of one of the two forms

$$
T(x) = \prod_{i\in S} x_i \quad (\text{positive term}),
\qquad
T(x) = \prod_{i\in S} (1-x_i) \quad (\text{negative term}),
$$

for a nonempty $S \subseteq \lbrace 1,\dots,n\rbrace $, so $T(x) \in \lbrace 0,1\rbrace $ and $T(x) = 1$ exactly when its literals are all satisfied. A function $f : \lbrace 0,1\rbrace ^n \to \lbrace 0,1\rbrace $ has a **monotone-term DNF with $s$ terms** if there are monotone terms $T_1,\dots,T_s$ with $f(x) = 1 \iff \exists r : T_r(x) = 1$.

**Theorem.** If $f$ has a monotone-term DNF with $s$ terms, then

$$
H^{*}(f) \leq s .
$$

> **Corollary.** Every monotone Boolean function $f$ satisfies $H^{*}(f) \leq (\text{number of prime implicants of } f)$, since a monotone function is the OR of its prime implicants and each prime implicant is a positive monotone term.

This is the corrected form of the general DNF bound: a single head's denominator has one-sided slopes (the monotone bias of [013_atom_dictionary.md](../01_foundations_and_normal_form/013_atom_dictionary.md)), so the per-term reciprocal bump is a valid one-head atom only when the term has a single literal polarity. Mixed-literal terms are not covered by one head each.

## Proof

We use the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md): $H^{*}(f) \leq s$ holds whenever there are $s$ one-head atoms $b_1,\dots,b_s$ and a constant $c$ with $f(x) = 1 \iff c + \sum_r b_r(x) > 0$ for all $x$.

Assume $f$ has terms $T_1,\dots,T_s$ with supports $S_r$. Set $\lambda = 2s$ and pick $\epsilon \in (0, \tfrac{1}{2sn})$, so $\lambda\epsilon n < 1$. Give every coordinate a positive weight

$$
w^{(r)}_i = \begin{cases} 1, & i \in S_r, \\ \epsilon, & i \notin S_r, \end{cases}
$$

and define the **violation count**

$$
v_r(x) = \sum_{i=1}^n w^{(r)}_i (1 - x_i) \ \text{ (positive term)},
\qquad
v_r(x) = \sum_{i=1}^n w^{(r)}_i\, x_i \ \text{ (negative term)}.
$$

### Violation bounds

All weights are positive and $x_i, 1-x_i \in \lbrace 0,1\rbrace $, so $v_r(x) \geq 0$.

- If $T_r(x) = 1$: for a positive term every $i \in S_r$ has $x_i = 1$, so $1-x_i = 0$ there and only out-of-support coordinates (weight $\epsilon$) contribute, giving $0 \leq v_r(x) \leq \epsilon n$. The negative-term case is identical with $x_i$ in place of $1-x_i$.
- If $T_r(x) = 0$: some in-support $j \in S_r$ violates its literal, contributing weight $w^{(r)}_j = 1$ (the term $1 \cdot (1 - x_j) = 1$ for a positive term, or $1 \cdot x_j = 1$ for a negative term). All other summands are nonnegative, so $v_r(x) \geq 1$.

### Each bump is a one-head atom

Set $b_r(x) = \dfrac{1}{1 + \lambda v_r(x)}$; the denominator is $\geq 1 > 0$, so $b_r$ is well defined and nonnegative.

**Negative term:** $v_r(x) = \sum_i w^{(r)}_i x_i$. Choose $\alpha_r > 1$ with $\sum_i \frac{\lambda w^{(r)}_i}{\alpha_r - 1} < 1$, and set $\rho^{(r)}_i = \frac{\lambda w^{(r)}_i}{\alpha_r - 1} > 0$, $\gamma_r = 1 - \sum_i \rho^{(r)}_i > 0$, $\eta_r = 1$, $\delta_r = 0$, $m^{(r)}_i = 0$. Using $\alpha_r^{x_i} = 1 + (\alpha_r-1)x_i$,

$$
\gamma_r + \sum_i \rho^{(r)}_i \alpha_r^{x_i}
= \Big(\gamma_r + \sum_i \rho^{(r)}_i\Big) + \sum_i \rho^{(r)}_i(\alpha_r - 1)x_i
= 1 + \lambda \sum_i w^{(r)}_i x_i
= 1 + \lambda v_r(x),
$$

and the numerator is $\eta_r + \sum_i \rho^{(r)}_i \alpha_r^{x_i}(0 + 0\cdot x_i) = 1$. So $b_r$ is a one-head atom.

**Positive term:** $v_r(x) = W_r - \sum_i w^{(r)}_i x_i$ with $W_r = \sum_i w^{(r)}_i$. Choose $\alpha_r \in (0,1)$ small enough that $1 + \lambda W_r - \frac{\lambda W_r}{1-\alpha_r} > 0$, and set $\rho^{(r)}_i = \frac{\lambda w^{(r)}_i}{1-\alpha_r} > 0$, $\gamma_r = 1 + \lambda W_r - \sum_i \rho^{(r)}_i > 0$, $\eta_r = 1$, $\delta_r = 0$, $m^{(r)}_i = 0$. Using $\alpha_r^{x_i} = 1 - (1-\alpha_r)x_i$,

$$
\gamma_r + \sum_i \rho^{(r)}_i \alpha_r^{x_i}
= \big(1 + \lambda W_r\big) - \sum_i \lambda w^{(r)}_i x_i
= 1 + \lambda v_r(x),
$$

and again the numerator is $1$. So $b_r$ is a one-head atom.

### Threshold separation

If some term is satisfied at $x$, that $b_r(x) \geq \frac{1}{1 + \lambda \epsilon n} > \frac12$ (since $\lambda\epsilon n < 1$), and all $b_q \geq 0$, so $\sum_q b_q(x) > \frac12$.

If no term is satisfied at $x$, every $v_r(x) \geq 1$ gives $b_r(x) \leq \frac{1}{1+\lambda} = \frac{1}{1+2s}$, so $\sum_r b_r(x) \leq \frac{s}{1+2s} < \frac12$.

### Conclusion

Take $c = -\tfrac12$. If $f(x) = 1$ some term is satisfied, so $c + \sum_r b_r(x) > 0$. If $c + \sum_r b_r(x) > 0$ then $\sum_r b_r(x) > \tfrac12$, which forces some term satisfied, hence $f(x) = 1$. Thus $f(x) = 1 \iff c + \sum_r b_r(x) > 0$ for all $x$, with $s$ one-head atoms. By the normal form, $H^{*}(f) \leq s$. $\blacksquare$

## Consequence

This is the first exact-flavored upper bound for a genuinely nonsymmetric family. Combined with the threshold-degree lower bound [006_threshold_degree_head_complexity_bound.md](../01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md), it sandwiches $H^{*}$ for monotone functions between $\deg_{\pm}(f)$ and the prime-implicant count.
