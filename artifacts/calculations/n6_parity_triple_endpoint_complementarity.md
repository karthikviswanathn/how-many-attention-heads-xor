# Endpoint-Ray Complementarity Stratum

## Setup

Let $s : \lbrace -1,1\rbrace^6 \to \lbrace -1,1\rbrace$ be the sign function encoded by `0x96696bd669b69669`, and let $U$ be the fixed 54-point support obtained by omitting

$$ \lbrace 6,9,16,21,27,36,42,47,54,57\rbrace. $$

For $z\in\lbrace -1,1\rbrace^6$, define

$$ S(z)=\sum_{i=0}^5z_i, \qquad T(z)=z_0+z_1+z_2+z_3-3z_4+z_5=S(z)-4z_4. $$

Choose real parameters $6<A<C$ and the four strictly positive affine denominators

$$ B_0=A-S, \qquad B_1=C-S, \qquad B_2=A+S, \qquad B_3=C+S. $$

Set $F=\prod_{h=0}^3B_h$ and $P_h=F/B_h$. The cleared tangent row has the 25 coordinates

$$ W(z)=s(z)\left(F(z),\left(z_iP_h(z)\right)_{0\leq h\leq 3, 0\leq i\leq 5}\right). $$

## Weak Endpoint Separator

Let $a=(1,1,1,1,-3,1)$. Choose global coefficient zero and the four six-coordinate tangent blocks

$$ (A^2-4)a, \qquad -(C^2-4)a, \qquad -(A^2-4)a, \qquad (C^2-4)a. $$

Before multiplication by the target sign, the resulting cleared polynomial factors as

$$ P(z)=2(C^2-A^2)T(z)S(z)(S(z)^2-4). $$

This identity follows by grouping the first and third head terms, then the second and fourth head terms:

$$ \begin{aligned} P(z)&=T(z)\left((A^2-4)(P_0-P_2)+(C^2-4)(P_3-P_1)\right) \\ &=2(C^2-A^2)T(z)S(z)(S(z)^2-4). \end{aligned} $$

On $U$, this polynomial vanishes at every Hamming level except the two endpoints. At levels $S=\pm4$, the only vertices where $T$ is nonzero are codes 16 and 47, which are omitted from $U$. Hence

$$ s(z)P(z)>0 \text{ exactly for }z\in\lbrace 0,63\rbrace, \qquad s(z)P(z)=0 \text{ on the other 52 points of }U. $$

Thus this denominator family has a weak separator supported only at the antipodal endpoints.

## Complementary Four-Point Circuit

The four cleared rows at codes 35, 38, 41, and 44 satisfy

$$ W(35)+W(38)+W(41)+W(44)=0. $$

All four codes lie in the 52-point zero set of the weak separator. Therefore the equal weights form a positive Gordan circuit complementary to the endpoint ray.

At the exact instance $A=7$ and $C=8$, integer arithmetic gives

$$ \mathrm{rank}(W|_U)=25, \qquad \mathrm{rank}(W|_{U\setminus\lbrace 0,63\rbrace})=24. $$

The separator is consequently the unique ray orthogonal to the 52 zero rows.

## Consequence

This is an admissible interior stratum, not merely a zero-denominator limit. It shows that a homotopy proof cannot assume a strictly positive dual throughout denominator space. Weak separators can occur in the interior, but here complementarity immediately supplies a four-point obstruction to strict realization.

## Verification

Run:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_endpoint_complementarity.py
```

The verifier uses $A=7$ and $C=8$. It checks denominator positivity on all 64 vertices, the factorization on the full cube, nonnegativity and the exact 52-point zero set on $U$, the ranks 25 and 24, and the equal-weight four-point circuit.
