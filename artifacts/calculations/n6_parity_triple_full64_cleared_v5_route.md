# Full-Cube Cleared Degree-Five Multiplier Route

## Setup

Let

$$ p(z)=\prod_{i=0}^5z_i $$

be six-bit parity in sign coordinates. The target sign $s$ equals $p$ except at

$$ E=\lbrace21,38,41\rbrace, $$

where $p=-1$ and $s=1$. Thus

$$ s=p+2\mathbf{1}_E. $$

For four strictly positive oriented affine denominators $B_h$, put

$$ F=\prod_{h=0}^3B_h, \qquad P_h=\frac{F}{B_h}. $$

The cleared signed tangent row is

$$ G(z)=s(z)\left(F(z),\left(z_iP_h(z)\right)_{0\leq h\leq3, 0\leq i\leq5}\right)\in\mathbb{R}^{25}. $$

The degree-at-most-five value space on the full six-cube is exactly

$$ V_5=\left\lbrace q\in\mathbb{R}^{64}:\sum_zp(z)q(z)=0\right\rbrace. $$

The proposed full-cube multiplier statement is

$$ q(z)>0, \qquad G^{\top}q=0, \qquad p^{\top}q=0. $$

If this statement holds for every admissible four-denominator dictionary, then the target has no four-head representation.

## Exact Gordan Alternative

Write

$$ R(z)=aF(z)+\sum_{h=0}^3\ell_h(z)P_h(z), $$

where each $\ell_h$ is homogeneous linear. Gordan's strict alternative says that a positive $q$ exists exactly when there is no nonzero coefficient tuple $(a,\ell_0,\ldots,\ell_3,\beta)$ satisfying

$$ A(z):=s(z)R(z)+\beta p(z)\geq0 \qquad\text{for every }z. $$

This is the exact augmented alternative for the row matrix $[G,p]$.

There is a useful moment identity. For every affine $H$,

$$ \sum_zH(z)A(z)=2\sum_{e\in E}H(e)R(e). $$

Indeed, $HR$ has degree at most five, so it is orthogonal to parity, and the same is true of $H$.

The nonnegative affine forms

$$ H_{21}=1-z_4, \qquad H_{38}=1+z_0, \qquad H_{41}=1+z_2 $$

take value $2$ at the indexed exception and vanish at the other two. Therefore every nonnegative augmented separator must satisfy

$$ R(21)\geq0, \qquad R(38)\geq0, \qquad R(41)\geq0. $$

The pointwise inequalities at the exceptions also give

$$ \beta\leq\min_{e\in E}R(e). $$

These are exact necessary conditions for a counterexample to the multiplier statement.

## Antipodal Pair Form

Choose one representative $z$ from each pair $\lbrace z,-z\rbrace$. Since the dimension is even, $p(-z)=p(z)$. For a prospective multiplier define

$$ e_z=q(z)+q(-z), \qquad o_z=q(z)-q(-z). $$

Strict positivity is equivalent to

$$ e_z>0, \qquad \lvert o_z\rvert<e_z. $$

The parity relation becomes

$$ \sum_{lbrace z,-z\rbrace}p(z)e_z=0, $$

and the cleared tangent relation becomes

$$ \sum_{lbrace z,-z\rbrace}\left(\frac{e_z}{2}\left(G(z)+G(-z)\right)+\frac{o_z}{2}\left(G(z)-G(-z)\right)\right)=0. $$

The dual alternative also has a compact pair form. Put

$$ E_R(z)=\frac{R(z)+R(-z)}{2}, \qquad O_R(z)=\frac{R(z)-R(-z)}{2}. $$

On a regular pair, where $s(z)=s(-z)=p(z)=\varepsilon$, the two inequalities $A\geq0$ are equivalent to

$$ \varepsilon\left(E_R(z)+\beta\right)\geq\lvert O_R(z)\rvert. $$

Orient each exceptional pair so that $e\in E$ is the first point. Since $s(e)=1$, $s(-e)=-1$, and $p(e)=p(-e)=-1$, its two inequalities are equivalent to

$$ O_R(e)-\beta\geq\lvert E_R(e)\rvert. $$

## Why the Uncleared Degree-Five Route Fails

For the uncleared row

$$ W(z)=s(z)\left(1,\left(\frac{z_i}{B_h(z)}\right)_{h,i}\right), $$

