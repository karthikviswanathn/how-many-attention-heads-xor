# Problem: A tangential-Chow sandwich for head complexity

## Background and definitions (self-contained)

Fix $n \geq 1$, work on $\{0,1\}^n$. For $\alpha>0$, $b\in\{0,1\}$: $\alpha^0=1$, $\alpha^1=\alpha$. A function $A(x)=a_0+\sum_{i=1}^n a_i x_i$ is **affine** (slopes $a_1,\dots,a_n$); it is **positive on the cube** if $A>0$ everywhere on $\{0,1\}^n$. A polynomial $P$ **sign-represents** $f:\{0,1\}^n\to\{0,1\}$ if $f(x)=1 \iff P(x)>0$ for all $x\in\{0,1\}^n$.

The **threshold degree** $\deg_{\pm}(f)$ is the least degree of a polynomial sign-representing $f$.

A **one-head atom** is $\phi(x) = \dfrac{\eta + \sum_i \rho_i\alpha^{x_i}(m_i+\delta x_i)}{\gamma + \sum_i \rho_i\alpha^{x_i}}$ with $\gamma>0,\rho_i>0,\alpha>0$ and $\eta,\delta,m_i\in\mathbb{R}$.

**Established normal form (use as the definition of head complexity).** $H^{*}(f) \leq H$ iff there exist one-head atoms $\phi_1,\dots,\phi_H$ and $c\in\mathbb{R}$ with $f(x)=1 \iff c+\sum_{h=1}^H \phi_h(x)>0$ for all $x$.

**Established atom fact (you may use it).** Every one-head atom equals $N/D$ where $N,D$ are affine and $D$ is positive on the cube. (This follows by expanding $\alpha^{x_i}=1+(\alpha-1)x_i$; you may either cite it or reprove it in one line.)

**Tangential-Chow sign-rank.** Define $\mathrm{tChow}_{\pm}(f)$ to be the least $H\geq 0$ for which there exist *arbitrary* affine functions $N_1,D_1,\dots,N_H,D_H$ (no positivity or sign constraints) and $\theta\in\mathbb{R}$ such that the polynomial

$$
P(x) = \theta\prod_{h=1}^{H} D_h(x) + \sum_{h=1}^{H} N_h(x)\prod_{g\neq h} D_g(x)
$$

sign-represents $f$. (For $H=0$, $P=\theta$.) This $P$ is exactly a tangent vector at the product point $\prod_h D_h$ to the variety of products of $H$ affine forms.

## Claim to prove

For every $f:\{0,1\}^n\to\{0,1\}$,

$$
\deg_{\pm}(f) \;\leq\; \mathrm{tChow}_{\pm}(f) \;\leq\; H^{*}(f).
$$

> **Interpretation.** Head complexity is squeezed between ordinary threshold degree and the positivity-restricted tangential-Chow rank: $H^{*}$ is the same tangential-Chow quantity with the extra requirement that each base factor $D_h$ be positive on the cube with one-sided slopes. The attention-specific positivity/monotone constraints are exactly the gap between $H^{*}$ and the unconstrained algebraic invariant.

## Guidance (prove every step rigorously)

**Left inequality $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f)$.**
1. Let $H=\mathrm{tChow}_{\pm}(f)$ with witnesses $N_h,D_h,\theta$ and polynomial $P$ sign-representing $f$.
2. Each $\prod_{h}D_h$ has degree $\leq H$ and each $N_h\prod_{g\neq h}D_g$ has degree $\leq 1+(H-1)=H$, so $\deg P \leq H$.
3. Since $P$ sign-represents $f$ and has degree $\leq H$, $\deg_{\pm}(f)\leq H = \mathrm{tChow}_{\pm}(f)$.

**Right inequality $\mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$.**
1. Let $H=H^{*}(f)$, with atoms $\phi_h$ and constant $c$ from the normal form, and write $\phi_h=N_h/D_h$ with $N_h,D_h$ affine and $D_h$ positive on the cube (established atom fact).
2. Then $\Pi(x):=\prod_g D_g(x)>0$ for all $x$ (finite product of positives).
3. Multiplying the strict inequality $c+\sum_h N_h/D_h>0$ by $\Pi(x)>0$ is sign-faithful, giving $f(x)=1 \iff P(x)>0$ where $P=c\prod_g D_g+\sum_h N_h\prod_{g\neq h}D_g$.
4. $P$ is a valid tangential-Chow polynomial (the $N_h,D_h$ are affine, $\theta=c$), so $\mathrm{tChow}_{\pm}(f)\leq H=H^{*}(f)$.

Combine the two inequalities. Also state the immediate refinement: $H^{*}(f)$ equals the same minimization with the added constraints "$D_h$ positive on the cube and one-sided slopes," so the gap $H^{*}-\mathrm{tChow}_{\pm}$ is governed precisely by those constraints.

Give a complete, rigorous proof.
