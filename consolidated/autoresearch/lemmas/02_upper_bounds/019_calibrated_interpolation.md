# Calibrated Positive-Weighted-Sum Interpolation

## Statement

Let $t(x) = \sum_{i=1}^n \lambda_i x_i$ with all $\lambda_i > 0$, and let $\mathrm{Im}(t) = \lbrace \tau_1 < \dots < \tau_M\rbrace$ be its $M$ distinct values on the cube.

**Part 1 (calibrated interpolation).** For every $G : \mathrm{Im}(t) \to \mathbb{R}$ there exist $M - 1$ one-head atoms $\psi_1,\dots,\psi_{M-1}$ and a constant $a_0$ with

$$
a_0 + \sum_{j=1}^{M-1} \psi_j(x) = G(t(x)) \qquad \text{for all } x \in \lbrace 0,1\rbrace^n .
$$

**Part 2 (additive composition).** If $f(x) = \mathbf{1}\big[\theta + \sum_{r=1}^s a_r G_r(t_r(x)) > 0\big]$ with each $t_r(x) = \sum_i \lambda_{ri}x_i$, $\lambda_{ri} > 0$, and each $G_r : \mathrm{Im}(t_r) \to \mathbb{R}$ arbitrary, then

$$
H^{*}(f) \leq \sum_{r=1}^{s}\big(|\mathrm{Im}(t_r)| - 1\big).
$$

> Part 1 upgrades the weighted-sum bound [009_weighted_sum_upper_bound.md](../01_foundations_and_normal_form/009_weighted_sum_upper_bound.md) from a sign representation to an exact real (calibrated) one; that calibration is what lets blocks be combined additively in Part 2.

## Proof

We use the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md).

### Part 1

If $M = 1$, take $a_0 = G(\tau_1)$ and zero atoms; since $t \equiv \tau_1$, this equals $G(t(x))$. Assume $M \geq 2$.

**Kernels are one-head atoms.** For $\beta > 0$ set $k_\beta(x) = \frac{1}{\beta + t(x)}$. With $L = \sum_i \lambda_i > 0$, choose $\alpha > 1 + L/\beta$, $\rho_i = \lambda_i/(\alpha-1) > 0$, $\gamma = \beta - \sum_i \rho_i = \beta - \frac{L}{\alpha-1} > 0$. Using $\alpha^{x_i} = 1 + (\alpha-1)x_i$,

$$
\gamma + \sum_i \rho_i \alpha^{x_i} = \Big(\gamma + \sum_i \rho_i\Big) + \sum_i \rho_i(\alpha-1)x_i = \beta + \sum_i \lambda_i x_i = \beta + t(x),
$$

and with $\eta = c$, $m_i = \delta = 0$ the numerator is the constant $c$. So $c\,k_\beta$ is a one-head atom for any $c \in \mathbb{R}$. Also $\beta + t(x) > 0$ on the cube ($\beta > 0$, $t \geq 0$).

**Interpolation system.** Pick distinct positive reals $\beta_1,\dots,\beta_{M-1}$ (e.g. $\beta_j = j$); then $\beta_j + \tau_\ell > 0$ for all $j,\ell$. Seek $(a_0, c_1,\dots,c_{M-1})$ solving

$$
a_0 + \sum_{j=1}^{M-1} \frac{c_j}{\beta_j + \tau_\ell} = G(\tau_\ell), \qquad \ell = 1,\dots,M.
$$

This is an $M \times M$ real linear system.

**Invertibility.** Suppose the homogeneous system holds. The rational function $\Phi(s) = a_0 + \sum_j \frac{c_j}{\beta_j + s} = R(s)/\prod_j(\beta_j + s)$ has numerator

$$
R(s) = a_0\prod_{j}(\beta_j + s) + \sum_{j} c_j \prod_{j' \neq j}(\beta_{j'} + s)
$$

of degree $\leq M-1$. Since $\beta_j + \tau_\ell \neq 0$, $\Phi(\tau_\ell) = 0$ forces $R(\tau_\ell) = 0$ at all $M$ distinct $\tau_\ell$, so $R \equiv 0$. Evaluating $R$ at $s = -\beta_{j_0}$ kills every term but the $j_0$ one, giving $c_{j_0}\prod_{j' \neq j_0}(\beta_{j'} - \beta_{j_0}) = 0$; the $\beta_j$ being distinct forces $c_{j_0} = 0$ for all $j_0$. Then $R(s) = a_0\prod_j(\beta_j + s) \equiv 0$ forces $a_0 = 0$. So the homogeneous system has only the zero solution and the matrix is invertible; the interpolation system has a unique solution.

**Assemble.** Set $\psi_j = c_j k_{\beta_j}$, a one-head atom. For each $x$, $t(x) = \tau_\ell$ for some $\ell$, so $a_0 + \sum_j \psi_j(x) = a_0 + \sum_j \frac{c_j}{\beta_j + \tau_\ell} = G(\tau_\ell) = G(t(x))$. $\square$

### Part 2

Apply Part 1 to each $t_r$ with the scaled table $\widetilde G_r = a_r G_r$: get $M_r - 1$ atoms $\psi_{r,j}$ ($M_r = |\mathrm{Im}(t_r)|$) and a constant $b_r$ with $b_r + \sum_j \psi_{r,j}(x) = a_r G_r(t_r(x))$. With $c = \theta + \sum_r b_r$,

$$
c + \sum_{r=1}^s \sum_{j=1}^{M_r - 1} \psi_{r,j}(x) = \theta + \sum_{r=1}^s a_r G_r(t_r(x)),
$$

so $f(x) = 1 \iff c + \sum_{r,j}\psi_{r,j}(x) > 0$, a constant plus $\sum_r(M_r - 1)$ atoms. By the normal form, $H^{*}(f) \leq \sum_r(|\mathrm{Im}(t_r)| - 1)$. $\blacksquare$

## Remark

Taking $G = F$ a $\lbrace 0,1\rbrace$-valued table and thresholding $a_0 - \tfrac12 + \sum_j \psi_j$ recovers $H^{*}(f) \leq M - 1$ (the weighted-sum bound L9). The new content is the exact real identity, which makes positive-weighted-sum blocks additively composable, a building block for the sparse threshold-density bound [020_sparse_threshold_density.md](020_sparse_threshold_density.md).
