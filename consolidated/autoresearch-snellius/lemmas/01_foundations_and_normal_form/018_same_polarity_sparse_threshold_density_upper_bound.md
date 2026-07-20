# Same-Polarity Sparse Threshold-Density Upper Bound

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), and let $H^{\ast}(f)$ be the least number of attention heads needed to compute $f : \{0,1\}^{n} \to \{0,1\}$ with a final strict threshold at the query token.

Fix a polarity $\zeta\in\{0,1\}$. Let $s\geq 0$, and let $A_1,\ldots,A_s\subseteq\{1,\ldots,n\}$ be nonempty coordinate sets. For each $r$, define

$$
q_r(x)=\mathbf{1}[x_i=\zeta\text{ for every }i\in A_r].
$$

Suppose there are real numbers $\theta,c_1,\ldots,c_s$ such that

$$
f(x)=1 \Longleftrightarrow \theta+\sum_{r=1}^{s} c_r q_r(x)>0
$$

for every $x\in\{0,1\}^n$, with positive margin

$$
\mu=\min_{x\in\{0,1\}^n}\left|\theta+\sum_{r=1}^{s}c_r q_r(x)\right|>0.
$$

Then

$$
H^{\ast}(f)\leq s.
$$

> **Equivalently.** Every strict linear threshold of $s$ coordinate-subcube indicators anchored at one Boolean vertex is computable with at most one head per subcube.

## Proof

Let

$$
Q:=\{0,1\}^{n},
\qquad
T(x):=\theta+\sum_{r=1}^{s}c_rq_r(x).
$$

By Lemma 10, it is enough to construct $s$ one-head atoms $\phi_1,\ldots,\phi_s$ such that the strict threshold of

$$
S(x):=\theta+\sum_{r=1}^{s}\phi_r(x)
$$

agrees with the strict threshold of $T$ on $Q$.

If $s=0$, then $T(x)=\theta$ for every $x$. Since $\mu=|\theta|>0$, the sign of $T$ is constant on $Q$. The zero-head case of Lemma 10 computes this constant function, so $H^{\ast}(f)=0\leq s$. Thus assume $s\geq 1$. Since each $A_r$ is nonempty, $n\geq 1$.

For each coordinate, define the violation indicator

$$
\nu_i(x)=
\begin{cases}
x_i, & \zeta=0,\\
1-x_i, & \zeta=1.
\end{cases}
$$

Then $\nu_i(x)\in\{0,1\}$, and $\nu_i(x)=0$ if and only if $x_i=\zeta$. For each $r$, set

$$
V_r(x):=\sum_{i\in A_r}\nu_i(x).
$$

Because $V_r(x)$ is a sum of Boolean violation indicators,

$$
q_r(x)=1 \Longleftrightarrow V_r(x)=0,
\qquad
q_r(x)=0 \Longrightarrow V_r(x)\geq 1.
$$

Set

$$
B:=\sum_{r=1}^{s}|c_r|,
\qquad
\varepsilon:=\frac{\mu}{4(B+1)}.
$$

Then $\varepsilon>0$. Choose real numbers $\Lambda$ and $\kappa$ such that

$$
\Lambda>\max\{0,\varepsilon^{-1}-1\},
\qquad
0<\kappa<\frac{\varepsilon}{n}.
$$

Hence

$$
\frac{1}{1+\Lambda}<\varepsilon,
\qquad
\kappa n<\varepsilon.
$$

For each $r$ and $i$, define

$$
\beta_{r,i}:=
\begin{cases}
\Lambda, & i\in A_r,\\
\kappa, & i\notin A_r,
\end{cases}
$$

and

$$
D_r(x):=1+\sum_{i=1}^{n}\beta_{r,i}\nu_i(x),
\qquad
\phi_r(x):=\frac{c_r}{D_r(x)}.
$$

Every $\beta_{r,i}$ is positive and every $\nu_i(x)$ is nonnegative, so $D_r(x)\geq 1$ on $Q$.

### Lemma 1. The fractions are one-head atoms

**Claim.** For every $r$, the function $\phi_r$ is a valid one-head atom.

**Proof.** Fix $r$ and write

$$
S_r:=\sum_{i=1}^{n}\beta_{r,i}>0.
$$

First suppose $\zeta=0$. Then

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

Using $\alpha_r^{x_i}=1+(\alpha_r-1)x_i$ on the Boolean cube,

$$
\begin{aligned}
\gamma_r+\sum_i\rho_{r,i}\alpha_r^{x_i}
&=\frac{1}{2}+\sum_i\frac{\beta_{r,i}}{2S_r}\left(1+2S_r x_i\right) \\
&=1+\sum_i\beta_{r,i}x_i \\
&=D_r(x).
\end{aligned}
$$

The numerator is $c_r$ because $m_{r,i}=0$ and $\delta_r=0$.

Now suppose $\zeta=1$. Then

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

Again the numerator is $c_r$. Thus $\phi_r=c_r/D_r$ is a one-head atom in both polarity cases. $\blacksquare$

### Lemma 2. Each atom approximates its subcube indicator

**Claim.** For every $r$ and every $x\in Q$,

$$
|\phi_r(x)-c_rq_r(x)|\leq |c_r|\varepsilon.
$$

**Proof.** Define

$$
W_r(x):=\sum_{i\notin A_r}\nu_i(x).
$$

Then

$$
D_r(x)=1+\Lambda V_r(x)+\kappa W_r(x).
$$

If $q_r(x)=1$, then $V_r(x)=0$. Since $0\leq W_r(x)\leq n$,

$$
1\leq D_r(x)=1+\kappa W_r(x)\leq 1+\kappa n<1+\varepsilon.
$$

Hence

$$
\begin{aligned}
|\phi_r(x)-c_rq_r(x)|
&=\left|\frac{c_r}{D_r(x)}-c_r\right| \\
&=|c_r|\frac{D_r(x)-1}{D_r(x)} \\
&\leq |c_r|\varepsilon.
\end{aligned}
$$

If $q_r(x)=0$, then $V_r(x)\geq 1$. Therefore

$$
D_r(x)\geq 1+\Lambda,
$$

and so

$$
|\phi_r(x)-c_rq_r(x)|=\left|\frac{c_r}{D_r(x)}\right|\leq \frac{|c_r|}{1+\Lambda}<|c_r|\varepsilon.
$$

The two cases prove the claim. $\blacksquare$

### Lemma 3. The strict signs are preserved

**Claim.** For every $x\in Q$,

$$
f(x)=1 \Longleftrightarrow S(x)>0.
$$

**Proof.** By Lemma 2 and the triangle inequality,

$$
\begin{aligned}
|S(x)-T(x)|
&=\left|\sum_{r=1}^{s}\phi_r(x)-\sum_{r=1}^{s}c_rq_r(x)\right| \\
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

If $f(x)=0$, the strict-threshold hypothesis gives $T(x)\leq 0$. Since $|T(x)|\geq\mu$, this implies $T(x)\leq -\mu$. Thus

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

For a fixed polarity $\zeta$, head complexity is at most same-polarity subcube-threshold density. In particular, any strict signed threshold of $s$ coordinate-subcube indicators anchored at the same Boolean vertex has an $s$-head construction, with one calibrated reciprocal bump atom per subcube.
