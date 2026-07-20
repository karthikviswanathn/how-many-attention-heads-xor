# Problem: Restricting a coordinate cannot increase head complexity

## Background and definitions (self-contained)

Fix $n \geq 2$ and work on $\{0,1\}^n$. For $\alpha > 0$, $b \in \{0,1\}$: $\alpha^0 = 1$, $\alpha^1 = \alpha$.

A **one-head atom on $\{0,1\}^n$** is a function $\phi : \{0,1\}^n \to \mathbb{R}$ of the form

$$
\phi(x) = \frac{\eta + \sum_{i=1}^{n} \rho_i \alpha^{x_i}(m_i + \delta x_i)}{\gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i}},
\qquad \gamma>0,\ \rho_i>0,\ \alpha>0,\ \eta,\delta,m_i\in\mathbb{R}.
$$

A one-head atom on $\{0,1\}^{n-1}$ is defined identically with the index set $\{1,\dots,n-1\}$ (or any $(n-1)$-element index set).

**Established normal form (use as the definition of head complexity).** For any integer $H \geq 0$ and any $g : \{0,1\}^{N} \to \{0,1\}$,

$$
H^{*}(g) \leq H
\iff
\exists\ \text{one-head atoms on } \{0,1\}^N\ \phi_1,\dots,\phi_H,\ c\in\mathbb{R}:\quad
\big(g(x)=1 \iff c + \textstyle\sum_{h=1}^{H}\phi_h(x) > 0\big)\ \forall x.
$$

So $H^{*}(g)$ is the least such $H$.

**Restriction.** Fix a coordinate index $k \in \{1,\dots,n\}$ and a value $c_0 \in \{0,1\}$. The **restriction** $f|_{x_k = c_0} : \{0,1\}^{n-1} \to \{0,1\}$ is the function of the remaining $n-1$ coordinates obtained by fixing $x_k = c_0$.

## Claim to prove

For every $f : \{0,1\}^n \to \{0,1\}$, every coordinate $k$, and every value $c_0 \in \{0,1\}$,

$$
H^{*}\big(f|_{x_k = c_0}\big) \;\leq\; H^{*}(f).
$$

By iterating, for any subset of coordinates fixed to any values, the resulting subfunction $g$ satisfies $H^{*}(g) \leq H^{*}(f)$.

State and prove also the two consequences:

- **(Lower bounds by restriction.)** If some restriction of $f$ to a sub-cube equals (a relabeling of) a function $g$, then $H^{*}(f) \geq H^{*}(g)$. In particular, since $H^{*}(\mathrm{XOR}_m) = m$ (established), any $f$ having a sub-cube restriction equal to $\mathrm{XOR}_m$ satisfies $H^{*}(f) \geq m$.
- **(Checkerboard as a special case.)** A $2$-bit checkerboard restriction is $\mathrm{XOR}_2$ on two coordinates, so it forces $H^{*}(f) \geq 2$.

## Guidance (prove every step rigorously)

The single key fact is that a one-head atom stays a one-head atom under fixing one coordinate.

1. **Restricting an atom yields an atom.** Let $\phi$ be a one-head atom on $\{0,1\}^n$ with parameters $\gamma, \alpha, \{\rho_i\}_{i=1}^n, \eta, \delta, \{m_i\}_{i=1}^n$. Fix $x_k = c_0$. Split off the $k$-th terms: the numerator's $k$-th summand becomes the constant $\rho_k \alpha^{c_0}(m_k + \delta c_0)$, and the denominator's $k$-th summand becomes the constant $\rho_k \alpha^{c_0}$. Define new parameters on the index set $\{1,\dots,n\}\setminus\{k\}$ (an $(n-1)$-element set):
   $$ \gamma' := \gamma + \rho_k \alpha^{c_0}, \qquad \eta' := \eta + \rho_k \alpha^{c_0}(m_k + \delta c_0), $$
   keeping the same $\alpha, \delta$ and the same $\rho_i, m_i$ for $i \neq k$. Show that
   $$ \phi(x)\big|_{x_k = c_0} = \frac{\eta' + \sum_{i \neq k} \rho_i \alpha^{x_i}(m_i + \delta x_i)}{\gamma' + \sum_{i \neq k} \rho_i \alpha^{x_i}}, $$
   and that the new parameters are valid: $\gamma' > 0$ (since $\gamma>0$ and $\rho_k\alpha^{c_0}>0$), $\rho_i>0$ for $i\neq k$, $\alpha>0$. Hence the restriction of $\phi$ is a one-head atom on $\{0,1\}^{n-1}$.

2. **Restricting a representation.** Let $H = H^{*}(f)$, witnessed by atoms $\phi_1,\dots,\phi_H$ and constant $c$ with $f(x) = 1 \iff c + \sum_h \phi_h(x) > 0$. Fixing $x_k = c_0$ and applying Step 1 to each $\phi_h$ gives atoms $\phi_h'$ on $\{0,1\}^{n-1}$ and the same constant $c$ with $f|_{x_k=c_0}(y) = 1 \iff c + \sum_h \phi_h'(y) > 0$ for all $y \in \{0,1\}^{n-1}$. By the normal form, $H^{*}(f|_{x_k=c_0}) \leq H = H^{*}(f)$.

3. **Iterate and conclude the consequences.** Fixing several coordinates one at a time gives the general restriction statement. The lower-bound consequence is the contrapositive: if a restriction equals $g$ (up to relabeling coordinates, which does not change head complexity), then $H^{*}(g) \leq H^{*}(f)$. Apply with $g = \mathrm{XOR}_m$ and with $g = \mathrm{XOR}_2$ for the checkerboard case.

Give a complete, rigorous proof.
