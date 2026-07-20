# Problem: Positivity is free at level one (tChow and H* agree below 2)

## Background and definitions (self-contained)

Fix $n\geq 1$, work on $\{0,1\}^n$. An **affine** function is $A(x)=a_0+\sum_i a_i x_i$. $f$ is a **linear threshold function (LTF)** if $f(x)=\mathbf 1[A(x)>0]$ for some affine $A$.

**Tangential-Chow sign-rank.** $\mathrm{tChow}_{\pm}(f)$ is the least $H\geq 0$ for which there are arbitrary affine $N_1,D_1,\dots,N_H,D_H$ and $\theta\in\mathbb{R}$ with
$$ P(x)=\theta\prod_{h=1}^H D_h(x)+\sum_{h=1}^H N_h(x)\prod_{g\neq h}D_g(x) $$
sign-representing $f$ (for $H=0$, $P=\theta$; for $H=1$, $P=\theta D_1 + N_1$).

**Established result you may cite (L11).** $H^{*}(f)\leq 1$ if and only if $f$ is constant or an LTF. ($H^{*}(f)=0$ iff $f$ constant; $H^{*}(f)=1$ iff $f$ is a nonconstant LTF.) Also $\mathrm{tChow}_{\pm}(f)\leq H^{*}(f)$ for every $f$.

## Claim to prove

For every $f:\{0,1\}^n\to\{0,1\}$,

$$
\mathrm{tChow}_{\pm}(f)\leq 1 \iff H^{*}(f)\leq 1 \iff f \text{ is constant or an LTF}.
$$

Consequently $\mathrm{tChow}_{\pm}(f)=H^{*}(f)$ whenever either side is $\leq 1$: **the attention positivity/one-sided-slope constraints cost nothing at level one** (the base case of the question whether $\mathrm{tChow}_{\pm}=H^{*}$ in general).

## Guidance (prove every step rigorously)

1. **$H^{*}(f)\leq 1 \iff f$ constant or LTF.** This is L11; cite it.

2. **$\mathrm{tChow}_{\pm}(f)\leq 1 \Rightarrow f$ constant or LTF.** If $\mathrm{tChow}_{\pm}(f)=0$, then $P=\theta$ is constant, so $f$ is constant. If $\mathrm{tChow}_{\pm}(f)=1$, then $P(x)=\theta D_1(x)+N_1(x)$ with $D_1,N_1$ affine; $P$ is itself affine (sum of scalar-times-affine and affine), and $f(x)=1\iff P(x)>0$, so $f$ is an LTF (or constant if $P$ is constant).

3. **$f$ constant or LTF $\Rightarrow \mathrm{tChow}_{\pm}(f)\leq 1$.** If $f$ is constant, take $H=0$, $P=\theta$ with the correct sign. If $f$ is an LTF, $f(x)=\mathbf 1[A(x)>0]$ for affine $A$; take $H=1$, $D_1\equiv 1$ (constant affine), $N_1=A$, $\theta=0$, so $P=\theta D_1+N_1 = A$ sign-represents $f$. Hence $\mathrm{tChow}_{\pm}(f)\leq 1$.

4. **Conclude the equivalences**, and that $\mathrm{tChow}_{\pm}(f)=H^{*}(f)$ when either is $\leq 1$: both equal $0$ for constants and $1$ for nonconstant LTFs (using $\mathrm{tChow}_{\pm}\leq H^{*}$ and the equivalences to pin the exact value).

Give a complete, rigorous proof.
