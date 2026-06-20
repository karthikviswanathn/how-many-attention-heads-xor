# Fresh-XOR Affine-Statistic Sign-Change Bound

## Statement

Let

$$
L(y)=a+\sum_{i=1}^{m}\alpha_i y_i
$$

be an affine statistic on $\{0,1\}^{m}$, and let

$$
k:=\lvert\{i:\alpha_i\neq0\}\rvert.
$$

Let $G:\operatorname{Im}(L)\to\{0,1\}$, and define

$$
T(y):=G(L(y)).
$$

Write the distinct image values as

$$
\lambda_1<\lambda_2<\cdots<\lambda_M,
$$

and let $C$ be the number of sign changes in the sequence

$$
G(\lambda_1),G(\lambda_2),\ldots,G(\lambda_M).
$$

Define

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
H^{*}(z\oplus T(y))
\leq
1+\sum_{r=2}^{\min\{D_{\oplus}(C),k+1\}}\binom{k+1}{r},
$$

and the same upper bound holds for XNOR.

> **Interpretation.** Fresh XOR over one affine statistic doubles the sign-change pattern and adds one boundary change exactly when the original pattern starts and ends with the same label.

## Proof

Choose $B>0$ so large that

$$
B>\lambda_M-\lambda_1,
$$

and define the affine statistic on $(z,y)$

$$
M_B(z,y):=L(y)+Bz.
$$

The image values of $M_B$ are ordered as

$$
\lambda_1<\cdots<\lambda_M<B+\lambda_1<\cdots<B+\lambda_M.
$$

Define $H:\operatorname{Im}(M_B)\to\{0,1\}$ by

$$
H(\lambda_i):=G(\lambda_i),
\qquad
H(B+\lambda_i):=1-G(\lambda_i).
$$

Then

$$
z\oplus T(y)=H(M_B(z,y)).
$$

The first block

$$
H(\lambda_1),\ldots,H(\lambda_M)
$$

has $C$ sign changes. The second block

$$
H(B+\lambda_1),\ldots,H(B+\lambda_M)
$$

is the complement of the same sequence, so it also has $C$ sign changes.

There is one additional boundary change between the two blocks exactly when

$$
G(\lambda_M)\neq1-G(\lambda_1),
$$

or equivalently when

$$
G(\lambda_M)=G(\lambda_1).
$$

Since each sign change flips the current label, this last equality holds exactly when $C$ is even. Hence the sign-change count of $H$ along $\operatorname{Im}(M_B)$ is $D_{\oplus}(C)$.

The statistic $M_B$ uses at most $k+1$ variables. Applying the affine-statistic sign-change theorem [57_affine_statistic_sign_changes.md](../03_function_families_and_affine_geometry/57_affine_statistic_sign_changes.md) gives the following.

If $C=0$, then $D_{\oplus}(C)=1$, so $z\oplus T$ is a nonconstant LTF and

$$
H^{*}(z\oplus T)=1.
$$

If $C=1$, then $D_{\oplus}(C)=2$, so the same theorem gives

$$
H^{*}(z\oplus T)\leq2.
$$

In this case $T$ is a nonconstant LTF, so the LTF one-bit gate classification [123_ltf_one_bit_gate_classification.md](123_ltf_one_bit_gate_classification.md) gives the matching lower bound and exact value

$$
H^{*}(z\oplus T)=2.
$$

If $C\geq2$, then $D_{\oplus}(C)\geq3$, and the same affine-statistic theorem gives

$$
H^{*}(z\oplus T)
\leq
1+\sum_{r=2}^{\min\{D_{\oplus}(C),k+1\}}\binom{k+1}{r}.
$$

Finally, XNOR is the output complement of fresh XOR, and output complement preserves head complexity by [22_restrictions_and_sign_rank.md](../02_complexity_measure_upper_bounds/22_restrictions_and_sign_rank.md). This proves all claims. $\blacksquare$

## Consequences

If $T$ is a non-LTF affine slab, then $C=2$, so

$$
D_{\oplus}(C)=5
$$

and therefore

$$
H^{*}(z\oplus T)
\leq
1+\sum_{r=2}^{\min\{5,k+1\}}\binom{k+1}{r}.
$$

This is the current orientation-free fallback for fresh XOR over affine slabs beyond the LTF case. The endpoint and one-threshold cases are sharper: they are exactly two-head by Lemmas 127 and 129.
