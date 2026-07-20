# Flattening (Sign-Rank) Lower Bound

## Statement

Fix a bipartition of the coordinates $\lbrace 1,\dots,n\rbrace = A \sqcup B$ and identify $x$ with $(u,v)$, $u \in \lbrace 0,1\rbrace^A$, $v \in \lbrace 0,1\rbrace^B$. For $g : \lbrace 0,1\rbrace^n \to \mathbb{R}$ let $M_g$ be the real matrix $M_g[u,v] = g(u,v)$. Let $\mathrm{sr}_{A|B}(f)$ be the least rank of a real matrix $R$ with $R[u,v] > 0$ when $f(u,v)=1$ and $R[u,v] < 0$ when $f(u,v)=0$ (a strict sign-representation of $f$ across the cut).

**Theorem.** For every $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$ and every bipartition $A|B$,

$$
\mathrm{sr}_{A|B}(f) \;\leq\; \big(H^{*}(f)+1\big)\,2^{H^{*}(f)} + 1 .
$$

Equivalently,

$$
H^{*}(f) \;=\; \Omega\big(\log \mathrm{sr}_{A|B}(f)\big).
$$

> **The first $H^{*}$ lower bound that does not pass through threshold degree.** It also lower-bounds $\mathrm{tChow}_{\pm}(f)$ (the proof never uses positivity), and it is computable: any cut $A|B$ with large sign-rank certifies a large head complexity. Since a degree-$d$ sign-representation gives sign-rank at most $\binom{n}{\leq d} = n^{O(d)}$, any $f$ whose sign-rank exceeds $\mathrm{poly}(n)$ while $\deg_{\pm}(f) = O(1)$ already has $H^{*}(f) = \omega(1)$ with $\deg_{\pm}(f)$ bounded: a separation of $H^{*}$ from threshold degree.

## Proof

Let $H = H^{*}(f)$; all logarithms are base $2$.

### A cleared-denominator sign representation

By the normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md) and the atom dictionary [013_atom_dictionary.md](../01_foundations_and_normal_form/013_atom_dictionary.md), write $\phi_h = N_h/D_h$ ($N_h,D_h$ affine, $D_h > 0$ on the cube) with $f(x) = 1 \iff c + \sum_h N_h/D_h > 0$. Multiplying by $\prod_g D_g > 0$ (sign-faithful), the polynomial

$$
P(x) = c\prod_{h=1}^H D_h(x) + \sum_{h=1}^H N_h(x)\prod_{g\neq h}D_g(x)
$$

satisfies $f(x) = 1 \iff P(x) > 0$.

### Affine forms have cut-rank at most 2

For affine $L(x) = \ell_0 + \sum_i \ell_i x_i$, split over $A,B$: $L(u,v) = \varphi(u) + \psi(v)$ with $\varphi(u) = \ell_0 + \sum_{i\in A}\ell_i u_i$, $\psi(v) = \sum_{i\in B}\ell_i v_i$. Then $M_L = \varphi\,\mathbf 1_B^\top + \mathbf 1_A\,\psi^\top$, a sum of two rank-$\leq 1$ matrices, so $\mathrm{rank}(M_L) \leq 2$.

### Hadamard rank submultiplicativity

For same-shaped $M = \sum_{p=1}^r a_p b_p^\top$, $M' = \sum_{q=1}^{r'} c_q d_q^\top$, the entrywise product is $M \circ M' = \sum_{p,q}(a_p \circ c_q)(b_p \circ d_q)^\top$, a sum of $rr'$ rank-$\leq 1$ matrices, so $\mathrm{rank}(M \circ M') \leq \mathrm{rank}(M)\,\mathrm{rank}(M')$. Also $M_{gg'} = M_g \circ M_{g'}$ entrywise.

### Rank of the cleared polynomial's matrix

By the two facts above, $M_{\prod_h D_h} = M_{D_1}\circ\cdots\circ M_{D_H}$ has rank $\leq 2^H$, and each $M_{N_h\prod_{g\neq h}D_g}$ has rank $\leq 2\cdot 2^{H-1} = 2^H$. Since $M_P = c\,M_{\prod_h D_h} + \sum_h M_{N_h\prod_{g\neq h}D_g}$ is a sum of $H+1$ matrices each of rank $\leq 2^H$, subadditivity gives $\mathrm{rank}(M_P) \leq (H+1)2^H$.

### Strict sign representation

If $f$ is constant, $\mathrm{sr}_{A|B}(f) = 1 \leq (H+1)2^H + 1$. Otherwise let $p_+ = \min\lbrace P(x) : f(x)=1\rbrace > 0$, pick $\nu \in (0, p_+)$, and set $R = M_P - \nu J$ ($J$ all-ones, rank $1$). On $f^{-1}(1)$, $R = P - \nu \geq p_+ - \nu > 0$; on $f^{-1}(0)$, $P \leq 0$ so $R \leq -\nu < 0$. Thus $R$ strictly sign-represents $f$, and $\mathrm{rank}(R) \leq \mathrm{rank}(M_P) + 1 \leq (H+1)2^H + 1$. Hence $\mathrm{sr}_{A|B}(f) \leq (H+1)2^H + 1$.

### Logarithmic form

Since $(H+1)2^H \geq 1$, $\mathrm{sr}_{A|B}(f) \leq 2(H+1)2^H$, so $\log \mathrm{sr}_{A|B}(f) \leq H + \log(H+1) + 1$, giving $H \geq \log \mathrm{sr}_{A|B}(f) - \log(H+1) - 1 = \Omega(\log \mathrm{sr}_{A|B}(f))$. $\blacksquare$

## Consequence

This is the lower-bound counterpart to the upper-bound toolkit: head complexity is bounded below by the cut sign-rank (logarithmically) and above by single-polarity threshold density and weighted-sum image size. It is the first tool able to certify $H^{*}(f) > \deg_{\pm}(f)$, since sign-rank can be super-polynomial in the threshold-degree monomial count. The Warren counting bound (in `BLUEPRINT.md`) pushes the separation from logarithmic to linear for some degree-2 functions.
