# Limit of the Blockwise Low-Degree Dual Construction

## Setup

Let $S$ be the 54-vertex union of the 40-row degree-three circuit support and its antipodal image. Let $E_2$ be signed evaluation on $S$ of all characters of degree at most two. Thus its rows are

$$ (E_2)_{v,T}=f(v)\chi_T(v), \qquad v\in S, \qquad \lvert T\rvert\leq2. $$

The full cone of nonnegative degree-two dual measures on this support is

$$ \mathcal C_2=\lbrace y\geq0:E_2^{\top}y=0\rbrace. $$

This cone contains every degree-three dual measure on $S$. In particular, it contains the equal-weight 16-flat circuit and the original 40-row circuit.

Fix four positive affine denominators $D_1,\ldots,D_4$, and put

$$ P_h=\prod_{j\neq h}D_j. $$

If $y\in\mathcal C_2$, then $y/P_h$ annihilates the full $h$-th affine numerator block. Indeed, multiplying it by $P_hA_h$ leaves the degree-one polynomial $A_h$, which $y$ annihilates. This suggests the blockwise cone

$$ \mathcal B_2(D)=\left\lbrace\sum_{h=1}^4\frac{y_h}{P_h}:y_h\in\mathcal C_2\right\rbrace. $$

If a nonzero element of $\mathcal B_2(D)$ also annihilated the full tangent matrix, it would give the desired four-head obstruction.

## Exact counterexample

The construction fails for the following small integer denominators in sign coordinates:

$$ \begin{aligned} D_1&=(28,-5,-4,-8,-3,-3,-4), \\ D_2&=(32,-8,-5,-8,-5,-1,-4), \\ D_3&=(33,5,6,3,3,5,6), \\ D_4&=(30,8,5,2,3,8,2). \end{aligned} $$

The first two rows have strictly negative slopes, and the last two have strictly positive slopes. Every intercept strictly exceeds the sum of the slope magnitudes. Hence every $D_h$ is strictly positive on the cube.

Let $K$ be the 54 by 28 signed tangent evaluation matrix for this tuple. The exact verifier supplies an integer tangent vector $x$ and four degree-two coefficient vectors $a_h$ such that

$$ r_h=Kx-P_hE_2a_h>0 \qquad (1\leq h\leq4) $$

entrywise on $S$. All displayed certificate coefficients have magnitude at most $1000$, and the smallest integer entry among the four vectors $r_h$ is $54912$.

Now take $z=\sum_h y_h/P_h\in\mathcal B_2(D)$. Since $E_2^{\top}y_h=0$,

$$ \begin{aligned} x^{\top}K^{\top}z &=\sum_{h=1}^4\sum_{v\in S}y_h(v)\frac{(Kx)(v)}{P_h(v)} \\ &=\sum_{h=1}^4\sum_{v\in S}y_h(v)\left((E_2a_h)(v)+\frac{r_h(v)}{P_h(v)}\right) \\ &=\sum_{h=1}^4\sum_{v\in S}y_h(v)\frac{r_h(v)}{P_h(v)}. \end{aligned} $$

This quantity is strictly positive whenever $z$ is nonzero. Therefore $K^{\top}z\neq0$ for every nonzero $z\in\mathcal B_2(D)$.

## Consequence

The 16-flat circuit cannot be completed by taking nonnegative sums of blockwise rescaled degree-two measures. Since $\mathcal C_3\subseteq\mathcal C_2$, the same counterexample rules out the analogous construction from the entire degree-three cone.

This does not refute a full 54-row tangent dual. It shows that such a dual must use affine-moment cancellations across the four blocks that cannot be decomposed into separately low-degree-balanced measures.

The exact calculation is reproduced by [`verify_n6_parity_triple_blockwise_degree2_limit.py`](verify_n6_parity_triple_blockwise_degree2_limit.py).
