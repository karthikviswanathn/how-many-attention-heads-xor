# Full-Input Complement Invariance

## Statement

For $x \in \lbrace 0,1\rbrace^n$ write $\bar{x} = \mathbf{1} - x$, and let $f^{c}(x) := f(\bar{x})$ be the **input-complement** of $f$. Then

$$
H^{*}(f^{c}) = H^{*}(f).
$$

> Complementing **all** inputs simultaneously is free: the model has a global $0 \leftrightarrow 1$ symmetry. This works because $x \mapsto \bar x$ replaces the shared base $\alpha$ by $1/\alpha$ uniformly across every coordinate. A **single**-bit negation is more delicate: it flips one slope of each denominator, so the *naive same-atom argument breaks* (an admissible denominator becomes mixed-slope). This is a real effect of the monotone bias, but it does **not** show $H^{*}$ changes. In fact $\mathrm{tChow}_{\pm}$ is single-bit-negation invariant (arbitrary affine factors are preserved), and $H^{*} = \deg_{\pm}$ (also negation invariant) for all $n \leq 4$, so $H^{*}$ **is** single-bit-negation invariant there. Whether it is in general is **open**, and would follow from $\mathrm{tChow}_{\pm} = H^{*}$ (the F4 question, [030_tchow_level1.md](../01_foundations_and_normal_form/030_tchow_level1.md)).

## Proof

We use the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md).

**The input-complement of an atom is an atom.** Let $\phi$ be a one-head atom with parameters $\gamma,\alpha,\lbrace\rho_i\rbrace,\eta,\delta,\lbrace m_i\rbrace$. Using $\alpha^{1-x_i} = \alpha\,(1/\alpha)^{x_i}$ (valid for $x_i \in \lbrace 0,1\rbrace$) and $m_i + \delta(1-x_i) = (m_i + \delta) - \delta x_i$, set

$$
\alpha' = 1/\alpha,\quad \rho_i' = \rho_i\alpha,\quad m_i' = m_i + \delta,\quad \delta' = -\delta,\quad \gamma' = \gamma,\quad \eta' = \eta,
$$

all valid ($\alpha' > 0$, $\rho_i' > 0$, $\gamma' > 0$). Then

$$
\gamma + \sum_i \rho_i\alpha^{1-x_i} = \gamma + \sum_i \rho_i'\alpha'^{x_i},
\qquad
\eta + \sum_i \rho_i\alpha^{1-x_i}(m_i + \delta(1-x_i)) = \eta + \sum_i \rho_i'\alpha'^{x_i}(m_i' + \delta' x_i),
$$

so $\phi(\bar x) = \dfrac{\eta + \sum_i \rho_i'\alpha'^{x_i}(m_i' + \delta' x_i)}{\gamma + \sum_i \rho_i'\alpha'^{x_i}}$ is a one-head atom in $x$.

**Main argument.** Let $H = H^{*}(f)$, witnessed by atoms $\phi_h$ and constant $c$ with $f(y) = 1 \iff c + \sum_h \phi_h(y) > 0$. For any $x$, with $y = \bar x$, $f^{c}(x) = f(\bar x)$ and $f^{c}(x) = 1 \iff c + \sum_h \phi_h(\bar x) > 0$, where each $x \mapsto \phi_h(\bar x)$ is a one-head atom. So $H^{*}(f^{c}) \leq H = H^{*}(f)$. Applying this to $f^{c}$ (using $(f^{c})^{c} = f$) gives the reverse inequality, hence equality. $\blacksquare$

## Consequence

The structural toolkit (closure under negation/permutation L15, junta invariance L21, restriction L17) now also includes the global input complement. So head-complexity questions may be canonicalized up to output negation, input permutation, and simultaneous input complement. Single-bit-negation invariance is a separate, open question (it holds for $n \leq 4$ and would hold in general iff positivity is free); the monotone bias only obstructs the naive same-atom proof, not necessarily the invariance itself.
