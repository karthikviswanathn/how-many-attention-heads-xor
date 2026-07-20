# Problem: Calibrated positive-weighted-sum interpolation

## Background and definitions (self-contained)

Fix $n\geq 1$, work on $\{0,1\}^n$. For $\alpha>0$, $b\in\{0,1\}$: $\alpha^0=1$, $\alpha^1=\alpha$.

A **one-head atom** is $\phi(x)=\dfrac{\eta+\sum_{i=1}^n\rho_i\alpha^{x_i}(m_i+\delta x_i)}{\gamma+\sum_{i=1}^n\rho_i\alpha^{x_i}}$ with $\gamma>0,\rho_i>0,\alpha>0$ and $\eta,\delta,m_i\in\mathbb{R}$.

**Established normal form (use as the definition of head complexity).** $H^{*}(f)\leq H$ iff there exist one-head atoms $\phi_1,\dots,\phi_H$ and $c\in\mathbb{R}$ with $f(x)=1 \iff c+\sum_{h=1}^H\phi_h(x)>0$ for all $x$.

Let $t(x)=\sum_{i=1}^n\lambda_i x_i$ with all $\lambda_i>0$, and let $\mathrm{Im}(t)=\{\tau_1<\tau_2<\dots<\tau_M\}$ be its set of $M$ distinct values on the cube (so $\tau_1=0$, $\tau_M=\sum_i\lambda_i$, and $M\geq 1$).

## Claim to prove

**Part 1 (calibrated interpolation).** For every function $G:\mathrm{Im}(t)\to\mathbb{R}$ there exist $M-1$ one-head atoms $\psi_1,\dots,\psi_{M-1}$ and a constant $a_0\in\mathbb{R}$ such that

$$
a_0+\sum_{j=1}^{M-1}\psi_j(x) = G(t(x)) \qquad \text{for all } x\in\{0,1\}^n.
$$

That is, any real-valued table on the $M$ levels of a positive weighted sum is exactly represented as a constant plus $M-1$ one-head atoms (a calibrated real feature, not merely a sign).

**Part 2 (additive composition corollary).** Suppose

$$
f(x) = \mathbf{1}\Big[\theta + \sum_{r=1}^{s} a_r\, G_r\big(t_r(x)\big) > 0\Big],
$$

where each $t_r(x)=\sum_i\lambda_{ri}x_i$ has all $\lambda_{ri}>0$, each $G_r:\mathrm{Im}(t_r)\to\mathbb{R}$ is arbitrary, and $a_r,\theta\in\mathbb{R}$. Then

$$
H^{*}(f) \leq \sum_{r=1}^{s}\big(|\mathrm{Im}(t_r)|-1\big).
$$

## Guidance (prove every step rigorously)

### Part 1

1. **Kernels are one-head atoms.** Fix any real $\beta>0$. Show $k_\beta(x):=\dfrac{1}{\beta+t(x)}$ is a one-head atom: its denominator $\beta+\sum_i\lambda_i x_i$ is affine, equals $\gamma+\sum_i\rho_i\alpha^{x_i}$ for $\alpha>1$, $\rho_i=\lambda_i/(\alpha-1)>0$, $\gamma=\beta-\sum_i\rho_i$ (which is $>0$ for $\alpha$ large since $\beta>0$); its numerator $1$ is obtained with $\delta=0$, $m_i=0$, $\eta=1$. More generally, for any real $c$, $c\cdot k_\beta$ is a one-head atom (take $\eta=c$, $m_i=\delta=0$). Note $\beta+t(x)>0$ on the cube since $\beta>0$ and $t(x)\geq 0$.

2. **Choose distinct shifts.** Pick $M-1$ distinct positive reals $\beta_1,\dots,\beta_{M-1}$ (e.g. $\beta_j=j$). Each $\beta_j+\tau_\ell>0$ since $\beta_j>0$ and $\tau_\ell\geq 0$.

