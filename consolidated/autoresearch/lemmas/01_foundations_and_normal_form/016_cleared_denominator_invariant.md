# Cleared-Denominator (Tangential) Sign-Rank Equals Head Complexity

## Statement

Call an ordered pair $(N, D)$ of affine functions on $\lbrace 0,1\rbrace ^n$ **admissible** if $D$ is positive on the cube and the slopes of $D$ are either all $\geq 0$ or all $\leq 0$, with $N$ arbitrary affine; call it **strictly admissible** if in addition every slope of $D$ is nonzero. Define the **tangential cleared-denominator sign-rank** $\mathrm{MFdeg}_{\pm}(f)$ as the least $H \geq 0$ for which there are admissible pairs $(N_1,D_1),\dots,(N_H,D_H)$ and $\theta \in \mathbb{R}$ such that

$$
P(x) = \theta \prod_{h=1}^{H} D_h(x) + \sum_{h=1}^{H} N_h(x) \prod_{g \neq h} D_g(x)
$$

(of total degree $\leq H$) sign-represents $f$ on the cube, i.e. $f(x) = 1 \iff P(x) > 0$.

**Theorem.**

$$
H^{*}(f) = \mathrm{MFdeg}_{\pm}(f).
$$

> **Interpretation.** Head complexity is exactly the least $H$ for which $f$ is sign-represented by a tangent vector, at a product of $H$ one-sided positive affine forms, to the variety of degree-$H$ products of affine forms. This is the sharp restatement of the gap between $H^{*}$ and ordinary threshold degree: the only extra constraints are positivity and one-sided (monotone) slopes on the base factors $D_h$.

## Proof

We use the atom dictionary [013_atom_dictionary.md](013_atom_dictionary.md) (reproved compactly here) and the normal form [010_linear_fractional_normal_form.md](010_linear_fractional_normal_form.md).

### Lemma 1. Every one-head atom is an admissible ratio

Let $\phi$ be a one-head atom with parameters $\gamma,\rho_i,\alpha,\eta,\delta,m_i$. Substituting $\alpha^{x_i} = 1 + (\alpha-1)x_i$ and $x_i^2 = x_i$,

$$
D(x) := \gamma + \sum_i \rho_i\alpha^{x_i} = \Big(\gamma + \sum_i \rho_i\Big) + \sum_i \rho_i(\alpha-1)x_i,
$$

$$
N(x) := \eta + \sum_i \rho_i\alpha^{x_i}(m_i + \delta x_i) = \Big(\eta + \sum_i \rho_i m_i\Big) + \sum_i \rho_i\big((\alpha-1)m_i + \alpha\delta\big)x_i,
$$

are affine, $D$ is a sum of strictly positive terms hence positive on the cube, and the slopes $\rho_i(\alpha-1)$ all share the weak sign of $\alpha-1$. So $(N,D)$ is admissible and $\phi = N/D$. $\square$

### Lemma 2. Every strictly admissible ratio is a one-head atom

Let $(N,D)$ be strictly admissible, $D(x) = d_0 + \sum_i d_i x_i$, $N(x) = e_0 + \sum_i e_i x_i$, with all $d_i$ of one strict sign.

**Positive case ($d_i > 0$).** Positivity at $\mathbf 0$ gives $d_0 > 0$. Choose $\alpha > 1 + \tfrac{S}{d_0}$ where $S = \sum_i d_i$; set $\rho_i = d_i/(\alpha-1) > 0$ and $\gamma = d_0 - \sum_i \rho_i = d_0 - \tfrac{S}{\alpha-1} > 0$.

**Negative case ($d_i < 0$).** Positivity at $\mathbf 1$ gives $d_0 > S := \sum_i |d_i| > 0$. Choose $\alpha \in (0, 1 - \tfrac{S}{d_0})$; set $\rho_i = d_i/(\alpha-1) > 0$ and $\gamma = d_0 - \sum_i \rho_i = d_0 - \tfrac{S}{1-\alpha} > 0$.

In both cases $\alpha > 0$, $\alpha \neq 1$, $\rho_i > 0$, $\gamma > 0$, with $\rho_i(\alpha-1) = d_i$ and $\gamma + \sum_i \rho_i = d_0$, so $\gamma + \sum_i \rho_i\alpha^{x_i} = D(x)$. Take $\delta = 0$, $m_i = e_i/(\rho_i(\alpha-1))$, $\eta = e_0 - \sum_i \rho_i m_i$; then $\eta + \sum_i \rho_i\alpha^{x_i}(m_i + \delta x_i) = N(x)$. Hence $N/D$ is a one-head atom. $\square$

### Step 1. Clearing denominators (the forward inequality)

Let $H = H^{*}(f)$, witnessed by atoms $\phi_h$ and constant $c$ with $f(x) = 1 \iff c + \sum_h \phi_h(x) > 0$. By Lemma 1, $\phi_h = N_h/D_h$ with $(N_h, D_h)$ admissible and $D_h > 0$; so $\Pi(x) := \prod_g D_g(x) > 0$. Multiplying the strict inequality by $\Pi(x) > 0$ is sign-faithful:

