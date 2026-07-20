# Quadratic Threshold Functions Can Require Linearly Many Heads

## Statement

Let $H^{\ast}(f)$ be the minimum number of heads in the one-layer softmax-attention model of [../../model.md](../../model.md) whose thresholded scalar output agrees with $f : \{0,1\}^{n} \to \{0,1\}$ on the Boolean cube. Let $\deg_{\pm}(f)$ be the least degree of a real polynomial $p$ such that $p(x)>0$ whenever $f(x)=1$ and $p(x)<0$ whenever $f(x)=0$.

There are absolute constants $c>0$ and $n_0$ such that for every $n\geq n_0$ there exists a Boolean function $f_n : \{0,1\}^{n}\to\{0,1\}$ with

$$
f_n(x)=\mathbf{1}[q_n(x)>0]
$$

for some real polynomial $q_n$ of degree at most $2$, and satisfying

$$
\deg_{\pm}(f_n)=2
\qquad\text{and}\qquad
H^{\ast}(f_n)\geq c n.
$$

> **Equivalently.** Ordinary threshold degree can stay equal to $2$ while head complexity grows linearly in the number of input bits.

## Proof

For $H\geq 1$, write

$$
\mathcal{F}_{n,H}:=\{f:\{0,1\}^{n}\to\{0,1\}:H^{\ast}(f)\leq H\}.
$$

We use two facts already proved in the lemma stack.

1. Lemma 19 gives an absolute constant $C>0$ such that, for all $n\geq 1$ and $H\geq 1$,

$$
\log_2|\mathcal{F}_{n,H}|\leq C H n\bigl(n+\log_2(H+1)\bigr).
$$

2. Lemma 11 says that constants have $H^{\ast}=0$, and every nonconstant affine threshold function has $H^{\ast}=1$.

### Lemma 1. Many affine threshold functions

**Claim.** If $\mathrm{LTF}_m$ denotes the class of Boolean functions on $\{0,1\}^{m}$ strictly represented by affine linear forms, then for every $m\geq 2$,

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

For every cube point, the value

$$
\sum_{i=1}^{k}2^{i-1}y_i-\sum_{j=1}^{k}a_jz_j
$$

is an integer. Hence $L_a$ never vanishes on the cube, and $\mathbf{1}[L_a>0]$ is a strict affine threshold function.

If $a\neq b$, choose $j$ with $a_j\neq b_j$. After swapping the names if necessary, assume $a_j<b_j$. Choose $y$ whose binary value is $a_j+1$, and choose $z=e_j$. This is possible because $0\leq a_j<a_j+1\leq 2^k-1$. Then

$$
L_a(y,e_j,r)=(a_j+1)-a_j-\frac12=\frac12>0,
$$

while

$$
L_b(y,e_j,r)=(a_j+1)-b_j-\frac12\leq (a_j+1)-(a_j+1)-\frac12=-\frac12<0.
$$

Thus the map $a\mapsto \mathbf{1}[L_a>0]$ is injective. Therefore

$$
|\mathrm{LTF}_m|\geq (2^k)^k=2^{k^2}.
$$

Since $k=\lfloor m/2\rfloor\geq m/3$ for $m\geq 2$, this gives

$$
|\mathrm{LTF}_m|\geq 2^{m^2/9}.
$$

$\blacksquare$

### Lemma 2. Many quadratic threshold functions

**Claim.** Let $\mathcal{Q}_n$ be the class of Boolean functions on $\{0,1\}^{n}$ strictly sign-representable by real polynomials of degree at most $2$. For every $n\geq 4$,

$$
|\mathcal{Q}_n|\geq 2^{n^3/243}.
$$

**Proof.** Put $m=\lfloor n/2\rfloor$. Split the first $2m$ variables as $u,v\in\{0,1\}^{m}$, and ignore the remaining $n-2m$ variables.

For each tuple $(g_1,\ldots,g_m)\in(\mathrm{LTF}_m)^m$, choose strict affine representatives $\ell_i(v)$, so that $\ell_i(v)>0$ exactly when $g_i(v)=1$ and $\ell_i(v)<0$ exactly when $g_i(v)=0$. Define

$$
\mu=\min_{1\leq i\leq m,\ v\in\{0,1\}^{m}}|\ell_i(v)|.
$$

The representatives are strict and the cube is finite, so $\mu>0$.

Set

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

