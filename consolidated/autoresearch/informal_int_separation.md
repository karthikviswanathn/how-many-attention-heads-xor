# Problem: A rigorous explicit separation of head complexity from threshold degree via set intersection

## Background and definitions (self-contained)

Fix $n \geq 2$. The **set-intersection function** (also called NOT-disjointness) is the Boolean function on $2n$ variables
$$
\mathrm{INT}_n(x,y) \;=\; \bigvee_{i=1}^n (x_i \wedge y_i), \qquad x,y \in \lbrace 0,1\rbrace^n,
$$
i.e. $\mathrm{INT}_n(x,y) = 1$ iff there exists an index $i$ with $x_i = y_i = 1$, and $0$ otherwise. We regard $\mathrm{INT}_n$ as a Boolean function on the $2n$ input bits $(x,y)$.

A real polynomial $p$ in the $2n$ variables **sign-represents** a Boolean function $g$ on $\lbrace 0,1\rbrace^{2n}$ if $g(z) = 1 \Rightarrow p(z) > 0$ and $g(z) = 0 \Rightarrow p(z) < 0$ for all $z$ (so $p$ is nonzero on the cube). The **threshold degree** $\deg_{\pm}(g)$ is the least degree of a polynomial that sign-represents $g$.

For a bipartition of the input coordinates $A \sqcup B$ and a Boolean function $g$, write each input as $(u,v)$ with $u \in \lbrace 0,1\rbrace^A$, $v \in \lbrace 0,1\rbrace^B$. The **cut sign-rank** $\mathrm{sr}_{A|B}(g)$ is the least rank of a real matrix $R$ indexed by $(u,v)$ with $R[u,v] > 0$ when $g(u,v) = 1$ and $R[u,v] < 0$ when $g(u,v) = 0$ (a strict sign-representation across the cut). $H^{*}(g)$ denotes the head complexity (minimum attention heads) of $g$; only the cited inequality below is used about it.

For $\mathrm{INT}_n$ we always use the canonical cut $A = \lbrace x\text{-coordinates}\rbrace$, $B = \lbrace y\text{-coordinates}\rbrace$, and write $\mathrm{sr}_{x|y}(\mathrm{INT}_n)$. For $S \subseteq [n]$ let $\mathbf 1_S \in \lbrace 0,1\rbrace^n$ be its indicator vector, and let $e_i = \mathbf 1_{\lbrace i\rbrace}$ be the $i$-th standard basis vector.

**Established result (cite as given).**

- **(Flattening / sign-rank upper bound, L22.)** For every Boolean function $g$ on $\lbrace 0,1\rbrace^N$ and every bipartition $A \sqcup B$ of its coordinates,
  $$
  \mathrm{sr}_{A|B}(g) \;\leq\; \big(H^{*}(g) + 1\big)\,2^{H^{*}(g)} + 1 .
  $$

## Claim to prove

1. **Threshold degree.** $\deg_{\pm}(\mathrm{INT}_n) = 2$ for every $n \geq 2$.
2. **Sign-rank lower bound.** $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$ for every $n \geq 1$.
3. **Explicit separation.** For every $n \geq 14$, $H^{*}(\mathrm{INT}_n) \geq 3$. Consequently, for $n \geq 14$,
   $$
   \deg_{\pm}(\mathrm{INT}_n) = 2 \;<\; 3 \;\leq\; H^{*}(\mathrm{INT}_n).
   $$
   This is an explicit Boolean function (on $N = 2n \geq 28$ bits) whose head complexity strictly exceeds its threshold degree, proved without any numerical search.

## Guidance (prove every step rigorously)

### Part 1: $\deg_{\pm}(\mathrm{INT}_n) = 2$

**Upper bound $\deg_{\pm}(\mathrm{INT}_n) \leq 2$.**

1. Define the degree-2 polynomial $p(x,y) = \sum_{i=1}^n x_i y_i - \tfrac12$.
2. If $\mathrm{INT}_n(x,y) = 1$, there is an index $i$ with $x_i = y_i = 1$, so $\sum_i x_i y_i \geq 1$ and $p(x,y) \geq \tfrac12 > 0$. *(justification: each term $x_i y_i \in \lbrace 0,1\rbrace$ is nonnegative and at least one equals $1$.)*
3. If $\mathrm{INT}_n(x,y) = 0$, then $x_i y_i = 0$ for every $i$, so $\sum_i x_i y_i = 0$ and $p(x,y) = -\tfrac12 < 0$. *(justification: definition of $\mathrm{INT}_n = 0$.)*
4. Hence $p$ sign-represents $\mathrm{INT}_n$ and has degree $2$, so $\deg_{\pm}(\mathrm{INT}_n) \leq 2$.

**Lower bound $\deg_{\pm}(\mathrm{INT}_n) \geq 2$** (i.e. no affine/degree-$1$ polynomial sign-represents $\mathrm{INT}_n$, using $n \geq 2$).