3. **Solve the interpolation system.** Seek $a_0,c_1,\dots,c_{M-1}\in\mathbb{R}$ with
   $$ a_0+\sum_{j=1}^{M-1}\frac{c_j}{\beta_j+\tau_\ell} = G(\tau_\ell), \qquad \ell=1,\dots,M. $$
   This is an $M\times M$ linear system in $(a_0,c_1,\dots,c_{M-1})$ with coefficient matrix having a column of ones and columns $\big(\tfrac{1}{\beta_j+\tau_\ell}\big)_\ell$.

4. **Invertibility via a degree argument.** Show the only solution of the homogeneous system is zero, hence the matrix is invertible. Suppose $a_0+\sum_j\frac{c_j}{\beta_j+\tau_\ell}=0$ for all $\ell$. Consider the rational function
   $$ \Phi(s) = a_0+\sum_{j=1}^{M-1}\frac{c_j}{\beta_j+s} = \frac{R(s)}{\prod_{j=1}^{M-1}(\beta_j+s)}, $$
   where $R(s)=a_0\prod_{j}(\beta_j+s)+\sum_{j}c_j\prod_{j'\neq j}(\beta_{j'}+s)$ is a polynomial of degree $\leq M-1$. Since $\beta_j+\tau_\ell\neq 0$, $\Phi(\tau_\ell)=0$ forces $R(\tau_\ell)=0$ for all $M$ distinct $\tau_\ell$. A polynomial of degree $\leq M-1$ with $M$ distinct roots is identically zero, so $R\equiv 0$. Evaluating $R$ at $s=-\beta_{j_0}$ kills every term except the $j_0$ one, giving $c_{j_0}\prod_{j'\neq j_0}(\beta_{j'}-\beta_{j_0})=0$; since the $\beta_j$ are distinct, $c_{j_0}=0$ for every $j_0$. Then $R(s)=a_0\prod_j(\beta_j+s)\equiv 0$ forces $a_0=0$. Hence the homogeneous system has only the zero solution and the matrix is invertible.

5. **Assemble.** With the unique solution $(a_0,c_1,\dots,c_{M-1})$, set $\psi_j(x):=c_j\,k_{\beta_j}(x)$, a one-head atom by Step 1. For every $x$, $t(x)=\tau_\ell$ for some $\ell$, so by Step 3 $a_0+\sum_j\psi_j(x)=a_0+\sum_j\frac{c_j}{\beta_j+\tau_\ell}=G(\tau_\ell)=G(t(x))$. This proves Part 1.

### Part 2

1. Apply Part 1 to each block $G_r$ on $t_r$: get $M_r-1$ atoms ($M_r=|\mathrm{Im}(t_r)|$) and a constant $a_0^{(r)}$ with $a_0^{(r)}+\sum_j\psi_j^{(r)}(x)=G_r(t_r(x))$. Absorbing the scalar $a_r$ (replace $G_r$ by $a_rG_r$, or scale each atom and constant by $a_r$; scaling a one-head atom by a real keeps it a one-head atom), get $a_r G_r(t_r(x)) = a_r a_0^{(r)} + \sum_j (a_r\psi_j^{(r)})(x)$ with $M_r-1$ atoms.

2. Sum over $r$ and add $\theta$: the total constant is $c:=\theta+\sum_r a_r a_0^{(r)}$ and the total number of atoms is $\sum_r(M_r-1)$, and
   $$ c+\sum_{r}\sum_{j}(a_r\psi_j^{(r)})(x) = \theta+\sum_r a_r G_r(t_r(x)). $$
3. Therefore $f(x)=1 \iff c+(\text{sum of } \sum_r(M_r-1) \text{ atoms})>0$, so by the normal form $H^{*}(f)\leq\sum_r(M_r-1)$.

State as a remark that Part 1 with $G=F$ (a $\{0,1\}$-valued table) and a final threshold recovers the weighted-sum upper bound $H^{*}(f)\leq M-1$; the new content is the exact real (calibrated) representation, which is what makes blocks additively composable in Part 2.

Give a complete, rigorous proof of Parts 1 and 2.
