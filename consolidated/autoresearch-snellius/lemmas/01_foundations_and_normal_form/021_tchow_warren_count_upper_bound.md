# Warren Counting Bound for Unrestricted Tangential-Chow Complexity

## Statement

Let $n,H \geq 1$. For an integer $K\geq 0$, affine forms

$$
L_h(x)=a_{h,0}+\sum_{i=1}^{n}a_{h,i}x_i, \qquad M_h(x)=b_{h,0}+\sum_{i=1}^{n}b_{h,i}x_i,
$$

and a scalar $\theta\in\mathbb R$, define an unrestricted tangential-Chow sign-representer of order $K$ by

$$
P(x)=\theta\prod_{h=1}^{K}L_h(x)+\sum_{h=1}^{K}M_h(x)\prod_{g\neq h}L_g(x).
$$

For $K=0$, the empty product is $1$ and the empty sum is $0$. Say that $f:\{0,1\}^{n}\to\{0,1\}$ has $\mathrm{tChow}_{\pm}(f)\leq H$ if such a $P$ exists for some $K\leq H$, satisfies $P(x)\neq 0$ on the Boolean cube, and obeys

$$
f(x)=1 \qquad\Longleftrightarrow\qquad P(x)>0.
$$

Let

$$
\mathcal T_{n,H}:=\{f:\{0,1\}^{n}\to\{0,1\}:\mathrm{tChow}_{\pm}(f)\leq H\}.
$$

Then there is an absolute constant $C>0$ such that

$$
\log_2 |\mathcal T_{n,H}| \leq C H n\bigl(n+\log_2(H+1)\bigr).
$$

> **Equivalently.** Unrestricted tangential-Chow forms of order at most $H$ realize at most
>
> $$
> 2^{C H n(n+\log_2(H+1))}
> $$
>
> strict Boolean-cube sign patterns.

## Proof

Let

$$
Q:=\{0,1\}^{n}, \qquad m:=|Q|=2^n.
$$

We use Warren's sign-condition theorem in the following form. There is an absolute constant $A\geq 1$ such that, if $m\geq \ell$, then $m$ real polynomials in $\ell$ real variables, each of degree at most $d$, realize at most

$$
\left(\frac{A d m}{\ell}\right)^\ell
$$

sign conditions in $\{-1,0,+1\}^{m}$.

### Lemma 1. Polynomial parameterization

**Claim.** Every function in $\mathcal T_{n,H}$ is induced on $Q$ by the signs of $m$ polynomials in

$$
\ell=1+2H(n+1)
$$

real parameters, each of degree at most $H+1$. Moreover,

$$
\ell\leq 5Hn.
$$

**Proof.** Fix $f\in\mathcal T_{n,H}$. Choose an order $K\leq H$ unrestricted tangential-Chow witness $P_K$. Pad it to order $H$ by setting $L_h\equiv 1$ and $M_h\equiv 0$ for every $K<h\leq H$. The multiplicative identity $1$ and additive identity $0$ show that the padded order-$H$ expression equals $P_K$ on every point, so it still strictly represents $f$ on $Q$.

Now regard all coefficients as free real parameters

$$
\Theta=\left(\theta,(a_{h,i})_{1\leq h\leq H,0\leq i\leq n},(b_{h,i})_{1\leq h\leq H,0\leq i\leq n}\right).
$$

The number of parameters is

$$
\ell=1+H(n+1)+H(n+1)=1+2H(n+1).
$$

Since $n\geq 1$ and $H\geq 1$, we have $1\leq Hn$ and $H\leq Hn$, hence

$$
\ell=1+2Hn+2H\leq Hn+2Hn+2Hn=5Hn.
$$

For fixed $x\in Q$, each $L_h(x)$ is linear in the variables $a_{h,0},\ldots,a_{h,n}$, and each $M_h(x)$ is linear in the variables $b_{h,0},\ldots,b_{h,n}$. Thus $\prod_{h=1}^{H}L_h(x)$ has parameter degree at most $H$, so $\theta\prod_{h=1}^{H}L_h(x)$ has parameter degree at most $H+1$. For each $h$, the term $M_h(x)\prod_{g\neq h}L_g(x)$ has parameter degree at most $1+(H-1)=H$. Therefore the full value $P(x;\Theta)$ has parameter degree at most $H+1$.

