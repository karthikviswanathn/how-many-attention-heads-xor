# HDTH4 Mixed Curvature Certificate

## Statement

Let $x,y\in\lbrace0,1\rbrace^4$, and let $p(x,y)$ be any real quadratic polynomial of the form

$$ p(x,y)=p_X(x)+p_Y(y)+x^{\top}K y. $$

Suppose

$$ p(x,y)<0 \quad\text{when } d_{\mathrm{H}}(x,y)\leq1, \qquad p(x,y)>0 \quad\text{when } d_{\mathrm{H}}(x,y)\geq2. $$

Then the symmetric part

$$ S=\frac{K+K^{\top}}{2} $$

is negative definite. In particular, $K$ is nonsingular.

For an affine map $F(x,y)=r+Px+Qy$ and a nondegenerate quadratic form $q$ with matrix $J$, the mixed matrix is

$$ K=2P^{\top}JQ. $$

Consequently, if $q(F(x,y))$ has the HDTH4 signs above, then both $P$ and $Q$ are nonsingular.

## Checkerboard inequality

Consider row endpoints $x_0,x_1$ and column endpoints $y_0,y_1$ for which the four labels form the negative-diagonal checkerboard

$$ \begin{pmatrix}-&+\\+&-\end{pmatrix}. $$

The mixed second difference is strictly negative:

$$ \begin{aligned} &p(x_0,y_0)-p(x_0,y_1)-p(x_1,y_0)+p(x_1,y_1) \\ &= (x_0-x_1)^{\top}K(y_0-y_1)<0. \end{aligned} $$

The within-block terms $p_X,p_Y$ cancel. Transposing the rectangle gives the same inequality with $K^{\top}$. Hence, if $a=x_0-x_1$ and $b=y_0-y_1$, then

$$ a^{\top}S b<0. $$

## Exact rectangles

Write $e_1,\ldots,e_4$ for the standard basis and

$$ p_i=e_1+\cdots+e_i. $$

Every row of the following table has Hamming distances at most $1$ on the diagonal and at least $2$ off the diagonal. It therefore certifies the displayed inequality $a^{\top}Sb<0$. Bitstrings list coordinates from $1$ through $4$.

| $a$ | $b$ | $x_0$ | $x_1$ | $y_0$ | $y_1$ |
|---|---|---:|---:|---:|---:|
| $p_1$ | $p_1$ | `1000` | `0000` | `1001` | `0001` |
| $p_2$ | $p_2$ | `1100` | `0000` | `1100` | `0000` |
| $p_3$ | $p_3$ | `1110` | `0000` | `1110` | `0000` |
| $p_4$ | $p_4$ | `1111` | `0000` | `1111` | `0000` |
| $p_1$ | $p_3$ | `1010` | `0010` | `1110` | `0000` |
| $p_2$ | $p_3$ | `1100` | `0000` | `1110` | `0000` |
| $p_2$ | $p_4$ | `1101` | `0001` | `1111` | `0000` |
| $p_3$ | $p_4$ | `1110` | `0000` | `1111` | `0000` |
| $p_1$ | $p_2-e_3$ | `1000` | `0000` | `1100` | `0010` |
| $p_1$ | $p_4-e_2$ | `1001` | `0001` | `1011` | `0000` |
| $p_1$ | $p_4-e_3$ | `1001` | `0001` | `1101` | `0000` |
| $p_4$ | $e_1+e_2$ | `1111` | `0000` | `1101` | `0001` |
| $p_4$ | $e_1+e_3$ | `1111` | `0000` | `1011` | `0001` |
| $p_4$ | $e_1+e_4$ | `1111` | `0000` | `1011` | `0010` |

The table directly gives

$$ p_i^{\top}S p_i<0 $$

for every $i$, together with

$$ p_1^{\top}S p_3<0, \quad p_2^{\top}S p_3<0, \quad p_2^{\top}S p_4<0, \quad p_3^{\top}S p_4<0. $$

It also gives

$$ p_1^{\top}S p_2=\frac{1}{2}\left(p_1^{\top}S(p_2-e_3)+p_1^{\top}S p_3\right)<0. $$

## Negative definiteness

Signed coordinate permutations preserve Hamming distance and the checkerboard inequalities. Given a nonzero $w\in\mathbb{R}^4$, apply one so that

$$ w_1\geq w_2\geq w_3\geq w_4\geq0. $$

Set

$$ \alpha_1=w_1-w_2, \quad \alpha_2=w_2-w_3, \quad \alpha_3=w_3-w_4, \quad \alpha_4=w_4. $$