5. Suppose for contradiction an affine $A(x,y) = c + \sum_i a_i x_i + \sum_i b_i y_i$ sign-represents $\mathrm{INT}_n$. Consider the four inputs obtained by setting all coordinates outside $\lbrace 1,2\rbrace$ to $0$:
   - $P_1$: $x = e_1,\ y = e_1$ (i.e. $x_1=y_1=1$, rest $0$); $\mathrm{INT}_n(P_1) = 1$.
   - $P_2$: $x = e_1,\ y = e_2$; $\mathrm{INT}_n(P_2) = 0$.
   - $P_3$: $x = e_2,\ y = e_1$; $\mathrm{INT}_n(P_3) = 0$.
   - $P_4$: $x = e_2,\ y = e_2$; $\mathrm{INT}_n(P_4) = 1$.
   *(justification: evaluate $\bigvee_i (x_i \wedge y_i)$; only $P_1$ and $P_4$ have a coordinate where both $x$ and $y$ are $1$.)*
6. Sign-representation requires $A(P_1) > 0$, $A(P_4) > 0$, $A(P_2) < 0$, $A(P_3) < 0$.
7. Compute the two diagonal sums using $A(x,y) = c + \sum a_i x_i + \sum b_i y_i$:
   $$
   A(P_1) + A(P_4) = \big(c + a_1 + b_1\big) + \big(c + a_2 + b_2\big) = 2c + a_1 + a_2 + b_1 + b_2,
   $$
   $$
   A(P_2) + A(P_3) = \big(c + a_1 + b_2\big) + \big(c + a_2 + b_1\big) = 2c + a_1 + a_2 + b_1 + b_2.
   $$
   So $A(P_1) + A(P_4) = A(P_2) + A(P_3)$. *(justification: direct substitution; both sums collect $a_1+a_2$ and $b_1+b_2$.)*
8. But Step 6 gives $A(P_1) + A(P_4) > 0$ while $A(P_2) + A(P_3) < 0$, contradicting their equality. Hence no affine sign-representation exists and $\deg_{\pm}(\mathrm{INT}_n) \geq 2$.
9. Combining Steps 4 and 8, $\deg_{\pm}(\mathrm{INT}_n) = 2$.

### Part 2: $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$

Let $r = \mathrm{sr}_{x|y}(\mathrm{INT}_n)$ and let $R$ be a real matrix of rank $r$, rows indexed by $x \in \lbrace 0,1\rbrace^n$ and columns by $y \in \lbrace 0,1\rbrace^n$, with $R[x,y] > 0$ when $\mathrm{INT}_n(x,y) = 1$ and $R[x,y] < 0$ when $\mathrm{INT}_n(x,y) = 0$.

10. **Factorize.** Since $\mathrm{rank}(R) = r$, there exist vectors $a_x \in \mathbb{R}^r$ (for each row $x$) and $b_y \in \mathbb{R}^r$ (for each column $y$) with $R[x,y] = \langle a_x, b_y\rangle$. *(justification: a rank-$r$ real matrix factors as $R = U V^{\top}$ with $U$ having $r$ columns; take $a_x$ = row $x$ of $U$, $b_y$ = row $y$ of $V$.)*
11. **Membership submatrix.** For $S \subseteq [n]$ and $i \in [n]$, evaluate $\mathrm{INT}_n(\mathbf 1_S, e_i) = \bigvee_{j} \big((\mathbf 1_S)_j \wedge (e_i)_j\big)$. The $j$-th disjunct is $1$ iff $j \in S$ and $j = i$; the disjunction is therefore $1$ iff $i \in S$. So $\mathrm{INT}_n(\mathbf 1_S, e_i) = 1$ if $i \in S$ and $0$ if $i \notin S$. *(justification: $(e_i)_j = 1 \iff j = i$, and $(\mathbf 1_S)_i = 1 \iff i \in S$.)*
12. **Dichotomies are homogeneous halfspaces.** By Steps 10 and 11, for each $S \subseteq [n]$ and each $i \in [n]$,
    $$
    \langle a_{\mathbf 1_S}, b_{e_i}\rangle = R[\mathbf 1_S, e_i] \;\begin{cases} > 0 & i \in S, \\ < 0 & i \notin S. \end{cases}
    $$
    Thus the linear functional $z \mapsto \langle a_{\mathbf 1_S}, z\rangle$ on $\mathbb{R}^r$ is strictly positive on $\lbrace b_{e_i} : i \in S\rbrace$ and strictly negative on $\lbrace b_{e_i} : i \notin S\rbrace$. As $S$ ranges over all $2^n$ subsets, every dichotomy (two-coloring) of the $n$ points $b_{e_1},\dots,b_{e_n}$ is realized by some homogeneous linear functional. *(justification: each subset $S$ gives the dichotomy with positive class exactly $\lbrace b_{e_i}: i\in S\rbrace$, and all subsets occur.)*
