# Problem: A sign-change upper bound for functions of one positive weighted sum

## Background and definitions (self-contained)

Fix $n \geq 1$, work on $\{0,1\}^n$. For $\alpha>0$, $b\in\{0,1\}$: $\alpha^0=1$, $\alpha^1=\alpha$.

A **one-head atom** is $\phi(x)=\dfrac{\eta+\sum_i\rho_i\alpha^{x_i}(m_i+\delta x_i)}{\gamma+\sum_i\rho_i\alpha^{x_i}}$, $\gamma>0,\rho_i>0,\alpha>0,\ \eta,\delta,m_i\in\mathbb{R}$.

**Established normal form (use as the definition of head complexity).** $H^{*}(f)\leq H$ iff there exist one-head atoms $\phi_1,\dots,\phi_H$ and $c\in\mathbb{R}$ with $f(x)=1 \iff c+\sum_{h=1}^H\phi_h(x)>0$ for all $x$.

**Established kernel fact (you may cite, or reprove in one line).** For any $\beta>0$ and any $A\in\mathbb{R}$, with $t(x)=\sum_i w_i x_i$, $w_i>0$, the function $x\mapsto \dfrac{A}{\beta+t(x)}$ is a one-head atom. (Its denominator $\beta+\sum_i w_i x_i$ is affine, positive on the cube, with all slopes $w_i>0$; choose $\alpha>1$, $\rho_i=w_i/(\alpha-1)$, $\gamma=\beta-\sum_i\rho_i>0$ for $\alpha$ large, and numerator parameters $\eta=A,\ m_i=\delta=0$.)

Let $t(x)=\sum_{i=1}^n w_i x_i$ with all $w_i>0$, and let $\mathrm{Im}(t)=\{\tau_1<\tau_2<\dots<\tau_M\}$ be its $M$ distinct values. Let $F:\mathrm{Im}(t)\to\{0,1\}$ and define $f(x)=F(t(x))$. Let

$$
C(F) = \#\{\, k\in\{1,\dots,M-1\} : F(\tau_k)\neq F(\tau_{k+1}) \,\}
$$

be the number of sign changes of $F$ along the increasing value sequence.

## Claim to prove

$$
H^{*}(f) \leq C(F).
$$

(This generalizes the symmetric sign-change result from equal weights to arbitrary positive weights, and strengthens the weighted-sum bound $H^{*}\leq M-1$ since $C(F)\leq M-1$. When the $w_i$ are unequal, $f=F(t)$ is in general a nonsymmetric function.)

## Guidance (prove every step rigorously)

Write $C=C(F)$. If $C=0$ then $F$ is constant on $\mathrm{Im}(t)$, so $f$ is constant and $H^{*}(f)=0$; assume $C\geq 1$.

1. **A univariate sign-representer of degree $C$.** Let $k_1<\dots<k_C$ be the indices where $F$ changes ($F(\tau_{k_r})\neq F(\tau_{k_r+1})$). Choose real cut points $\mu_r$ with $\tau_{k_r}<\mu_r<\tau_{k_r+1}$, and set
   $$ q(s) = \epsilon\prod_{r=1}^C (s-\mu_r), \qquad \epsilon\in\{+1,-1\}. $$
   Show that $q$ has degree $C$, that $q(\tau_k)\neq 0$ for all $k$ (no $\tau_k$ equals a $\mu_r$), and that as $s$ increases past each $\mu_r$, $q$ changes sign; since the $\mu_r$ are exactly the gaps where $F$ flips, $q(\tau_k)$ and $q(\tau_{k+1})$ have the same sign iff $F(\tau_k)=F(\tau_{k+1})$. Hence, choosing $\epsilon$ to fix the first interval, $\mathrm{sgn}\,q(\tau_k)=+1 \iff F(\tau_k)=1$ for every $k$. Therefore $f(x)=1 \iff q(t(x))>0$.

2. **Choose $C$ admissible denominators.** Pick $C$ distinct reals $\beta_1,\dots,\beta_C>0$. Each $\beta_r+t(x)>0$ on the cube ($\beta_r>0$, $t\geq 0$), and the poles $-\beta_r$ are distinct and lie outside $[\,0,\sum_i w_i\,]\supseteq\mathrm{Im}(t)$.

3. **Partial fractions.** The rational function $q(s)/\prod_{r=1}^C(\beta_r+s)$ has numerator degree $C$ equal to denominator degree $C$ with $C$ distinct simple poles, so it admits a partial-fraction decomposition
   $$ \frac{q(s)}{\prod_{r=1}^C(\beta_r+s)} = \theta + \sum_{r=1}^C \frac{A_r}{\beta_r+s}, $$
   with a real constant $\theta$ (the ratio of leading coefficients) and real residues $A_r = q(-\beta_r)\big/\prod_{g\neq r}(\beta_g-\beta_r)$. Verify this identity (clear denominators and match the degree-$C$ polynomials, or cite the standard simple-pole partial-fraction theorem and compute the residues).

4. **Clear the positive denominator.** Put $\Pi(s)=\prod_{r=1}^C(\beta_r+s)$, which is $>0$ for $s\in\mathrm{Im}(t)$. From Step 3, $q(s) = \big(\theta+\sum_r A_r/(\beta_r+s)\big)\Pi(s)$, and since $\Pi(t(x))>0$,
   $$ q(t(x))>0 \iff \theta + \sum_{r=1}^C \frac{A_r}{\beta_r+t(x)} > 0. $$

5. **Read off atoms.** By the kernel fact, each $x\mapsto A_r/(\beta_r+t(x))$ is a one-head atom. Combining Steps 1 and 4,
   $$ f(x)=1 \iff q(t(x))>0 \iff \theta + \sum_{r=1}^C \frac{A_r}{\beta_r+t(x)} > 0 , $$
   a constant plus $C$ one-head atoms. By the normal form, $H^{*}(f)\leq C=C(F)$.

Note in a closing remark that a matching lower bound (hence the exact value $H^{*}=C(F)$) holds for equal weights by the symmetric theory, but for unequal weights the lower bound is not established here (the threshold degree of a function of one linear form need not equal its sign-change count when the weights are unequal).

Give a complete, rigorous proof.