Then every $\alpha_i$ is nonnegative and

$$ w=\alpha_1p_1+\alpha_2p_2+\alpha_3p_3+\alpha_4p_4. $$

All diagonal and cross terms in $w^{\top}Sw$ are strictly negative, except that the table does not directly determine $p_1^{\top}S p_4$. The missing combination is controlled in two cases.

If $\alpha_1\geq\alpha_4$, define

$$ q_2=p_4-e_2, \qquad q_3=p_4-e_3, \qquad q_4=p_4-e_4. $$

The table gives $p_1^{\top}S q_j<0$ for every $j$, and $q_2+q_3+q_4=p_1+2p_4$. Therefore

$$ \begin{aligned} \alpha_1^2p_1^{\top}Sp_1+2\alpha_1\alpha_4p_1^{\top}Sp_4 &= \alpha_1(\alpha_1-\alpha_4)p_1^{\top}Sp_1 \\ &\quad+\alpha_1\alpha_4\sum_{j=2}^4p_1^{\top}Sq_j\leq0. \end{aligned} $$

If $\alpha_4\geq\alpha_1$, define

$$ r_2=e_1+e_2, \qquad r_3=e_1+e_3, \qquad r_4=e_1+e_4. $$

The table gives $p_4^{\top}S r_j<0$ for every $j$, and $r_2+r_3+r_4=2p_1+p_4$. Thus

$$ \begin{aligned} \alpha_4^2p_4^{\top}Sp_4+2\alpha_1\alpha_4p_1^{\top}Sp_4 &= \alpha_4(\alpha_4-\alpha_1)p_4^{\top}Sp_4 \\ &\quad+\alpha_1\alpha_4\sum_{j=2}^4p_4^{\top}Sr_j\leq0. \end{aligned} $$

The controlled two-term combination is strictly negative whenever $\alpha_1+\alpha_4>0$. If $\alpha_1=\alpha_4=0$, then at least one of $\alpha_2,\alpha_3$ is positive, and its diagonal term is strictly negative. Every other nonzero term in the expansion is also strictly negative. Hence

$$ w^{\top}Sw<0. $$

This proves that $S$ is negative definite. If $Kz=0$, then $z^{\top}Sz=z^{\top}Kz=0$, so $z=0$. Therefore $K$ is nonsingular. $\blacksquare$

## Equivalent matched and mismatched slopes

In sign coordinates, write the affine map as

$$ F(u,v)=r+Pu+Qv. $$

Let $A=P+Q$ and $B=P-Q$. The conclusion above is equivalently

$$ B^{\top}JB-A^{\top}JA=-2(P^{\top}JQ+Q^{\top}JP)\succ0. $$

Thus the pullback quadratic form on mismatch directions strictly dominates the pullback form on match directions in every nonzero coordinate direction, not only on the four coordinate axes.

## Lyapunov normal form

Since $K=2P^{\top}JQ$ is nonsingular, both $P$ and $Q$ are nonsingular. Set

$$ T=Q^{-1}P, \qquad G=Q^{\top}JQ. $$

Then $G$ has signature $(2,2)$ and

$$ T^{\top}G+GT\prec0. $$

In particular, $T$ has no eigenvalue on the imaginary axis. To see this, if $Tz=i\omega z$ for a nonzero complex vector $z$, then

$$ z^{\ast}(T^{\top}G+GT)z=2\mathrm{Re}(i\omega z^{\ast}Gz)=0, $$

contrary to negative definiteness.

Moreover, $T$ has exactly two eigenvalues in each open half-plane, counted with algebraic multiplicity. On the stable generalized eigenspace, the function

$$ t\longmapsto (e^{tT}z)^{\ast}G(e^{tT}z) $$

is strictly decreasing and tends to $0$ as $t\to+\infty$. Hence $G$ is positive definite on the stable space, whose dimension is at most $2$. Running the same argument backward on the unstable generalized eigenspace shows that $G$ is negative definite there, so its dimension is also at most $2$. The two dimensions sum to $4$, and therefore both equal $2$.

Finally, a common real coordinate change on the two four-dimensional input blocks puts the mixed matrix in the form

$$ K=-I+\Omega, \qquad \Omega^{\top}=-\Omega. $$

Indeed, first choose $R$ with $R^{\top}SR=-I$ and replace $K$ by $R^{\top}KR$. Its symmetric part is then $-I$, leaving a skew-symmetric remainder $\Omega$.