$$
c + \sum_h \frac{N_h(x)}{D_h(x)} > 0
\iff
\underbrace{c\prod_g D_g(x) + \sum_h N_h(x)\prod_{g\neq h}D_g(x)}_{=: P(x)} > 0 .
$$

$P$ has the required form with $\theta = c$ and admissible pairs, so $f(x) = 1 \iff P(x) > 0$ and $\mathrm{MFdeg}_{\pm}(f) \leq H$. $\square$

### Step 2. Dividing (the reverse inequality, with a strict-margin perturbation)

Let $H = \mathrm{MFdeg}_{\pm}(f)$ with admissible $(N_h, D_h)$, $\theta$, and $P$ sign-representing $f$. If $H = 0$ then $P = \theta$ is constant and $f$ is computed with $0$ atoms; if $f \equiv 0$ then $H^{*}(f) = 0$. So assume $H \geq 1$ and $f \not\equiv 0$.

Each $D_h > 0$, so $\Pi := \prod_h D_h > 0$, and with $Q(x) := \theta + \sum_h N_h(x)/D_h(x)$ we have $Q\,\Pi = P$, hence $P(x) > 0 \iff Q(x) > 0$, so $f(x) = 1 \iff Q(x) > 0$.

**Threshold shift.** Let $q_+ := \min\lbrace Q(x) : f(x) = 1\rbrace  > 0$ (finite nonempty set) and $\nu := q_+/3$, so $0 < \nu < q_+$. Put $Q_\nu := Q - \nu$. Then on $f^{-1}(1)$, $Q_\nu \geq q_+ - \nu > \nu > 0$; on $f^{-1}(0)$, $Q \leq 0$ so $Q_\nu \leq -\nu < 0$. Thus $f(x) = 1 \iff Q_\nu(x) > 0$ and $|Q_\nu(x)| \geq \nu$ for all $x$.

**Denominator perturbation.** Write $D_h(x) = d_{h,0} + \sum_i d_{h,i}x_i$. Pick a common strict sign $\sigma_h \in \lbrace \pm 1\rbrace $ for the nonzero slopes of $D_h$ (or $+1$ if all are zero), and replace each zero slope $d_{h,i}$ by $\sigma_h\varepsilon$, giving $D_h^\varepsilon$ with all slopes nonzero and of one strict sign. With $m_h := \min_x D_h(x) > 0$ and $|D_h^\varepsilon - D_h| \leq n\varepsilon$, choosing $n\varepsilon < m_h/2$ keeps $D_h^\varepsilon > m_h/2 > 0$, so each $(N_h, D_h^\varepsilon)$ is strictly admissible. Writing $M_h := \max_x |N_h(x)|$,

$$
\left| \frac{N_h}{D_h^\varepsilon} - \frac{N_h}{D_h} \right| = |N_h|\,\frac{|D_h - D_h^\varepsilon|}{D_h^\varepsilon D_h} \leq \frac{2 M_h n}{m_h^2}\,\varepsilon ,
$$

so with $B := \sum_h \tfrac{2M_h n}{m_h^2}$ and $Q_\nu^\varepsilon := (\theta - \nu) + \sum_h N_h/D_h^\varepsilon$ we get $|Q_\nu^\varepsilon - Q_\nu| \leq B\varepsilon$. Choosing $\varepsilon$ small enough that $B\varepsilon < \nu$ (and $n\varepsilon < m_h/2$) and using $|Q_\nu| \geq \nu$, the sign of $Q_\nu^\varepsilon$ matches $Q_\nu$ at every $x$:

$$
f(x) = 1 \iff Q_\nu^\varepsilon(x) > 0 .
$$

**Read off atoms.** Each $(N_h, D_h^\varepsilon)$ is strictly admissible, so by Lemma 2 each $N_h/D_h^\varepsilon$ is a one-head atom. Thus $Q_\nu^\varepsilon = (\theta - \nu) + \sum_h (\text{atom}_h)$ is a constant plus $H$ atoms whose threshold is $f$. By the normal form, $H^{*}(f) \leq H$. $\square$

Combining Steps 1 and 2, $H^{*}(f) = \mathrm{MFdeg}_{\pm}(f)$. $\blacksquare$

## Corollaries

1. **Recovers the threshold-degree bound.** The polynomial $P$ from Step 1 has total degree $\leq H = H^{*}(f)$ and sign-represents $f$, so $\deg_{\pm}(f) \leq H^{*}(f)$, recovering [006_threshold_degree_head_complexity_bound.md](006_threshold_degree_head_complexity_bound.md) from the normal form.

2. **Tangent-vector form.** With $F = \prod_h D_h$,

$$
P = \theta F + \sum_{h=1}^{H} N_h \prod_{g \neq h} D_g = \left.\frac{d}{dt}\right|_{t=0} \Big[(1 + t\theta)\prod_{h=1}^{H}(D_h + t N_h)\Big],
$$

so $P$ is a tangent vector at the point $\prod_h D_h$ to the variety of products of $H$ affine forms, with the base factors $D_h$ constrained to be positive on the cube with one-sided slopes. This is the bridge from $H^{*}$ toward a tangential-Chow algebraic invariant: dropping the positivity and one-sided-slope constraints yields a known-flavored (unrestricted) invariant that lower-bounds $H^{*}$.