a positive degree-five multiplier $y$ would satisfy both $s^{\top}y=0$ and $p^{\top}y=0$. Their difference is

$$ 0=(s-p)^{\top}y=2\sum_{e\in E}y(e), $$

which contradicts $y>0$. Thus the uncleared full-cube degree-five cone is structurally impossible, independently of the denominators.

## Stacked Common Kernel

Across all literal-corner dictionaries, the inner cleared tangent polynomials span all of $V_4$. Put

$$ d(z)=s(z)p(z), $$

so $d=-1$ on $E$ and $d=1$ elsewhere. The common kernel of every corner tangent matrix together with the parity relation is exactly

$$ q(z)=d(z)L(z), $$

where $L$ is affine and

$$ \sum_{e\in E}L(e)=0. $$

This space has dimension six. One basis is obtained from the six forms

$$ L_i(z)=3z_i-u_i, \qquad u=(-1,1,-1,1,1,-1). $$

There is no nonzero nonnegative vector in this common kernel. If $q=dL\geq0$, then $L\geq0$ off $E$ and $L(e)\leq0$ on $E$. The displayed sum condition forces $L(e)=0$ for all three exceptions. The three exceptions vary in every coordinate, so the only affine form nonnegative on the cube and vanishing at all three is zero.

Consequently, a proof cannot use one multiplier common to all literal corners. It must use local face-dependent multipliers or a direct exclusion of the augmented alternative.

## Literal-Corner Audit

An admissible oriented denominator is an interior convex combination of $1$ and the six literals $1+\sigma z_i$. Head permutation and simultaneous orientation reversal reduce the corner audit to orientation counts $0,1,2$. There are

$$ 3\cdot7^4=7203 $$

corner dictionaries.

The numerical LP audit found a nonzero nonnegative multiplier at every corner. It found strict multipliers at 6966 corners and boundary-only multipliers at 237 corners:

| Orientation count | Boundary only | Strict |
|---:|---:|---:|
| 0 | 25 | 2376 |
| 1 | 115 | 2286 |
| 2 | 97 | 2304 |

The boundary-only corners have four combinatorial types:

1. all four denominators are constant;

2. exactly one denominator is nonconstant;

3. exactly two opposite-orientation denominators use the same coordinate;

4. all four denominators use distinct coordinates, in 72 cases at orientation count 1 and 48 cases at orientation count 2.

The first type has augmented rank 8. The second and third types have rank 13. The distinct-coordinate type has rank 14. In the first three types, a nonnegative separator can be supported exactly on $E$. In the last type, a nonnegative separator can be supported on a four-point affine rectangle on which the target is positive.

The smallest positive normalized corner margin was $0.01$, so the strict corner classifications are numerically well separated from zero. The script [audit_n6_parity_triple_full64_cleared_v5_corners.py](audit_n6_parity_triple_full64_cleared_v5_corners.py) reproduces the complete audit.

## Simplex-Edge Common Kernels

With the other three denominators fixed, $G$ is affine in the remaining denominator. A multiplier common to the two endpoints of a literal-simplex edge therefore annihilates every denominator on that edge.

An exhaustive numerical audit of the 36015 inequivalent edge classes found a nonzero nonnegative common multiplier on every edge. It found strict common multipliers on 31044 edges and boundary-only common multipliers on 4971 edges. The five head-orientation classes gave:

| Orientation count and changed head | Boundary only | Strict |
|---|---:|---:|
| 0 | 813 | 6390 |
| 1, positive head | 1011 | 6192 |
| 1, negative head | 1053 | 6150 |
| 2, positive head | 1047 | 6156 |
| 2, negative head | 1047 | 6156 |

The script [audit_n6_parity_triple_full64_cleared_v5_edges.py](audit_n6_parity_triple_full64_cleared_v5_edges.py) reproduces this audit.

These edge results support a simplex-face induction, but they do not complete one. Higher-dimensional faces need common multipliers, and the boundary-only edge classes need exact facial reduction.

## Hard-Tuple and Adversarial Screen

The cleared full-cube cone survived five denominator tuples that defeat earlier fixed-support or degree-four ansatzes. Their normalized margins were:

