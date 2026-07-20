# Two-Polarity Sparse Threshold-Density Upper Bound

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), and let $H^{\ast}(f)$ be the least number of attention heads needed to compute $f : \{0,1\}^{n} \to \{0,1\}$ with a final strict threshold at the query token.

Let $s\geq 0$. For each $r\in\{1,\ldots,s\}$, fix a nonempty coordinate set $A_r\subseteq\{1,\ldots,n\}$ and a polarity $\zeta_r\in\{0,1\}$. Define

$$
I_r(x):=\mathbf{1}\left[x_i=\zeta_r\text{ for every }i\in A_r\right].
$$

Suppose there are real numbers $\theta,c_1,\ldots,c_s$ such that

$$
f(x)=\mathbf{1}\left[\theta+\sum_{r=1}^{s}c_r I_r(x)>0\right]
$$

for every $x\in\{0,1\}^{n}$, with positive margin on the Boolean cube, meaning

$$
\theta+\sum_{r=1}^{s}c_r I_r(x)\neq 0
\qquad \text{for every }x\in\{0,1\}^{n}.
$$

Then

$$
H^{\ast}(f)\leq s.
$$

> **Equivalently.** Every strict signed threshold of $s$ coordinate-subcube indicators, where each term is anchored either at $\vec 0$ or at $\vec 1$, is computable with at most one head per subcube. The polarity may vary with $r$, but all literals inside a single term have the same polarity.

## Proof

Let

$$
Q:=\{0,1\}^{n},
\qquad
T(x):=\theta+\sum_{r=1}^{s}c_rI_r(x).
$$

The proof is the construction of Lemma 18 with a violation indicator indexed by the term $r$. We give the details because the polarity now varies from term to term.

Since $T(x)\neq 0$ for every $x\in Q$ and $Q$ is finite, define

$$
\mu:=\min_{x\in Q}|T(x)|>0.
$$

By Lemma 10, it is enough to construct one-head atoms $\phi_1,\ldots,\phi_s$ such that the strict threshold of

$$
S(x):=\theta+\sum_{r=1}^{s}\phi_r(x)
$$

agrees with the strict threshold of $T$ on $Q$.

If $s=0$, then $T(x)=\theta$ for every $x\in Q$. Since $\mu=|\theta|>0$, the sign of $T$ is constant on $Q$. The zero-head case of Lemma 10 computes this constant function, so $H^{\ast}(f)=0\leq s$. Thus assume $s\geq 1$. Since $A_1$ is nonempty, $n\geq 1$.

For every $r\in\{1,\ldots,s\}$ and $i\in\{1,\ldots,n\}$, define

$$
\nu_{r,i}(x):=
\begin{cases}
x_i, & \zeta_r=0,\\
1-x_i, & \zeta_r=1.
\end{cases}
$$

Then $\nu_{r,i}(x)\in\{0,1\}$, and

$$
\nu_{r,i}(x)=0
\quad\Longleftrightarrow\quad
x_i=\zeta_r.
$$

For each $r$, set

$$
V_r(x):=\sum_{i\in A_r}\nu_{r,i}(x).
$$

Because $V_r(x)$ is a sum of Boolean violation indicators,

$$
I_r(x)=1 \Longleftrightarrow V_r(x)=0,
\qquad
I_r(x)=0 \Longrightarrow V_r(x)\geq 1.
$$

Set

$$
B:=\sum_{r=1}^{s}|c_r|,
\qquad
\varepsilon:=\frac{\mu}{4(B+1)}.
$$

Then $\varepsilon>0$. Choose

$$
\Lambda:=\varepsilon^{-1}+1,
\qquad
\kappa:=\frac{\varepsilon}{2n}.
$$

Since $n\geq 1$,

$$
\frac{1}{1+\Lambda}<\varepsilon,
\qquad
\kappa n=\frac{\varepsilon}{2}<\varepsilon.
$$

For every $r$ and $i$, define

$$
\beta_{r,i}:=
\begin{cases}
\Lambda, & i\in A_r,\\
\kappa, & i\notin A_r.
\end{cases}
$$

Also define

$$
D_r(x):=1+\sum_{i=1}^{n}\beta_{r,i}\nu_{r,i}(x),
\qquad
\phi_r(x):=\frac{c_r}{D_r(x)}.
$$

Every $\beta_{r,i}$ is positive and every $\nu_{r,i}(x)$ is nonnegative, so $D_r(x)\geq 1$ on $Q$.

### Lemma 1. Reciprocal bump atoms

**Claim.** For every $r$, the function $\phi_r$ is a valid one-head atom.

**Proof.** Fix $r$ and write

$$
S_r:=\sum_{i=1}^{n}\beta_{r,i}>0.
$$

First suppose $\zeta_r=0$. Then

$$
D_r(x)=1+\sum_{i=1}^{n}\beta_{r,i}x_i.
$$

Choose

$$
\alpha_r:=1+2S_r,
\qquad
\rho_{r,i}:=\frac{\beta_{r,i}}{2S_r},
\qquad
\gamma_r:=\frac{1}{2},
\qquad
\eta_r:=c_r,
\qquad
m_{r,i}:=0,
\qquad
\delta_r:=0.
$$

Then $\alpha_r>0$, $\rho_{r,i}>0$, and $\gamma_r>0$. For Boolean $x_i$,

$$
\alpha_r^{x_i}=1+(\alpha_r-1)x_i.
$$

Therefore

