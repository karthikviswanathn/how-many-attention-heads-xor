# Six-Bit Parity-Triple Slice Poset

## Scope

Let $f$ be six-bit parity with the three weight-three vertices $21,38,41$ flipped. This note gives exact reductions for the quartic coefficient cone forced by the six one-exception slices. It also records an orientation symmetry and a pair-symmetric boundary obstruction.

These statements do not by themselves prove $H^{\ast}(f)>4$.

## One-exception slices

For coordinates $0,\ldots,5$, choose the slice signs

$$ c=(1,-1,1,-1,-1,1). $$

The corresponding slices contain exactly the exceptions

$$ e=(38,38,41,41,21,21). $$

Let $p(z)=\sum_S p_S z_S$ be any degree-at-most-four sign polynomial for $f$ in sign coordinates. If $i\notin S$ and $S$ is a proper subset of the other five coordinates, the five-bit parity-one-flip argument gives

$$ \chi_S(e_i)(p_S+c_i p_{S\cup\lbrace i\rbrace})>0. $$

There are $31$ inequalities per coordinate and $186$ in total.

## Diagonal sign transform

Put

$$ A=\lbrace0,2,5\rbrace, \qquad d_S=(-1)^{\lvert S\cap A\rvert}, \qquad q_S=d_Sp_S. $$

Since $d_{S\cup\lbrace i\rbrace}=-c_i d_S$, every slice inequality becomes

$$ \chi_S(e_i)d_S(q_S-q_{S\cup\lbrace i\rbrace})>0. $$

Use the coordinate pairs

$$ P_0=\lbrace0,1\rbrace, \qquad P_1=\lbrace2,3\rbrace, \qquad P_2=\lbrace4,5\rbrace. $$

For every $i\notin S$, one has

$$ \chi_S(e_i)d_S=(-1)^{\lvert S\cap P(i)\rvert}, $$

where $P(i)$ is the pair containing $i$. Because $i\notin S$, the exponent is $1$ exactly when the mate of $i$ already belongs to $S$. Consequently, the inequality says the following:

> Replacing an empty or full coordinate-pair state by a singleton state strictly decreases the transformed coefficient $q_S$.

Thus the slice coefficient cone is an open order cone on a product of three four-state pair posets. The rank of a mask is the number of coordinate pairs in a singleton state.

The middle levels initially studied as an obstruction are masks of sizes two, three, and four. Their four rank layers have respectively

$$ 6,12,24,8 $$

nodes. The underlying undirected graph is connected, so its oriented incidence matrix has exact rank $49$ on the $50$ coefficient nodes.

The smaller size-one and size-three subsystem splits into two connected components. The size-one and size-two component has $21$ nodes and incidence rank $20$. The size-three and size-four component has $35$ nodes and incidence rank $34$. Hence the combined $90$-row incidence matrix has rank $54$.

These incidence subsystems are useful structurally, but neither is a universal four-head obstruction. The exact witnesses in [n6_parity_triple_slice_cone_limit.md](n6_parity_triple_slice_cone_limit.md) and [n6_parity_triple_edge_cut_cone_limit.md](n6_parity_triple_edge_cut_cone_limit.md) give admissible tangent polynomials inside the strict order cone.

## Orientation-count symmetry

On every coordinate pair, apply

$$ (x_{2j},x_{2j+1})\longmapsto(1-x_{2j+1},1-x_{2j}). $$

This transformation fixes each of the three exceptional vertices $21,38,41$. It preserves six-bit parity, so it preserves $f$. It changes every positive denominator slope into a negative slope and conversely. Therefore the four-head orientation counts $r$ and $4-r$ are equivalent.

It is enough to analyze orientation counts $0,1,2$.

## Pair-symmetric boundary obstruction

Suppose every denominator has equal slopes in coordinate pairs $P_a$ and $P_b$. Choose the two exceptional vertices that differ exactly in those two pair choices. Together with the other two corners, they form a rectangle whose positive vertices are one diagonal and whose negative vertices are the other diagonal.

For example, for $P_0$ and $P_1$, the positive vertices are $38,41$ and the negative vertices are $37,42$. Their bit vectors satisfy

$$ x(38)+x(41)=x(37)+x(42). $$

Every denominator is constant on this rectangle when its two slopes agree within both varying coordinate pairs. Each ratio therefore restricts to an affine function on the rectangle. A sum of affine functions cannot have the XOR sign pattern because the displayed parallelogram identity makes the two diagonal sums equal.

The analogous exact circuits are

$$ x(21)+x(38)=x(37)+x(22), $$

for pairs $P_0,P_2$, and

$$ x(21)+x(41)=x(25)+x(37), $$

for pairs $P_1,P_2$.

Hence a four-head representation cannot lie on any boundary subfamily where every denominator is pair-symmetric in two of the three coordinate pairs.

## Cofactor degree and denominator collisions

Every one-bit cofactor of $f$ has threshold degree exactly four.

On the chosen slice $z_i=c_i$, there is one exceptional vertex. If $J$ is the set of five remaining coordinates and $e$ is the exception, then

$$ \chi_J(z)-\chi_J(e)\prod_{j\in J}(1+e_jz_j) $$

has degree at most four and flips parity exactly at $e$. Fixing any remaining coordinate opposite to its value at $e$ leaves a four-dimensional face with no exception, so the restriction is pure four-bit parity. This proves the matching degree-four lower bound.

The opposite slice contains two exceptions $e_1,e_2$ at Hamming distance four. The polynomial

$$ 2\chi_J(z)-\chi_J(e_1)\prod_{j\in J}(1+(e_1)_jz_j)-\chi_J(e_2)\prod_{j\in J}(1+(e_2)_jz_j) $$

again has degree at most four and flips parity exactly at the two exceptions. The exceptions agree in exactly one of the five remaining coordinates. Fixing that coordinate to the opposite value leaves a pure four-bit parity face, giving the lower bound.

Now suppose a four-head score represents $f$. Restrict it to any coordinate slice. If two restricted denominators are proportional, their two ratios combine into one ratio, leaving at most three heads. If a restricted denominator is constant, its affine ratio can be absorbed into any other numerator, again leaving at most three heads. Either conclusion contradicts threshold degree four of the cofactor.

Therefore every restricted denominator is nonconstant, and the four restricted denominators are pairwise nonproportional on every one-bit slice. In particular, every collision hypersurface of the form

$$ B_h\big|_{x_i=c}\propto B_k\big|_{x_i=c} $$

is excluded from an exact representation.

This identifies the boundary approached by several continuous searches. For example, one optimized all-positive tuple makes two denominators proportional on the slice $x_2=1$ to numerical precision. Such a limit can have zero margin but cannot be perturbed into an exact strict representation while the collision persists.

## Limitation of the poset reduction

After the diagonal transform, a putative admissible four-head tangent coefficient vector must be strictly decreasing along every edge of the $50$-node product-poset subgraph on degrees two through four. The initially proposed lower-bound route was to construct, for every admissible denominator tuple, a positive flow on these $120$ directed edges whose divergence annihilates the $25$-dimensional tangent numerator space.

The exact edge-cone witnesses cited above prove that such a universal flow does not exist. Even adding all 15 nonexceptional quotient-coset mass inequalities does not restore a universal Gordan multiplier.

Therefore the poset reduction is a necessary-condition diagnostic, not a complete lower-bound route. Any rigorous four-head obstruction for this candidate must retain pointwise truth-table information or add stronger within-coset constraints.
