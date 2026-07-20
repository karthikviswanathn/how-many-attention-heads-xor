# Weighted-Sum Sign-Change Upper Bound

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), with a final strict threshold at the query token. Let $H^{\ast}(f)$ be the minimum number of one-layer attention heads needed to compute $f : \{0,1\}^{n} \to \{0,1\}$, with $H^{\ast}(f)=0$ allowed only for constant functions.

Suppose there are positive weights

$$
\lambda_1,\ldots,\lambda_n>0,
$$

a statistic

$$
t(x)=\sum_{i=1}^{n}\lambda_i x_i,
$$

and a function $F:\operatorname{Im}(t)\to\{0,1\}$ such that

$$
f(x)=F(t(x))
$$

for every $x\in\{0,1\}^{n}$. List the distinct values of $t$ as

$$
\tau_0<\tau_1<\cdots<\tau_{M-1}.
$$

Define

$$
\sigma_j:=
\begin{cases}
+1, & \text{if } F(\tau_j)=1,\\
-1, & \text{if } F(\tau_j)=0,
\end{cases}
$$

and let

$$
C_t(F):=\left|\left\{j\in\{1,\ldots,M-1\}:\sigma_{j-1}\neq\sigma_j\right\}\right|.
$$

Then

$$
H^{\ast}(f)\leq C_t(F).
$$

> **Equivalently.** If a Boolean function depends only on one positive weighted sum, then one head suffices for each sign change along the ordered image of that weighted sum.

## Proof

Set

$$
Q:=\{0,1\}^{n},
\qquad
\Lambda:=\sum_{i=1}^{n}\lambda_i.
$$

Since each $\lambda_i>0$, the statistic $t$ is nonnegative on $Q$, and

$$
t(0,\ldots,0)=0.
$$

Therefore $\tau_0=0$.

We use the one-head normal form from Lemma 10. A scalar one-head atom has the form

$$
\phi(x)=
\frac{\eta+\sum_{i=1}^{n}\rho_i\alpha^{x_i}(m_i+\delta x_i)}
{\gamma+\sum_{i=1}^{n}\rho_i\alpha^{x_i}},
\qquad
\gamma>0,
\qquad
\rho_i>0,
\qquad
\alpha>0.
$$

By Lemma 10, any score equal to a constant plus a sum of $H$ such atoms is computable with $H$ attention heads.

Let

$$
J:=\left\{j\in\{1,\ldots,M-1\}:\sigma_{j-1}\neq\sigma_j\right\},
\qquad
C:=\lvert J\rvert=C_t(F).
$$

If $C=0$, then the ordered sign sequence never changes, so $\sigma_j=\sigma_0$ for every $j$. Thus $F$ is constant on $\operatorname{Im}(t)$, hence $f$ is constant on $Q$. By the zero-head convention, $H^{\ast}(f)=0=C$.

Assume from now on that $C\geq 1$.

### Lemma 1. Sign polynomial on the weighted image

There is a degree $C$ polynomial $P$ such that

$$
\operatorname{sgn}(P(\tau_\ell))=\sigma_\ell
\qquad \text{for every }0\leq \ell\leq M-1.
$$

**Proof.** For every $j\in J$, choose

$$
m_j\in(\tau_{j-1},\tau_j),
$$

and define

$$
P(s):=\sigma_0\prod_{j\in J}(m_j-s).
$$

Fix $\ell\in\{0,\ldots,M-1\}$. The factor $m_j-\tau_\ell$ is negative exactly when $j\leq \ell$, and positive exactly when $j>\ell$. Therefore

$$
\operatorname{sgn}(P(\tau_\ell))
=
\sigma_0(-1)^{\lvert\{j\in J:j\leq\ell\}\rvert}.
$$

The sign sequence $\sigma_\ell$ flips precisely at the indices in $J$. Induction on $\ell$ gives

$$
\sigma_\ell
=
\sigma_0(-1)^{\lvert\{j\in J:j\leq\ell\}\rvert}.
$$

Hence

$$
\operatorname{sgn}(P(\tau_\ell))=\sigma_\ell
\qquad \text{for every }0\leq\ell\leq M-1.
$$

Also $P(\tau_\ell)\neq0$, since no $m_j$ is one of the values $\tau_\ell$. $\blacksquare$

### Lemma 2. Partial fractions preserve the signs

