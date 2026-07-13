# Paley-Hadamard Bilinear Strict Separation

## Statement

Let $q=19$, let $\mathbb{F}_{19}$ be the field of residues modulo $19$, and let $\chi:\mathbb{F}_{19}\to\lbrace-1,0,+1\rbrace$ be the quadratic character, with $\chi(0)=0$. Index a matrix $H_{20}$ by $\lbrace\infty\rbrace\cup\mathbb{F}_{19}$ in both coordinates, and define

$$ H_{20}(\infty,\infty)=1, \qquad H_{20}(\infty,j)=1, \qquad H_{20}(i,\infty)=-1, \qquad H_{20}(i,j)=\chi(i-j)+\mathbf{1}[i=j]. $$

Let

$$ H_2:=\begin{pmatrix}1&1\\1&-1\end{pmatrix}, \qquad H_{40}:=H_2\otimes H_{20}. $$

Order the rows and columns of $H_{40}$ lexicographically as

$$ (0,\infty),(0,0),\ldots,(0,18),(1,\infty),(1,0),\ldots,(1,18), $$

and let $S$ be its leading $38\times38$ principal submatrix. Introduce two blocks of Boolean variables

$$ x=(x_1,\ldots,x_{38}), \qquad y=(y_1,\ldots,y_{38}). $$

Define

$$ P(x,y):=\frac{1}{2}+\sum_{i=1}^{38}\sum_{j=1}^{38}S_{i,j}x_i y_j, $$

and define $f_{\mathrm{PH}}:\lbrace0,1\rbrace^{76}\to\lbrace0,1\rbrace$ by

$$ f_{\mathrm{PH}}(x,y)=1 \qquad\Longleftrightarrow\qquad P(x,y)>0. $$

Then

$$ \deg_{\pm}(f_{\mathrm{PH}})=2 \qquad\text{and}\qquad H^{\ast}(f_{\mathrm{PH}})\geq3. $$

In particular,

$$ \deg_{\pm}(f_{\mathrm{PH}})<H^{\ast}(f_{\mathrm{PH}}). $$

> **Interpretation.** Threshold degree is not always equal to head complexity. This explicit function on $76$ bits has a quadratic sign representation, but no sum of two one-head linear-fractional atoms can realize its sign pattern.

## Proof

### Lemma 1. The Paley-Hadamard submatrix has sign-rank at least seven

For a sign matrix $M\in\lbrace-1,+1\rbrace^{m\times n}$, let $\mathrm{srank}(M)$ denote the least rank of a real matrix with the same strict entrywise signs as $M$.

Forster's spectral-norm bound states that

$$ \mathrm{srank}(M)\geq\frac{\sqrt{mn}}{\lVert M\rVert_2}. $$

