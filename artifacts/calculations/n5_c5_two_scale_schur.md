# Five-Bit Cycle-Adapted Two-Scale Schur Construction

## Status

This note gives a rigorous sufficient condition for orienting a rank-four completion in the complementary-five-cycle case. It also gives an exhaustive exact cocircuit and tangent-tope reduction proving that every fully locked complementary-cycle sign cell has a two-head certificate.

The global certificate closes the complementary-five-cycle case. Together with the reductions to this last locked edge-sign pattern, it completes the five-bit degree-two two-head theorem.

**Global theorem.** For every Boolean function $f:\lbrace0,1\rbrace^5\to\lbrace0,1\rbrace$,

$$ \deg_{\pm}(f)=2 \qquad\Longrightarrow\qquad H^{\ast}(f)=2. $$

The analytic matrix-completion and sign-cell reductions are recorded in [the universal two-head reduction](n5_universal_h2_theorem_lead.md). The exhaustive last case is proved below and is stated formally in [the five-bit degree-two lemma](../../lemmas/06_strict_separations/187_five_bit_degree_two_exact.md).

All arithmetic claims about the explicit cell are reproduced by the [C5 locked-cell verifier](verify_n5_c5_locked_cell_h2.py).

## Two-scale Schur criterion

Use core coordinates $0,a,b,k$ and outside slope coordinates $p,q$. Write the two outside columns over the core as $r,s$, put $\alpha=M_{pq}$, and assume

$$ r_k s_k\alpha\neq0, \qquad d^{\ast}=\frac{r_ks_k}{\alpha}, \qquad \sigma=\mathrm{sgn}(d^{\ast}). $$

Choose $g>0$, $0<\delta<1$, and $R,S>0$ satisfying

$$ \delta R^2+(1-\delta)S^2=1, \qquad \delta R+(1-\delta)S<1. $$

On the three large core coordinates $0,a,b$, set

$$ \Gamma=g\sigma\mathop{\mathrm{diag}}(1,-\delta,-(1-\delta)), \qquad Y=(1,\delta R,(1-\delta)S)^{\top}. $$

Then

$$ \mathbf{1}^{\top}\mathop{\mathrm{diag}}(\Gamma)=0, \qquad Y^{\top}\Gamma^{-1}Y=0, \qquad \Gamma^{-1}Y=\frac{\sigma}{g}(1,-R,-S)^{\top}. $$

Let $h$ be the vector of prescribed entries from $0,a,b$ to $k$, and let $r_L,s_L$ be the restrictions of $r,s$ to $0,a,b$. Define

$$ H=h^{\top}\Gamma^{-1}Y, \qquad P=r_L^{\top}\Gamma^{-1}Y, \qquad Q=s_L^{\top}\Gamma^{-1}Y. $$

**Lemma.** If there is a number $c>0$ such that

$$ P+\frac{\alpha}{s_k}(c-H)>0, \qquad Q+\frac{\alpha}{r_k}(c-H)>0, $$

then the prescribed partial matrix has a trace-preserving rank-four completion of inertia $(2,2)$ whose dual null cone meets the positive admissible cone.

**Proof.** Give the first three core diagonals leading terms $T\Gamma$, allow an $O(1)$ correction in one of them, and let the pivot diagonal vary near $d^{\ast}$. Complete the two outside diagonals by the Schur formulas. The off-diagonal Schur equation and the trace equation converge to

$$ \frac{r_ks_k}{d}=\alpha, \qquad \Delta+d+\frac{r_k^2+s_k^2}{d}=\tau. $$

Their limiting Jacobian with respect to $(d,\Delta)$ is nonsingular. The implicit function theorem therefore gives exact solutions for all sufficiently large $T$. The signs of $\Gamma$ together with the sign of $d^{\ast}$ give inertia $(2,2)$.

For the core target vector use

$$ y(T)=\left(y_0(T),\delta R,(1-\delta)S,\frac{c}{T}\right)^{\top}. $$

After multiplication by $T$, the equation $y(T)^{\top}K(T)^{-1}y(T)=0$ converges, as a function of its first coordinate, to

$$ \frac{\sigma}{g}(y_0^2-1)=0. $$