There are positive numbers $r_1,\ldots,r_C$ and real numbers $c,d_1,\ldots,d_C$ such that

$$
\operatorname{sgn}\left(c+\sum_{h=1}^{C}\frac{d_h}{\tau_\ell+r_h}\right)=\sigma_\ell
\qquad \text{for every }0\leq\ell\leq M-1.
$$

**Proof.** Choose pairwise distinct numbers

$$
r_1,\ldots,r_C>0,
$$

and put

$$
B(s):=\prod_{h=1}^{C}(s+r_h).
$$

Because every $\tau_\ell\geq0$, we have $B(\tau_\ell)>0$.

Since $\deg P=C=\deg B$ and $B$ has simple real roots, the rational function $P(s)/B(s)$ has a partial-fraction decomposition of the form

$$
\frac{P(s)}{B(s)}
=
c+\sum_{h=1}^{C}\frac{d_h}{s+r_h}
$$

for some real numbers $c,d_1,\ldots,d_C$.

For every $\ell$,

$$
c+\sum_{h=1}^{C}\frac{d_h}{\tau_\ell+r_h}
=
\frac{P(\tau_\ell)}{B(\tau_\ell)}.
$$

Since $B(\tau_\ell)>0$, Lemma 1 gives

$$
\operatorname{sgn}\left(c+\sum_{h=1}^{C}\frac{d_h}{\tau_\ell+r_h}\right)
=
\operatorname{sgn}(P(\tau_\ell))
=
\sigma_\ell.
$$

This proves the claim. $\blacksquare$

### Lemma 3. Weighted shifted reciprocals cost one head

For every $r>0$ and $d\in\mathbb{R}$, the function

$$
x\mapsto\frac{d}{t(x)+r}
$$

is a valid one-head atom.

**Proof.** Since $C\geq1$, the image of $t$ has at least two values, so $\Lambda>0$. Choose

$$
\alpha:=1+\frac{2\Lambda}{r},
\qquad
\rho_i:=\frac{\lambda_i}{\alpha-1},
\qquad
\gamma:=\frac{r}{2},
$$

and set

$$
\eta:=d,
\qquad
m_i:=0,
\qquad
\delta:=0.
$$

Then $\alpha>1$, $\rho_i>0$, and $\gamma>0$. Since $x_i\in\{0,1\}$,

$$
\alpha^{x_i}=1+(\alpha-1)x_i.
$$

The denominator of the atom is

$$
\begin{aligned}
\gamma+\sum_i\rho_i\alpha^{x_i}
&=\frac{r}{2}
+\sum_i\frac{\lambda_i}{\alpha-1}
+\sum_i\lambda_i x_i \\
&=\frac{r}{2}
+\frac{\Lambda}{\alpha-1}
+t(x) \\
&=\frac{r}{2}+\frac{r}{2}+t(x) \\
&=t(x)+r.
\end{aligned}
$$

The numerator is

$$
\eta+\sum_i\rho_i\alpha^{x_i}(m_i+\delta x_i)=d.
$$

Thus the atom is exactly $d/(t(x)+r)$. $\blacksquare$

### Conclusion

Apply Lemma 3 to the numbers $r_h,d_h$ from Lemma 2, and define the score

$$
S(x):=c+\sum_{h=1}^{C}\frac{d_h}{t(x)+r_h}.
$$

By Lemma 10, this score is computable with $C$ attention heads. If $t(x)=\tau_\ell$, then Lemma 2 gives

$$
\operatorname{sgn}(S(x))=\sigma_\ell.
$$

By the definition of $\sigma_\ell$, this means

$$
S(x)>0 \Longleftrightarrow F(t(x))=1,
\qquad
S(x)<0 \Longleftrightarrow F(t(x))=0.
$$

Since $f(x)=F(t(x))$, the strict threshold rule $S(x)>0$ computes $f$ with $C$ heads. Hence

$$
H^{\ast}(f)\leq C=C_t(F).
$$

This proves the theorem. $\blacksquare$

## Consequence

Since

$$
J\subseteq\{1,\ldots,M-1\},
$$

we have

$$
C_t(F)\leq M-1.
$$

Therefore

$$
H^{\ast}(f)\leq C_t(F)\leq M-1.
$$

This recovers Lemma 9 as the weaker weighted-sum interpolation bound.
