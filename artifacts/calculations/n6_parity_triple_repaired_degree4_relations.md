# Repaired-Support Degree-Four Relations

## Evaluation Ranks

Let $U$ be the 54-point support obtained by deleting the ten zeros of

$$ L(z)=2z_0+z_1-2z_2-3z_3-z_4+z_5. $$

Define

$$ S_{55}=U\cup\lbrace47\rbrace, \qquad S_{56}=U\cup\lbrace16,47\rbrace. $$

The restrictions of the 57 Fourier monomials of degree at most four have ranks

$$ \mathrm{rank}(V_4|_{S_{55}})=54, \qquad \mathrm{rank}(V_4|_{S_{56}})=54. $$

Thus $S_{55}$ has one value relation, while $S_{56}$ has two.

For $S_{55}$, the relation is

$$ R(z)=\left(\prod_{i=0}^5z_i\right)L(z). $$

For $S_{56}$, set

$$ M_1(z)=z_2+z_3, \qquad M_2(z)=2z_0+z_1+z_2-z_4+z_5. $$

Then $L=M_2-3M_1$, and a basis of the two-dimensional relation space is

$$ R_k(z)=\left(\prod_{i=0}^5z_i\right)M_k(z), \qquad k\in\lbrace1,2\rbrace. $$

Both relations are odd under the antipodal map.

## Antipodal Pair Variables

The support $S_{56}$ consists of 28 antipodal pairs. Choose one representative $z$ from each pair and define

$$ e_z=y(z)+y(-z), \qquad o_z=y(z)-y(-z), \qquad \epsilon_z=\frac{s(-z)}{s(z)}\in\lbrace-1,1\rbrace. $$

Strict positivity of both endpoint weights is equivalent to

$$ e_z>\lvert o_z\rvert. $$

Only two pairs have opposite target labels:

$$ \lbrace22,41\rbrace, \qquad \lbrace25,38\rbrace. $$

For every other pair, $\epsilon_z=1$.

Let $F(z)=\prod_hB_h(z)$ and $P_h(z)=F(z)/B_h(z)$. Write $F_+=F(z)$, $F_-=F(-z)$, $P_{h,+}=P_h(z)$, and $P_{h,-}=P_h(-z)$. The contribution of one pair to the global cleared tangent column is

$$ \frac{s(z)}{2}\left(e_z(F_++\epsilon_zF_-)+o_z(F_+-\epsilon_zF_-)\right). $$

Its contribution to the coordinate $i$ column of head $h$ is

$$ \frac{s(z)z_i}{2}\left(e_z(P_{h,+}-\epsilon_zP_{h,-})+o_z(P_{h,+}+\epsilon_zP_{h,-})\right). $$

The two degree-four relations depend only on the odd pair variables:

$$ \sum_zR_1(z)o_z=0, \qquad \sum_zR_2(z)o_z=0. $$

Therefore the symmetric repaired-support problem becomes a 28-pair cone problem with 25 tangent equations, two scalar odd relations, and the inequalities $e_z>\lvert o_z\rvert$.

## Verification

Run:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_repaired_degree4_relations.py
```

The verifier checks both ranks, all relation identities on the 57 degree-at-most-four monomials, antipodal oddness, and the two opposite-label pairs.
