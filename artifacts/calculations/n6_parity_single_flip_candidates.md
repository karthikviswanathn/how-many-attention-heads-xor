# Six-Bit Parity With One Flipped Vertex

## Status

This note records the exact resolution of the six-bit parity-with-one-flip family. It does not give a strict separation.

Let $v\in\lbrace0,1\rbrace^6$, and let $f_v$ agree with even parity except at $v$. Every $f_v$ has threshold degree exactly five, and every coordinate-permutation orbit has an exact five-head certificate. Thus $H^{\ast}(f_v)=\deg_{\pm}(f_v)=5$ for every $v$.

The exact calculations are checked by [verify_n6_parity_single_flip_candidates.py](verify_n6_parity_single_flip_candidates.py).

## Exact Threshold Degree

Use sign coordinates $z_i=(-1)^{x_i}$, and write

$$ \chi(z)=z_1z_2z_3z_4z_5z_6. $$

Let the sign vector of the exceptional vertex also be denoted by $v\in\lbrace-1,1\rbrace^6$. Define

$$ P_v(z)=\chi(z)-\chi(v)\prod_{i=1}^{6}(1+v_i z_i). $$

At every vertex $z\neq v$, one factor in the product vanishes, so $P_v(z)=\chi(z)$. At $z=v$, the product equals $64$, so

$$ P_v(v)=-63\chi(v). $$

The degree-six terms in the two products cancel. Thus $P_v$ has degree at most five and strictly sign-represents $f_v$.

For the matching lower bound, let $s_v$ be the target sign function and define positive integer weights

$$ \lambda_v(x)=\begin{cases}1&x=v,\\2d_{\mathrm{H}}(x,v)-1&x\neq v.\end{cases} $$

For every Fourier character $\chi_S$ with $\lvert S\rvert\leq4$, direct expansion gives

$$ \sum_{x\in\lbrace0,1\rbrace^6}\lambda_v(x)s_v(x)\chi_S(x)=0. $$

Equivalently, in sign coordinates the signed dual measure is

$$ \lambda_v(z)s_v(z)=\chi(z)\left(5-\sum_{i=1}^{6}v_i z_i\right). $$

Its Fourier support has degrees five and six only. The weights are strictly positive because the affine factor equals $-1$ at $v$ and equals $2d_{\mathrm{H}}(z,v)-1$ elsewhere, while the target sign is flipped only at $v$.

This is a positive Gordan obstruction to every polynomial of degree at most four. Therefore

$$ \deg_{\pm}(f_v)=5. $$

## Fourier-Orthant Rigidity

Every degree-at-most-five sign representative of $f_v$ lies in one strict Fourier coefficient orthant. This is much stronger than the existence of the canonical polynomial above.

Let $P$ be any degree-at-most-five polynomial that strictly sign-represents $f_v$, and put

$$ r(z)=\chi(z)P(z). $$

Then $r(z)>0$ for $z\neq v$, while $r(v)<0$. Since $P$ has no degree-six Fourier term,

$$ \sum_z r(z)=\sum_z\chi(z)P(z)=0. $$

Consequently,

$$ r(v)=-\sum_{z\neq v}r(z). $$

Fix a proper subset $S\subsetneq[6]$, and put $T=[6]\setminus S$. The set $T$ is nonempty. The unnormalized Fourier coefficient of $P$ at $S$ is

$$ \begin{aligned} \sum_z\chi_S(z)P(z) &= \sum_z\chi_T(z)r(z) \\ &= \sum_{z\neq v}\bigl(\chi_T(z)-\chi_T(v)\bigr)r(z). \end{aligned} $$

Every nonzero summand has sign $-\chi_T(v)$, and at least one such summand occurs. Hence

$$ \mathrm{sgn}\bigl(\widehat P(S)\bigr)=-\chi_{[6]\setminus S}(v) \qquad (S\subsetneq[6]). $$

Now reorient the variables by $y_i=v_i z_i$. If $\widetilde P(y)=P(z)$, then

$$ \widehat{\widetilde P}(S)=\chi_S(v)\widehat P(S). $$

It follows that all $63$ proper Fourier coefficients of $\widetilde P$ have the same strict sign:

$$ \mathrm{sgn}\bigl(\widehat{\widetilde P}(S)\bigr)=-\chi(v) \qquad (S\subsetneq[6]). $$

This rigidity gives an algebraic formulation of the five-head search. A valid tangent product must meet not only this open coefficient orthant, but also the weighted-cut cone imposed by the full target signs. The exact certificates below show that both middle orbits do meet the required strict cone.

## Exact Five-Head Certificates

The verifier contains integer five-head certificates for representatives of all four coordinate-permutation orbits up to global input complementation:

- $v=000000$, with minimum signed cleared score $11464$;

- $v=000001$, with minimum signed cleared score $13400$.

- $v=000011$, with minimum signed cleared score $108571693319292$.

- $v=000111$, with minimum signed cleared score $5063509014022934970$.

Every denominator in those certificates is strictly positive on the cube and has all slopes positive or all slopes negative. Hence

$$ H^{\ast}(f_v)=\deg_{\pm}(f_v)=5 $$

for every $v\in\lbrace0,1\rbrace^6$, using coordinate permutations and global input complementation.

The verifier checks denominator positivity, common slope orientation within every head, and every one of the $64$ strict target-sign inequalities using integer arithmetic.

## Search Resolution

Initial all-orientation logistic searches and thousands of fixed-denominator linear programs did not find middle-orbit representations. The decisive search used the exact weighted-cut description of all degree-five sign representatives. For each fixed denominator tuple, a linear program projected its tangent space onto a normalized strict slice of the weighted-cut cone. Differentiating the matching primal and dual programs gave an exact numerical subgradient with respect to denominator logits.

That target-aware optimization found integer-verifiable five-head certificates for both middle orbits. Consequently, the earlier search failures and tuple-specific dual obstructions were local phenomena, not evidence of a global head lower bound.