## Shell-two transition moment

The following consequence uses only the signs on shells $1$ and $2$. It does not use the shell $3$ or shell $4$ values needed by the negative-definiteness proof above.

In sign coordinates, set

$$ A_i=P_i+Q_i, \qquad B_i=P_i-Q_i. $$

For a defect set $S\subseteq\lbrace1,2,3,4\rbrace$, let $C_S$ be the matrix whose $i$-th column is $B_i$ when $i\in S$ and $A_i$ otherwise. Thus the target values with defect set $S$ are

$$ F_S(\epsilon)=r+C_S\epsilon, \qquad \epsilon\in\lbrace-1,1\rbrace^4. $$

Define the signed moment matrix

$$ M_S=\mathbb{E}_{\epsilon}\left[q(F_S(\epsilon))\begin{pmatrix}1\\\epsilon\end{pmatrix}\begin{pmatrix}1\\\epsilon\end{pmatrix}^{\top}\right]. $$

If $q(F_S(\epsilon))<0$ for every $\epsilon$, then $M_S\prec0$. Indeed, for any nonzero affine coefficient vector $v$, the quantity

$$ v^{\top}M_Sv=\mathbb{E}_{\epsilon}\left[q(F_S(\epsilon))(v_0+v_1\epsilon_1+\cdots+v_4\epsilon_4)^2\right] $$

is strictly negative. The corresponding statement with positive signs gives $M_S\succ0$.

Fix distinct $i,j$. Shell $1$ and shell $2$ therefore give

$$ M_{\lbrace i\rbrace}\prec0, \qquad M_{\lbrace i,j\rbrace}\succ0, \qquad M_{\lbrace i,j\rbrace}-M_{\lbrace i\rbrace}\succ0. $$

Put $d_j=B_j-A_j$ and

$$ \delta_j=q(B_j)-q(A_j). $$

Replacing $A_j\epsilon_j$ by $B_j\epsilon_j$ changes the score by

$$ q(F_{\lbrace i,j\rbrace}(\epsilon))-q(F_{\lbrace i\rbrace}(\epsilon))=\delta_j+2\langle d_j,r\rangle_q\epsilon_j+2\sum_{k\neq j}\langle d_j,(C_{\lbrace i\rbrace})_k\rangle_q\epsilon_j\epsilon_k. $$

Order the affine monomials as $1,\epsilon_j,(\epsilon_k)_{k\neq j}$. The moment-matrix difference has the arrow form

$$ M_{\lbrace i,j\rbrace}-M_{\lbrace i\rbrace}=\begin{pmatrix}\delta_j&L&0\\L&\delta_j&c^{\top}\\0&c&\delta_jI_3\end{pmatrix}, $$

where

$$ L=2\langle d_j,r\rangle_q, \qquad c_k=2\langle d_j,(C_{\lbrace i\rbrace})_k\rangle_q. $$

Its positive definiteness is equivalent to

$$ \delta_j>0, \qquad \delta_j^2>L^2+\lVert c\rVert_2^2. $$

Consequently, for every $i\neq j$,

$$ \delta_j^2>4\left(\langle d_j,r\rangle_q^2+\langle d_j,B_i\rangle_q^2+\sum_{k\notin\lbrace i,j\rbrace}\langle d_j,A_k\rangle_q^2\right). $$

These twelve Euclidean row-contraction inequalities are a shell-two-only constraint on any putative affine split-quadratic realization.

## Pointwise transition strengthening

The full pointwise signs give a stronger exact inequality. For fixed distinct $i,j$, every value on shell $2$ is positive and the corresponding value on shell $1$ is negative. Hence their difference is positive for every $\epsilon$:

$$ \delta_j+2\langle d_j,r\rangle_q\epsilon_j+2\sum_{k\neq j}\langle d_j,(C_{\lbrace i\rbrace})_k\rangle_q\epsilon_j\epsilon_k>0. $$

The four signs $\epsilon_j$ and $(\epsilon_j\epsilon_k)_{k\neq j}$ vary independently. Taking the minimum over them gives the exact strict condition

$$ \delta_j>2\left(\left|\langle d_j,r\rangle_q\right|+\left|\langle d_j,B_i\rangle_q\right|+\sum_{k\notin\lbrace i,j\rbrace}\left|\langle d_j,A_k\rangle_q\right|\right). $$

This pointwise $\ell_1$ inequality strictly strengthens the Euclidean moment inequality above.

## Normalized transition coordinates

The transition inequalities admit a useful square normalization. Put

