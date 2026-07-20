# Problem: Exact dictionary of one-head atoms (affine-ratio characterization)

## Background and definitions (all self-contained; nothing external is assumed)

Fix an integer $n \geq 1$. We work on the Boolean cube $\{0,1\}^n$. For a real number $\alpha > 0$ and a bit $b \in \{0,1\}$ we write $\alpha^{b}$ for the ordinary power, so $\alpha^{0} = 1$ and $\alpha^{1} = \alpha$.

A **one-head atom** is a function $\phi : \{0,1\}^n \to \mathbb{R}$ of the form

$$
\phi(x) \;=\; \frac{\eta + \sum_{i=1}^{n} \rho_i\, \alpha^{x_i}\,(m_i + \delta x_i)}{\gamma + \sum_{i=1}^{n} \rho_i\, \alpha^{x_i}},
$$

where the parameters satisfy

$$
\gamma > 0, \qquad \rho_1,\dots,\rho_n > 0, \qquad \alpha > 0,
$$

and

$$
\eta,\ \delta,\ m_1,\dots,m_n \in \mathbb{R}
$$

are arbitrary real numbers. (This is the exact scalar contribution of a single attention head to the query-token readout in the project's model; here it is taken as the definition.)

Call a function $A : \{0,1\}^n \to \mathbb{R}$ **affine** if there are real constants $a_0, a_1, \dots, a_n$ with $A(x) = a_0 + \sum_{i=1}^{n} a_i x_i$ for all $x \in \{0,1\}^n$. The constants $a_1,\dots,a_n$ are the **slopes** of $A$ and $a_0$ is its **constant term**. (On the cube the affine representation of a function is unique, since the monomials $1, x_1, \dots, x_n$ are linearly independent as functions on $\{0,1\}^n$ for $n \geq 1$.)

We say an affine function $D$ is **positive on the cube** if $D(x) > 0$ for every $x \in \{0,1\}^n$.

## Claim to prove

Prove BOTH of the following statements.

**Part A (necessity: every atom is an admissible affine ratio).**
Let $\phi$ be a one-head atom with parameters $\gamma,\rho_i,\alpha,\eta,\delta,m_i$ as above. Then $\phi = N/D$ where:

- $D(x) = d_0 + \sum_{i=1}^n d_i x_i$ with $d_0 = \gamma + \sum_{i=1}^n \rho_i$ and $d_i = \rho_i(\alpha - 1)$;
- $N(x) = e_0 + \sum_{i=1}^n e_i x_i$ with $e_0 = \eta + \sum_{i=1}^n \rho_i m_i$ and $e_i = \rho_i\big((\alpha - 1)m_i + \alpha\delta\big)$;
- $D$ is affine and positive on the cube;
- $N$ is affine;
- the slopes $d_1,\dots,d_n$ of $D$ all share one sign: they are all $> 0$ if $\alpha > 1$, all $= 0$ if $\alpha = 1$, and all $< 0$ if $\alpha < 1$. Equivalently, $\operatorname{sign}(d_i) = \operatorname{sign}(\alpha - 1)$ for every $i$.

**Part B (sufficiency: every strictly-monotone-denominator affine ratio is an atom).**
Let $N(x) = e_0 + \sum_{i=1}^n e_i x_i$ be an arbitrary affine function, and let $D(x) = d_0 + \sum_{i=1}^n d_i x_i$ be an affine function that is positive on the cube and whose slopes are either all strictly positive ($d_i > 0$ for all $i$) or all strictly negative ($d_i < 0$ for all $i$). Then the ratio $N/D$ is a one-head atom; that is, there exist parameters $\gamma > 0$, $\rho_i > 0$, $\alpha > 0$, and $\eta,\delta,m_i \in \mathbb{R}$ realizing it.

In particular, conclude the **dictionary**: the one-head atoms whose denominator has no zero slope are exactly the ratios $N/D$ with $N$ an arbitrary affine function and $D$ an affine function that is positive on the cube with all slopes strictly of one common sign.

## Guidance on what to establish (you must still prove each step rigorously)

1. Use the identity $\alpha^{x_i} = 1 + (\alpha - 1)x_i$, valid because $x_i \in \{0,1\}$, to expand both numerator and denominator into affine form, and read off the coefficients $d_0,d_i,e_0,e_i$ exactly as stated in Part A.
2. For positivity of $D$ on the cube in Part A: each summand $\rho_i \alpha^{x_i}$ is positive and $\gamma > 0$, so the original denominator is a sum of positive terms.
3. For the sign claim in Part A: $\rho_i > 0$, so $\operatorname{sign}(\rho_i(\alpha-1)) = \operatorname{sign}(\alpha - 1)$, independent of $i$.
4. For Part B, treat the two cases $d_i > 0$ (choose some $\alpha > 1$) and $d_i < 0$ (choose some $\alpha \in (0,1)$). In each case set $\rho_i = d_i/(\alpha - 1) > 0$, and show the constant term $\gamma := d_0 - \sum_i \rho_i$ can be made strictly positive by an appropriate choice of $\alpha$. Explicitly: in the positive case, $\sum_i \rho_i = \frac{1}{\alpha-1}\sum_i d_i \to 0$ as $\alpha \to \infty$, while $d_0 > 0$ is fixed (note $d_0 = D(\mathbf{0}) > 0$), so $\gamma > 0$ for large $\alpha$. In the negative case, note positivity of $D$ at the all-ones point gives $d_0 + \sum_i d_i > 0$, i.e. $d_0 > \sum_i |d_i|$, and $\sum_i \rho_i = \frac{1}{1-\alpha}\sum_i |d_i| \to \sum_i |d_i|$ as $\alpha \to 0^{+}$, so $\gamma = d_0 - \sum_i \rho_i \to d_0 - \sum_i|d_i| > 0$; hence $\gamma > 0$ for $\alpha$ small enough.
5. Given $\rho_i, \alpha, \gamma$ fixed as above (so the denominator already matches the target $D$), realize the arbitrary numerator $N$ by setting $\delta = 0$, then $m_i = e_i/(\rho_i(\alpha - 1))$ (well defined since $\alpha \neq 1$ and $\rho_i \neq 0$), and finally $\eta = e_0 - \sum_i \rho_i m_i$. Verify these reproduce the target coefficients $e_0, e_i$ from Part A's formulas with $\delta = 0$.
6. Conclude the dictionary statement by combining Parts A and B.

Provide a complete, rigorous, step-by-step proof of Parts A and B and the dictionary conclusion.