13. **Shattering forces dimension.** Prove the following self-contained fact: if $n$ points $q_1,\dots,q_n \in \mathbb{R}^r$ admit, for every subset $T \subseteq [n]$, a vector $w_T \in \mathbb{R}^r$ with $\langle w_T, q_i\rangle > 0$ for $i \in T$ and $\langle w_T, q_i\rangle < 0$ for $i \notin T$, then $n \leq r$. *(Proof: suppose $r < n$. Then $q_1,\dots,q_n$ are linearly dependent, so there is a nonzero $c \in \mathbb{R}^n$ with $\sum_{i=1}^n c_i q_i = 0$. Replacing $c$ by $-c$ if needed, assume the set $P = \lbrace i : c_i > 0\rbrace$ is nonempty. Apply the hypothesis with $T = P$ to get $w_P$ with $\langle w_P, q_i\rangle > 0$ for $i \in P$ and $\langle w_P, q_i\rangle < 0$ for $i \notin P$. Then*
    $$
    0 = \Big\langle w_P, \sum_{i=1}^n c_i q_i \Big\rangle = \sum_{i=1}^n c_i \langle w_P, q_i\rangle .
    $$
    *Examine each term: if $c_i > 0$ then $i \in P$ so $\langle w_P, q_i\rangle > 0$ and $c_i \langle w_P, q_i\rangle > 0$; if $c_i < 0$ then $i \notin P$ so $\langle w_P, q_i\rangle < 0$ and again $c_i \langle w_P, q_i\rangle > 0$; if $c_i = 0$ the term is $0$. Since $P \neq \emptyset$ at least one term is strictly positive and none is negative, so the sum is $> 0$, contradicting $= 0$. Hence $r \geq n$.)*
14. Apply Step 13 with $q_i = b_{e_i}$ (the hypothesis is exactly Step 12, taking $w_T = a_{\mathbf 1_T}$). Conclude $n \leq r = \mathrm{sr}_{x|y}(\mathrm{INT}_n)$.

### Part 3: the separation

15. By Part 2, $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$. By the flattening bound L22 applied to $g = \mathrm{INT}_n$ with the cut $x|y$,
    $$
    n \;\leq\; \mathrm{sr}_{x|y}(\mathrm{INT}_n) \;\leq\; \big(H^{*}(\mathrm{INT}_n) + 1\big)\,2^{H^{*}(\mathrm{INT}_n)} + 1 .
    $$
16. Let $H = H^{*}(\mathrm{INT}_n)$ and $\Phi(H) = (H+1)2^H + 1$. Then $\Phi(0) = 2$, $\Phi(1) = 5$, $\Phi(2) = 13$, and $\Phi$ is strictly increasing for integer $H \geq 0$ (since $(H+2)2^{H+1} > (H+1)2^H$). *(justification: direct evaluation and $(H{+}2)2^{H+1} - (H{+}1)2^H = 2^H(2H{+}4 - H{-}1) = 2^H(H{+}3) > 0$.)*
17. Suppose $H \leq 2$. Then $\Phi(H) \leq \Phi(2) = 13$ by monotonicity, so Step 15 gives $n \leq 13$. *(justification: monotonicity of $\Phi$ and the chain $n \leq \Phi(H) \leq 13$.)*
18. Contrapositive: if $n \geq 14$ then $H = H^{*}(\mathrm{INT}_n) \geq 3$.
19. By Part 1, $\deg_{\pm}(\mathrm{INT}_n) = 2$. Therefore for every $n \geq 14$,
    $$
    \deg_{\pm}(\mathrm{INT}_n) = 2 < 3 \leq H^{*}(\mathrm{INT}_n),
    $$
    an explicit Boolean function on $2n \geq 28$ bits whose head complexity strictly exceeds its threshold degree. $\blacksquare$

## Pitfalls to address explicitly

- In Step 10, the factorization yields a **homogeneous** inner product (no additive constant); Step 13 must use homogeneous halfspaces (functionals through the origin), whose shattering bound is $n \leq r$ (not $n \leq r+1$). The proof of Step 13 must not silently assume an affine separator.
- In Step 13, handle the sign bookkeeping for all three cases $c_i > 0$, $c_i < 0$, $c_i = 0$, and justify why $P$ can be taken nonempty (replace $c$ by $-c$ if necessary; $c \neq 0$ guarantees $P \cup \lbrace i : c_i < 0\rbrace \neq \emptyset$).
- The constant in L22 is exactly $(H+1)2^H + 1$; the threshold $n \geq 14$ comes from $\Phi(2) = 13$. Do not weaken it.
- Sign-representation is strict ($R[x,y] \neq 0$); this is what makes every term in Step 13 strictly signed.
- The result is a separation between $\deg_{\pm}$ and $H^{*}$ of the **same** function; it does not assert anything about positivity (tChow) beyond what L22 gives.
