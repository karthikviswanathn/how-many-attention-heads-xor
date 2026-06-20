# Affine-Cylinder Cost Hierarchy

## Statement

Let $\operatorname{afs}_{\pm}(f)$ be the affine-free polynomial-threshold sparsity from [42_affine_free_sparsity_upper_bound.md](42_affine_free_sparsity_upper_bound.md), and let $\operatorname{ptfsp}(f)$ be ordinary polynomial-threshold sparsity. Then

$$
\operatorname{actc}(f)
\leq
\operatorname{afs}_{\pm}(f)
\leq
\operatorname{ptfsp}(f).
$$

Combining with Lemma 103 gives

$$
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\min\{\operatorname{ctc}(f),\operatorname{afs}_{\pm}(f)\}.
$$

Consequently, if $f$ is nonconstant and $\deg_{\pm}(f)\leq d$, then

$$
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
1+\sum_{r=2}^{d}\binom{n}{r}.
$$

> **Interpretation.** The affine-cylinder invariant is a common refinement of two upper-bound routes: signed local cylinder votes and affine-free sparse sign polynomials.

## Proof

Let

$$
P(x)
=
a_{\varnothing}
+
\sum_{\varnothing\neq S\subseteq\{1,\ldots,n\}}a_S\prod_{i\in S}x_i
$$

be a strict sign-representing polynomial for $f$. Split it as

$$
P(x)
=
A(x)
+
\sum_{S\in\mathcal{M}}a_S\prod_{i\in S}x_i,
$$

where

$$
A(x)
:=
a_{\varnothing}
+
\sum_{i=1}^{n}a_{\{i\}}x_i
$$

is the affine part and

$$
\mathcal{M}
:=
\{S:\lvert S\rvert\geq2,\ a_S\neq0\}.
$$

For each $S\in\mathcal{M}$,

$$
\prod_{i\in S}x_i
=
C_{S,\varnothing}(x)
$$

and

$$
\kappa(S,\varnothing)=1.
$$

Therefore the same strict sign polynomial is an affine-cylinder threshold representation:

$$
f(x)=1
\qquad\Longleftrightarrow\qquad
A(x)+\sum_{S\in\mathcal{M}}a_SC_{S,\varnothing}(x)>0.
$$

Its affine-cylinder cost is

$$
\lambda(A)+\lvert\mathcal{M}\rvert
=
\operatorname{afs}(P).
$$

Thus

$$
\operatorname{actc}(f)\leq\operatorname{afs}(P).
$$

Minimizing over all strict sign-representing polynomials proves

$$
\operatorname{actc}(f)\leq\operatorname{afs}_{\pm}(f).
$$

For every polynomial $P$, the affine-free support cost is at most the number of nonconstant monomials in $P$: all nonzero linear monomials together cost at most one, and all nonlinear monomials are counted exactly. Taking a polynomial that achieves $\operatorname{ptfsp}(f)$ gives

$$
\operatorname{afs}_{\pm}(f)\leq\operatorname{ptfsp}(f).
$$

Lemma 103 gives

$$
H^{*}(f)\leq\operatorname{actc}(f)
\qquad
\text{and}
\qquad
\operatorname{actc}(f)\leq\operatorname{ctc}(f).
$$

Combining these inequalities yields

$$
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\min\{\operatorname{ctc}(f),\operatorname{afs}_{\pm}(f)\}.
$$

Finally, if $f$ is nonconstant and $\deg_{\pm}(f)\leq d$, choose a degree-at-most-$d$ sign polynomial. Its affine-free support cost is at most

$$
1+\sum_{r=2}^{d}\binom{n}{r},
$$

because all linear terms together cost one affine block and there are at most $\binom{n}{r}$ monomials of each degree $r\geq2$. The degree corollary follows. $\blacksquare$

## Consequences

The ordinary sparse-PTF theorem and the affine-free sparse-PTF theorem both factor through $\operatorname{actc}$:

$$
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\operatorname{afs}_{\pm}(f)
\leq
\operatorname{ptfsp}(f).
$$

Together with Lemma 103,

$$
\operatorname{actc}(f)
\leq
\min\{\operatorname{ctc}(f),\operatorname{afs}_{\pm}(f)\}.
$$

Thus the next sharper upper-bound search can ask for a strict threshold of locally cheap cylinders after first extracting one dense affine component.
