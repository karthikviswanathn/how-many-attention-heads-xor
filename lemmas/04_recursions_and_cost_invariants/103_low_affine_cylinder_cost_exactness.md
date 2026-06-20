# Low Affine-Cylinder Cost Is Exact

## Statement

If

$$
\operatorname{actc}(f)\leq2,
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

In particular, every nonconstant non-LTF with $\operatorname{actc}(f)\leq2$ is exactly two-head.

> **Interpretation.** Once the affine-cylinder certificate reaches two heads, the only remaining question is the universal zero-head and one-head split.

## Proof

Lemma 103 gives

$$
H^{*}(f)\leq\operatorname{actc}(f).
$$

Thus the hypothesis implies

$$
H^{*}(f)\leq2.
$$

The exact zero-head and one-head characterization from [05_linear_fractional_normal_form.md](05_linear_fractional_normal_form.md) says:

- $H^{*}(f)=0$ exactly for constant functions,
- $H^{*}(f)=1$ exactly for nonconstant LTFs,
- every nonconstant non-LTF has $H^{*}(f)\geq2$.

Combining this lower split with the upper bound $H^{*}(f)\leq2$ proves the displayed case distinction. $\blacksquare$

## Consequences

This upgrades any low-cost affine-cylinder representation into an exact head count. In particular, every nonconstant non-LTF that can be written as a strict threshold of one affine score plus locally cheap cylinders of total cost at most one is exactly two-head.

Since

$$
\operatorname{actc}(f)
\leq
\min\{\operatorname{ctc}(f),\operatorname{afs}_{\pm}(f)\},
$$

the same exactness conclusion applies whenever either $\operatorname{ctc}(f)\leq2$ or $\operatorname{afs}_{\pm}(f)\leq2$.
