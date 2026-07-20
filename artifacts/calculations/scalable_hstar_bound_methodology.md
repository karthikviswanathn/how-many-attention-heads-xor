# Scalable Certified Bounds For Head Complexity

## Objective

Given a complete truth table

$$ f:\lbrace0,1\rbrace^n\to\lbrace0,1\rbrace, $$

the computational goal is an anytime interval

$$ L(f)\leq H^{\ast}(f)\leq U(f). $$

Every update to either endpoint must leave an independently checkable certificate. Floating optimization may guide the computation, but a failed search never raises $L(f)$ and an unverified numerical fit never lowers $U(f)$.

The main conclusion of this review is that no single generic solver is likely to scale. The most promising architecture is a hierarchy:

1. inexpensive structural upper and lower bounds;

2. exact threshold degree and optimized partition sign-rank certificates;

3. slice-rank-two Grassmann projection, positive secants, and balanced split forms;

4. homogeneous coefficient lifts with catalecticant, Jacobian, and stronger Chow-secant equations;

5. cost-aware sparse construction, denominator-group boosting, and exact witness subsets;

6. robust positive-basis cells and low-degree adjustable Gordan policies;

7. positive circuits, Bernstein subdivision, and exact real-algebraic solvers only on the ill-conditioned residual.

The detailed analytic derivations and literature map are in [general_hstar_scalable_research_program.md](general_hstar_scalable_research_program.md). The executable scheduling policy, proof graph, certificate schemas, and cost gates are consolidated in [adaptive_general_hstar_estimator.md](adaptive_general_hstar_estimator.md). The main change from the earlier design is that a circuit atlas is now a residual exact layer. Sparse construction is broadly applicable. Matrix and slice layers should run only when their rank screens leave room to improve the endpoint. Model-aware positive cofactors, direct denominator search, and exact residual methods handle the middle-head regime where both generic relaxations lose strength.

For a complete truth table, polynomial time in $V=2^n$ is polynomial in the input length. For a succinct circuit or membership oracle, exact equality is a different problem: sampling can mine witnesses, but it cannot replace a complete symbolic or exhaustive sign check. The methodology below assumes truth-table input unless a structured verifier is supplied.

## Exact Compact Formulation

Let $y_x=2f(x)-1$. For an orientation $\sigma\in\lbrace+,-\rbrace$, define

$$ L_i^+(x)=x_i,\qquad L_i^-(x)=1-x_i,\qquad L_0^{\sigma}(x)=1. $$

Normalize head $h$ by a simplex vector $\theta_h\in\Delta_n$ and put

$$ B&#95;h(x;\theta&#95;h)=\sum&#95;{i=0}^n\theta&#95;{hi}L&#95;i^{\sigma&#95;h}(x). $$

The interior of $\Delta_n$ gives exactly the strictly oriented model denominators up to positive scale. Boundary points are useful compactification limits.

For $a(x)=(1,x_1,\ldots,x_n)$, define the cleared feature row

$$ C&#95;H(x;\theta)=\left(\prod&#95;hB&#95;h(x),\ a(x)\prod&#95;{g\neq1}B&#95;g(x),\ldots,a(x)\prod&#95;{g\neq H}B&#95;g(x)\right). $$

The displayed feature list has $1+H(n+1)$ columns, but each numerator block has one gauge direction proportional to its denominator, which contributes only the global product column. Its effective rank is at most

$$ d=1+Hn. $$

Let

$$ R_{H,f}^{\sigma}(\theta)[x,:]=y_xC_H(x;\theta). $$

After normalizing the readout by $\lVert w\rVert_1\leq1$, define the branch margin

$$ \mu&#95;{H,f}^{\sigma}=\max&#95;{\theta\in(\Delta&#95;n)^H}\max&#95;{\lVert w\rVert&#95;1\leq1}\min&#95;xR&#95;{H,f}^{\sigma}(\theta)[x,:]w. $$

Then

$$ H^{\ast}(f)\leq H\quad\Longleftrightarrow\quad\max&#95;{\sigma}\mu&#95;{H,f}^{\sigma}>0. $$

The closed simplex is exact for this strict sign problem. If a boundary tuple has positive margin, perturb every denominator toward the simplex barycenter. Continuity on the finite cube preserves a positive margin and produces strictly model-faithful denominators.

Heads are exchangeable, so only the $H+1$ orientation counts need to be considered. A symmetry of the target may reduce this further.

## Pointwise Gordan Geometry

For fixed $\theta$, minimax duality gives

$$ \max&#95;{\lVert w\rVert&#95;1\leq1}\min&#95;xR(\theta)[x,:]w=\min&#95;{q\in\Delta&#95;{2^n}}\lVert R(\theta)^{\top}q\rVert&#95;{\infty}. $$

Therefore the fixed denominator tuple has no strict separating readout exactly when

$$ q\geq0,\qquad\mathbf1^{\top}q=1,\qquad R(\theta)^{\top}q=0. $$

Equivalently, the origin lies in the convex hull of the signed feature rows. Carathéodory's theorem implies that a pointwise obstruction can be supported on at most

$$ d+1\leq Hn+2 $$

cube vertices. This is the key finite reduction. It does not say that the same support works for all $\theta$.

Carathéodory does not preserve robust interior containment. A well-conditioned cell may require up to $2d$ selected rows. The Steinitz theorem and its quantitative refinement give the appropriate sparse robust support, as discussed below.

The global lower-bound condition is

$$ H^{\ast}(f)>H\quad\Longleftrightarrow\quad\text{for every orientation branch and every }\theta\in(\Delta_n)^H\text{, such a }q\text{ exists}. $$

