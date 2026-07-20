# Problem: Head complexity equals the cleared-denominator (tangential) sign-rank

## Background and definitions (self-contained)

Fix $n \geq 1$ and work on $\{0,1\}^n$. For $\alpha > 0$, $b \in \{0,1\}$: $\alpha^0 = 1$, $\alpha^1 = \alpha$. A function $A : \{0,1\}^n \to \mathbb{R}$ is **affine** if $A(x) = a_0 + \sum_{i=1}^n a_i x_i$; the $a_i$ ($i \geq 1$) are its **slopes**, $a_0$ its constant term. On the cube the affine representation is unique. $A$ is **positive on the cube** if $A(x) > 0$ for all $x \in \{0,1\}^n$.

A **one-head atom** is a function $\phi : \{0,1\}^n \to \mathbb{R}$ of the form

$$
\phi(x) = \frac{\eta + \sum_{i=1}^{n} \rho_i \alpha^{x_i}(m_i + \delta x_i)}{\gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i}},
\qquad \gamma>0,\ \rho_i>0,\ \alpha>0,\ \eta,\delta,m_i\in\mathbb{R}.
$$

**Established normal form (use as the definition of head complexity).** For any integer $H \geq 0$,

$$
H^{*}(f) \leq H
\iff
\exists\ \text{one-head atoms } \phi_1,\dots,\phi_H,\ c\in\mathbb{R}:\quad
\big(f(x)=1 \iff c + \textstyle\sum_{h=1}^{H}\phi_h(x) > 0\big)\ \forall x \in \{0,1\}^n .
$$

Thus $H^{*}(f)$ is the least such $H$. (For $H=0$ the sum is empty and $f$ is constant.)

Call an ordered pair $(N, D)$ of affine functions **admissible** if $D$ is positive on the cube and the slopes of $D$ are either all $\geq 0$ or all $\leq 0$ (one common weak sign), while $N$ is arbitrary affine. Call it **strictly admissible** if in addition every slope of $D$ is nonzero (so all slopes are strictly positive, or all strictly negative).

Define the **tangential cleared-denominator sign-rank** $\mathrm{MFdeg}_{\pm}(f)$ as the least $H \geq 0$ for which there are admissible pairs $(N_1,D_1),\dots,(N_H,D_H)$ and a real $\theta$ such that the polynomial

$$
P(x) \;=\; \theta \prod_{h=1}^{H} D_h(x) \;+\; \sum_{h=1}^{H} N_h(x) \prod_{g \neq h} D_g(x)
$$

(of total degree $\leq H$) sign-represents $f$, i.e. $f(x)=1 \iff P(x) > 0$ for all $x \in \{0,1\}^n$. (For $H=0$, $P = \theta$.)

## Claim to prove

$$
H^{*}(f) = \mathrm{MFdeg}_{\pm}(f).
$$

## Required dictionary lemma (prove it inline; it is short)

**(a)** Every one-head atom $\phi$ equals $N/D$ for an admissible pair $(N,D)$.

**(b)** Conversely, for every strictly admissible pair $(N,D)$, the ratio $N/D$ is a one-head atom.

Proof to give:

- (a) Substitute $\alpha^{x_i} = 1 + (\alpha-1)x_i$ (valid since $x_i \in \{0,1\}$). Then $D(x) = (\gamma + \sum_i \rho_i) + (\alpha-1)\sum_i \rho_i x_i$ and $N(x) = (\eta + \sum_i \rho_i m_i) + \sum_i \rho_i((\alpha-1)m_i + \alpha\delta)x_i$ are affine. The original denominator is a sum of strictly positive terms, hence positive on the cube; its slopes $\rho_i(\alpha-1)$ all share the sign of $\alpha-1$. So $(N,D)$ is admissible.
- (b) Given strictly admissible $(N,D)$, $D(x) = d_0 + \sum_i d_i x_i$ with all $d_i$ of one strict sign and $D>0$ on the cube. If $d_i>0$ choose $\alpha>1$; if $d_i<0$ choose $\alpha\in(0,1)$. Set $\rho_i = d_i/(\alpha-1)>0$ and $\gamma = d_0 - \sum_i \rho_i$. Show $\gamma>0$ for a suitable extreme $\alpha$: in the positive case $\sum_i \rho_i = \frac{1}{\alpha-1}\sum_i d_i \to 0$ as $\alpha\to\infty$ while $d_0 = D(\mathbf 0)>0$; in the negative case $D(\mathbf 1) = d_0 - \sum_i|d_i|>0$ and $\sum_i\rho_i = \frac{1}{1-\alpha}\sum_i|d_i| \to \sum_i|d_i|$ as $\alpha\to 0^+$. Then the denominator $\gamma + \sum_i \rho_i\alpha^{x_i} = D(x)$. Realize the target numerator $N$ (slopes $e_i$, constant $e_0$) with $\delta=0$, $m_i = e_i/(\rho_i(\alpha-1))$, $\eta = e_0 - \sum_i \rho_i m_i$; verify the atom's numerator equals $N$. Hence $N/D$ is a one-head atom.

