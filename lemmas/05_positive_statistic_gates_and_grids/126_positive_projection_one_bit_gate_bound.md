# Positive-Projection One-Bit Gate Bound

## Statement

Let

$$
t(y)=\sum_{i=1}^{m}\lambda_i y_i,
\qquad
\lambda_i>0,
$$

and let $F:\operatorname{Im}(t)\to\{0,1\}$. Define

$$
T(y):=F(t(y)).
$$

Write the image of $t$ as

$$
0=\tau_0<\tau_1<\cdots<\tau_{M-1}.
$$

Let $G:\{0,1\}^{2}\to\{0,1\}$ be any two-input Boolean gate, and define

$$
H_G(z,y):=G(z,T(y)).
$$

Form the concatenated gate sequence

$$
\mathcal{S}_{G,t}
:=
G(0,F(\tau_0)),\ldots,G(0,F(\tau_{M-1})),
G(1,F(\tau_0)),\ldots,G(1,F(\tau_{M-1})).
$$

Let $C_{G,t}$ be the number of sign changes in this sequence. Then

$$
H^{*}(H_G)\leq C_{G,t}.
$$

More precisely:

1. If $C_{G,t}=0$, then $H^{*}(H_G)=0$.

2. If $C_{G,t}=1$, then $H^{*}(H_G)=1$.

3. If $C_{G,t}=2$, then

$$
H^{*}(H_G)=
\begin{cases}
1 & \text{if } H_G \text{ is a nonconstant LTF},\\
2 & \text{otherwise}.
\end{cases}
$$

> **Interpretation.** A raw bit appended to a positive-projection feature remains a positive projection after separating the two slices. The cost is the sign-change count of the two gate slices written end to end.

## Proof

Choose

$$
B>\tau_{M-1}.
$$

Define the positive weighted sum

$$
s(z,y):=Bz+t(y).
$$

Its image is ordered as

$$
\tau_0<\tau_1<\cdots<\tau_{M-1}<B+\tau_0<B+\tau_1<\cdots<B+\tau_{M-1}.
$$

Define $R:\operatorname{Im}(s)\to\{0,1\}$ by

$$
R(\tau_j):=G(0,F(\tau_j)),
\qquad
R(B+\tau_j):=G(1,F(\tau_j)).
$$

Then

$$
H_G(z,y)=R(s(z,y)).
$$

The sign-change count of $R$ along the ordered image of $s$ is exactly $C_{G,t}$, by construction. The positive-projection sign-change theorem [07_positive_projection_sign_changes.md](../01_foundations_and_normal_form/07_positive_projection_sign_changes.md) gives

$$
H^{*}(H_G)\leq C_{G,t}.
$$

If $C_{G,t}=0$, then $R$ is constant on $\operatorname{Im}(s)$, so $H_G$ is constant and $H^{*}(H_G)=0$.

If $C_{G,t}=1$, then the same theorem gives $H^{*}(H_G)\leq1$, and $H_G$ is nonconstant. The zero-head and one-head characterization [05_linear_fractional_normal_form.md](../01_foundations_and_normal_form/05_linear_fractional_normal_form.md) gives

$$
H^{*}(H_G)=1.
$$

If $C_{G,t}=2$, then $H^{*}(H_G)\leq2$. If $H_G$ is a nonconstant LTF, the one-head characterization gives $H^{*}(H_G)=1$. Otherwise $H_G$ is nonconstant and not an LTF, so the same characterization gives $H^{*}(H_G)\geq2$. Hence $H^{*}(H_G)=2$ in the non-LTF case. $\blacksquare$

## Consequences

Let $C$ be the sign-change count of $F$ along $\operatorname{Im}(t)$. For literal gates such as $z\wedge T$, $z\vee T$, and their complements, the concatenated sequence has at most $C+1$ sign changes. Therefore

$$
H^{*}(z\wedge T)\leq C+1,
\qquad
H^{*}(z\vee T)\leq C+1,
$$

and the same bound holds for their complements.

For XOR and XNOR, this lemma recovers the doubled sign-change count in [125_positive_projection_fresh_xor_sign_change_bound.md](125_positive_projection_fresh_xor_sign_change_bound.md).
