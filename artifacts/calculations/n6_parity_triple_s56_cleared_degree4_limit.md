# S56 Cleared Degree-Four Multiplier Limitation

## Ansatz

Let $U$ be the fixed 54-point support and set

$$ S_{56}=U\cup\lbrace16,47\rbrace. $$

For four positive affine denominators $B_h$, put $F=\prod_hB_h$ and define the cleared signed tangent row

$$ G(z)=s(z)\left(F(z),\left(\frac{z_iF(z)}{B_h(z)}\right)_{0\leq h\leq3, 0\leq i\leq5}\right). $$

The cleared ansatz asks for a strictly positive value vector $q$ on $S_{56}$ such that $G^{\top}q=0$ and $q$ is the restriction of a Fourier polynomial of degree at most four.

The degree-at-most-four evaluation space on $S_{56}$ has rank 54. Its two independent relations are

$$ R_1(z)=\left(\prod_{i=0}^5z_i\right)M_1(z), \qquad R_2(z)=\left(\prod_{i=0}^5z_i\right)M_2(z), $$

where

$$ M_1(z)=z_2+z_3, \qquad M_2(z)=2z_0+z_1+z_2-z_4+z_5. $$

Hence the ansatz is equivalent to finding $q>0$ with

$$ G^{\top}q=0, \qquad R_1^{\top}q=R_2^{\top}q=0. $$

## Exact Denominators

Use the sign-coordinate affine denominator rows

$$ \begin{aligned} B_0&=(100;-5,-49,-1,-4,-1,-39), \\ B_1&=(101;-2,-36,-25,-1,-33,-3), \\ B_2&=(100;-7,-6,-2,-7,-7,-30), \\ B_3&=(100;-7,-1,-6,-6,-22,-57). \end{aligned} $$

Their exact ranges on the cube are

$$ [1,199], \qquad [1,201], \qquad [41,159], \qquad [1,199]. $$

Thus all four denominators are strictly positive.

## Exact Augmented Separator

Use the following 27 coefficients, consisting of one global tangent coefficient, six slope coefficients for each head, and two final coefficients multiplying $R_1$ and $R_2$:

$$ \begin{aligned} a={}&(5777;\ 122716,-2239037,-103031,292071,-2957531,-1609447; \\ &-60847,-899092,-1092096,-47421,-588822,-2872907; \\ &-169197,-7262409,202449,-239922,1622945,-285419; \\ &325227,10613939,847057,193611,2206967,6632861; \\ &-10000000000,5191960708). \end{aligned} $$

Let $x$ be the first 25 coefficients, $alpha=-10000000000$, and $\beta=5191960708$. Exact integer evaluation gives

$$ G(z)x+\alpha R_1(z)+\beta R_2(z)>0 \qquad\text{for every }z\in S_{56}. $$

The exact minimum is

$$ \min_{z\in S_{56}}\left(G(z)x+\alpha R_1(z)+\beta R_2(z)\right)=852046508, $$

attained at code 51.

If a positive cleared ansatz vector $q$ existed, multiplying these inequalities by $q(z)$ and summing would give

$$ 0<\sum_{z\in S_{56}}q(z)\left(G(z)x+\alpha R_1(z)+\beta R_2(z)\right)=x^{\top}G^{\top}q+\alpha R_1^{\top}q+\beta R_2^{\top}q=0, $$

a contradiction.

This is an exact strict augmented separator. It refutes the cleared degree-four multiplier ansatz on $S_{56}$. It does not separate the ordinary S56 Gordan cone and does not give a four-head realization of the target.

## Verification

Run:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_s56_cleared_degree4_limit.py
```

The verifier checks denominator positivity, the rank-54 evaluation space and both relations, and every exact augmented score on $S_{56}$.