$$
\begin{aligned}
\gamma_r+\sum_i\rho_{r,i}\alpha_r^{x_i}
&=\frac{1}{2}+\sum_i\frac{\beta_{r,i}}{2S_r}\left(1+2S_rx_i\right) \\
&=\frac{1}{2}+\frac{1}{2S_r}\sum_i\beta_{r,i}+\sum_i\beta_{r,i}x_i \\
&=1+\sum_i\beta_{r,i}x_i \\
&=D_r(x).
\end{aligned}
$$

The numerator is $c_r$ because $\eta_r=c_r$, $m_{r,i}=0$, and $\delta_r=0$.

Now suppose $\zeta_r=1$. Then

$$
D_r(x)=1+\sum_i\beta_{r,i}(1-x_i)=1+S_r-\sum_i\beta_{r,i}x_i.
$$

Choose

$$
\alpha_r:=\frac{1}{2(1+S_r)},
\qquad
\rho_{r,i}:=\frac{\beta_{r,i}}{1-\alpha_r},
\qquad
\gamma_r:=\frac{1+S_r}{1+2S_r},
\qquad
\eta_r:=c_r,
\qquad
m_{r,i}:=0,
\qquad
\delta_r:=0.
$$

Then $0<\alpha_r<1$, $\rho_{r,i}>0$, and $\gamma_r>0$. Also

$$
1-\alpha_r=\frac{1+2S_r}{2(1+S_r)},
$$

so

$$
\gamma_r+\sum_i\rho_{r,i}=1+S_r,
\qquad
\rho_{r,i}(\alpha_r-1)=-\beta_{r,i}.
$$

Therefore

$$
\begin{aligned}
\gamma_r+\sum_i\rho_{r,i}\alpha_r^{x_i}
&=\gamma_r+\sum_i\rho_{r,i}\left(1+(\alpha_r-1)x_i\right) \\
&=1+S_r-\sum_i\beta_{r,i}x_i \\
&=D_r(x).
\end{aligned}
$$

Again the numerator is $c_r$. Thus $\phi_r=c_r/D_r$ has the one-head atom form from Lemma 10. The two cases realize the all-positive and all-negative affine denominator classes isolated in Lemma 13. $\blacksquare$

### Lemma 2. Approximation of each indicator

**Claim.** For every $r$ and every $x\in Q$,

$$
|\phi_r(x)-c_rI_r(x)|\leq |c_r|\varepsilon.
$$

**Proof.** Define

$$
W_r(x):=\sum_{i\notin A_r}\nu_{r,i}(x).
$$

Then

$$
D_r(x)=1+\Lambda V_r(x)+\kappa W_r(x).
$$

If $I_r(x)=1$, then $V_r(x)=0$. Since $0\leq W_r(x)\leq n$,

$$
1\leq D_r(x)=1+\kappa W_r(x)\leq 1+\kappa n<1+\varepsilon.
$$

Hence

$$
\begin{aligned}
|\phi_r(x)-c_rI_r(x)|
&=\left|\frac{c_r}{D_r(x)}-c_r\right| \\
&=|c_r|\frac{D_r(x)-1}{D_r(x)} \\
&\leq |c_r|\varepsilon.
\end{aligned}
$$

If $I_r(x)=0$, then $V_r(x)\geq 1$. Therefore

$$
D_r(x)\geq 1+\Lambda,
$$

and so

$$
|\phi_r(x)-c_rI_r(x)|=\left|\frac{c_r}{D_r(x)}\right|\leq \frac{|c_r|}{1+\Lambda}<|c_r|\varepsilon.
$$

The two cases prove the claim. $\blacksquare$

### Lemma 3. Strict sign preservation

**Claim.** For every $x\in Q$,

$$
f(x)=1 \Longleftrightarrow S(x)>0.
$$

**Proof.** By Lemma 2 and the triangle inequality,

$$
\begin{aligned}
|S(x)-T(x)|
&=\left|\sum_{r=1}^{s}\phi_r(x)-\sum_{r=1}^{s}c_rI_r(x)\right| \\
&\leq \sum_{r=1}^{s}|c_r|\varepsilon \\
&=B\varepsilon \\
&=\frac{\mu B}{4(B+1)} \\
&<\frac{\mu}{4}.
\end{aligned}
$$

Since $\mu=\min_{x\in Q}|T(x)|$, we have $|T(x)|\geq\mu$ for every $x\in Q$.

If $f(x)=1$, then $T(x)>0$, hence $T(x)\geq\mu$. Thus

$$
S(x)\geq T(x)-|S(x)-T(x)|>\mu-\frac{\mu}{4}=\frac{3\mu}{4}>0.
$$

If $f(x)=0$, the strict-threshold hypothesis gives $T(x)\leq 0$. Since $T(x)\neq 0$ and $|T(x)|\geq\mu$, this implies $T(x)\leq -\mu$. Thus

$$
S(x)\leq T(x)+|S(x)-T(x)|<-\mu+\frac{\mu}{4}=-\frac{3\mu}{4}<0.
$$

Therefore $f(x)=1$ if and only if $S(x)>0$. $\blacksquare$

### Conclusion

The score $S$ is the constant $\theta$ plus a sum of the $s$ one-head atoms $\phi_1,\ldots,\phi_s$. By Lemma 10, the one-layer attention model computes $f$ with at most $s$ heads. Hence

$$
H^{\ast}(f)\leq s.
$$

$\blacksquare$

## Consequence

Head complexity is at most two-polarity sparse threshold density for coordinate subcubes anchored termwise at $\vec 0$ or $\vec 1$. In particular, taking $\theta=-1/2$ and $c_r=1$ for all $r$ shows that a DNF whose terms are such same-literal-polarity coordinate subcubes satisfies $H^{\ast}(f)\leq s$.

This does not cover general subcubes with mixed literal polarities inside a single term.
