# Low Affine-Free Support Is Exact

## Statement

Let

$$
f:\{0,1\}^n\to\{0,1\}.
$$

Suppose

$$
\operatorname{afs}_{\pm}(f)\leq2,
$$

where $\operatorname{afs}_{\pm}$ is the affine-free polynomial-threshold support cost from [42_affine_free_sparsity_upper_bound.md](42_affine_free_sparsity_upper_bound.md). Then

$$
H^{*}(f)\leq2.
$$

More precisely,

$$
H^{*}(f)
=
\begin{cases}
0 & \text{if } f \text{ is constant},\\
1 & \text{if } f \text{ is a nonconstant linear threshold function},\\
2 & \text{otherwise}.
\end{cases}
$$

In particular, this applies whenever $f$ is sign-represented by a polynomial of the form

$$
P(x)=A(x)+b\prod_{i\in S}x_i,
\qquad
\lvert S\rvert\geq2,
$$

where $A$ is affine. It also applies to sign polynomials with no affine part and at most two nonlinear monomials.

> **Interpretation.** The affine-free support bound has an exact first nontrivial regime. Any Boolean function whose sign polynomial consists of one affine part plus one genuinely nonlinear monomial is either an LTF already or has exact value two.

## Proof

The affine-free sparsity theorem [42_affine_free_sparsity_upper_bound.md](42_affine_free_sparsity_upper_bound.md) gives

$$
H^{*}(f)\leq\operatorname{afs}_{\pm}(f).
$$

Hence the hypothesis implies

$$
H^{*}(f)\leq2.
$$

If $f$ is constant, then $H^{*}(f)=0$. If $f$ is a nonconstant LTF, the one-head characterization from [05_linear_fractional_normal_form.md](../01_foundations_and_normal_form/05_linear_fractional_normal_form.md) gives

$$
H^{*}(f)=1.
$$

If $f$ is neither constant nor a nonconstant LTF, the same characterization gives

$$
H^{*}(f)\geq2.
$$

Together with the two-head upper bound, this proves

$$
H^{*}(f)=2.
$$

Finally, a sign polynomial of the displayed form has affine-free support cost at most two: the whole affine part costs one head, and the single nonlinear monomial costs one more. If the affine part is absent, two nonlinear monomials also have affine-free support cost at most two. $\blacksquare$

## Consequence

This gives a practical exactness test:

1. Find a sign polynomial with at most two affine-free pieces.
2. Check whether the function is constant or an LTF.
3. If not, conclude $H^{*}(f)=2$.

The criterion is complementary to the low positive-projection alternation criterion. It can certify two heads even when no good one-dimensional positive ordering is known.
