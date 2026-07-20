# Quadratic Threshold Functions Can Require Linearly Large Unrestricted Tangential-Chow Complexity

## Statement

Let $\mathrm{tChow}_{\pm}(f)$ denote the least integer $H$ such that $f : \{0,1\}^{n} \to \{0,1\}$ is strictly sign-represented on the Boolean cube by a polynomial of the unrestricted tangential-Chow form

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x),
$$

where $\theta\in\mathbb R$ and $N_h,D_h$ are arbitrary affine real functions of $x_1,\ldots,x_n$. Let $\deg_{\pm}(f)$ be the threshold degree of $f$.

There are absolute constants $c>0$ and $n_0$ such that for every $n\geq n_0$ there exists a Boolean function $f_n : \{0,1\}^{n}\to\{0,1\}$ with

$$
\deg_{\pm}(f_n)=2
$$

and

$$
\mathrm{tChow}_{\pm}(f_n)\geq c n.
$$

> **Equivalently.** Even after dropping all attention positivity and admissibility restrictions, unrestricted tangential-Chow complexity can be linearly larger than ordinary threshold degree.

## Proof

The previously proved head-complexity separation does not by itself imply the theorem, since the sandwich has the direction

$$
\deg_{\pm}(f)\leq \mathrm{tChow}_{\pm}(f)\leq H^{\ast}(f).
$$

Thus a lower bound on $H^{\ast}(f)$ need not lower-bound $\mathrm{tChow}_{\pm}(f)$. We count unrestricted tangential-Chow forms directly.

### Lemma 1. Sign-counting bound

**Claim.** Let $q_1,\ldots,q_M$ be real polynomials of degree at most $d\geq 1$ in $r$ real parameters. The number of subsets of $[M]$ of the form

$$
\{i:q_i(a)>0\}
$$

as $a\in\mathbb R^r$ varies is at most

$$
(16Md)^{r+3}.
$$

**Proof.** We first use the following component bound. If $F$ is a nonzero real polynomial of degree $\Delta\geq 1$ in $s$ variables, then

$$
\mathbb R^s\setminus\{F=0\}
$$

has at most

$$
(16\Delta)^{s+2}
$$

connected components.

To prove this, homogenize $F$ to $\overline F$ and set $G=X_0\overline F$ on the sphere $S^s$. The factor $X_0$ adds the hyperplane at infinity, so every component of $\mathbb R^s\setminus\{F=0\}$ embeds into a component of $S^s\setminus\{G=0\}$.

Take any finite list of distinct components of $S^s\setminus\{G=0\}$ and choose one point in each. Pick $\eta>0$ smaller than all corresponding $|G|$ values, with both $\eta$ and $-\eta$ regular values of $G|_{S^s}$. Then the chosen points lie in distinct components of

$$
S^s\setminus\{G^2=\eta^2\}.
$$

The hypersurface $\{G^2=\eta^2\}\subset S^s$ is smooth and is cut out by a polynomial of degree

$$
D=2(\Delta+1)\leq 4\Delta.
$$

If it has $B$ connected components, its complement in $S^s$ has at most $B+1$ components. A generic linear height function has at least one critical point on each component. The critical points satisfy the Lagrange multiplier equations for the two constraints $K=0$ and $\sum X_i^2=1$, where $K=G^2-\eta^2$. These equations have degrees at most

$$
D,\ 2,\ D,\ldots,D,
$$

so the number of isolated real critical points is at most $2D^{s+2}$ by the Bezout product bound. Hence

$$
B+1\leq 2D^{s+2}+1\leq (16\Delta)^{s+2}.
$$

Since the finite list of components was arbitrary, the component bound follows.

Now apply this to sign patterns. For a realized positive set $S=\{i:q_i(a)>0\}$, choose $\varepsilon>0$ smaller than every positive $q_i(a)$, or choose any $\varepsilon>0$ if $S=\varnothing$. Then

$$
q_i(a)-\varepsilon>0
\qquad\Longleftrightarrow\qquad
i\in S.
$$

Thus every positive set is a strict sign pattern of the polynomials $q_i-\varepsilon$ in $r+1$ variables. Strict sign patterns are constant on connected components of the complement of

$$
\prod_{i=1}^M(q_i-\varepsilon)=0.
$$

This product has degree at most $Md$. The component bound with $s=r+1$ gives at most