$$ D=(d_1,d_2,d_3,d_4), \qquad \Delta=\mathrm{diag}(\delta_1,\delta_2,\delta_3,\delta_4), $$

and define four covectors

$$ \phi_j(x)=\frac{2\langle d_j,x\rangle_q}{\delta_j}. $$

Let $\Phi$ be the matrix with rows $\phi_j$, and set

$$ C=\Phi P, \qquad E=\Phi Q, \qquad t=\Phi r. $$

Since $d_j=-2Q_j$ and $Q$ is nonsingular, $\Phi$ is nonsingular. The definitions give

$$ C_{jj}=1, \qquad \Delta E=E^{\top}\Delta, \qquad \Delta C+C^{\top}\Delta\succ0. $$

The last inequality is the mixed-curvature conclusion in these coordinates. Indeed,

$$ \Delta C+C^{\top}\Delta=2\left(D^{\top}JP+P^{\top}JD\right)\succ0. $$

For distinct $i,j$, the shell-transition inequality becomes

$$ t_j^2+(C_{ji}-E_{ji})^2+\sum_{k\notin\lbrace i,j\rbrace}(C_{jk}+E_{jk})^2<1. $$

Thus every row has three different Euclidean contraction inequalities, one for each choice of the pre-existing defect $i$.

The pointwise strengthening becomes

$$ |t_j|+|C_{ji}-E_{ji}|+\sum_{k\notin\lbrace i,j\rbrace}|C_{jk}+E_{jk}|<1. $$

These twelve strict $\ell_1$ contractions retain information that the moment matrices discard.

There is also a scalar constraint that comes from averaging the score over the sign vector $\epsilon$. Define

$$ \alpha_0=q(r)+\sum_{k=1}^4q(A_k). $$

The Fourier constant on defect set $S$ is

$$ \alpha_S=\alpha_0+\sum_{i\in S}\delta_i. $$

Shells $0$, $1$, and $2$ therefore imply, with $\tau=-\alpha_0$,

$$ \tau>0, \qquad 0<\delta_i<\tau, \qquad \delta_i+\delta_j>\tau \quad(i\neq j). $$

These relations are independent of the higher Fourier coefficients.

## Exact admissible-factor reduction

Suppose the four-dimensional factor span contains an admissible affine factor. After complementing all eight input bits if necessary, write it as

$$ \ell(F(u,v))=c+a^{\top}u+b^{\top}v, $$

where every coordinate of $a$ and $b$ is strictly positive and

$$ c>\sum_{i=1}^4(a_i+b_i). $$

For a factor in a split form $q=AD+CB$, the covector $\ell$ is null for the dual quadratic form:

$$ \ell^{\top}J^{-1}\ell=0. $$

Conversely, a dual-null covector is exactly a possible affine factor of a rank-four split quadratic form. The one-admissible-factor reparameterization then turns it into two admissible denominators.

Because $\Phi$ is invertible, write

$$ \ell(x)=\lambda^{\top}\Phi x. $$

The denominator slopes and intercept become

$$ a=C^{\top}\lambda, \qquad b=E^{\top}\lambda, \qquad c=\lambda^{\top}t. $$

Moreover,

$$ \Phi J^{-1}\Phi^{\top}=-4E\Delta^{-1}. $$

In particular, the symmetric matrix $E\Delta^{-1}$ is nonsingular and has signature $(2,2)$.

Hence dual nullness is the single quadratic equation

$$ \lambda^{\top}E\Delta^{-1}\lambda=0. $$

An admissible factor can therefore exist only if there is a nonzero $\lambda$ satisfying

$$ C^{\top}\lambda>0, \qquad E^{\top}\lambda>0, \qquad \lambda^{\top}E\Delta^{-1}\lambda=0, $$

and

$$ \lambda^{\top}t>\mathbf{1}^{\top}C^{\top}\lambda+\mathbf{1}^{\top}E^{\top}\lambda. $$

## Exact zonotope and kernel formulation

In normalized coordinates, the convex hull of all factor-space vertices is the zonotope

$$ Z=t+C[-1,1]^4+E[-1,1]^4. $$

A covector $\lambda$ is strictly positive on every vertex exactly when

$$ \lambda^{\top}t>\lVert C^{\top}\lambda\rVert_1+\lVert E^{\top}\lambda\rVert_1. $$

Thus $0\notin Z$ exactly when the factor span contains some globally positive affine function. An admissible positive-orientation factor additionally requires

