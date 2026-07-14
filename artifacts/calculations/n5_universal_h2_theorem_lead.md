# Five-Bit Universal Two-Head Theorem Lead

## Status

This note records the analytic reduction proving that every five-bit quadratic threshold has two heads unless its strict sign cell is fully locked into a complementary-five-cycle interaction orthant. The pair-only K5 argument is complete, including its exceptional cases. A later section gives the full diagonally scaled K6 loop-stress system. The matrix-completion argument proves the full oriented result whenever the five slope coordinates contain a monochromatic triangle. A convex-cone argument then reduces the remaining case to sign cells in which all ten interaction signs are locked by nonnegative Fourier-moment duals.

The exhaustive cocircuit and tangent-tope argument in [the two-scale C5 note](n5_c5_two_scale_schur.md) resolves every fully locked cell. Consequently, for every Boolean function $f:\lbrace0,1\rbrace^5\to\lbrace0,1\rbrace$,

$$ \deg_{\pm}(f)=2 \qquad\Longrightarrow\qquad H^{\ast}(f)=2. $$

The finite rank, harmonicity, exceptional-factor, and expansion checks are reproduced by [`verify_n5_k5_stress_reduction.py`](verify_n5_k5_stress_reduction.py).

## Normalized exact equations

Let

$$ q(x)=q_0+\sum_{i=1}^{5}q_i x_i+\sum_{1\leq i<j\leq5}q_{ij}x_ix_j. $$

Consider denominators

$$ B(x)=s+\sum_{i=1}^{5}x_i, \qquad D(x)=s t_0+\sum_{i=1}^{5}t_i x_i, $$

and numerators

$$ A(x)=s u_0+\sum_{i=1}^{5}u_i x_i, \qquad C(x)=s v_0+\sum_{i=1}^{5}v_i x_i. $$

Set $r_i=u_i t_i+v_i$ for $i=0,\ldots,5$. Reducing $A D+C B$ by $x_i^2=x_i$ gives the following necessary and sufficient equations for exact equality with $q$ on the Boolean cube:

$$ q_0=s^2r_0, $$

$$ q_{ij}=r_i+r_j+(u_i-u_j)(t_j-t_i) \qquad (1\leq i<j\leq5), $$

$$ q_i=s\bigl(r_0+r_i+(u_0-u_i)(t_i-t_0)\bigr)+r_i \qquad (1\leq i\leq5). $$

If $s>0$, a common sufficiently large positive translation of $t_0,\ldots,t_5$ makes both denominators positively oriented and positive. If $s<-5$, a common sufficiently large negative translation makes both denominators negatively oriented and positive after changing the signs of the corresponding numerators and denominators. Thus the admissible normalized range is

$$ s\in(-\infty,-5)\cup(0,\infty). $$

Equivalently, for $z=1/s$ the admissible range is

$$ z\in\left(-\frac{1}{5},0\right)\cup(0,\infty). $$

## The K5 pair stress

Fix distinct $t_1,\ldots,t_5$ and define

$$ \lambda_i=\frac{1}{\prod_{k\neq i}(t_i-t_k)}, \qquad w_{ij}=\lambda_i\lambda_j(t_i-t_j)^2. $$

The weights satisfy

$$ \sum_{j\neq i}w_{ij}=0, \qquad \sum_{j\neq i}w_{ij}(t_j-t_i)=0. $$

The linear map

$$ (r,u)\longmapsto\bigl(r_i+r_j+(u_i-u_j)(t_j-t_i)\bigr)_{i<j} $$

has rank $9$. Its unique compatibility condition is

$$ \sum_{i<j}w_{ij}q_{ij}=0. $$

Let

$$ \Delta(t)=\prod_{i<j}(t_i-t_j) $$

and, for a three-element set $R=\lbrace a<b<c\rbrace$, let

$$ \Delta_R(t)=(t_a-t_b)(t_a-t_c)(t_b-t_c). $$

After multiplying the stress equation by $\Delta(t)$, its left side is the polynomial

$$ F_q(t)=\sum_{i<j}(-1)^{i+j}q_{ij}(t_i-t_j)\Delta_{\lbrace1,\ldots,5\rbrace\setminus\lbrace i,j\rbrace}(t). $$

Each of the ten basis summands is translation-invariant, homogeneous of degree $4$, and harmonic. The three-variable Vandermonde is harmonic, and its variables are disjoint from the remaining difference factor.

### Distinct-root lemma

The polynomial $F_q$ has a real zero with all five coordinates distinct unless it is a nonzero scalar multiple of one individual edge-triangle summand.

Here is the proof reduction. A nonzero homogeneous harmonic polynomial has mean zero on the unit sphere, so it cannot be semidefinite. Suppose all zeros of $F_q$ lay in the collision arrangement $t_i=t_j$. Factor every collision form that divides $F_q$. The residual has constant sign off the arrangement, hence is semidefinite and has even degree.

