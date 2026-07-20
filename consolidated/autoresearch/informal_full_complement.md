# Problem: Head complexity is invariant under complementing all inputs

## Background and definitions (self-contained)

Fix $n \geq 1$, work on $\{0,1\}^n$. For $\alpha > 0$, $b \in \{0,1\}$: $\alpha^0 = 1$, $\alpha^1 = \alpha$.

A **one-head atom** is $\phi(x) = \dfrac{\eta + \sum_{i=1}^n \rho_i \alpha^{x_i}(m_i + \delta x_i)}{\gamma + \sum_{i=1}^n \rho_i \alpha^{x_i}}$ with $\gamma>0,\rho_i>0,\alpha>0$ and $\eta,\delta,m_i \in \mathbb{R}$.

**Established normal form (use as the definition of head complexity).** $H^{*}(f) \leq H$ iff there exist one-head atoms $\phi_1,\dots,\phi_H$ and $c \in \mathbb{R}$ with $f(x) = 1 \iff c + \sum_{h=1}^H \phi_h(x) > 0$ for all $x$.

For $x \in \{0,1\}^n$ write $\bar{x} = \mathbf{1} - x = (1 - x_1, \dots, 1 - x_n)$, and define the **input-complement** $f^{c}(x) := f(\bar{x})$.

## Claim to prove

For every $f : \{0,1\}^n \to \{0,1\}$,

$$
H^{*}(f^{c}) = H^{*}(f).
$$

> Complementing **all** inputs is free, reflecting a global $0 \leftrightarrow 1$ symmetry of the model. (Contrast: complementing a **single** input is in general *not* free, because all heads share one base $\alpha$; this lemma works precisely because $x \mapsto \bar x$ replaces $\alpha$ by $1/\alpha$ uniformly across every coordinate.)

## Guidance (prove every step rigorously)

**Key step: the input-complement of an atom is an atom.** Let $\phi$ be a one-head atom with parameters $\gamma,\alpha,\{\rho_i\},\eta,\delta,\{m_i\}$. Consider $\phi(\bar x) = \phi(1-x_1,\dots,1-x_n)$.

1. For each $i$ and $x_i \in \{0,1\}$, $\alpha^{1-x_i} = \alpha \cdot \alpha^{-x_i} = \alpha\,(1/\alpha)^{x_i}$. (Check both cases $x_i=0,1$.)

2. Define new parameters
   $$ \alpha' = 1/\alpha,\qquad \rho_i' = \rho_i\alpha,\qquad m_i' = m_i + \delta,\qquad \delta' = -\delta, $$
   and keep $\gamma' = \gamma$, $\eta' = \eta$. Show $\alpha' > 0$, $\rho_i' > 0$, $\gamma' > 0$, so these are valid atom parameters.

3. Verify the denominator transforms correctly:
   $$ \gamma + \sum_i \rho_i \alpha^{1-x_i} = \gamma + \sum_i \rho_i' \alpha'^{x_i}. $$

4. Verify the numerator transforms correctly. Using $m_i + \delta(1-x_i) = (m_i + \delta) - \delta x_i = m_i' + \delta' x_i$,
   $$ \eta + \sum_i \rho_i \alpha^{1-x_i}(m_i + \delta(1-x_i)) = \eta + \sum_i \rho_i' \alpha'^{x_i}(m_i' + \delta' x_i). $$

5. Conclude $\phi(\bar x) = \dfrac{\eta + \sum_i \rho_i' \alpha'^{x_i}(m_i' + \delta' x_i)}{\gamma + \sum_i \rho_i' \alpha'^{x_i}}$, which is a one-head atom in the variable $x$.

**Main argument.** Let $H = H^{*}(f)$, witnessed by atoms $\phi_1,\dots,\phi_H$ and constant $c$ with $f(y) = 1 \iff c + \sum_h \phi_h(y) > 0$. For any $x$, set $y = \bar x$; then $f^{c}(x) = f(\bar x) = f(y)$ and
$$ f^{c}(x) = 1 \iff c + \sum_h \phi_h(\bar x) > 0. $$
By the key step each $x \mapsto \phi_h(\bar x)$ is a one-head atom, so $f^{c}$ is represented by $H$ atoms and constant $c$; hence $H^{*}(f^{c}) \leq H = H^{*}(f)$. Applying the same to $f^{c}$ (and noting $(f^{c})^{c} = f$, since $\bar{\bar x} = x$) gives $H^{*}(f) \leq H^{*}(f^{c})$, hence equality.

Give a complete, rigorous proof.
