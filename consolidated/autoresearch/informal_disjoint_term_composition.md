# Problem: ORing a disjoint monotone term costs at most one head

## Background and definitions (self-contained)

A **monotone term** on a variable set $A$ is $T(z) = \bigwedge_{i\in A} z_i = \prod_{i\in A} z_i$ (the AND of those variables). A **one-head atom** (L10/L13) is a function $\phi(x) = N(x)/D(x)$ where $N, D$ are affine, $D > 0$ on the cube, and $D$'s slopes are all of one sign (admissible); equivalently $\phi$ arises as $\eta + \sum_i \rho_i\alpha^{x_i}(\ldots)$ over $\gamma + \sum_i\rho_i\alpha^{x_i}$ with $\gamma,\rho_i,\alpha > 0$. $H^{*}(g) \leq H$ iff $g(x) = 1 \iff c + \sum_{h=1}^H \phi_h(x) > 0$ for some constant $c$ and admissible atoms $\phi_1,\dots,\phi_H$ (L10).

Let $f$ be a Boolean function on a variable set $Z$, and let $T(w) = \bigwedge_{i\in A} w_i$ be a monotone term on a variable set $A$ **disjoint** from $Z$. Define $f \vee T$ on $Z \cup A$ by $(f\vee T)(z, w) = \max(f(z), T(w))$.

## Claim to prove

$$
H^{*}(f \vee T) \leq H^{*}(f) + 1 .
$$

## Guidance (prove every step rigorously)

Let $H = H^{*}(f)$, so $f(z) = 1 \iff V(z) > 0$ where $V(z) = c + \sum_{h=1}^H \phi_h(z)$, the $\phi_h$ admissible atoms on $Z$. Since the cube is finite and the representation is strict, set
$$
m = \min\lbrace V(z) : f(z)=1\rbrace > 0, \quad \mu = \min\lbrace -V(z) : f(z)=0\rbrace > 0, \quad B = \max_z |V(z)| < \infty .
$$

**Step 1 (a one-sided atom that detects $T$).** Pick $\alpha \in (0,1)$, $\gamma > 0$, $\rho > 0$, and a constant $M > 0$, and define on the $A$-variables
$$
\psi(w) = \frac{M}{\,\gamma + \rho\sum_{i\in A}\alpha^{w_i}\,} =: \frac{M}{D(w)} .
$$
Verify $\psi$ is an admissible atom: the denominator $D(w) = \gamma + \rho\sum_{i\in A}\alpha^{w_i}$ expands (via $\alpha^{w_i} = 1 + (\alpha-1)w_i$) to the affine form $\big(\gamma + \rho|A|\big) + \rho(\alpha-1)\sum_{i\in A} w_i$, which is positive on the cube ($\gamma,\rho>0$, $\alpha^{w_i}>0$) and has all slopes $\rho(\alpha-1) < 0$ (one-sided, since $\alpha<1$); $N = M$ is affine. So $\psi = N/D$ is an admissible atom, and $\psi(w) > 0$ everywhere.

**Step 2 (its values on/off $T$).** $D$ is minimized when all $w_i=1$ (each $\alpha^{1}=\alpha$ is the smallest value of $\alpha^{w_i}$ since $\alpha<1$): $D(\mathbf 1) = \gamma + \rho|A|\alpha$, so $\psi(T{=}1) = M/(\gamma + \rho|A|\alpha)$. When $T(w)=0$, at least one $w_i=0$ contributing $\alpha^0 = 1$, so $D(w) \geq \gamma + \rho\cdot 1 = \gamma + \rho$, giving $\psi(w) \leq M/(\gamma+\rho)$ on $T=0$. *(justification: a single $w_i=0$ term contributes $1$; the rest contribute $\geq 0$.)*