$$
(16Md)^{r+3}
$$

patterns. $\blacksquare$

### Lemma 2. Low tangential-Chow count

**Claim.** There is an absolute constant $C>0$ such that, for all $n\geq 4$ and $1\leq H\leq n$, if

$$
\mathcal T_{n,H}
=
\{f:\{0,1\}^n\to\{0,1\}:\mathrm{tChow}_{\pm}(f)\leq H\},
$$

then

$$
|\mathcal T_{n,H}|\leq 2^{C H n^2}.
$$

**Proof.** Every witness of order $K\leq H$ can be padded to order $H$ by setting $D_h\equiv 1$ and $N_h\equiv 0$ for $K<h\leq H$. Thus it suffices to count order-$H$ forms

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x).
$$

Write

$$
D_h(x)=a_{h,0}+\sum_{i=1}^n a_{h,i}x_i,
\qquad
N_h(x)=b_{h,0}+\sum_{i=1}^n b_{h,i}x_i.
$$

The number of real parameters is

$$
\ell=1+2H(n+1).
$$

For each cube point $x$, the value $P(x)$ is a polynomial in these $\ell$ parameters of degree at most $H+1$. Since a represented Boolean function is determined by the positive set of the $2^n$ values $P(x)$, Lemma 1 gives

$$
|\mathcal T_{n,H}|
\leq
\bigl(16\cdot 2^n(H+1)\bigr)^{\ell+3}.
$$

For $1\leq H\leq n$ and $n\geq 4$,

$$
\ell+3\leq 8Hn,
\qquad
\log_2\bigl(16\cdot 2^n(H+1)\bigr)\leq 3n.
$$

Therefore

$$
|\mathcal T_{n,H}|\leq 2^{24Hn^2}.
$$

Taking $C=24$ proves the claim. $\blacksquare$

### Lemma 3. Many affine threshold functions

**Claim.** If $\mathrm{LTF}_m$ denotes the set of Boolean functions on $\{0,1\}^{m}$ strictly represented by affine linear forms, then for every $m\geq 2$,

$$
|\mathrm{LTF}_m|\geq 2^{m^2/9}.
$$

**Proof.** Put $k=\lfloor m/2\rfloor$. For every

$$
a=(a_1,\ldots,a_k)\in\{0,\ldots,2^k-1\}^k,
$$

define an affine form on variables $y,z\in\{0,1\}^k$, ignoring any remaining variable, by

$$
L_a(y,z)=\sum_{i=1}^k 2^{i-1}y_i-\sum_{j=1}^k a_jz_j-\frac12.
$$

The value before subtracting $1/2$ is always integral, so $L_a$ never vanishes on the cube.

If $a\neq b$, choose $j$ with $a_j<b_j$ after swapping the names if necessary. Since $a_j+1\leq 2^k-1$, choose $y$ whose binary value is $a_j+1$, and set $z=e_j$. Then

$$
L_a(y,e_j)=\frac12>0,
\qquad
L_b(y,e_j)\leq -\frac12<0.
$$

Thus distinct $a$ give distinct affine threshold functions. Therefore

$$
|\mathrm{LTF}_m|\geq (2^k)^k=2^{k^2}\geq 2^{m^2/9}
$$

for $m\geq 2$. $\blacksquare$

### Lemma 4. Many quadratic threshold functions

**Claim.** Let $\mathcal Q_n$ be the set of Boolean functions on $\{0,1\}^n$ with threshold degree at most $2$. For every $n\geq 4$,

$$
|\mathcal Q_n|\geq 2^{n^3/243}.
$$

**Proof.** Put $m=\lfloor n/2\rfloor$. Split the first $2m$ variables as $u,v\in\{0,1\}^m$ and ignore any remaining variables.

For each tuple $(g_1,\ldots,g_m)\in(\mathrm{LTF}_m)^m$, choose affine forms $\ell_i(v)$ that strictly represent $g_i$. This is possible because each $g_i$ is an affine threshold function, and the cube is finite. Let

$$
\mu=\min_{i,v}|\ell_i(v)|>0.
$$

Choose

$$
t\in(-\mu,\mu)
$$

avoiding the finite set

$$
\left\{-\sum_{i=1}^m u_i\ell_i(v):u,v\in\{0,1\}^m\right\}.
$$

Define

$$
q(u,v)=t+\sum_{i=1}^m u_i\ell_i(v).
$$

