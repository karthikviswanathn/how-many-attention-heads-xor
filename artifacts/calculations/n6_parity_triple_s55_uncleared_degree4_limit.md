# S55 Uncleared Degree-Four Multiplier Limitation

## Ansatz

Let $U$ be the fixed 54-point support and set

$$ S_{55}=U\cup\lbrace47\rbrace. $$

For four positive affine denominators $B_h$, define the uncleared signed tangent row

$$ W(z)=s(z)\left(1,\left(\frac{z_i}{B_h(z)}\right)_{0\leq h\leq3, 0\leq i\leq5}\right). $$

The proposed ansatz asks for a strictly positive value vector $y$ on $S_{55}$ such that $W^{\top}y=0$ and $y$ is the restriction of a Fourier polynomial of degree at most four.

The degree-at-most-four evaluation space on $S_{55}$ has rank 54. Its sole relation is

$$ R(z)=\left(\prod_{i=0}^5z_i\right)L(z), \qquad L(z)=2z_0+z_1-2z_2-3z_3-z_4+z_5. $$

Hence the ansatz is equivalent to finding $y>0$ with

$$ W^{\top}y=0, \qquad R^{\top}y=0. $$

## Exact Denominators

Use the sign-coordinate affine denominator rows

$$ \begin{aligned} B_0&=(10000;-533,-6866,-155,-454,-239,-955), \\ B_1&=(10000;-213,-4005,-3706,-299,-1322,-290), \\ B_2&=(9999;-783,-1196,-1359,-517,-862,-1107), \\ B_3&=(9999;-1540,-108,-2040,-1623,-889,-3741). \end{aligned} $$

Their exact ranges on the cube are

$$ [798,19202], \qquad [165,19835], \qquad [4175,15823], \qquad [58,19940]. $$

Thus all four denominators are strictly positive.

## Exact Augmented Separator

Use the following 26 coefficients, consisting of one global tangent coefficient, six slope coefficients for each head, and a final coefficient multiplying $R$:

$$ \begin{aligned} a={}&(676232;\ 22438139,-5813574063,-1434011511,-97943353,-53959409,-283505930; \\ &-72894416,-262051774,-171916900,-242913606,-535526130,-1362791895; \\ &112519085,755398088,662838623,329628783,496579781,1138945474; \\ &1385506287,10000000000,2343529441,1501385062,837077587,3658910650;\ 774). \end{aligned} $$

Let $x$ be the first 25 coefficients and $\alpha=774$. Exact integer evaluation, after multiplying each row by the positive product $F(z)=\prod_hB_h(z)$, gives

$$ F(z)\left(W(z)x+\alpha R(z)\right)>0 \qquad\text{for every }z\in S_{55}. $$

The exact minimum is

$$ \min_{z\in S_{55}}F(z)\left(W(z)x+\alpha R(z)\right)=557595572110905986, $$

attained at code 31.

If a positive ansatz vector $y$ existed, multiplying these strict inequalities by $y(z)$ and summing would give

$$ 0<\sum_{z\in S_{55}}y(z)\left(W(z)x+\alpha R(z)\right)=x^{\top}W^{\top}y+\alpha R^{\top}y=0, $$

a contradiction.

## Why the Symmetric Repair Survives This Example

At the added antipode code 16, the same cleared augmented score is

$$ -172843742437269688320<0. $$

Therefore this separator does not extend to the antipodally repaired support $S_{56}=U\cup\lbrace16,47\rbrace$. Numerically, the corrected two-relation $S_{56}$ cone has a positive margin at this tuple.

This counterexample disproves only the uncleared degree-four multiplier ansatz on $S_{55}$. It is not a separator for the ordinary repaired Gordan cone and is not a four-head realization of the target.

## Verification

Run:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_s55_uncleared_degree4_limit.py
```

The verifier checks denominator positivity, the rank-54 evaluation space and its relation, every exact augmented score on $S_{55}$, and the negative score at code 16.
