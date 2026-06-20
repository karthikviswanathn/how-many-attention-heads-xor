# Positive-Projection Fresh-XOR Sign-Change Bound

## Statement

Let

$$
t(y)=\sum_{i=1}^{m}\lambda_i y_i,
\qquad
\lambda_i>0,
$$

and let $G:\operatorname{Im}(t)\to\{0,1\}$. Define

$$
T(y):=G(t(y)).
$$

Write the image of $t$ as

$$
0=\tau_0<\tau_1<\cdots<\tau_{M-1},
$$

and let $C$ be the number of sign changes in

$$
G(\tau_0),G(\tau_1),\ldots,G(\tau_{M-1}).
$$

Set

$$
D_{\oplus}(C):=
\begin{cases}
2C+1 & \text{if } C \text{ is even},\\
2C & \text{if } C \text{ is odd}.
\end{cases}
$$

Then:

1. If $C=0$, then

$$
H^{*}(z\oplus T(y))=H^{*}(1-(z\oplus T(y)))=1.
$$

2. If $C=1$, then

$$
H^{*}(z\oplus T(y))=H^{*}(1-(z\oplus T(y)))=2.
$$

3. If $C\geq2$, then

$$
H^{*}(z\oplus T(y))\leq D_{\oplus}(C),
$$

and the same upper bound holds for XNOR. Moreover, if

$$
\deg_{\pm}(T)+1=D_{\oplus}(C),
$$

then fresh XOR and XNOR over $T$ have exact head complexity $D_{\oplus}(C)$.

> **Interpretation.** For positive one-dimensional projections, the fresh-XOR construction pays directly for the doubled sign-change sequence, not for an affine-free monomial expansion.

## Proof

Choose

$$
B>\tau_{M-1}.
$$

Define a positive weighted sum on the variables $(z,y)$ by

$$
s(z,y):=Bz+t(y).
$$

Since $B>\tau_{M-1}$, the image of $s$ is ordered in two separated blocks:

$$
\tau_0<\tau_1<\cdots<\tau_{M-1}<B+\tau_0<B+\tau_1<\cdots<B+\tau_{M-1}.
$$

Define $H:\operatorname{Im}(s)\to\{0,1\}$ by

$$
H(\tau_j):=G(\tau_j),
\qquad
H(B+\tau_j):=1-G(\tau_j).
$$

Then

$$
z\oplus T(y)=H(s(z,y)).
$$

The first block has $C$ sign changes, and the second block is the complement of the first, so it also has $C$ sign changes. The boundary between the two blocks changes label exactly when

$$
G(\tau_{M-1})\neq1-G(\tau_0),
$$

which is equivalent to

$$
G(\tau_{M-1})=G(\tau_0).
$$

After $C$ sign changes, the final label equals the initial label exactly when $C$ is even. Therefore the sign-change count of $H$ along the ordered image of $s$ is $D_{\oplus}(C)$.

If $C\geq2$, the positive-projection sign-change theorem [07_positive_projection_sign_changes.md](../01_foundations_and_normal_form/07_positive_projection_sign_changes.md) gives

$$
H^{*}(z\oplus T(y))\leq D_{\oplus}(C).
$$

If $C=0$, then $T$ is constant, and $z\oplus T$ is either $z$ or $1-z$. Hence

$$
H^{*}(z\oplus T)=1.
$$

If $C=1$, then $T$ is a nonconstant LTF. The LTF one-bit gate classification [123_ltf_one_bit_gate_classification.md](123_ltf_one_bit_gate_classification.md) gives

$$
H^{*}(z\oplus T)=2.
$$

Finally, XNOR is the output complement of fresh XOR, and output complement preserves head complexity by [22_restrictions_and_sign_rank.md](../02_complexity_measure_upper_bounds/22_restrictions_and_sign_rank.md). This gives the same values and upper bounds for XNOR.

For the exactness clause, the fresh-bit XOR threshold-degree theorem [75_fresh_bit_xor_threshold_degree.md](../04_recursions_and_cost_invariants/75_fresh_bit_xor_threshold_degree.md) gives

$$
H^{*}(z\oplus T)\geq\deg_{\pm}(T)+1.
$$

If $\deg_{\pm}(T)+1=D_{\oplus}(C)$, this lower bound matches the positive-projection upper bound. The same complement argument handles XNOR. $\blacksquare$

## Consequences

If $T$ is a positive-projection predicate with $C=2$, such as a non-LTF interval along a positive weighted sum, then

$$
H^{*}(z\oplus T)\leq5.
$$

This improves the orientation-free affine-statistic fallback from Lemma 130 whenever $k$ is large. The remaining gap for positive slabs is between the threshold-degree lower bound $3$ and this five-head sign-change construction.
