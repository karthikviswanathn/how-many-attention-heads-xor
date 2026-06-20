# Sparse Support Upper Bound

## Statement

Let

$$
f : \{0,1\}^n \to \{0,1\}
$$

and define the minority support size

$$
s(f)
:=
\min\{
\lvert f^{-1}(1)\rvert,
\lvert f^{-1}(0)\rvert
\}.
$$

Then

$$
H^{*}(f)\leq 2s(f).
$$

In particular, every function with at most $s$ true inputs or at most $s$ false inputs satisfies

$$
H^{*}(f)\leq 2s.
$$

If $s(f)=1$, then the sharper bound

$$
H^{*}(f)\leq1
$$

holds.

> **Interpretation.** Sparse and co-sparse functions are easy even when their true points have no monotone or symmetric structure. The invariant is the size of the smaller label class.

## Proof

If $f$ is constant, then $s(f)=0$ and $H^{*}(f)=0$.

Assume $f$ is nonconstant. Choose the positive injective statistic

$$
t(x):=\sum_{i=1}^{n}2^{i-1}x_i.
$$

This statistic is injective on $\{0,1\}^n$, so $f$ factors through $t$.

List the cube points in increasing order of $t$:

$$
x^{(0)},x^{(1)},\ldots,x^{(2^n-1)}.
$$

Let

$$
a_j:=f(x^{(j)}).
$$

Let $m:=s(f)$, and choose the minority label $\beta\in\{0,1\}$ so that

$$
\lvert\{j:a_j=\beta\}\rvert=m.
$$

The sign-change count of the sequence $a_0,\ldots,a_{2^n-1}$ is at most $2m$: each maximal contiguous block of minority labels contributes at most two boundary changes, one on entry and one on exit. The number of such blocks is at most $m$.

Therefore the positive-projection sign-change theorem [07_positive_projection_sign_changes.md](07_positive_projection_sign_changes.md) gives

$$
H^{*}(f)\leq C_t(f)\leq2m=2s(f).
$$

If $s(f)=1$, then either $f^{-1}(1)=\{a\}$ or $f^{-1}(0)=\{a\}$ for some point $a\in\{0,1\}^n$. The singleton indicator is a linear threshold function:

$$
\mathbf{1}[x=a]=1
\qquad\Longleftrightarrow\qquad
\sum_{i:a_i=1}x_i+\sum_{i:a_i=0}(1-x_i)>n-\frac{1}{2}.
$$

Its complement is also a linear threshold function. By the exact one-head characterization from [05_linear_fractional_normal_form.md](05_linear_fractional_normal_form.md), every nonconstant linear threshold function has $H^{*}=1$. Hence $H^{*}(f)\leq1$ when $s(f)=1$. $\blacksquare$

## Consequence

Let

$$
N_1(f):=\lvert f^{-1}(1)\rvert,
\qquad
N_0(f):=\lvert f^{-1}(0)\rvert.
$$

Then

$$
H^{*}(f)\leq2\min\{N_1(f),N_0(f)\}.
$$

This improves the generic $2^n-1$ bound whenever the smaller label class has size below $2^{n-1}$. It is especially useful for rare-event predicates and complements of rare-event predicates, where no low-dimensional positive projection or monotone normal form is visible.

The first nontrivial sparse case is sharper than the displayed general bound. If $s(f)\leq2$, then [58_two_point_support_exact.md](58_two_point_support_exact.md) gives

$$
H^{*}(f)\leq2,
$$

with exact value determined by the constant, LTF, and non-LTF split.

The same sharpening applies to a larger geometric class. If a label class $A$ is exactly

$$
\operatorname{aff}(A)\cap\{0,1\}^n
$$

and $\operatorname{aff}(A)$ is proper, then [59_affine_hull_clean_supports.md](59_affine_hull_clean_supports.md) gives the same two-head upper bound and exact split.
