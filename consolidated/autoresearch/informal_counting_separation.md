# Problem: A counting separation of head complexity from threshold degree

## Background and definitions (self-contained)

Fix $n \geq 2$, work on $\{0,1\}^n$. A function $A(x) = a_0 + \sum_i a_i x_i$ is **affine**. $\deg_{\pm}(f)$ is the least degree of a real polynomial sign-representing $f$ on the cube.

**Established results (cite as given):**

- **(Cleared normal form, L16.)** $H^{*}(f) \leq H$ if and only if there exist affine functions $N_1,D_1,\dots,N_H,D_H$ with each $D_h > 0$ on the cube and slopes of one sign (admissible), and $\theta \in \mathbb{R}$, such that
  $$ P(x) = \theta\prod_{h=1}^H D_h(x) + \sum_{h=1}^H N_h(x)\prod_{g\neq h}D_g(x) $$
  satisfies $f(x) = 1 \iff P(x) > 0$ for all $x$.

**External theorems (state precisely; used as given inputs, standard in the literature):**

- **(Warren / Milnor-Thom sign-pattern bound.)** There is an absolute constant $C \geq 1$ such that for any $m \geq 1$ real polynomials $q_1,\dots,q_m$ in $p \geq 1$ real variables, each of degree at most $d \geq 1$, the number of distinct sign vectors
  $$ \big(\mathrm{sgn}\,q_1(w),\dots,\mathrm{sgn}\,q_m(w)\big) \in \{-1,0,1\}^m, \qquad w \in \mathbb{R}^p, $$
  that actually occur is at most $\big(C\,d\,m / p\big)^{p}$ whenever $m \geq p$. (In particular it is at most $2^{O(p\log(dm/p))}$.)
- **(Degree-2 PTF count.)** There is an absolute constant $c_0 > 0$ such that for all large $n$, the number of Boolean functions $f : \{0,1\}^n \to \{0,1\}$ with $\deg_{\pm}(f) \leq 2$ is at least $2^{c_0 n^3}$.

## Claim to prove

**(a) Counting upper bound.** There is an absolute constant $c_1$ such that for every $H \geq 1$ and large $n$,

$$
\#\{\, f : \{0,1\}^n \to \{0,1\} \;\mid\; H^{*}(f) \leq H \,\} \;\leq\; 2^{c_1 H n^2}.
$$

**(b) Separation.** For all large $n$, there exists $f : \{0,1\}^n \to \{0,1\}$ with

$$
\deg_{\pm}(f) \leq 2 \qquad\text{and}\qquad H^{*}(f) \geq \Omega(n).
$$

Hence head complexity is not bounded by any function of threshold degree alone: $H^{*}$ is strictly finer than $\deg_{\pm}$.

## Guidance (prove every step rigorously)

**Part (a).**

1. **Parametrize.** By L16, every $f$ with $H^{*}(f) \leq H$ is realized by a parameter vector $w$ collecting the coefficients of the $H$ affine pairs $(N_h, D_h)$ and the scalar $\theta$. Each affine function on $n$ variables has $n+1$ real coefficients, so $w \in \mathbb{R}^{p}$ with $p = 2H(n+1) + 1$. (Admissibility constrains $w$ to a subset of $\mathbb{R}^p$, which can only decrease the count below; so it suffices to count over all $w \in \mathbb{R}^p$.)

2. **One polynomial per cube point.** For each fixed $x \in \{0,1\}^n$, define
   $$ q_x(w) := \theta\prod_{h=1}^H D_h(x) + \sum_{h=1}^H N_h(x)\prod_{g\neq h}D_g(x), $$
   viewed as a polynomial in $w$. Show $\deg_w q_x \leq H+1$: for fixed $x$, each $D_h(x)$ and $N_h(x)$ is an affine (degree-$1$) function of the corresponding block of $w$; the term $\theta\prod_h D_h(x)$ is a product of $H+1$ degree-$1$ factors in disjoint blocks (degree $\leq H+1$), and each $N_h(x)\prod_{g\neq h}D_g(x)$ is a product of $H$ degree-$1$ factors (degree $\leq H$). So all $q_x$ have degree $\leq H+1$.

3. **Functions are sign patterns.** By L16, for the witness $w$ realizing $f$, $f(x) = 1 \iff q_x(w) > 0$, i.e. $f(x)$ is determined by $\mathrm{sgn}\,q_x(w)$ (with $f(x) = 1$ iff the sign is $+1$, and $f(x) = 0$ iff the sign is $0$ or $-1$). Hence the map $w \mapsto f_w$ (the function realized by $w$) factors through the sign vector $(\mathrm{sgn}\,q_x(w))_{x}$. Therefore
   $$ \#\{f : H^{*}(f) \leq H\} \leq \#\{\text{occurring sign vectors of } (q_x)_{x \in \{0,1\}^n}\}. $$

4. **Apply Warren.** Here $m = 2^n$ (one polynomial per cube point), $d = H+1$, and $p = 2H(n+1)+1 = \Theta(Hn)$. Check $m \geq p$ for large $n$. The Warren bound gives at most $(C(H+1)2^n / p)^p$ sign vectors. Take logs base $2$:
   $$ \log_2(\#) \leq p\log_2\!\Big(\tfrac{C(H+1)2^n}{p}\Big) = \Theta(Hn)\cdot\big(n - \Theta(\log(Hn)) + O(1)\big) = O(Hn^2). $$
   This proves (a) with a suitable constant $c_1$.

**Part (b).**

5. Suppose, for contradiction, that every degree-$2$ PTF on $n$ variables had $H^{*}(f) \leq H$ for some $H = o(n)$. By the degree-2 PTF count, the number of degree-$2$ PTFs is at least $2^{c_0 n^3}$, so by part (a),
   $$ 2^{c_0 n^3} \leq \#\{f : H^{*}(f) \leq H\} \leq 2^{c_1 H n^2}. $$
6. Taking logs, $c_0 n^3 \leq c_1 H n^2$, i.e. $H \geq (c_0/c_1)\,n$. This contradicts $H = o(n)$ for large $n$.

7. Therefore, for all large $n$, some degree-$2$ PTF $f$ has $H^{*}(f) \geq (c_0/c_1)\,n = \Omega(n)$, while $\deg_{\pm}(f) \leq 2$. This is the claimed separation.

Be careful and explicit about: the degree-in-$w$ computation in Step 2; the inequality $m \geq p$; that the admissibility constraints only shrink the realized set; and the logarithm estimate in Step 4. Provide a complete, rigorous proof of (a) and (b).