There are only three degree possibilities.

1. With no collision factors, $F_q$ itself would be semidefinite, which contradicts harmonicity.

2. With two collision factors, one would have $F_q=(a^\top t)(b^\top t)Q(t)$ for a positive semidefinite quadratic form $Q$. Expanding the Laplacian shows that no nonzero polynomial of this form is harmonic. For orthogonal collision normals, the coefficient of $(a^\top t)(b^\top t)$ forces the trace of $Q$ and both corresponding diagonal entries to vanish. For nonorthogonal normals, restriction to their span would give a nonzero two-variable harmonic quartic with a semidefinite quadratic factor, which is impossible.

3. With four collision factors, direct expansion of the Laplacian shows that the only harmonic products are the ten edge multisets consisting of a triangle and its disjoint edge. These are exactly the ten individual basis summands of $F_q$.

The ten summands span a space of dimension $5$, not $10$. The kernel of the map $q\mapsto F_q$ is exactly the additive-edge space

$$ q_{ij}=\rho_i+\rho_j. $$

Indeed, every additive-edge table annihilates every K5 stress, and the incidence map $\rho\mapsto(\rho_i+\rho_j)_{i<j}$ has rank $5$. Consequently, the exceptional coefficient tables are exactly

$$ q_{ij}=\rho_i+\rho_j+\kappa\mathbf{1}_{\lbrace i,j\rbrace=\lbrace a,b\rbrace} $$

for some edge $\lbrace a,b\rbrace$ and some nonzero $\kappa$. This proves the distinct-root lemma with the correct exceptional families.

A common translation makes any distinct real root $t_1,\ldots,t_5$ strictly positive without changing the pair equations.

The exceptional families also satisfy the pair equations, but with a collision. The additive part is represented by $r_i=\rho_i$ and $u_i=0$. For the extra edge $\lbrace a,b\rbrace$, set the other three $t$ coordinates equal to a positive number $T$. Choose positive $t_a,t_b$ with $t_b\neq T$, set

$$ u_a=\frac{\kappa}{t_b-T}, \qquad r_a=u_a(t_a-T), $$

and set the remaining added $u_i,r_i$ to zero. A direct substitution gives value $\kappa$ on edge $\lbrace a,b\rbrace$ and zero on the other nine edges. Thus every five-vertex pair table has a representation with positive $t_i$.

## Full affine compatibility

The K5 stress condition does not handle $q_0,q_1,\ldots,q_5$. Suppose a pair root $t$ and a pair solution $(r,u)$ have been fixed. Define vectors in $\mathbb{R}^5$ by

$$ p_i=u_it_i-r_i=-v_i, \qquad h_i=q_i-r_i. $$

The five affine equations are equivalent to

$$ Y_i=p_i+zh_i-q_0z^2=t_0u_i+u_0t_i-u_0t_0. $$

Let

$$ U=\mathrm{span}\lbrace\mathbf{1},t,u\rbrace. $$

For generic pair data, $U$ has dimension $3$. Choose $\lambda,\mu$ spanning $U^\perp$. The existence of some $z$ for which $p+zh\in U$ is equivalent to

$$ (\lambda^\top p)(\mu^\top h)-(\mu^\top p)(\lambda^\top h)=0. $$

When a denominator in the formula for $z$ is nonzero, the required value is

$$ z=-\frac{\lambda^\top p}{\lambda^\top h}. $$

Write the resulting vector uniquely as

$$ p+zh=c\mathbf{1}+\alpha u+\beta t. $$

Then $t_0=\alpha$ and $u_0=\beta$. The final constant compatibility condition is

$$ c-q_0z^2=-\alpha\beta. $$

Consequently, the full construction requires three scalar equations:

1. the pair stress equation $F_q(t)=0$;

2. the quotient-collinearity equation for $p$ and $h$ modulo $U$;

3. the final scalar equation $c-q_0z^2+\alpha\beta=0$.

Modulo translation and scaling of $t$, the distinct pair-root family has two parameters. Together with $z$, this gives three variables for the three equations. Dimension counting is exact, but it is not an existence proof.

## Full diagonally scaled K6 system

The equal-slope ansatz is not the most general positively oriented denominator pair. Introduce homogeneous coordinates $y_0=1$ and $y_i=x_i$. Let $b_i>0$ and write

$$ B(y)=\sum_{i=0}^{5}b_i y_i, \qquad D(y)=\sum_{i=0}^{5}b_i t_i y_i, $$

$$ A(y)=\sum_{i=0}^{5}b_i u_i y_i, \qquad C(y)=\sum_{i=0}^{5}b_i v_i y_i. $$

Again set $r_i=u_it_i+v_i$. Exact equality on the Boolean cube is equivalent to

$$ q_0=b_0^2r_0, $$

$$ q_{ij}=b_ib_j\bigl(r_i+r_j+(u_i-u_j)(t_j-t_i)\bigr), $$

