# Quadratic Threshold Functions Can Require Linearly Many Heads

## Statement

Let $H^{\ast}(f)$ be the least number of heads needed to compute $f : \{0,1\}^{n} \to \{0,1\}$ in the one-layer attention model, equivalently the least number of admissible linear-fractional atoms needed before a strict final threshold as in Lemma 10. Let $\deg_{\pm}(f)$ be the least degree of a real polynomial $p$ such that $p(x)>0$ exactly when $f(x)=1$ and $p(x)<0$ exactly when $f(x)=0$ on the Boolean cube.

There is an absolute constant $c>0$ such that, for all sufficiently large $n$, there exists a Boolean function $f_n : \{0,1\}^{n} \to \{0,1\}$ with

$$
\deg_{\pm}(f_n)=2
$$

and

$$
H^{\ast}(f_n) \geq c n.
$$

## Proof

For $H\geq 1$, write

$$
\mathcal{F}_{n,H}:=\{f:\{0,1\}^{n}\to\{0,1\}:H^{\ast}(f)\leq H\}.
$$

We use two proved facts from the lemma stack.

1. Lemma 19 gives an absolute constant $C>0$ such that, for all $n\geq 1$ and $H\geq 1$,

$$
\log_2|\mathcal{F}_{n,H}|\leq C H n(n+\log_2(H+1)).
$$

2. Lemma 11 says that constants have $H^{\ast}=0$, and every nonconstant linear threshold function has $H^{\ast}=1$.

### Lemma 1. Many strict linear threshold functions

**Claim.** If $\mathrm{LTF}_m$ denotes the set of Boolean functions on $\{0,1\}^{m}$ strictly represented by affine linear forms, then for every $m\geq 2$,

$$
|\mathrm{LTF}_m|\geq 2^{m^2/9}.
$$

**Proof.** Put $k=\lfloor m/2\rfloor$. For every vector

$$
a=(a_1,\ldots,a_k)\in\{0,\ldots,2^k-1\}^{k},
$$

define the affine form

$$
L_a(y,z,r)=\sum_{i=1}^{k}2^{i-1}y_i-\sum_{j=1}^{k}a_jz_j-\frac12,
$$

where $y,z\in\{0,1\}^{k}$ and $r$ denotes the remaining $m-2k$ variables, if any.

For each cube point, the value $\sum_i2^{i-1}y_i-\sum_ja_jz_j$ is an integer. Hence $L_a$ never vanishes on the cube. Therefore

$$
g_a=\mathbf{1}[L_a>0]
$$

is strictly represented by an affine linear form.

If $a\neq b$, choose $j$ with $a_j\neq b_j$. After swapping the names if necessary, assume $a_j<b_j$. Choose $y$ whose binary value is $a_j+1$, and choose $z=e_j$. This is possible because $0\leq a_j<a_j+1\leq 2^k-1$. Then

$$
L_a(y,e_j,r)=(a_j+1)-a_j-\frac12=\frac12>0,
$$

while

$$
L_b(y,e_j,r)=(a_j+1)-b_j-\frac12\leq (a_j+1)-(a_j+1)-\frac12=-\frac12<0.
$$

Thus $g_a\neq g_b$. The map $a\mapsto g_a$ is injective, so

$$
|\mathrm{LTF}_m|\geq (2^k)^k=2^{k^2}.
$$

Since $k=\lfloor m/2\rfloor\geq m/3$ for $m\geq 2$, this gives

$$
|\mathrm{LTF}_m|\geq 2^{m^2/9}.
$$

$\blacksquare$

### Lemma 2. Many quadratic threshold functions

**Claim.** Let $\mathcal{Q}_n$ be the set of Boolean functions $f:\{0,1\}^{n}\to\{0,1\}$ with $\deg_{\pm}(f)\leq 2$. For every $n\geq 4$,

$$
|\mathcal{Q}_n|\geq 2^{n^3/243}.
$$

**Proof.** Put $m=\lfloor n/2\rfloor$. Split the first $2m$ variables as $u,v\in\{0,1\}^{m}$, and ignore the remaining $n-2m$ variables.

For each tuple $(g_1,\ldots,g_m)\in(\mathrm{LTF}_m)^m$, choose strict affine representatives $\ell_i(v)$, so that $\ell_i(v)>0$ exactly when $g_i(v)=1$ and $\ell_i(v)<0$ exactly when $g_i(v)=0$. Define

