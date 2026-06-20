# Cylinder-Threshold Cost And PTF Sparsity

## Statement

Let $\operatorname{ptfsp}(f)$ be the least number of nonconstant monomials in a real multilinear polynomial that sign-represents $f$ on the Boolean cube. Then

$$
\operatorname{ctc}(f)\leq\operatorname{ptfsp}(f).
$$

Consequently, if $\deg_{\pm}(f)\leq d$, then

$$
\operatorname{ctc}(f)
\leq
\sum_{r=1}^{d}\binom{n}{r}.
$$

Combining with Lemma 99 gives

$$
H^{*}(f)
\leq
\operatorname{ctc}(f)
\leq
\operatorname{ptfsp}(f).
$$

> **Interpretation.** Sparse polynomial threshold representations are special cylinder-threshold representations. Thus $\operatorname{ctc}$ sits between head complexity and ordinary PTF sparsity in the upper-bound hierarchy.

## Proof

Let

$$
P(x)
=
a_{\varnothing}
+
\sum_{S\in\mathcal{M}}a_S\prod_{i\in S}x_i
$$

be a strict sign-representing polynomial for $f$, where every $S\in\mathcal{M}$ is nonempty and every $a_S\neq0$.

For a nonempty set $S$, the monomial

$$
\prod_{i\in S}x_i
$$

is the subcube indicator $C_{S,\varnothing}(x)$. Its local cost is

$$
\kappa(S,\varnothing)
=
\min\{2^{\lvert S\rvert},1\}
=
1.
$$

Therefore the same polynomial is a strict cylinder-threshold representation:

$$
f(x)=1
\qquad\Longleftrightarrow\qquad
a_{\varnothing}
+
\sum_{S\in\mathcal{M}}a_SC_{S,\varnothing}(x)>0.
$$

By the definition of $\operatorname{ctc}$,

$$
\operatorname{ctc}(f)
\leq
\sum_{S\in\mathcal{M}}\kappa(S,\varnothing)
=
\lvert\mathcal{M}\rvert.
$$

Minimizing over all strict sign-representing polynomials proves

$$
\operatorname{ctc}(f)\leq\operatorname{ptfsp}(f).
$$

If $\deg_{\pm}(f)\leq d$, choose a degree-at-most-$d$ sign-representing polynomial. It has at most

$$
\sum_{r=1}^{d}\binom{n}{r}
$$

nonconstant monomials. The displayed degree-$d$ bound follows.

Finally, Lemma 99 gives $H^{*}(f)\leq\operatorname{ctc}(f)$, so

$$
H^{*}(f)
\leq
\operatorname{ctc}(f)
\leq
\operatorname{ptfsp}(f).
$$

$\blacksquare$

## Consequences

The polynomial-threshold sparsity theorem [35_ptf_sparsity_upper_bound.md](35_ptf_sparsity_upper_bound.md) factors through $\operatorname{ctc}$. Any future improvement to $\operatorname{ctc}$ over sparse monomial support automatically sharpens the sparse-PTF route without changing the underlying sign polynomial.

This comparison does not replace the affine-free sparsity theorem [42_affine_free_sparsity_upper_bound.md](42_affine_free_sparsity_upper_bound.md): a dense affine threshold can have small $H^{*}$ while its monomial-cylinder representation has large $\operatorname{ctc}$ cost. The value of the comparison is that it locates $\operatorname{ctc}$ inside the existing hierarchy of general upper-bound invariants.
