# Tangential-Chow Sandwich

## Statement

For affine $N_1,D_1,\dots,N_H,D_H$ (arbitrary, no positivity or sign constraints) and $\theta \in \mathbb{R}$, the polynomial

$$
P(x) = \theta\prod_{h=1}^{H} D_h(x) + \sum_{h=1}^{H} N_h(x)\prod_{g\neq h} D_g(x)
$$

is a tangent vector, at the product point $\prod_h D_h$, to the variety of products of $H$ affine forms. Define the **tangential-Chow sign-rank** $\mathrm{tChow}_{\pm}(f)$ as the least $H \geq 0$ for which some such $P$ sign-represents $f$ on the cube (for $H = 0$, $P = \theta$).

**Theorem.** For every $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$,

$$
\deg_{\pm}(f) \;\leq\; \mathrm{tChow}_{\pm}(f) \;\leq\; H^{*}(f).
$$

> **Interpretation.** Head complexity is squeezed between ordinary threshold degree and the unconstrained tangential-Chow rank. $H^{*}(f) = \mathrm{MFdeg}_{\pm}(f)$ [016_cleared_denominator_invariant.md](016_cleared_denominator_invariant.md) is the *same* tangential-Chow minimization with the added attention constraints that each base factor $D_h$ be positive on the cube with one-sided slopes. Those positivity/monotone constraints are exactly the gap between $H^{*}$ and the known-flavored algebraic invariant $\mathrm{tChow}_{\pm}$.

## Proof

### Left inequality (threshold degree)

Let $H = \mathrm{tChow}_{\pm}(f)$ with witnesses $N_h, D_h, \theta$ and polynomial $P$ sign-representing $f$. Each $D_h$ is affine ($\deg \leq 1$), so $\prod_h D_h$ has degree $\leq H$ and each $N_h\prod_{g\neq h}D_g$ has degree $\leq 1 + (H-1) = H$. Scaling by $\theta$ does not raise degree, and the degree of a sum is at most the maximum summand degree, so $\deg P \leq H$. Since $P$ sign-represents $f$ with degree $\leq H$, $\deg_{\pm}(f) \leq H = \mathrm{tChow}_{\pm}(f)$.

### Right inequality (head complexity)

Let $H = H^{*}(f)$, witnessed by atoms $\phi_h$ and constant $c$ with $f(x) = 1 \iff c + \sum_h \phi_h(x) > 0$ (normal form [010_linear_fractional_normal_form.md](010_linear_fractional_normal_form.md)). By the atom dictionary [013_atom_dictionary.md](013_atom_dictionary.md), $\phi_h = N_h/D_h$ with $N_h, D_h$ affine and $D_h > 0$ on the cube. Then $\Pi(x) := \prod_g D_g(x) > 0$, so multiplying the strict inequality by $\Pi(x)$ is sign-faithful:

$$
c + \sum_h \frac{N_h(x)}{D_h(x)} > 0
\iff
\underbrace{c\prod_g D_g(x) + \sum_h N_h(x)\prod_{g\neq h}D_g(x)}_{=: P(x)} > 0 ,
$$

using $\frac{N_h}{D_h}\Pi = N_h\prod_{g\neq h}D_g$ (valid as $D_h > 0$). The $N_h, D_h$ are affine and $\theta = c$, so $P$ is a valid tangential-Chow witness, giving $\mathrm{tChow}_{\pm}(f) \leq H = H^{*}(f)$.

Chaining the two inequalities yields the sandwich. $\blacksquare$

## Refinement

For a one-head denominator $D_h(x) = \gamma_h + \sum_i \rho_{h,i}\alpha_h^{x_i} = (\gamma_h + \sum_i \rho_{h,i}) + \sum_i \rho_{h,i}(\alpha_h - 1)x_i$, the factor is positive on the cube and its slopes $\rho_{h,i}(\alpha_h - 1)$ are all of one sign (the sign of $\alpha_h - 1$). Hence $H^{*}(f)$ is the tangential-Chow minimization restricted to such admissible base factors, and $\mathrm{tChow}_{\pm}(f)$ drops those restrictions. By the corollary in [016_cleared_denominator_invariant.md](016_cleared_denominator_invariant.md), whether $\mathrm{tChow}_{\pm}(f) = H^{*}(f)$ (positivity free) or there is a strict gap is exactly the open comparison toward the first core question.