This is the main matrix theorem in [Forster, *A linear lower bound on the unbounded error probabilistic communication complexity*](https://doi.org/10.1016/S0022-0000(02)00019-3).

Let $Q$ be the $19\times19$ matrix with entries $Q_{i,j}=\chi(i-j)$. The standard quadratic-character correlation identity gives

$$ \sum_{k\in\mathbb{F}_{19}}\chi(i-k)\chi(j-k)=\begin{cases}18,&i=j,\\-1,&i\neq j.\end{cases} $$

Because $19\equiv3\pmod4$, one also has $\chi(-1)=-1$. Therefore

$$ Q\mathbf{1}=0, \qquad Q^{\top}=-Q, \qquad QQ^{\top}=19I-J. $$

Writing $B=Q+I$, the definition of $H_{20}$ becomes

$$ H_{20}=\begin{pmatrix}1&\mathbf{1}^{\top}\\-\mathbf{1}&B\end{pmatrix}. $$

The displayed identities imply

$$ B\mathbf{1}=\mathbf{1}, \qquad BB^{\top}=20I-J, $$

and hence

$$ H_{20}H_{20}^{\top}=20I. $$

Since $H_2H_2^{\top}=2I$, the Kronecker product satisfies

$$ H_{40}H_{40}^{\top}=40I. $$

Thus $H_{40}$ is a sign matrix with spectral norm $\sqrt{40}$. Restricting rows and columns cannot increase operator norm, so

$$ \lVert S\rVert_2\leq\sqrt{40}. $$

Forster's bound now gives

$$ \mathrm{srank}(S)\geq\frac{38}{\lVert S\rVert_2}\geq\frac{38}{\sqrt{40}}>6. $$

Since sign-rank is an integer,

$$ \mathrm{srank}(S)\geq7. $$

### Lemma 2. Two heads give singleton-slice sign-rank at most six

Let $g$ be a Boolean function whose variables are split into blocks

$$ a=(a_1,\ldots,a_m), \qquad b=(b_1,\ldots,b_n). $$

For each $i,j$, let $z^{i,j}$ be the input with $a_i=b_j=1$ and every other coordinate equal to $0$. Define its two-block singleton-slice sign matrix by

$$ \Sigma_g(i,j):=\begin{cases}+1,&g(z^{i,j})=1,\\-1,&g(z^{i,j})=0.\end{cases} $$

If $g$ is computable with at most two heads, then

$$ \mathrm{srank}(\Sigma_g)\leq6. $$

**Proof.** By the linear-fractional normal form [010_linear_fractional_normal_form.md](../01_foundations_and_normal_form/010_linear_fractional_normal_form.md), after adding a zero atom if necessary, a two-head score has the form

$$ A(z)=c+\frac{N_1(z)}{D_1(z)}+\frac{N_2(z)}{D_2(z)}, $$

where every $N_h$ and $D_h$ is affine on the Boolean cube and

$$ D_1(z)>0, \qquad D_2(z)>0. $$

Clearing the positive denominators preserves the sign. The resulting quadratic polynomial is

$$ R(z)=(N_1(z)+cD_1(z))D_2(z)+N_2(z)D_1(z). $$

Thus $R$ is a sum of two products of affine functions.

Consider one such product $F(z)G(z)$. On the singleton slice, write

$$ F(z^{i,j})=\alpha+p_i+q_j, \qquad G(z^{i,j})=\beta+r_i+s_j. $$

Define

$$ R_i:=(\alpha+p_i)(\beta+r_i), \qquad C_j:=\alpha s_j+\beta q_j+q_j s_j. $$

Then

$$ F(z^{i,j})G(z^{i,j})=R_i+C_j+p_i s_j+r_i q_j. $$

Consequently, the matrix of this product on the singleton slice is the sum of one row-only matrix, one column-only matrix, and two outer products. For the sum of two affine products, the two row-only terms combine into one rank-one matrix, the two column-only terms combine into one rank-one matrix, and four outer products remain. Hence

$$ \mathrm{rank}\left([R(z^{i,j})]_{i,j}\right)\leq6. $$

The matrix $[R(z^{i,j})]_{i,j}$ has strict sign pattern $\Sigma_g$, so

$$ \mathrm{srank}(\Sigma_g)\leq6. \qquad\blacksquare $$

### Lemma 3. The Paley-Hadamard function has threshold degree two

The quantity

$$ \sum_{i=1}^{38}\sum_{j=1}^{38}S_{i,j}x_i y_j $$

is an integer on every Boolean input. Therefore $P(x,y)$ is always a nonzero half-integer. It strictly sign-represents $f_{\mathrm{PH}}$ and has degree $2$, so

$$ \deg_{\pm}(f_{\mathrm{PH}})\leq2. $$

For the reverse inequality, suppose an affine function $L$ sign-represents $f_{\mathrm{PH}}$. On the two-block singleton slice, it has the form

$$ L(z^{i,j})=\lambda+\alpha_i+\beta_j. $$

The matrix $[L(z^{i,j})]_{i,j}$ has rank at most $2$. On the other hand,

$$ P(z^{i,j})=\frac{1}{2}+S_{i,j}, $$

so its strict sign pattern is $S$. Thus the existence of $L$ would imply

$$ \mathrm{srank}(S)\leq2, $$

contradicting Lemma 1. Hence $f_{\mathrm{PH}}$ has no affine sign representation, and

$$ \deg_{\pm}(f_{\mathrm{PH}})=2. $$

### Conclusion

The singleton-slice sign matrix of $f_{\mathrm{PH}}$ is exactly $S$, because

$$ \mathrm{sign}(P(z^{i,j}))=S_{i,j}. $$

If two heads computed $f_{\mathrm{PH}}$, Lemma 2 would give $\mathrm{srank}(S)\leq6$. Lemma 1 gives $\mathrm{srank}(S)\geq7$, a contradiction. Therefore

$$ H^{\ast}(f_{\mathrm{PH}})\geq3. $$

Together with Lemma 3,

$$ \deg_{\pm}(f_{\mathrm{PH}})=2<3\leq H^{\ast}(f_{\mathrm{PH}}). \qquad\blacksquare $$

## Consequence

The universal lower bound

$$ \deg_{\pm}(f)\leq H^{\ast}(f) $$

can be strict even for a function with threshold degree two. The obstruction is visible on a non-subcube slice: two heads force rank at most six on every two-block singleton slice after clearing denominators, while this explicit Paley-Hadamard slice has sign-rank at least seven.

This construction proves that a strict separation exists on $76$ input bits. It does not prove that $76$ is the least possible dimension.
