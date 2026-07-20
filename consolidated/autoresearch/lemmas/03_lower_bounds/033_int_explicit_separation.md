# An Explicit Function Separating Head Complexity from Threshold Degree

## Statement

Let $\mathrm{INT}_n(x,y) = \bigvee_{i=1}^n (x_i \wedge y_i)$ be the set-intersection (NOT-disjointness) function on $2n$ bits, $x,y \in \lbrace 0,1\rbrace^n$. Then:

**(a)** $\deg_{\pm}(\mathrm{INT}_n) = 2$ for every $n \geq 2$.

**(b)** $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$ for every $n \geq 1$, where $x|y$ is the cut separating the $x$-coordinates from the $y$-coordinates.

**(c)** For every $n \geq 14$,

$$
\deg_{\pm}(\mathrm{INT}_n) = 2 \;<\; 3 \;\leq\; H^{*}(\mathrm{INT}_n).
$$

> **The first explicit (non-counting, non-numerical) separation of $H^{*}$ from threshold degree.** The counting separation [023_counting_separation.md](023_counting_separation.md) produces a $\deg_{\pm}=2$ function with $H^{*}=\Omega(n)$ but only nonconstructively; the $\neg\mathrm{DISJ}_4$ candidate (`claude-comments/empirical_findings.md`) was numerical. Here a single named function, $\mathrm{INT}_{14}$ on $28$ bits, is *proved* to need a third head while sign-representable in degree $2$. The lower bound is the flattening/sign-rank obstruction [022_flattening_lower_bound.md](022_flattening_lower_bound.md), so by [029_tchow_flattening.md](029_tchow_flattening.md) the same bound gives $\mathrm{tChow}_{\pm}(\mathrm{INT}_{14}) \geq 3$: the separation is **positivity-free**.

## Proof

### (a) Threshold degree is exactly 2

**Upper bound.** The degree-2 polynomial $p(x,y) = \sum_{i=1}^n x_i y_i - \tfrac12$ sign-represents $\mathrm{INT}_n$: if $\mathrm{INT}_n(x,y)=1$ some $x_i y_i = 1$ so $\sum_i x_i y_i \geq 1$ and $p \geq \tfrac12 > 0$; if $\mathrm{INT}_n(x,y)=0$ then every $x_i y_i = 0$ so $\sum_i x_i y_i = 0$ and $p = -\tfrac12 < 0$. Hence $\deg_{\pm}(\mathrm{INT}_n) \leq 2$.

**Lower bound.** Suppose an affine $A(x,y) = c + \sum_i a_i x_i + \sum_i b_i y_i$ sign-represented $\mathrm{INT}_n$ ($n \geq 2$). Set all coordinates outside $\lbrace 1,2\rbrace$ to $0$ and consider $P_1 = (e_1, e_1)$, $P_2 = (e_1, e_2)$, $P_3 = (e_2, e_1)$, $P_4 = (e_2, e_2)$, with $\mathrm{INT}_n$-values $1,0,0,1$ respectively. Sign-representation forces $A(P_1), A(P_4) > 0$ and $A(P_2), A(P_3) < 0$. But

$$
A(P_1) + A(P_4) = 2c + a_1 + a_2 + b_1 + b_2 = A(P_2) + A(P_3),
$$

so a strictly positive sum equals a strictly negative sum, a contradiction. Hence $\deg_{\pm}(\mathrm{INT}_n) \geq 2$, and with the upper bound, $\deg_{\pm}(\mathrm{INT}_n) = 2$.

### (b) Cut sign-rank is at least n