The derivative at $y_0=1$ is nonzero, so there is an exact solution $y_0(T)\to1$. If $b(T)$ is the full image vector obtained from $y(T)$ through the Schur factorization, its two outside coordinates satisfy

$$ \begin{aligned} T b_p(T)&\to P+\frac{\alpha}{s_k}(c-H), \\ T b_q(T)&\to Q+\frac{\alpha}{r_k}(c-H). \end{aligned} $$

The assumed inequalities make all five slope coordinates positive for large $T$. Moreover,

$$ b_0(T)\to1, \qquad \sum_{i=1}^{5}b_i(T)\to\delta R+(1-\delta)S<1. $$

Thus $b(T)$ is admissible. The dual-isotropic criterion gives the required factorization. $\blacksquare$

The two strict inequalities can be checked by intersecting three open intervals in the single variable $c-H$. This makes the criterion useful for exact screening. They are not consequences of the five-cycle edge signs alone.

There is a symmetric negative-orientation version. Replace $Y$ by

$$ Y=(1,-\delta R,-(1-\delta)S)^{\top}, \qquad \Gamma^{-1}Y=\frac{\sigma}{g}(1,R,S)^{\top}, $$

and define $H,P,Q$ using this new inverse-shape vector. If $c>0$ and

$$ P-\frac{\alpha}{s_k}(c+H)<0, \qquad Q-\frac{\alpha}{r_k}(c+H)<0, $$

then the same proof gives a dual-null vector whose five slope coordinates are negative and whose constant coordinate dominates their absolute sum.

After scaling, both versions are linear feasibility problems. Put $t=1/g$. In the positive case write $c-H=tZ$; the three orientation inequalities become

$$ Z+H_0>0, \qquad P_0+\frac{\alpha}{s_k}Z>0, \qquad Q_0+\frac{\alpha}{r_k}Z>0. $$

In the negative case write $c+H=tZ$; they become

$$ Z-H_0>0, \qquad \frac{\alpha}{s_k}Z-P_0>0, \qquad \frac{\alpha}{r_k}Z-Q_0>0. $$

Here $H_0,P_0,Q_0$ are affine in $R,S$, with $0<R<1<S$. For every such pair, the required weight is recovered as

$$ \delta=\frac{S^2-1}{S^2-R^2}. $$

The weighted root-mean-square of $R,S$ is one, while their weighted mean is strictly smaller than one. Thus each fixed choice of pivot and outside indices is decided by a linear program in $R,S,Z$.

## Representative-level screening

The linear criterion is not universal for a fixed coefficient table. In particular, the symmetric representative of the canonical cycle cell fails both orientation versions. The boundary-factor representative of the same function passes. Therefore any universal claim must allow the quadratic representative to move within its strict sign cell.

The deterministic diagnostic [two-scale C5 screen](screen_n5_c5_two_scale.py) checks this distinction. With seed $20260714$, $1000$ random strict complementary-cycle tables, and $24$ alternative-representative objectives per direct failure, it reports

$$ 986\text{ direct successes}, \qquad 14\text{ successes after changing representative}, \qquad 0\text{ unresolved}. $$

The alternative-representative linear programs preserve both the truth table and all ten complementary-cycle coefficient signs. This is evidence that the two-scale criterion may be universal at the sign-cell level. It is not a proof, because only finitely many coefficient tables and finitely many alternative representatives were tested.

The [locked-cell survey](survey_n5_c5_locked_cells.py) performs a different diagnostic. Starting from the rigid cell below, it walks through single-vertex neighbors that remain quadratic and fully locked by all ten dual cone tests. At a cap of $1000$ cells, it finds $373$ classes under the order $40$ symmetry group of the fixed coefficient orthant. The linear-program representative passes directly in $991$ cells. All remaining $9$ cells pass after searching $64$ deterministic alternative-representative objectives, leaving no unresolved cell in the sample. The walk is not exhaustive, and its floating-point linear programs are not an exact universal certificate.

## Fixed-chord extremal reduction

The alternative-representative search can be replaced by one deterministic objective. For a sign table $s$, put

$$ a_z=s(z)\Phi(z), \qquad d_s=\sum_z a_z, $$

