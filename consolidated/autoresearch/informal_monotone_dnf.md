# Problem: A monotone-term DNF needs at most one head per term

## Background and definitions (self-contained)

Fix an integer $n \geq 1$ and work on the Boolean cube $\{0,1\}^n$. For $\alpha > 0$ and $b \in \{0,1\}$, $\alpha^b$ is the ordinary power ($\alpha^0 = 1$, $\alpha^1 = \alpha$).

A **one-head atom** is a function $\phi : \{0,1\}^n \to \mathbb{R}$ of the form

$$
\phi(x) = \frac{\eta + \sum_{i=1}^{n} \rho_i \alpha^{x_i}(m_i + \delta x_i)}{\gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i}},
\qquad \gamma>0,\ \rho_i>0,\ \alpha>0,\ \eta,\delta,m_i\in\mathbb{R}.
$$

**Established normal form (you may use this as the definition of head complexity).** It is a proved result for this project's model (the linear-fractional normal form) that for any $H \geq 0$,

$$
H^{*}(f) \leq H
\quad\Longleftrightarrow\quad
\exists\ \text{one-head atoms } \phi_1,\dots,\phi_H \text{ and a constant } c\in\mathbb{R}
\text{ with } \Big(f(x)=1 \iff c + \sum_{h=1}^{H}\phi_h(x) > 0\Big)\ \forall x\in\{0,1\}^n.
$$

So to prove $H^{*}(f) \leq H$ it suffices to exhibit $H$ one-head atoms and a constant whose thresholded sum equals $f$ on the cube.

**Monotone terms and DNF.** A **literal** is $x_i$ (a positive literal) or $\overline{x_i} = 1 - x_i$ (a negative literal). A **monotone term** is a conjunction of literals that are either all positive or all negative; concretely it is the indicator of a subcube of one of the two forms

$$
T(x) = \prod_{i\in S} x_i \quad(\text{a positive term}),
\qquad\text{or}\qquad
T(x) = \prod_{i\in S} (1-x_i) \quad(\text{a negative term}),
$$

for some nonempty $S \subseteq \{1,\dots,n\}$, with $T(x) \in \{0,1\}$ and $T(x) = 1$ exactly when the term is satisfied. We say $f : \{0,1\}^n \to \{0,1\}$ has a **monotone-term DNF with $s$ terms** if there are monotone terms $T_1,\dots,T_s$ with

$$
f(x) = 1 \iff \exists\, r\in\{1,\dots,s\}:\ T_r(x) = 1.
$$

## Claim to prove

If $f$ has a monotone-term DNF with $s$ terms (each term monotone, as above), then

$$
H^{*}(f) \leq s.
$$

As a corollary, every monotone Boolean function $f$ satisfies $H^{*}(f) \leq (\text{number of prime implicants of } f)$, since a monotone function is the OR of its prime implicants, each a positive monotone term.

## Guidance toward the construction (prove every step rigorously)

For each term $T_r$ define a nonnegative "violation count" that is an affine function with all slopes of one strict sign, by spreading a tiny weight $\epsilon > 0$ onto the coordinates not appearing in the term:

- If $T_r = \prod_{i \in S_r} x_i$ (positive term), set weights $w^{(r)}_i = 1$ for $i \in S_r$ and $w^{(r)}_i = \epsilon$ for $i \notin S_r$, and define
  $$ v_r(x) = \sum_{i=1}^n w^{(r)}_i (1 - x_i). $$
- If $T_r = \prod_{i \in S_r} (1 - x_i)$ (negative term), set the same weights and define
  $$ v_r(x) = \sum_{i=1}^n w^{(r)}_i\, x_i. $$

Establish the following facts.

1. **$v_r \geq 0$ on the cube, and $v_r = 0$ exactly on the satisfied subcube up to the $\epsilon$ slack.** Show: if $T_r(x) = 1$ then $0 \leq v_r(x) \leq \epsilon n$; if $T_r(x) = 0$ then $v_r(x) \geq 1$ (some in-term literal is violated, contributing weight $1$). Use $0 < \epsilon$.

2. **The bump is a one-head atom.** Fix $\lambda > 0$ and set $b_r(x) = \dfrac{1}{1 + \lambda v_r(x)}$. Show $b_r$ is a one-head atom by exhibiting explicit parameters. (For a negative term: $v_r(x) = \sum_i w^{(r)}_i x_i$, choose $\alpha > 1$, $\rho_i = \lambda w^{(r)}_i/(\alpha - 1) > 0$, and $\gamma = 1 - \sum_i \rho_i$, which is $> 0$ for $\alpha$ large; then the denominator equals $1 + \lambda v_r$ and, taking $\delta = 0$, $m_i = 0$, $\eta = 1$, the numerator equals $1$. For a positive term: $v_r(x) = (\sum_i w^{(r)}_i) - \sum_i w^{(r)}_i x_i$, choose $\alpha \in (0,1)$, $\rho_i = \lambda w^{(r)}_i/(1 - \alpha) > 0$, and check $\gamma = (1 + \lambda \sum_i w^{(r)}_i) - \sum_i \rho_i > 0$ for $\alpha$ near $0$; numerator $1$ as before.) Verify in each case that the constructed denominator equals $1 + \lambda v_r(x)$ for all $x$ and the numerator equals $1$.

3. **Separation by choosing the constants.** Take $\lambda = 2s$ and then $\epsilon \in \big(0, \tfrac{1}{2sn}\big)$ so that $\lambda \epsilon n < 1$. Show:
   - if some term is satisfied at $x$, then that $b_r(x) \geq \dfrac{1}{1 + \lambda \epsilon n} > \tfrac12$, hence $\sum_{r=1}^s b_r(x) > \tfrac12$ (all $b_r \geq 0$);
   - if no term is satisfied at $x$, then every $b_r(x) \leq \dfrac{1}{1 + \lambda} = \dfrac{1}{1 + 2s}$, hence $\sum_{r=1}^s b_r(x) \leq \dfrac{s}{1 + 2s} < \tfrac12$.

4. **Conclude.** With $c = -\tfrac12$, the $s$ atoms $b_1,\dots,b_s$ satisfy $f(x) = 1 \iff c + \sum_{r=1}^s b_r(x) > 0$ for every $x$. By the established normal form, $H^{*}(f) \leq s$. State the monotone-function corollary.

Give a complete, rigorous proof.
