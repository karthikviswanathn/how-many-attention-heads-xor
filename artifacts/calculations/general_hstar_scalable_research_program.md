# General Scalable Research Program For Certified Head Bounds

## Scope

Let

$$ f:\lbrace0,1\rbrace^n\to\lbrace0,1\rbrace $$

be given by a truth table, and let $H^{\ast}(f)$ be the minimum head count in the one-layer model of [model.md](../../model.md). The goal is not merely to guess $H^{\ast}(f)$. It is to maintain an anytime interval

$$ L(f)\leq H^{\ast}(f)\leq U(f) $$

whose endpoints have independently checkable certificates.

The current conclusion is that a scalable estimator should be a portfolio. Different relaxations see genuinely different obstructions:

1. threshold degree sees only the degree of the cleared polynomial;

2. optimized partition norms see low-rank evaluation matrices;

3. slice rank sees the codimension-two linear space contained in every cleared hypersurface;

4. tangential-Chow secants and flattenings see additional coefficient structure;

5. sparse support and denominator dictionaries search for constructive upper certificates;

6. exact witness subsets see local inconsistency on a small part of the cube;

7. robust positive bases and adjustable Gordan policies cover regions of denominator space;

8. exact real-algebraic solvers handle the small unresolved frontier.

The circuit atlas remains useful, but it should be a residual exact layer rather than the center of the whole methodology.

This notion of scalability is relative to explicit truth-table input. Reading the input already costs $2^n$, so algorithms polynomial in $V=2^n$ are appropriate. If $f$ is given by a circuit or membership oracle, sampled search can discover lower witnesses and candidate constructions, but an exact endpoint still needs a symbolic verifier or an exhaustive cube scan.

## Exact Candidate-Count Problem

Write $y_x=2f(x)-1$. For a fixed orientation branch, normalize denominator $h$ as

$$ B&#95;h(x;\theta&#95;h)=\sum&#95;{i=0}^n\theta&#95;{hi}L&#95;i^{\sigma&#95;h}(x),\qquad \theta&#95;h\in\Delta&#95;n, $$

where $L_0^{\sigma}=1$, $L_i^+(x)=x_i$, and $L_i^-(x)=1-x_i$. Put $a(x)=(1,x_1,\ldots,x_n)$ and define

$$ C&#95;H(x;\theta)=\left(\prod&#95;hB&#95;h(x),\ a(x)\prod&#95;{g\neq1}B&#95;g(x),\ldots,a(x)\prod&#95;{g\neq H}B&#95;g(x)\right). $$

The repeated constant columns leave at most

$$ d=1+Hn $$

effective readout coordinates. With $R(\theta)[x,:]=y_xC_H(x;\theta)$, define

$$ v_H(\theta)=\max_{\lVert w\rVert_1\leq1}\min_xR(\theta)[x,:]w. $$

Then

$$ H^{\ast}(f)\leq H\quad\Longleftrightarrow\quad\max&#95;{\sigma}\max&#95;{\theta\in(\Delta&#95;n)^H}v&#95;H(\theta)>0. $$

Head exchangeability reduces the $2^H$ orientation vectors to $H+1$ orientation counts.

For fixed $\theta$, minimax duality gives

$$ v&#95;H(\theta)=\min&#95;{q\in\Delta&#95;{2^n}}\lVert R(\theta)^{\top}q\rVert&#95;{\infty}. $$

Thus the exact lower-bound quantifiers are

$$ \forall\theta\in(\Delta_n)^H\quad\exists q\in\Delta_{2^n}\quad R(\theta)^{\top}q=0. $$

This is adjustable robust feasibility. Replacing $q$ by one fixed multiplier changes the quantifiers and gives only a sufficient certificate.

## Established Geometric Facts

### Strict classification is unchanged by Euclidean closure

Let $\mathcal S_H\subseteq\mathbb R^{2^n}$ be the set of score vectors produced by $H$ heads, and let

$$ \mathcal O_f=\lbrace s:y_xs_x>0\text{ for every }x\rbrace. $$

Then

$$ \mathcal O_f\cap\mathcal S_H\neq\varnothing\quad\Longleftrightarrow\quad\mathcal O_f\cap\overline{\mathcal S_H}\neq\varnothing. $$

**Proof.** The forward implication is immediate. For the reverse implication, choose $s\in\mathcal O_f\cap\overline{\mathcal S_H}$. The strict orthant $\mathcal O_f$ is open, so some Euclidean ball around $s$ lies inside it. Since $s$ is in the closure of $\mathcal S_H$, that ball contains a point of $\mathcal S_H$. $\blacksquare$

This makes Euclidean border methods exact for strict classification. Passing to a larger Zariski closure is still only a relaxation.

### The cleared form is a Chow tangent

After homogenizing the affine forms with a variable $z_0$, an $H$-head cleared score is a degree $H$ form

$$ P=c\prod&#95;{h=1}^HB&#95;h+\sum&#95;{h=1}^HA&#95;h\prod&#95;{g\neq h}B&#95;g. $$

Absorb the constant term by replacing $A_1$ with $A_1+cB_1$. Then

$$ P=\left.\frac{d}{dt}\prod&#95;{h=1}^H(B&#95;h+tA&#95;h)\right\rvert&#95;{t=0}. $$

Consequently, the projective class of $P$ lies in the tangential variety of the degree $H$ Chow variety of products of linear forms.

