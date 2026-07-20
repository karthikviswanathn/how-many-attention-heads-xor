# Head Hierarchy Pattern

## Main Pattern

Let $\mathcal{H}_H$ be the class of Boolean functions computable with at most $H$ heads.

The exact normal form says that $f \in \mathcal{H}_H$ if and only if there are $H$ one-head atoms

$$
\phi_h(x) = \frac{A_h(x)}{D_h(x)}
$$

and a constant $c$ such that

$$
f(x) = 1
\qquad \Longleftrightarrow \qquad
c + \sum_{h=1}^{H} \phi_h(x) > 0.
$$

Here $A_h$ is affine on the Boolean cube and $D_h$ is a positive one-head denominator. Concretely,

$$
D_h(x) = \gamma_h + \sum_{i=1}^{n} \rho_{h,i}\alpha_h^{x_i},
\qquad
\gamma_h > 0,
\qquad
\rho_{h,i} > 0,
\qquad
\alpha_h > 0.
$$

After expanding on $\{0,1\}^n$, each $D_h$ is a positive affine function whose variable coefficients all have the same sign, unless $\alpha_h = 1$, in which case $D_h$ is constant.

Clearing denominators gives the equivalent sign polynomial

$$
P(x)
=
c\prod_{h=1}^{H}D_h(x)
+
\sum_{h=1}^{H}
A_h(x)\prod_{g \neq h}D_g(x).
$$

Since $\prod_h D_h(x) > 0$ on the cube, $P$ has the same signs as the head score. Thus every $H$-head function has threshold degree at most $H$, but it is not an arbitrary degree-$H$ polynomial threshold function. It is a degree-$H$ polynomial with an $H$-pole decomposition.

So the hierarchy is best viewed as:

$$
\mathcal{H}_H
=
\left\{
\text{sign patterns of sums of } H
\text{ affine-over-positive-unate-affine atoms}
\right\}.
$$

## First Levels

The first two levels are exact.

$$
\mathcal{H}_0
=
\{\text{constant functions}\}.
$$

$$
\mathcal{H}_1
=
\{\text{linear threshold functions}\}.
$$

The next level is already a restricted quadratic threshold class. A two-head score clears to

$$
P(x)
=
cD_1(x)D_2(x)
+ A_1(x)D_2(x)
+ A_2(x)D_1(x).
$$

Thus $\mathcal{H}_2$ consists of sign patterns of quadratic polynomials that admit this two-pole form with positive one-head denominators.

For fixed denominators $D_1,\ldots,D_H$, the cleared numerator space has effective dimension at most

$$
Hn + 1.
$$

This comes from the $H$ affine numerators plus the constant term, modulo the redundancy from adding multiples of $D_h$ to the corresponding numerator. For generic denominators this bound is the expected dimension until capped by the $2^n$ values on the cube.

This is much smaller than the space of all degree-$H$ polynomials once $n$ is large. This explains why threshold degree is a lower bound but should not be expected to characterize head complexity in general.

## Three-Bit Consequence

For $n = 3$, the restricted quadratic issue disappears. Every quadratic polynomial on the three-bit cube admits a two-pole decomposition.

Let

$$
D_1(x) = 10 + x_1 + x_2 + x_3,
\qquad
D_2(x) = 20 + 2x_1 + 3x_2 + 5x_3.
$$

Both are valid positive one-head denominators. Indeed, take $\alpha = 2$. For $D_1$, choose $\rho = (1,1,1)$ and $\gamma = 7$. For $D_2$, choose $\rho = (2,3,5)$ and $\gamma = 10$.

Let $\mathcal{A}$ be the vector space of affine functions in $x_1,x_2,x_3$. The space of quadratic polynomials on the Boolean cube has basis

$$
1,\ x_1,\ x_2,\ x_3,\ x_1x_2,\ x_1x_3,\ x_2x_3.
$$

The seven columns

$$
D_1,\ x_1D_1,\ x_2D_1,\ x_3D_1,\ D_2,\ x_1D_2,\ x_2D_2
$$

have coordinate matrix

$$
\begin{pmatrix}
10 & 0 & 0 & 0 & 20 & 0 & 0 \\
1 & 11 & 0 & 0 & 2 & 22 & 0 \\
1 & 0 & 11 & 0 & 3 & 0 & 23 \\
1 & 0 & 0 & 11 & 5 & 0 & 0 \\
0 & 1 & 1 & 0 & 0 & 3 & 2 \\
0 & 1 & 0 & 1 & 0 & 5 & 0 \\
0 & 0 & 1 & 1 & 0 & 0 & 5
\end{pmatrix}
$$

in that basis. Its determinant is

$$
-1320 \neq 0.
$$

Therefore

$$
\mathcal{A}D_1 + \mathcal{A}D_2
$$

is the full space of quadratic polynomials on the three-bit cube. If $Q$ is any quadratic sign representation, write

$$
Q = U D_1 + W D_2
$$

with affine $U,W$. Then

$$
\frac{W}{D_1} + \frac{U}{D_2}
$$

has the same sign as $Q$, because $D_1D_2 > 0$. Hence two heads realize every three-bit quadratic threshold function.

The resulting three-bit picture is:

$$
H^{*}(f) = 0
\quad \Longleftrightarrow \quad
f \text{ is constant},
$$

$$
H^{*}(f) = 1
\quad \Longleftrightarrow \quad
f \text{ is a nonconstant linear threshold function},
$$

$$
H^{*}(f) = 3
\quad \Longleftrightarrow \quad
f \text{ is parity or its complement}.
$$

All remaining three-bit functions have $H^{*}(f) = 2$.

A finite threshold-degree check over all $256$ three-bit truth tables gives the distribution

$$
\deg_{\pm}(f) = 0: 2,
\qquad
\deg_{\pm}(f) = 1: 102,
\qquad
\deg_{\pm}(f) = 2: 150,
\qquad
\deg_{\pm}(f) = 3: 2.
$$

The two degree-three functions are parity and its complement.

## Positive Parallel Subpattern

There is also a clean sufficient condition that explains the symmetric theorem.

Suppose

$$
t(x) = \sum_{i=1}^{n}\lambda_i x_i,
\qquad
\lambda_i > 0,
$$

and $f(x) = F(t(x))$. Order the distinct values of $t$ on the cube and count the number $C_t(F)$ of label changes along that ordered profile. Then

$$
H^{*}(f) \leq C_t(F).
$$

The proof is one-dimensional: build a univariate sign polynomial with one root between each label change, divide by a positive denominator, and decompose into partial fractions

$$
c + \sum_{j=1}^{C_t(F)} \frac{b_j}{t(x)+r_j}.
$$

Each reciprocal term is one head.

For symmetric functions, $t(x)=\lvert x\rvert$, and the threshold-degree lower bound matches this construction. Hence

$$
H^{*}(f) = \text{number of sign changes in the Hamming-weight profile}.
$$

This gives:

- monotone symmetric thresholds: $1$ head,
- exact internal Hamming weights: $2$ heads,
- $n$-bit parity: $n$ heads.

## Working Conjectural Picture

The useful mental model is:

1. One head gives one affine-over-positive-unate-affine atom.
2. $H$ heads give an $H$-pole rational threshold function.
3. Clearing denominators gives a degree-$H$ polynomial threshold lower bound.
4. Exact equality with threshold degree holds for the first levels, for symmetric functions, and for all three-bit functions.
5. In general, head complexity is finer than threshold degree because the degree-$H$ sign polynomial must admit the special $H$-pole decomposition.
