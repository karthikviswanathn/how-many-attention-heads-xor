# Six-Bit Edge-and-Cut Cone Limitation

## Purpose

This note records an exact tangent polynomial that satisfies all 120 middle-level slice inequalities and all 15 nonexceptional quotient-cut inequalities. Therefore even the combined edge-and-cut cone is too weak to prove a universal four-head obstruction for the parity-triple candidate.

The exact verifier is [verify_n6_parity_triple_edge_cut_cone_limit.py](verify_n6_parity_triple_edge_cut_cone_limit.py).

## Construction

Use the four same-oriented affine denominator rows

$$ D=\begin{pmatrix}135562&-131072&-256&-128&-4096&-1&-8\\794898&-524288&-8&-2&-8192&-262144&-8\\2433&-16&-1&-64&-256&-32&-2048\\1328512&-128&-262144&-1048576&-512&-512&-16384\end{pmatrix}. $$

Their strict diagonal-dominance slacks are

$$ (1,256,16,256). $$

Use the affine numerator rows

$$ A=\begin{pmatrix}-11329030&5108461&4538&24829&-46162&-6293421&-4856\\100000000&-70958010&135121&-777072&261965&-4288401&264425\\-234193&1551&254&6225&24745&3060&197204\\30311522&-851731&-6352293&-24270944&-17408&227195&-455650\end{pmatrix}. $$

Let $q$ be the Boolean Fourier coefficient vector of

$$ P=\sum_{h=1}^{4}A_h\prod_{g\neq h}D_g. $$

Exact XOR convolution verifies that $q_S=0$ for $lvert S\rvert>4$.

## Strict edge and cut feasibility

All 120 one-exception slice rows with subset sizes $2$ and $3$ are strictly positive. Their minimum is

$$ 16025004790688768. $$

Let $U=\mathrm{span}_{\mathbb{F}_2}\lbrace51,60\rbrace$ and let $C=21+U$ be the exceptional coset. For every other coset $Q$, define

$$ \beta_Q=\sum_{z\in Q}\chi_{63}(z)P(z). $$

All 15 quotient masses are strictly positive. Their minimum is

$$ 5642691207806809016. $$

Thus this fixed tangent space intersects the strict cone formed by all 120 Hasse-edge rows and the full 15-facet quotient-cut cone.

## Why the polynomial is not a sign representative

The polynomial fails the target sign at $29$ vertices. Its worst signed target value is

$$ -194977864413678764224 $$

at vertex $13$.

It also satisfies only $174$ of the full 186 one-exception slice rows, so the omitted low and high slice levels detect part of the failure. More importantly, positive total mass on each four-point quotient coset does not enforce the correct sign at every point inside that coset.

## Consequence for the proof strategy

Neither middle-level slice monotonicity nor the full quotient-cut cone, separately or together, yields a universal four-head lower bound. Any further reduced cone must be checked against extreme anisotropic denominator tuples before it is treated as a proof candidate.

The remaining exact route must retain pointwise truth-table information, or add stronger within-coset compatibility constraints that recover it.