$$ C^{\top}\lambda>0, \qquad E^{\top}\lambda>0, \qquad \lambda^{\top}E\Delta^{-1}\lambda=0. $$

Under the two coordinatewise positivity conditions, the zonotope inequality reduces to the intercept inequality in the preceding section. This is the exact polar-zonotope and dual-null-kernel formulation of the orientation problem. Proving $0\in Z$ for every HDTH4 realization would be stronger than necessary and would rule out two heads immediately.

## Symmetric scaling and a corrected finite target

The diagonal weights can be removed from the remaining algebra. Set

$$ U=\Delta C, \qquad V=\Delta E, \qquad w=\Delta t, \qquad \mu=\Delta^{-1}\lambda. $$

Then

$$ U_{jj}=\delta_j>0, \qquad U+U^{\top}\succ0, \qquad V=V^{\top}, \qquad \mathrm{inertia}(V)=(2,2). $$

The twelve pointwise transition inequalities become strict row diagonal-dominance inequalities:

$$ |w_j|+|U_{ji}-V_{ji}|+\sum_{k\notin\lbrace i,j\rbrace}|U_{jk}+V_{jk}|<U_{jj} \quad(i\neq j). $$

An admissible dual-null factor becomes a nonzero $\mu$ satisfying

$$ U^{\top}\mu>0, \qquad V\mu>0, \qquad \mu^{\top}V\mu=0, $$

and

$$ \mu^{\top}w>\mathbf{1}^{\top}U^{\top}\mu+\mathbf{1}^{\top}V\mu. $$

This is a symmetric, scale-free finite target. One possible closing lemma would assert that the strict diagonal-dominance inequalities and the four factor conditions force $V$ to have at most one positive eigenvalue. The final proof does not require that stronger statement. The column-max closure below rules out the finite target directly.

There is a useful exact reduction of that lemma. For any choice function $\sigma$ with $\sigma(j)\neq j$, define a matrix $M_{\sigma}$ by

$$ (M_{\sigma})_{jj}=U_{jj}, \qquad (M_{\sigma})_{jk}=\begin{cases}U_{jk}-V_{jk},&k=\sigma(j),\\U_{jk}+V_{jk},&k\neq j,\sigma(j).\end{cases} $$

Every $M_{\sigma}$, and every rowwise convex combination of these matrices, satisfies

$$ |w_j|+\sum_{k\neq j}|(M_{\sigma})_{jk}|<(M_{\sigma})_{jj}. $$

If one can choose such a rowwise convex combination $M$ with

$$ M^{\top}\mu\geq0, \qquad \mathbf{1}^{\top}M^{\top}\mu\leq\mathbf{1}^{\top}U^{\top}\mu+\mathbf{1}^{\top}V\mu, $$

then the contradiction is immediate. Indeed, strict row diagonal dominance and the triangle inequality give

$$ \mu^{\top}w<\lVert M^{\top}\mu\rVert_1=\mathbf{1}^{\top}M^{\top}\mu, $$

contrary to the intercept inequality. Thus the unresolved orientation question has been reduced to a concrete matrix-selection problem. Any proof of the selection statement from the displayed symmetric conditions would finish the eight-bit obstruction.

The structural identities, scalar shell constraints, and Euclidean contractions do not by themselves give such an obstruction. The following exact witness disproves that weaker relaxation.

## Counterexample to the shell-moment obstruction

Set $\Delta=I$, $\tau=3/2$, and

$$ \lambda=\begin{pmatrix}1\\1\\-1\\-1\end{pmatrix}, \qquad t=\begin{pmatrix}17/25\\17/25\\-99/100\\-99/100\end{pmatrix}. $$

Take

$$ E=\frac{1}{100}\begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&-1&0\\0&0&0&-1\end{pmatrix}, \qquad C=\begin{pmatrix}1&0&51/100&51/100\\0&1&51/100&51/100\\0&0&1&0\\0&0&0&1\end{pmatrix}. $$

Then $E\Delta^{-1}=E$ is symmetric with signature $(2,2)$, every diagonal entry of $C$ is $1$, and $C+C^{\top}$ has eigenvalues

$$ \frac{49}{50}, \quad 2, \quad 2, \quad \frac{151}{50}. $$

Thus all three normalized structural identities hold. The row-contraction left side equals $4913/5000$ in rows $1$ and $2$, for every permitted choice of $i$, and equals $9801/10000$ in rows $3$ and $4$. All twelve values are strictly less than $1$. Taking $\delta_i=1$ for every $i$ gives

