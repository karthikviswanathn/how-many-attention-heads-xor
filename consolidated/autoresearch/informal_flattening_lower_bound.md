# Problem: A sign-rank (flattening) lower bound on head complexity

## Background and definitions (self-contained)

Fix $n \geq 1$, work on $\{0,1\}^n$. For $\alpha>0$, $b\in\{0,1\}$: $\alpha^0=1$, $\alpha^1=\alpha$. A function $A(x) = a_0 + \sum_i a_i x_i$ is **affine**.

A **one-head atom** is $\phi(x) = \dfrac{\eta + \sum_i \rho_i\alpha^{x_i}(m_i+\delta x_i)}{\gamma + \sum_i \rho_i\alpha^{x_i}}$ with $\gamma>0,\rho_i>0,\alpha>0$.

**Established results you may cite and use as given:**

- **(Atom fact.)** Every one-head atom equals $N/D$ with $N, D$ affine and $D > 0$ on the cube. (Expand $\alpha^{x_i} = 1+(\alpha-1)x_i$.)
- **(Normal form.)** $H^{*}(f)$ is the least $H$ such that, for some one-head atoms $\phi_1,\dots,\phi_H$ and $c \in \mathbb{R}$, $f(x)=1 \iff c+\sum_h \phi_h(x) > 0$ for all $x$.

**Bipartition and matrices.** Fix a partition of the coordinate set $\{1,\dots,n\}$ into two disjoint blocks $A$ and $B$. Identify $x \in \{0,1\}^n$ with a pair $(u,v)$, $u \in \{0,1\}^A$, $v \in \{0,1\}^B$. For $g : \{0,1\}^n \to \mathbb{R}$, its **$A|B$ matrix** $M_g$ is the real matrix indexed by $(u,v)$ with $M_g[u,v] = g(u,v)$. Write $\mathrm{rank}$ for real matrix rank, and $\circ$ for the entrywise (Hadamard) product of equally-shaped matrices.

**Sign-rank.** Define $\mathrm{sr}_{A|B}(f)$ as the least rank of a real matrix $R$ (indexed by $(u,v)$) such that $R[u,v] > 0$ whenever $f(u,v)=1$ and $R[u,v] < 0$ whenever $f(u,v)=0$ (so $R$ is nowhere zero and its entrywise sign matches $2f-1$).

## Claim to prove

For every $f : \{0,1\}^n \to \{0,1\}$ and every bipartition $A | B$,

$$
\mathrm{sr}_{A|B}(f) \;\leq\; \big(H^{*}(f)+1\big)\,2^{H^{*}(f)} + 1 .
$$

Consequently $H^{*}(f) \geq \log_2 \mathrm{sr}_{A|B}(f) - \log_2\big(H^{*}(f)+1\big) - 1$; in particular $H^{*}(f) = \Omega\big(\log \mathrm{sr}_{A|B}(f)\big)$. This lower bound does not pass through the threshold degree.

## Guidance (prove every step rigorously)

Let $H = H^{*}(f)$.

1. **A cleared-denominator sign representation.** By the normal form and the atom fact, write $\phi_h = N_h/D_h$ ($N_h, D_h$ affine, $D_h > 0$ on the cube) and $f(x)=1 \iff c + \sum_h N_h/D_h > 0$. Multiplying by $\prod_g D_g > 0$ (sign-faithful), the polynomial
   $$ P(x) = c\prod_{h=1}^H D_h(x) + \sum_{h=1}^H N_h(x)\prod_{g\neq h} D_g(x) $$
   satisfies $f(x)=1 \iff P(x) > 0$ for all $x$.

2. **Affine forms have $A|B$ rank $\leq 2$.** For affine $L(x) = \ell_0 + \sum_i \ell_i x_i$, split the sum over $A$ and $B$: $L(u,v) = \big(\ell_0 + \sum_{i\in A}\ell_i u_i\big) + \big(\sum_{i\in B}\ell_i v_i\big) = \varphi(u) + \psi(v)$. Hence $M_L = \varphi\,\mathbf{1}^\top + \mathbf{1}\,\psi^\top$ (with $\mathbf 1$ the all-ones vector of the appropriate size), a sum of two rank-$\leq 1$ matrices, so $\mathrm{rank}(M_L) \leq 2$.

3. **Hadamard rank submultiplicativity.** Prove: for matrices $M, M'$ of the same shape, $\mathrm{rank}(M \circ M') \leq \mathrm{rank}(M)\,\mathrm{rank}(M')$. (Write $M = \sum_{p=1}^{r} a_p b_p^\top$ and $M' = \sum_{q=1}^{r'} c_q d_q^\top$; then $M \circ M' = \sum_{p,q}(a_p \circ c_q)(b_p \circ d_q)^\top$, a sum of $rr'$ rank-$\leq 1$ matrices.) Note also that for a product of functions $g\cdot g'$, $M_{g g'} = M_g \circ M_{g'}$ entrywise.

4. **Rank of each term.** Using Steps 2 and 3: $M_{\prod_h D_h} = M_{D_1}\circ\cdots\circ M_{D_H}$ has rank $\leq 2^H$; and for each $h$, $M_{N_h \prod_{g\neq h}D_g}$ has rank $\leq \mathrm{rank}(M_{N_h})\prod_{g\neq h}\mathrm{rank}(M_{D_g}) \leq 2\cdot 2^{H-1} = 2^H$.

5. **Rank of $P$.** $M_P = c\,M_{\prod_h D_h} + \sum_h M_{N_h\prod_{g\neq h}D_g}$ is a sum of $H+1$ matrices each of rank $\leq 2^H$, so by subadditivity of rank, $\mathrm{rank}(M_P) \leq (H+1)2^H$.

6. **Make it strictly sign-representing.** $P > 0$ exactly on $f^{-1}(1)$, and $P \leq 0$ on $f^{-1}(0)$ (where it might be $0$). If $f$ is constant, $\mathrm{sr}_{A|B}(f) = 1 \leq (H+1)2^H + 1$ and we are done. Otherwise let $p_+ := \min\{P(x): f(x)=1\} > 0$, pick $\nu \in (0, p_+)$, and set $R := M_P - \nu J$ where $J$ is the all-ones matrix (rank $1$). Then $R[u,v] = P(u,v) - \nu$ is $> 0$ on $f^{-1}(1)$ (since $P \geq p_+ > \nu$) and $< 0$ on $f^{-1}(0)$ (since $P \leq 0$). So $R$ strictly sign-represents $f$, and $\mathrm{rank}(R) \leq \mathrm{rank}(M_P) + 1 \leq (H+1)2^H + 1$.

7. **Conclude.** $\mathrm{sr}_{A|B}(f) \leq \mathrm{rank}(R) \leq (H+1)2^H + 1$. Rearranging gives the stated logarithmic lower bound on $H = H^{*}(f)$.

Give a complete, rigorous proof, including the Hadamard submultiplicativity lemma.
