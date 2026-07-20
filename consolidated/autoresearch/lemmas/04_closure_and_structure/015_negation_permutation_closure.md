# Negation and Permutation Closure

## Statement

Let $f : \lbrace 0,1\rbrace ^n \to \lbrace 0,1\rbrace $.

**(1) Output negation.** For $\overline{f} := 1 - f$,

$$
H^{*}(\overline{f}) = H^{*}(f).
$$

**(2) Input permutation.** For a permutation $\pi$ of $\lbrace 1,\dots,n\rbrace $ and $f^{\pi}(x) := f(x_{\pi(1)},\dots,x_{\pi(n)})$,

$$
H^{*}(f^{\pi}) = H^{*}(f).
$$

> Head complexity is an invariant of a Boolean function up to complementation of the output and relabeling of the inputs. (Invariance under negating a *single* input coordinate is a separate, open question: the shared bit direction $e_1 - e_0$ breaks the naive same-atom argument (the monotone bias, [013_atom_dictionary.md](../01_foundations_and_normal_form/013_atom_dictionary.md)), but $H^{*}$ is in fact single-bit-negation invariant for $n \leq 4$ and would be invariant in general iff positivity is free, $\mathrm{tChow}_{\pm} = H^{*}$.)

## Proof

Throughout we use the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md): $H^{*}(g)$ is the least $H$ for which there are one-head atoms $\phi_1,\dots,\phi_H$ and $c \in \mathbb{R}$ with $g(x) = 1 \iff c + \sum_h \phi_h(x) > 0$. Every atom denominator $\gamma + \sum_i \rho_i \alpha^{x_i}$ is positive on the cube.

### Part 1. Output negation

**Negating an atom gives an atom.** If $\phi$ has parameters $\gamma,\rho_i,\alpha,\eta,\delta,m_i$, then keeping $\gamma,\rho_i,\alpha$ and replacing $\eta,\delta,m_i$ by $-\eta,-\delta,-m_i$ negates the numerator while fixing the (positive) denominator, so the result is the one-head atom $-\phi$.

**Main argument.** Let $H = H^{*}(f)$ with atoms $\phi_1,\dots,\phi_H$, constant $c$, and $S(x) := c + \sum_h \phi_h(x)$.

If $f \equiv 0$ then $\overline f \equiv 1$; both are computed with $0$ heads (constant $c = -1$ and $c = 1$ respectively), so $H^{*}(\overline f) = 0 = H^{*}(f)$.

Otherwise $A := f^{-1}(1)$ is nonempty and finite, with $S(x) > 0$ on $A$. Let $s_{\min} := \min_{x \in A} S(x) > 0$ and pick $\mu$ with $0 < \mu < s_{\min}$. Set $S'(x) := (\mu - c) + \sum_h (-\phi_h)(x) = \mu - S(x)$, a constant plus the $H$ atoms $-\phi_h$.

- If $f(x) = 1$: $x \in A$ so $S(x) \geq s_{\min} > \mu$, hence $S'(x) = \mu - S(x) < 0$; and $\overline f(x) = 0$. Consistent.
- If $f(x) = 0$: the equivalence for $f$ gives $S(x) \leq 0$, hence $S'(x) = \mu - S(x) \geq \mu > 0$; and $\overline f(x) = 1$. Consistent.

So $\overline f(x) = 1 \iff S'(x) > 0$, witnessing $H^{*}(\overline f) \leq H$. Applying the same to $\overline f$ (whose complement is $f$) gives $H^{*}(f) \leq H^{*}(\overline f)$, hence equality. $\square$

### Part 2. Input permutation

**Permuting inputs preserves atoms.** Let $\phi$ have parameters $\gamma,\rho_i,\alpha,\eta,\delta,m_i$. With $\rho'_i := \rho_{\pi^{-1}(i)}$, $m'_i := m_{\pi^{-1}(i)}$ (still positive resp. real) and the same $\gamma,\alpha,\eta,\delta$, reindexing the sums by $j = \pi(i)$ gives

$$
\gamma + \sum_i \rho_i \alpha^{x_{\pi(i)}} = \gamma + \sum_j \rho'_j \alpha^{x_j},
\qquad
\eta + \sum_i \rho_i \alpha^{x_{\pi(i)}}(m_i + \delta x_{\pi(i)}) = \eta + \sum_j \rho'_j \alpha^{x_j}(m'_j + \delta x_j),
$$

so $x \mapsto \phi(x_{\pi(1)},\dots,x_{\pi(n)})$ is a one-head atom.

**Main argument.** Let $H = H^{*}(f)$ with atoms $\phi_h$ and constant $c$. For any $x$, writing $y = (x_{\pi(1)},\dots,x_{\pi(n)})$, we have $f^{\pi}(x) = f(y)$ and

$$
f^{\pi}(x) = 1 \iff f(y) = 1 \iff c + \sum_h \phi_h(y) > 0 \iff c + \sum_h \phi_h(x_{\pi(1)},\dots,x_{\pi(n)}) > 0 .
$$

By the lemma each summand is a one-head atom, so $H^{*}(f^{\pi}) \leq H$. Applying this to $f^{\pi}$ with $\pi^{-1}$ (and $(f^{\pi})^{\pi^{-1}} = f$) gives $H^{*}(f) \leq H^{*}(f^{\pi})$, hence equality. $\blacksquare$

## Consequence

These closures let later arguments reduce to a canonical representative: any single output negation is free, and coordinates may be relabeled at will. Together with restriction monotonicity [017_restriction_monotonicity.md](../03_lower_bounds/017_restriction_monotonicity.md), they form the basic structural toolkit for transporting head-complexity bounds between related functions.