$$ 0<\delta_i<\tau, \qquad \delta_i+\delta_j>\tau. $$

The proposed factor vector nevertheless satisfies

$$ C^{\top}\lambda=\begin{pmatrix}1\\1\\1/50\\1/50\end{pmatrix}>0, \qquad E^{\top}\lambda=\frac{1}{100}\begin{pmatrix}1\\1\\1\\1\end{pmatrix}>0, $$

$$ \lambda^{\top}E\Delta^{-1}\lambda=0, $$

and

$$ \lambda^{\top}t=\frac{167}{50}>\frac{52}{25}=\mathbf{1}^{\top}C^{\top}\lambda+\mathbf{1}^{\top}E^{\top}\lambda. $$

This witness is compatible with the full normalized affine geometry, not merely with isolated matrix inequalities. One may take

$$ \Phi=I, \qquad P=C, \qquad Q=E, \qquad r=t, \qquad J=\mathrm{diag}(-25,-25,25,25). $$

Then $d_j=-2Q_j$, every $\delta_j=q(B_j)-q(A_j)$ equals $1$, and the definition of each row $\phi_j$ is satisfied. The covector $\lambda^{\top}\Phi$ is dual-null and gives the strictly positive affine factor displayed above.

The associated quadratic does not have the HDTH4 pointwise signs. Therefore this is not a two-head construction for HDTH4. It shows instead that shell averages and affine moment matrices discard essential pointwise information.

Indeed, for rows $1$ and $2$ the left side of the pointwise $\ell_1$ contraction is

$$ \frac{17}{25}+2\left(\frac{51}{100}\right)=\frac{17}{10}>1. $$

Thus the corrected pointwise invariant rejects the witness.

The remaining sound route is to combine the exact zonotope and kernel formulation with the twelve pointwise $\ell_1$ contractions. The next section records the closure of that route. The mixed-curvature theorem, the moment inequalities, and the pointwise transition inequalities above remain valid.

## Column-max closure

The normalized pointwise system above is infeasible. First suppose every coordinate of $\mu$ is nonzero. Put

$$ s_i=\mathrm{sgn}(\mu_i), \qquad r_i=|\mu_i|, \qquad R=\mathrm{diag}(r_i), \qquad S=\mathrm{diag}(s_i), $$

and define

$$ H=RSVSR, \qquad q_i=\frac{1}{r_i}, \qquad g=H\mathbf{1}. $$

Then $H$ has inertia $(2,2)$, every $g_i$ is nonzero, and

$$ \mathrm{sgn}(g_i)=s_i, \qquad \sum_i g_i=0, \qquad \mathbf{1}^{\top}V\mu=\sum_iq_i|g_i|. $$

Apply one pointwise contraction in each row and choose its exceptional column optimally. The scalar inequalities

$$ -|X-Y|-tX\leq-tY, \qquad -|X+Y|-tX\leq tY $$

give

$$ \mathbf{1}^{\top}V\mu<\sum_j\left(\sum_{k\neq j}q_kH_{jk}-2\max_{i\neq j}(q_iH_{ij})\right). $$

After reindexing, this strict inequality says $L<0$, where

$$ L=\sum_iq_i(H_{ii}+|g_i|-g_i)+2\sum_j\max_{i\neq j}(q_iH_{ij}). $$

Set

$$ \widetilde{C}=H+\mathrm{diag}(|g|-g), \qquad M=\mathrm{diag}(q_i)\widetilde{C}. $$

The matrix $M$ has positive row sums, is diagonally symmetrizable, and has at least two positive eigenvalues. Moreover,

$$ L=\mathrm{tr}(M)+2\sum_j\max_{i\neq j}M_{ij}. $$

The four-dimensional column-max spectral inequality proves that the right side is strictly positive, contradicting $L<0$. The proof of that inequality centers the symmetric representative to zero row sums and expresses every four-point squared-distance vector as a nonnegative combination of the $81$ column-choice coefficient vectors.

If some coordinate of $\mu$ vanishes, perturb the zero coordinates and use one nonzero coordinate to preserve the null equation by the implicit function theorem. All other inequalities are strict, so the perturbed vector remains admissible and reduces to the preceding case.

Thus the normalized pointwise system has no admissible dual-null factor. This completes the eight-bit obstruction in [Lemma 189](../../lemmas/06_strict_separations/189_eight_bit_hamming_threshold_strict_separation.md). The exact finite identities are checked by [`verify_eight_bit_hamming_threshold_separation.py`](verify_eight_bit_hamming_threshold_separation.py).
