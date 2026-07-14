# Positive Quartic Support-54 Ansatz Limitation

## Setup

Let $s : \lbrace -1,1\rbrace^6 \to \lbrace -1,1\rbrace$ be the sign function encoded by `0x96696bd669b69669`. Its fixed 54-point support is

$$ U = \lbrace z \in \lbrace -1,1\rbrace^6 : L(z) \neq 0\rbrace, \qquad L(z)=2z_0+z_1-2z_2-3z_3-z_4+z_5. $$

Consider the four positive affine denominators

$$ \begin{aligned} B_0(z)&=323384-45582z_0-3z_1-74z_2-8850z_3-268810z_4-55z_5, \\ B_1(z)&=10469-245z_0-58z_1-145z_2-2843z_3-7092z_4-76z_5, \\ B_2(z)&=135697804-17211z_0-19850000z_1-45z_2-262047z_3-75713338z_4-39855153z_5, \\ B_3(z)&=3423-1788z_0-1498z_1-z_2-z_3-z_4-124z_5. \end{aligned} $$

Each constant term is ten more than the sum of the absolute values of its six slopes. Hence every $B_h$ is strictly positive on the cube.

Set $D(z)=\prod_{h=0}^3 B_h(z)$. The 25-dimensional cleared tangent row is

$$ G(z)=s(z)\left(D(z),\left(z_i\frac{D(z)}{B_h(z)}\right)_{0\leq h\leq 3, 0\leq i\leq 5}\right). $$

The positive quartic ansatz seeks a Fourier polynomial $q$ of degree at most four such that $q(z)>0$ on $U$ and

$$ \sum_{z\in U}q(z)G(z)=0. $$

It would then give the positive tangent multiplier $\lambda(z)=D(z)q(z)$.

## Unique Quartic Evaluation Relation

The restrictions to $U$ of the 57 Fourier monomials of degree at most four have rank 53. A nonzero relation on their value space is

$$ R(z)=\left(\prod_{i=0}^5z_i\right)L(z). $$

Indeed, $L$ vanishes on the ten omitted vertices, while $R$ is a pure degree-five Fourier polynomial on the full cube. Therefore every degree-at-most-four polynomial $q$ satisfies

$$ \sum_{z\in U}R(z)q(z)=0. $$

The exact verifier checks both the rank and this identity on all 57 monomials.

## Exact Separation of the Quartic Ansatz

There are $y\in\mathbb{Q}^{25}$ and $\beta\in\mathbb{Q}$ such that

$$ G(z)\cdot y+\beta\geq R(z) \quad\text{for every }z\in U, \qquad \beta=-1.9886660626801822\ldots<0. $$

The verifier reconstructs $y$ and $\beta$ exactly from 26 active equalities, then checks all 54 inequalities using rational arithmetic.

Suppose a nonzero nonnegative $q$ satisfied the tangent equations, and normalize it by $\sum_{z\in U}q(z)=1$. Multiplying the separating inequalities by $q(z)$ and summing gives

$$ \sum_{z\in U}R(z)q(z)\leq\sum_{z\in U}q(z)G(z)\cdot y+\beta=\beta<0. $$

This contradicts the quartic evaluation relation. Thus no nonzero nonnegative quartic $q$ lies in the tangent kernel for this denominator tuple.

## Unrestricted Cone Still Survives

This is a limitation of the quartic ansatz, not a support-54 lower bound. On a different 26-point subset of $U$, the verifier reconstructs strictly positive integers $w_z$ satisfying

$$ \sum_z w_zG(z)=0. $$

The largest primitive weight has 325 decimal digits. Consequently the unrestricted positive tangent cone remains nonempty at the same tuple.

## Verification

Run:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_quartic_positive_limit.py
```

The script uses only Python integer and `Fraction` arithmetic. It verifies denominator positivity, the rank-53 quartic evaluation space, the unique relation, the rational separator with negative $\beta$, and the positive unrestricted 26-point circuit.