Let $r = \mathrm{sr}_{x|y}(\mathrm{INT}_n)$ and let $R$ be a rank-$r$ real matrix (rows $x$, columns $y$) with $R[x,y] > 0$ iff $\mathrm{INT}_n(x,y)=1$. Factor $R[x,y] = \langle a_x, b_y\rangle$ with $a_x, b_y \in \mathbb{R}^r$ (a homogeneous inner product). For $S \subseteq [n]$ and $i \in [n]$, $\mathrm{INT}_n(\mathbf 1_S, e_i) = 1$ iff $i \in S$ (the only coordinate where $e_i$ is $1$ is $i$, and $(\mathbf 1_S)_i = 1$ iff $i \in S$). Thus $\langle a_{\mathbf 1_S}, b_{e_i}\rangle > 0$ for $i \in S$ and $< 0$ for $i \notin S$: every dichotomy of the $n$ points $b_{e_1}, \dots, b_{e_n} \in \mathbb{R}^r$ is realized by a homogeneous linear functional.

If $r < n$ the points $b_{e_1}, \dots, b_{e_n}$ are linearly dependent: $\sum_i c_i b_{e_i} = 0$ with $c \neq 0$; negating $c$ if needed, $P = \lbrace i : c_i > 0\rbrace \neq \emptyset$. Taking the functional $w = a_{\mathbf 1_P}$ realizing the dichotomy $P$,

$$
0 = \Big\langle w, \sum_i c_i b_{e_i}\Big\rangle = \sum_i c_i \langle w, b_{e_i}\rangle .
$$

Each term is $\geq 0$: for $c_i > 0$, $i \in P$ so $\langle w, b_{e_i}\rangle > 0$; for $c_i < 0$, $i \notin P$ so $\langle w, b_{e_i}\rangle < 0$; for $c_i = 0$ the term vanishes. Since $P \neq \emptyset$ some term is strictly positive, so the sum is $> 0$, contradicting $0$. Hence $r \geq n$.

### (c) The separation

By (b) and the flattening bound [022_flattening_lower_bound.md](022_flattening_lower_bound.md) on the cut $x|y$,

$$
n \;\leq\; \mathrm{sr}_{x|y}(\mathrm{INT}_n) \;\leq\; \big(H^{*}(\mathrm{INT}_n)+1\big)\,2^{H^{*}(\mathrm{INT}_n)} + 1 .
$$

Write $\Phi(H) = (H+1)2^H + 1$, strictly increasing with $\Phi(2) = 13$. If $H^{*}(\mathrm{INT}_n) \leq 2$ then $n \leq \Phi(2) = 13$. Contrapositively, $n \geq 14$ forces $H^{*}(\mathrm{INT}_n) \geq 3$. With (a), $\deg_{\pm}(\mathrm{INT}_n) = 2 < 3 \leq H^{*}(\mathrm{INT}_n)$. $\blacksquare$

## Consequence

This is the first per-function lower bound that provably beats threshold degree on a *named* function. Two strengthenings follow from the same chain:

- **Unbounded explicit separation.** For $H \geq 2$, $\Phi(H) \leq 2^H(H+2) \leq 4^H$, so $n \leq 4^{H^{*}(\mathrm{INT}_n)}$ and $H^{*}(\mathrm{INT}_n) \geq \tfrac12\log_2 n \to \infty$, while $\deg_{\pm}(\mathrm{INT}_n) = 2$ for all $n$ (see [034_int_logarithmic_separation.md](034_int_logarithmic_separation.md)).
- **Flattening is logarithmically capped on constant-degree functions.** A degree-$d$ sign-representation gives $\mathrm{sr}_{A|B} \leq \binom{N}{\leq d}$, so for $\deg_{\pm}(f) = O(1)$ the flattening bound can never exceed $H^{*}(f) = \Omega(\log N)$. So the flattening route gives only $\Omega(\log n)$ here ([034_int_logarithmic_separation.md](034_int_logarithmic_separation.md)). The genuinely stronger, polynomial-rate explicit separation comes from a *different* obstruction ([035_int_nearlinear_lower.md](035_int_nearlinear_lower.md), a singleton-column Warren count): $H^{*}(\mathrm{INT}_n) = \Omega(n/\log n)$, near-linear and positivity-free, so $H^{*}(\mathrm{INT}_n) = \widetilde{\Theta}(n)$. This $\mathrm{INT}_n$ separation is thus far stronger than flattening alone suggests.
