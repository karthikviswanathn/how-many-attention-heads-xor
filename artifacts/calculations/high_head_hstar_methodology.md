# High-Head Certified Methodology

## Scope

This note isolates the regime near or above $H=n/2$. Several attractive generic relaxations have a real midpoint ceiling:

- partition sign-rank cannot rule out $H$ heads unless $n\geq2H+2$;

- the plain and positivity-aware slice relaxations collapse to threshold degree when $H\geq\lceil(n+1)/2\rceil$;

- the first catalecticant constraint $\mathrm{rank}(\mathrm{Cat}&#95;1(P))\leq2H$ is vacuous once $2H\geq n+1$;

- [Theorem 192](../../lemmas/02_complexity_measure_upper_bounds/192_multiway_sign_tensor_rank.md) proves that adding more coordinate blocks cannot improve the universal matrix input-count screen by CP-rank size alone.

The midpoint is not a ceiling for the full denominator-aware geometry. The most promising high-head program keeps the product factors, their positivity, or the exact adjustable Gordan quantifiers.

## Dimension Audit

Let

$$ D&#95;H=\sum&#95;{j=0}^{H}\binom{n}{j} $$

be the dimension of evaluated cube polynomials of degree at most $H$. The projective Chow variety of products of $H$ linear forms has dimension $Hn$. Its tangential variety has dimension at most $2Hn$, and its second secant has dimension at most $2Hn+1$.

Therefore the evaluated tangent and secant closures remain proper whenever

$$ D&#95;H-1>2Hn+1. $$

Near $H=n/2$, the left side is exponential in $n$, while the right side is quadratic. For $n=6$ and $H=3$, one has $D_3-1=41$, while the tangent and secant dimension bounds are $36$ and $37$. This remains true even though the freed slice incidence is dominant in the same case.

Dimension does not refute a specified sign table. It does show that the high-head obstruction has not disappeared. It lives in factor compatibility rather than in one flattening or one freed slice plane.

## Exact Denominator Atlas

For one orientation-count branch, normalize the $H$ denominators in $(\Delta_n)^H$. The parameter dimension is $Hn$, and the effective signed feature dimension is

$$ d=1+Hn. $$

At a fixed denominator tuple $\theta$, exact infeasibility is equivalent to a Gordan multiplier

$$ q\in\Delta&#95;{2^n},\qquad\sum&#95;xq&#95;x r&#95;x(\theta)=0. $$

A lower certificate must cover the adjustable quantifiers

$$ \forall\theta\in(\Delta&#95;n)^H\quad\exists q\in\Delta&#95;{2^n}\quad\sum&#95;xq&#95;x r&#95;x(\theta)=0. $$

The robust positive-basis method remains exact above the midpoint:

1. Solve a rational centered-hull LP at a denominator-cell center.

2. Retain a positive basis using at most $2d=2+2Hn$ truth-table rows.

3. Certify its inradius by rational kernel weights and one exact determinant.

4. Compare that inradius with the attention-specific telescoping row-motion bound.

5. Store the cell, selected rows, convex weights, determinant, and exact comparison.

At $H\asymp n/2$, each robust leaf needs only $O(n^2)$ witness rows. The number of cells can still be exponential in $Hn$. The difficult locus is the zero-inradius discriminant, not a midpoint rank ceiling.

## Positive-Secant Ranking Relaxation

Every strict $H$-head tangent sign pattern has a nearby positive secant of two denominator products with paired orientations:

$$ sQ&#95;1(x)-(1-s)Q&#95;0(x),\qquad Q&#95;a(x)=\prod&#95;{h=1}^{H}B&#95;h^{(a)}(x),\qquad a\in\lbrace0,1\rbrace. $$

Let $P=f^{-1}(1)$ and $N=f^{-1}(0)$. Since the products are positive and $f$ is nonconstant, a valid mixture has $0<s<1$. Its strict signs are equivalent to

$$ \frac{s}{1-s}>\frac{Q&#95;0(p)}{Q&#95;1(p)}\quad\text{for every }p\in P,\qquad \frac{s}{1-s}<\frac{Q&#95;0(n)}{Q&#95;1(n)}\quad\text{for every }n\in N. $$

The scalar $s$ can therefore be eliminated exactly. A positive secant exists if and only if

$$ \max&#95;{p\in P}\frac{Q&#95;0(p)}{Q&#95;1(p)}<\min&#95;{n\in N}\frac{Q&#95;0(n)}{Q&#95;1(n)}. $$

Equivalently, every positive-negative pair satisfies the polynomial inequality

$$ Q&#95;0(p)Q&#95;1(n)<Q&#95;0(n)Q&#95;1(p). $$

This yields an exact necessary condition:

> If the pairwise polynomial system is infeasible in every orientation-count branch, then $H^{\ast}(f)>H$.

The logarithmic statistic is

$$ G(x)=\sum&#95;{h=1}^{H}\left(\log B&#95;h^{(0)}(x)-\log B&#95;h^{(1)}(x)\right). $$

Thus positive secant feasibility is a model-specific likelihood-ratio ranking problem. It uses $2Hn$ factor variables after eliminating $s$. Each pairwise cross inequality has degree $2H$ and is multiaffine across the $2H$ denominator blocks.

### Proposed solver

1. Retain the mixture scalar and replace its joint endpoint diagonal by the signed charts of Theorem 194.

2. Use one signed margin constraint per truth-table vertex. Generate active vertices on demand if the full table is large.

3. Introduce prefix products for $Q_0(x)$ and $Q_1(x)$.

4. Apply rational McCormick envelopes to each bilinear prefix relation.

5. Optimize a common signed margin and add the most violated vertices or a band of near ties.

6. Subdivide product-simplex and direction cells and store exact rational LP dual bounds.

7. Send zero-gap residual cells to the original unblown signed system before invoking Stengle, SOS, NLSAT, or CAD.

The key limitation is structural. Taking $Q_0=Q_1$ makes every pairwise gap zero, so the global maximum gap is always at least zero. When no positive secant exists, the optimum is usually exactly zero. Pure interval subdivision may converge forever without proving equality. Exact zero-valued LP duals can close some cells, while the remaining diagonal or discriminant cells need algebraic certificates.

[McCormick's factorable relaxation](https://doi.org/10.1007/BF01580665) supplies the convergent convex outer approximation. [Stengle's Positivstellensatz](https://doi.org/10.1007/BF01362149) handles strict polynomial infeasibility and zero-margin boundary cases.

### Blow up the diagonal

[Theorem 193](../../lemmas/02_complexity_measure_upper_bounds/193_positive_secant_diagonal_blowup.md) gives an exact repair for the artificial zero family $Q_0=Q_1$. Collect all paired endpoint parameters and write

$$ \theta^{(1)}=\theta^{(0)}+tv,\qquad t=\lVert\theta^{(1)}-\theta^{(0)}\rVert&#95;{\infty}. $$

Use finitely many charts that choose one coordinate $v_j=1$ or $v_j=-1$, with every other coordinate in $[-1,1]$. The blockwise simplex equalities impose zero block sums on $v$. For a positive-negative pair, define

$$ G&#95;{p,n}(t)=Q&#95;0(n)Q&#95;t(p)-Q&#95;0(p)Q&#95;t(n). $$

The polynomial $G_{p,n}(t)$ vanishes at $t=0$, so it is exactly divisible by $t$:

$$ G&#95;{p,n}(t)=t\widetilde G&#95;{p,n}(t). $$

For $t>0$, strict positivity of every divided gap is equivalent to the original positive-secant ranking. At $t=0$, the divided gap is the directional logarithmic derivative

$$ \widetilde G&#95;{p,n}(0)=Q&#95;0(p)Q&#95;0(n)\sum&#95;{h=1}^{H}\left(\frac{\dot B&#95;h(p)}{B&#95;h(p)}-\frac{\dot B&#95;h(n)}{B&#95;h(n)}\right). $$

Thus the diagonal is replaced by normalized tangent directions rather than by an identically zero objective. The theorem proves that strict feasibility at $t=0$ gives a strict positive secant for all sufficiently small $t>0$. On a denominator-simplex face, the direction lies in the one-sided tangent cone. A finite face and maximal-coordinate atlas enforces this condition exactly.

This does not eliminate every zero-gap discriminant, but it removes the largest one and lowers the degree in the scalar separation variable from $H$ to $H-1$. It remains useful for likelihood-ratio diagnostics and active pair discovery.

### Retain the scalar for certified subdivision

[Theorem 194](../../lemmas/02_complexity_measure_upper_bounds/194_signed_secant_diagonal_blowup.md) gives the preferred spatial branch-and-bound formulation. Retain the mixture scalar and write

$$ \theta^{(1)}=\theta+tv,\qquad 2s-1=ta,qquad \max\lbrace\lVert v\rVert&#95;{\infty},\lvert a\rvert\rbrace=1. $$

For each truth-table vertex, the signed secant score is divisible by $t$. Its quotient is

$$ \widetilde{\mathcal S}&#95;x=\frac12\left(\frac{Q&#95;{\theta+tv}(x)-Q&#95;\theta(x)}{t}+a\left(Q&#95;{\theta+tv}(x)+Q&#95;\theta(x)\right)\right). $$

This changes the computational profile materially:

- the constraint count is $2^n$, rather than $\lvert P\rvert\lvert N\rvert$;

- there are no cross-vertex product nodes;

- the standard total degree is at most $2H+1$, rather than $3H-1$ for the divided pair gaps;

- each joint head block $(\theta&#95;h,v&#95;h)$ has degree at most one;

- the normalized chart domain is closed and compact, with no simplex-face implication.

The last point uses strictification. At $t=0$, first perturb the base tuple into the product-simplex interior. The finitely many strict quotient inequalities persist. Then every zero-block-sum direction becomes feasible for a sufficiently short ray. Thus outward-pointing boundary directions are not spurious and no face atlas is needed.

There are $2H(n+1)+2$ raw maximal-coordinate charts. Simultaneous head permutations within an orientation class reduce this to at most $4(n+1)+2$ chart types per orientation-count branch, independent of $H$.

The quotient has a linear-size factor graph. Introduce the shared lift $z&#95;{hi}=tv&#95;{hi}$, so the endpoint constraint $\theta+z\in\Theta$ is linear. For one active vertex define

$$ b&#95;h=B&#95;h(x;\theta&#95;h),\qquad d&#95;h=B&#95;h(x;v&#95;h),\qquad c&#95;h=B&#95;h(x;\theta&#95;h+z&#95;h). $$

Starting with $P&#95;0=1$ and $R&#95;0=0$, use

$$ P&#95;h=P&#95;{h-1}b&#95;h,\qquad R&#95;h=R&#95;{h-1}c&#95;h+P&#95;{h-1}d&#95;h. $$

Then

$$ P&#95;H=Q&#95;\theta(x),\qquad R&#95;H=\frac{Q&#95;{\theta+tv}(x)-Q&#95;\theta(x)}{t},\qquad Q&#95;{\theta+tv}(x)=P&#95;H+tR&#95;H. $$

With $m$ active vertices, this uses $O(Hn)$ shared bilinear nodes and $O(Hm)$ vertex-specific nodes. The redundant exact identity in the last display should be added as an RLT cut because independent McCormick envelopes otherwise forget it.

For a cell $C$, a compact exact infeasibility leaf consists of a rational distribution $\lambda\in\Delta&#95;{2^n}$ and a rational upper certificate

$$ \sup&#95;{z\in C}\sum&#95;x\lambda&#95;x y&#95;x\widetilde{\mathcal S}&#95;x(z)\leq0. $$

Such a leaf rules out simultaneous strict positivity on the whole cell. The polynomial upper bound can come from rational McCormick, RLT, Bernstein, Handelman, or SOS dual data. A single active vertex is the special case where $\lambda$ is a point mass.

The blow-up is not automatically best for algebraic decision procedures. The original retained-s system has $2Hn+1$ dimensions, only $2^n$ constraints, and total degree $H+1$. CAD, NLSAT, and direct Positivstellensatz searches should therefore receive the original system, or a residual cell projected back to it. The signed blow-up is primarily a spatial subdivision and max-margin device.

## Polynomial Adjustable Multipliers

The exact Gordan quantifier suggests a convex sufficient certificate. Search for polynomial weights $\lambda_x(\theta)$ such that

$$ \lambda&#95;x(\theta)\geq0,\qquad \Lambda(\theta):=\sum&#95;x\lambda&#95;x(\theta)>0, $$

and impose the polynomial identity

$$ \sum&#95;x\lambda&#95;x(\theta)r&#95;x(\theta)=0. $$

Then

$$ q&#95;x(\theta)=\frac{\lambda&#95;x(\theta)}{\Lambda(\theta)} $$

is a valid Gordan multiplier for every denominator tuple. This proves $H^{\ast}(f)>H$.

For a fixed policy degree $r$:

- coefficient matching in the annihilation identity is linear;

- a nonnegative Handelman expansion on the product of simplices is an LP certificate for each $\lambda_x$;

- SOS positivity gives a stronger SDP certificate;

- a separate positive lower certificate for $\Lambda$ prevents the policy from vanishing simultaneously;

- every rational result has a small independent coefficient-identity and positivity checker.

The raw number of policy coefficients is approximately

$$ 2^n\binom{Hn+r}{r}. $$

Degree one is polynomial in the truth-table size. The naive identity expansion of degree $H+r$ has $(n+1)^H$ multiblock terms, so the first implementation should use mined truth-table supports, separable or cellwise policies, arithmetic-circuit identity checking, and head-permutation symmetry.

Degree-zero policies contain the fixed threshold-degree dual route. Degree-one and degree-two policies can use denominator dependence and are genuinely model-specific.

[Handelman's theorem](https://doi.org/10.2140/pjm.1988.132.35) and [adjustable robust optimization](https://doi.org/10.1007/s10107-003-0454-y) give the relevant certificate templates. Handelman expansions are used here as sufficient rational positivity certificates, not as an assumption that every boundary-nonnegative policy has a short expansion.

## Small Witness Refutation

The exact $H$-head family has $O(Hn)$ real parameters and degree $O(H)$. Warren and Goldberg-Jerrum growth bounds suggest that random labelings are often refuted on a subset of

$$ O\left(Hn\log(H^2n)\right) $$

vertices. This is a probabilistic mining heuristic, not a deterministic theorem for every specified table.

The residual workflow is:

1. Mine a small hard subset numerically.

2. Formulate the exact denominator or positive-secant system only on that subset.

3. Refute it with NLSAT, CAD, or a bounded-degree Positivstellensatz.

4. Store the subset and exact algebraic certificate.

[Parrilo's SDP hierarchy](https://www.mit.edu/~parrilo/pubs/files/SDPrelaxations.pdf) and [Lasserre's moment hierarchy](https://doi.org/10.1137/S1052623400366802) are complete residual tools in principle. Their moment matrices scale combinatorially with the parameter count and relaxation degree, so they should never receive the unreduced full high-head system first.

## Tangential Equations

The normalized denominator coefficients form a rank-one nonnegative tensor, and the cleared numerator is tangent to its Segre or Chow image. Low-degree tangential equations retain compatibility across all flattenings. [Oeding and Raicu](https://arxiv.org/abs/1111.6202) prove degree bounds for tangential Segre-Veronese ideals, while [Guan](https://arxiv.org/abs/1602.04275) develops equations for Chow secants.

The complete latent head tensor has $(n+1)^H$ entries, and the symmetric coefficient lift of degree $H$ has $\binom{n+H}{H}$ entries. Both are unattractive near $H=n/2$. Selected contractions and equations are useful diagnostics or witness miners, but a complete latent tensor should not be the default arbitrary-table representation.

## Multiway Tensor Limitation

For $k$ coordinate blocks, [Theorem 192](../../lemmas/02_complexity_measure_upper_bounds/192_multiway_sign_tensor_rank.md) gives the tangent cap

$$ R&#95;k(H)=k\left(k^H-(k-1)^H\right). $$

For block sizes $b_1,\ldots,b_k$, every tensor has CP rank at most

$$ 2^{n-\max_i b_i}\leq2^{n-\lceil n/k\rceil}. $$

Asymptotically, even an exact sign-CP oracle can rule out $H$ only in the range

$$ \frac{H}{n}<\frac{1-1/k}{\log&#95;2 k}. $$

The right side is $0.5$ for $k=2$, approximately $0.42062$ for $k=3$, and $0.375$ for $k=4$, then decreases. Matrices are already asymptotically optimal among block counts for reaching the midpoint. Every ordinary tensor flattening is another partition sign-rank test. Generic tensor spectral, nuclear, and rank computations are also NP-hard, as shown by [Hillar and Lim](https://doi.org/10.1145/2512329).

## Ranked Next Prototypes

1. Extend the exact sparse McCormick discovery and cover-tree checker with automatic split selection, active vertex generation, chart symmetry, and a complete global cover manifest.

2. Implement a degree-one adjustable Gordan-policy LP on mined supports. Use Handelman positivity, a positive normalization for $\Lambda$, and an exact rational checker.

3. Compare McCormick, RLT, Bernstein, and low-degree Handelman upper bounds on the same signed cells.

4. Benchmark the secant and policy routes at $(n,H)=(6,3)$ and $(8,4)$. These are the first regimes where slice rank has lost generic force but the full tangent and positive secant remain proper.

5. Project unresolved cells back to the lower-degree original signed system, then feed them to the positive-basis atlas and exact semialgebraic solvers only after witness reduction.

6. Treat tangential Segre or Chow equations as selective diagnostics until a contraction scheme avoids the full latent lift.

## Falsifiable Research Hypotheses

The next experiments should test four concrete hypotheses rather than only report solver time.

1. A degree-one adjustable policy supported on $O(Hn)$ mined rows covers most random infeasible branches away from the denominator boundary.

2. Signed-secant feasibility is controlled by a small active set of vertices, so row generation keeps the working system much smaller than the full truth table on structured examples.

3. After the signed diagonal blow-up, most remaining zero-gap cells lie on identifiable rank-drop or tangent-kernel strata and can be delegated to the positive-basis atlas.

4. For random truth tables, an exact refuting subset of size $O(Hn\log(H^2n))$ is typically sufficient, even though no deterministic worst-case theorem of this size is currently known.

Each hypothesis is easy to falsify by recording support size, active-pair count, residual-cell dimension, and exact witness size across the benchmark suite.