and consider the normalized closed sign cell

$$ \mathcal{P}_s=\left\lbrace\theta:\langle a_z,\theta\rangle\geq0\text{ for every }z,\quad \langle d_s,\theta\rangle=1\right\rbrace. $$

This is a compact polytope. Indeed, the map $\theta\mapsto(\langle a_z,\theta\rangle)_z$ is injective because the degree-at-most-two Fourier matrix has full column rank. It maps $\mathcal{P}_s$ into the standard simplex, so its inverse image is bounded and closed. A strict quadratic representative makes $\mathcal{P}_s$ nonempty.

Fix the chord $e=02$, whose prescribed sign is $\sigma_e=-1$, and choose

$$ \theta^{\ast}\in\mathop{\mathrm{argmax}}_{\theta\in\mathcal{P}_s}\sigma_e\theta_e. $$

Let $\theta^{\circ}$ be any normalized strict representative and put

$$ \theta_{\varepsilon}=(1-\varepsilon)\theta^{\ast}+\varepsilon\theta^{\circ} \qquad (0<\varepsilon<1). $$

If the sign cell is fully locked, every edge dual gives $\sigma_{ij}\theta^{\ast}_{ij}\geq0$. Therefore $\theta_{\varepsilon}$ is a strict representative in the prescribed complementary-cycle orthant for every $\varepsilon>0$.

For exact checking, fix a pivot $k$, outside indices $p,q$, ordered large indices $a,b$, and one of the two orientations. All coefficients of $\theta_{\varepsilon}$ may be rational. Set

$$ \alpha=M_{pq}, \qquad r=M_{kp}, \qquad s=M_{kq}, \qquad \sigma=\mathrm{sgn}(\alpha r s). $$

For the positive orientation, define $H,P,Q$ by pairing the three corresponding matrix-entry columns with $\sigma(1,-R,-S)$. The criterion is the exact rational system

$$ 0<R<1<S, \qquad Z+H>0, \qquad P+\frac{\alpha}{s}Z>0, \qquad Q+\frac{\alpha}{r}Z>0. $$

For the negative orientation, pair the columns with $\sigma(1,R,S)$. The exact rational system is

$$ 0<R<1<S, \qquad Z-H>0, \qquad \frac{\alpha}{s}Z-P>0, \qquad \frac{\alpha}{r}Z-Q>0. $$

Thus a rational optimizer ray, a rational interior perturbation, and rational values of $\varepsilon,R,S,Z$ give a completely exact certificate. No limiting or floating-point assertion is needed once these quantities are recorded.

The deterministic fixed-chord diagnostic gives a stronger survey result than the random objective search. On all $1000$ cells in the locked neighbor walk, the chord-maximal optimizer passes directly in $170$ cells. A convex perturbation toward the stored interior representative passes in the remaining $830$, with no unresolved cell. The boundary optimizers reduce to $132$ primitive small-integer coefficient rays and $111$ classes under the order $40$ symmetry group. The same fixed objective was also tested on $1000$ arbitrary complementary-cycle tables; it failed on $23$, and every failed sign table was not fully locked.

The [fixed-chord extremizer verifier](verify_n5_c5_fixed_chord_extremizer.py) upgrades the walked-cell result from floating evidence to exact finite certificates. For every one of the $1000$ walked cells, it reconstructs the optimizer over the rationals, proves its optimality with a rational dual supported on active cube vertices, reconstructs a rational strict interior point, and checks rational values of $\varepsilon,R,S,Z$ in one of the displayed systems. It finds $850$ positive-orientation and $150$ negative-orientation certificates.

Walking directly in the order $40$ quotient exhausts the component of the rigid cell at $379$ classes. Exact extremal certificates cover all $379$. The fixed chord $02$ covers $378$ classes; the exceptional class **0x01021049** is covered by maximizing chord $14$. A gated MILP found a second component with canonical mask **0x3a8ac089**. It is an isolated quotient class and has an exact fixed-chord certificate. The resulting archive contains $380$ quotient classes in two one-flip components.

