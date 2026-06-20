# Affine-Cylinder Threshold-Degree Sandwich

## Statement

For every Boolean function $f$,

$$
\deg_{\pm}(f)
\leq
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\min\{\operatorname{ctc}(f),\operatorname{afs}_{\pm}(f)\}.
$$

Consequently,

$$
\deg_{\pm}(f)
\leq
\operatorname{actc}(f)
\leq
\operatorname{ctc}(f),
$$

and

$$
\deg_{\pm}(f)
\leq
\operatorname{afs}_{\pm}(f)
\leq
\operatorname{ptfsp}(f).
$$

> **Interpretation.** The affine-cylinder invariant is now bracketed from both sides. It is an optimized upper-bound target, but it cannot be smaller than threshold degree.

## Proof

The threshold-degree lower bound [006_threshold_degree_head_complexity_bound.md](../01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md) gives

$$
\deg_{\pm}(f)\leq H^{*}(f).
$$

The affine-cylinder threshold-cost lemma [103_affine_cylinder_threshold_cost.md](103_affine_cylinder_threshold_cost.md) gives

$$
H^{*}(f)\leq\operatorname{actc}(f)
$$

and

$$
\operatorname{actc}(f)\leq\operatorname{ctc}(f).
$$

The affine-cylinder hierarchy lemma [104_affine_cylinder_cost_hierarchy.md](104_affine_cylinder_cost_hierarchy.md) gives

$$
\operatorname{actc}(f)\leq\operatorname{afs}_{\pm}(f)
\leq
\operatorname{ptfsp}(f).
$$

Combining these inequalities proves

$$
\deg_{\pm}(f)
\leq
H^{*}(f)
\leq
\operatorname{actc}(f)
\leq
\min\{\operatorname{ctc}(f),\operatorname{afs}_{\pm}(f)\}.
$$

The two displayed consequences follow by deleting intermediate terms from the same chain. $\blacksquare$

## Consequences

For parity,

$$
\operatorname{actc}(\mathrm{XOR}_n)\geq n,
$$

because $\deg_{\pm}(\mathrm{XOR}_n)=n$.

For the halfspace-intersection family $F_n=T_n\wedge U_n$ from [105_halfspace_intersection_head_lower_bound.md](105_halfspace_intersection_head_lower_bound.md),

$$
\operatorname{actc}(F_n)\geq c n.
$$

Thus $\operatorname{actc}$ correctly assigns large cost to the families that refute uncalibrated threshold-vote and LTF decision-list upper bounds.
