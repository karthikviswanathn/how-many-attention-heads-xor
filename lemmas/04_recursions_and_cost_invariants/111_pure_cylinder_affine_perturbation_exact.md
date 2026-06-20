# Pure-Cylinder Affine Perturbations Are Exact

## Statement

Let

$$
f:\{0,1\}^{n}\to\{0,1\}.
$$

Suppose there are disjoint sets $P,N\subseteq\{1,\ldots,n\}$ with either $P=\varnothing$ or $N=\varnothing$, an affine form

$$
A(x)=a_0+\sum_{i=1}^{n}a_i x_i,
$$

and a real coefficient $c$ such that

$$
f(x)=1
\qquad\Longleftrightarrow\qquad
A(x)+cC_{P,N}(x)>0
$$

strictly on the cube. Then

$$
\operatorname{actc}(f)\leq2.
$$

Consequently,

$$
H^{*}(f)
=
\begin{cases}
0, & \text{if } f \text{ is constant},\\
1, & \text{if } f \text{ is a nonconstant LTF},\\
2, & \text{otherwise}.
\end{cases}
$$

> **Interpretation.** A single pure positive or pure negative cylinder can be added to an arbitrary affine score at two-head cost. This includes negative-literal conjunctions without expanding them into many positive monomials.

## Proof

If $P=N=\varnothing$, then $C_{P,N}$ is constant, so the displayed score is affine. Hence $f$ is constant or a nonconstant LTF, and the conclusion follows from the zero-head and one-head characterization [05_linear_fractional_normal_form.md](05_linear_fractional_normal_form.md).

Assume now that $(P,N)$ is nonvacuous. Since either $P=\varnothing$ or $N=\varnothing$,

$$
\kappa(P,N)=1.
$$

The displayed strict score is an affine-cylinder representation with one affine part and one nonvacuous cylinder. Its cost is at most

$$
\lambda(A)+\kappa(P,N)\leq2.
$$

Therefore

$$
\operatorname{actc}(f)\leq2.
$$

The exact case distinction now follows from the low affine-cylinder exactness theorem [103_low_affine_cylinder_cost_exactness.md](103_low_affine_cylinder_cost_exactness.md). $\blacksquare$

## Consequences

Every function that is neither constant nor a nonconstant LTF and has the form

$$
x\mapsto
\mathbf{1}\!\left[
A(x)+c\prod_{i\in P}x_i>0
\right]
$$

is exactly two-head.

The same is true for every function that is neither constant nor a nonconstant LTF and has the form

$$
x\mapsto
\mathbf{1}\!\left[
A(x)+c\prod_{j\in N}(1-x_j)>0
\right].
$$

The second family can have a large positive-monomial expansion, but the affine-cylinder certificate pays only the local cylinder cost $1$.
