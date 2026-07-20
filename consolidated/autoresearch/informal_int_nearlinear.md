# Problem: An explicit near-linear lower bound on the head complexity of set intersection

## Background and definitions (self-contained)

For $n \geq 1$, the set-intersection function on $2n$ bits is $\mathrm{INT}_n(x,y) = \bigvee_{i=1}^n (x_i \wedge y_i)$, $x,y \in \lbrace 0,1\rbrace^n$; it is $1$ iff some index $i$ has $x_i = y_i = 1$. For $S \subseteq [n]$, $\mathbf 1_S \in \lbrace 0,1\rbrace^n$ is its indicator and $e_j = \mathbf 1_{\lbrace j\rbrace}$.

**The tangent-form normal form (established, L16).** A function $A(x,y) = a_0 + \sum_i a_i x_i + \sum_i a'_i y_i$ is **affine**. For $H \geq 1$, $\mathrm{tChow}_{\pm}(g) \leq H$ means there exist affine $N_1,D_1,\dots,N_H,D_H$ (arbitrary, no positivity constraint) and $\theta \in \mathbb{R}$ such that the **tangent form**

$$
P(x,y) = \theta \prod_{h=1}^H D_h(x,y) + \sum_{h=1}^H N_h(x,y)\prod_{g\neq h} D_g(x,y)
$$

**sign-represents** $g$: $g(x,y) = 1 \iff P(x,y) > 0$, and $g(x,y) = 0 \iff P(x,y) < 0$, for all $(x,y)$. The head complexity satisfies $\mathrm{tChow}_{\pm}(g) \leq H^{*}(g)$ (the sandwich, L18), since $H^{*}$ uses the same form with the extra admissibility constraints $D_h > 0$ on the cube and one-sided slopes; dropping those constraints only lowers the value. Hence **any lower bound on $\mathrm{tChow}_{\pm}$ is also a lower bound on $H^{*}$**.

**External theorem (Warren / Milnor-Thom sign-pattern bound; used as given).** There is an absolute constant $C \geq 1$ such that for any $m \geq 1$ real polynomials $q_1,\dots,q_m$ in $p \geq 1$ real variables, each of degree at most $d \geq 1$, the number of distinct sign vectors $(\mathrm{sgn}\,q_1(w),\dots,\mathrm{sgn}\,q_m(w)) \in \lbrace -1,0,1\rbrace^m$ realized over all $w \in \mathbb{R}^p$ is at most $(C d m / p)^{p}$, provided $m \geq p$.

## Claim to prove

There is an absolute constant $c > 0$ such that for all sufficiently large $n$,

$$
H^{*}(\mathrm{INT}_n) \;\geq\; \mathrm{tChow}_{\pm}(\mathrm{INT}_n) \;\geq\; \frac{c\,n}{\log_2 n}.
$$

That is, the head complexity of set intersection is near-linear, while $\deg_{\pm}(\mathrm{INT}_n) = 2$ (constant): an **explicit** separation of head complexity from threshold degree at a polynomial (near-linear) rate, requiring no positivity. (Contrast the flattening bound, which gives only $\Omega(\log n)$ here.)

## Guidance (prove every step rigorously)

Fix a sign-representing tangent form $P$ of order $H = \mathrm{tChow}_{\pm}(\mathrm{INT}_n)$, with affine
$$
N_h(x,y) = a_h + \sum_i p_{hi} x_i + \sum_i q_{hi} y_i, \qquad
D_h(x,y) = b_h + \sum_i r_{hi} x_i + \sum_i s_{hi} y_i,
$$
and scalar $\theta$.

**Case A (small $H$): assume $2H + 1 \leq n$.** (The complementary case $2H+1 > n$ is handled at the end.)

1. **Restrict to rows $x = \mathbf 1_S$ and singleton columns $y = e_j$.** For $S \subseteq [n]$, $j \in [n]$, define
   $$
   \alpha_{h,S} = a_h + \sum_{i \in S} p_{hi}, \qquad \beta_{h,S} = b_h + \sum_{i \in S} r_{hi}.
   $$
   Then $N_h(\mathbf 1_S, e_j) = \alpha_{h,S} + q_{hj}$ and $D_h(\mathbf 1_S, e_j) = \beta_{h,S} + s_{hj}$. *(justification: $(\mathbf 1_S)_i = [i \in S]$ and $(e_j)_i = [i = j]$, substituted into the affine forms.)*

2. **The restricted tangent value.** Therefore
   $$
   P(\mathbf 1_S, e_j) = \theta \prod_{h=1}^H (\beta_{h,S} + s_{hj}) + \sum_{h=1}^H (\alpha_{h,S} + q_{hj}) \prod_{g \neq h} (\beta_{g,S} + s_{gj}).
   $$
   *(justification: substitute Step 1 into the definition of $P$.)*

3. **The sign pattern realized by each $S$.** Since $\mathrm{INT}_n(\mathbf 1_S, e_j) = 1 \iff j \in S$ (the only common-$1$ coordinate could be $j$, present iff $j \in S$), and $P$ sign-represents $\mathrm{INT}_n$,
   $$
   \mathrm{sgn}\, P(\mathbf 1_S, e_j) = +1 \text{ if } j \in S, \qquad \mathrm{sgn}\, P(\mathbf 1_S, e_j) = -1 \text{ if } j \notin S.
   $$
   *(justification: strict sign-representation evaluated at the cube point $(\mathbf 1_S, e_j)$.)*