**Step 3 (choose parameters).** Fix $\gamma = 1$. Choose $\rho$ large enough that $M/(1+\rho) < \mu$ for the $M$ to be chosen — precisely, first pick $\rho > 0$, then we will pick $M < \mu(1+\rho)$, which forces $\psi(T{=}0) \leq M/(1+\rho) < \mu$. We also need $\psi(T{=}1) = M/(1 + \rho|A|\alpha) > B$. Choose $\alpha \in (0,1)$ small enough that $\rho|A|\alpha < 1$ (possible for any fixed $\rho$), so $1 + \rho|A|\alpha < 2$ and $\psi(T{=}1) > M/2$. Now choose $M$ with $2B < M < \mu(1+\rho)$; such $M$ exists once $\rho$ is large enough that $\mu(1+\rho) > 2B$ (i.e. $\rho > 2B/\mu - 1$). With this $M$: $\psi(T{=}1) > M/2 > B$ and $\psi(T{=}0) \leq M/(1+\rho) < \mu$. *(Summary of order of choices: $\gamma=1$; $\rho > 2B/\mu - 1$; $M \in (2B,\ \mu(1+\rho))$; $\alpha \in (0,\ 1/(\rho|A|))$.)*

**Step 4 (the combined representation).** Define $S(z,w) = V(z) + \psi(w) = c + \sum_{h=1}^H \phi_h(z) + \psi(w)$, a constant plus $H+1$ admissible atoms. Check $\mathrm{sign}(S) = f\vee T$ at every point:
- If $f(z)=1$: $V(z) \geq m > 0$ and $\psi(w) > 0$, so $S \geq m > 0$; and $(f\vee T)(z,w)=1$. *(correct sign)*
- If $f(z)=0$ and $T(w)=1$: $V(z) \geq -B$ and $\psi(w) = \psi(T{=}1) > B$, so $S > -B + B = 0$; and $(f\vee T)=1$. *(correct)*
- If $f(z)=0$ and $T(w)=0$: $V(z) \leq -\mu$ and $0 < \psi(w) \leq \psi(T{=}0) < \mu$, so $S < -\mu + \mu = 0$; and $(f\vee T)=0$. *(correct)*

Thus $f\vee T = 1 \iff S > 0$ with $S = c + \sum_{h=1}^{H+1}(\text{admissible atoms})$, so $H^{*}(f\vee T) \leq H+1 = H^{*}(f)+1$. $\blacksquare$

## Consequence (state and prove)

**Corollary.** $H^{*}(\mathrm{INT}_n) \leq n-1$ for all $n \geq 3$, where $\mathrm{INT}_n(x,y) = \bigvee_{i=1}^n(x_i\wedge y_i)$.

*Proof.* $\mathrm{INT}_{k+1} = \mathrm{INT}_k(\text{pairs }1..k) \vee T_{k+1}$ with $T_{k+1} = x_{k+1}\wedge y_{k+1}$ a monotone term on the fresh pair, disjoint from the first $k$ pairs. By the theorem, $H^{*}(\mathrm{INT}_{k+1}) \leq H^{*}(\mathrm{INT}_k) + 1$. Starting from $H^{*}(\mathrm{INT}_3) = 2$ (L39) and inducting, $H^{*}(\mathrm{INT}_n) \leq 2 + (n-3) = n-1$ for $n\geq 3$. $\square$

## Pitfalls

- The new term is summed as an **atom** $\psi$ into $c + \sum\phi_h + \psi$ (the genuine head-complexity form $c + \sum N_h/D_h$), NOT as a product — so the count is genuinely $H+1$ heads. (This is unlike a degree-2 "sum of products", which is an order-2 tangent form only because $K=2$.)
- The construction needs $\psi \geq 0$ everywhere (so it never hurts $f=1$ points), $\psi(T{=}1) > B$ (to flip $f=0,T=1$ points positive), and $\psi(T{=}0) < \mu$ (to keep $f=0,T=0$ points negative). Verify all three from the parameter choice.
- This works because $T$ is a **monotone term**: the single admissible atom $\psi$ can be made $\approx 0$ off $T$ and large on $T$. It does **not** extend to $f\vee g$ for general $g$ (a general $g$'s value is bounded-negative off its support, not $\approx 0$, causing interference).
- Admissibility of $\psi$: one shared $\alpha < 1$ gives all denominator slopes the same (negative) sign — one-sided — and $D>0$; state both.
