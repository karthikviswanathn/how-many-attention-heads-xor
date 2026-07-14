# Eight-Bit Cofactor Candidate Checkpoint

## Candidate and exact sign-cell interval

For sign variables $x,y\in\lbrace-1,1\rbrace^4$, put

$$ Q_{\lambda}(x,y)=(1+\sum_i x_i)(1+\sum_i y_i)-\lambda(1+\sum_i x_i y_i). $$

The candidate in the search is $Q_3$. Its highlighted columns are exact:

$$ Q_3(x,-\mathbf{1})=-6, \qquad Q_3(x,\mathbf{1}-2e_j)=6x_j. $$

The whole interval $2\leq\lambda<5$ lies in the same strict quadratic sign cell. Indeed, direct integer evaluation gives

$$ \mathrm{sign}(Q_3(x,y))Q_2(x,y)>0, \qquad \mathrm{sign}(Q_3(x,y))Q_5(x,y)\geq0 $$

at all $256$ inputs. Since $Q_{\lambda}$ is affine in $\lambda$, strict positivity at the left endpoint and weak positivity at the excluded right endpoint prove the assertion.

## Singular mixed representative

The mixed coefficient matrix of $Q_{\lambda}$ is $J_4-\lambda I_4$. At $\lambda=4$,

$$ (J_4-4I_4)\mathbf{1}=0, \qquad \mathrm{rank}(J_4-4I_4)=3. $$

Thus the strict sign cell itself contains a representative with singular mixed block. No argument using only the target signs can force mixed-block nonsingularity, an inverse mixed block, or the absence of a prescribed left-null vector.

This directly blocks the proposed cofactor route. A rank-four pullback proof would need additional structure that is special to rank four, not merely a consequence of the quadratic sign cell.

## Pairwise checkerboards

Every negative-diagonal or positive-diagonal checkerboard gives a strict linear inequality on the sixteen mixed coefficients. Exact enumeration produces $571$ distinct inequality normals. Their span has dimension $16$, and $J_4-3I_4$ satisfies every inequality with integer margin at least $8$.

Consequently, the checkerboard cone is full-dimensional. Pairwise slices cannot force an exact cofactor identity or a fixed null vector. This conclusion is consistent with the explicit singular representative $Q_4$ above.

The finite claims are checked by [`verify_q8_cofactor_checkpoint.py`](verify_q8_cofactor_checkpoint.py).

## HDTH4 diagonal mixed subcase

The HDTH4 normalized pointwise system uses matrices $U,V$, a vector $w$, and a dual-null vector $\mu$. Suppose the off-diagonal entries of $V$ vanish. Then every choice of the exceptional index in the pointwise contraction gives

$$ |w_j|+\sum_{k\neq j}|U_{jk}|<U_{jj}. $$

For every vector $\mu$, the reverse triangle inequality yields

$$ \begin{aligned} \lVert U^{\top}\mu\rVert_1 &\geq \sum_j |\mu_j|\left(U_{jj}-\sum_{k\neq j}|U_{jk}|\right) \\ &>\sum_j|\mu_j||w_j|\geq\mu^{\top}w. \end{aligned} $$

Dual-null admissibility requires $U^{\top}\mu>0$, so

$$ \lVert U^{\top}\mu\rVert_1=\mathbf{1}^{\top}U^{\top}\mu. $$

It also requires $V\mu>0$. Hence

$$ \mu^{\top}w<\mathbf{1}^{\top}U^{\top}\mu<\mathbf{1}^{\top}U^{\top}\mu+\mathbf{1}^{\top}V\mu, $$

contradicting the admissible-factor intercept inequality. Therefore the HDTH4 finite system is infeasible whenever $V$ is diagonal. The general case, including off-diagonal mixed terms, is closed by the column-max spectral argument in [Lemma 189](../../lemmas/06_strict_separations/189_eight_bit_hamming_threshold_strict_separation.md).
