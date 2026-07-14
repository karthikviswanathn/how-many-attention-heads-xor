# Five-Head Fourier Orthant Refutation

## Status

The middle-weight parity-with-one-flip functions have an exact coefficient rigidity property. After sending the exceptional vertex to the all-positive sign vertex and normalizing the output, every degree-at-most-five sign representative has all $63$ proper Fourier coefficients strictly negative.

This note shows that the coefficient orthant alone is not a five-head obstruction. The full $64$ target-sign inequalities remain essential. Subsequent weighted-cut optimization found exact five-head certificates for both middle orbits, so this family is now fully resolved with equality.

The calculation is checked exactly by [verify_n6_parity_single_flip_orthant_refutation.py](verify_n6_parity_single_flip_orthant_refutation.py).

## Boolean Quotient-Ring Form

Work in sign coordinates $w_i^2=1$. Multiplication of Fourier coefficient vectors is XOR convolution on subsets of $\lbrace1,\ldots,6\rbrace$.

Let the exceptional sign pattern before reorientation be

$$ v=(-1,-1,-1,1,1,1). $$

Use the following five denominator rows, where each row lists the constant coefficient followed by the six slope coefficients:

$$ \begin{aligned} B_1&=(20;1,3,3,-5,-5,-1),\\ B_2&=(27;1,5,2,-6,-6,-4),\\ B_3&=(24;2,4,5,-6,-1,-5),\\ B_4&=(18;2,2,3,-4,-1,-4),\\ B_5&=(25;1,2,3,-1,-5,-6). \end{aligned} $$

For every row, the constant coefficient is strictly larger than the sum of the absolute slope coefficients. Thus $B_i$ is strictly positive on the full sign cube. Moreover, multiplying the slope vector coordinatewise by $v$ makes every slope strictly negative. These are five admissible denominators of one common orientation.

Take affine numerators

$$ \begin{aligned} A_1&=(0;-14480,1768,28332,29468,115306,0),\\ A_2&=(0;-503,-18040,-27708,0,-82845,20470),\\ A_3&=(0;-9127,21989,-15559,-41077,0,-90655),\\ A_4&=(-33433;36671,0,4930,32365,-115827,41477),\\ A_5&=(0;-20102,-5547,2203,-49910,73492,1252). \end{aligned} $$

Define the cleared five-head tangent form

$$ F(w)=\sum_{i=1}^{5}A_i(w)\prod_{j\neq i}B_j(w), $$

with every product reduced by $w_i^2=1$.

## Exact Outcome

The coefficient of $w_1w_2w_3w_4w_5w_6$ is zero, as it must be for a degree-at-most-five form. Every other Fourier coefficient is strictly negative. Their exact range is

$$ -1574974786\leq \widehat F(S)\leq -404109. $$

Therefore this admissible five-head tangent space intersects the full strict rigidity orthant.

However, $F$ does not sign-represent the target. It has the correct target sign on only $31$ of the $64$ vertices. This example refutes only the proposed orthant-only lower-bound route. It is not a five-head certificate for the parity-with-one-flip function.

## Weighted-cut strengthening

The full vertex signs impose a strict cut-cone condition on the coefficient magnitudes. Let $G$ be any degree-at-most-five sign representative after the exceptional vertex has been sent to the all-positive vertex, and put

$$ P(w)=-w_1w_2w_3w_4w_5w_6G(w). $$

Then $P(1)>0$, while $P(w)<0$ at every other sign vertex. Its constant Fourier coefficient is zero. Write

$$ u_w=-P(w)>0 \qquad (w\neq1). $$

The zero constant coefficient gives $P(1)=\sum_{w\neq1}u_w$. Therefore every nonempty Fourier coefficient satisfies

$$ \widehat P(T)=\frac{1}{32}\sum_{w:\chi_T(w)=-1}u_w>0. $$

Thus the $63$ positive coefficient magnitudes are a strictly positive weighted cut metric on the group $\mathbb{F}_2^6$. In particular, for all nonempty $A,B,A\mathbin{\triangle}B$,

$$ \widehat P(A\mathbin{\triangle}B)\leq\widehat P(A)+\widehat P(B). $$

Indeed, the cut indexed by $A\mathbin{\triangle}B$ is the symmetric difference of the cuts indexed by $A$ and $B$, hence is contained in their union.

The tangent form above violates even this simplest triangle inequality. Its shifted positive coefficient magnitudes satisfy

$$ \widehat P(\lbrace1\rbrace)=993952, \qquad \widehat P(\lbrace2\rbrace)=997151, \qquad \widehat P(\lbrace1,2\rbrace)=7348490. $$

Consequently,

$$ 7348490>993952+997151. $$

This gives an exact coefficient-level explanation for why the tangent form lies in the correct orthant but fails the target vertex signs.

## Consequence

The orthant-only obstruction was insufficient. The exact target-value condition supplies the sharper weighted-cut formulation. If

$$ F(w)=-\sum_{S\subsetneq[6]}a_S w_S, \qquad a_S>0, $$

then the shifted polynomial

$$ P(w)=-w_1w_2w_3w_4w_5w_6F(w) $$

has zero constant coefficient and strictly positive coefficients on every nonempty character. Sign representation additionally requires the weighted-cut identities and all of their cut-cone inequalities. The tangent example above fails a two-generator triangle inequality, while the later exact five-head certificates meet a strict normalized slice of the full weighted-cut cone.
