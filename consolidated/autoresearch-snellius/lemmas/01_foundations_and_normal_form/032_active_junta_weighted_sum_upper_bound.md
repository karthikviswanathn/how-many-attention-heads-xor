# Active-Junta Weighted-Sum Sign-Change Upper Bound

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), with a final strict threshold at the query token. Let $H^{\ast}(f)$ be the minimum number of attention heads needed to compute $f$.

Let $f : \{0,1\}^{n}\to\{0,1\}$ depend only on a coordinate set $I\subseteq\{1,\ldots,n\}$ with $|I|=k$. Thus there is a function $g:\{0,1\}^{I}\to\{0,1\}$ such that

$$
f(x)=g(x_I)
$$

for every $x\in\{0,1\}^{n}$.

Suppose there are positive weights $\lambda_i>0$ for $i\in I$, a statistic

$$
t_I(u)=\sum_{i\in I}\lambda_i u_i,
$$

and a function $G:\operatorname{Im}(t_I)\to\{0,1\}$ such that

$$
g(u)=G(t_I(u))
$$

for every $u\in\{0,1\}^{I}$. List the distinct values of $t_I$ as

$$
\tau_0<\tau_1<\cdots<\tau_{M-1}.
$$

Define

$$
\sigma_j=
\begin{cases}
+1, & \text{if } G(\tau_j)=1,\\
-1, & \text{if } G(\tau_j)=0,
\end{cases}
$$

and

$$
C_{t_I}(G)=\left|\left\{j\in\{1,\ldots,M-1\}:\sigma_{j-1}\neq\sigma_j\right\}\right|.
$$

Then

$$
H^{\ast}(f)\leq C_{t_I}(G).
$$

In particular, every $k$-junta satisfies

$$
H^{\ast}(f)\leq 2^k-1.
$$

## Proof

If $k=0$, then $I=\varnothing$, the active cube has one point, $t_I$ has one image value, and $C_{t_I}(G)=0$. The function $f$ is constant, so $H^{\ast}(f)=0$. The desired bound follows.

Assume from now on that $k\geq1$.

### Lemma 1. Active-coordinate relabeling

There is a function $h:\{0,1\}^{k}\to\{0,1\}$ and a positive weighted sum

$$
s(y)=\sum_{r=1}^{k}\mu_r y_r
$$

such that $h(y)=G(s(y))$ for every $y\in\{0,1\}^{k}$ and

$$
C_s(G)=C_{t_I}(G),
$$

where $C_s(G)$ is the sign-change count for $G$ along the ordered image of $s$.

**Proof.** Choose an enumeration

$$
I=\{i_1,\ldots,i_k\}.
$$

Define the relabeling map $R:\{0,1\}^{k}\to\{0,1\}^{I}$ by

$$
R(y)_{i_r}=y_r
\qquad
\text{for } r\in\{1,\ldots,k\}.
$$

Set

$$
h(y)=g(R(y)),
\qquad
\mu_r=\lambda_{i_r},
\qquad
s(y)=\sum_{r=1}^{k}\mu_r y_r.
$$

Since each $\lambda_i>0$, each $\mu_r>0$. Also $s(0,\ldots,0)=0$, so the normalization used in Lemma 30 is automatic.

For every $y\in\{0,1\}^{k}$,

$$
\begin{aligned}
s(y)
&=\sum_{r=1}^{k}\mu_r y_r \\
&=\sum_{r=1}^{k}\lambda_{i_r}y_r \\
&=\sum_{r=1}^{k}\lambda_{i_r}R(y)_{i_r} \\
&=t_I(R(y)).
\end{aligned}
$$

Therefore

$$
\begin{aligned}
h(y)
&=g(R(y)) \\
&=G(t_I(R(y))) \\
&=G(s(y)).
\end{aligned}
$$

The map $R$ is a bijection, since the enumeration of $I$ uses each active coordinate exactly once. Hence

$$
\operatorname{Im}(s)=\operatorname{Im}(t_I).
$$

Thus the ordered image values for $s$ are the same values $\tau_0<\tau_1<\cdots<\tau_{M-1}$, and the sign sequence used to compute $C_s(G)$ is exactly $\sigma_0,\ldots,\sigma_{M-1}$. Hence

$$
C_s(G)=C_{t_I}(G).
$$

This proves the lemma. $\blacksquare$

