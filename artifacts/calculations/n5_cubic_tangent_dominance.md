# Five-Bit Cubic Tangent Dominance

## Statement

Work in the Boolean quotient $x_i^2=x_i$ on five variables. For affine forms $A_1,A_2,A_3,B_1,B_2,B_3$, define

$$ \Phi(B,A):=A_1B_2B_3+A_2B_1B_3+A_3B_1B_2. $$

There is an explicit point at which all three $B_h$ are strictly admissible positive-orientation attention denominators and the parameter Jacobian of $\Phi$ has rank $26$. This is the dimension of the whole space of five-bit polynomials of degree at most three.

At the same point, the numerator parameters alone have rank $16$, and their projection to the ten squarefree cubic coefficients has rank $10$.

Consequently:

1. The squarefree cubic leading part is not an obstruction near this point.

2. A Euclidean open set of five-bit cubics has an exact admissible three-denominator tangent factorization.

3. The algebraic map $\Phi$ is dominant. Equivalently, the Zariski closure of these tangent spaces is the full $26$-dimensional cubic space.

The dominance statement does not by itself prove that every real cubic has an exact admissible factorization. It also does not distinguish exact membership from a boundary or coalescent limit. Those are the remaining global issues.

## Explicit chart

Use coefficient order $(1,x_1,x_2,x_3,x_4,x_5)$. Take

$$ \begin{aligned} B_1&=(7,1,2,3,5,8), & A_1&=(1,-2,3,-1,2,-3), \\ B_2&=(11,2,3,5,7,11), & A_2&=(-2,1,-1,4,-2,1), \\ B_3&=(13,3,4,7,9,14), & A_3&=(3,2,-4,1,1,-2). \end{aligned} $$

Every coefficient of every $B_h$ is positive. In particular, each $B_h$ is strictly positive on the Boolean cube and is in the interior of the positive-orientation denominator chart.

Order the $26$ squarefree monomials by their bit mask, retaining precisely the masks of Hamming weight at most three. In this order, the coefficient vector of $\Phi(B,A)$ is

$$ (192,-8,175,41,848,87,441,39,804,97,285,32,1215,77,211,-1455,-457,-466,-38,469,-25,116,-541,-84,-82,341). $$

The verifier forms the exact integer Jacobian by changing one scalar parameter by $1$. This finite difference is the exact derivative because $\Phi$ is affine in each scalar parameter separately.

## Exact rank certificate

Row reduction modulo the prime $1000003$ gives

$$ \mathrm{rank}(D_A\Phi)=16, \qquad \mathrm{rank}(D_A\Phi\vert_{\deg 3})=10, \qquad \mathrm{rank}(D_{B,A}\Phi)=26. $$

A nonzero minor modulo a prime is a nonzero integer minor, so these are exact characteristic-zero rank certificates.

The ten pivot numerator columns for the cubic leading part are

$$ (1,2,3,4,5,7,8,9,10,13). $$

The $26$ pivot columns for the full Jacobian are

$$ (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26). $$

Thus the ordinary real submersion theorem gives exact admissible factorizations throughout a neighborhood of the displayed cubic. Algebraically, the same nonzero Jacobian minor proves dominance.

## Verification

Run:

```bash
python artifacts/calculations/verify_n5_cubic_tangent_dominance.py
```

The script performs all polynomial arithmetic in the Boolean quotient using integer coefficients and verifies every stated rank modulo $1000003$.
