# Five-Bit Support-Eight Circuit Classification

## Statement

Every support-eight circuit of the five-bit quadratic Fourier configuration comes from a quadratic of the form

$$ Q(z)=cB_1(z)B_2(z), $$

where $c\neq0$ and each affine factor is one of

$$ 1\mathbin{\pm}z_i \qquad\text{or}\qquad z_i\mathbin{\pm}z_j. $$

Up to coordinate permutations, individual coordinate sign flips, and global circuit sign, there are exactly four types:

1. two coordinate factors, represented by $(1-z_1)(1-z_2)$;

2. a coordinate factor and a disjoint comparison, represented by $(1-z_1)(z_2-z_3)$;

3. two incident comparisons, represented by $(z_1-z_2)(z_1-z_3)$;

4. two disjoint comparisons, represented by $(z_1-z_2)(z_3-z_4)$.

The smaller input symmetry group that visibly preserves head complexity, coordinate permutations and simultaneous complementation of all inputs, splits these into exactly nine orbits.

For every type, the circuit support is a three-dimensional affine flat over $\mathbb{F}_2$. After choosing three free affine coordinates on that flat, the forced circuit signs are the three-bit parity signs, up to a global sign.

## Equality case of the support bound

We first record the equality case behind the classification.

**Lemma.** Let $P$ be a nonzero multilinear polynomial of degree at most $d$ on the sign cube. If

$$ \lvert\mathrm{supp}(P)\rvert=2^{n-d}, $$

then, for $d=2$, $P$ is a nonzero scalar multiple of a product of two factors of the displayed forms.

**Proof.** Induct on $n$. Write

$$ P(z',z_n)=A(z')+z_nB(z'). $$

If $B=0$, the support doubles between the two $z_n$ slices, so equality reduces to the same statement in dimension $n-1$.

Suppose $B\neq0$. The ordinary support-bound proof gives

$$ \lvert\mathrm{supp}(P)\rvert\geq\lvert\mathrm{supp}(B)\rvert\geq2^{n-2}. $$

Equality forces $B$ to have minimum support among affine functions, and it forces exactly one of $A+B$ and $A-B$ to be nonzero at every point where $B$ is nonzero. A nonzero affine function on a sign cube has support exactly half the cube only in the forms

$$ c(1\mathbin{\pm}z_i) \qquad\text{or}\qquad c(z_i\mathbin{\pm}z_j). $$

Moreover, $A$ vanishes wherever $B$ vanishes. Directly separating the two slices of the coordinate or comparison defining $B=0$ shows that $A=BL$ for an affine function $L$, modulo values off the support of $B$. The equality condition gives $L\in\lbrace-1,1\rbrace$ throughout that half cube. An affine function taking only the values $-1$ and $1$ on a cube is either constant or a signed coordinate. Consequently, on the support of $B$ one may take

$$ L=\mathbin{\pm}1 \qquad\text{or}\qquad L=\mathbin{\pm}z_i. $$

Therefore

$$ P=B(L+z_n) $$

is a product of two factors of the required forms. The base case is the indicator of one vertex on the two-cube, which is a scalar multiple of $(1\mathbin{\pm}z_1)(1\mathbin{\pm}z_2)$. $\blacksquare$

## Four incidence types

Represent $1\mathbin{\pm}z_i$ by a loop at coordinate $i$, and represent $z_i\mathbin{\pm}z_j$ by an edge between $i$ and $j$. Each factor is nonzero on one half of the cube. A support-eight product is the intersection of two independent half-cube constraints.

Two loops reduce to type 1. A loop and an incident edge also fix two coordinates and reduce to type 1; a disjoint edge gives type 2. Two edges either share one endpoint, giving type 3, or are disjoint, giving type 4. Parallel equal constraints have support sixteen, while parallel opposite constraints have empty support. This proves that the list is exhaustive.

For $\lambda=\chi Q$, Gale self-duality gives the associated circuit. On its three-dimensional support, all quadratic characters span the seven characters of degree at most two in three free affine coordinates. Their one-dimensional orthogonal complement is the degree-three character. Hence $\lambda$ restricts to three-bit parity, up to sign.

## Consequence for the Remaining Degree-Three Class

Every minimum circuit therefore anchors a three-bit parity pattern on one of four affine-flat geometries. The labels on the other $24$ vertices remain free. Exact threshold degree three is obtained by deleting precisely those extensions whose forced parity twist admits a nonzero weak affine separator.

The four full-cube types are useful for structural recursion, but individual coordinate complementation does not visibly preserve admissible denominator orientation. Any head-complexity proof must therefore restore the nine orbits under the smaller valid symmetry group.

The [exact verifier](verify_n5_degree3_support8_circuits.py) enumerates the $30$ minimum-support affine factors and all $420$ qualifying factor pairs. It verifies every circuit dependency and reports four full-cube orbits and nine valid-symmetry orbits.
