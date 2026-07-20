# Problem: Head complexity is invariant under output negation and input permutation

## Background and definitions (self-contained)

Fix $n \geq 1$ and work on $\{0,1\}^n$. For $\alpha > 0$, $b \in \{0,1\}$: $\alpha^0 = 1$, $\alpha^1 = \alpha$.

A **one-head atom** is a function $\phi : \{0,1\}^n \to \mathbb{R}$ of the form

$$
\phi(x) = \frac{\eta + \sum_{i=1}^{n} \rho_i \alpha^{x_i}(m_i + \delta x_i)}{\gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i}},
\qquad \gamma>0,\ \rho_i>0,\ \alpha>0,\ \eta,\delta,m_i\in\mathbb{R}.
$$

**Established normal form (use as the definition of head complexity).** For any $H \geq 0$,

$$
H^{*}(f) \leq H
\iff
\exists\ \text{one-head atoms } \phi_1,\dots,\phi_H,\ c\in\mathbb{R}:\quad
\big(f(x)=1 \iff c + \textstyle\sum_{h=1}^{H}\phi_h(x) > 0\big)\ \forall x.
$$

Consequently $H^{*}(f)$ is the least such $H$, and is finite for every $f$.

## Claim to prove

Let $f : \{0,1\}^n \to \{0,1\}$ be arbitrary. Prove the two invariances:

**(1) Output negation.** Let $\overline{f} := 1 - f$ be the complementary function. Then

$$
H^{*}(\overline{f}) = H^{*}(f).
$$

**(2) Input permutation.** Let $\pi$ be a permutation of $\{1,\dots,n\}$ and define $f^{\pi}(x) := f(x_{\pi(1)}, \dots, x_{\pi(n)})$. Then

$$
H^{*}(f^{\pi}) = H^{*}(f).
$$

## Guidance (prove every step rigorously)

For (1):

1. First show that if $\phi = N/D$ is a one-head atom then so is $-\phi$. Concretely, expanding via $\alpha^{x_i} = 1 + (\alpha-1)x_i$, the numerator and denominator are affine and the denominator is positive on the cube with slopes all of one sign; negating only the numerator parameters ($\eta \mapsto -\eta$, $m_i \mapsto -m_i$, $\delta \mapsto -\delta$) keeps the same positive denominator and negates $\phi$. Hence $-\phi$ is a one-head atom realized by the same $\gamma, \rho_i, \alpha$.
2. Suppose $H^{*}(f) = H$, witnessed by atoms $\phi_1,\dots,\phi_H$ and constant $c$ with $f(x) = 1 \iff c + \sum_h \phi_h(x) > 0$. Let $S(x) := c + \sum_h \phi_h(x)$. If $f \equiv 0$ then $\overline f \equiv 1$ and both have head complexity $0$; otherwise let $s_{\min} := \min\{S(x) : f(x) = 1\} > 0$, which exists and is positive because the cube is finite and $S > 0$ exactly on $f^{-1}(1) \neq \emptyset$. Pick any $\mu$ with $0 < \mu < s_{\min}$.
3. Define $S'(x) := \mu - c + \sum_h(-\phi_h)(x) = -S(x) + \mu$. Show $\overline f(x) = 1 \iff S'(x) > 0$ for all $x$: on $f^{-1}(1)$, $S(x) \geq s_{\min} > \mu$ so $S'(x) < 0$ ($\overline f = 0$ there); on $f^{-1}(0)$, $S(x) \leq 0$ so $S'(x) \geq \mu > 0$ ($\overline f = 1$ there). Hence $\overline f$ is computed by the $H$ atoms $-\phi_h$ with constant $\mu - c$, so $H^{*}(\overline f) \leq H = H^{*}(f)$.
4. Apply the same inequality to $\overline f$ (whose complement is $f$) to get $H^{*}(f) \leq H^{*}(\overline f)$, hence equality.

For (2):

1. Show that if $\phi$ is a one-head atom with parameters $\gamma, \alpha, \{\rho_i\}, \eta, \delta, \{m_i\}$, then the function $x \mapsto \phi(x_{\pi(1)}, \dots, x_{\pi(n)})$ is again a one-head atom, realized by the same $\gamma, \alpha, \eta, \delta$ and the permuted coordinate parameters $\rho'_i := \rho_{\pi(i)}$, $m'_i := m_{\pi(i)}$. (Both $\sum_i \rho_i \alpha^{y_i}$ evaluated at $y = (x_{\pi(1)},\dots)$ and the analogous numerator sum are just reindexings of the sum over $i$.)
2. Conclude: a representation of $f$ by $H$ atoms and constant $c$ yields, by composing each atom with $\pi$, a representation of $f^{\pi}$ by $H$ atoms and the same constant $c$. Hence $H^{*}(f^{\pi}) \leq H^{*}(f)$.
3. Apply the same to $f^{\pi}$ with the inverse permutation $\pi^{-1}$ (noting $(f^{\pi})^{\pi^{-1}} = f$) to get the reverse inequality, hence equality.

Give a complete, rigorous proof of both invariances.
