# Sign-Change Upper Bound for Functions of One Positive Weighted Sum

## Statement

Let $t(x) = \sum_{i=1}^n w_i x_i$ with all $w_i > 0$, and $\mathrm{Im}(t) = \lbrace \tau_1 < \dots < \tau_M\rbrace$. Let $F : \mathrm{Im}(t) \to \lbrace 0,1\rbrace$, $f(x) = F(t(x))$, and let

$$
C(F) = \#\lbrace k \in \lbrace 1,\dots,M-1\rbrace : F(\tau_k) \neq F(\tau_{k+1})\rbrace
$$

be the number of sign changes of $F$ along the increasing value sequence. Then

$$
H^{*}(f) \leq C(F).
$$

> Generalizes the symmetric sign-change result [012_symmetric_sign_changes.md](../01_foundations_and_normal_form/012_symmetric_sign_changes.md) from equal weights to arbitrary positive weights (and strengthens the weighted-sum bound $H^{*} \leq M-1$ since $C(F) \leq M-1$). When the $w_i$ are unequal, $f = F(t)$ is in general nonsymmetric.

## Proof

Assume $C := C(F) \geq 1$ (else $f$ is constant and $H^{*}=0$). We use the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md) and the fact that $A/(\beta + t(x))$ is a one-head atom for $\beta > 0$ (denominator $\beta + \sum_i w_i x_i$ is affine, positive on the cube, slopes $w_i > 0$ all one sign; numerator the constant $A$).

**A degree-$C$ univariate sign-representer.** Let $k_1 < \dots < k_C$ be the indices where $F$ flips, pick cut points $\mu_r \in (\tau_{k_r}, \tau_{k_r+1})$, and set $q(s) = \epsilon\prod_{r=1}^C(s - \mu_r)$. Then $q$ has degree $C$, $q(\tau_k) \neq 0$, and $q$ changes sign exactly across each $\mu_r$, i.e. exactly at the flips of $F$; choosing $\epsilon = \pm 1$ to align the first interval gives $\mathrm{sgn}\,q(\tau_k) = +1 \iff F(\tau_k) = 1$. Hence $f(x) = 1 \iff q(t(x)) > 0$.

**Partial fractions into $C$ atoms.** Choose distinct $\beta_1,\dots,\beta_C > 0$ (so $\beta_r + t(x) > 0$ on the cube, distinct poles $-\beta_r$ outside $\mathrm{Im}(t)$). Since $q$ has degree $C$ and $\prod_r(\beta_r + s)$ has degree $C$ with simple poles,

$$
\frac{q(s)}{\prod_{r=1}^C(\beta_r + s)} = \theta + \sum_{r=1}^C \frac{A_r}{\beta_r + s},
\qquad \theta,\,A_r = \frac{q(-\beta_r)}{\prod_{g\neq r}(\beta_g - \beta_r)} \in \mathbb{R}.
$$

Since $\Pi(s) := \prod_r(\beta_r + s) > 0$ on $\mathrm{Im}(t)$, $q(t(x)) > 0 \iff \theta + \sum_r A_r/(\beta_r + t(x)) > 0$. Each $A_r/(\beta_r + t(x))$ is a one-head atom, so

$$
f(x) = 1 \iff \theta + \sum_{r=1}^C \frac{A_r}{\beta_r + t(x)} > 0
$$

is a constant plus $C$ atoms. By the normal form, $H^{*}(f) \leq C = C(F)$. $\blacksquare$

## Remark on the lower bound

For equal weights the matching lower bound holds (symmetric theory, L12), giving the exact $H^{*} = C(F)$. For **unequal** weights only the upper bound holds: the exact value can be far smaller. With superincreasing weights $t(x) = \sum_i 2^{i-1}x_i$, $t$ injects the cube into $\lbrace 0,\dots,2^n-1\rbrace$, so e.g. $F(k) = (-1)^k$ gives $f(x) = (-1)^{x_1}$, a dictator with $H^{*}(f) = 1$ but $C(F) = 2^n - 1$. Thus "factors through one positive weighted sum" is vacuous for generic weights, and $C(F)$ is then an artifact of the encoding order, not intrinsic complexity. The right intuitive invariant is the **minimized** alternation count $A_{+}(f)$ [026_alternation_upper_bound.md](026_alternation_upper_bound.md).