$$
\mu=\min_{1\leq i\leq m,\ v\in\{0,1\}^{m}}|\ell_i(v)|.
$$

The representatives are strict and the cube is finite, so $\mu>0$.

Now set

$$
A(u,v)=\sum_{i=1}^{m}u_i\ell_i(v).
$$

The set $\{-A(u,v):u,v\in\{0,1\}^{m}\}$ is finite. Choose

$$
t\in(-\mu,\mu)
$$

outside this finite set, and define

$$
q(u,v)=t+\sum_{i=1}^{m}u_i\ell_i(v).
$$

The choice of $t$ gives $q(u,v)\neq 0$ on the Boolean cube. Since each $\ell_i$ is affine in $v$, each product $u_i\ell_i(v)$ has degree at most $2$. Thus $q$ has degree at most $2$.

For $u=e_i$,

$$
q(e_i,v)=t+\ell_i(v).
$$

If $\ell_i(v)>0$, then $\ell_i(v)\geq\mu$, so $q(e_i,v)\geq\mu-|t|>0$. If $\ell_i(v)<0$, then $\ell_i(v)\leq-\mu$, so $q(e_i,v)\leq-\mu+|t|<0$. Therefore the sign of $q(e_i,v)$ recovers $g_i(v)$.

Consequently, distinct tuples $(g_1,\ldots,g_m)$ give distinct Boolean functions sign-represented by degree at most $2$ polynomials. Hence

$$
|\mathcal{Q}_n|\geq |\mathrm{LTF}_m|^m
\geq 2^{m^3/9}.
$$

Since $m=\lfloor n/2\rfloor\geq n/3$ for $n\geq 4$,

$$
|\mathcal{Q}_n|\geq 2^{n^3/243}.
$$

$\blacksquare$

### Lemma 3. Pigeonhole separation

**Claim.** There is an absolute constant $c>0$ such that, for all sufficiently large $n$, some $f_n\in\mathcal{Q}_n$ satisfies $H^{\ast}(f_n)\geq c n$.

**Proof.** Let

$$
a=\frac{1}{243}.
$$

Let $C$ be the constant from Lemma 19, and choose

$$
c=\min\left\{1,\frac{a}{4C}\right\}.
$$

For sufficiently large $n$, set

$$
H_n=\lfloor c n\rfloor.
$$

Then $H_n\geq 1$ and $H_n\leq n$. Since $\log_2(n+1)\leq n$ for $n\geq 1$,

$$
\begin{aligned}
\log_2|\mathcal{F}_{n,H_n}|
&\leq C H_n n(n+\log_2(H_n+1)) \\
&\leq C c n\cdot n\cdot 2n \\
&\leq \frac{a}{2}n^3.
\end{aligned}
$$

By Lemma 2,

$$
\log_2|\mathcal{Q}_n|\geq a n^3.
$$

Therefore $|\mathcal{F}_{n,H_n}|<|\mathcal{Q}_n|$. By the pigeonhole principle, there exists

$$
f_n\in\mathcal{Q}_n\setminus\mathcal{F}_{n,H_n}.
$$

Thus $\deg_{\pm}(f_n)\leq 2$ and $H^{\ast}(f_n)>H_n$.

Because $H_n\geq 1$, every function with threshold degree at most $1$ lies in $\mathcal{F}_{n,H_n}$ by Lemma 11: constants have head complexity $0$, and nonconstant affine threshold functions have head complexity $1$. Hence this $f_n$ cannot have $\deg_{\pm}(f_n)\leq 1$. Combining this with $\deg_{\pm}(f_n)\leq 2$ gives

$$
\deg_{\pm}(f_n)=2.
$$

Finally, since $H^{\ast}(f_n)$ is an integer and $H^{\ast}(f_n)>\lfloor c n\rfloor$,

$$
H^{\ast}(f_n)\geq \lfloor c n\rfloor+1>c n.
$$

This proves the claim. $\blacksquare$

### Conclusion

Lemma 3 gives, for all sufficiently large $n$, a Boolean function $f_n:\{0,1\}^{n}\to\{0,1\}$ such that

$$
\deg_{\pm}(f_n)=2
\qquad\text{and}\qquad
H^{\ast}(f_n)\geq c n.
$$

This is the desired separation. $\blacksquare$

## Consequence

Head complexity can be linearly larger than ordinary threshold degree. In particular, even among quadratic threshold functions, the one-layer attention model can require $\Omega(n)$ heads although the representing polynomial has degree $2$.