The global cocircuit tangent cover below proves that every fully locked complementary-cycle cell is symmetry-equivalent to a member of this archive. The [fixed-chord extremizer verifier](verify_n5_c5_fixed_chord_extremizer.py) gives an exact H2 certificate for every archived class. Thus the extremal reduction is universal at the sign-cell level, even though a single fixed chord is not universal.

## Gordan dual of orientation failure

There is a useful exact alternative for each fixed choice of pivot, outside indices, and ordered large indices. It exposes the cancellation needed by a possible cyclic proof.

Fix pivot $k$, outside indices $p,q$, and ordered large indices $a,b$. Write

$$ \alpha=M_{pq}, \qquad r=M_{kp}, \qquad s=M_{kq}, \qquad \rho_k=1, \qquad \rho_p=\frac{\alpha}{s}, \qquad \rho_q=\frac{\alpha}{r}, \qquad \sigma=\mathrm{sgn}(\alpha r s). $$

For $t\in\lbrace k,p,q\rbrace$, put $l_t=M_{0t}$. Let $\eta=1$ denote the positive orientation and $\eta=-1$ denote the negative orientation. With homogeneous variables $u=(u_0,R,S,Z)$, both orientation systems consist of positivity of the following six row pairings:

$$ b_1=(0,1,0,0), \qquad b_2=(1,-1,0,0), \qquad b_3=(-1,0,1,0), $$

and

$$ g_t^{\eta}=(\eta\sigma l_t,-\sigma M_{at},-\sigma M_{bt},\rho_t), \qquad t\in\lbrace k,p,q\rbrace. $$

Indeed, the first three rows say $0<R<u_0<S$. After scaling $u_0=1$, the last three rows are exactly the three positive-orientation inequalities when $\eta=1$, and exactly the three negative-orientation inequalities when $\eta=-1$.

By Gordan's theorem, orientation $\eta$ fails if and only if there are nonnegative numbers $\beta_1,\beta_2,\beta_3,w_k,w_p,w_q$, not all zero, such that

$$ \begin{aligned} w_k+\frac{\alpha}{s}w_p+\frac{\alpha}{r}w_q&=0, \\ \beta_1-\beta_2-\sigma\sum_t w_tM_{at}&=0, \\ \beta_3-\sigma\sum_t w_tM_{bt}&=0, \\ \beta_2-\beta_3+\eta\sigma\sum_t w_tl_t&=0. \end{aligned} $$

Equivalently, if

$$ A(w)=\sigma\sum_t w_tM_{at}, \qquad B(w)=\sigma\sum_t w_tM_{bt}, \qquad C(w)=\sigma\sum_t w_tl_t, $$

then failure is equivalent to a nonzero $w\geq0$ satisfying the balance equation and

$$ B(w)\geq0, \qquad B(w)-\eta C(w)\geq0, \qquad A(w)+B(w)-\eta C(w)\geq0. $$

The affine quantity $C(w)$ changes sign between the two orientations, while the edge quantities $A(w)$ and $B(w)$ do not. Thus a positive-negative pair with matched balance weights cancels its affine column exactly. A proof based only on this alternative would need to choose or combine the balance weights around the five-cycle so that all five affine columns cancel while the remaining strict edge signs contradict an edge-maximal KKT equation. The displayed alternative isolates that step, but does not by itself prove that such a cyclic matching always exists.

## No weak affine ray

Full locking has one useful exact consequence for global enumeration.

**Lemma.** A fully locked complementary-cycle sign cell has no nonzero affine polynomial in its closed sign cone.

**Proof.** Suppose an affine polynomial $g$ satisfies $s(z)g(z)\geq0$ at every cube vertex. For every edge $e$, choose a locking dual

$$ \sigma_e e_e=\sum_z\lambda^e_zs(z)\Phi(z), \qquad \lambda^e_z\geq0. $$

Taking the inner product with the affine coefficient vector of $g$ gives zero on the left and a sum of nonnegative terms on the right. Consequently, every vertex in the positive support of $\lambda^e$ lies in the zero set $Z$ of $g$. Hence every one of the ten edge basis vectors belongs to

$$ V_Z=\mathrm{span}\left\lbrace\Phi(z):z\in Z\right\rbrace. $$

