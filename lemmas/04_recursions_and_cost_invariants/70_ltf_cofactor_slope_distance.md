# LTF Cofactor Slope Distance

## Statement

Let

$$
f:\{0,1\}^{n}\to\{0,1\},
$$

and split off one coordinate, writing inputs as $(z,y)\in\{0,1\}\times\{0,1\}^{n-1}$. Let

$$
f_0(y):=f(0,y),
\qquad
f_1(y):=f(1,y).
$$

Suppose $f_0$ and $f_1$ have affine sign representations

$$
L_b(y)
=
\beta_b+\sum_{i=1}^{n-1}\alpha_{b,i}y_i
\qquad
(b\in\{0,1\}),
$$

meaning

$$
f_b(y)=1
\qquad\Longleftrightarrow\qquad
L_b(y)>0
$$

on the $(n-1)$-cube. Let

$$
\Delta(L_0,L_1)
:=
\left\{
i\in\{1,\ldots,n-1\}:
\alpha_{0,i}\neq\alpha_{1,i}
\right\},
$$

and set

$$
t:=\lvert\Delta(L_0,L_1)\rvert.
$$

Then

$$
H^{*}(f)\leq1+t.
$$

In particular, if both cofactors are constants or linear threshold functions, then

$$
H^{*}(f)\leq n.
$$

If the affine sign representations can be chosen with $t=0$, then $f$ is constant or a nonconstant linear threshold function, so

$$
H^{*}(f)\in\{0,1\}.
$$

If they can be chosen with $t\leq1$, then

$$
H^{*}(f)
=
\begin{cases}
0 & \text{if } f \text{ is constant},\\
1 & \text{if } f \text{ is a nonconstant linear threshold function},\\
2 & \text{otherwise}.
\end{cases}
$$

> **Interpretation.** When the two slices across one bit are LTFs, the cost is controlled by how many affine slopes change across the split. The constant term and all unchanged slopes are free inside one affine head; each changed slope creates one mixed monomial $zy_i$.

## Proof

Define the cofactor interpolation polynomial

$$
P(z,y):=(1-z)L_0(y)+zL_1(y).
$$

Then $P(0,y)=L_0(y)$ and $P(1,y)=L_1(y)$, so

$$
f(z,y)=1
\qquad\Longleftrightarrow\qquad
P(z,y)>0.
$$

Thus $P$ sign-represents $f$.

Expanding,

$$
\begin{aligned}
P(z,y)
&=L_0(y)+z\bigl(L_1(y)-L_0(y)\bigr)\\
&=
\beta_0+\sum_{i=1}^{n-1}\alpha_{0,i}y_i
+z(\beta_1-\beta_0)
+\sum_{i\in\Delta(L_0,L_1)}(\alpha_{1,i}-\alpha_{0,i})zy_i.
\end{aligned}
$$

The first three terms are affine in $(z,y)$. The only nonlinear monomials are the $t$ mixed monomials

$$
zy_i
\qquad
(i\in\Delta(L_0,L_1)).
$$

Therefore

$$
\operatorname{afs}(P)\leq1+t.
$$

The affine-free sparsity theorem [42_affine_free_sparsity_upper_bound.md](42_affine_free_sparsity_upper_bound.md) gives

$$
H^{*}(f)\leq1+t.
$$

If both cofactors are constants or LTFs, affine sign representations exist and $t\leq n-1$, so $H^{*}(f)\leq n$.

If $t=0$, then $P$ is affine in $(z,y)$. Hence $f$ is constant or a nonconstant LTF, giving $H^{*}(f)\in\{0,1\}$ by the one-head characterization [05_linear_fractional_normal_form.md](05_linear_fractional_normal_form.md).

If $t\leq1$, then $\operatorname{afs}(P)\leq2$. The exact classification follows from the low affine-free support theorem [64_low_affine_free_support_exact.md](64_low_affine_free_support_exact.md). $\blacksquare$

## Consequences

For functions with LTF cofactors along one split, define the slope cost of a chosen pair of affine cofactor separators as the number of coordinates whose linear coefficients differ. Minimizing this cost over all separator choices gives a concrete invariant $\sigma_z(f)$ for that split, and the theorem gives

$$
H^{*}(f)\leq1+\sigma_z(f).
$$

This is useful because affine separators are not unique. A bad pair of separators may change many slopes, while a better pair can reveal that the glued function is already an LTF or exactly two-head.