Then $q$ never vanishes on the cube, and $q$ has degree at most $2$. Moreover, for $u=e_i$,

$$
q(e_i,v)=t+\ell_i(v),
$$

whose sign agrees with the sign of $\ell_i(v)$ because $|t|<\mu\leq|\ell_i(v)|$.

Thus the quadratic threshold function represented by $q$ recovers every $g_i$ from its values on the slice $u=e_i$. Distinct tuples $(g_1,\ldots,g_m)$ therefore give distinct quadratic threshold functions. Hence, for $n\geq 4$,

$$
|\mathcal Q_n|
\geq
|\mathrm{LTF}_m|^m
\geq
2^{m^3/9}
\geq
2^{n^3/243}.
$$

$\blacksquare$

### Lemma 5. Pigeonhole separation

**Claim.** There are absolute constants $c>0$ and $n_0$ such that, for every $n\geq n_0$, some $f_n\in\mathcal Q_n$ satisfies

$$
\deg_{\pm}(f_n)=2
\qquad\text{and}\qquad
\mathrm{tChow}_{\pm}(f_n)\geq c n.
$$

**Proof.** Set

$$
a=\frac1{243}
$$

and choose

$$
c=\min\left\{1,\frac{a}{4C}\right\},
$$

where $C$ is the absolute constant from Lemma 2. Choose $n_0$ large enough that for every $n\geq n_0$, we have $n\geq 4$ and $H_n=\lfloor c n\rfloor\geq 1$.

For $n\geq n_0$, let

$$
H_n=\lfloor c n\rfloor.
$$

Then $1\leq H_n\leq n$, and Lemma 2 gives

$$
|\mathcal T_{n,H_n}|
\leq
2^{C H_n n^2}
\leq
2^{C c n^3}
\leq
2^{a n^3/4}.
$$

On the other hand, Lemma 4 gives

$$
|\mathcal Q_n|\geq 2^{a n^3}.
$$

Therefore

$$
|\mathcal T_{n,H_n}|<|\mathcal Q_n|.
$$

So there exists

$$
f_n\in\mathcal Q_n\setminus\mathcal T_{n,H_n}.
$$

Since $f_n\in\mathcal Q_n$,

$$
\deg_{\pm}(f_n)\leq 2.
$$

Since $f_n\notin\mathcal T_{n,H_n}$,

$$
\mathrm{tChow}_{\pm}(f_n)>H_n,
$$

and because $\mathrm{tChow}_{\pm}(f_n)$ is integer-valued when finite,

$$
\mathrm{tChow}_{\pm}(f_n)\geq H_n+1>c n.
$$

It remains to rule out threshold degree $0$ or $1$. Suppose $\deg_{\pm}(f_n)\leq 1$. Then some affine polynomial $p$ satisfies

$$
p(x)>0
\qquad\Longleftrightarrow\qquad
f_n(x)=1.
$$

But $p$ is an order-one tangential-Chow form: take

$$
\theta=0,
\qquad
D_1\equiv 1,
\qquad
N_1=p.
$$

Then $P=p$. Since $H_n\geq 1$, padding with $D_h\equiv 1$ and $N_h\equiv 0$ for $2\leq h\leq H_n$ gives an order-$H_n$ witness. Hence $f_n\in\mathcal T_{n,H_n}$, contradicting the choice of $f_n$.

Thus $\deg_{\pm}(f_n)>1$. Together with $\deg_{\pm}(f_n)\leq 2$, this yields

$$
\deg_{\pm}(f_n)=2.
$$

This proves the claim. $\blacksquare$

### Conclusion

Lemma 5 proves that for all sufficiently large $n$, there is a Boolean function $f_n:\{0,1\}^n\to\{0,1\}$ such that

$$
\deg_{\pm}(f_n)=2
\qquad\text{and}\qquad
\mathrm{tChow}_{\pm}(f_n)\geq c n.
$$

Therefore unrestricted tangential-Chow complexity can be linearly larger than ordinary threshold degree, even among quadratic threshold functions. $\blacksquare$

## Consequence

The lower sandwich inequality

$$
\deg_{\pm}(f)\leq \mathrm{tChow}_{\pm}(f)
$$

can be linearly strict. In particular, unrestricted tangential-Chow complexity is already a strictly finer measure than ordinary threshold degree on quadratic threshold functions.