The same product-of-sums architecture appears in [Shin and Ghosh's Pi-Sigma network](https://doi.org/10.1109/IJCNN.1991.155142) and their later [ridge polynomial networks](https://doi.org/10.1109/72.377967). The attention normal form is a constrained first-order derivative of one Pi-Sigma product, not a generic sum of independent product units. This older literature is therefore useful for constructive optimization heuristics, but its approximation results do not provide the positivity-aware exact lower certificates needed here.

### Tangential Chow lies in the second secant

For any projective variety $X$, a tangent line is a limit of secant lines. Therefore

$$ \mathrm{Tan}(X)\subseteq\sigma_2(X). $$

Applied to the Chow variety, every cleared $H$-head form has Chow border rank at most two. This does not mean that its ordinary Chow rank is at most two. The distinction is essential.

Chow secants and their equations are studied directly by [Guan](https://arxiv.org/abs/1602.04275), while [Torrance and Vannieuwenhoven](https://arxiv.org/abs/2005.12436) study dimensions and generic ranks of Chow secants. The attention model uses only a highly constrained real, positive part of this geometry.

### A direct real two-product relaxation

The secant containment has a concrete real form that is useful computationally. After absorbing $cB_1$ into $A_1$, put

$$ F(t)=\prod_{h=1}^H(B_h+tA_h). $$

The difference quotient

$$ P_t=\frac{F(t)-F(0)}{t} $$

is a real sum of two products of $H$ real linear forms and converges coefficientwise to the cleared tangent $P$ as $t\to0$. A strict finite-cube sign pattern has positive margin, so for all sufficiently small nonzero real $t$, the form $P_t$ has the same signs as $P$ on the cube.

Consequently, if $H^{\ast}(f)\leq H$, then there exist real scalars and real linear forms satisfying

$$ y&#95;x\left(\lambda\prod&#95;{h=1}^HL&#95;h(1,x)+\mu\prod&#95;{h=1}^HM&#95;h(1,x)\right)>0 $$

for every cube vertex. With $\lambda,\mu$ explicit, this gives an orientation-free candidate $H$ relaxation with $2H(n+1)+2$ raw variables and total parameter degree $H+1$. Absorbing each scalar into one factor removes two variables and gives degree $H$ inequalities. Its infeasibility proves $H^{\ast}(f)>H$; its feasibility is inconclusive. It is stronger than tests that retain only selected secant equations, but its nonconvexity makes it a residual factor-search layer rather than the first coefficient test.

The same argument retains more model structure. First perturb every boundary denominator toward the barycenter of its orientation simplex. The cleared tangent changes continuously, so its strict cube signs persist. For the resulting interior factors, choose $t>0$ small enough that every $B_h+tA_h$ stays in the same orientation cone. Normalize the factors at both endpoints, writing

$$ F(t)=\rho_1Q_1,\qquad F(0)=\rho_0Q_0,\qquad \rho_1,\rho_0>0. $$

Multiplying the difference quotient by $t/(\rho_0+\rho_1)$ gives $sQ_1-(1-s)Q_0$ with $s=\rho_1/(\rho_0+\rho_1)$. A necessary positive-secant relaxation is therefore

$$ y&#95;x\left(s\prod&#95;{h=1}^HB&#95;h^{(1)}(1,x)-(1-s)\prod&#95;{h=1}^HB&#95;h^{(0)}(1,x)\right)>0,\qquad 0\leq s\leq1, $$

where each paired factor $B_h^{(0)},B_h^{(1)}$ has the same orientation and lies in its normalized denominator simplex. This compact problem has $2Hn+1$ scalar dimensions and no numerator variables. It is weaker than positive tangency because it permits arbitrary chords, but stronger than the unrestricted real second-secant relaxation.

There are now two exact treatments of the artificial zero diagonal. [Theorem 193](../../lemmas/02_complexity_measure_upper_bounds/193_positive_secant_diagonal_blowup.md) eliminates $s$ and divides every positive-negative pair gap. [Theorem 194](../../lemmas/02_complexity_measure_upper_bounds/194_signed_secant_diagonal_blowup.md) retains $s$, writes $\theta^{(1)}=\theta+tv$ and $2s-1=ta$, and divides the signed score at each vertex. The signed formulation is preferable for spatial branch-and-bound: it has $2^n$ inequalities instead of $\lvert f^{-1}(1)\rvert\lvert f^{-1}(0)\rvert$, no cross-vertex products, joint head-block degree one, and a closed compact chart domain with no simplex-face cases. The original unblown retained-s system has total degree only $H+1$, so it remains preferable for CAD, NLSAT, or direct Positivstellensatz residual solving.

### A slice-rank-two invariant

There is a simpler necessary condition that does not require a limit. For $H\geq2$, isolate the first head:

$$ P=(A&#95;1+cB&#95;1)\prod&#95;{h=2}^HB&#95;h+B&#95;1\sum&#95;{h=2}^HA&#95;h\prod&#95;{\substack{g=2\\g\neq h}}^HB&#95;g. $$

Thus every cleared $H$-head form can be written

$$ P=L_1Q_1+L_2Q_2, $$

where $L_1,L_2$ are real linear forms and $Q_1,Q_2$ have degree $H-1$. In the standard terminology, $P$ has real polynomial slice rank at most two. Equivalently, the real projective hypersurface $V(P)$ contains the codimension-at-most-two real linear subspace $V(L_1,L_2)$, and the statement remains true after base change to $\mathbb C$. Moreover, $L_2=B_1$ can be chosen from an admissible attention-denominator cone. Dropping this last orientation condition gives a clean algebraic relaxation; retaining it gives a stronger positivity-aware relaxation. The self-contained proof is [Theorem 190](../../lemmas/02_complexity_measure_upper_bounds/190_slice_rank_two_obstruction.md).

For a fixed two-dimensional subspace $U$ of linear forms, the degree $H$ forms in its generated ideal have dimension

$$ \dim I(U)_H=2\binom{n+H-1}{H-1}-\binom{n+H-2}{H-2}. $$

The signed cube-margin problem is therefore an LP once $U$ is fixed. Only $U$ matters, so the nonlinear search is over

$$ \mathrm{Gr}(2,n+1),\qquad \dim\mathrm{Gr}(2,n+1)=2(n-1). $$

The outer dimension is independent of $H$ and grows as roughly $2n$, rather than roughly $2Hn$. That attractive count is not enough. Boolean evaluation can erase the formal coefficient obstruction.

Put

$$ D&#95;d=\sum&#95;{j=0}^{d}\binom{n}{j}. $$

The maximum evaluated fixed-plane rank is exactly

$$ r&#95;H=\min\left\lbrace D&#95;H,2D&#95;{H-1}-D&#95;{H-2}\right\rbrace. $$

This is [Theorem 191](../../lemmas/02_complexity_measure_upper_bounds/191_boolean_cube_slice_relaxation_ceiling.md). If $H\geq\lceil(n+1)/2\rceil$, then $r_H=D_H$: the single plane $\mathrm{span}(1,\sum_i x_i)$ spans every degree at most $H$ cube polynomial and contains admissible positive denominators. Plain and positivity-aware slice rank then collapse exactly to threshold degree. A slice backend must run this rank screen before any Grassmann search.

Below the middle level, the generic fixed-plane codimension is $\binom{n}{H}-\binom{n}{H-1}$. After allowing the $2(n-1)$ Grassmann variables, dimension alone guarantees a proper incidence only when

$$ \binom{n}{H}-\binom{n}{H-1}>2(n-1). $$

In the surviving regime, a practical slice engine should optimize $U$, solve the inner LP, exchange violated cube constraints, and then certify global infeasibility with exact Grassmann cells, elimination equations, or a real-algebraic solver. Failure of a local Grassmann search is not a certificate.

### A bounded Grassmann atlas with robust cells

When the Boolean rank screen leaves room for improvement, the Grassmann search has a particularly simple exact atlas. Put $q=n+1$ and let

$$ N=\binom{n+H-1}{H-1}. $$

For each pair of pivot coordinates $a<b$, write a two-plane as the row span of $[I_2\ T]$ after permuting the coordinates. Normalize the Plücker vector and select a pivot coordinate of largest absolute value. Every entry of $T$ is then a ratio of Plücker coordinates and has absolute value at most one. Consequently, the $\binom q2$ boxes

$$ T\in[-1,1]^{2(q-2)} $$

cover the whole real Grassmannian, with overlap allowed.

Let $L_1(T),L_2(T)$ be the two chart generators and let $m$ range over all degree $H-1$ homogeneous monomials. For a cube point $z=(1,x)$, first form the redundant signed feature row

$$ \widetilde r_x(T)=y_x\left(L_1(T)(z)m(z),L_2(T)(z)m(z)\right)_m\in\mathbb R^{2N}. $$

There is a degree $H$ sign lift in the ideal generated by the plane exactly when some vector strictly separates all these rows from the origin. The redundant coordinates cannot be used directly for an inradius certificate because Koszul relations and Boolean evaluation identities give a common nullspace.

Let $r$ be the generic column rank of the full evaluation matrix on the chart. On a maximal-rank cell, choose $r$ feature columns $C$ and $r$ cube rows whose pivot minor is certified nonzero throughout the cell. Once the generic rank cap $r$ is established, these columns span the full evaluated slice space. Write $r_x^C(T)\in\mathbb R^r$ for the selected row. Gordan's alternative for the selected matrix is then equivalent to the full fixed-plane LP.

The important simplification is that every selected row is affine in $T$. If $r_1$ selected columns come from the $L_1$ block, $r_2$ come from the $L_2$ block, and a chart cell centered at $T_0$ satisfies

$$ \lVert T_i-(T_0)_i\rVert_1\leq\delta_i\qquad (i=1,2), $$

then, for every cube point,

$$ \lVert r_x^C(T)-r_x^C(T_0)\rVert_2\leq\sqrt{r_1\delta_1^2+r_2\delta_2^2}. $$

If the selected center rows contain a certified centered ball of larger radius, the whole rank cell is infeasible. Rational crosspolytope witnesses remove the square roots exactly as in the positive-basis construction below.

There is a smaller exact leaf when the center obstruction has a quantitative positive basis. Let the selected center rows be the rows of $A&#95;S\in\mathbb Q^{s\times r}$, and suppose a rational LP returns weights

$$ \lambda&#95;i\geq t>0,\qquad\sum&#95;{i=1}^{s}\lambda&#95;i=1,\qquad\sum&#95;{i=1}^{s}\lambda&#95;ia&#95;i=0. $$

Let $B$ be any nonsingular $r\times r$ row submatrix of $A_S$. The center hull has Euclidean inradius at least

$$ \rho\geq\frac{t\sigma&#95;{\min}(A&#95;S)}{\sqrt{s}}\geq\frac{t\lvert\det B\rvert}{\sqrt{s}\lVert B\rVert&#95;F^{r-1}}. $$

Thus a uniform row-motion bound $delta$ certifies the entire cell whenever

$$ \delta^2s\lVert B\rVert&#95;F^{2r-2}<t^2(\det B)^2. $$

This certificate needs one rational kernel LP, one nonzero determinant, and one exact integer inequality. Because the moved hull still contains a ball, the selected evaluation matrix keeps row rank $r$ throughout the cell. Once $r$ is already a global rank cap, no separate interval proof for a pivot minor is needed.

This gives a branch-and-bound lower certificate with only $2(n-1)$ outer variables and affine row motion. It needs a certified rank pivot, but it does not need a cofactor formula for the Gordan multiplier. The maximal-Plücker boxes are a complete compact cover. Once every maximal-rank cell is covered, closedness extends infeasibility to the rank-deficient locus. Cells with zero inradius still require subdivision, a circuit, elimination equations, or an exact real-arithmetic solver. For the positivity-aware refinement, add an admissible normalized denominator $B\in U$ and quotient the redundant choice of $B$ within the plane; the plain slice atlas should be attempted first because it has fewer variables.

The formal homogeneous count can be badly misleading after cube evaluation. For $n=6$ and $H=3$, the evaluated fixed-plane rank is $37$ inside the $42$-dimensional degree-three cube space, while the Grassmannian has dimension $10$. An exact parameter-Jacobian calculation attains rank $42$, so the evaluated slice incidence is Zariski dense and contains a real open set. The executable certificate is [boolean_cube_slice_rank_and_n6_cubic_dominance.md](boolean_cube_slice_rank_and_n6_cubic_dominance.md). It may still miss individual sign cones, but the formal projective count $58<83$ is not evidence that it does. For $n=6$ and $H=4$, the collapse is complete: slice feasibility is exactly degree-four threshold feasibility.

The slice form also implies

$$ \mathrm{Sing}(V(P))\supseteq V(L_1,L_2,Q_1,Q_2). $$

Over the complex numbers, when $n+1\geq5$, the singular locus therefore has codimension at most four in the ambient projective space, equivalently at most three inside $V(P)$ when $P\neq0$. This weaker consequence can be tested with Jacobian and Macaulay rank conditions before attempting the full slice incidence problem. [Flavi, Gesmundo, Oneto, and Ventura](https://arxiv.org/abs/2509.12322) develop determinantal equations for small strength from syzygies of partial derivatives, together with a generic-section reduction theorem for cubic slice rank two. Slice rank at most two implies strength at most two, so the strength equations are necessary prefilters here. Whether their strongest matrices remain economical after intersecting the truth-table sign cone is an open implementation question.

There is a concrete cubic pilot. With seven homogeneous variables, $H=3$, and Macaulay degree four, multiplication by the seven quadratic partial derivatives gives a $210\times196$ matrix. Slice rank at most two forces its rank to be at most $169$. This is a moderate-size numerical rank screen, and a fixed-form Hilbert-series computation is practical. Direct $170\times170$ exact minors can still be expensive, and any selected minor constrains only one coefficient lift unless it is embedded in the full truth-table feasibility problem. The Jacobian condition is only necessary, so a feasible result remains inconclusive.

### Balanced split-form relaxation

For any split of the head indices into nonempty blocks $I,J$ of sizes $1\leq k\leq H-1$ and $H-k$, define the block products and tangents after absorbing the constant term into one numerator:

$$ F&#95;I=\prod&#95;{i\in I}B&#95;i,\qquad G&#95;I=\sum&#95;{i\in I}A&#95;i\prod&#95;{r\in I\setminus\lbrace i\rbrace}B&#95;r, $$

and analogously define $F_J,G_J$. Grouping the tangent terms gives

$$ P=G_IF_J+F_IG_J, $$

where $F_I,G_I$ have degree $k$ and $F_J,G_J$ have degree $H-k$. Freeing all four block forms gives a bilinear relaxation with

$$ 2\left(\binom{n+k}{k}+\binom{n+H-k}{H-k}\right) $$

coefficient variables. A balanced split scales as $O(n^{\lceil H/2\rceil})$, rather than the $O(n^H)$ full coefficient lift, and all truth-table inequalities are bilinear in the two blocks. For $k=1$ or $k=H-1$, freeing the factors gives exactly the slice-rank-two form. Internal splits with $2\leq k\leq H-2$ exist only when $H\geq4$ and provide distinct necessary conditions. Intersecting all available splits with slice and catalecticant constraints gives a stronger combined system, although strict improvement on a given sign cone must be tested. A positivity-aware intermediate layer keeps $F_I,F_J$ as products of admissible denominators while freeing $G_I,G_J$.

### Catalecticant rank bound

Let $\mathrm{Cat}_k(P)$ be the order $k$ derivative catalecticant of a homogeneous degree $H$ form. If

$$ Q=\prod_{h=1}^HL_h, $$

then every order $k$ derivative of $Q$ lies in the span of the products obtained by deleting $k$ distinct factors. Hence

$$ \mathrm{rank}\left(\mathrm{Cat}_k(Q)\right)\leq\binom{H}{k}. $$

Catalecticant rank is subadditive, and the condition that a matrix have rank at most $r$ is closed. The second-secant containment therefore gives the necessary condition

$$ \mathrm{rank}\left(\mathrm{Cat}_k(P)\right)\leq2\binom{H}{k}\qquad 0\leq k\leq H. $$

In particular,

$$ \mathrm{rank}\left(\mathrm{Cat}_1(P)\right)\leq2H. $$

The first catalecticant rank is the number of essential linear directions of the form. Thus every $H$-head cleared form depends on at most $2H$ linear directions, even though it is evaluated in $n+1$ homogeneous variables.

This motivates the linear-form threshold dimension

$$ \mathrm{ltdim}&#95;H(f)=\min\left\lbrace\mathrm{rank}\left(\mathrm{Cat}&#95;1(P)\right):y&#95;xP(1,x)>0\text{ for every }x\right\rbrace, $$

where $P$ ranges over homogeneous degree $H$ forms. Then

$$ H^{\ast}(f)\leq H\quad\Longrightarrow\quad\mathrm{ltdim}_H(f)\leq2H. $$

For a fixed polynomial, gradient-span methods detect and exploit dependence on a few linear forms. [Lasserre](https://arxiv.org/abs/2204.01319) gives exact and sampled detection procedures and low-dimensional optimization reductions. The new difficulty here is that the polynomial itself must be chosen from a truth-table sign cone.

The first-catalecticant test is useful only when $n+1>2H$. For example, a cubic three-head obstruction can use it starting at six input bits, where it asks whether every cubic sign lift needs all seven homogeneous directions. When $n+1\leq2H$, middle catalecticants and stronger flattenings may still be nontrivial.

For $H=2$, this recovers the rank-four quadratic obstruction that appears in the strict separation calculations. Real inertia and admissible-factor orientation can strengthen rank alone.

### Exact quadratic second-secant relaxation

For $H=2$, write

$$ P=A_1B_2+A_2B_1. $$

The symmetric matrix of one product of two real linear forms has at most one positive and one negative eigenvalue. Inertia is subadditive under matrix addition, so the quadratic matrix $M_P$ satisfies

$$ n&#95;+(M&#95;P)\leq2,\qquad n&#95;-(M&#95;P)\leq2. $$

Equivalently, the real second-secant relaxation can be parameterized as

$$ M_P=U\mathrm{Diag}(1,1,-1,-1)U^{\top}, $$

with zero columns allowed. The truth-table inequalities become

$$ y_x(1,x)^{\top}U\mathrm{Diag}(1,1,-1,-1)U^{\top}(1,x)\geq1. $$

This is a quadratic feasibility problem in $4(n+1)$ factor variables. It omits the requirement that one of the two base factors be an admissible attention denominator, but it is strictly stronger than threshold degree and stronger than rank at most four alone.

### Coefficient-lift lower invariant

Let

$$ M_H=\binom{n+H}{H} $$

be the number of coefficients of a degree $H$ homogeneous form in $n+1$ variables. Consider the feasibility problem

$$ y_xP(1,x)\geq1\qquad\text{for every }x\in\lbrace0,1\rbrace^n, $$

together with

$$ \mathrm{rank}\left(\mathrm{Cat}_k(P)\right)\leq2\binom{H}{k}. $$

If this system is infeasible for any one $k$, then

$$ H^{\ast}(f)>H. $$

This is a valid relaxation because every true $H$-head representation supplies such a homogeneous form. Feasibility is inconclusive because the rank constraints omit the full Chow equations, reality conditions, denominator positivity, and orientation.

The rank constraints must be applied to the raw homogeneous coefficient lift. Multilinear reduction modulo $x_i^2-x_i$ can change formal derivative flattenings and is not interchangeable with this argument without a separate proof.

For fixed small $H$, the coefficient lift is polynomial in $n$. Representative sizes are:

| $n$ | Quadratic lift | Cubic lift | Quartic middle lift |
| ---: | ---: | ---: | ---: |
| $6$ | $28$ coefficients, $7\times7$, rank at most $4$ | $84$ coefficients, $7\times28$, rank at most $6$ | $210$ coefficients, $28\times28$, rank at most $12$ |
| $8$ | $45$ coefficients, $9\times9$, rank at most $4$ | $165$ coefficients, $9\times45$, rank at most $6$ | $495$ coefficients, $45\times45$, rank at most $12$ |
| $12$ | $91$ coefficients, $13\times13$, rank at most $4$ | $455$ coefficients, $13\times91$, rank at most $6$ | $1820$ coefficients, $91\times91$, rank at most $12$ |
| $20$ | $231$ coefficients, $21\times21$, rank at most $4$ | $1771$ coefficients, $21\times231$, rank at most $6$ | $10626$ coefficients, $231\times231$, rank at most $12$ |

The cube evaluation inequalities still number $2^n$. Constraint exchange can reduce the working set during search, but an accepted upper certificate still needs a full scan and an exact lower certificate needs a sound infeasibility witness.

### Grassmann variable projection

The first-catalecticant relaxation has a lower-dimensional search form. Put $r=2H$ and choose an $r$-dimensional subspace represented by a full-rank matrix

$$ U\in\mathbb R^{(n+1)\times r}. $$

Every homogeneous degree $H$ form with essential linear dimension at most $r$ can be written

$$ P(z)=g(U^{\top}z) $$

for a homogeneous degree $H$ form $g$ in $r$ variables. For fixed $U$, the coefficients of $g$ enter the truth-table inequalities linearly. Thus the best signed margin is one LP with feature rows

$$ \Phi_U(x,\alpha)=\left(U^{\top}(1,x)\right)^{\alpha},\qquad \lvert\alpha\rvert=H. $$

Only the subspace of $U$ matters, so the nonlinear search lives on a Grassmannian of dimension

$$ r(n+1-r)=2H(n+1-2H), $$

when $2H<n+1$. This suggests a second variable-projection engine:

1. optimize the subspace $U$ on the Grassmannian;

2. solve the inner signed-margin LP for $g$;

3. use constraint exchange to discover active cube vertices;

4. exactify rank or minor obstructions in coefficient space;

5. attempt robust Gordan cells in subspace coordinates only after the numerical geometry is understood.

A feasible point proves only that the coefficient relaxation is feasible. It does not give an attention upper bound. A failed local search proves nothing. The value of this engine is to test and mine certificates for the new lower layer at roughly $O(Hn)$ nonlinear dimension.

### Stronger coefficient flattenings

Catalecticants are only the first family of equations. Koszul and Young flattenings produce equations for Chow varieties and their secants, as developed by [Guan](https://arxiv.org/abs/1510.00886). Shifted partial derivatives are the related arithmetic-circuit measure used for products and low-depth formulas, for example by [Amireddy, Garg, Kayal, Saha, and Thankey](https://arxiv.org/abs/2211.07691).

The proposed order is:

1. first catalecticant rank;

2. middle catalecticants;

3. Koszul or Young flattenings;

4. selected shifted-partial matrices;

5. full Chow-secant equations only on small residual instances.

Each layer is a necessary condition. Exact infeasibility needs rational minors, an exact real-algebraic certificate, or a rationalized SOS certificate. A small singular value is only a search signal.

## Independence-Tensor Lift

Expand the denominator product in the literal basis:

$$ \prod&#95;{h=1}^HB&#95;h(x)=\sum&#95;{c&#95;1,\ldots,c&#95;H}\pi&#95;{c&#95;1,\ldots,c&#95;H}\prod&#95;{h=1}^HL&#95;{c&#95;h}^{\sigma&#95;h}(x), $$

where

$$ \pi=\theta_1\otimes\cdots\otimes\theta_H. $$

Thus $\pi$ is a nonnegative rank-one probability tensor. It is the independence model, or the nonnegative part of a Segre variety. In the same coordinates, the cleared numerator is a tangent vector

$$ c\pi+\sum_{h=1}^H\theta_1\otimes\cdots\otimes\eta_h\otimes\cdots\otimes\theta_H, $$

followed by a fixed linear evaluation map to the Boolean cube.

This produces a natural relaxation ladder.

1. **Degree only.** Forget tensor rank and tangency. The product literals span all multilinear polynomials of degree at most $H$, giving the threshold-degree LP.

2. **Marginal consistency.** Retain low-order marginals of the rank-one tensor and impose consistency constraints.

3. **Flattening constraints.** Enforce selected rank-one minors and tangential catalecticant or Koszul ranks.

4. **Sparse moment constraints.** Use moment matrices for small groups of head blocks.

5. **Exact factorization.** Restore the head vectors $\theta_h$ and tangent directions $\eta_h$.

Theta bodies provide SDP relaxations for polynomial ideals, as introduced by [Gouveia, Parrilo, and Thomas](https://doi.org/10.1137/090746525). Rank-one tensor optimization also has direct SOS relaxations, for example [Nie and Wang](https://arxiv.org/abs/1308.6562).

There is an important warning. Intersecting the truth-table sign cone with the convex hull of the model image can be much weaker than intersecting the model itself. A useful moment relaxation must preserve the existential parameter constraints and converge to their feasibility problem. It should not silently replace the model by an arbitrary mixture of models.

## Partition Matrix Bounds

For every coordinate bipartition $I\sqcup J$, let $S_{I,J}$ be the truth-table sign matrix. The proved tangent expansion gives

$$ \mathrm{srank}(S_{I,J})\leq2^{H^{\ast}(f)+1}-2. $$

Therefore any certified sign-rank lower bound $r$ yields

$$ H^{\ast}(f)\geq\left\lceil\log_2(r+2)\right\rceil-1. $$

The current implementation uses Forster's spectral bound with an exact integer Gram-matrix upper bound on the spectral norm.

A stronger general backend comes from Linial, Mendelson, Schechtman, and Shraibman. Their variant after Lemma 4.4 applies to every real matrix $W$ with sign pattern $S$. For an $M\times N$ sign matrix, define the optimized sign-realization value

$$ \tau(S)=\min\left\lbrace\gamma&#95;2^{\ast}(W):S&#95;{ij}W&#95;{ij}\geq1\text{ for every }i,j\right\rbrace. $$

Then

$$ \mathrm{srank}(S)\geq\frac{MN}{\tau(S)}. $$

See [Complexity Measures of Sign Matrices](https://www2.mta.ac.il/~adish/Pubs/Papers/complexity_matrices.pdf). This is stronger than evaluating the norm only at the literal matrix $W=S$.

The optimized value has one joint SDP. Define

$$ C(W)=\begin{bmatrix}0&W/2\\W^{\top}/2&0\end{bmatrix}. $$

Then

$$ \tau(S)=\min&#95;{W,z}\left\lbrace\sum&#95;{k=1}^{M+N}z&#95;k:S\circ W\geq\mathbf1,\ z\geq0,\ \mathrm{Diag}(z)-C(W)\succeq0\right\rbrace. $$

Any rational feasible pair $(W,z)$ gives the safe certificate

$$ U=\sum_kz_k\geq\tau(S),\qquad \mathrm{srank}(S)\geq\left\lceil\frac{MN}{U}\right\rceil. $$

The checker needs only the entrywise sign-margin inequalities and an exact rational PSD check, for example a rational $LDL^{\top}$ factorization. No proof of optimality is required. The SDP has PSD order $M+N$ and $MN+M+N$ main scalar variables. Because $W=S$ is feasible,

$$ \tau(S)\leq\gamma_2^{\ast}(S), $$

so this backend formally dominates the literal $\gamma_2^{\ast}$ certificate. It also dominates the optimized spectral star bound through

$$ \tau(S)\leq\sqrt{MN}\min_{S\circ W\geq\mathbf1}\lVert W\rVert_2. $$

There is one stronger convex-geometric extension. [Hatami, Hatami, Pires, Tao, and Zhao](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2022.22) prove

$$ \mathrm{srank}(S)\geq\frac1{m_{\mathrm{avg}}(S)}. $$

For rational row and column distributions $p,q$, let

$$ \phi&#95;{p,q}(S)=\max\left\lbrace\sum&#95;{ij}p&#95;iq&#95;jS&#95;{ij}B&#95;{ij}:\gamma&#95;2(B)\leq1,\ S\circ B\geq0\right\rbrace. $$

Writing the minimum over rows as a minimum over $p\in\Delta_M$ and applying Sion's theorem for each fixed $q\in\Delta_N$ gives the equivalent product formulation

$$ m&#95;{\mathrm{avg}}(S)=\inf&#95;{p\in\Delta&#95;M,\ q\in\Delta&#95;N}\phi&#95;{p,q}(S). $$

The weak inequalities $S\circ B\geq0$ describe the closure of strict sign realizations. The supremum is unchanged because an arbitrarily small strict realization can be added in an orthogonal direct sum.

For fixed $p,q$, define

$$ E&#95;{ij}=\frac{S&#95;{ij}}2\left(e&#95;ie&#95;{M+j}^{\top}+e&#95;{M+j}e&#95;i^{\top}\right),\qquad C&#95;{p,q}=\sum&#95;{ij}p&#95;iq&#95;jE&#95;{ij}. $$

A rational feasible point of the dual SDP

$$ \min&#95;{z,\beta}\left\lbrace\sum&#95;kz&#95;k:z\geq0,\ \beta\geq0,\ \mathrm{Diag}(z)-C&#95;{p,q}-\sum&#95;{ij}\beta&#95;{ij}E&#95;{ij}\succeq0\right\rbrace $$

with value $U=\sum_kz_k$ satisfies

$$ U\geq\phi&#95;{p,q}(S)\geq m&#95;{\mathrm{avg}}(S),\qquad \mathrm{srank}(S)\geq\left\lceil\frac1U\right\rceil. $$

Uniform $p,q$ recover $\phi_{p,q}(S)=\tau(S)/(MN)$. Searching nonuniform product weights can therefore improve the optimized-realization bound. Global solution of the outer nonconvex weight problem is unnecessary: every chosen rational $p,q$ and every exact inner dual certificate is independently safe.

The fixed-weight dual has the same implementation as weighted $\tau$. Eliminate $\beta$ by setting $W&#95;{ij}=S&#95;{ij}(p&#95;iq&#95;j+\beta&#95;{ij})$. Then

$$ \phi&#95;{p,q}(S)=\min&#95;{W,z}\left\lbrace\sum&#95;kz&#95;k:S\circ W\geq pq^{\top},\ \mathrm{Diag}(z)-C(W)\succeq0\right\rbrace. $$

The same inner solver and exact checker therefore handle both $\tau$ and product average margin. An outer alternating search can optimize $p$ with $q$ fixed, then $q$ with $p$ fixed. Each subproblem is convex, but global convergence is not needed for validity. Zero weights automatically select a deterministic submatrix. In a diagnostic pilot, an $8\times8$ Sylvester block padded by all-positive entries had uniform value about $0.68$ at size $16\times16$ and about $0.83$ at size $32\times32$. Weights supported uniformly on the hard block gave about $0.353546$ in both cases, which is already consistent with a sign-rank-three certificate after exact repair.

For these particular block PSD duals, diagonally dominant and scaled diagonally dominant inner cones are safe but useless. In the optimized $\tau$ SDP, scaled diagonal dominance with positive scaling entries $d$ forces

$$ \sum&#95;kz&#95;k\geq\frac12\sum&#95;{ij}\lvert W&#95;{ij}\rvert\left(\frac{d&#95;{M+j}}{d&#95;i}+\frac{d&#95;i}{d&#95;{M+j}}\right)\geq\sum&#95;{ij}\lvert W&#95;{ij}\rvert\geq MN. $$

It therefore certifies only sign-rank one. The same calculation in the product-average dual gives $U\geq1$ and again only rank one. Nontrivial scalable substitutes must retain larger PSD blocks, use matrix-free optimization followed by a full rational PSD check, or work on deterministic submatrices. Fixed exception sets combined with the Razborov and Sherstov hybrid Forster bound give another route when a few entries dominate the spectral obstruction.

Factor-width cones have a related ceiling. If $Q=\mathrm{Diag}(z)-C(W)$ is represented as a sum of positive semidefinite blocks, each supported on at most $k$ coordinates, then

$$ \sum&#95;az&#95;a=\mathrm{tr}(Q)\geq\frac{1}{k-1}\sum&#95;{ij}\lvert W&#95;{ij}\rvert. $$

For $\tau$, the right side is at least $MN/(k-1)$, so the resulting sign-rank certificate is at most $k-1$. For product weights it is at least $1/(k-1)$, with the same rank ceiling. Therefore a factor-width relaxation with width $k$ can prove $H^{\ast}(f)\geq h$ only if $k\geq2^h$, since ruling out $h-1$ heads needs sign-rank at least $2^h-1$. Small fixed blocks cannot scale to large head lower bounds.

A practical dependency-light discovery solver is a semi-infinite LP cutting-plane method, following [Krishnan and Mitchell](https://optimization-online.org/2001/08/365/). The PSD condition is the family $v^{\top}Qv\geq0$. Given $v=(a,b)$, add the linear cut

$$ a^{\top}Wb-\sum&#95;ia&#95;i^2z&#95;i-\sum&#95;jb&#95;j^2z&#95;{M+j}\leq0. $$

Solve the current LP with HiGHS, compute the most negative eigenvectors of $Q$, add their violated cuts, and repeat. A $16\times16$ Sylvester pilot reached objective $63.999998$ with minimum eigenvalue above $-10^{-6}$ in $26$ rounds and about $0.6$ seconds. A $32\times32$ pilot reached $181.019330$ in $37$ rounds and about $12$ seconds, close to the known value $181.019336$. These are candidate points only.

Exactification should repair a nearly feasible matrix rather than impose diagonal dominance on $Q$ itself. Round $W,z&#95;0$ and an approximate Gram factor to rational data, put

$$ Q&#95;0=\mathrm{Diag}(z&#95;0)-C(W),\qquad E=Q&#95;0-LL^{\top}, $$

and define

$$ \delta&#95;i=\max\left\lbrace0,\sum&#95;{j\neq i}\lvert E&#95;{ij}\rvert-E&#95;{ii}\right\rbrace. $$

Then $E+\mathrm{Diag}(\delta)$ is symmetric diagonally dominant with nonnegative diagonal, hence positive semidefinite, and

$$ Q&#95;0+\mathrm{Diag}(\delta)=LL^{\top}+E+\mathrm{Diag}(\delta)\succeq0 $$

holds exactly. The certificate stores rational $W,z&#95;0,L,\delta$; the verifier checks the sign margins, the exact residual identity, and diagonal dominance using integer arithmetic after clearing denominators. This repair can be much tighter than requiring $Q$ itself to be diagonally dominant.

The standalone implementation is [weighted_tau_partition_pilot.py](weighted_tau_partition_pilot.py). It uses only NumPy, SciPy, and Python `Fraction` arithmetic. Its current exact smoke results are:

| Sign matrix | Exact weighted objective | Certified sign-rank |
| --- | ---: | ---: |
| All-positive $4\times4$ | $1075102001/1073741824$ | $1$ |
| Sylvester $4\times4$ | $134484937/268435456$ | $2$ |
| Sylvester $8\times8$ | $1527368337/4294967296$ | $3$ |
| Sylvester $8\times8$ core padded to $16\times16$ | $3/8$ | $3$ |

The complete smoke run takes about one second on the current machine. The first three certificates are rationalized numerical discoveries. The padded certificate is an exact analytic construction and verifies after a JSON round trip. Fixed weights, dense eigendecomposition, and cubic exact Gram checking remain the main limitations.

The tangent theorem also gives the side-sensitive cap. If

$$ B(a,h)=\sum_{i=0}^{\min(h,a)}\binom{a}{i}, $$

then every feasible head count $h$ satisfies

$$ \min\left\lbrace2^{h+1}-2,B(\lvert I\rvert,h),B(\lvert J\rvert,h)\right\rbrace\geq r. $$

However, the two binomial terms never strengthen the inversion. If a side size $s\leq h$, then $B(s,h)=2^s\geq r$ because sign-rank cannot exceed that matrix side. If $s\geq h+1$, then $B(s,h)\geq2^{h+1}-1>2^{h+1}-2$. Thus the logarithmic conversion from the universal cap is already optimal among these three caps. The binomial bounds remain useful only as consistency checks. Any deterministic submatrix is valid because sign-rank cannot increase when rows or columns are deleted.

The estimator should optimize over several balanced and unbalanced partitions and over deterministic submatrices. The matrix ladder is literal spectral, optimized spectral star, optimized $\tau$, and then product average margin. A failed numerical SDP must have no effect on $L(f)$.

Before running that ladder at candidate count $H$, apply the side-size screen. Ruling out $H$ heads needs sign-rank at least $2^{H+1}-1$, but a partition matrix has sign-rank at most $2^{\min(\lvert I\rvert,\lvert J\rvert)}$. Hence the matrix route can improve the endpoint only if

$$ \min(\lvert I\rvert,\lvert J\rvert)\geq H+1, $$

which requires $n\geq2H+2$. The exact objective stopping thresholds are

$$ U<\frac{MN}{2^{H+1}-2} $$

for $\tau$, and

$$ U<\frac1{2^{H+1}-2} $$

for weighted $\tau$. Once exact repair preserves the relevant strict inequality, further numerical optimization is unnecessary.

Nonuniform weights can matter qualitatively. Embed an $8\times8$ Sylvester matrix in an otherwise all-positive larger matrix, and put $p,q$ uniformly on the hard block. Set $W&#95;{ij}=S&#95;{ij}/64$ on that block and zero elsewhere, and set each of the sixteen active diagonal variables to $3/128$. The active dual block is positive semidefinite because

$$ \frac3{128}>\frac{\sqrt2}{64}, $$

which is exactly the integer inequality $9>8$ after squaring. Its objective is $3/8$, so every padded matrix has certified sign-rank at least three. Uniform weights dilute this hard core.

Unbounded-error communication complexity is essentially the logarithm of sign-rank, so it is a reformulation of this backend rather than an independent one. Exact sign-rank is not an appropriate default solver: deciding whether a sign matrix has sign-rank at most three is already hard, as shown by [Bhangale and Kopparty](https://arxiv.org/abs/1503.04486). The average-margin, VC-dimension, and monochromatic-rectangle methods are also incomplete. Hatami and coauthors construct matrices of polynomial sign-rank on which all three remain constant.

Recent methods may strengthen structured families without yet giving a generic table backend. [Frick, Hosseini, and Vasileuski](https://arxiv.org/abs/2604.01510) use a $\mathbb Z_2$-topological index to lower-bound exact sign-rank, with sharp Gap Hamming Distance applications. [Bindu, Hatami, Karimi, and Robere](https://arxiv.org/abs/2605.01038) use hyperplane avoidance for approximate sign-rank. Since approximate sign-rank is a relaxation of exact sign-rank, its lower bounds also apply to exact sign-rank. The published certificates are currently family-specific or asymptotic, so these belong in the structured-function layer rather than the default arbitrary-table implementation.

### Multiway partition tensor extension

There is an exact $k$-block extension of the tangent rank cap. Partition the variables into nonempty blocks $I&#95;1,\ldots,I&#95;k$, evaluate the truth table as a $k$-tensor, and define its sign CP rank as the least real CP rank among tensors with the same strict sign pattern. If $f$ is nonconstant and $H=H^{\ast}(f)$, then

$$ \mathrm{signCP}_{I&#95;1,\ldots,I&#95;k}(f)\leq k\left(k^H-(k-1)^H\right). $$

To prove the bound, decompose each affine numerator and denominator as a sum of $k$ block functions. For an assignment $\tau:\lbrace1,\ldots,H\rbrace\to\lbrace1,\ldots,k\rbrace$, let

$$ A&#95;{\tau,b}=\prod&#95;{h:\tau(h)=b}d&#95;{h,b},\qquad R&#95;{\tau,b}=\sum&#95;{h:\tau(h)=b}n&#95;{h,b}\prod&#95;{\substack{g\neq h\\ \tau(g)=b}}d&#95;{g,b}. $$

The contribution indexed by $\tau$ is

$$ c\prod&#95;bA&#95;{\tau,b}+\sum&#95;bR&#95;{\tau,b}\prod&#95;{a\neq b}A&#95;{\tau,a}. $$

Choose one occupied block and absorb the first product into its $R$ factor. The contribution then has CP rank at most $\lvert\mathrm{im}(\tau)\rvert$. Finally,

$$ \sum&#95;{\tau}\lvert\mathrm{im}(\tau)\rvert=k\left(k^H-(k-1)^H\right), $$

because a fixed block is used by $k^H-(k-1)^H$ assignments.

For $k=2$, this is exactly $2^{H+1}-2$. The ambient CP-rank ceiling for block sizes $n&#95;1,\ldots,n&#95;k$ is

$$ 2^{n-\max&#95;j n&#95;j}\leq2^{n-\lceil n/k\rceil}. $$

[Theorem 192](../../lemmas/02_complexity_measure_upper_bounds/192_multiway_sign_tensor_rank.md) proves the resulting universal limitation exactly. If $H\geq2$ and $n\leq2H+1$, then this ambient ceiling is at most $k(k^H-(k-1)^H)$ for every $k\geq2$. Thus even an exact sign-CP-rank oracle cannot improve the balanced matrix input-count screen by rank size alone. Useful multiway methods would have to enforce compatibility among flattenings, factor positivity, or shared tangential equations. CP-rank optimization is also substantially harder, so this remains a structured-function research layer rather than a default backend. The communication-tensor connection is developed in [Villagra, Nakanishi, Yamashita, and Nakashima](https://arxiv.org/abs/1202.6444).

### Why discrepancy is only conditional

Margin complexity and discrepancy can be strong for well-conditioned representations, but they do not lower-bound ordinary $H^{\ast}$ without additional hypotheses. Sign-rank permits arbitrarily small margins. In particular, low sign-rank can coexist with exponentially small discrepancy.

The last phenomenon is proved quantitatively by [Hatami, Hosseini, and Lovett](https://theoryofcomputing.org/articles/v018a019/). It blocks any unconditional inference from discrepancy alone to ordinary head complexity.

If denominators are normalized so that

$$ \max_xB_h(x)=1,\qquad \min_xB_h(x)\geq\delta, $$

and the rational score is normalized with

$$ \max_x\lvert S(x)\rvert=1,\qquad \min_x\lvert S(x)\rvert\geq\gamma, $$

then the cleared matrix has rank at most $r=2^{H+1}-2$, maximum entry at most one, and minimum absolute entry at least $\gamma\delta^H$. Standard factorization and discrepancy inequalities then constrain $H$, $\gamma$, and $\delta$ jointly. This is useful for $H^{\ast}_{\kappa}$ and for diagnosing ill-conditioning, but it is not an unconditional lower bound on $H^{\ast}$.

## Rational Approximation And Threshold Density

The rational-function literature initially looks closer to the model than it is.

If a rational function $p/q$ has $q>0$ on the cube, then

$$ \mathrm{sign}(p/q)=\mathrm{sign}(p). $$

Consequently, minimum sign degree with a positive denominator is exactly threshold degree. The denominator becomes informative only after imposing the shared-factor tangent identity

$$ p=c\prod_hB_h+\sum_hA_h\prod_{g\neq h}B_g. $$

Uniform rational approximation degree is also not an unconditional lower bound for head complexity. Linear threshold functions have $H^{\ast}=1$, while some halfspaces have large rational approximation degree. Rational approximation remains relevant for composition theorems, intersections of halfspaces, and conditioned margins, but it should not be presented as a direct estimator of $H^{\ast}$.

Threshold density has a valid but mostly degree-level direction. If $D(f)$ is a certified lower bound on the number of Walsh monomials in any sign-representing polynomial, then an $H$-head representation implies

$$ D(f)\leq\sum_{i=0}^{H}\binom{n}{i}. $$

Inverting this inequality gives a lower bound on $H^{\ast}$. It normally recovers a coarse threshold-degree obstruction and does not see the tangential-Chow structure.

Sherstov's work on intersections of halfspaces develops rational approximation and Walsh threshold density in a form relevant to this comparison; see [The Intersection of Two Halfspaces Has High Threshold Degree](https://arxiv.org/abs/0910.1862).

## Average-Sensitivity Presolve

Average sensitivity gives a very cheap degree screen. Let $E(f)$ be the number of undirected cube edges whose endpoints receive different labels. Then

$$ \mathrm{AS}(f)=\frac{E(f)}{2^{n-1}}. $$

[Diakonikolas, Raghavendra, Servedio, and Tan](https://arxiv.org/abs/0909.5011) prove the explicit bound

$$ \mathrm{AS}(f)\leq2n^{1-1/2^d} $$

for every degree $d$ PTF, with the sharper bound $\mathrm{AS}(f)\leq\sqrt n$ for $d=1$. Since an $H$-head function is a PTF of degree at most $H$, the following integer comparisons are certified lower screens:

$$ E(f)^2>n2^{2n-2}\quad\Longrightarrow\quad H^{\ast}(f)>1, $$

and, for $H\geq2$,

$$ E(f)^{2^H}>2^{n2^H}n^{2^H-1}\quad\Longrightarrow\quad H^{\ast}(f)>H. $$

The edge count costs $O(n2^n)$ and the same test can be run on selected restrictions. It is exact and portable, but usually weak. In small pilot calculations it did not beat the threshold-degree lower bound on parity, the six-bit parity perturbation, or random truth tables. [Kane's](https://arxiv.org/abs/1210.1283) later near $\sqrt n$ bound has hidden degree-dependent constants, so it is not yet a convenient finite integer certificate. The [2026 Boolean-surface-area bound](https://arxiv.org/abs/2604.08095) controls $\mathbb E\sqrt{s&#95;f(x)}$, not average sensitivity itself, and therefore does not directly strengthen this endpoint.

## Exact Witness Subsets And Capacity

### Exact one-way implication

Let $T$ be any subset of cube vertices. If an exact certificate proves that no $H$-head model agrees with $f$ on $T$, then no $H$-head model agrees with $f$ on the full cube. Therefore

$$ H^{\ast}(f)>H. $$

This elementary implication is algorithmically valuable. A lower certificate may involve far fewer than $2^n$ truth-table rows.

The reverse implication is false. Fitting a subset never proves a global upper bound.

### Capacity bound

A slightly enlarged $H$-head family uses

$$ p=1+2H(n+1) $$

real coefficients. After denominators are cleared, membership of one input is one polynomial inequality of degree at most $H+1$. Theorem 2.2 of [Goldberg and Jerrum](https://www.cs.ox.ac.uk/people/paul.goldberg/papers/goldbergjerrum.pdf) gives

$$ \mathrm{VCdim}(\mathcal C_H)\leq2p\log_2\left(8e(H+1)\right). $$

This justifies random witness mining and estimates distance to the $H$-head class. It does not estimate exact $H^{\ast}(f)$ under uniform sampling unless the target error is below $2^{-n}$, which removes the sampling advantage.

For a fixed set of $m\geq p$ inputs with uniformly random labels, Warren's bound gives the explicit fitting probability

$$ \Pr[\text{some }H\text{-head model fits the sample}]\leq2^{-m}\left(\frac{4e(H+1)m}{p}\right)^p. $$

Thus samples of order $p\log(p(H+1))$ are likely to refute small $H$ for random targets. The probability only guides witness discovery. Once an exact solver certifies the sampled subsystem infeasible, the resulting lower bound is deterministic.

The correct use is:

1. sample or greedily choose a small witness set;

2. fit or refute the candidate head count on that set;

3. if refuted, exactify the subset certificate and raise the lower endpoint;

4. if fitted, search the full cube for a counterexample;

5. accept an upper bound only after exact verification on every vertex.

## Robust Positive-Basis Cells

The circuit atlas can be replaced on well-conditioned regions by a simpler convex-hull certificate.

Define the signed hull condition margin

$$ \gamma&#95;{\mathrm{hull}}(\theta)=\min&#95;{\lVert u\rVert&#95;2=1}\max&#95;x\langle u,r&#95;x(\theta)\rangle. $$

Then $\gamma&#95;{\mathrm{hull}}(\theta)<0$ exactly when a strict readout exists, $\gamma&#95;{\mathrm{hull}}(\theta)=0$ when the origin is on the hull boundary, and $\gamma&#95;{\mathrm{hull}}(\theta)>0$ when the origin is in the hull interior. In the last case it is the radius of the largest centered Euclidean ball in the row hull. This separates robust open cells from the ill-posed discriminant.

Fix $\theta_0$, and let $r_x(\theta)$ be the signed feature rows in $\mathbb R^d$. Suppose a selected support $S$ satisfies

$$ \rho\mathbb B_2^d\subseteq\mathrm{conv}\lbrace r_x(\theta_0):x\in S\rbrace $$

for some $\rho>0$. Suppose a parameter cell $C$ has the certified row-motion bound

$$ \lVert r_x(\theta)-r_x(\theta_0)\rVert_2\leq\delta<\rho $$

for every $x\in S$ and every $\theta\in C$. Then

$$ (\rho-\delta)\mathbb B_2^d\subseteq\mathrm{conv}\lbrace r_x(\theta):x\in S\rbrace $$

throughout $C$. In particular, every $\theta\in C$ has a Gordan multiplier.

**Proof.** Corresponding convex hulls have support functions differing by at most $\delta$ in every unit direction. The center hull has support at least $\rho$ in every such direction, so the moved hull has support at least $\rho-\delta$. Support-function domination is equivalent to containment of the centered ball. $\blacksquare$

There is a simple attention-specific row-motion bound on an interior denominator chart. Gauge each numerator by a multiple of its denominator so that its coefficient of $L_0^{\sigma}=1$ vanishes. This is valid whenever $\theta_{h0}>0$, in particular throughout the strict simplex interior. Use the effective feature basis consisting of

$$ F(x)=\prod_hB_h(x) $$

and the $Hn$ coordinates

$$ L_i^{\sigma_h}(x)P_h(x),\qquad P_h(x)=\prod_{g\neq h}B_g(x). $$

For normalized simplex denominators, $0\leq B_h(x)\leq1$. Put

$$ t_h=\lVert\theta_h-\theta_{0h}\rVert_1,\qquad T=\sum_ht_h. $$

Literal evaluations are zero or one, so

$$ \lvert B_h(x;\theta_h)-B_h(x;\theta_{0h})\rvert\leq t_h. $$

Telescoping products give

$$ \lvert F(\theta)-F(\theta_0)\rvert\leq T,\qquad \lvert P_h(\theta)-P_h(\theta_0)\rvert\leq T-t_h. $$

Therefore every signed row obeys

$$ \lVert r_x(\theta)-r_x(\theta_0)\rVert_2^2\leq T^2+n\sum_{h=1}^H(T-t_h)^2. $$

This bound uses only rational cell radii and avoids symbolic determinants. A boundary face with $\theta_{h0}=0$ requires another nonzero-coefficient chart, a redundant feature representation, or lower-dimensional recursion.

A support of size $d+1$ need not preserve interior containment. A square around the origin is the smallest example. The classical Steinitz theorem gives a subset of at most $2d$ rows whose convex hull still contains the origin in its interior. More quantitatively, [Ivanov and Naszódi](https://arxiv.org/abs/2212.04308) prove that if the original hull contains a unit ball, at most $2d$ vertices retain a ball of radius at least $1/(5d^2)$.

Thus every full-dimensional robust Gordan obstruction has an $O(d)$-row robust support with only polynomial loss of inradius. Since $d=1+Hn$, this is at most

$$ 2+2Hn $$

rows. This is a stronger scaling principle than enumerating all minimal circuits.

An exact leaf can store:

1. a rational center $\theta_0$;

2. at most $2d$ row indices;

3. an exact lower bound on a centered inradius, or a rational polyhedral inner body;

4. exact interval or Bernstein row-motion bounds;

5. the inequality $\delta<\rho$.

The inradius evidence can also be completely polyhedral. Store rational convex combinations proving that every point $\pm re_j$ belongs to the selected row hull. The hull then contains the crosspolytope

$$ \lbrace z:\lVert z\rVert_1\leq r\rbrace, $$

and therefore contains a Euclidean ball of radius $r/\sqrt d$.

For a fixed selected support, the largest such axis-aligned $r$ is one rational LP. Introduce convex weights $\lambda&#95;{j,+}$ and $\lambda&#95;{j,-}$ and maximize $r$ subject to

$$ \sum&#95;{x\in S}\lambda&#95;{j,+,x}r&#95;x(\theta&#95;0)=re&#95;j,\qquad \sum&#95;{x\in S}\lambda&#95;{j,-,x}r&#95;x(\theta&#95;0)=-re&#95;j, $$

with every weight nonnegative and each weight vector summing to one. The robust-cell comparison can avoid square roots by checking

$$ d\delta^2<r^2. $$

Support discovery can maximize this LP value under greedy row exchange or use a numerical Euclidean inradius first. The final certificate trusts only the stored rational convex combinations and the exact row-motion inequality.

Rank-deficient or zero-inradius points remain. They lie on ill-conditioned strata and should be handled by lower-dimensional recursion, polynomial selectors, circuits, or an exact real-arithmetic solver.

## Complexity Of Complete Decision

For one orientation-count branch, the compact primal formulation has approximately

$$ k=2Hn+1 $$

effective real variables, namely $Hn$ denominator variables and $1+Hn$ readout variables. It has

$$ s=2^n+O(Hn) $$

polynomial constraints of degree at most $H+1$.

Existential real-arithmetic algorithms are singly exponential in the variable count. Suppressing coefficient bit complexity, the resulting form is

$$ (s(H+1))^{O(k)}. $$

If the truth-table input length is $N=2^n$, then for fixed $H$ this becomes

$$ N^{O(H\log N)}. $$

Thus complete candidate $H$ decision is quasi-polynomial in truth-table length for fixed $H$ at the level of this general bound. The constants remain too large for this to be a default implementation. Renegar's primary existential-theory analysis is [On the Computational Complexity and Geometry of the First-Order Theory of the Reals](https://doi.org/10.1016/S0747-7171(10)80003-3).

The practical implication is parameterized rather than absolute. Exact real solvers become plausible after restrictions, partition witnesses, coefficient flattenings, or robust cells reduce the residual dimension.

## Conditioned Numerical Complexity

Exact head complexity permits representations with arbitrarily small margins or denominator coefficients. Numerical optimization should therefore expose conditioning instead of hiding it.

For $\kappa\geq n+1$, define a diagnostic conditioned problem by requiring

$$ \theta_{hi}\geq\frac1\kappa,\qquad \lVert w\rVert_1\leq1,\qquad \min_xR(\theta)[x,:]w\geq\frac1\kappa. $$

Let $H^{\ast}_{\kappa}(f)$ be the least feasible head count under these constraints. Then

$$ H^{\ast}_{\kappa}(f)\geq H^{\ast}(f), $$

and increasing $\kappa$ gives a systematic upper-search continuation. Any exact finite-cube representation can be perturbed and normalized to satisfy the conditioned constraints for some finite $\kappa$.

Therefore:

- finding a conditioned representation proves an exact upper bound;

- failure at one $\kappa$ proves nothing about exact $H^{\ast}(f)$;

- the smallest successful $\kappa$ is a useful numerical stability statistic.

## A New Fourier-Sparse Upper Bound

There is a sharper constructive consequence of the exact parity construction. Suppose

$$ R(x)=c&#95;{\varnothing}+\sum&#95;{S\in\mathcal A,\ S\neq\varnothing}c&#95;S\chi&#95;S(x) $$

strictly sign-represents $f$, where

$$ \chi_S(x)=(-1)^{\sum_{i\in S}x_i}. $$

Then

$$ H^{\ast}(f)\leq a_1(R)+\sum_{S\in\mathcal A,\ \lvert S\rvert\geq2}\lvert S\rvert, $$

where $a&#95;1(R)$ is one when the affine portion is nonconstant and zero otherwise.

**Proof idea.** The sum of the constant and singleton characters is affine. Divide this affine score by $1+\varepsilon\sum_ix_i$ to approximate it uniformly with one head, or use no head when it is constant. On its active variables, every remaining $\chi_S$ is parity, and the weighted-sum interpolation construction realizes the real-valued score $c_S\chi_S$ exactly using $\lvert S\rvert$ heads. Extend those atoms to the ambient cube with sufficiently small positive dummy-coordinate weights. Since the support is finite and $R$ has a strict finite-cube margin, all extensions can be chosen so that their total error is smaller than that margin. Summing the components gives a score with the sign of $R$. $\blacksquare$

Thus a Walsh PTF with $m&#95;1$ singleton terms and $m&#95;{\geq2}$ nonsingleton terms of degree at most $d$ gives

$$ H^{\ast}(f)\leq\mathbf{1}[m_1>0]+dm_{\geq2}. $$

This improves the earlier monomial-expansion cost and avoids paying separately for every linear character. The strengthened result is now formalized in [045_fourier_support_upper_bound.md](../../lemmas/02_complexity_measure_upper_bounds/045_fourier_support_upper_bound.md) and should be added to the upper-bound presolve.

There is an exact escalation for the absolute Fourier-tail criterion. Use unnormalized coefficients $c_S$, retain the constant for free, bundle every singleton coefficient into one cost-one item, and give each nonsingleton coefficient value $\lvert c_S\rvert$ and cost $\lvert S\rvert$. Requiring omitted mass below $2^n$ is then a zero-one knapsack cover. Because total compiler cost is at most $n2^n+1$, [Theorem 196](../../lemmas/02_complexity_measure_upper_bounds/196_optimal_fourier_tail_knapsack.md) computes the best such certificate in $O(n4^n)$ integer operations, polynomial in the truth-table length. Greedy mass-per-head selection remains the fast default.

## Cost-Aware Sparse Construction

The constructive endpoint should search for a score, not merely truncate the unique Fourier expansion. Sign representations are nonunique. For any proposed feature support, the coefficients can be refit by the exact margin LP

$$ y_xR(x)\geq1\qquad\text{for every }x. $$

If the support LP is feasible, rational coefficients and a full-cube integer sign check turn the support into a certified upper bound. Greedy deletion, iterative reweighted $\ell_1$, and column generation are only support-discovery heuristics. A restricted library need not initially separate the table, so column generation must begin with Phase I artificial variables or soft-margin slacks. Remove the slacks before treating the final support as feasible.

There is a zero-search first pass. Whenever the threshold-degree backend already returns an exact integer sign polynomial, charge its nonzero monomial support with the affine-free compiler. Evaluate that same integer score on the cube, apply an integer fast Walsh-Hadamard transform, and charge the nonzero Walsh support with the Fourier compiler. These are immediate verified upper certificates extracted from work the lower-degree backend has already done.

For a weighted $\ell_1$ restricted master with feature costs $c_j$, the dual pricing constraints have the form

$$ \left\lvert\sum_x\lambda_xy_x\phi_j(x)\right\rvert\leq c_j. $$

Pricing must maximize cost-normalized absolute correlation, or equivalently find the most violated inequality. A free global bias also imposes $\sum_x\lambda_xy_x=0$. Any free affine block imposes the analogous orthogonality constraints for all its columns.

Three feature libraries have fast or structured pricing.

**Walsh characters.** Allow either no affine part or one free affine block, and minimize a weighted $\ell_1$ surrogate over characters of size at least two. The initial cost of a nonsingleton $\chi_S$ is $c_S=\lvert S\rvert$. Every absolute dual correlation can be computed simultaneously by a fast Walsh-Hadamard transform in $O(n2^n)$ time. Price by the ratio of that absolute correlation to $c_S$. Refit the final support and charge the exact Fourier compiler cost from the preceding section.

**Monotone monomials.** For $q_S(x)=\prod_{i\in S}x_i$, all reduced-cost correlations are

$$ g(S)=\sum_{X\supseteq S}\lambda_Xy_X. $$

They are computed by one superset zeta transform in $O(n2^n)$ time. Pricing uses $\lvert g(S)\rvert$, with unit cost for every nonlinear monomial. The exact monomial compiler charges at most one head for the whole affine portion and one head for each selected monomial of degree at least two.

The first prototype should run the Walsh and monotone masters separately because they have clean diagnostics. The stronger follow-up is one mixed restricted master with both dictionaries and one shared affine block. Each pricing round computes both transforms and adds whichever cost-normalized columns are most violated. Mixed representations can be strictly cheaper than the better pure-basis representation, although duplicate spans require aggressive pruning and exact refitting.

**Subcube cylinders.** There are two distinct valid searches. A certificate-cover master uses only cylinders contained in one label class, integer cover variables, and the repository cost

$$ \kappa(P,N)=\min\left\lbrace2^{\lvert P\rvert},2^{\lvert N\rvert}\right\rbrace $$

for a nonvacuous cylinder. A fractional cover is only a lower bound for that integer master and is not an upper certificate. A different signed-threshold master permits real signed cylinder coefficients plus an affine block; for a fixed support, its certificate is the full-cube margin LP. There are $3^n$ cylinders, so [branch-and-price](https://doi.org/10.1287/opre.46.3.316) or mixed-integer pricing is more appropriate than explicit enumeration at larger $n$. A BDD for $f$ can validate and seed implicants, but arbitrary dual-weight pricing needs an ADD, a dedicated dynamic program, or a mixed-integer oracle. [Lawless, Dash, Günlük, and Wei](https://jmlr.org/papers/v24/22-0880.html) provide a close rule-set column-generation analogue.

The sparse PTF literature supplies both theory and practical deletion heuristics. See [O'Donnell and Servedio](https://www.cs.cmu.edu/~odonnell/papers/ptf-extremal.pdf) for extremal PTF density, [Oztop](https://doi.org/10.1162/neco.2006.18.12.3119) for a constructive three-quarters density bound, and [Sezener and Oztop](https://arxiv.org/abs/1504.01167) for low-density support search. [Dantzig and Wolfe](https://doi.org/10.1287/opre.8.1.101) and [LPBoost](https://doi.org/10.1023/A:1012470815092) supply the restricted-master and pricing template. Sezener and Oztop use the bipolar Walsh basis, so their deletion strategy transfers but their density values do not become monomial head bounds. Classical density counts do not equal head cost: a nonsingleton Walsh character costs $\lvert S\rvert$ heads here, while a monotone monomial costs one and all linear terms share one affine head.

After a support is found, compile the same score in several ways and keep the cheapest exact certificate: affine-free monomials, character-by-character parity, affine cylinders, positive statistics, or small overlapping feature blocks. This compiler portfolio can exploit cancellations that any one basis misses.

The bounded prototype is [sparse_ptf.py](../../src/hstar/sparse_ptf.py), with smoke verifier [verify_sparse_ptf_prototype.py](verify_sparse_ptf_prototype.py). It now contains both full-dictionary backward deletion and transform-priced column generation. The restricted master has a free affine block, weighted positive and negative feature columns, and one Phase I artificial raw-score column. Walsh pricing uses one fast Walsh-Hadamard transform, while monotone pricing uses one superset zeta transform. Every proposed support is refit and rounded, and every returned certificate is independently checked with integer arithmetic. Full-basis exact interpolation remains a safe fallback.

| Case | Selected basis | Sparse-compiler bound | Existing comparison |
| --- | --- | ---: | --- |
| Six-bit parity | Walsh | $6$ | exact value $6$ |
| Six-bit parity triple flip | Walsh | $14$ | verified exact-model upper bound $6$ |
| Equality of two three-bit strings | Monotone | $4$ | generic estimator interval $[2,10]$, known exact value $2$ |
| Fixed pseudorandom six-bit table | Monotone | $21$ | universal upper bound $11$ |

The equality case shows genuine endpoint improvement over the generic projection route, while the random case shows why the portfolio must retain universal determinant constructions. The smoke suite also verifies both full bases on all $256$ three-bit truth tables, for $512$ exact certificates total.

The transform-priced pilot gives a first scale test beyond a materialized dictionary. For equality of two six-bit strings, hence $n=12$, it used $80$ generated nonlinear columns and at most $712704$ restricted-master entries, instead of the $16777216$ entries in the full feature matrix. It returned an independently verified $7$-head monotone certificate with support size $19$. This is evidence for memory scalability, not an optimality theorem. On twelve-bit parity the column budget missed the unique expensive parity feature, and on a random six-bit table column generation was weaker than backward deletion. Cost-weighted $\ell_1$ is a support heuristic rather than the discrete head objective, so deletion, transform pricing, and structural seeds should remain a portfolio.

### Direct denominator-group boosting

There is also a model-native continuous dictionary. The group-norm surrogate follows the [group lasso](https://doi.org/10.1111/j.1467-9868.2005.00532.x), while fully corrective sparse atomic optimization gives a related algorithmic viewpoint in [Jaggi](https://proceedings.mlr.press/v28/jaggi13.html). A normalized admissible denominator $B$ contributes the feature group

$$ \Phi_B(x)=\frac{(1,x_1,\ldots,x_n)}{B(x)}. $$

An arbitrary non-gauge coefficient vector on this group costs at most one head. A zero vector costs nothing, and a numerator proportional to $B$ is a constant that can be absorbed into the global bias. For a finite denominator library, use the soft-margin group master

$$ \min_{c,w,\xi}\left(\sum_B\lVert w_B\rVert_2+C\sum_x\xi_x\right)\quad\text{subject to}\quad y_x\left(c+\sum_B\Phi_B(x)^{\top}w_B\right)\geq1-\xi_x,\quad \xi_x\geq0. $$

Once the hard-margin phase is feasible, its dual includes $\lambda\geq0$, the bias constraint $\sum_x\lambda_xy_x=0$, and one group constraint for every denominator. The pricing objective is

$$ \max_{B}\left\lVert\sum_x\lambda_xy_x\frac{(1,x)}{B(x)}\right\rVert_2. $$

Pricing over the two denominator simplices is nonconvex but only $n$-dimensional. To avoid singular boundary behavior, either require every simplex coefficient to be at least a fixed $\varepsilon>0$, use conditioned continuation, or treat faces separately and perturb a successful boundary point back to strict positivity. Add the best rationalized denominator to the restricted master, refit all numerator coefficients, and repeat. Every stored denominator must be strictly oriented and positive. A successful rational library is checked by the existing fixed-denominator verifier and lowers $U(f)$. Failed pricing or failed multistart search proves nothing about $L(f)$.

[Theorem 195](../../lemmas/02_complexity_measure_upper_bounds/195_atomic_margin_sparsification.md) supplies a principled support target after normalizing atoms in score space. If a convex atomic score has scale $\Lambda$ and cube margin $\gamma$, approximate Carathéodory yields an $O(n(\Lambda/\gamma)^2)$-head representation. A finite rational decomposition is already a direct certificate, while failure to find a favorable atomic condition number has no lower-bound meaning.

## Recommended Anytime Portfolio

### Lower endpoint

Run the following layers at the current frontier $H=L(f)$.

1. restrictions, parity subcubes, structural theorems, average sensitivity, and exact threshold degree;

2. partition VC and spectral screens, optimized $\gamma_2^{\ast}$ and $\tau$ certificates, then product average margin;

3. the Boolean slice-rank screen, followed by Grassmann variable projection only below the collapse range and preferably when the incidence codimension remains positive;

4. exact infeasibility on mined witness subsets for every relaxation above;

5. positive secants, unrestricted real second secants, and balanced split-form feasibility;

6. first and middle catalecticants, Jacobian Macaulay ranks, and selected stronger syzygy equations;

7. robust positive-basis cells on the well-conditioned exact denominator locus;

8. low-degree adjustable Gordan policies, positive circuits, and lower-dimensional strata;

9. NLSAT, CAD, or Positivstellensatz certificates on the residual.

Only an exact certificate can raise $L(f)$.

### Upper endpoint

Use the existing constructive invariants before nonlinear fitting:

1. constants, linear thresholds, symmetric sign changes, positive projections, and archived exact families;

2. cost-aware sparse PTF refitting in the monomial and Walsh bases;

3. affine-cylinder branch-and-price, grids, multigrids, and compiler selection;

4. DNF, CNF, decision-tree, restriction, recursion, and hard-subfunction decompositions;

5. direct denominator-group boosting;

6. variable-projected optimization over the $Hn$ exact denominator variables;

7. conditioned-margin continuation, rationalization, and exact full-cube verification.

Only a verified representation can lower $U(f)$.

### Evidence that never changes an endpoint

The following are useful diagnostics but are not exact bounds:

- a small numerical margin;

- a failed local search;

- a nearly singular flattening;

- an incomplete parameter-space cover;

- a feasible sampled fit;

- a PAC or scenario guarantee;

- an SDP or SOS result without rational reconstruction.

## Scaling Regimes

No one backend dominates in every regime.

| Regime | Most promising first methods | Main limitation |
| --- | --- | --- |
| Small $H$, large $n$ | restrictions, optimized matrix norms, screened slice rank, witness subsets | most coefficient relaxations lose orientation |
| Moderate $n$ and $H$ | positive-secant projection, sparse construction, robust positive bases | slice rank often collapses to degree; cell count and conditioning remain |
| Small $n$, exact value | circuit atlas, NLSAT, CAD, exact coefficient equations | exponential constants |
| Structured functions | existing combinatorial invariants and symmetry quotients | structure detection |
| Random or black-box targets | sampling, VC diagnostics, witness mining | exact equality still needs full verification |

## Immediate Experiments

The next implementation sprint should test the hierarchy on a benchmark suite, not only on the six-bit parity perturbation.

1. Benchmark the public Walsh and monomial column-generation backend together with the budgeted exact Fourier-tail backend, greedy Fourier tails, deletion, and exact interpolation.

2. Promote the weighted $\tau$ eigenvector-cut pilot into the library, then add rational nonuniform product weights, hard-core support mining, and the exact admission gate in [weighted_tau_hard_core_scheduler.md](weighted_tau_hard_core_scheduler.md).

3. Implement a degree-one adjustable Gordan-policy LP on mined supports, with Handelman positivity, positive normalization, and an independent coefficient checker.

4. Extend the implemented Theorem 194 sparse discovery and cover-tree stack with automatic split selection, active vertex generation, chart symmetry, and a complete global cover manifest. Project residual cells back to the lower-degree original signed system for exact algebraic handling. The high-head design is in [high_head_hstar_methodology.md](high_head_hstar_methodology.md).

5. Add direct denominator-group boosting and route every rational hit to the fixed-denominator verifier.

6. Run plain and positivity-aware Grassmann projection only on instances that pass the implemented Boolean slice-rank screen. Build the bounded atlas before adding broader coefficient lifts.

7. Add exact subset infeasibility as a reusable certificate type across threshold, slice, positive-secant, and exact-head formulations.

8. At sampled exact-denominator points, maximize the centered hull inradius and compare positive-basis coverage with minimal-circuit and adjustable-policy coverage.

Useful targets should include parity, majority, random functions, juntas, DNF and CNF families, address functions, and parity with sparse flips. The six-bit example is one stress test, not the design target.

## Main Open Questions

1. In the low-head regime that survives Theorem 191, which sign cones are separated by plain or positivity-aware slice rank beyond threshold degree?

2. Which 2025 small-slice-rank syzygy equations give the best cost-to-strength ratio?

3. Can positivity of one slice generator be eliminated into low-degree coefficient inequalities?

4. Can the nonnegative independence-tensor structure yield an LP or small-SDP hierarchy stronger than threshold degree without immediately becoming dense SOS?

5. Can hard witness subsets be found with a deterministic cutting-plane rule and certified with substantially fewer than $2^n$ rows?

6. Which sparse compiler and direct denominator pricing rule best predicts the smallest successful exact head count?

7. Is the weak-separator discriminant small enough that robust positive-basis cells cover most practical denominator space?

The strongest broadly applicable low-head lower lead is optimized product average margin. Above the matrix and slice midpoint ceilings, the strongest current leads are adjustable Gordan policies, signed-secant refutation, and robust positive-basis cells. The strongest upper-search lead is the implemented cost-aware column generation followed by direct denominator-group boosting. The resulting estimator should be a coupled exchange process: dual violations generate new upper features, while uncovered denominator tuples generate new lower scenarios and small Gordan supports. These routes are certificate compatible and should be benchmarked in parallel.
