# Warren Counting Bound for Low Head Complexity

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), and let $H^{\ast}(f)$ be the least number of attention heads needed to compute $f : \{0,1\}^{n} \to \{0,1\}$ with a final strict threshold at the query token.

For integers $n\geq 1$ and $H\geq 1$, define

$$
\mathcal{F}_{n,H}:=\{f:\{0,1\}^{n}\to\{0,1\}: H^{\ast}(f)\leq H\}.
$$

There is an absolute constant $C>0$ such that

$$
\log_2 |\mathcal{F}_{n,H}| \leq C H n\bigl(n+\log_2(H+1)\bigr).
$$

> **Equivalently.** The class of Boolean functions computable with at most $H$ heads has at most
>
> $$
> 2^{C H n(n+\log_2(H+1))}
> $$
>
> possible strict-threshold sign patterns on the Boolean cube.

## Proof

Let

$$
Q:=\{0,1\}^{n},
\qquad
m:=|Q|=2^n.
$$

We use the following standard sign-condition form of Warren's theorem. There is an absolute constant $A\geq 1$ such that, whenever $m\geq \ell$, any $m$ real polynomials in $\ell$ real variables, each of degree at most $d$, realize at most

$$
\left(\frac{A d m}{\ell}\right)^\ell
$$

sign conditions in $\{-1,0,+1\}^{m}$.

### Lemma 1. Polynomial parameterization

**Claim.** Every function in $\mathcal{F}_{n,H}$ is induced on $Q$ by the signs of $m$ polynomials in

$$
\ell=1+2H(n+1)
$$

real parameters, each of degree at most $H+1$. Moreover,

$$
\ell\leq 5Hn.
$$

**Proof.** Fix $f\in\mathcal{F}_{n,H}$. By Lemma 14, for some $K\leq H$ there are affine functions

$$
N_h(x)=a_{h,0}+\sum_{i=1}^{n}a_{h,i}x_i,
\qquad
D_h(x)=d_{h,0}+\sum_{i=1}^{n}d_{h,i}x_i,
$$

and a real threshold parameter $\theta$ such that the cleared-denominator polynomial

$$
P_K(x)=\theta\prod_{h=1}^{K}D_h(x)+\sum_{h=1}^{K}N_h(x)\prod_{g\neq h}D_g(x)
$$

strictly represents $f$ on $Q$.

Pad to exactly $H$ heads by setting, for $K<h\leq H$,

$$
D_h(x):=1,
\qquad
N_h(x):=0.
$$

Then

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x)
$$

still strictly represents $f$ on $Q$.

Now regard all coefficients as free real parameters

$$
\Theta=(\theta,(a_{h,i})_{1\leq h\leq H,0\leq i\leq n},(d_{h,i})_{1\leq h\leq H,0\leq i\leq n}).
$$

The number of parameters is

$$
\ell=1+2H(n+1).
$$

Since $n\geq 1$ and $H\geq 1$,

$$
\ell=1+2H(n+1)\leq Hn+4Hn=5Hn.
$$

For fixed $x\in Q$, each $N_h(x)$ and $D_h(x)$ is affine linear in $\Theta$. Therefore $\theta\prod_{h=1}^{H}D_h(x)$ has parameter degree at most $H+1$, while each term $N_h(x)\prod_{g\neq h}D_g(x)$ has parameter degree at most $H$. Thus $P(x;\Theta)$ has parameter degree at most $H+1$.

Enumerate $Q$ as $x^{(1)},\ldots,x^{(m)}$ and define

$$
p_j(\Theta):=P(x^{(j)};\Theta).
$$

The function represented by $\Theta$ is the label vector

$$
x^{(j)}\mapsto \mathbf{1}[p_j(\Theta)>0].
$$

The admissibility restrictions from Lemma 14 only shrink the set of allowed parameter values, so counting all real values of $\Theta$ gives an upper bound. Also, a sign condition of $p_1,\ldots,p_m$ determines this label vector, since labels are exactly the coordinates with positive sign. Hence $|\mathcal{F}_{n,H}|$ is at most the number of sign conditions realized by $p_1,\ldots,p_m$. $\blacksquare$

### Lemma 2. The large cube case

**Claim.** If $m\geq \ell$, then there is an absolute constant $C_2$ such that

$$
\log_2 |\mathcal{F}_{n,H}| \leq C_2 H n\bigl(n+\log_2(H+1)\bigr).
$$

**Proof.** By Lemma 1 and the sign-condition bound with $d=H+1$,

$$
|\mathcal{F}_{n,H}|
\leq
\left(\frac{A(H+1)2^n}{\ell}\right)^\ell.
$$

Taking base $2$ logarithms gives

$$
\log_2 |\mathcal{F}_{n,H}|
\leq
\ell\log_2\left(\frac{A(H+1)2^n}{\ell}\right).
$$

Since $\ell\geq 1$,

$$
\log_2\left(\frac{A(H+1)2^n}{\ell}\right)
\leq
n+\log_2 A+\log_2(H+1).
$$

Choose an absolute constant $C_1$ such that, for all $n\geq 1$ and $H\geq 1$,

$$
n+\log_2 A+\log_2(H+1)
\leq
C_1\bigl(n+\log_2(H+1)\bigr).
$$

Using $\ell\leq 5Hn$ from Lemma 1,

$$
\log_2 |\mathcal{F}_{n,H}|
\leq
5C_1 H n\bigl(n+\log_2(H+1)\bigr).
$$

Thus the claim holds with $C_2=5C_1$. $\blacksquare$

### Lemma 3. The small cube case

**Claim.** If $m<\ell$, then

$$
\log_2 |\mathcal{F}_{n,H}| \leq 5Hn\bigl(n+\log_2(H+1)\bigr).
$$

**Proof.** There are exactly $2^m$ Boolean functions on $Q$, so

$$
|\mathcal{F}_{n,H}|\leq 2^m
$$

and hence

$$
\log_2 |\mathcal{F}_{n,H}|\leq m=2^n.
$$

The assumption $m<\ell$ and Lemma 1 give

$$
2^n=m<\ell\leq 5Hn.
$$

Since $n+\log_2(H+1)\geq 1$,

$$
2^n\leq 5Hn\bigl(n+\log_2(H+1)\bigr).
$$

Combining the last two displays proves the claim. $\blacksquare$

### Conclusion

Let

$$
C:=\max\{5,C_2\}.
$$

Lemma 2 covers the case $m\geq \ell$, and Lemma 3 covers the case $m<\ell$. Therefore, for all $n\geq 1$ and $H\geq 1$,

$$
\log_2 |\mathcal{F}_{n,H}| \leq C H n\bigl(n+\log_2(H+1)\bigr).
$$

This proves the Warren counting bound. $\blacksquare$

## Consequence

The family of all Boolean functions computable with at most $H$ heads in the one-layer attention model has cardinality at most

$$
2^{C H n(n+\log_2(H+1))}.
$$

Equivalently, the $H$-head model realizes at most this many strict-threshold sign patterns on $\{0,1\}^{n}$. This supplies the counting upper bound needed for future separation arguments under `frontier:counting_separation`.
