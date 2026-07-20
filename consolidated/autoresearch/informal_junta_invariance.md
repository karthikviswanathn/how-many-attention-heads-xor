# Problem: Head complexity ignores irrelevant variables (junta invariance)

## Background and definitions (self-contained)

Fix integers $n \geq k \geq 1$, work on $\{0,1\}^n$ and $\{0,1\}^k$. For $\alpha>0$, $b\in\{0,1\}$: $\alpha^0=1$, $\alpha^1=\alpha$.

A **one-head atom on $\{0,1\}^N$** is a function $\phi:\{0,1\}^N\to\mathbb{R}$ of the form $\phi(x)=\dfrac{\eta+\sum_{i=1}^N\rho_i\alpha^{x_i}(m_i+\delta x_i)}{\gamma+\sum_{i=1}^N\rho_i\alpha^{x_i}}$ with $\gamma>0,\rho_i>0,\alpha>0$ and $\eta,\delta,m_i\in\mathbb{R}$.

**Established normal form (use as the definition of head complexity).** For any $N$ and any $h:\{0,1\}^N\to\{0,1\}$, $H^{*}(h)\leq H$ iff there exist one-head atoms on $\{0,1\}^N$ $\phi_1,\dots,\phi_H$ and $c\in\mathbb{R}$ with $h(z)=1 \iff c+\sum_{r=1}^H\phi_r(z)>0$ for all $z$.

**Established restriction monotonicity (you may cite it).** For any $h:\{0,1\}^N\to\{0,1\}$, fixing one coordinate to a constant gives a function $h'$ on $\{0,1\}^{N-1}$ with $H^{*}(h')\leq H^{*}(h)$.

Let $g:\{0,1\}^k\to\{0,1\}$ and define $f:\{0,1\}^n\to\{0,1\}$ by $f(x)=g(x_1,\dots,x_k)$ (so $f$ does not depend on $x_{k+1},\dots,x_n$).

## Claim to prove

$$
H^{*}(f) = H^{*}(g).
$$

That is, padding a function with any number of irrelevant variables does not change its head complexity.

## Guidance (prove every step rigorously)

**Lower bound $H^{*}(g)\leq H^{*}(f)$.** Restrict $f$ by fixing $x_{k+1}=\dots=x_n=0$. The resulting function on $\{0,1\}^k$ is exactly $g$. By iterated restriction monotonicity, $H^{*}(g)\leq H^{*}(f)$.

**Upper bound $H^{*}(f)\leq H^{*}(g)$.** Let $H=H^{*}(g)$, witnessed by one-head atoms $\phi_1,\dots,\phi_H$ on $\{0,1\}^k$ (with parameters $\gamma_r,\alpha_r,\{\rho_{r,i}\}_{i\leq k},\eta_r,\delta_r,\{m_{r,i}\}_{i\leq k}$) and constant $c$, so that $g(y)=1 \iff c+\sum_r\phi_r(y)>0$.

1. **Pad each atom with the irrelevant coordinates at weight $\epsilon$.** For $\epsilon>0$, define an atom $\phi_r^\epsilon$ on $\{0,1\}^n$ that keeps $\gamma_r,\alpha_r,\eta_r,\delta_r$ and $\rho_{r,i},m_{r,i}$ for $i\leq k$, and sets $\rho_{r,i}=\epsilon$, $m_{r,i}=0$ for $k<i\leq n$. Verify $\phi_r^\epsilon$ is a valid one-head atom on $\{0,1\}^n$ (all $\rho_{r,i}>0$, $\gamma_r>0$, $\alpha_r>0$).

2. **Uniform convergence on the finite cube.** For $x\in\{0,1\}^n$ write $y=(x_1,\dots,x_k)$. Show
   $$ \phi_r^\epsilon(x) = \frac{N_r(y) + \epsilon\sum_{i>k}\alpha_r^{x_i}\cdot 0}{D_r(y) + \epsilon\sum_{i>k}\alpha_r^{x_i}} = \frac{N_r(y)}{D_r(y) + \epsilon E_r(x)}, $$
   where $N_r(y),D_r(y)$ are the numerator and denominator of $\phi_r$ on $\{0,1\}^k$ (so $\phi_r(y)=N_r(y)/D_r(y)$, $D_r(y)>0$), and $E_r(x)=\sum_{i>k}\alpha_r^{x_i}$ satisfies $0\leq E_r(x)\leq (n-k)\max(1,\alpha_r)$. Conclude that as $\epsilon\to 0^+$, $\phi_r^\epsilon(x)\to\phi_r(y)$ uniformly over the finite set $\{0,1\}^n$. (Use $D_r(y)\geq d_{\min}:=\min_{y}D_r(y)>0$ and a bound on $|N_r(y)|$.)

3. **Margin argument.** Define $S(x):=c+\sum_{r=1}^H\phi_r(x_1,\dots,x_k)=c+\sum_r\phi_r(y)$, which equals the score for $g$ at $y$, so $f(x)=1 \iff S(x)>0$. If $f\equiv$ constant the claim is immediate by the $0$-head case; otherwise let $\mu:=\min_{x:S(x)\neq 0}|S(x)|$. Since $S$ takes finitely many values, either $\mu>0$ or $S(x)=0$ for some $x$; handle the latter by first shifting the constant $c$ by a tiny amount to make $S$ nowhere zero on the cube while preserving $f(x)=1\iff S(x)>0$ (finite-cube margin shift). Then with $\mu>0$ and $S^\epsilon(x):=c+\sum_r\phi_r^\epsilon(x)$, Step 2 gives $\sup_x|S^\epsilon(x)-S(x)|\to 0$, so for $\epsilon$ small enough $|S^\epsilon(x)-S(x)|<\mu$ for all $x$, whence $S^\epsilon(x)$ has the same sign as $S(x)$ at every $x$. Therefore $f(x)=1 \iff S^\epsilon(x)>0$.

4. **Conclude.** $S^\epsilon=c+\sum_{r=1}^H\phi_r^\epsilon$ is a constant plus $H$ one-head atoms on $\{0,1\}^n$, so by the normal form $H^{*}(f)\leq H=H^{*}(g)$.

Combine the two bounds to get $H^{*}(f)=H^{*}(g)$.

Give a complete, rigorous proof.
