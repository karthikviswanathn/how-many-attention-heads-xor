# Problem: Sparse single-polarity threshold-density upper bound

## Background and definitions (self-contained)

Fix $n\geq 1$, work on $\{0,1\}^n$. For $\alpha>0$, $b\in\{0,1\}$: $\alpha^0=1$, $\alpha^1=\alpha$.

A **one-head atom** is $\phi(x)=\dfrac{\eta+\sum_{i=1}^n\rho_i\alpha^{x_i}(m_i+\delta x_i)}{\gamma+\sum_{i=1}^n\rho_i\alpha^{x_i}}$ with $\gamma>0,\rho_i>0,\alpha>0$ and $\eta,\delta,m_i\in\mathbb{R}$.

**Established normal form (use as the definition of head complexity).** $H^{*}(f)\leq H$ iff there exist one-head atoms $\phi_1,\dots,\phi_H$ and $c\in\mathbb{R}$ with $f(x)=1 \iff c+\sum_{h=1}^H\phi_h(x)>0$ for all $x$.

A **monotone subcube indicator** is $\mathbf{1}_{T}$ where $T$ is given by a nonempty $S\subseteq\{1,\dots,n\}$ as either $\mathbf{1}_T(x)=\prod_{i\in S}x_i$ (positive type) or $\mathbf{1}_T(x)=\prod_{i\in S}(1-x_i)$ (negative type); so $\mathbf{1}_T(x)\in\{0,1\}$ and equals $1$ exactly on the subcube.

## Claim to prove

Let $T_1,\dots,T_s$ be monotone subcubes (each single-polarity, as above), let $c_1,\dots,c_s,\theta\in\mathbb{R}$, and define the real **score**

$$
\Sigma(x) := \theta + \sum_{j=1}^{s} c_j\, \mathbf{1}_{T_j}(x).
$$

Suppose $f:\{0,1\}^n\to\{0,1\}$ is computed with a strict margin by this score, i.e.

$$
f(x)=1 \iff \Sigma(x)>0 \qquad\text{and}\qquad \Sigma(x)\neq 0 \ \text{ for all } x\in\{0,1\}^n.
$$

Then

$$
H^{*}(f) \leq s.
$$

> This generalizes the monotone-term DNF bound (the case $c_j=1$, $\theta=-\tfrac12$): any function expressed as a thresholded sparse sum of $s$ single-polarity subcube indicators with positive margin needs at most $s$ heads.

## Guidance (prove every step rigorously)

The plan: replace each indicator $\mathbf{1}_{T_j}$ by a one-head atom $b_j$ that approximates it uniformly, and use the finite-cube margin of $\Sigma$ to keep the classification exact.

1. **A calibrated bump for each subcube.** For $\lambda>0$ and $\epsilon>0$ define a strictly one-sided affine violation count
   $$ v_j(x) = \sum_{i=1}^n w^{(j)}_i (1-x_i) \ \text{(positive type)}, \qquad v_j(x) = \sum_{i=1}^n w^{(j)}_i x_i \ \text{(negative type)}, $$
   with $w^{(j)}_i = 1$ for $i\in S_j$ and $w^{(j)}_i=\epsilon$ for $i\notin S_j$. Show $v_j\geq 0$, with $0\leq v_j(x)\leq \epsilon n$ when $\mathbf{1}_{T_j}(x)=1$ and $v_j(x)\geq 1$ when $\mathbf{1}_{T_j}(x)=0$.

2. **The bump is a one-head atom.** Set $b_j(x)=\dfrac{1}{1+\lambda v_j(x)}$. Show $b_j$ is a one-head atom by exhibiting parameters (negative type: $\alpha>1$, $\rho_i=\lambda w^{(j)}_i/(\alpha-1)$, $\gamma=1-\sum_i\rho_i>0$ for $\alpha$ large, $\eta=1$, $\delta=0$, $m_i=0$, giving denominator $1+\lambda v_j$ and numerator $1$; positive type: $\alpha\in(0,1)$ analogously). Note $1+\lambda v_j(x)\geq 1>0$.

3. **Uniform approximation.** Show that for $x$ with $\mathbf{1}_{T_j}(x)=1$, $1\geq b_j(x)\geq \dfrac{1}{1+\lambda\epsilon n}$, and for $x$ with $\mathbf{1}_{T_j}(x)=0$, $0\leq b_j(x)\leq \dfrac{1}{1+\lambda}$. Conclude the pointwise error bound
   $$ |b_j(x)-\mathbf{1}_{T_j}(x)| \leq \max\Big(1-\tfrac{1}{1+\lambda\epsilon n},\ \tfrac{1}{1+\lambda}\Big) =: \rho(\lambda,\epsilon) $$
   for every $x$, and that $\rho(\lambda,\epsilon)\to 0$ when $\lambda\to\infty$ with $\lambda\epsilon\to 0$ (e.g. $\epsilon=\lambda^{-2}$).

4. **Use the margin.** Let $\mu:=\min_{x\in\{0,1\}^n}|\Sigma(x)|>0$ (finite cube, $\Sigma$ nowhere zero). Set $C:=\sum_{j=1}^s|c_j|$. Define $\widetilde\Sigma(x):=\theta+\sum_{j=1}^s c_j b_j(x)$. Show
   $$ |\widetilde\Sigma(x)-\Sigma(x)| \leq \sum_{j=1}^s |c_j|\,|b_j(x)-\mathbf{1}_{T_j}(x)| \leq C\,\rho(\lambda,\epsilon). $$
   Choose $\lambda$ large and $\epsilon=\lambda^{-2}$ so that $C\,\rho(\lambda,\epsilon)<\mu$. Then for every $x$, $\widetilde\Sigma(x)$ has the same sign as $\Sigma(x)$ (because $|\Sigma(x)|\geq\mu$), so
   $$ f(x)=1 \iff \Sigma(x)>0 \iff \widetilde\Sigma(x)>0. $$

5. **Conclude.** $\widetilde\Sigma = \theta + \sum_{j=1}^s c_j b_j$ is a constant plus $s$ one-head atoms (each $c_j b_j$ is a one-head atom: scale the numerator parameter $\eta$ by $c_j$, i.e. $\eta=c_j$, keeping the same positive denominator). By the normal form, $H^{*}(f)\leq s$.

Note the corollary: taking all $c_j=1$ and $\theta=-\tfrac12$ recovers the $s$-term single-polarity DNF bound.

Give a complete, rigorous proof.
