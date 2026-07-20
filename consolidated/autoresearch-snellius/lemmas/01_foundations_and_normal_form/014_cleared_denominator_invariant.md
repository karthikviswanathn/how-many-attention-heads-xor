# Cleared-Denominator Polynomial Invariant

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md). Let $f : \{0,1\}^{n} \to \{0,1\}$, and let $H^{\ast}(f)$ be the least number of attention heads needed to compute $f$ with a final strict threshold at the query token.

Call an affine pair $(N,D)$ admissible if it is exactly one of the affine one-head pairs characterized in [013_affine_atom_dictionary.md](013_affine_atom_dictionary.md). Equivalently, write

$$
N(x)=a_0+\sum_{i=1}^{n}a_i x_i,
\qquad
D(x)=d_0+\sum_{i=1}^{n}d_i x_i.
$$

Then $D(x)>0$ on $\{0,1\}^{n}$, and for $n\geq 1$ its denominator class is exactly one of the following:

1. $D$ is constant positive, meaning $d_i=0$ for every $i$ and $d_0>0$.

2. Every coordinate coefficient is strictly positive, meaning $d_i>0$ for every $i$, and $d_0>0$.

3. Every coordinate coefficient is strictly negative, meaning $d_i<0$ for every $i$, and the all-ones value is positive:

$$
d_0+\sum_{i=1}^{n}d_i>0.
$$

For $n=0$, only the constant positive class occurs. If $D$ is nonconstant, then $N$ is an arbitrary affine function. If $D$ is constant, then the coordinate coefficients of $N$ are all strictly positive, all strictly negative, or all zero, while the constant coefficient of $N$ is arbitrary.

Define $\mathrm{MFdeg}_{\pm}(f)$ to be the least integer $H\geq 0$ for which there exist admissible affine pairs $(N_h,D_h)$, $1\leq h\leq H$, and a real constant $\theta$ such that

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x)
$$

strictly sign-represents $f$ on $\{0,1\}^{n}$, meaning $P(x)>0$ when $f(x)=1$ and $P(x)<0$ when $f(x)=0$. For $H=0$, the empty product is $1$ and the sum is $0$.

Then

$$
H^{\ast}(f)=\mathrm{MFdeg}_{\pm}(f).
$$

## Proof

Let

$$
Q:=\{0,1\}^{n}.
$$

Let $L_{\mathrm{frac}}(f)$ be the least integer $H\geq 0$ such that there are one-head atoms $\phi_1,\ldots,\phi_H$ and a constant $c\in\mathbb{R}$ with

$$
f(x)=1 \quad\Longleftrightarrow\quad c+\sum_{h=1}^{H}\phi_h(x)>0
$$

for every $x\in Q$. By [010_linear_fractional_normal_form.md](010_linear_fractional_normal_form.md),

$$
H^{\ast}(f)=L_{\mathrm{frac}}(f).
$$

By [013_affine_atom_dictionary.md](013_affine_atom_dictionary.md), each one-head atom has the form

$$
\phi_h(x)=\frac{N_h(x)}{D_h(x)}
$$

with $(N_h,D_h)$ admissible and $D_h(x)>0$ on $Q$. Conversely, every admissible pair gives a one-head atom through the ratio $N_h/D_h$.

If $f\equiv 1$, then $L_{\mathrm{frac}}(f)=0$ by taking the constant score $1$, and $\mathrm{MFdeg}_{\pm}(f)=0$ by taking $H=0$ and $\theta=1$. If $f\equiv 0$, then $L_{\mathrm{frac}}(f)=0$ by taking the constant score $-1$, and $\mathrm{MFdeg}_{\pm}(f)=0$ by taking $H=0$ and $\theta=-1$. Hence the theorem holds for constant $f$.

Assume from now on that $f$ is nonconstant.

### Lemma 1. Clearing identity

Let $(N_h,D_h)$, $1\leq h\leq H$, be admissible pairs, and let $\theta\in\mathbb{R}$. Define

$$
B(x):=\prod_{h=1}^{H}D_h(x),
\qquad
R(x):=\theta+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}.
$$

Then $B(x)>0$ for every $x\in Q$, and

$$
B(x)R(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x).
$$

**Proof.** Each admissible pair has $D_h(x)>0$ on $Q$, so the finite product $B(x)$ is positive on $Q$.

For each $x\in Q$,

$$
\begin{aligned}
B(x)R(x)
&=\left(\prod_{h=1}^{H}D_h(x)\right)
\left(\theta+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}\right) \\
&=\theta\prod_{h=1}^{H}D_h(x)
+\sum_{h=1}^{H}N_h(x)\frac{\prod_{j=1}^{H}D_j(x)}{D_h(x)} \\
&=\theta\prod_{h=1}^{H}D_h(x)
+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x).
\end{aligned}
$$

The cancellation is valid because each $D_h(x)$ is positive, hence nonzero. $\blacksquare$

### Lemma 2. Strict perturbation

Suppose one has admissible pairs $(N_h,D_h)$, $1\leq h\leq H$, and $c\in\mathbb{R}$ such that

$$
f(x)=1 \quad\Longleftrightarrow\quad c+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}>0
$$

for every $x\in Q$. Then there is a real $\theta$ such that

$$
\theta+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}>0
\quad\text{when } f(x)=1,
$$

and

$$
\theta+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}<0
\quad\text{when } f(x)=0.
$$

