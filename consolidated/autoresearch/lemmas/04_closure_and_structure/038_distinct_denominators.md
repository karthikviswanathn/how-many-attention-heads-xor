# Equal Denominators Collapse a Tangent Form to a Linear Threshold Function

## Statement

Let $P = \theta \prod_{h=1}^H D_h + \sum_{h=1}^H N_h \prod_{g\neq h} D_g$ be an order-$H$ tangent form ($H \geq 1$) with each $N_h$ affine and each $D_h$ an affine denominator positive on the cube, and suppose all denominators are equal: $D_1 = \cdots = D_H = D$. If $P$ sign-represents $f$, then $f$ is a linear threshold function.

Equivalently: any $f$ with $H^{*}(f) \geq 2$ (non-LTF) cannot be realized by heads sharing a single denominator; **at least two distinct denominators are required.** Since a head's denominator is its attention weight pattern (atom dictionary [013_atom_dictionary.md](../01_foundations_and_normal_form/013_atom_dictionary.md)), expressivity beyond linear threshold demands **distinct attention patterns across heads** — adding heads with the same pattern buys nothing.

## Proof

With $D_h = D$ for all $h$, $\prod_{h=1}^H D_h = D^H$ and $\prod_{g\neq h} D_g = D^{H-1}$, so

$$
P = \theta D^H + \sum_{h=1}^H N_h D^{H-1} = D^{H-1}\Big(\theta D + \sum_{h=1}^H N_h\Big) = D^{H-1} A,
$$

where $A := \theta D + \sum_{h=1}^H N_h$ is affine (a sum of affine functions). Since $D > 0$ on the cube, $D^{H-1} > 0$ on the cube (with $D^0 = 1$ when $H=1$), so $\mathrm{sgn}\,P(x) = \mathrm{sgn}\,A(x)$ for every $x$. As $P$ sign-represents $f$, $f(x) = 1 \iff P(x) > 0 \iff A(x) > 0$ with $A$ affine, so $f$ is a linear threshold function (constant if $A$ does not change sign). $\blacksquare$

## Consequence

The collapse uses only positivity of the shared denominator, not the one-sided-slope part of admissibility, so it applies to the head model and to any positivity-respecting variant. It isolates *where* the head model's power comes from: not from the number of heads alone, but from the **diversity of their denominators (attention patterns)**. One head, or many heads with a common attention pattern, computes only a linear threshold function ($H^{*} \leq 1$, cf. [011_one_head_characterization.md](../01_foundations_and_normal_form/011_one_head_characterization.md)); every harder function forces genuinely different attention patterns. This is the structural reason the model's complexity is a *tangential* (rather than secant) Chow rank: the leading product $\prod_h D_h$ must be a genuine product of distinct factors to escape the linear-threshold regime. (The positivity hypothesis is essential: with an arbitrary common factor $D$ that may vanish or change sign, $\mathrm{sgn}\,D^{H-1}$ need not be constant and the collapse can fail.)
