# Junta Invariance

## Statement

Let $g : \lbrace 0,1\rbrace^k \to \lbrace 0,1\rbrace$ and let $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$ ($n \geq k$) be the padding $f(x) = g(x_1,\dots,x_k)$, which ignores $x_{k+1},\dots,x_n$. Then

$$
H^{*}(f) = H^{*}(g).
$$

> Head complexity depends only on the relevant variables: padding with irrelevant coordinates changes nothing. Together with negation/permutation closure [015_negation_permutation_closure.md](015_negation_permutation_closure.md) and restriction monotonicity [017_restriction_monotonicity.md](../03_lower_bounds/017_restriction_monotonicity.md), this lets arguments reduce to the relevant-variable core.

## Proof

We use the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md).

### Lower bound

Fixing $x_{k+1} = \dots = x_n = 0$ in $f$ yields exactly $g$ on $\lbrace 0,1\rbrace^k$. By iterated restriction monotonicity [017_restriction_monotonicity.md](../03_lower_bounds/017_restriction_monotonicity.md), $H^{*}(g) \leq H^{*}(f)$.

### Upper bound

Let $H = H^{*}(g)$, witnessed by atoms $\phi_r = N_r/D_r$ on $\lbrace 0,1\rbrace^k$ (parameters $\gamma_r,\alpha_r,\lbrace\rho_{r,i}, m_{r,i}\rbrace_{i\leq k},\eta_r,\delta_r$) and constant $c$, so $g(y) = 1 \iff c + \sum_r \phi_r(y) > 0$. If $H = 0$, $g$ and hence $f$ are the same constant, so $H^{*}(f) = 0$. Assume $H \geq 1$.

**Pad each atom at weight $\epsilon$.** For $\epsilon > 0$, define $\phi_r^\epsilon$ on $\lbrace 0,1\rbrace^n$ keeping the $i \leq k$ parameters and setting $\rho_{r,i} = \epsilon$, $m_{r,i} = 0$ for $i > k$. This is a valid one-head atom (all $\rho > 0$, $\gamma_r > 0$, $\alpha_r > 0$). Writing $y = (x_1,\dots,x_k)$,

$$
\phi_r^\epsilon(x) = \frac{N_r(y) + \epsilon F_r(x)}{D_r(y) + \epsilon E_r(x)},
\quad
E_r(x) = \sum_{i>k}\alpha_r^{x_i},
\quad
F_r(x) = \delta_r \sum_{i>k} x_i \alpha_r^{x_i}.
$$

**Uniform convergence.** With $d_r = \min_y D_r(y) > 0$, $M_r = \max_y |N_r(y)|$, $L_r = \max_y D_r(y)$, $A_r = \max(1,\alpha_r)$, $t = n-k$: $0 \leq E_r(x) \leq tA_r$ and $|F_r(x)| \leq |\delta_r| tA_r$, so

$$
|\phi_r^\epsilon(x) - \phi_r(y)| \leq \epsilon\,\frac{L_r|\delta_r| tA_r + M_r tA_r}{d_r^2} \xrightarrow{\epsilon \to 0^+} 0
$$

uniformly over the finite cube. (The $\delta_r \neq 0$ contribution $\epsilon F_r$ is kept and bounded; it does not vanish but is $O(\epsilon)$.)

**Margin.** Let $S(y) = c + \sum_r \phi_r(y)$. After a tiny shift of $c$ (if some $S(y) = 0$, replace $c$ by $c - p/2$ with $p = \min\lbrace S(y) : S(y) > 0\rbrace$), we have $g(y) = 1 \iff S(y) > 0$ with $S$ nowhere zero; set $\mu = \min_y |S(y)| > 0$. With $S^\epsilon(x) = c + \sum_r \phi_r^\epsilon(x)$, uniform convergence gives $\sup_x |S^\epsilon(x) - S(x_1,\dots,x_k)| \to 0$, so for $\epsilon$ small, $|S^\epsilon - S| < \mu$ everywhere, whence $S^\epsilon(x)$ has the same sign as $S(x_1,\dots,x_k)$. Thus $f(x) = 1 \iff S^\epsilon(x) > 0$, a constant plus $H$ atoms on $\lbrace 0,1\rbrace^n$. By the normal form, $H^{*}(f) \leq H = H^{*}(g)$. $\blacksquare$

## Consequence

Combined with restriction (L17), head complexity is determined by a function's action on its relevant variables; e.g. an $n$-variable padding of $\mathrm{XOR}_k$ has $H^{*} = k$. This justifies stating upper and lower bounds in terms of relevant-variable structure only.