**Proof.** Put

$$
S(x):=c+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}.
$$

Since $f$ is nonconstant, the set

$$
Q_1:=\{x\in Q:f(x)=1\}
$$

is nonempty. For every $x\in Q_1$, the assumed representation gives $S(x)>0$. Since $Q_1$ is finite, the minimum

$$
m:=\min_{x\in Q_1}S(x)
$$

exists and satisfies $m>0$.

Choose

$$
\varepsilon:=\frac{m}{2},
\qquad
\theta:=c-\varepsilon.
$$

Then $0<\varepsilon<m$. If $f(x)=1$, then $x\in Q_1$ and

$$
\theta+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}
=S(x)-\varepsilon
\geq m-\varepsilon
>0.
$$

If $f(x)=0$, then the implication $S(x)>0 \Rightarrow f(x)=1$ gives $S(x)\leq 0$. Hence

$$
\theta+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}
=S(x)-\varepsilon
\leq -\varepsilon
<0.
$$

This proves the strict two-sided sign separation. $\blacksquare$

### Lemma 3. From heads to cleared polynomials

$$
\mathrm{MFdeg}_{\pm}(f)\leq H^{\ast}(f).
$$

**Proof.** Set

$$
A:=H^{\ast}(f).
$$

By the linear-fractional normal form and the affine atom dictionary, there are admissible pairs $(N_h,D_h)$, $1\leq h\leq A$, and a constant $c\in\mathbb{R}$ such that

$$
f(x)=1 \quad\Longleftrightarrow\quad c+\sum_{h=1}^{A}\frac{N_h(x)}{D_h(x)}>0
$$

for every $x\in Q$.

By Lemma 2, after replacing $c$ by some $\theta$, the rational score

$$
R(x):=\theta+\sum_{h=1}^{A}\frac{N_h(x)}{D_h(x)}
$$

is positive on $f^{-1}(1)$ and negative on $f^{-1}(0)$. Let

$$
P(x):=\theta\prod_{h=1}^{A}D_h(x)+\sum_{h=1}^{A}N_h(x)\prod_{g\neq h}D_g(x).
$$

By Lemma 1, $P(x)=B(x)R(x)$ where $B(x)=\prod_{h=1}^{A}D_h(x)>0$ on $Q$. Multiplication by $B(x)$ preserves strict signs. Thus $P$ strictly sign-represents $f$ using $A$ admissible pairs.

Therefore

$$
\mathrm{MFdeg}_{\pm}(f)\leq A=H^{\ast}(f).
$$

$\blacksquare$

### Lemma 4. From cleared polynomials to heads

$$
H^{\ast}(f)\leq \mathrm{MFdeg}_{\pm}(f).
$$

**Proof.** Set

$$
M:=\mathrm{MFdeg}_{\pm}(f).
$$

By definition of $M$, there are admissible pairs $(N_h,D_h)$, $1\leq h\leq M$, and $\theta\in\mathbb{R}$ such that

$$
P(x)=\theta\prod_{h=1}^{M}D_h(x)+\sum_{h=1}^{M}N_h(x)\prod_{g\neq h}D_g(x)
$$

strictly sign-represents $f$ on $Q$.

Let

$$
B(x):=\prod_{h=1}^{M}D_h(x).
$$

Admissibility gives $D_h(x)>0$ on $Q$, so $B(x)>0$ on $Q$. Define

$$
R(x):=\frac{P(x)}{B(x)}.
$$

By Lemma 1, for every $x\in Q$,

$$
R(x)=\theta+\sum_{h=1}^{M}\frac{N_h(x)}{D_h(x)}.
$$

Since division by the positive number $B(x)$ preserves strict signs, $R(x)>0$ whenever $f(x)=1$ and $R(x)<0$ whenever $f(x)=0$. Because $f$ is Boolean-valued,

$$
f(x)=1 \quad\Longleftrightarrow\quad R(x)>0
$$

for every $x\in Q$.

By the converse direction of the affine atom dictionary, each ratio $N_h/D_h$ is a one-head atom. Hence $f$ is computed by a constant plus $M$ one-head atoms, so

$$
L_{\mathrm{frac}}(f)\leq M.
$$

Using $H^{\ast}(f)=L_{\mathrm{frac}}(f)$, we get

$$
H^{\ast}(f)\leq M=\mathrm{MFdeg}_{\pm}(f).
$$

$\blacksquare$

### Conclusion

Lemmas 3 and 4 give

$$
\mathrm{MFdeg}_{\pm}(f)\leq H^{\ast}(f)
\qquad\text{and}\qquad
H^{\ast}(f)\leq \mathrm{MFdeg}_{\pm}(f).
$$

Therefore

$$
H^{\ast}(f)=\mathrm{MFdeg}_{\pm}(f).
$$

This proves the theorem. $\blacksquare$

## Consequence

The head complexity $H^{\ast}(f)$ is exactly the least number of admissible affine denominator factors needed so that a polynomial in the cleared tangent form

$$
\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x)
$$

strictly sign-represents $f$ on the Boolean cube.

Since each $N_h$ and $D_h$ is affine, every such witness has degree at most $H$. Thus the threshold-degree lower bound $\deg_{\pm}(f)\leq H^{\ast}(f)$ follows again from this invariant. The extra content is the admissible factor structure, which is the input for the tangential-Chow frontier node.