$$ q_i=b_0b_i\bigl(r_0+r_i+(u_0-u_i)(t_i-t_0)\bigr)+b_i^2r_i. $$

All $b_i$ are positive, and a common sufficiently large positive translation of the $t_i$ makes $D$ positive without changing its span with $B$. Thus this parameterization retains the full positive-orientation denominator family.

## Fixed-denominator loop stress

There is also a direct dual formulation. Normalize

$$ Q_0=\frac{q_0}{b_0^2}, \qquad L_i=\frac{q_i}{b_0b_i}, \qquad M_{ij}=\frac{q_{ij}}{b_ib_j}, \qquad \rho_i=\frac{b_i}{b_0}. $$

For fixed $b,t_0,\ldots,t_5$, a dual vector consists of five star weights $a_i$ and ten internal edge weights $w_{ij}$. It annihilates every numerator choice exactly when

$$ (1+\rho_i)a_i+\sum_{j\neq i}w_{ij}=0, $$

$$ \sum_i a_i(t_i-t_0)=0, $$

$$ -a_i(t_i-t_0)+\sum_{j\neq i}w_{ij}(t_j-t_i)=0. $$

These equations have a compact K6 form. Define a symmetric $6\times6$ matrix $\Omega$ by

$$ \Omega_{0i}=a_i, \qquad \Omega_{ij}=w_{ij}, \qquad \Omega_{ii}=\rho_i a_i, \qquad \Omega_{00}=-\sum_i a_i. $$

Then the three equilibrium families above are exactly

$$ \Omega\mathbf{1}=0, \qquad \Omega t=0, $$

together with the five loop constraints $\Omega_{ii}=\rho_i\Omega_{0i}$. Thus the Boolean problem is an ordinary K6 stress with five prescribed positive loop-to-star ratios.

For every such loop stress, the compatibility equation is

$$ \sum_i a_i(L_i-Q_0)+\sum_{i<j}w_{ij}M_{ij}=0. $$

Generically this dual space has dimension $5$. The factor $\rho_i a_i$ in the first equation is the loop contribution created by the Boolean reduction $x_i^2=x_i$. Omitting it gives the ordinary homogenized K6 stress and loses the affine information. The earlier equal-slope ansatz is the specialization $b_0=s$ and $b_i=1$, so $\rho_i=1/s$.

## Boolean matrix completion form

There is an equivalent symmetric-matrix formulation which separates the ordinary rank obstruction from denominator orientation. Put

$$ z_i=2x_i-1, \qquad y=(y_0,z_1,z_2,z_3,z_4,z_5)^{\top}. $$

Write the quadratic polynomial in the new variables as

$$ p(z)=c+\sum_{i=1}^{5}\ell_i z_i+\sum_{1\leq i<j\leq5}m_{ij}z_iz_j. $$

Let $M_0$ be the symmetric matrix defined by

$$ (M_0)_{00}=c, \qquad (M_0)_{0i}=\frac{\ell_i}{2}, \qquad (M_0)_{ij}=\frac{m_{ij}}{2}, \qquad (M_0)_{ii}=0. $$

For a vector $\lambda\in\mathbb{R}^5$, define the trace-preserving diagonal completion

$$ M(\lambda)=M_0+\mathrm{diag}\left(-\sum_{i=1}^{5}\lambda_i,\lambda_1,\lambda_2,\lambda_3,\lambda_4,\lambda_5\right). $$

Then

$$ y^{\top}M(\lambda)y=p(z)+\sum_{i=1}^{5}\lambda_i(z_i^2-y_0^2). $$

The five displayed Boolean relations form the full kernel of evaluation of homogeneous quadratics on the five-dimensional sign cube. Indeed, the space of homogeneous quadratics in six variables has dimension $21$, the space of Boolean polynomials of degree at most two has dimension $16$, and the five relations are independent.

For column vectors $u,v$, set

$$ \mathrm{sym}(u,v)=\frac{uv^{\top}+vu^{\top}}{2}. $$

The exact one-admissible-factor condition is now the following matrix completion problem. There must exist $\lambda$ and affine coefficient vectors $a,d,c',b$ such that