| Tuple | Margin |
|---|---:|
| support54 escape | $3.21179507231\times10^{-7}$ |
| positive quartic limit | $0.0106399524517$ |
| S55 uncleared degree-four limit | $0.00902454470097$ |
| S56 uncleared degree-four limit | $0.00899734704693$ |
| S56 cleared degree-four limit | $0.00791502096735$ |

Twelve adversarial restarts from the last tuple found no negative margin. The smallest value was $5.77519450779\times10^{-8}$, reached only by pushing literal weights to the imposed $10^{-9}$ floor. This is evidence for boundary-limited positivity, not a proof.

The script [screen_n6_parity_triple_full64_v5_hard_tuples.py](screen_n6_parity_triple_full64_v5_hard_tuples.py) reproduces the five hard-tuple margins. The adversarial restart was an exploratory optimization and is not an exact certificate.

## Failed Cubic Structured Subcone

The tempting restriction

$$ q=dr, \qquad \deg(r)\leq3 $$

cannot work. Positivity of $q$ forces $r(e)<0$ for every $e\in E$. The parity relation would require

$$ 0=p^{\top}q=\sum_zs(z)r(z)=2\sum_{e\in E}r(e)<0, $$

where the middle equality uses orthogonality of parity to every cubic. Thus this 42-variable subcone is structurally empty.

## Weak Multipliers And Generic Closure

For the four-head lower bound, a weak Gordan multiplier is enough:

$$ q\geq0,\qquad q\neq0,\qquad G^{\top}q=0,\qquad p^{\top}q=0. $$

Strict positivity of all 64 coordinates is a stronger convenience, not a requirement. Normalize a weak multiplier by $\mathbf1^{\top}q=1$. For a denominator parameter $\theta$, define

$$ K(\theta)=\lbrace q\in\Delta_{63}:[G(\theta),p]^{\top}q=0\rbrace. $$

The set of parameters for which $K(\theta)$ is nonempty is closed. Indeed, if $\theta_j\to\theta$ and $q_j\in K(\theta_j)$, compactness of $\Delta_{63}$ gives a convergent subsequence $q_{j_k}\to q$. Continuity gives $q\in K(\theta)$.

The script [verify_n6_parity_triple_full64_augmented_generic_rank.py](verify_n6_parity_triple_full64_augmented_generic_rank.py) constructs one strictly interior integer denominator tuple in each orientation-count branch and proves rank $26$ modulo $1000003$. Since the augmented matrix has 26 columns, this proves rational rank $26$. The rank-$26$ locus is therefore Zariski open and dense in every branch.

Consequently, it is enough to prove $K(\theta)\neq\varnothing$ on the rank-$26$ locus. Closedness then supplies every rank-deficient and boundary tuple automatically. Carathéodory reduces each pointwise multiplier on this locus to at most 27 cube vertices.

For an ordered 27-vertex support $S=\lbrace x_0,\ldots,x_{26}\rbrace$, define

$$ q_j^S(\theta)=(-1)^j\det [G(\theta),p]_{S\setminus\lbrace x_j\rbrace}. $$

The cofactor identity gives $[G(\theta),p]^{\top}q^S(\theta)=0$ identically. Wherever these 27 cofactors have one weak sign and are not all zero, the support supplies a weak Gordan multiplier. Each cofactor has denominator-block multidegree $(19,19,19,19)$ and total degree $76$.

Thus the best finite reduction is an exact atlas of positive oriented-matroid circuits covering the rank-$26$ parameter locus. This route permits the multiplier to vary with the denominators and avoids separate facial reduction once dense-locus coverage is proved.

## Status

The full-cube cleared degree-five cone is the strongest surviving multiplier route for the six-bit parity-triple candidate. The exact alternative, pair reduction, common-kernel description, moment constraints, generic rank, and closure reduction are rigorous. The corner, edge, hard-tuple, and adversarial results are numerical audits.

A proof still needs one of the following:

- an exact positive-circuit atlas covering the rank-$26$ denominator locus;

- an argument that the exact augmented alternative $A=sR+\beta p\geq0$ contradicts denominator orientation;

- an exact positive multiplier formula depending on the four denominator coefficient vectors.

A fixed multiplier on a full-dimensional parameter cell cannot work. Polynomial identity would extend it to every denominator tuple, contradicting the exact common-kernel obstruction. Any full-dimensional atlas must therefore use varying circuit or polynomial multiplier formulas.
