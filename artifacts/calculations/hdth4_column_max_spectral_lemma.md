# Four-Dimensional Column-Max Spectral Lemma

## Statement

Let $M$ be a diagonally symmetrizable real $4\times4$ matrix. Suppose

$$ M\mathbf{1}>0. $$

Define

$$ \mathcal{F}(M)=\mathrm{tr}(M)+2\sum_{j=1}^4\max_{i\neq j}M_{ij}. $$

If $M$ has at least two positive eigenvalues, then

$$ \mathcal{F}(M)>0. $$

Equivalently, if $\mathcal{F}(M)\leq0$, then $M$ has at most one positive eigenvalue.

The maximum is a column maximum. This index convention is essential.

## Symmetric reduction

Choose positive diagonal matrices $D,Q$ with $Q=D^{-1}$ such that

$$ C=DM \qquad\text{is symmetric}, \qquad M=QC. $$

Write $q_i=Q_{ii}$. Since $M\mathbf{1}>0$, the vector

$$ g=C\mathbf{1}=DM\mathbf{1} $$

is strictly positive. Moreover, $M$ is similar to the symmetric matrix $Q^{1/2}CQ^{1/2}$, which is congruent to $C$. Thus $M$ and $C$ have the same numbers of positive and negative eigenvalues.

For a symmetric matrix $A$, set

$$ \mathcal{F}_q(A)=\sum_iq_iA_{ii}+2\sum_j\max_{i\neq j}(q_iA_{ij}). $$

Then $\mathcal{F}(M)=\mathcal{F}_q(C)$.

Put

$$ \sigma=\mathbf{1}^{\top}g, \qquad B=C-\frac{gg^{\top}}{\sigma}. $$

The matrix $B$ is symmetric and $B\mathbf{1}=0$. Since $C$ is obtained from $B$ by a positive semidefinite rank-one update, two positive eigenvalues of $C$ force at least one positive eigenvalue of $B$. Also, $gg^{\top}/\sigma$ is entrywise positive, and $\mathcal{F}_q$ is increasing in every matrix entry. Therefore

$$ \mathcal{F}_q(C)>\mathcal{F}_q(B). $$

It remains to prove that a symmetric zero-row-sum matrix $B$ with a positive eigenvalue satisfies $\mathcal{F}_q(B)>0$.

## The coefficient cone

Assume for a contradiction that

$$ \mathcal{F}_q(B)\leq0. $$

Let $f$ range over the $3^4$ maps on $\lbrace1,2,3,4\rbrace$ satisfying $f(j)\neq j$. Define

$$ \ell_f(B)=\sum_iq_iB_{ii}+2\sum_jq_{f(j)}B_{f(j),j}. $$

The four choices in the column maxima are independent, so

$$ \mathcal{F}_q(B)=\max_f\ell_f(B). $$

Hence $\ell_f(B)\leq0$ for every $f$. Since $B\mathbf{1}=0$, define, for $i<j$,

$$ a^f_{ij}=q_i+q_j-2q_i\mathbf{1}[f(j)=i]-2q_j\mathbf{1}[f(i)=j]. $$

Then

$$ -\ell_f(B)=\sum_{i<j}B_{ij}a^f_{ij}\geq0. $$

We next prove that every squared-distance vector on four real points is a nonnegative combination of the vectors $a^f$.

## Four-vertex fractional edge allocation

Fix $x\in\mathbb{R}^4$. If all $x_i$ are equal, its squared-distance vector is zero and there is nothing to prove. Otherwise, put

$$ v_i=\frac{1}{q_i}, \qquad S=\sum_iv_i, \qquad \mu=\frac{1}{S}\sum_iv_ix_i, \qquad V=\sum_iv_i(x_i-\mu)^2, \qquad y_i=\frac{x_i-\mu}{\sqrt{V}}. $$

Thus

$$ \sum_iv_iy_i=0, \qquad \sum_iv_iy_i^2=1. $$

For every unordered pair $\lbrace i,j\rbrace$, define the edge capacity

$$ c_{ij}=\frac{v_iv_j}{2}\left(q_i+q_j-(y_i-y_j)^2\right)=\frac{v_i+v_j-v_iv_j(y_i-y_j)^2}{2}. $$

Weighted Cauchy-Schwarz gives

