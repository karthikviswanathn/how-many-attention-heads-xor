# Affine Atom Dictionary for One Head

## Statement

Work in the one-layer attention model of `model.md`. By Lemma 10, a one-head atom is a function

$$
\phi(x)=\frac{\eta+\sum_{i=1}^{n}\rho_i\alpha^{x_i}(m_i+\delta x_i)}{\gamma+\sum_{i=1}^{n}\rho_i\alpha^{x_i}},
$$

where $x\in\{0,1\}^n$, $\gamma>0$, $\rho_i>0$, $\alpha>0$, and $\eta,m_i,\delta\in\mathbb R$.

Prove that every such atom can be written on the Boolean cube as

$$
\phi(x)=\frac{N(x)}{D(x)},\qquad N(x)=a_0+\sum_{i=1}^{n}a_i x_i,\qquad D(x)=d_0+\sum_{i=1}^{n}d_i x_i,
$$

with $D(x)>0$ on $\{0,1\}^n$. Moreover, characterize exactly the possible affine denominators $D$:

1. $D$ is constant positive, namely $d_i=0$ for all $i$ and $d_0>0$;
2. all coordinate coefficients are strictly positive, namely $d_i>0$ for all $i$ and $d_0>0$;
3. all coordinate coefficients are strictly negative and the all-ones value is positive, namely $d_i<0$ for all $i$ and $d_0+\sum_i d_i>0$.

Conversely, every affine denominator in one of these three classes arises from some choice of $\gamma>0$, $\rho_i>0$, and $\alpha>0$.

Also record the numerator freedom needed for later cleared-denominator arguments: if $D$ is nonconstant, then any affine numerator $N$ can be realized with that $D$; if $D$ is constant, then the direct atom representation has numerator coefficients either all strictly positive, all strictly negative, or all zero, while the constant coefficient is arbitrary.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Use $x_i^2=x_i \Rightarrow \alpha^{x_i}=1+(\alpha-1)x_i$** to read off $d_i=\rho_i(\alpha-1)$, $d_0=\gamma+\sum\rho_i$; this single identity gives the affine form and the whole denominator trichotomy via the sign of $\alpha-1$.
2. **Frame the trichotomy as shared-base sign-uniformity** ($\rho_i>0$, one $\alpha$): the genuinely informative line, and the reason mixed-sign positive denominators are excluded.
3. **Converse = explicit linear feasibility:** set $\rho_i=d_i/(\alpha-1)$, $\gamma=d_0-\sum\rho_i$, choose $\alpha$ large (class 2) or near $0$ (class 3); the feasibility threshold is exactly the corner condition $d_0+\sum d_i>0$ — cite Farkas/Fourier–Motzkin only as the framing.
4. **Positivity:** forward is a sum-of-positives (`Finset.sum_pos`, `Real.exp_pos`); converse positivity-on-cube reduces to a single corner by coordinatewise monotonicity (`Monotone.map_min`, `lineMap_mono`) / Bauer's principle.
5. **Numerator freedom:** treat $(m_i,\eta)\mapsto(a_i,a_0)$ as a linear map, invertible iff $\alpha\ne1$ — directly yields "nonconstant $D$ ⇒ any $N$" and "constant $D$ ⇒ $a_i=\rho_i\delta$ uniform-sign."