Consequently, distinct tuples $(g_1,\ldots,g_m)$ give distinct Boolean functions in $\mathcal{Q}_n$. Hence

$$
|\mathcal{Q}_n|\geq |\mathrm{LTF}_m|^m\geq 2^{m^3/9}.
$$

Since $m=\lfloor n/2\rfloor\geq n/3$ for $n\geq 4$,

$$
|\mathcal{Q}_n|\geq 2^{n^3/243}.
$$

$\blacksquare$

### Lemma 3. Pigeonhole separation

**Claim.** There are absolute constants $c>0$ and $n_0$ such that, for every $n\geq n_0$, some $f_n\in\mathcal{Q}_n$ satisfies

$$
\deg_{\pm}(f_n)=2
\qquad\text{and}\qquad
H^{\ast}(f_n)\geq c n.
$$

**Proof.** Let

$$
a=\frac{1}{243}.
$$

Let $C$ be the absolute constant from Lemma 19, and choose

$$
c=\min\left\{1,\frac{a}{4C}\right\}.
$$

Choose $n_0$ large enough that for every $n\geq n_0$, we have $n\geq 4$ and $\lfloor c n\rfloor\geq 1$. For such $n$, set

$$
H_n=\lfloor c n\rfloor.
$$

Then $1\leq H_n\leq n$, and

$$
\log_2(H_n+1)\leq\log_2(n+1)\leq n.
$$

Therefore Lemma 19 gives

$$
\begin{aligned}
\log_2|\mathcal{F}_{n,H_n}|
&\leq C H_n n\bigl(n+\log_2(H_n+1)\bigr) \\
&\leq C c n\cdot n\cdot 2n \\
&=2 C c n^3 \\
&\leq \frac{a}{2}n^3.
\end{aligned}
$$

On the other hand, Lemma 2 gives

$$
\log_2|\mathcal{Q}_n|\geq a n^3.
$$

Thus $|\mathcal{F}_{n,H_n}|<|\mathcal{Q}_n|$. Hence there exists

$$
f_n\in\mathcal{Q}_n\setminus\mathcal{F}_{n,H_n}.
$$

Since $f_n\in\mathcal{Q}_n$, there is a real polynomial $q_n$ of degree at most $2$ such that

$$
f_n(x)=\mathbf{1}[q_n(x)>0]
$$

on the Boolean cube. In particular, $\deg_{\pm}(f_n)\leq 2$.

Also $f_n\notin\mathcal{F}_{n,H_n}$, so $H^{\ast}(f_n)>H_n$. Because $H_n\geq 1$, Lemma 11 implies that $f_n$ cannot have threshold degree at most $1$: constants have head complexity $0$, and nonconstant affine threshold functions have head complexity $1$. Therefore

$$
\deg_{\pm}(f_n)>1.
$$

Combining the two inequalities gives

$$
\deg_{\pm}(f_n)=2.
$$

Finally, since $H^{\ast}(f_n)$ is an integer and $H^{\ast}(f_n)>\lfloor c n\rfloor$,

$$
H^{\ast}(f_n)\geq \lfloor c n\rfloor+1>c n.
$$

This proves the claim. $\blacksquare$

### Conclusion

Lemma 3 proves that for every $n\geq n_0$ there is a Boolean function $f_n:\{0,1\}^{n}\to\{0,1\}$ with

$$
f_n(x)=\mathbf{1}[q_n(x)>0],
\qquad
\deg_{\pm}(f_n)=2,
\qquad
H^{\ast}(f_n)\geq c n,
$$

where $q_n$ has degree at most $2$. This is exactly the desired separation. $\blacksquare$

## Consequence

The capacity gap is the whole reason the separation is linear. It is the $n^2$-vs-$n^3$ gap: quadratic threshold functions contain at least $2^{\Omega(n^3)}$ functions, while $H$-head attention realizes only $2^{O(H n^2)}$ functions up to the logarithmic factor when $H\leq n$. Therefore some quadratic threshold function must require $H=\Omega(n)$ heads.

This is the Warren (1968) sign-pattern counting method, in the same nonconstructive spirit as Shannon (1949) and the later threshold-counting literature of Goldberg and Jerrum (1995) and of Anthony and Bartlett (1999). It also shows that Lemma 6 can be far from tight: ordinary threshold degree may stay equal to $2$ while $H^{\ast}$ grows linearly.