$$ M(\lambda)=\mathrm{sym}(a,d)+\mathrm{sym}(c',b), $$

where $b$ represents an admissible denominator. In sign coordinates, its precise positive-orientation cone is

$$ b_0>\sum_{i=1}^{5}|b_i|, \qquad b_i>0 \quad (1\leq i\leq5), $$

and the negative-orientation cone has the same first inequality and $b_i<0$ for every $i\geq1$.

This formulation is equivalent to the affine identity $q=AD+CB$ in the Boolean quotient. One direction follows by homogenizing the four affine factors. In the other direction, the difference between the two homogeneous quadratics vanishes on the sign cube, so it is a unique linear combination of the five Boolean relations above.

If the cone condition on one factor is temporarily omitted, the matrix condition is equivalent to finding a completion with

$$ \mathrm{rank}(M(\lambda))\leq4, \qquad n_{+}(M(\lambda))\leq2, \qquad n_{-}(M(\lambda))\leq2. $$

Every sum of two symmetrized products has these inertia bounds. Conversely, a real symmetric matrix with these bounds is a sum of at most two products: pair one positive square with one negative square using $u^2-v^2=(u-v)(u+v)$, and use a square as a product when one sign is unpaired.

## Generic rank-four completion theorem

The unoriented rank condition never obstructs an open quadratic sign cell. More precisely, consider any real symmetric $6\times6$ partial matrix whose off-diagonal entries and total trace $\tau$ are prescribed. Suppose three indices form a triangle of nonzero prescribed entries. Then there is a diagonal completion of rank $4$ and inertia $(2,2)$.

Relabel the triangle vertices as $4,5,6$, and use $1,2,3,4$ as a four-element core. Write a completion in block form as

$$ M=\begin{pmatrix}K&R\\R^{\top}&S\end{pmatrix}, \qquad R=\begin{pmatrix}r&s\end{pmatrix}, \qquad S_{12}=S_{21}=\alpha. $$

Here $\alpha$, $r$, $s$, and the off-diagonal entries of $K$ are prescribed, while all six diagonal entries are free subject to their sum being $\tau$. By the triangle hypothesis,

$$ \alpha r_4s_4\neq0. $$

Whenever $K$ is invertible, set

$$ S_{11}=r^{\top}K^{-1}r, \qquad S_{22}=s^{\top}K^{-1}s. $$

The Schur complement vanishes exactly when

$$ r^{\top}K^{-1}s=\alpha. $$

In that case $M$ is congruent to $\mathrm{diag}(K,0,0)$, so it has the same nonzero inertia as $K$.

It remains to satisfy the off-diagonal Schur equation and the trace equation simultaneously. Let

$$ d^{\ast}=\frac{r_4s_4}{\alpha}, \qquad \delta^{\ast}=\tau-d^{\ast}-\frac{r_4^2+s_4^2}{d^{\ast}}. $$

Choose nonzero numbers $\gamma_1,\gamma_2,\gamma_3$ with sum zero. For a large positive parameter $T$, assign the core diagonal entries

$$ d_1=T\gamma_1, \qquad d_2=T\gamma_2, \qquad d_3=T\gamma_3+\delta, \qquad d_4=d. $$

As $T\to\infty$,

$$ K^{-1}\to\mathrm{diag}\left(0,0,0,\frac{1}{d}\right). $$

Hence the Schur equation and total trace converge respectively to

$$ \frac{r_4s_4}{d}=\alpha, \qquad \delta+d+\frac{r_4^2+s_4^2}{d}=\tau. $$

They are solved by $(d,\delta)=(d^{\ast},\delta^{\ast})$. The limiting Jacobian with respect to $(d,\delta)$ is triangular, with diagonal entries

$$ -\frac{r_4s_4}{(d^{\ast})^2}\neq0, \qquad 1. $$

The implicit function theorem therefore supplies real $d(T)$ and $\delta(T)$ solving both exact equations for every sufficiently large $T$.

If $d^{\ast}>0$, choose the signs of $(\gamma_1,\gamma_2,\gamma_3)$ to be one positive and two negative. If $d^{\ast}<0$, choose two positive and one negative. For large $T$, the core $K$ then has inertia $(2,2)$. The resulting full matrix has rank $4$, inertia $(2,2)$, the prescribed off-diagonal entries, and trace $\tau$.

Applied to $M(\lambda)$, this proves that every strict five-bit quadratic sign cone contains a representative with an unoriented two-product factorization. Indeed, perturb the quadratic coefficients by an arbitrarily small amount so that one off-diagonal triangle is nonzero. Strict signs on the finite cube survive the perturbation, and the theorem gives the required trace-fixed rank-four completion.

Thus the remaining five-bit problem is purely an orientation problem: one must ensure that some two-product factorization contains a vector in one of the admissible cones. This condition is essential. Rank four and inertia $(2,2)$ by themselves do not orient either denominator.

## Dual-isotropic factor criterion

For the rank-four case, the orientation condition has an exact intrinsic form. Let $M$ be a real symmetric matrix of rank $4$ and inertia $(2,2)$. Write $M^{\dagger}$ for its Moore-Penrose inverse, and let $\mathcal{C}$ be either admissible cone displayed above. Then the following conditions are equivalent:

1. $M=\mathrm{sym}(a,d)+\mathrm{sym}(c',b)$ for some $b\in\mathcal{C}$;

2. there is a vector $b\in\mathcal{C}\cap\mathrm{im}(M)$ such that $b^{\top}M^{\dagger}b=0$;

3. there is a vector $u$ such that $u^{\top}Mu=0$ and $Mu\in\mathcal{C}$.

To prove the nontrivial direction, work first on the four-dimensional space $W=\mathrm{im}(M)$, where $M$ is nonsingular. Fix a nonzero $b\in W$ and use an orthonormal basis whose first vector is parallel to $b$. In block form,

$$ M=\begin{pmatrix}\alpha&r^{\top}\\r&S\end{pmatrix}. $$

The determinant identity for a principal hyperplane restriction gives

$$ \det(S)=\det(M)\frac{b^{\top}M^{-1}b}{b^{\top}b}. $$

Thus $b^{\top}M^{-1}b=0$ exactly when the restriction $S$ is singular. Since a hyperplane restriction of a nonsingular form has nullity at most one, and since $M$ has inertia $(2,2)$, this singular restriction has inertia $(1,1,0)$. Choose $c'$ so that $\mathrm{sym}(c',b)$ agrees with the first row and column of $M$. The residual is then the zero extension of $S$, so it has inertia $(1,1)$ and rank $2$. It is therefore one symmetrized product, using $v^2-w^2=(v-w)(v+w)$. This proves condition 2 implies condition 1.

Conversely, suppose $M=\mathrm{sym}(a,d)+\mathrm{sym}(c',b)$ has rank $4$. The four factor vectors span $\mathrm{im}(M)$, so in particular $b\in\mathrm{im}(M)$. On the Euclidean hyperplane $b^{\perp}$, the restriction of $M$ equals the restriction of $\mathrm{sym}(a,d)$ and hence has rank at most $2$. The determinant identity forces $b^{\top}M^{\dagger}b=0$. This proves condition 1 implies condition 2.

Finally, if $b=Mu$, then

$$ b^{\top}M^{\dagger}b=u^{\top}Mu. $$

The identity is unchanged if a kernel vector is added to $u$, so conditions 2 and 3 are equivalent.

Applied to the trace-fixed family, this reduces the full rank-four target to the explicit semialgebraic system

$$ \mathrm{rank}(M(\lambda))=4, \qquad \mathrm{inertia}(M(\lambda))=(2,2), \qquad u^{\top}M(\lambda)u=0, \qquad M(\lambda)u\in\mathcal{C}. $$

For fixed $u$, both $M(\lambda)u$ and $u^{\top}M(\lambda)u$ are affine in $\lambda$. Therefore, after fixing an orthant for the absolute values in $\mathcal{C}$, the isotropy and orientation parts are one linear equation and finitely many strict linear inequalities in the five diagonal-shift variables. The remaining nonlinear condition is precisely the rank-four completion condition.

## Monochromatic-triangle orientation theorem

The generic rank-four construction can be oriented whenever three slope coordinates have pairwise off-diagonal entries of the same sign. More precisely, suppose that the prescribed entries among slope indices contain distinct $k,p,q$ such that

$$ \alpha=M_{pq}, \qquad r_k=M_{kp}, \qquad s_k=M_{kq} $$

are all positive or all negative. Then there is a trace-preserving diagonal completion of rank $4$ and inertia $(2,2)$ for which the dual null cone meets the positive admissible cone.

Use the constant coordinate, two unused slope coordinates, and $k$ as the four-element core. Use $p,q$ as the outside coordinates. In the notation of the generic completion theorem, the limiting pivot diagonal is

$$ d^{\ast}=\frac{r_ks_k}{\alpha}. $$

Let $\sigma=\mathrm{sgn}(d^{\ast})$, which is the common sign of $\alpha,r_k,s_k$. For the three large core diagonals choose

$$ (\gamma_0,\gamma_1,\gamma_2)=(-\sigma,2\sigma,-\sigma). $$

Their sum is zero. Together with the finite pivot of sign $\sigma$, they give inertia $(2,2)$. The implicit-function construction in the generic theorem supplies an exact Schur completion for all sufficiently large $T$.

Write the resulting core as

$$ K(T)=\begin{pmatrix}A(T)&h\\h^{\top}&d(T)\end{pmatrix}, \qquad A(T)=T\Gamma+O(1), \qquad \Gamma=\mathrm{diag}(-\sigma,2\sigma,-\sigma), $$

with $d(T)\to d^{\ast}$. Fix $0<\varepsilon<1/3$ and put

$$ Y=(1,\varepsilon,\varepsilon)^{\top}. $$

The leading inverse-core value is

$$ L=Y^{\top}\Gamma^{-1}Y=-\sigma\left(1+\frac{\varepsilon^2}{2}\right). $$

It has sign opposite to $d^{\ast}$. Hence there is a positive number $\kappa$ satisfying

$$ L+\frac{\kappa^2}{d^{\ast}}=0. $$

For a core vector of the form

$$ y(T)=\left(Y,\frac{\kappa(T)}{\sqrt{T}}\right), $$

the equation $y(T)^{\top}K(T)^{-1}y(T)=0$, after multiplication by $T$, converges to the preceding scalar equation. Its derivative with respect to $\kappa$ is $2\kappa/d^{\ast}\neq0$. The implicit function theorem therefore gives an exact positive solution $\kappa(T)\to\kappa$.

The full Schur completion has the factorization

$$ M(T)=\begin{pmatrix}I\\R^{\top}K(T)^{-1}\end{pmatrix}K(T)\begin{pmatrix}I&K(T)^{-1}R\end{pmatrix}. $$

Define

$$ b(T)=\begin{pmatrix}I\\R^{\top}K(T)^{-1}\end{pmatrix}y(T). $$

The constant component of $b(T)$ tends to $1$, and the two fixed core slope components tend to $\varepsilon$. The pivot component is positive and tends to zero. The two outside components satisfy

$$ \sqrt{T}b_p(T)\to\frac{r_k\kappa}{d^{\ast}}>0, \qquad \sqrt{T}b_q(T)\to\frac{s_k\kappa}{d^{\ast}}>0. $$

Thus, for all sufficiently large $T$, every slope component is positive and

$$ b_0(T)>\sum_{i=1}^{5}b_i(T). $$

Finally, with $u(T)=(K(T)^{-1}y(T),0,0)^{\top}$, one has

$$ M(T)u(T)=b(T), \qquad u(T)^{\top}M(T)u(T)=0. $$

The dual-isotropic criterion gives a two-product factorization containing the admissible factor $b(T)$. Therefore every strict five-bit quadratic sign cell whose slope-edge signs contain a monochromatic triangle has a two-head representative.

This leaves one sign-coloring family. After an arbitrarily small perturbation inside a strict sign cell, assume all ten slope off-diagonal entries are nonzero and color each edge of $K_5$ by its sign. If there is no monochromatic triangle, each vertex has degree at most two in either color: three neighbors of one color would form a triangle of the other color. Since the total degree is four, every vertex has degree exactly two in each color. Hence each color class is a five-cycle. Up to relabeling and global sign reversal, this is the unique triangle-free two-coloring of $K_5$.

At this stage, the five-bit orientation problem is confined to the complementary-five-cycle slope sign pattern.

## Sign-cell locking reduction

The complementary-cycle remainder can be sharpened further. Let $\Phi(z)$ be the vector of all Fourier monomials of degree at most two, let $s(z)$ be a strict quadratic threshold sign pattern, and define its open coefficient cone by

$$ \mathcal{C}_s=\left\lbrace\theta:s(z)\langle\Phi(z),\theta\rangle>0\text{ for every }z\in\lbrace-1,1\rbrace^5\right\rbrace. $$

Suppose $\mathcal{C}_s$ contains a coefficient vector whose ten interaction signs form a fixed complementary pair of five-cycles. Write $\sigma_{ij}\in\lbrace-1,1\rbrace$ for those signs.

**Lemma.** Either $\mathcal{C}_s$ contains a representative whose interaction signs have a monochromatic triangle, or every interaction sign is locked throughout the cone:

$$ \sigma_{ij}\theta_{ij}>0 \qquad\text{for every }\theta\in\mathcal{C}_s\text{ and every }i<j. $$

**Proof.** The cone $\mathcal{C}_s$ is open and convex. If one interaction sign is not locked, the cone contains a point where that signed coordinate is nonpositive. If it is zero, a sufficiently small perturbation in the negative coordinate direction stays inside the open cone. Thus two points of the cone can be joined by a path along which that coordinate changes sign. Perturb the path inside the open cone so that it crosses the ten coordinate hyperplanes $\theta_{ij}=0$ transversely and one at a time. Immediately after the first crossing, exactly one edge of the initial complementary-cycle coloring has changed color.

Flipping one edge of a complementary-five-cycle coloring creates a monochromatic triangle. If a cycle edge is flipped to the chord color, its endpoints have a common chord neighbor. If a chord is flipped to the cycle color, its endpoints have a common cycle neighbor. Hence the coefficient vector immediately after the crossing has a monochromatic triangle. $\blacksquare$

The locking property has an exact finite dual certificate. Put

$$ K_s=\mathrm{cone}\left\lbrace s(z)\Phi(z):z\in\lbrace-1,1\rbrace^5\right\rbrace, $$

and let $e_{ij}$ denote the coefficient basis vector for the monomial $z_i z_j$. Then the sign of edge $ij$ is locked exactly when

$$ \sigma_{ij}e_{ij}\in K_s. $$

Indeed, membership gives nonnegative weights $\lambda_z$ satisfying

$$ \sum_z\lambda_zs(z)\Phi(z)=\sigma_{ij}e_{ij}. $$

Taking the inner product with any $\theta\in\mathcal{C}_s$ proves $\sigma_{ij}\theta_{ij}>0$. Conversely, if $\sigma_{ij}e_{ij}\notin K_s$, separation from the closed polyhedral cone gives a vector $\eta$ such that

$$ \langle\eta,s(z)\Phi(z)\rangle\geq0\text{ for every }z, \qquad \langle\eta,\sigma_{ij}e_{ij}\rangle<0. $$

Adding a sufficiently small positive multiple of any point of $\mathcal{C}_s$ makes all the first inequalities strict while preserving the second. The resulting point lies in $\mathcal{C}_s$ and reverses the edge sign. This proves the equivalence.

Consequently, the monochromatic-triangle theorem resolves every complementary-cycle sign cone except those for which all ten signed edge basis vectors lie in $K_s$. Each remaining cone therefore has ten nonnegative Fourier-moment certificates of exactly the form used for the explicit rigid cell below.

## Endpoint-boundary reduction

For a strict sign polynomial, it is enough to find one factor on the endpoint boundary of the positive-orientation cone. Suppose

$$ q(x)=A(x)D(x)+C(x)B(x), \qquad B(x)=\sum_{i=1}^{5}b_i x_i, \qquad b_i>0. $$

The form $B$ is nonnegative on the cube but vanishes at the origin, so it is not itself a valid denominator. For $\varepsilon>0$, put $B_{\varepsilon}=B+\varepsilon$ and

$$ q_{\varepsilon}=A D+C B_{\varepsilon}=q+\varepsilon C. $$

Since the cube is finite and $q$ has no zero, all sufficiently small positive $\varepsilon$ preserve every sign of $q$. The form $B_{\varepsilon}$ is a valid positive-orientation denominator. A sufficiently large positive shift $D+kB_{\varepsilon}$ is also positive and positively oriented, and

$$ q_{\varepsilon}=A(D+kB_{\varepsilon})+(C-kA)B_{\varepsilon}. $$

Thus an exact endpoint-boundary factorization of any strict quadratic sign representative already proves a two-head upper bound for its sign function.

There is a five-dimensional matrix form of this boundary problem. Write

$$ q(x)=q_0+\sum_{i=1}^{5}q_i x_i+\sum_{1\leq i<j\leq5}q_{ij}x_ix_j. $$

Strictness gives $q_0=q(0)\neq0$. For $t\in\mathbb{R}^5$, define the symmetric matrix $S(t)$ by

$$ S_{ii}(t)=q_i-q_0(2t_i+t_i^2), \qquad S_{ij}(t)=\frac{q_{ij}}{2}-q_0t_it_j \quad (i\neq j). $$

Boolean reduction gives the exact identity

$$ q(x)=q_0(1+t^{\top}x)^2+x^{\top}S(t)x. $$

In the generic rank-three case, an endpoint-boundary factorization exists exactly when there are $t$ and $b\in\mathbb{R}_{>0}^{5}\cap\mathrm{im}(S(t))$ such that

$$ b^{\top}S(t)^{\dagger}b=0, $$

and the inertia of $S(t)$ is $(1,2)$ when $q_0>0$, or $(2,1)$ when $q_0<0$. Equivalently, one may seek $t,u$ satisfying

$$ \mathrm{rank}(S(t))=3, \qquad u^{\top}S(t)u=0, \qquad S(t)u\in\mathbb{R}_{>0}^{5}, $$

together with the stated inertia condition.

To see necessity, first use the shear $A\mapsto A+\kappa B$ and $C\mapsto C-\kappa D$ to make the constant term of $C$ zero. Normalize

$$ A=a_0(1+\alpha^{\top}x), \qquad D=d_0(1+\delta^{\top}x), \qquad a_0d_0=q_0. $$

With $t=(\alpha+\delta)/2$ and $v=(\alpha-\delta)/2$, one has

$$ A D=q_0(1+t^{\top}x)^2-q_0(v^{\top}x)^2. $$

Consequently,

$$ S(t)=\mathrm{sym}(c,b)-q_0vv^{\top}, $$

where $c$ is the slope vector of $C$. If this matrix has rank $3$, its inertia is the one stated above. The three vectors $b,c,v$ span its image, and restriction to $b^{\perp}$ has rank one. The dual-isotropic determinant identity therefore gives $b^{\top}S(t)^{\dagger}b=0$.

Conversely, the same block argument used in the rank-four criterion shows that dual isotropy lets one choose $c$ so that

$$ S(t)-\mathrm{sym}(c,b)=\eta vv^{\top}, $$

where $\eta$ has sign opposite to $q_0$. Set $\kappa=\sqrt{-\eta/q_0}$. Then

$$ q_0(1+t^{\top}x)^2+\eta(v^{\top}x)^2=(1+t^{\top}x+\kappa v^{\top}x)q_0(1+t^{\top}x-\kappa v^{\top}x), $$

which reconstructs the required boundary factorization.

This reduction removes all affine intercept variables. The generic rank-four theorem already handles the rank and inertia requirements. The remaining question at this stage is whether every strict five-bit quadratic sign cone in the complementary-five-cycle family contains coefficients for which this rank-three dual null cone meets the positive orthant. The global completion section below answers it through the exhaustive tangent-tope certificate.

## Canonical complementary-cycle cell

There is a natural strict cell in which the complementary-five-cycle interaction pattern is forced. Index the coordinates cyclically modulo $5$. Let $e(x)$ be the number of cycle edges whose two endpoints belong to the support of $x$, and let $k=\lvert x\rvert$. Define

$$ Q_{\mathrm{cyc}}(x)=1-2k^2+8e(x). $$

Equivalently, its multilinear coefficients are

$$ Q_{\mathrm{cyc}}(x)=1-2\sum_i x_i+4\sum_{\lbrace i,j\rbrace\in C_5}x_ix_j-4\sum_{\lbrace i,j\rbrace\notin C_5}x_ix_j. $$

This polynomial is positive exactly at the empty set and the five cycle edges. It equals $1$ at the empty set, $-1$ at every singleton, $1$ at a cycle edge, and $-7$ at a chord. A three-element subset spans at most two cycle edges, so its value is at most $-1$. The values on supports of size four and five are respectively $-7$ and $-9$.

Every quadratic sign representative of this function has the same complementary-cycle interaction signs. For a cycle edge, fix all other bits to zero. The four labels form the XNOR pattern, so the alternating face sum, which is the corresponding quadratic coefficient, is positive. For a chord, fix its unique common cycle neighbor to one and the other two coordinates to zero. The four labels form the XOR pattern, so the corresponding coefficient is negative. Thus no perturbation within this sign cell can create a monochromatic slope triangle.

Nevertheless, this cell has an explicit positive-endpoint factorization. Put

$$ B(x)=x_1+x_2+x_3+x_4+x_5, $$

and define the three affine forms

$$ A(x)=-1-29x_1-51x_2+57x_3-24x_4-29x_5, $$

$$ D(x)=-1-2x_1+2x_2+2x_3+x_4, $$

$$ C(x)=-34-57x_1+51x_2-24x_3+32x_4+3x_5. $$

The boundary score

$$ Q_{\partial}(x)=A(x)D(x)+C(x)B(x) $$

has the same signs as $Q_{\mathrm{cyc}}$ on all $32$ vertices. Its minimum signed value is $1$, while

$$ \max_{x\in\lbrace0,1\rbrace^5}|C(x)|=115. $$

Take $\varepsilon=1/256$, set $B_{\varepsilon}=B+\varepsilon$, and shift the other factor by

$$ E=D+257B_{\varepsilon}. $$

Both denominator forms are strictly positive and positively oriented. Their coefficient vectors are

$$ B_{\varepsilon}=\left(\frac{1}{256},1,1,1,1,1\right), \qquad E=\left(\frac{1}{256},255,259,259,258,257\right). $$

The exact two-head cleared score is

$$ A E+(C-257A)B_{\varepsilon}=Q_{\partial}+\frac{1}{256}C. $$

Its signs agree with $Q_{\partial}$ because $115/256<1$. The cycle cell is not an LTF, as witnessed by any cycle-edge XNOR face. Therefore this canonical forced-cycle example satisfies

$$ \deg_{\pm}(f_{\mathrm{cyc}})=H^{\ast}(f_{\mathrm{cyc}})=2. $$

This certificate resolves the most symmetric forced-cycle cell directly.

A second exact cell is rigidly locked into the same complementary-cycle coefficient orthant by ten nonnegative Fourier-moment duals, yet it also has an exact two-head certificate. A cycle-adapted two-scale Schur lemma orients that representative through three large core coordinates and one finite pivot. The lemma, the rational Schur inequalities, the locked-cell duals, and the exact two-head factors are recorded in [the two-scale C5 note](n5_c5_two_scale_schur.md) and checked by [its exact verifier](verify_n5_c5_locked_cell_h2.py).

The two-scale inequalities are sufficient but are not implied by the edge signs alone. Their universal use requires varying the coefficient representative inside each strict sign cell.

## Global completion of the locked case

The [two-scale C5 note](n5_c5_two_scale_schur.md) completes this final family by an exact finite argument. Full locking first implies that the normalized closed sign cone is a bounded polytope. An exhaustive rank $15$ cocircuit enumeration gives $2272$ extreme-ray orbits in the closed complementary-cycle orthant. An exact tangent-tope cover uses $5837$ wrong-edge quadratics and $892$ nonnegative integer Gordan circuits to reduce every fully locked tangent assignment to an archive of $380$ symmetry classes. Finally, the exact fixed-chord verifier gives a rational two-scale Schur certificate for every archived class.

Thus the monochromatic-triangle theorem, sign-cell locking reduction, exhaustive tangent cover, and exact archived certificates together prove the five-bit degree-two theorem stated above.