If $g$ is a nonzero constant, then $Z$ is empty, which is already impossible. Otherwise choose a nonzero slope coefficient $g_i$ and an index $j\neq i$. In the Boolean quotient, the quadratic polynomial $g(z)z_j$ vanishes on $Z$. Its coefficient vector is therefore orthogonal to $V_Z$, hence orthogonal to all ten edge basis vectors. But its $ij$ coefficient is $g_i\neq0$, a contradiction. Thus $g=0$. $\blacksquare$

Put $\ell(\theta)=\sum_e\sigma_e\theta_e$. Full locking gives $\ell\geq0$ on the closed sign cone. The lemma shows that equality is possible only at the origin, because equality forces all ten edge coefficients to vanish. Therefore the affine section $\ell=1$ of every fully locked sign cone is a bounded polytope. The next two sections enumerate every extreme ray of these bounded sections and cover every incident tangent tope exactly.

## Global cocircuit inventory

The rank $15$ extreme rays themselves can be enumerated without walking the chamber graph. Let $V$ be the $16$-dimensional space of degree-at-most-two evaluation vectors on the five-cube, and let $\chi_{12345}$ be the parity character. Fourier orthogonality gives the exact self-duality

$$ V^{\perp}=\chi_{12345}V. $$

Consequently, if $q\in V$ spans a rank $15$ evaluation hyperplane, then $\lambda=\chi_{12345}q$ is a signed circuit in $V^{\perp}$. Conversely, parity twisting any such circuit gives a rank $15$ cocircuit ray. The support of the circuit is the nonzero set of $q$, so it has size at most $17$.

The exhaustive [support-seventeen circuit enumerator](enumerate_n5_support17_circuit_orbits.cpp) now has a closed-C5 mode. It visits all $565722720$ fifteen-subsets, reduces them to $158658$ full-cube orbits, retains all $120395$ rank $15$ cases, and deduplicates the full zero-set closures. This gives $4400$ cocircuit orbits under all cube automorphisms. Filtering every exact transformed coefficient vector by the closed complementary-cycle edge orthant gives

$$ 87142\text{ primitive rays}, \qquad 2272\text{ order-}40\text{ ray orbits}. $$

Their zero-set-size distribution in the order $40$ quotient is

$$ 15:1466, \quad 16:428, \quad 17:240, \quad 18:73, \quad 19:22, \quad 20:33, \quad 22:4, \quad 24:6. $$

The [cocircuit inventory verifier](verify_n5_c5_cocircuit_inventory.py) checks every quotient representative exactly. It proves primitivity, the complementary-cycle edge inequalities, rank $15$ of the zero rows, the parity-twisted circuit equation, the order $40$ quotient, and the file digests. It also confirms that the $3948$ rays found in the $380$ archived classes form $747$ of the $2272$ global ray orbits.

## Exact tangent-tope cover

Fix one of the $2272$ quotient rays $q$, and let $Z$ be its zero set. Every sign cell whose closure contains $q$ agrees with $\mathrm{sgn}(q)$ outside $Z$. Its remaining possibilities are therefore indexed by the Boolean cube $\lbrace-1,1\rbrace^Z$.

Two exact clause types discard tangent assignments.

1. A **wrong-edge clause** is a quadratic coefficient vector $h$ such that $s(z)h(z)\geq0$ at every vertex and $\sigma_eh_e<0$ for at least one edge. Such an $h$ lies in the closed sign cone of $s$, so $s$ cannot be fully locked to the complementary-cycle orthant.

2. A **Gordan clause** consists of nonnegative integers $\lambda_z,\mu_e$, not all zero, satisfying

$$ \sum_z\lambda_zs(z)\Phi(z)+\sum_e\mu_e\sigma_e e_e=0. $$

If a strict complementary-cycle representative $\theta$ existed, taking its inner product with this identity would give a sum of strictly positive terms equal to zero. Thus no such representative exists.

For simple rays with $\lvert Z\rvert=15$, zero edges give an additional exact shortcut. If $q_e=0$, any locking dual for edge $e$ must be supported on $Z$. Since $\Phi(Z)$ has rank $15$, the representation