## Main argument

**Step 1: $\mathrm{MFdeg}_{\pm}(f) \leq H^{*}(f)$ (clearing denominators; no perturbation needed).**
Let $H = H^{*}(f)$ with atoms $\phi_h = N_h/D_h$ and constant $c$ from the normal form. By (a) each $(N_h,D_h)$ is admissible and $D_h>0$ on the cube, so $\prod_{g} D_g(x) > 0$ for every $x$. Multiplying the strict inequality $c + \sum_h N_h/D_h > 0$ by this positive number is sign-faithful:

$$
c + \sum_h \frac{N_h(x)}{D_h(x)} > 0
\iff
c\prod_g D_g(x) + \sum_h N_h(x)\prod_{g\neq h}D_g(x) > 0 .
$$

The right side is $P(x)$ with $\theta = c$ and admissible pairs $(N_h,D_h)$. So $P$ sign-represents $f$ and $\mathrm{MFdeg}_{\pm}(f) \leq H$.

**Step 2: $H^{*}(f) \leq \mathrm{MFdeg}_{\pm}(f)$ (dividing; with a strict-margin perturbation for zero slopes).**
Let $H = \mathrm{MFdeg}_{\pm}(f)$ with admissible pairs $(N_h,D_h)$, real $\theta$, and $P$ sign-representing $f$. Each $D_h>0$ on the cube so $\Pi(x) := \prod_h D_h(x) > 0$, and dividing is sign-faithful:

$$
P(x) > 0 \iff Q(x) := \theta + \sum_h \frac{N_h(x)}{D_h(x)} > 0 .
$$

So $f(x) = 1 \iff Q(x) > 0$. Now make two adjustments to land exactly in the normal form with genuine atoms.

1. **Threshold shift to create a two-sided margin.** If $f \equiv 0$ then $H^{*}(f) = 0 \leq H$ and we are done; otherwise let $q_+ := \min\{Q(x): f(x)=1\} > 0$ (finite cube, nonempty set). Pick $\nu$ with $0 < \nu < q_+$ and replace $\theta$ by $\theta - \nu$, giving $Q_\nu := Q - \nu$. Then $Q_\nu(x) \geq q_+ - \nu > 0$ on $f^{-1}(1)$ and $Q_\nu(x) = Q(x) - \nu \leq -\nu < 0$ on $f^{-1}(0)$ (where $Q \leq 0$). So $f(x) = 1 \iff Q_\nu(x) > 0$, with $|Q_\nu(x)| \geq \nu$ everywhere.

2. **Perturb zero slopes to make every denominator strictly admissible.** For each $h$ with some zero slopes, replace $D_h$ by $D_h^\varepsilon$ obtained by adding $\varepsilon$ to each zero slope if the nonzero slopes of $D_h$ are $\geq 0$ (or subtracting $\varepsilon$ if they are $\leq 0$; if $D_h$ is constant, add $+\varepsilon$ to all slopes). For small $\varepsilon>0$, $D_h^\varepsilon$ is still positive on the cube and now strictly admissible, and $D_h^\varepsilon \to D_h$ uniformly on the finite cube as $\varepsilon \to 0$. Hence $Q_\nu^\varepsilon := (\theta-\nu) + \sum_h N_h/D_h^\varepsilon \to Q_\nu$ uniformly on the finite cube. Choose $\varepsilon$ small enough that $|Q_\nu^\varepsilon(x) - Q_\nu(x)| < \nu$ for all $x$; then $Q_\nu^\varepsilon$ has the same sign as $Q_\nu$ at every $x$ (since $|Q_\nu| \geq \nu$), so $f(x) = 1 \iff Q_\nu^\varepsilon(x) > 0$.

3. **Read off the atoms.** Each pair $(N_h, D_h^\varepsilon)$ is strictly admissible, so by (b) the summand $N_h/D_h^\varepsilon$ is a one-head atom. Thus $Q_\nu^\varepsilon = (\theta - \nu) + \sum_h (\text{atom}_h)$ is a constant plus $H$ atoms whose threshold equals $f$. By the normal form, $H^{*}(f) \leq H$.

**Conclusion.** Steps 1 and 2 give $H^{*}(f) = \mathrm{MFdeg}_{\pm}(f)$. $\blacksquare$

Note for the writeup: also record the immediate corollary that $\deg_{\pm}(f) \leq H^{*}(f)$ (since $P$ has total degree $\leq H$), and that $P$ is exactly a tangent vector at the point $\prod_h D_h$ to the variety of products of $H$ affine forms, subject to the positivity and one-sided-slope (monotone) constraints on the factors.

Give a complete, rigorous proof of the dictionary (a),(b) and Steps 1-2.
