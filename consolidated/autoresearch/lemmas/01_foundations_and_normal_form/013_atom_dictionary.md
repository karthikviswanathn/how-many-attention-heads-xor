# Atom Dictionary

## Statement

Work on the Boolean cube $\lbrace 0,1\rbrace ^n$, $n \geq 1$. For $\alpha > 0$ and $b \in \lbrace 0,1\rbrace $, $\alpha^{b}$ is the ordinary power. A **one-head atom** is a function $\phi : \lbrace 0,1\rbrace ^n \to \mathbb{R}$ of the form

$$
\phi(x) = \frac{\eta + \sum_{i=1}^{n} \rho_i \alpha^{x_i}(m_i + \delta x_i)}{\gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i}},
\qquad \gamma>0,\ \rho_i>0,\ \alpha>0,\ \eta,\delta,m_i\in\mathbb{R}.
$$

A function $A(x) = a_0 + \sum_{i=1}^n a_i x_i$ is **affine**, with **slopes** $a_1,\dots,a_n$; it is **positive on the cube** if $A(x) > 0$ for all $x$.

**Part A (necessity).** Every one-head atom equals $N/D$ where $D(x) = d_0 + \sum_i d_i x_i$ with $d_0 = \gamma + \sum_i \rho_i$ and $d_i = \rho_i(\alpha-1)$, and $N(x) = e_0 + \sum_i e_i x_i$ with $e_0 = \eta + \sum_i \rho_i m_i$ and $e_i = \rho_i((\alpha-1)m_i + \alpha\delta)$. Here $D$ is affine and positive on the cube, $N$ is affine, and the slopes $d_1,\dots,d_n$ all share the sign of $\alpha - 1$ (all $>0$ if $\alpha>1$, all $=0$ if $\alpha=1$, all $<0$ if $\alpha<1$).

**Part B (sufficiency).** For any affine $N$ and any affine $D$ that is positive on the cube with all slopes strictly of one common sign (all $d_i > 0$ or all $d_i < 0$), the ratio $N/D$ is a one-head atom.

> **Dictionary.** The one-head atoms whose denominator has no zero slope are exactly the ratios $N/D$ with $N$ an arbitrary affine function and $D$ an affine function positive on the cube whose slopes are all strictly of one common sign.

This is the structural refinement underlying the cleared-denominator normal form [016_cleared_denominator_invariant.md](016_cleared_denominator_invariant.md). It also exposes the model's **monotone bias**: because $e_1 - e_0$ is position-independent, a single shared $\alpha$ governs every coordinate, so each head's denominator is a monotone affine form.

## Proof

### Part A

1. Since $x_i \in \lbrace 0,1\rbrace $, a case split gives $\alpha^{x_i} = 1 + (\alpha - 1)x_i$.

2. The denominator $D(x) = \gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i}$ expands as

$$
\begin{aligned}
D(x)
&= \gamma + \sum_{i=1}^{n} \rho_i \bigl(1 + (\alpha - 1)x_i\bigr)
= \Big(\gamma + \sum_{i=1}^{n} \rho_i\Big) + \sum_{i=1}^{n} \rho_i(\alpha - 1)x_i,
\end{aligned}
$$

so $D$ is affine with $d_0 = \gamma + \sum_i \rho_i$ and $d_i = \rho_i(\alpha - 1)$.

3. Since $\gamma>0$, $\rho_i>0$, $\alpha>0$, each term $\rho_i\alpha^{x_i}>0$, hence $D(x) > 0$ on the cube.

4. For the numerator, again using $x_i^2 = x_i$ on $\lbrace 0,1\rbrace $,

$$
\alpha^{x_i}(m_i + \delta x_i)
= \bigl(1 + (\alpha-1)x_i\bigr)(m_i + \delta x_i)
= m_i + \bigl((\alpha-1)m_i + \alpha\delta\bigr)x_i .
$$

5. Multiplying by $\rho_i$ and summing,

