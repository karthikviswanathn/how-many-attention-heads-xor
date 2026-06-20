# Split Affine-Cylinder Cost

## Statement

Let

$$
f:\{0,1\}^{n}\to\{0,1\}
$$

with $n\geq1$. Fix a split coordinate $j$ and write the inputs as

$$
(z,y)\in\{0,1\}\times\{0,1\}^{n-1}.
$$

For $b\in\{0,1\}$, let

$$
f_b(y):=f(b,y).
$$

Given strict affine-cylinder scores $S_0,S_1$ for the two cofactors, written as in [111_affine_cylinder_cofactor_interpolation.md](111_affine_cylinder_cofactor_interpolation.md), define their split interpolation cost by

$$
\begin{aligned}
I(S_0,S_1)
:={}&
\eta(A_0,A_1)
+
\lvert\Delta_{\mathrm{lin}}\rvert \\
&+
\sum_{\gamma=(P,N)\in\Gamma_0}\kappa(P,N)
+
\sum_{\gamma=(P,N)\in\Delta_{\mathrm{cyl}}}\kappa(P\cup\{z\},N).
\end{aligned}
$$

Let

$$
\operatorname{sactc}_{j}(f)
$$

be the minimum of $I(S_0,S_1)$ over all choices of strict affine-cylinder scores for $f_0$ and $f_1$ along the split coordinate $j$, and define

$$
\operatorname{sactc}(f)
:=
\min_{1\leq j\leq n}\operatorname{sactc}_{j}(f).
$$

Then

$$
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\operatorname{sactc}(f).
$$

If

$$
\operatorname{sactc}(f)\leq2,
$$

then

$$
H^{*}(f)
=
\begin{cases}
0, & \text{if } f \text{ is constant},\\
1, & \text{if } f \text{ is a nonconstant LTF},\\
2, & \text{otherwise}.
\end{cases}
$$

> **Interpretation.** The split affine-cylinder cost is an optimized recursive certificate. It is not a new lower bound on $\operatorname{actc}$; it is a structured way to produce affine-cylinder certificates by interpolating two cofactors.

## Proof

For every split coordinate $j$, the two cofactors have strict affine-cylinder scores because $\operatorname{actc}$ is finite for every Boolean function by [103_affine_cylinder_threshold_cost.md](103_affine_cylinder_threshold_cost.md). Hence the minimum defining $\operatorname{sactc}_{j}(f)$ is over a nonempty set of nonnegative integers.

Fix a split coordinate $j$ and strict affine-cylinder cofactor scores $S_0,S_1$. Lemma [111_affine_cylinder_cofactor_interpolation.md](111_affine_cylinder_cofactor_interpolation.md) gives

$$
\operatorname{actc}(f)\leq I(S_0,S_1).
$$

Minimizing first over the two cofactor scores and then over the split coordinate gives

$$
\operatorname{actc}(f)\leq\operatorname{sactc}(f).
$$

The affine-cylinder threshold-cost theorem [103_affine_cylinder_threshold_cost.md](103_affine_cylinder_threshold_cost.md) gives

$$
H^{*}(f)\leq\operatorname{actc}(f).
$$

Combining the two inequalities proves

$$
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\operatorname{sactc}(f).
$$

If $\operatorname{sactc}(f)\leq2$, then $\operatorname{actc}(f)\leq2$. The low affine-cylinder exactness theorem [109_low_affine_cylinder_cost_exactness.md](109_low_affine_cylinder_cost_exactness.md) now gives the displayed constant, nonconstant LTF, or two-head split. $\blacksquare$

## Consequences

This packages Lemma 111 as a reusable invariant for recursive search. To prove a small head upper bound, it is enough to find one coordinate whose two cofactors admit affine-cylinder scores with small base cost and few changed coefficients.

The exact low-cost corollary is especially useful: every nonconstant non-LTF with $\operatorname{sactc}(f)\leq2$ is exactly two-head.
