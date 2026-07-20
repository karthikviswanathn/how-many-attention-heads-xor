# Problem: The separation from threshold degree already holds without positivity

## Background and definitions (self-contained)

Fix $n \geq 2$, work on $\{0,1\}^n$. A function $A(x) = a_0 + \sum_i a_i x_i$ is **affine**. $\deg_{\pm}(f)$ is the least degree of a real polynomial sign-representing $f$ on the cube (meaning $f(x)=1 \iff Q(x)>0$).

**Tangential-Chow sign-rank.** Define $\mathrm{tChow}_{\pm}(f)$ as the least $H \geq 0$ for which there exist *arbitrary* affine functions $N_1,D_1,\dots,N_H,D_H$ (no positivity or sign constraints) and $\theta \in \mathbb{R}$ such that

$$
P(x) = \theta\prod_{h=1}^H D_h(x) + \sum_{h=1}^H N_h(x)\prod_{g\neq h}D_g(x)
$$

sign-represents $f$ (i.e. $f(x)=1 \iff P(x)>0$ for all $x$). (For $H=0$, $P=\theta$.)

**Established facts you may cite and use:**
- **(Sandwich, L18.)** $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$ for every $f$.

**External theorems (state precisely; standard, used as given inputs):**
- **(Warren 1968.)** There is an absolute constant $C$ such that for $m \geq p \geq 1$ real polynomials $q_1,\dots,q_m$ in $p$ variables of degree $\leq d$, the number of distinct sign vectors $(\mathrm{sgn}\,q_1(w),\dots,\mathrm{sgn}\,q_m(w)) \in \{-1,0,1\}^m$ realized over $w \in \mathbb{R}^p$ is at most $(C\,d\,m/p)^p$.
- **(Degree-2 PTF count; Baldi-Vershynin 2019.)** The number of degree-$\leq 2$ polynomial threshold functions on $\{0,1\}^n$ is at least $2^{c_0 n^3}$ for an absolute constant $c_0 > 0$ and all large $n$.

## Claim to prove

**(a)** There is an absolute constant $c_1$ with $\#\{ f : \mathrm{tChow}_{\pm}(f) \leq H \} \leq 2^{c_1 H n^2}$ for every $H \geq 1$ and large $n$.

**(b)** For all large $n$ there exists $f$ with $\deg_{\pm}(f) \leq 2$ and $\mathrm{tChow}_{\pm}(f) = \Omega(n)$.

**(c)** Consequently, since $\mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$, the same $f$ has $\deg_{\pm}(f) \leq 2$ and $H^{*}(f) = \Omega(n)$. Moreover the separation of head complexity from threshold degree is **already present at the positivity-free level**: the attention-specific positivity/one-sided-slope constraints are not the source of the gap between $\deg_{\pm}$ and $H^{*}$.

## Guidance (prove every step rigorously)

**Part (a).**
1. By definition, $f$ with $\mathrm{tChow}_{\pm}(f) \leq H$ is realized by a parameter vector $w$ collecting the coefficients of the $H$ affine pairs $(N_h, D_h)$ and $\theta$; since each affine function has $n+1$ coefficients, $w \in \mathbb{R}^p$ with $p = 2H(n+1) + 1 = \Theta(Hn)$. (No admissibility constraint here, unlike for $H^{*}$.)
2. For each $x \in \{0,1\}^n$, $q_x(w) := \theta\prod_h D_h(x) + \sum_h N_h(x)\prod_{g\neq h}D_g(x)$ is a polynomial in $w$ of degree $\leq H+1$ (for fixed $x$, each $D_h(x), N_h(x)$ is degree $1$ in $w$; the products have degree $\leq H+1$). By definition of $\mathrm{tChow}_{\pm}$, $f(x) = 1 \iff q_x(w) > 0$, so $f$ is determined by the sign vector $(\mathrm{sgn}\,q_x(w))_x$.
3. Hence $\#\{f : \mathrm{tChow}_{\pm}(f) \leq H\} \leq \#\{\text{sign vectors of } (q_x)_x\}$. Apply Warren with $m = 2^n$, $d = H+1$, $p = \Theta(Hn)$ (check $m \geq p$ for large $n$): the count is at most $(C(H+1)2^n/p)^p$, so $\log_2(\#) \leq p\log_2(C(H+1)2^n/p) = O(Hn^2)$.

**Part (b).**
4. Let $\mathcal T_n = \{f : \deg_{\pm}(f) \leq 2\}$, with $|\mathcal T_n| \geq 2^{c_0 n^3}$. If every $f \in \mathcal T_n$ had $\mathrm{tChow}_{\pm}(f) \leq H_n := \lfloor \gamma n\rfloor$ with $\gamma = c_0/(2c_1)$, then by part (a), $2^{c_0 n^3} \leq 2^{c_1 H_n n^2} \leq 2^{(c_0/2)n^3}$, a contradiction for large $n$. So some $f \in \mathcal T_n$ has $\mathrm{tChow}_{\pm}(f) > \lfloor\gamma n\rfloor$, hence $\mathrm{tChow}_{\pm}(f) \geq \gamma n = \Omega(n)$, while $\deg_{\pm}(f) \leq 2$.

**Part (c).**
5. By the sandwich $\mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$, the same $f$ has $H^{*}(f) \geq \mathrm{tChow}_{\pm}(f) = \Omega(n)$ and $\deg_{\pm}(f) \leq 2$. State the conclusion that the separation holds already without positivity, so positivity is not the cause of the $\deg_{\pm}$-to-$H^{*}$ gap; whether positivity adds any FURTHER cost (i.e. whether $\mathrm{tChow}_{\pm} < H^{*}$ for some $f$) is left open.

Give a complete, rigorous proof of (a), (b), (c).