$$
N(x) = \Big(\eta + \sum_{i=1}^{n}\rho_i m_i\Big) + \sum_{i=1}^{n}\rho_i\bigl((\alpha-1)m_i + \alpha\delta\bigr)x_i ,
$$

so $N$ is affine with $e_0 = \eta + \sum_i \rho_i m_i$ and $e_i = \rho_i((\alpha-1)m_i + \alpha\delta)$.

6. As $\phi = N/D$, this proves $\phi$ is an affine ratio with $D$ positive on the cube. Finally $d_i = \rho_i(\alpha-1)$ and $\rho_i>0$ give $\mathrm{sign}(d_i) = \mathrm{sign}(\alpha-1)$ for all $i$. $\square$

### Part B

Let $N(x) = e_0 + \sum_i e_i x_i$ and $D(x) = d_0 + \sum_i d_i x_i$ with $D > 0$ on the cube and all $d_i$ strictly of one sign.

**Case 1: all $d_i > 0$.** Since $D(\mathbf 0) = d_0$, positivity gives $d_0 > 0$. Choose $\alpha > 1$ large enough that $\frac{1}{\alpha-1}\sum_i d_i < d_0$ (possible since $\sum_i d_i$ is fixed and $(\alpha-1)^{-1}\to 0$). Set $\rho_i = d_i/(\alpha-1) > 0$ and $\gamma = d_0 - \sum_i \rho_i > 0$. Then $\rho_i(\alpha-1) = d_i$ and $\gamma + \sum_i \rho_i = d_0$.

**Case 2: all $d_i < 0$.** Since $D(\mathbf 1) = d_0 + \sum_i d_i > 0$ and $d_i < 0$ gives $\sum_i d_i = -\sum_i |d_i|$, we have $d_0 - \sum_i |d_i| > 0$. Choose $\alpha \in (0,1)$ small enough that $\frac{1}{1-\alpha}\sum_i |d_i| < d_0$ (possible since the left side $\to \sum_i |d_i| < d_0$ as $\alpha \to 0^+$). Set $\rho_i = d_i/(\alpha-1) = |d_i|/(1-\alpha) > 0$ and $\gamma = d_0 - \sum_i \rho_i > 0$. Then $\rho_i(\alpha-1) = d_i$ and $\gamma + \sum_i \rho_i = d_0$.

**Numerator realization.** In both cases we have $\alpha > 0$, $\alpha \neq 1$, $\rho_i > 0$, $\gamma > 0$, with $d_0 = \gamma + \sum_i \rho_i$ and $d_i = \rho_i(\alpha-1)$. Put $\delta = 0$, $m_i = e_i/(\rho_i(\alpha-1))$ (well defined since $\rho_i \neq 0 \neq \alpha-1$), and $\eta = e_0 - \sum_i \rho_i m_i$. Then $\rho_i((\alpha-1)m_i + \alpha\delta) = \rho_i(\alpha-1)m_i = e_i$ and $\eta + \sum_i \rho_i m_i = e_0$. By Part A's coefficient formulas, the constructed atom has denominator $D$ and numerator $N$, so it equals $N/D$ on the cube. $\square$

### Dictionary conclusion

By Part A, every one-head atom is an affine ratio $N/D$ with $D$ positive on the cube and slopes all of the common sign of $\alpha-1$; the denominator has no zero slope exactly when $\alpha \neq 1$, forcing all slopes strictly of one sign. By Part B, every such ratio is realized. Hence the two descriptions coincide. $\blacksquare$

## Consequence

The dictionary turns head complexity into a question about ratios of affine forms with a one-sided (monotone) positive denominator. Clearing the positive denominators of a sum of atoms yields the cleared-denominator polynomial normal form [016_cleared_denominator_invariant.md](016_cleared_denominator_invariant.md), and the monotone-bias constraint on denominators is what separates this model's invariant from an unrestricted polynomial threshold degree.
