# Split Affine-Cylinder Refines Split Affine-Free Support

## Statement

For every Boolean function

$$
f:\{0,1\}^{n}\to\{0,1\}
$$

with $n\geq1$,

$$
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\operatorname{sactc}(f)
\leq
\operatorname{scafs}_{\pm}(f),
$$

where $\operatorname{scafs}_{\pm}$ is the split affine-free support invariant from [72_split_affine_free_support_invariant.md](72_split_affine_free_support_invariant.md).

Consequently, every split affine-free support certificate is also a split affine-cylinder certificate of no larger cost.

> **Interpretation.** The affine-cylinder split invariant is a genuine refinement of the earlier split sparse-PTF recursion. It keeps all positive monomial certificates, and it can also exploit mixed-literal cylinders with cheap local expansion.

## Proof

Fix a split coordinate and write inputs as

$$
(z,y)\in\{0,1\}\times\{0,1\}^{n-1}.
$$

Let $P_0,P_1$ be strict sign polynomials for the two cofactors, written as in [72_split_affine_free_support_invariant.md](72_split_affine_free_support_invariant.md):

$$
P_b(y)
=
c_b+\sum_{i=1}^{n-1}\alpha_{b,i}y_i
+
\sum_{\substack{S\subseteq\{1,\ldots,n-1\}\\ \lvert S\rvert\geq2}}
a_{b,S}\prod_{i\in S}y_i.
$$

View each $P_b$ as an affine-cylinder score by taking

$$
A_b(y):=c_b+\sum_{i=1}^{n-1}\alpha_{b,i}y_i
$$

and replacing every nonzero nonlinear monomial by the cylinder

$$
\prod_{i\in S}y_i=C_{S,\varnothing}(y).
$$

For such a base nonlinear monomial,

$$
\kappa(S,\varnothing)=1.
$$

If the coefficient of the nonlinear monomial changes across the split, the interpolation term is

$$
z\prod_{i\in S}y_i=C_{S\cup\{z\},\varnothing}(z,y),
$$

and again

$$
\kappa(S\cup\{z\},\varnothing)=1.
$$

Therefore the affine-cylinder interpolation cost of these two scores is exactly the split affine-free support cost of the two polynomials:

$$
I(P_0,P_1)
=
\lambda(P_0,P_1)
+
\lvert\mathcal{N}_0\rvert
+
\lvert\mathcal{L}_{\Delta}\rvert
+
\lvert\mathcal{N}_{\Delta}\rvert.
$$

Taking the minimum over $P_0,P_1$ for this split gives

$$
\operatorname{sactc}_{j}(f)
\leq
\operatorname{scafs}_{\pm,j}(f).
$$

Taking the minimum over split coordinates yields

$$
\operatorname{sactc}(f)
\leq
\operatorname{scafs}_{\pm}(f).
$$

The split affine-cylinder cost lemma [106_split_affine_cylinder_cost.md](106_split_affine_cylinder_cost.md) gives

$$
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\operatorname{sactc}(f).
$$

Combining the two chains proves the theorem. $\blacksquare$

## Consequences

The old cofactor sparse-polynomial route now factors through the affine-cylinder split invariant:

$$
H^{*}(f)
\leq
\operatorname{sactc}(f)
\leq
\operatorname{scafs}_{\pm}(f).
$$

Thus any improvement to local cylinder scoring immediately improves the recursive split search without losing any certificate already covered by split affine-free support.
