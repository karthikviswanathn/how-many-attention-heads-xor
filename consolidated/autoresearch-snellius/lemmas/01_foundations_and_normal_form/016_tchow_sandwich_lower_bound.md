# Unrestricted Tangential-Chow Sandwich Bound

## Statement

Let $f : \{0,1\}^{n} \to \{0,1\}$ and write $\sigma_f(x)=+1$ if $f(x)=1$ and $\sigma_f(x)=-1$ if $f(x)=0$. Let $H^{\ast}(f)$ be the least number of heads in the one-layer attention model of `model.md` computing $f$, with $H^{\ast}(f)=0$ for constant functions. Let $\deg_{\pm}(f)$ be the least degree of a real polynomial $p$ such that

$$
\sigma_f(x)p(x)>0
$$

for every $x \in \{0,1\}^{n}$.

Define $\mathrm{tChow}_{\pm}(f)$ to be the least $H \geq 0$ for which there are affine forms $D_1,\ldots,D_H,N_1,\ldots,N_H$ on $\mathbb{R}^{n}$ and a scalar $\theta \in \mathbb{R}$ such that

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x)
$$

strictly sign-represents $f$ on the Boolean cube, meaning

$$
\sigma_f(x)P(x)>0
$$

for all $x \in \{0,1\}^{n}$. For $H=0$, the product is $1$ and the sum is $0$.

Then

$$
\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{\ast}(f).
$$

Equivalently, unrestricted tangential-Chow threshold degree is an algebraic lower bound on head complexity that always dominates threshold degree.

## Proof

Let

$$
Q:=\{0,1\}^{n}.
$$

We use Lemma 14 in the following form. The invariant $\mathrm{MFdeg}_{\pm}(f)$ is defined by the same cleared-denominator expression as above, but with each affine pair $(N_h,D_h)$ required to be an admissible attention-head pair. Lemma 14 proves

$$
H^{\ast}(f)=\mathrm{MFdeg}_{\pm}(f).
$$

Every admissible attention-head pair is, in particular, a pair of affine forms.

### Lemma 1. Constant functions

If $f$ is constant, then

$$
\deg_{\pm}(f)=\mathrm{tChow}_{\pm}(f)=H^{\ast}(f)=0.
$$

**Proof.** If $f\equiv 1$, take $p=1$ and take the $H=0$ tangential-Chow witness $\theta=1$. If $f\equiv 0$, take $p=-1$ and take the $H=0$ tangential-Chow witness $\theta=-1$.

In both cases $\sigma_f(x)p(x)=1>0$ for every $x\in Q$, and the $H=0$ empty-product convention gives $P=\theta$, so $\sigma_f(x)P(x)>0$ for every $x\in Q$. Thus $\deg_{\pm}(f)\leq 0$ and $\mathrm{tChow}_{\pm}(f)\leq 0$. Since both invariants are minimized over nonnegative integers, they are equal to $0$. Also $H^{\ast}(f)=0$ for constant functions by convention. $\blacksquare$

Assume from now on that $f$ is nonconstant.

### Lemma 2. Relaxation to unrestricted tangential-Chow witnesses

$$
\mathrm{tChow}_{\pm}(f)\leq H^{\ast}(f).
$$

**Proof.** Set

$$
M:=\mathrm{MFdeg}_{\pm}(f).
$$

By Lemma 14,

$$
M=H^{\ast}(f).
$$

By the definition of $\mathrm{MFdeg}_{\pm}(f)$, there are admissible affine pairs $(N_h,D_h)$ for $1\leq h\leq M$ and a scalar $\theta\in\mathbb{R}$ such that

$$
P(x)=\theta\prod_{h=1}^{M}D_h(x)+\sum_{h=1}^{M}N_h(x)\prod_{g\neq h}D_g(x)
$$

satisfies

$$
\sigma_f(x)P(x)>0
$$

for every $x\in Q$.

The unrestricted invariant $\mathrm{tChow}_{\pm}(f)$ imposes no admissibility restriction on the affine forms. Therefore the same $D_h$, $N_h$, $\theta$, and $P$ form a valid unrestricted tangential-Chow witness with $M$ factors. Since $\mathrm{tChow}_{\pm}(f)$ is the least number of factors admitting such a witness,

$$
\mathrm{tChow}_{\pm}(f)\leq M=H^{\ast}(f).
$$

$\blacksquare$

### Lemma 3. Degree of an unrestricted witness

$$
\deg_{\pm}(f)\leq \mathrm{tChow}_{\pm}(f).
$$

**Proof.** Set

$$
T:=\mathrm{tChow}_{\pm}(f).
$$

By Lemma 2, $T$ is finite. Choose affine forms $D_1,\ldots,D_T,N_1,\ldots,N_T$ and a scalar $\theta\in\mathbb{R}$ such that

$$
P(x)=\theta\prod_{h=1}^{T}D_h(x)+\sum_{h=1}^{T}N_h(x)\prod_{g\neq h}D_g(x)
$$

satisfies

$$
\sigma_f(x)P(x)>0
$$

for every $x\in Q$.

Let $\mathcal P_{\leq d}$ denote the real polynomials in $x_1,\ldots,x_n$ of total degree at most $d$. Every affine form belongs to $\mathcal P_{\leq 1}$, and the product of an element of $\mathcal P_{\leq a}$ with an element of $\mathcal P_{\leq b}$ belongs to $\mathcal P_{\leq a+b}$.

If $T=0$, then the empty product is $1$ and the sum is empty, so $P=\theta\in\mathcal P_{\leq 0}$.

If $T\geq 1$, then

$$
\prod_{h=1}^{T}D_h\in\mathcal P_{\leq T},
$$

and, for each $h$,

$$
N_h\prod_{g\neq h}D_g\in\mathcal P_{\leq T},
$$

because this term is a product of $T$ affine forms. Scalar multiplication and finite sums preserve the degree bound, so in every case

$$
P\in\mathcal P_{\leq T}.
$$

Thus $P$ is a real polynomial of degree at most $T$ that strictly sign-represents $f$ on the Boolean cube. By the definition of threshold degree,

$$
\deg_{\pm}(f)\leq T=\mathrm{tChow}_{\pm}(f).
$$

$\blacksquare$

### Conclusion

Lemma 2 and Lemma 3 give

$$
\deg_{\pm}(f)\leq \mathrm{tChow}_{\pm}(f)
\qquad\text{and}\qquad
\mathrm{tChow}_{\pm}(f)\leq H^{\ast}(f).
$$

Together with Lemma 1 for the constant case, this proves

$$
\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{\ast}(f)
$$

for every Boolean function $f$. $\blacksquare$

## Consequence

The unrestricted tangential-Chow invariant gives a model-independent algebraic lower bound on attention head complexity:

$$
\mathrm{tChow}_{\pm}(f)\leq H^{\ast}(f).
$$

It is at least as strong as the ordinary threshold-degree lower bound, since

$$
\deg_{\pm}(f)\leq \mathrm{tChow}_{\pm}(f).
$$

Thus any lower bound on $\mathrm{tChow}_{\pm}(f)$ is automatically a lower bound on $H^{\ast}(f)$, and any threshold-degree lower bound also passes through this stronger middle invariant.