$$ \sigma_e e_e=\sum_{z\in Z}\beta_z\Phi(z) $$

is unique. Every nonzero $\beta_z$ forces $s(z)=\mathrm{sgn}(\beta_z)$. Conflicting requirements from two zero edges eliminate the whole tangent cube. Exact rational solves eliminate $1030$ of the $1466$ simple ray orbits this way.

The final clause archive contains $5837$ primitive wrong-edge quadratics and $892$ nonnegative integer Gordan circuits. Together with singleton leaves for raw symmetry images of the $380$ archived masks, these clauses cover every tangent Boolean cube for all $2272$ ray orbits. The exact zero-set layers are

$$ 15:1466, \quad 16:428, \quad 17:240, \quad 18:73, \quad 19:22, \quad 20:33, \quad 22:4, \quad 24:6. $$

The [tangent-cover verifier](verify_n5_c5_cocircuit_tangent_cover.py) checks every wrong edge, every integer Gordan identity, every rational simple-ray forcing equation, and the complete Boolean cover. It uses no optimization solver. The optimization calls in the [clause discovery script](classify_n5_c5_cocircuit_tangent_topes.py) only find candidate clauses, which are reconstructed exactly before being stored.

**Theorem.** Every fully locked complementary-cycle quadratic sign cell is symmetry-equivalent to one of the $380$ archived classes and has head complexity at most two.

**Proof.** By the no-weak-affine-ray lemma, the section $\ell=1$ of the closed sign cone is a bounded polytope. Choose one of its vertices. The corresponding cone ray has at least $15$ independent zero evaluations, so it is one of the globally enumerated rank $15$ cocircuit rays in the closed complementary-cycle orthant. The sign cell gives one tangent assignment at that ray. The exact tangent cover either rules it out by a wrong-edge clause, rules out strict representability by a Gordan clause, or identifies it with an archived mask. The first two alternatives are impossible for a fully locked strict cell. Every archived mask has an exact two-scale certificate with two heads. Therefore the original cell has head complexity at most two. $\blacksquare$

## Extreme-ray bridge between locked components

The two known one-flip components meet at a common extreme ray. In Fourier coordinates, take

$$ q(z)=-1+z_0-z_1+z_0z_1-z_0z_2+z_0z_4+z_1z_2-z_1z_4. $$

This polynomial vanishes on $22$ cube vertices. The corresponding $22$ Fourier rows have exact rank $15$, so the zero set cuts out an extreme ray in the $16$-dimensional coefficient space.

An aligned cell from the main component has mask **0x3b8ad093**, whose order $40$ canonical form is **0x1bead0cb**. The isolated component has mask **0x3a8ac089**. Both closed sign cones contain the displayed ray. Their truth tables differ at vertices

$$ 1, 3, 4, 12, 24. $$

Those five Fourier rows have rank $5$, but the two chambers do not share a relative codimension-five face. The common strict-margin linear program with only those five evaluations set to zero has optimum zero. Their actual closure intersection contains the rank $15$ extreme ray above.

There is a geodesic through the tangent tope arrangement at that ray:

$$ \mathtt{0x3b8ad093}\to\mathtt{0x3b8ad091}\to\mathtt{0x3b8ad099}\to\mathtt{0x3b8ad089}\to\mathtt{0x3b8ac089}\to\mathtt{0x3a8ac089}. $$

The successive flips are exactly at vertices $1,3,4,12,24$. Every mask in the path has an exact strict quadratic representative in the complementary-cycle orthant. The four intermediate sign cells are not fully locked; each has an exact strict representative reversing chord $02$. All six strict representatives, the four unlocking representatives, the extreme ray, and both rank checks are verified by the [edge-extremal verifier](verify_n5_c5_fixed_chord_extremizer.py).

This identifies the correct global enumeration primitive. One must enumerate rank $15$ locked cocircuit rays, enumerate every strict tangent tope incident to each ray, retain the fully locked topes, and then quotient by the order $40$ symmetry group. Single-vertex adjacency among fully locked topes misses the isolated class, while cocircuit incidence detects it.

## A rigid complementary-cycle cell