4. **Define $n$ polynomials in $2H+1$ parameters.** Introduce the parameter vector $w = (\theta, \alpha_1, \dots, \alpha_H, \beta_1, \dots, \beta_H) \in \mathbb{R}^{2H+1}$. For each column $j \in [n]$, define
   $$
   Q_j(w) = \theta \prod_{h=1}^H (\beta_h + s_{hj}) + \sum_{h=1}^H (\alpha_h + q_{hj}) \prod_{g \neq h} (\beta_g + s_{gj}),
   $$
   where the $s_{hj}, q_{hj}$ are fixed real constants (read off from the fixed $P$). *(justification: definition; $Q_j$ is a polynomial in the $2H+1$ entries of $w$.)*

5. **Degree bound.** Each $Q_j$ has total degree at most $H+1$ in $w$: the term $\theta \prod_h (\beta_h + s_{hj})$ is a product of the $1$ variable $\theta$ and $H$ degree-$1$ factors $(\beta_h + s_{hj})$, degree $H+1$; each summand $(\alpha_h + q_{hj}) \prod_{g \neq h}(\beta_g + s_{gj})$ is a product of $H$ degree-$1$ factors, degree $H$. *(justification: degree of a product is the sum of degrees; constants $s_{hj}, q_{hj}$ have degree $0$.)*

6. **All $2^n$ sign patterns occur.** For $S \subseteq [n]$ put $w_S = (\theta, \alpha_{1,S}, \dots, \alpha_{H,S}, \beta_{1,S}, \dots, \beta_{H,S}) \in \mathbb{R}^{2H+1}$. By construction $Q_j(w_S) = P(\mathbf 1_S, e_j)$, so by Step 3 the sign vector $(\mathrm{sgn}\,Q_1(w_S), \dots, \mathrm{sgn}\,Q_n(w_S))$ equals the $\pm 1$ indicator vector of $S$ (entry $j$ is $+1$ iff $j \in S$). As $S$ ranges over all $2^n$ subsets of $[n]$, these indicator vectors are pairwise distinct, so at least $2^n$ distinct sign vectors of $(Q_1,\dots,Q_n)$ are realized over $w \in \mathbb{R}^{2H+1}$. *(justification: distinct subsets give distinct $\pm 1$ vectors; each is realized by its $w_S$.)*

7. **Apply Warren.** With $m = n$ polynomials, $p = 2H+1$ variables, degree $d = H+1$, and the hypothesis $m = n \geq 2H+1 = p$ (Case A), the number of realized sign vectors is at most $(C(H+1)n/(2H+1))^{2H+1}$. Combined with Step 6,
   $$
   2^n \;\leq\; \left(\frac{C(H+1)\,n}{2H+1}\right)^{2H+1}.
   $$
   *(justification: Warren's bound and Step 6.)*

8. **Take logarithms.** Since $(H+1)/(2H+1) \leq 1$, the base satisfies $C(H+1)n/(2H+1) \leq C n$. Taking $\log_2$,
   $$
   n \;\leq\; (2H+1)\,\log_2\!\left(\frac{C(H+1)n}{2H+1}\right) \;\leq\; (2H+1)\,\log_2(C n) = (2H+1)\,(\log_2 n + \log_2 C).
   $$
   *(justification: monotonicity of $\log_2$ on Step 7, then $C(H+1)n/(2H+1) \leq Cn$.)*

9. **Solve for $H$.** For large $n$, $\log_2 n + \log_2 C \leq 2\log_2 n$, so $n \leq (2H+1)\cdot 2\log_2 n$, giving
   $$
   2H + 1 \;\geq\; \frac{n}{2\log_2 n}, \qquad\text{hence}\qquad H \geq \frac{n}{4\log_2 n} - \frac12 \geq \frac{n}{8\log_2 n}
   $$
   for all sufficiently large $n$. *(justification: rearrange Step 8; absorb the $-\tfrac12$ for large $n$.)*

**Case B (large $H$): $2H+1 > n$.** Then $H > (n-1)/2 \geq n/(8\log_2 n)$ for large $n$ (since $4\log_2 n > 1$). So the bound $H \geq n/(8\log_2 n)$ holds here trivially.

10. **Conclude.** In both cases $H = \mathrm{tChow}_{\pm}(\mathrm{INT}_n) \geq n/(8\log_2 n)$ for large $n$; take $c = 1/8$. Since $\mathrm{tChow}_{\pm}(\mathrm{INT}_n) \leq H^{*}(\mathrm{INT}_n)$, the same bound holds for $H^{*}$. $\blacksquare$

## Pitfalls to address explicitly

- **The parameter count is the crux.** On singleton columns the row $\mathbf 1_S$ enters $P$ only through the $2H+1$ numbers $(\theta, \alpha_{h,S}, \beta_{h,S})$, independent of $n$. This "coefficient tying" is what makes Warren bite: although the full cleared matrix can have cut-rank $\sim 2^H$, here only $2H+1$ free parameters move. The proof must fix $P$ first (so the $q_{hj}, s_{hj}$ are constants) and vary only $w$.
- **Warren's hypothesis $m \geq p$** ($n \geq 2H+1$) is needed; the case $2H+1 > n$ must be dispatched separately (Case B), where the bound holds trivially.
- **Degree is $H+1$, not $2^H$.** The relevant complexity for Warren is the degree of $Q_j$ in the parameters ($H+1$), times the parameter dimension ($2H+1$); the exponential flattening rank is irrelevant on this slice.
- **No positivity is used.** $N_h, D_h$ are arbitrary affine forms; the bound is on $\mathrm{tChow}_{\pm}$, hence also on $H^{*}$. The argument is an explicit (function-specific) analogue of the nonconstructive counting separation, localized to $\mathrm{INT}_n$ via the singleton-column restriction.
- The $\pm 1$ indicator vectors of distinct subsets are distinct, giving exactly $2^n$ realized strict sign patterns; zeros do not occur because sign-representation is strict.