This is a fully adjustable robust-feasibility problem. Affine adjustable policies are useful certificate templates, but general adjustable robust optimization is already hard. Ben-Tal, Goryashko, Guslitzer, and Nemirovski develop the relevant policy viewpoint in [Adjustable Robust Solutions of Uncertain Linear Programs](https://www2.isye.gatech.edu/~nemirovs/MP_Elana_2004.pdf).

## Tangential Chow Geometry

After clearing denominators, every $H$-head score has the form

$$ P=c\prod&#95;{h=1}^HB&#95;h+\sum&#95;{h=1}^HA&#95;h\prod&#95;{g\neq h}B&#95;g. $$

This is a tangent vector at the split form $\prod_hB_h$ to the Chow variety of products of affine linear forms. Tangent normal forms of this type are standard in the geometry of tensor and Chow varieties; see [Qi, Comon, and Lim](https://www.stat.uchicago.edu/~lekheng/work/approx.pdf) and the computational Chow-variety work of [Torrance and Vannieuwenhoven](https://arxiv.org/abs/2005.12436).

This viewpoint explains a hierarchy of useful relaxations.

- Dropping positivity and orientation of the factors gives an algebraic tangential-Chow sign invariant between threshold degree and $H^{\ast}$.

- Flattenings of tangent forms give systematic rank bounds that are not consequences of degree alone.

Pure Chow equations are not sufficient by themselves. The polynomial coefficients may vary anywhere inside the open truth-table sign cone, and the attention-specific gap is exactly the positivity and one-sided orientation of the base factors.

The first coefficient engine should use a stronger elementary consequence. For $H\geq2$, isolate one head:

$$ P=(A&#95;1+cB&#95;1)\prod&#95;{h=2}^HB&#95;h+B&#95;1\sum&#95;{h=2}^HA&#95;h\prod&#95;{\substack{g=2\\g\neq h}}^HB&#95;g. $$

Hence every cleared score has real polynomial slice rank at most two:

$$ P=L_1Q_1+L_2Q_2. $$

For a fixed two-plane $U=\mathrm{span}(L_1,L_2)$ of linear forms, the admissible degree $H$ coefficient space has dimension

$$ 2\binom{n+H-1}{H-1}-\binom{n+H-2}{H-2}. $$

The truth-table margin problem is an LP for fixed $U$, while the nonlinear search is over $\mathrm{Gr}(2,n+1)$ of dimension $2(n-1)$. A positivity-aware version requires $U$ to contain one admissible denominator. Its nonlinear dimension is independent of $H$, but a Boolean evaluation rank screen is mandatory.

Let $D_d=\sum_{j=0}^{d}\binom nj$. [Theorem 191](../../lemmas/02_complexity_measure_upper_bounds/191_boolean_cube_slice_relaxation_ceiling.md) proves that the maximum fixed-plane evaluation rank is

$$ \min\left\lbrace D&#95;H,2D&#95;{H-1}-D&#95;{H-2}\right\rbrace. $$

For $H\geq\lceil(n+1)/2\rceil$, this equals $D_H$, and a single plane containing an admissible denominator spans every degree at most $H$ cube polynomial. In this range, both slice relaxations are exactly threshold degree and the atlas should be skipped. Below the middle level, dimension guarantees a proper incidence only when $\binom{n}{H}-\binom{n}{H-1}>2(n-1)$. Outside that favorable regime, a slice search is diagnostic unless it produces an exact infeasibility certificate.

When the screen passes, a complete bounded atlas is available. Choose the largest Plücker coordinate as pivot and write the plane as the row span of $[I_2\ T]$. The resulting chart entries lie in $[-1,1]$, and the $\binom{n+1}{2}$ pivot choices cover the Grassmannian. On a maximal-rank cell, select a full-rank set of evaluation columns. Those feature rows are affine in $T$, so a rational center-hull inradius plus an exact row-motion bound certifies the whole cell. Covering the maximal-rank locus suffices because closedness handles its rank-deficient boundary. This is the proposed exact branch-and-bound backend for the surviving slice instances.

When plain slice rank is too weak, retain the denominator cofactor product before moving to a full exact-head search:

$$ P=LF+BQ,\qquad F=\prod&#95;{h=2}^{H}B&#95;h. $$

Here $B,B&#95;2,\ldots,B&#95;H$ remain admissible denominators, while $L$ and $Q$ are free linear coefficient blocks of degrees one and at most $H-1$. This keeps all denominator factors but still permits variable projection. It is the next model-aware geometric prototype after the screened slice method.

The slice form implies that $V(P)$ contains a real linear space of codimension at most two, and the containment persists after base change to $\mathbb C$. For $n+1\geq5$, $\mathrm{Sing}(V(P))$ has codimension at most four in the ambient projective space, equivalently at most three inside $V(P)$ when $P\neq0$. Jacobian Macaulay ranks give coefficient-only prefilters. [Flavi, Gesmundo, Oneto, and Ventura](https://arxiv.org/abs/2509.12322) give determinantal equations for small strength and a generic-section reduction theorem for cubic slice rank two. Slice rank at most two implies strength at most two, so these conditions are necessary, not sufficient.

A second model-aware outer relaxation uses positive secants. After denominator normalization, test

$$ y_x\left(s\prod_hB_h^{(1)}(1,x)-(1-s)\prod_hB_h^{(0)}(1,x)\right)>0,\qquad 0\leq s\leq1, $$

where paired factors have the same orientation. This compact problem has $2Hn+1$ parameters. Any positive tangent sign pattern has a nearby positive chord with the same strict signs.

The derivation first perturbs every boundary denominator toward its simplex barycenter, chooses a sufficiently small positive secant parameter, and absorbs the two positive endpoint normalization scales into $s$. These steps preserve the strict cube signs and the paired orientations.

For any split $H=k+(H-k)$, the same tangent also has the balanced form

$$ P=G_IF_J+F_IG_J. $$

Freeing the four block forms gives a bilinear relaxation with $2\left(\binom{n+k}{k}+\binom{n+H-k}{H-k}\right)$ variables. A balanced split grows as $O(n^{\lceil H/2\rceil})$. When $k=1$ or $k=H-1$, this is exactly the slice-rank-two relaxation. Internal splits exist only for $H\geq4$ and give additional necessary conditions. Intersect all available splits with the slice and catalecticant constraints.

A tangent point is also a limit of unrestricted secants, so every cleared form lies in the second secant of the Chow variety and has Chow border rank at most two. If $\mathrm{Cat}_k(P)$ is its order $k$ derivative catalecticant, then

$$ \mathrm{rank}\left(\mathrm{Cat}_k(P)\right)\leq2\binom{H}{k}. $$

In particular, the first catalecticant has rank at most $2H$. To use this soundly, introduce an unknown homogeneous degree $H$ coefficient lift, impose the linear truth-table inequalities $y_xP(1,x)\geq1$, and then impose the rank constraints. Do not test the unique Boolean multilinear representative, because reduction modulo $x_i^2-x_i$ need not preserve these formal rank bounds.

For $H=2$, the real second-secant relaxation has an especially concrete form. If $M_P$ is the symmetric matrix of the homogeneous quadratic $P$, then

$$ n&#95;+(M&#95;P)\leq2,\qquad n&#95;-(M&#95;P)\leq2. $$

Indeed, one product of two real linear forms contributes at most one positive and one negative eigenvalue, and a second secant is a sum of two such products. Equivalently, zero columns allowed,

$$ M_P=U\mathrm{Diag}(1,1,-1,-1)U^{\top}. $$

Together with $y_xP(1,x)\geq1$, this gives a quadratic feasibility relaxation in $4(n+1)$ factor variables. It is stronger than rank at most four alone, but it still drops denominator positivity and tangent orientation.

The first-catalecticant condition also suggests variable projection. Put $r=\min\lbrace2H,n+1\rbrace$. Rank at most $r$ means that $P$ depends on at most $r$ linear forms, so write

$$ P(z)=g(U^{\top}z). $$

For fixed $U$, the coefficients of $g$ enter all signed truth-table inequalities linearly. The inner problem is therefore one margin LP, while the nonlinear search is over a Grassmannian of dimension $r(n+1-r)$. This reduces dimension only when $2H<n+1$. Failure of a local search is not a lower certificate. A globally certified infeasibility result is valid, while a feasible point proves only that this orientation-free relaxation is feasible. [Lasserre](https://arxiv.org/abs/2204.01319) gives the adjacent optimization theory for polynomials encoded by a few linear forms.

## A Stronger Partition Sign-Rank Bound

For every coordinate bipartition $I\sqcup J$, let $\mathrm{srank}_{I,J}(f)$ be the sign-rank of the corresponding truth-table sign matrix. The tangent structure gives the new bound

$$ \mathrm{srank}_{I,J}(f)\leq2^{H^{\ast}(f)+1}-2 $$

for every nonconstant $f$. Consequently,

$$ H^{\ast}(f)\geq\left\lceil\log_2\left(\mathrm{srank}_{I,J}(f)+2\right)\right\rceil-1. $$

The proof is in [028_restrictions_and_sign_rank.md](../../lemmas/02_complexity_measure_upper_bounds/028_restrictions_and_sign_rank.md). It expands every affine numerator and denominator as a sum of a function of the left block and a function of the right block. The two extreme subsets contribute one outer product each, and every other subset contributes at most two. For $H=2$, the cap is $6$, recovering the special rank-six theorem used in the strict-separation examples.

The estimator now has a portable spectral version. For an $m\times k$ sign matrix $S$, Forster's theorem gives

$$ \mathrm{srank}(S)\geq\frac{\sqrt{mk}}{\lVert S\rVert_2}. $$

See [Forster 2002](https://doi.org/10.1016/S0022-0000(02)00019-3). The implementation upper-bounds $\lVert S\rVert_2^2$ by an exact Gershgorin absolute row sum of $SS^{\top}$ or $S^{\top}S$. Thus the resulting integer sign-rank and head lower bounds need no floating-point trust. Deterministic submatrices keep the computation bounded for large partitions.

The next scalable backend should optimize the sign realization in the factorization-norm bound. For an $M\times N$ sign matrix, put

$$ \tau(S)=\min\left\lbrace\gamma_2^{\ast}(W):S\circ W\geq\mathbf1\right\rbrace. $$

The variant after Lemma 4.4 of [Linial, Mendelson, Schechtman, and Shraibman](https://www2.mta.ac.il/~adish/Pubs/Papers/complexity_matrices.pdf) gives

$$ \mathrm{srank}(S)\geq\frac{MN}{\tau(S)}. $$

With $C(W)=\begin{bmatrix}0&W/2\\W^{\top}/2&0\end{bmatrix}$, the joint SDP is

$$ \tau(S)=\min_{W,z}\left\lbrace\sum_kz_k:S\circ W\geq\mathbf1,\ z\geq0,\ \mathrm{Diag}(z)-C(W)\succeq0\right\rbrace. $$

Every rational feasible $(W,z)$ with value $U$ certifies $\mathrm{srank}(S)\geq\lceil MN/U\rceil$. It needs no optimality proof. Because $W=S$ is feasible, this always dominates the literal $\gamma_2^{\ast}(S)$ backend.

The stronger product-average-margin method of [Hatami, Hatami, Pires, Tao, and Zhao](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2022.22) searches rational row and column weights. For fixed rational $p,q$, a rational feasible point of the inner dual gives $U\geq\phi&#95;{p,q}(S)\geq m&#95;{\mathrm{avg}}(S)$ and therefore $\mathrm{srank}(S)\geq\lceil1/U\rceil$. Uniform weights give $\phi&#95;{p,q}(S)=\tau(S)/(MN)$, while nonuniform weights can improve it. Use deterministic submatrices to control PSD order. DD and SDD inner cones are provably zero-strength here: their row-sum inequalities force $U\geq1$, which yields only sign-rank one. Nontrivial approximations must retain larger PSD blocks or use a matrix-free numerical solve followed by a full rational PSD check.

For fixed weights, eliminate the slack variables and use the weighted $\tau$ form

$$ \phi&#95;{p,q}(S)=\min&#95;{W,z}\left\lbrace\sum&#95;kz&#95;k:S\circ W\geq pq^{\top},\ \mathrm{Diag}(z)-C(W)\succeq0\right\rbrace. $$

Thus one inner solver handles both matrix layers. Alternate convex optimization of $p$ and $q$ from uniform, sparse, and random starts. Every rational iterate is independently safe, and zero weights select hard submatrices automatically.

For candidate discovery, treat positive semidefiniteness as the semi-infinite family $v^{\top}Qv\geq0$. Solve an LP with the accumulated eigenvector cuts, diagonalize the candidate $Q$, add its most violated eigenvectors, and repeat. This uses the existing SciPy and HiGHS stack. It follows the semi-infinite SDP method of [Krishnan and Mitchell](https://optimization-online.org/2001/08/365/).

Exactify a numerical candidate by rationally approximating $W,z&#95;0$ and a Gram factor $L$. Put $E=\mathrm{Diag}(z&#95;0)-C(W)-LL^{\top}$ and add

$$ \delta&#95;i=\max\left\lbrace0,\sum&#95;{j\neq i}\lvert E&#95;{ij}\rvert-E&#95;{ii}\right\rbrace $$

to the corresponding diagonal variable. The residual becomes symmetric diagonally dominant with nonnegative diagonal, so the repaired matrix is exactly positive semidefinite. This uses diagonal dominance only for a small residual, not for the full dual matrix.

Factor-width cones of width $k$ cannot certify sign-rank above $k-1$. Indeed, every such decomposition forces $\mathrm{tr}(Q)\geq\sum&#95;{ij}\lvert W&#95;{ij}\rvert/(k-1)$. Hence proving $H^{\ast}(f)\geq h$ through this route requires $k\geq2^h$. Fixed small blocks are useful only for small target bounds.

A primal feasible Gram matrix has the wrong direction for all these lower certificates. Margin complexity and ordinary discrepancy require explicit score and denominator margins, so they apply to conditioned head complexity rather than ordinary $H^{\ast}$. Low sign-rank can coexist with exponentially small discrepancy, as shown by [Hatami, Hosseini, and Lovett](https://theoryofcomputing.org/articles/v018a019/). Exact sign-rank should not be the default backend: deciding whether sign-rank is at most three is already hard, as shown by [Bhangale and Kopparty](https://arxiv.org/abs/1503.04486).

There is a mandatory side-size screen at candidate count $H$. A partition certificate must reach sign-rank $2^{H+1}-1$ to rule out $H$ heads, while matrix size caps sign-rank by $2^{\min(\lvert I\rvert,\lvert J\rvert)}$. Thus no partition can improve the bound unless

$$ \min(\lvert I\rvert,\lvert J\rvert)\geq H+1,\qquad n\geq2H+2. $$

Stop numerical optimization as soon as exact repair gives $U<MN/(2^{H+1}-2)$ for $\tau$, or $U<1/(2^{H+1}-2)$ for weighted $\tau$.

## Cheap Sensitivity Screen

Let $E(f)$ count bichromatic undirected cube edges. Since $\mathrm{AS}(f)=E(f)/2^{n-1}$ and every degree $H$ PTF satisfies the explicit [Diakonikolas, Raghavendra, Servedio, and Tan](https://arxiv.org/abs/0909.5011) bound $\mathrm{AS}(f)\leq2n^{1-1/2^H}$, the exact integer test

$$ E(f)^{2^H}>2^{n2^H}n^{2^H-1} $$

proves $H^{\ast}(f)>H$ for $H\geq2$. The sharper one-head test is $E(f)^2>n2^{2n-2}$. This costs $O(n2^n)$ and can be repeated on restrictions. It is weak in small pilots, so keep it as presolve rather than a core backend.

## Robust Positive-Basis Cells

Let $r_x(\theta)$ be the effective signed feature rows in $\mathbb R^d$. Suppose that at a rational center $\theta_0$, selected rows contain a centered Euclidean ball of radius $\rho$ in their convex hull. If every selected row moves by at most $\delta<\rho$ throughout a parameter cell, then the moved hull contains a centered ball of radius $\rho-\delta$. Hence every point of the cell has a Gordan multiplier, without writing that multiplier as a function of $\theta$.

The classical Steinitz theorem retains interior containment with at most $2d$ selected rows. The quantitative theorem of [Ivanov and Naszódi](https://arxiv.org/abs/2212.04308) retains at least a $1/(5d^2)$ fraction of the inradius. Since $d=1+Hn$, a robust obstruction always has an $O(Hn)$-row support.

On an interior denominator chart, gauge each numerator along its denominator and use the effective features $\prod_hB_h$ and $L_i^{\sigma_h}\prod_{g\neq h}B_g$. For normalized simplex denominators, exact row-motion bounds follow from telescoping products. If

$$ t_h=\lVert\theta_h-\theta_{0h}\rVert_1,\qquad T=\sum_ht_h, $$

then

$$ \lVert r_x(\theta)-r_x(\theta_0)\rVert_2^2\leq T^2+n\sum_{h=1}^H(T-t_h)^2. $$

This gives determinant-free exact leaves on the well-conditioned open locus. Boundary faces require another nonzero-coefficient chart or lower-dimensional recursion. Positive circuits remain necessary on the zero-inradius discriminant.

A particularly compact exact leaf uses a rational positive basis. If selected center rows $a_i$ admit rational weights $\lambda_i\geq t>0$ with $\sum_i\lambda_i=1$ and $\sum_i\lambda_ia_i=0$, let $B$ be any nonsingular $d\times d$ row submatrix. The center inradius obeys

$$ \rho\geq\frac{t\lvert\det B\rvert}{\sqrt{s}\lVert B\rVert&#95;F^{d-1}}, $$

where $s$ is the number of selected rows. A row-motion bound $\delta$ therefore certifies the whole cell through the exact inequality

$$ \delta^2s\lVert B\rVert&#95;F^{2d-2}<t^2(\det B)^2. $$

The surviving ball itself proves full row rank throughout the cell. When a global rank cap is known, this removes the need for a separate interval pivot certificate.

## Why Fixed Multipliers And Face Enumeration Stall

The signed feature matrix is multi-affine in the denominator blocks. It is tempting to assign one multiplier $q$ to every vertex of a parameter cell and conclude by interpolation. This is a valid sufficient certificate: if

$$ R(v)^{\top}q=0 $$

at every product vertex $v$ of the cell, multi-affinity gives the identity throughout that cell.

For the six-bit cleared $V_5$ route, however, this cannot certify a full-dimensional cell. If one fixed $q$ annihilates the matrix on an open cell, polynomial identity forces it to annihilate the matrix for every denominator tuple. The exact common-kernel calculation in [n6_parity_triple_full64_cleared_v5_route.md](n6_parity_triple_full64_cleared_v5_route.md) proves that this global kernel contains no nonzero nonnegative vector.

Subdivision does not repair that obstruction. A fixed multiplier can still be useful on boundary faces, but every full-dimensional certificate must allow $q$ to vary with $\theta$.

Classical multiparametric LP suggests an active-set atlas. Borrelli, Bemporad, and Morari describe critical-region construction for standard multiparametric LP in [Geometric Algorithm for Multiparametric Linear Programming](https://doi.org/10.1023/B:JOTA.0000004869.66331.5c). Here the constraint matrix itself depends polynomially on $\theta$, so critical regions are semialgebraic rather than polyhedral. Murty's [parametric LP lower bound](https://deepblue.lib.umich.edu/items/563d7c96-761f-4d6d-84c2-1b4a36996500) also warns that the number of bases can be exponential even in simpler one-parameter families.

## The Circuit Atlas

Let $M(\theta)$ denote either the ordinary signed tangent matrix or an augmented matrix such as $[G,p]$. Suppose it has generic column rank $d$, and choose an ordered support

$$ S=\lbrace x_0,\ldots,x_d\rbrace. $$

Define cofactor coordinates

$$ q_j^S(\theta)=(-1)^j\det M_{S\setminus\lbrace x_j\rbrace}(\theta). $$

The cofactor identity gives

$$ M(\theta)^{\top}q^S(\theta)=0 $$

identically. Wherever the cofactors have one weak sign and are not all zero, normalizing $q^S$ gives a valid nonnegative Gordan multiplier. The validity region of one support is therefore a semialgebraic determinant-sign region.

This suggests a counterexample-guided algorithm.

1. Sample one denominator tuple in an unresolved cell.

2. Solve the pointwise Gordan LP and extract a minimal positive support.

3. Canonicalize the support under target and head symmetries.

4. Construct its exact cofactor arithmetic circuits.

5. Certify the common-sign region using Bernstein bounds, exact interval arithmetic, or a small real-arithmetic solver.

6. Mark the certified region, then search the uncovered remainder.

7. If only determinant-zero strata remain, use the closedness principle below. Otherwise reduce rank and recurse with a smaller circuit.

Todd's [oriented-matroid programming framework](https://doi.org/10.1016/0095-8956(85)90042-5) supplies the right combinatorial language: positive circuits are the finite alternatives to strict separation, and basis changes describe movement between local formulas.

The algorithm terminates with one of three honest outcomes:

- a finite exact circuit cover, which raises the lower endpoint;

- an uncovered tuple with a strict rational readout, which lowers the upper endpoint;

- a residual region, which leaves the certified interval unchanged.

### Closedness removes generic boundary work

Let

$$ K(\theta)=\lbrace q\in\Delta_{2^n}:M(\theta)^{\top}q=0\rbrace. $$

The set of parameters for which $K(\theta)$ is nonempty is closed. Indeed, if $\theta_j\to\theta$ and $q_j\in K(\theta_j)$, compactness of the multiplier simplex gives a convergent subsequence $q_{j_k}\to q$. Continuity of $M$ gives $q\in K(\theta)$.

Suppose one exact rational parameter has rank $r$, and $r$ is the maximum rank of $M$ on the branch. The rank $r$ locus is Zariski open and dense. If an atlas proves $K(\theta)\neq\varnothing$ on that entire locus, closedness extends the result automatically to every rank-deficient point and every boundary point in its closure.

This is stronger than face-by-face induction. Determinant-zero strata need separate treatment only when the atlas has not covered a dense maximal-rank locus or when the parameter domain has an additional component not reached by that locus.

## Bernstein And Polynomial Multiplier Certificates

Bernstein coefficients bound polynomial ranges on boxes and simplices, and subdivision tightens those bounds. Primary references include [Garloff](https://doi.org/10.1007/3-540-16437-5_5), [Zettler and Garloff](https://doi.org/10.1109/9.661615), and the LP relaxations of [Ben Sassi and Sankaranarayanan](https://arxiv.org/abs/1509.01156). Muñoz and Narkawicz give a formally verified treatment in [Formalization of Bernstein Polynomials and Applications to Global Optimization](https://doi.org/10.1007/s10817-012-9256-3).

There are two useful leaf types.

**Circuit leaf.** Certify that all nonzero cofactors of one support have a common sign throughout the cell.

**Polynomial-selector leaf.** Search for

$$ q&#95;x(\theta)=\sum&#95;{\alpha}c&#95;{x,\alpha}\mathcal B&#95;{\alpha}(\theta) $$

with nonnegative Bernstein coefficients, coefficientwise normalization, and the identity

$$ R(\theta)^{\top}q(\theta)\equiv0. $$

For a fixed basis degree, all unknown coefficient conditions are linear. This is an exact rational LP hierarchy. A selector identity holds globally as a polynomial identity, while its coefficient positivity need only hold on the chosen cell.

The constant-selector level should be attempted on boundary faces and on generic functions that have a global common kernel. It is known to fail on every full-dimensional cell of the six-bit cleared $V_5$ route.

## Zero-Margin Obstruction

Generic global optimization is useful for search but awkward for proving a lower bound. Because $w=0$ is always allowed,

$$ \mu_{H,f}^{\sigma}\geq0. $$

When the branch is impossible, its optimum is exactly zero. An interval, McCormick, Bernstein-range, or SOS upper bound may converge to zero forever without ever proving equality.

McCormick relaxations remain useful for selecting cells and excluding robustly positive regions; see [McCormick 1976](https://doi.org/10.1007/BF01580665). Lasserre's [moment and SOS hierarchy](https://doi.org/10.1137/S1052623400366802) supplies convergent polynomial-optimization bounds, and sparse SOS can exploit some block structure; see [Waki, Kim, Kojima, and Muramatsu](https://doi.org/10.1137/050623802). Numerical SOS becomes a proof only after rational reconstruction and exact identity checking.

For this reason, optimization relaxations should guide the circuit atlas rather than replace it.

## Complete Fallback

The direct feasibility branch is an existential real-arithmetic formula with roughly $2Hn+1$ effective real variables, $2^n$ sign inequalities, and polynomial degree at most $H$. Renegar's algorithms are singly exponential in the number of variables for the existential theory; see [Renegar 1992](https://doi.org/10.1016/S0747-7171(10)80003-3). This is complete in principle but becomes expensive quickly.

The best practical first backend is [NLSAT](https://www.microsoft.com/en-us/research/publication/solving-non-linear-arithmetic/), using the existential primal formulation. CAD is the final exact fallback. These tools should receive small residual cells with fixed determinant signs, not the unreduced global problem whenever avoidable.

## Upper-Bound Engine

The upper endpoint should combine theorem-backed constructions with variable projection.

1. Test constants, linear thresholds, symmetric sign changes, positive weighted projections, decision trees, DNF and CNF constructions, and archived exact families.

2. First score any exact threshold-polynomial certificate in both the monomial and Walsh compilers. Then search sparse monomial and Walsh PTF supports. Start the restricted master with Phase I or soft-margin slacks. Use fast Walsh-Hadamard and superset zeta transforms to price cost-normalized absolute dual correlations, then refit every proposed support by the full-cube hard-margin LP. Run pure bases first, followed by a mixed dictionary with one shared affine block.

3. Search pure certificate covers with an integer branch-and-price master, or search signed affine-cylinder thresholds with a real margin master. Fractional covers are not upper certificates. Use BDDs to seed and validate implicants; exact arbitrary-weight pricing needs an ADD, dynamic program, or mixed-integer oracle.

4. Run direct denominator-group boosting with a free global bias, group-norm soft-margin master, and conditioned or face-aware denominator pricing. Each selected admissible denominator supplies the whole feature group $(1,x)/B(x)$ and costs at most one head.

5. For fixed denominators, maximize the signed margin by LP over the readout coefficients. Optimize only the $Hn$ denominator parameters, using multiple orientation counts, face-biased starts, continuation from $H-1$, and warm-started inner LPs.

6. Rationalize a numerical hit to strictly oriented integer denominators. Re-solve and rationalize the readout, then verify every denominator value and every signed cleared score with integer arithmetic.

Only exact compilation, rationalization where required by the stored certificate, and a full-cube exact sign check can change $U(f)$. This variable-projection principle goes back to [Golub and Pereyra](https://doi.org/10.1137/0710036), although the inner problem here is an LP rather than least squares.

## Frontier Scheduler

Maintain one lower frontier $h=L(f)$ and one upper frontier $k=U(f)-1$.

At the lower frontier:

1. apply restrictions, threshold degree, and cheap exact screens;

2. enable the partition layer only if $n\geq2h+2$;

3. for $h\geq2$, enable plain slice only if $h<\lceil(n+1)/2\rceil$, and give it high priority only when $\binom{n}{h}-\binom{n}{h-1}>2(n-1)$;

4. otherwise move directly to positive cofactors, balanced splits, witness subsets, and the exact parameter-space residual;

5. raise $L(f)$ only when one backend returns a verified refutation of $h$ heads.

At the upper frontier, first search at $k$ because a near-current construction is usually easiest to find. After every verified hit, replace $U(f)$ by the new head count and continue downward. Sparse PTF and structural compilers run before nonlinear denominator fitting. A timeout, failed pricing step, or numerical near-hit returns `unknown` and leaves the interval unchanged.

This scheduler is target-adaptive. It avoids spending most of the budget on a relaxation whose own dimension or rank ceiling makes the desired endpoint impossible.

## Coupled Exchange Architecture

The upper and lower searches can share one exchange loop instead of behaving as unrelated solvers.

The upper restricted master keeps a small library of PTF features or admissible denominator groups. Its dual multipliers price a new feature by cost-normalized correlation, or a new denominator by group-norm violation. A successful candidate is refit on every truth-table row, exactified, and verified. A failed pricing search is only a heuristic miss.

The lower master keeps denominator cells, sampled tuples, and small Gordan supports. At one tuple, a hull LP either extracts a support of at most $Hn+2$ rows or returns a strict readout. The support seeds a robust positive-basis leaf, a circuit, or an adjustable polynomial policy. A separation search then looks for a denominator tuple not covered by the current leaves. A rational uncovered tuple with a strict readout is also a valuable starting point for the upper exact-head search.

Truth-table rows can be generated on demand inside both masters. Solve on an active row set, scan the full table for the most violated row, and repeat. This reduces working memory but does not weaken the certificate because the final verifier still checks all $2^n$ rows.

This produces four coupled oracles:

1. a truth-table row oracle;

2. an upper feature or denominator pricing oracle;

3. a pointwise Gordan-support oracle;

4. an uncovered-parameter oracle.

[Dantzig and Wolfe](https://doi.org/10.1287/opre.8.1.101) give the restricted-master foundation. [Zeng](https://optimization-online.org/2011/06/3065/) develops coupled column-and-constraint generation for adjustable robust optimization. [Wang and Guo](https://arxiv.org/abs/1306.1875) combine exchange methods with exact polynomial subproblems for compact semi-infinite systems. The present quantifiers and zero-margin boundary are different, so those papers motivate the architecture but do not supply a finite-convergence theorem here.

Every iteration is still useful without global convergence. Verified upper constructions lower $U(f)$ immediately. Verified lower leaves accumulate monotonically. If the budget expires, the estimator returns its current certified interval and the unresolved parameter regions.

## High-Head Route

The matrix and slice screens have midpoint ceilings, but the full factor geometry does not. Let $D_H=\sum&#95;{j=0}^{H}\binom{n}{j}$. The tangent and second-secant closures remain proper whenever

$$ D&#95;H-1>2Hn+1. $$

Near $H=n/2$, the left side is exponential in $n$ and the right side is quadratic. When the cheap screens are vacuous but this dimension audit passes, route directly to three model-aware layers:

1. signed positive-secant feasibility, with the joint endpoint and mixture diagonal replaced by the closed compact charts of [Theorem 194](../../lemmas/02_complexity_measure_upper_bounds/194_signed_secant_diagonal_blowup.md), and the pair-gap formulation of [Theorem 193](../../lemmas/02_complexity_measure_upper_bounds/193_positive_secant_diagonal_blowup.md) retained for likelihood-ratio diagnostics;

2. degree-one or degree-two adjustable Gordan policies on mined supports;

3. robust positive-basis cells, followed by exact semialgebraic refutation only on the zero-inradius residual.

The derivations, exact pairwise inequalities, policy coefficient counts, and ranked prototypes are in [high_head_hstar_methodology.md](high_head_hstar_methodology.md). [Theorem 192](../../lemmas/02_complexity_measure_upper_bounds/192_multiway_sign_tensor_rank.md) also shows that adding coordinate blocks cannot repair the midpoint by CP-rank size alone.

## Scalable Portfolio

Let $V=2^n$, let $D_t=\sum_{j=0}^t\binom nj$, and let $d\leq1+Hn$ be the effective tangent dimension.

| Stage | Main computational object | Typical role |
|---|---:|---|
| Structural recognizers | $O(nV)$ truth-table scans | Immediate exact families and restrictions |
| Sensitivity presolve | $O(nV)$ exact edge count | Cheap degree lower screen |
| Threshold degree | $V\times D_t$ primal and Gordan LPs | General certified lower bound |
| Partition spectral bound | small exact Gram matrices | Cheap lower bound beyond degree |
| Partition $\tau$ | eigenvector-cut LP plus rational PSD repair | Optimized sign-realization lower bound |
| Product average margin | weighted eigenvector-cut LP | Strongest current matrix lower layer |
| Screened slice-rank Grassmann search | $2(n-1)$ nonlinear variables plus one LP | Low-head geometric layer; skip at or above the Boolean middle level |
| Signed secant and balanced split | $O(Hn)$ or $O(n^{\lceil H/2\rceil})$ factor variables | Model-aware outer feasibility screens |
| Coefficient flattening | $\binom{n+H}{H}$ coefficient variables | Orientation-free algebraic lower bound |
| Witness subset | selected truth-table rows | Small exact lower certificate |
| Sparse support generation | Walsh or zeta pricing in $O(nV)$ | Constructive upper search |
| Optimal Fourier tail | exact knapsack in $O(nV^2)$ | Certified escalation beyond greedy truncation |
| Denominator-group boosting | $n$-dimensional pricing per new group | Model-native constructive upper search |
| Fixed denominator | $V\times d$ LP | Upper search and local obstruction discovery |
| Robust positive basis | support at most $2d$ | Determinant-free open-cell certificate |
| Polynomial selector | rational LP in basis coefficients | Flexible exact atlas leaf |
| Circuit atlas | cells in dimension $Hn$ | Ill-conditioned residual locus |
| Dense SOS | moment matrix $\binom{p+r}{r}$ | Small residual cells only |
| CAD or NLSAT | semialgebraic feasibility | Completeness fallback |

The truth table itself costs $V$, so methods polynomial in $V$ are reasonable. Methods exponential in $Hn$ must be reserved for the final unresolved frontier.

## Prototype Checkpoint

Four independent prototypes now validate the first implementation layers.

- Transform-priced sparse PTF generation verifies $512$ full-basis certificates, $256$ direct Fourier-tail certificates, and $256$ exact optimal-tail comparisons over all three-bit truth tables. The exact knapsack improves one fixed six-bit greedy tail bound from $119$ to $117$. Its public budgeted estimator path also gives an eight-head certificate for mask `0xb1e41b4e278d72d8`, improving exhaustive projection cost $15$, with $20$ executed dynamic-program transitions. On equality of two six-bit strings, column generation produced a verified $7$-head certificate from $80$ generated columns and at most $712704$ restricted-master entries, while the full matrix would contain $16777216$ entries.

- The weighted $\tau$ eigenvector-cut pilot returns exact rational Gram-plus-residual certificates for the all-positive matrix, Sylvester matrices of orders four and eight, and an eight-by-eight hard core padded to order sixteen. The hard core retains certified sign-rank at least three under zero-supported product weights.

- The Boolean slice verifier checks the fixed-plane rank formula on $21$ parameter pairs through $n=7$. It also gives an exact Jacobian witness of rank $42$ showing that the freed six-bit cubic slice incidence is dominant.

- The signed-secant verifier checks $1600$ exact random endpoint-to-chart identities, $2400$ factor-recurrence identities, $200$ scalar-elimination equivalences, and boundary strictification. For $n=6$ and $H=3$, the signed formulation has $64$ inequalities instead of $1024$ balanced pair gaps.

The corresponding files are [verify_sparse_ptf_prototype.py](verify_sparse_ptf_prototype.py), [verify_certified_hstar_estimator.py](verify_certified_hstar_estimator.py), [weighted_tau_partition_pilot.py](weighted_tau_partition_pilot.py), [verify_boolean_cube_slice_rank_and_n6_cubic_dominance.py](verify_boolean_cube_slice_rank_and_n6_cubic_dominance.py), and [verify_signed_secant_diagonal_blowup.py](verify_signed_secant_diagonal_blowup.py). Sparse PTF column generation and the budgeted optimal Fourier-tail dynamic program are now optional in the public interval estimator. The weighted $\tau$, slice, and secant layers remain standalone research prototypes.

## Symmetry And Caching

Safe symmetries include coordinate permutations preserving the target, output complement, global input complement, head permutations, and permutations within an orientation class. They should be used to canonicalize:

- truth tables and restriction witnesses;

- denominator tuples and parameter cells;

- Gordan supports and oriented circuits;

- determinant arithmetic circuits;

- verified atlas leaves.

Do not force the unknown parameters themselves to be symmetric unless a separate theorem justifies that restriction. A symmetric target need not have a minimal representation fixed by its symmetry group.

For SOS leaves, representation-theoretic block reduction is available from [Gatermann and Parrilo](https://arxiv.org/abs/math/0211450).

## Six-Bit Stress Test

For the parity triple-flip candidate and four heads, the denominator domain has dimension

$$ Hn=24. $$

The ordinary cleared tangent dimension is at most $25$. An ordinary pointwise Gordan obstruction therefore has support at most $26$. The augmented $[G,p]$ route has $26$ columns and circuits on at most $27$ vertices.

The exact script [verify_n6_parity_triple_full64_augmented_generic_rank.py](verify_n6_parity_triple_full64_augmented_generic_rank.py) checks one strictly interior rational tuple in each of the three orientation-count branches and gives augmented rank $26$. Thus the rank $26$ locus is open dense in every branch. If weak positive circuits cover those three full-rank loci, the closedness argument proves the boundary and rank-deficient cases automatically. The lower bound needs only $q\geq0$ and $q\neq0$; strict positivity of all $64$ coordinates is a stronger convenience, not a requirement of Gordan's alternative.

Carathéodory is a structural reduction, not an enumeration strategy. There are

$$ \binom{64}{27}=846636978475316672 $$

possible 27-row supports before symmetry.

For an ordered $27$-vertex support in the augmented route, each cofactor determinant has denominator-block multidegree

$$ (19,19,19,19), $$

and total degree $76$. For one block, the product column contributes degree one and the eighteen tangent columns belonging to the other three heads contribute degree eighteen. The parity column contributes degree zero.

This degree is too high for a dense four-block Bernstein tensor. A dense coefficient array would have

$$ \binom{25}{6}^4=983726214648100000000 $$

entries per cofactor. Cofactors must remain as factored determinant circuits. The practical first experiment is:

1. sample $10^4$ to $10^5$ denominator tuples across the three orientation-count classes;

2. measure the signed hull condition margin and extract inradius-oriented supports of at most $50$ rows;

3. certify retention cells using the telescoping row-motion bound;

4. compare the resulting open-locus coverage with basic Gordan circuit supports;

5. exactify frequent circuits only near the zero-inradius residual;

6. use polynomial selectors, determinant-sign subdivision, or NLSAT only on the uncovered cells.

This experiment tests whether most of the branch is metrically robust before committing to a large exact circuit run.

There is also a complete direct fallback for this particular branch. Failure of the universal weak-multiplier claim is equivalent to one existential formula with $24$ simplex parameters and a separator vector in $\mathbb R^{26}$:

$$ M(\theta)y\geq\mathbf1. $$

It has $50$ real variables, $64$ main inequalities, degree at most four in $\theta$, and total degree at most five after multiplication by $y$. NLSAT, CAD, or an exact Positivstellensatz proof of unsatisfiability would establish the four-head lower bound. This is complete but much less likely to scale than a circuit atlas.

## Certificate Format

A certified run should record the truth-table convention, exact mask, candidate head count, and the exact verifier version. It should then store one or more backend-specific objects.

A matrix lower certificate should contain:

- the coordinate partition and selected row and column lists;

- rational sign-realization, weight, and dual variables;

- an exact rational PSD witness, such as verified $LDL^{\top}$ pivots or a Gram factor plus a diagonally dominant residual;

- the exact logarithmic sign-rank-to-head inversion from the universal tangent cap.

A slice or coefficient lower certificate should contain:

- the homogeneous coefficient convention and cube evaluation map;

- for a Grassmann-atlas leaf, the maximal Plücker pivot, parameter box, certified rank pivot, selected evaluation columns, rational centered-hull witness, and exact row-motion bound;

- for a coefficient leaf, the Fano equations, Macaulay matrix, selected minors, or exact real-algebraic infeasibility certificate;

- the positivity condition for an admissible slice generator when that refinement is used;

- an independently checked implication from the coefficient condition to the ruled-out head count.

A parameter-space lower certificate should contain:

- every orientation-count branch;

- a rational product-simplex subdivision tree;

- for every leaf, a circuit support, polynomial selector, boundary reduction, or exact solver certificate;

- exact determinant or coefficient identities;

- exact positivity evidence;

- hashes linking repeated supports and subproofs.

An upper certificate should contain the exact selected feature or denominator library, rational coefficients, compilation cost, and a full-cube integer sign check. An independent verifier should reconstruct all relevant matrices and scores. It should not trust stored solver statuses, minima, or floating margins.

## Recommended Implementation Order

The sparse-PTF discovery and exact-verification core is now wired into the public interval estimator behind explicit budget flags. The weighted $\tau$ pilot remains standalone. The slice-rank formula, six-bit cubic dominance warning, and signed-secant compactification also have standalone exact verifiers. The rational signed-secant stack now includes sparse common-margin discovery, exact dual reconstruction, and binary cover-tree verification. It has covered one full two-head scalar chart of the eight-bit separation, but not all charts.

1. Keep the current certified interval estimator and exact integer upper verifier.

2. Keep the integrated cost-aware Walsh and monomial column generation and the verified exact tail knapsack behind public budget flags. Retain greedy Fourier tails, backward deletion, and full interpolation as fallbacks, and benchmark the portfolio on larger structured functions.

3. Promote the weighted $\tau$ eigenvector-cut LP and Gram-plus-residual checker into the library, then add rational product-weight search and hard-core scheduling.

4. Add a degree-one adjustable Gordan-policy LP on mined supports, with Handelman positivity and an exact coefficient checker.

5. Extend Theorem 194's exact prefix-product McCormick stack with automatic split selection, active vertex generation, symmetry reduction, and rational complete covers. Use the lower-degree original signed system for exact residual algebraic solving.

6. Add output-normalized denominator-group boosting using Theorem 195, and route every rational hit to the fixed-denominator verifier.

7. For instances that pass the implemented Boolean slice screen, add the fixed-plane margin LP and bounded maximal-Plücker atlas with rank-pivot and inradius leaves.

8. Add exact infeasible witness subsets as a shared certificate type for threshold, matrix, slice, positive-secant, and exact-head formulations.

9. Add cubic Jacobian Macaulay screens, balanced split forms, inradius-oriented positive-basis cells, polynomial selectors, and circuit leaves.

10. Add NLSAT or CAD calls only for unresolved residual leaves.

This order tests the broadly applicable implemented leads first, then attacks the high-head gap with model-aware certificates. Slice incidence remains a selective low-head route only where Boolean evaluation has not collapsed it to threshold degree.