Consider the truth table with hexadecimal mask **0x7b9af0d7**, where the vertex code is $x_1+2x_2+4x_3+8x_4+16x_5$. In sign coordinates $z_i=2x_i-1$, it is represented strictly by

$$ \begin{aligned} p(z)={}&988-12z_1-979z_2+997z_3-15z_4-15z_5 \\ &+6z_1z_2-1003z_1z_3-6z_1z_4+1009z_1z_5+497z_2z_3 \\ &-973z_2z_4-491z_2z_5+500z_3z_4-997z_3z_5+488z_4z_5. \end{aligned} $$

Its minimum signed value is $6$. The positive quadratic edges are

$$ 12,\ 23,\ 34,\ 45,\ 15, $$

and the other five edges are negative.

This coloring is forced for every strict quadratic representative of the same truth table. Let $\Phi(z)$ be the vector of all Fourier monomials of degree at most two, and let $s(z)$ be the target sign. For every edge $ij$, the verifier constructs a nonnegative integer vector $\lambda^{ij}$ and a positive integer $\kappa_{ij}$ such that

$$ \sum_z\lambda^{ij}_z s(z)\Phi(z)=\kappa_{ij}\sigma_{ij}e_{ij}, $$

where $\sigma_{ij}=1$ on the displayed cycle and $\sigma_{ij}=-1$ on its complement. Therefore, for any strict quadratic representative with coefficient vector $\theta$,

$$ \sigma_{ij}\theta_{ij}=\frac{1}{\kappa_{ij}}\sum_z\lambda^{ij}_z s(z)\langle\Phi(z),\theta\rangle>0. $$

One of these duals is supported on vertex codes $20,21,22,23$ with unit weights and has moment $4e_{12}$. It annihilates every affine monomial, proving that the threshold degree is exactly two.

## Exact two-head certificate

Despite this coefficient rigidity, the function has two heads. Put

$$ \begin{aligned} A(x)&=-10841+9502x_1+1103x_2-5699x_3+4965x_4+5363x_5, \\ B(x)&=15-10x_1-x_2-x_3-x_4-x_5, \\ C(x)&=-2658+3495x_1-4285x_2+648x_3-1971x_4+4603x_5, \\ D(x)&=-5+8x_1-5x_2-2x_3-6x_4+10x_5. \end{aligned} $$

The quadratic $A D+C B$ has the required signs, with minimum signed value $156$. The factor $B$ is admissible. Reparameterize with

$$ E=D+11B=160-102x_1-16x_2-13x_3-17x_4-x_5, $$

and

$$ C'=C-11A=116593-101027x_1-16418x_2+63337x_3-56586x_4-54390x_5. $$

Then

$$ A D+C B=A E+C'B. $$

Both $B$ and $E$ have negative slopes and are positive on the cube. Their value ranges are respectively $[1,15]$ and $[11,160]$, so this is an exact two-head certificate.

## Exact two-scale data

The strict representative above also satisfies the two-scale Schur criterion. With slope labels $k=1$, $p=2$, $q=3$, $a=4$, $b=5$, take

$$ R=\frac{1}{10}, \qquad S=\frac{6}{5}, \qquad \delta=\frac{4}{13}, \qquad g=1, \qquad \sigma=-1. $$

Then the two fixed core slope coordinates are $2/65$ and $54/65$. The exact limiting quantities are

$$ H=\frac{6111}{10}, \qquad P=\frac{585}{4}, \qquad Q=-\frac{10717}{10}, \qquad \frac{\alpha}{s_k}=-\frac{497}{1003}, \qquad \frac{\alpha}{r_k}=\frac{497}{6}. $$

Choosing

$$ c-H=\frac{3062379}{19880}, \qquad c=\frac{15211047}{19880} $$

gives the positive outside limits

$$ P+\frac{\alpha}{s_k}(c-H)=\frac{2805171}{40120}, \qquad Q+\frac{\alpha}{r_k}(c-H)=\frac{935057}{80}. $$

This example proves that a sign cell can be rigidly confined to the complementary-five-cycle coefficient orthant and still have two heads. A universal proof must use more than coefficient-sign flexibility, while a counterexample needs an obstruction stronger than the locked cycle coloring.
