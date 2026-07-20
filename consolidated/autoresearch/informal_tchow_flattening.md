# Problem: The flattening sign-rank bound holds for the positivity-free invariant

## Background and definitions (self-contained)

Fix $n\geq 1$, work on $\{0,1\}^n$. An **affine** function is $A(x)=a_0+\sum_i a_i x_i$. Fix a bipartition $A|B$ of the coordinates; identify $x$ with $(u,v)$, and for $g:\{0,1\}^n\to\mathbb{R}$ let $M_g[u,v]=g(u,v)$ be its $A|B$ matrix. Let $\mathrm{sr}_{A|B}(f)$ be the least rank of a real matrix $R$ with $R[u,v]>0$ when $f(u,v)=1$ and $R[u,v]<0$ when $f(u,v)=0$ (a strict sign-representation across the cut).

**Tangential-Chow sign-rank.** $\mathrm{tChow}_{\pm}(f)$ is the least $H\geq 0$ for which there exist *arbitrary* affine functions $N_1,D_1,\dots,N_H,D_H$ and $\theta\in\mathbb{R}$ such that
$$ P(x)=\theta\prod_{h=1}^H D_h(x)+\sum_{h=1}^H N_h(x)\prod_{g\neq h}D_g(x) $$
sign-represents $f$ (i.e. $f(x)=1\iff P(x)>0$). (No positivity or sign constraints on the $D_h$.)

**Established facts you may cite and use:**
- For an affine $L$, its $A|B$ matrix $M_L$ has rank $\leq 2$ (split $L(u,v)=\varphi(u)+\psi(v)$, so $M_L=\varphi\mathbf 1^\top+\mathbf 1\psi^\top$).
- Hadamard rank submultiplicativity: $\mathrm{rank}(M\circ M')\leq \mathrm{rank}(M)\mathrm{rank}(M')$, and $M_{gg'}=M_g\circ M_{g'}$.

## Claim to prove

For every $f:\{0,1\}^n\to\{0,1\}$ and every bipartition $A|B$,
$$ \mathrm{sr}_{A|B}(f) \leq \big(\mathrm{tChow}_{\pm}(f)+1\big)\,2^{\mathrm{tChow}_{\pm}(f)} + 1, $$
hence $\mathrm{tChow}_{\pm}(f)=\Omega\big(\log \mathrm{sr}_{A|B}(f)\big)$.

> The flattening / sign-rank lower bound is not specific to head complexity: it bounds the unconstrained tangential-Chow rank too (the argument never uses positivity of the $D_h$). So, like the counting separation, the sign-rank obstruction does not need the attention positivity/one-sided constraints. Combined with $\mathrm{tChow}_{\pm}(f)\leq H^{*}(f)$, this re-proves $H^{*}(f)=\Omega(\log\mathrm{sr}_{A|B}(f))$.

## Guidance (prove every step rigorously)

Let $H=\mathrm{tChow}_{\pm}(f)$, with witnesses $N_h,D_h$ (affine), $\theta$, and $P$ sign-representing $f$. All logs base $2$.

1. **Rank of $P$'s matrix.** Each $D_h, N_h$ is affine, so $M_{D_h}, M_{N_h}$ have rank $\leq 2$. By Hadamard submultiplicativity, $M_{\prod_h D_h}=M_{D_1}\circ\cdots\circ M_{D_H}$ has rank $\leq 2^H$, and each $M_{N_h\prod_{g\neq h}D_g}$ has rank $\leq 2\cdot 2^{H-1}=2^H$. Since $M_P=\theta M_{\prod_h D_h}+\sum_h M_{N_h\prod_{g\neq h}D_g}$ is a sum of $H+1$ matrices of rank $\leq 2^H$, $\mathrm{rank}(M_P)\leq (H+1)2^H$.

2. **Strict sign-representation.** If $f$ is constant, $\mathrm{sr}_{A|B}(f)=1\leq(H+1)2^H+1$. Otherwise let $p_+=\min\{P(x):f(x)=1\}>0$, pick $\nu\in(0,p_+)$, and set $R=M_P-\nu J$ ($J$ all-ones, rank $1$). On $f^{-1}(1)$, $R=P-\nu\geq p_+-\nu>0$; on $f^{-1}(0)$, $P\leq 0$ so $R\leq-\nu<0$. So $R$ strictly sign-represents $f$ and $\mathrm{rank}(R)\leq\mathrm{rank}(M_P)+1\leq(H+1)2^H+1$. Hence $\mathrm{sr}_{A|B}(f)\leq(H+1)2^H+1$.

3. **Logarithmic form.** Since $(H+1)2^H\geq 1$, $\mathrm{sr}_{A|B}(f)\leq 2(H+1)2^H$, so $\log\mathrm{sr}_{A|B}(f)\leq H+\log(H+1)+1$, giving $H=\Omega(\log\mathrm{sr}_{A|B}(f))$.

Give a complete, rigorous proof. (The proof is identical in form to the head-complexity flattening bound, with the single point that the polynomial $P$ here uses arbitrary affine $D_h$, and positivity is never invoked.)
