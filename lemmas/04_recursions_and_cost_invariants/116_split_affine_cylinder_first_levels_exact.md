# Split Affine-Cylinder First Levels Are Exact

## Statement

Let

$$
f:\{0,1\}^{n}\to\{0,1\}
$$

with $n\geq1$. Then

$$
\operatorname{sactc}(f)=0
\qquad\Longleftrightarrow\qquad
f \text{ is constant},
$$

and

$$
\operatorname{sactc}(f)=1
\qquad\Longleftrightarrow\qquad
f \text{ is a nonconstant LTF}.
$$

Equivalently,

$$
\operatorname{sactc}(f)\geq2
\qquad\Longleftrightarrow\qquad
f \text{ is neither constant nor a nonconstant LTF}.
$$

> **Interpretation.** Optimizing over cofactor interpolations does not distort the constant and one-head layers.

## Proof

The split affine-cylinder cost theorem [112_split_affine_cylinder_cost.md](112_split_affine_cylinder_cost.md) gives

$$
\operatorname{actc}(f)\leq\operatorname{sactc}(f).
$$

If $\operatorname{sactc}(f)=0$, then $\operatorname{actc}(f)=0$, so $f$ is constant by [115_affine_cylinder_first_levels_exact.md](115_affine_cylinder_first_levels_exact.md).

Conversely, if $f$ is constant, choose the same constant strict score on both cofactors. The interpolation cost has no affine part, no changed slopes, and no cylinders. Therefore

$$
\operatorname{sactc}(f)=0.
$$

Now let $f$ be a nonconstant LTF. Choose a strict affine separator

$$
A(x)=a+\sum_{i=1}^{n}\beta_i x_i.
$$

Fix any split coordinate and write $x=(z,y)$. Then

$$
A(z,y)=a+\beta_z z+\sum_i\alpha_i y_i,
$$

where the sum is over the remaining coordinates. The two cofactor affine scores are

$$
A_0(y)=a+\sum_i\alpha_i y_i,
\qquad
A_1(y)=a+\beta_z+\sum_i\alpha_i y_i.
$$

There are no cylinder terms and no changed affine slopes. Since $f$ is nonconstant, either $\beta_z\neq0$ or some $\alpha_i\neq0$. Hence the interpolation affine indicator satisfies

$$
\eta(A_0,A_1)=1.
$$

Thus this split certificate has cost $1$, and

$$
\operatorname{sactc}(f)\leq1.
$$

The function is nonconstant, so the first part rules out $\operatorname{sactc}(f)=0$. Hence

$$
\operatorname{sactc}(f)=1.
$$

Conversely, if $\operatorname{sactc}(f)=1$, then

$$
\operatorname{actc}(f)\leq1.
$$

By [115_affine_cylinder_first_levels_exact.md](115_affine_cylinder_first_levels_exact.md), $f$ is either constant or a nonconstant LTF. Since $\operatorname{sactc}(f)\neq0$, the first part rules out the constant case. Thus $f$ is a nonconstant LTF.

The last equivalence follows by negating the characterization that $\operatorname{sactc}(f)\leq1$ exactly for constants and nonconstant LTFs. $\blacksquare$

## Consequences

For $n\geq1$, the split invariant has no artificial low-level slack:

$$
\operatorname{sactc}(f)
=
H^{*}(f)
\qquad
\text{for }
\operatorname{sactc}(f)\in\{0,1\}.
$$

The first nontrivial split certificates are exactly the cost-$2$ certificates, and those are exact two-head certificates for non-LTFs by [112_split_affine_cylinder_cost.md](112_split_affine_cylinder_cost.md).