Enumerate $Q$ as $x^{(1)},\ldots,x^{(m)}$ and define

$$
p_j(\Theta):=P(x^{(j)};\Theta) \qquad 1\leq j\leq m.
$$

For any strict witness, the label vector of $f$ is obtained from the sign condition of $p_1,\ldots,p_m$ by declaring label $1$ exactly at the coordinates with positive sign. Warren's theorem counts all realized sign conditions, including those with zero entries, so it gives an upper bound for strict label vectors. Hence $|\mathcal T_{n,H}|$ is at most the number of sign conditions realized by $p_1,\ldots,p_m$. $\blacksquare$

### Lemma 2. The large cube case

**Claim.** If $m\geq \ell$, then

$$
\log_2 |\mathcal T_{n,H}| \leq 5(1+\log_2 A)Hn\bigl(n+\log_2(H+1)\bigr).
$$

**Proof.** By Lemma 1 and Warren's theorem with $d=H+1$,

$$
|\mathcal T_{n,H}|\leq \left(\frac{A(H+1)2^n}{\ell}\right)^\ell.
$$

Taking base $2$ logarithms gives

$$
\log_2 |\mathcal T_{n,H}|\leq \ell\log_2\left(\frac{A(H+1)2^n}{\ell}\right).
$$

Since $\ell\geq 1$,

$$
\log_2\left(\frac{A(H+1)2^n}{\ell}\right)\leq n+\log_2 A+\log_2(H+1).
$$

Set $s:=n+\log_2(H+1)$. Since $s\geq 1$ and $A\geq 1$,

$$
s+\log_2 A\leq (1+\log_2 A)s.
$$

Using $\ell\leq 5Hn$ from Lemma 1,

$$
\log_2 |\mathcal T_{n,H}|\leq 5(1+\log_2 A)Hn\bigl(n+\log_2(H+1)\bigr).
$$

This proves the claim. $\blacksquare$

### Lemma 3. The small cube case

**Claim.** If $m<\ell$, then

$$
\log_2 |\mathcal T_{n,H}| \leq 5Hn\bigl(n+\log_2(H+1)\bigr).
$$

**Proof.** There are exactly $2^m$ Boolean functions on $Q$, so

$$
|\mathcal T_{n,H}|\leq 2^m.
$$

Therefore

$$
\log_2 |\mathcal T_{n,H}|\leq m=2^n.
$$

The assumption $m<\ell$ and Lemma 1 give

$$
2^n=m<\ell\leq 5Hn.
$$

Since $n+\log_2(H+1)\geq 1$,

$$
\log_2 |\mathcal T_{n,H}|\leq 5Hn\bigl(n+\log_2(H+1)\bigr).
$$

This proves the claim. $\blacksquare$

### Conclusion

Set

$$
C:=5(1+\log_2 A).
$$

This is an absolute positive constant. Lemma 2 covers the case $m\geq \ell$, and Lemma 3 covers the case $m<\ell$, since $5\leq C$. Therefore, for all $n\geq 1$ and $H\geq 1$,

$$
\log_2 |\mathcal T_{n,H}| \leq C H n\bigl(n+\log_2(H+1)\bigr).
$$

Thus unrestricted tangential-Chow forms of order at most $H$ realize at most

$$
2^{C H n(n+\log_2(H+1))}
$$

strict Boolean-cube sign patterns. $\blacksquare$

## Consequence

The unrestricted tangential-Chow class satisfies the Warren counting upper bound

$$
|\mathcal T_{n,H}|\leq 2^{C H n(n+\log_2(H+1))}.
$$

This supplies the counting estimate for the unrestricted tangential-Chow comparison frontier and prepares the quadratic threshold function separation between $\deg_{\pm}$ and $\mathrm{tChow}_{\pm}$.