$$ (y_i-y_j)^2\leq\left(\frac{1}{v_i}+\frac{1}{v_j}\right)\sum_kv_ky_k^2=q_i+q_j, $$

so every $c_{ij}$ is nonnegative. The weighted variance identity gives

$$ \sum_{i<j}v_iv_j(y_i-y_j)^2=S\sum_iv_iy_i^2-\left(\sum_iv_iy_i\right)^2=S. $$

Consequently, the total edge capacity equals the total vertex demand:

$$ \sum_{i<j}c_{ij}=S=\sum_iv_i. $$

We claim that each edge capacity can be split between its two endpoints so that vertex $i$ receives exactly $v_i$. By the fractional edge-allocation form of the max-flow min-cut criterion, such a split exists if and only if

$$ \sum_{i\in A}v_i\geq\sum_{\lbrace i,j\rbrace\subseteq A}c_{ij} $$

for every vertex set $A$.

For completeness, join a super-source to one supply node for each edge, join that supply node to the two endpoint nodes, and give endpoint $i$ sink capacity $v_i$. A finite cut is determined by the endpoint set $A$ on the source side. Its capacity is the total edge supply minus the supply internal to $A$, plus the demand in $A$. Requiring this to be at least the total supply gives exactly the displayed inequalities.

For sets of size at most one, the inequality is immediate. For a two-vertex set,

$$ c_{ij}\leq\frac{v_i+v_j}{2}\leq v_i+v_j. $$

For the full vertex set, equality holds. It remains to check a three-vertex set, whose complement is a single vertex $k$. Using equality of total supply and demand, the required inequality is equivalent to

$$ \sum_{j\neq k}c_{kj}\geq v_k. $$

The left side is

$$ \sum_{j\neq k}c_{kj}=\frac{S+v_k-Sv_ky_k^2}{2}. $$

Finally, Cauchy-Schwarz and the two normalizations give

$$ (v_ky_k)^2=\left(\sum_{j\neq k}v_jy_j\right)^2\leq(S-v_k)(1-v_ky_k^2). $$

Rearranging yields

$$ Sv_ky_k^2\leq S-v_k, $$

which proves the three-vertex cut inequality.

Therefore there are nonnegative numbers $z_{ij}$ for ordered pairs $i\neq j$ such that

$$ z_{ij}+z_{ji}=c_{ij}, \qquad \sum_{j\neq i}z_{ij}=v_i. $$

Set

$$ p_{ij}=\frac{z_{ij}}{v_i}. $$

Every row of $P=(p_{ij})$ is a probability distribution on the other three vertices. Dividing the edge-splitting identity by $v_iv_j$ gives

$$ q_jp_{ij}+q_ip_{ji}=\frac{q_i+q_j-(y_i-y_j)^2}{2}. $$

Choose a random map $f$ by choosing $f(i)=j$ with probability $p_{ij}$, independently for the four vertices. For each $i<j$,

$$ \begin{aligned} \mathbb{E}[a^f_{ij}] &=q_i+q_j-2q_i p_{ji}-2q_jp_{ij} \\ &=(y_i-y_j)^2. \end{aligned} $$

Since $(x_i-x_j)^2=V(y_i-y_j)^2$, the squared-distance vector is the nonnegative combination

$$ \left((x_i-x_j)^2\right)_{i<j}=\sum_fV\mathbb{P}(f)\left(a^f_{ij}\right)_{i<j}. $$

## Conclusion

Apply the coefficient-cone identity to the inequalities $-\ell_f(B)\geq0$. For every $x\in\mathbb{R}^4$,

$$ \sum_{i<j}B_{ij}(x_i-x_j)^2\geq0. $$

Because $B\mathbf{1}=0$,

$$ x^{\top}Bx=-\sum_{i<j}B_{ij}(x_i-x_j)^2\leq0. $$

Thus $B$ is negative semidefinite, contradicting the positive eigenvalue forced by the inertia of $C$. Therefore $\mathcal{F}_q(C)>0$, and hence $\mathcal{F}(M)>0$. $\blacksquare$

## Exact role in the HDTH4 obstruction

In the normalized two-head obstruction, the remaining expression is precisely $\mathcal{F}(M)$ for a diagonally symmetrizable $4\times4$ matrix with positive row sums. The determinant condition gives two positive eigenvalues. The lemma therefore makes the remaining expression strictly positive, contradicting the required nonpositive inequality.
