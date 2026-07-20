# Sparse Single-Polarity Threshold-Density Upper Bound

## Statement

A **monotone subcube indicator** is $\mathbf{1}_T$ for $T$ given by a nonempty $S \subseteq \lbrace 1,\dots,n\rbrace$ as either $\prod_{i\in S}x_i$ (positive type) or $\prod_{i\in S}(1-x_i)$ (negative type).

**Theorem.** Let $T_1,\dots,T_s$ be monotone subcubes, $c_1,\dots,c_s,\theta \in \mathbb{R}$, and

$$
\Sigma(x) := \theta + \sum_{j=1}^{s} c_j\, \mathbf{1}_{T_j}(x).
$$

If $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$ is computed by this score with a strict margin, i.e. $f(x) = 1 \iff \Sigma(x) > 0$ and $\Sigma(x) \neq 0$ for all $x$, then

$$
H^{*}(f) \leq s.
$$

> Generalizes the monotone-term DNF bound [014_monotone_term_dnf.md](014_monotone_term_dnf.md) (the case $c_j = 1$, $\theta = -\tfrac12$): any thresholded sparse sum of $s$ single-polarity subcube indicators with positive margin needs at most $s$ heads. Each indicator is replaced by a calibrated one-head bump approximating it uniformly, and the finite-cube margin keeps the classification exact.

## Proof

We use the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md). Write $I_j = \mathbf{1}_{T_j}$ with support $S_j$.

**Calibrated bump.** For $\lambda > 0$, $\epsilon > 0$, set weights $w^{(j)}_i = 1$ ($i\in S_j$), $\epsilon$ ($i\notin S_j$), and the affine violation count $v_j(x) = \sum_i w^{(j)}_i(1-x_i)$ (positive type) or $\sum_i w^{(j)}_i x_i$ (negative type). As in [014_monotone_term_dnf.md](014_monotone_term_dnf.md): $v_j \geq 0$; if $I_j(x) = 1$ then $0 \leq v_j(x) \leq \epsilon n$; if $I_j(x) = 0$ then $v_j(x) \geq 1$.

Set $b_j(x) = \frac{1}{1 + \lambda v_j(x)}$ (denominator $\geq 1$). It is a one-head atom: for negative type choose $\alpha_j > 1 + \lambda W_j$ ($W_j = \sum_i w^{(j)}_i$), $\rho^{(j)}_i = \lambda w^{(j)}_i/(\alpha_j - 1) > 0$, $\gamma_j = 1 - \sum_i \rho^{(j)}_i > 0$; then $\gamma_j + \sum_i \rho^{(j)}_i\alpha_j^{x_i} = 1 + \lambda v_j(x)$, and numerator $1$ via $\eta = 1, \delta = m_i = 0$. Positive type is analogous with $\alpha_j \in (0, \frac{1}{1+\lambda W_j})$.

**Uniform approximation.** If $I_j(x) = 1$ then $b_j(x) \in [\frac{1}{1+\lambda\epsilon n}, 1]$; if $I_j(x) = 0$ then $b_j(x) \in [0, \frac{1}{1+\lambda}]$. Hence

$$
|b_j(x) - I_j(x)| \leq \rho(\lambda,\epsilon) := \max\Big(1 - \tfrac{1}{1+\lambda\epsilon n},\ \tfrac{1}{1+\lambda}\Big).
$$

Taking $\epsilon = \lambda^{-2}$, $1 - \frac{1}{1+\lambda\epsilon n} = \frac{n}{\lambda + n} \to 0$ and $\frac{1}{1+\lambda} \to 0$ as $\lambda \to \infty$, so $\rho(\lambda,\lambda^{-2}) \to 0$.

**Margin.** Let $\mu := \min_x |\Sigma(x)| > 0$ (finite cube, $\Sigma$ nowhere zero) and $C := \sum_j |c_j|$. Set $\widetilde\Sigma(x) := \theta + \sum_j c_j b_j(x)$; then

$$
|\widetilde\Sigma(x) - \Sigma(x)| = \Big|\sum_j c_j(b_j(x) - I_j(x))\Big| \leq C\,\rho(\lambda,\epsilon).
$$

Choose $\lambda$ large (with $\epsilon = \lambda^{-2}$) so that $C\rho(\lambda,\epsilon) < \mu$. Then since $|\Sigma(x)| \geq \mu$, $\widetilde\Sigma(x)$ has the same sign as $\Sigma(x)$ at every $x$ (if $\Sigma(x) \geq \mu$ then $\widetilde\Sigma > 0$; if $\Sigma(x) \leq -\mu$ then $\widetilde\Sigma < 0$). Hence

$$
f(x) = 1 \iff \Sigma(x) > 0 \iff \widetilde\Sigma(x) > 0 .
$$

**Conclusion.** Each $\psi_j := c_j b_j$ is a one-head atom (numerator constant $c_j$), so $\widetilde\Sigma = \theta + \sum_{j=1}^s \psi_j$ is a constant plus $s$ atoms whose threshold is $f$. By the normal form, $H^{*}(f) \leq s$. $\blacksquare$

## Consequence

Combined with calibrated interpolation [019_calibrated_interpolation.md](019_calibrated_interpolation.md), this completes the "positive feature, threshold once" upper-bound toolkit: any function written as a thresholded real combination of single-polarity subcube features (sparse threshold density $s$, with margin) has $H^{*} \leq s$. It is tight against the threshold-degree lower bound only when $\deg_{\pm}(f) = s$; closing the gap to a matching lower bound for nonsymmetric $f$ remains open.