### Lemma 2. Active bound lifts to the ambient cube

For the function $h$ from Lemma 1,

$$
H^{\ast}(f)=H^{\ast}(h).
$$

**Proof.** Let $J=\{1,\ldots,n\}\setminus I$, and enumerate

$$
J=\{j_1,\ldots,j_{n-k}\}.
$$

Define the dummy-variable extension $\widetilde h:\{0,1\}^{n}\to\{0,1\}$ by

$$
\widetilde h(y_1,\ldots,y_k,z_1,\ldots,z_{n-k})=h(y_1,\ldots,y_k).
$$

By Lemma 31, adding dummy variables does not change head complexity, so

$$
H^{\ast}(\widetilde h)=H^{\ast}(h).
$$

Define the coordinate permutation $\pi:\{0,1\}^{n}\to\{0,1\}^{n}$ by

$$
\pi(x)=(x_{i_1},\ldots,x_{i_k},x_{j_1},\ldots,x_{j_{n-k}}).
$$

For every $x\in\{0,1\}^{n}$,

$$
\begin{aligned}
\widetilde h(\pi(x))
&=h(x_{i_1},\ldots,x_{i_k}) \\
&=g(x_I) \\
&=f(x).
\end{aligned}
$$

Thus $f=\widetilde h\circ\pi$. By the coordinate-permutation invariance in Lemma 31,

$$
H^{\ast}(f)=H^{\ast}(\widetilde h).
$$

Combining the two equalities gives

$$
H^{\ast}(f)=H^{\ast}(h).
$$

This proves the lemma. $\blacksquare$

### Conclusion

By Lemma 1, the function $h$ satisfies the hypotheses of Lemma 30 with positive weights $\mu_1,\ldots,\mu_k$, statistic $s$, and function $G$. Therefore

$$
H^{\ast}(h)\leq C_s(G).
$$

Using Lemma 1 and Lemma 2,

$$
H^{\ast}(f)=H^{\ast}(h)\leq C_s(G)=C_{t_I}(G).
$$

This proves the active-junta weighted-sum sign-change upper bound. $\blacksquare$

## Consequence

Let $f$ be any $k$-junta. Then there is a set $I\subseteq\{1,\ldots,n\}$ with $|I|=k$ and a function $g:\{0,1\}^{I}\to\{0,1\}$ such that $f(x)=g(x_I)$.

If $k=0$, then $f$ is constant, so

$$
H^{\ast}(f)=0=2^0-1.
$$

Assume $k\geq1$, and enumerate

$$
I=\{i_1,\ldots,i_k\}.
$$

Set

$$
\lambda_{i_r}=2^{r-1}
\qquad
\text{for } r\in\{1,\ldots,k\}.
$$

These weights are positive. We claim that the statistic

$$
t_I(u)=\sum_{r=1}^{k}2^{r-1}u_{i_r}
$$

is injective on $\{0,1\}^{I}$.

Indeed, let $u\neq v$ in $\{0,1\}^{I}$, and let $m$ be the largest index such that $u_{i_m}\neq v_{i_m}$. Then

$$
t_I(u)-t_I(v)
=
2^{m-1}(u_{i_m}-v_{i_m})
+
\sum_{r=1}^{m-1}2^{r-1}(u_{i_r}-v_{i_r}).
$$

The first term has absolute value $2^{m-1}$. The remaining sum has absolute value at most

$$
\sum_{r=1}^{m-1}2^{r-1}=2^{m-1}-1.
$$

Hence $t_I(u)-t_I(v)\neq0$, so $t_I$ is injective. Therefore

$$
M=|\operatorname{Im}(t_I)|=|\{0,1\}^{I}|=2^k.
$$

Define $G:\operatorname{Im}(t_I)\to\{0,1\}$ by

$$
G(t_I(u))=g(u).
$$

This is well-defined because $t_I$ is injective, and it satisfies $g(u)=G(t_I(u))$ for all $u\in\{0,1\}^{I}$. The sign-change set defining $C_{t_I}(G)$ is a subset of $\{1,\ldots,M-1\}$, so

$$
C_{t_I}(G)\leq M-1=2^k-1.
$$

Applying the theorem gives

$$
H^{\ast}(f)\leq C_{t_I}(G)\leq 2^k-1.
$$

Thus every $k$-junta satisfies $H^{\ast}(f)\leq 2^k-1$. $\blacksquare$
