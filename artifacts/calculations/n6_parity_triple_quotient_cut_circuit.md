# Six-Bit Quotient-Cut Circuit

## Purpose

This note augments the 120 middle-level slice rows with 15 global quotient-cut rows. At the fixed denominator tuple in [n6_parity_triple_slice_cone_limit.md](n6_parity_triple_slice_cone_limit.md), the augmented system has an exact positive Gordan circuit.

This is a fixed-denominator diagnostic. It is not a parameter-uniform four-head obstruction.

The exact verifier is [verify_n6_parity_triple_quotient_cut_circuit.py](verify_n6_parity_triple_quotient_cut_circuit.py).

## Quotient-cut rows

Let

$$ U=\mathrm{span}_{\mathbb{F}_2}\lbrace51,60\rbrace, \qquad C=21+U=\lbrace21,26,38,41\rbrace. $$

For every coset $Q$ of $U$ other than $C$, define the parity-twisted coset mass

$$ \beta_Q=\sum_{z\in Q}\chi_{63}(z)P(z). $$

Every genuine sign representative of the parity-triple target satisfies $\beta_Q>0$, because none of these 15 cosets contains an exceptional vertex.

In Fourier coefficient coordinates, each $\beta_Q$ is a linear row supported on

$$ H=U^{\perp}=\lbrace0,3,12,15,48,51,60,21,22,25,26,37,38,41,42,63\rbrace. $$

The six masks $3,12,15,48,51,60$ are exactly the sources of the paired Hasse DAG. The eight masks $21,22,25,26,37,38,41,42$ are exactly its sinks. The remaining endpoint coordinates are $0$ and $63$, and every tangent quartic has coefficient $q_{63}=0$.

Thus the quotient-cut cone couples the constant coefficient and all Hasse endpoints. This is precisely the global information missing from the six separate one-exception slice cones.

## Exact circuit

Order the 120 slice rows first by coordinate, then by subset size $2,3$, then lexicographically. Order the 15 cut rows by the least vertex in their coset. The exact circuit has 26 rows: 24 slice rows and two cut rows.

The supported slice triples $(i,S,\lvert S\rvert)$ are

$$ \begin{aligned}(0,50,3);\quad &(1,20,2),(1,36,2),(1,24,2),(1,49,3),(1,44,3);\\ &(2,41,3),(2,50,3),(2,56,3);\\ &(3,5,2),(3,34,2),(3,20,2),(3,7,3),(3,19,3),(3,35,3),(3,22,3),(3,52,3);\\ &(4,9,2),(4,6,2),(4,34,2),(4,35,3),(4,13,3),(4,14,3);\quad (5,19,3).\end{aligned} $$

The supported cut cosets are

$$ Q_0=\lbrace0,15,51,60\rbrace, \qquad Q_7=\lbrace7,8,52,59\rbrace. $$

The verifier stores the primitive 26-entry positive integer vector `GORDAN_WEIGHTS` in this support order. Its largest entry has 83 decimal digits. Exact integer convolution verifies that its weighted sum annihilates all 28 affine-numerator tangent columns.

Consequently, no polynomial in this fixed tangent space can satisfy all 120 middle-level slice inequalities and all 15 quotient-cut inequalities strictly.

## Limitation

The support is not stable as the denominator tuple varies. Numerical stress tests find that sparse 26-row circuits change immediately across generic admissible samples. A universal proof therefore needs an adaptive positive-flow construction, a finite support atlas with proved coverage, or a direct structural theorem for the combined edge and cut cone.
