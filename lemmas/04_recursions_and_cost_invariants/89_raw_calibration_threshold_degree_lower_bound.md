# Raw Calibration Threshold-Degree Lower Bound

## Statement

Let

$$
T_1,\ldots,T_s:\{0,1\}^n\to\{0,1\}
$$

be Boolean features, and suppose

$$
f(x)=1
\qquad\Longleftrightarrow\qquad
c_0+\sum_{j=1}^{s}c_jT_j(x)>0
$$

with positive margin on the Boolean cube. Then

$$
\deg_{\pm}(f)
\leq
\sum_{j:c_j\neq0}\rho(T_j).
$$

In particular, if

$$
f(x)=T_1(x)\wedge T_2(x),
$$

then

$$
\rho(T_1)+\rho(T_2)
\geq
\deg_{\pm}(f),
$$

and hence

$$
\max\{\rho(T_1),\rho(T_2)\}
\geq
\frac{\deg_{\pm}(f)}{2}.
$$

> **Interpretation.** High threshold degree of a strict vote proves that its inner features cannot all have small raw calibration cost. This turns threshold-degree lower bounds into lower bounds on $\rho$ for at least one feature in the vote.

## Proof

The raw-calibrated vote support bound [87_raw_calibrated_vote_support_bound.md](87_raw_calibrated_vote_support_bound.md) gives

$$
H^{*}(f)
\leq
\sum_{j:c_j\neq0}\rho(T_j).
$$

The threshold-degree lower bound [xor_n_bits.md](../01_foundations_and_normal_form/xor_n_bits.md) gives

$$
\deg_{\pm}(f)\leq H^{*}(f).
$$

Combining the two inequalities proves

$$
\deg_{\pm}(f)
\leq
\sum_{j:c_j\neq0}\rho(T_j).
$$

For conjunction, use the strict vote

$$
T_1(x)\wedge T_2(x)=1
\qquad\Longleftrightarrow\qquad
T_1(x)+T_2(x)-\frac{3}{2}>0.
$$

This vote has margin $1/2$. Applying the first part gives

$$
\deg_{\pm}(T_1\wedge T_2)
\leq
\rho(T_1)+\rho(T_2).
$$

The maximum bound follows from

$$
\rho(T_1)+\rho(T_2)
\leq
2\max\{\rho(T_1),\rho(T_2)\}.
$$

$\blacksquare$

## Consequences

Sherstov's linear threshold-degree lower bounds for intersections of two halfspaces imply that some halfspaces have large raw calibration cost $\rho$. Otherwise the conjunction of two arbitrary halfspaces would have small $H^{*}$ by Lemma 93, contradicting the threshold-degree lower bound.

This is why the surviving decision-list target after Lemma 94 is not a bound depending only on length. The target is to classify low-$\rho$ test families and to prove $\rho$ lower bounds for hard internal tests.
