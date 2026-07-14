# Six-Bit Middle-Layer Triple Candidate

## Exact target

Use cube coordinates indexed by $0,\ldots,5$. Let $\chi(x)=(-1)^{\lvert x\rvert}$, and flip its sign at exactly the three vertices

$$ E=\lbrace21,38,41\rbrace=\lbrace010101,100110,101001\rbrace. $$

The resulting truth mask is

$$ \mathtt{0x96696bd669b69669}. $$

The exact verifier [verify_n6_parity_midlayer_triple_candidate.py](verify_n6_parity_midlayer_triple_candidate.py) checks an integer quartic sign polynomial with minimum signed value $1$. It also checks a positive Gordan relation of support $40$ annihilating every monomial of degree at most three. Therefore

$$ \deg_{\pm}(f)=4. $$

The rest of this note describes constraints satisfied by every quartic sign representative. These constraints do not yet prove $H^{\ast}(f)>4$.

## Parity-twist balance cone

Pass to sign coordinates $z_i=(-1)^{x_i}$. Let $p$ be any polynomial of degree at most four that strictly sign-represents $f$, and define

$$ r(z)=\chi(z)p(z). $$

Then $r$ is negative on $E$ and positive at every other cube vertex. Multiplication by $\chi$ sends Fourier degree at most four to Fourier degree at least two. Hence

$$ \sum_z r(z)=0, \qquad \sum_z r(z)z_i=0 \quad (0\leq i\leq5). $$

Conversely, any strictly signed value vector $r$ satisfying these seven equations gives a quartic sign representative after multiplication by $\chi$.

Write

$$ r(e)=-a_e<0 \quad (e\in E), \qquad r(z)=b_z>0 \quad (z\notin E), \qquad A=\sum_{e\in E}a_e. $$

The balance equations become

$$ \sum_{z\notin E}b_z=A, \qquad \sum_{z\notin E}b_z z=\sum_{e\in E}a_e e. $$

The three exceptional sign vectors have pairwise inner product $-2$. Fix $e\in E$ and take the inner product of the vector balance with $e$. This gives

$$ \sum_{z\notin E}b_z\langle e,z\rangle=6a_e-2(A-a_e)=8a_e-2A. $$

Among vertices outside $E$, the value $\langle e,z\rangle$ is at most $4$, and it is strictly below $4$ at some vertices of positive weight. Therefore

$$ 8a_e-2A<4A, \qquad 0<a_e<\frac{3A}{4}. $$

Thus no exceptional vertex can carry three quarters of the total negative mass.

## Fifteen rigid Fourier coefficients

Let

$$ U=\mathrm{span}_{\mathbb{F}_2}\lbrace51,60\rbrace. $$

The affine plane through the exceptional vertices is

$$ C=21+U=\lbrace21,38,41,26\rbrace. $$

Let $H=U^{\perp}\subseteq\mathbb{F}_2^6$. Then $\dim H=4$, and every character $\chi_h$ with $h\in H$ is constant on $C$. Denote this constant by $\eta_h$.

For nonzero $h\in H$, use the zero constant Fourier coefficient of $r$ to obtain

$$ \eta_h\sum_zr(z)\chi_h(z)=\sum_zr(z)\left(\eta_h\chi_h(z)-1\right)=-2\sum_{\eta_h\chi_h(z)=-1}r(z)<0. $$

Therefore

$$ \mathrm{sgn}\left(\widehat r(h)\right)=-\eta_h \qquad (0\neq h\in H). $$

Since $\widehat r(h)=\widehat p([6]\mathbin{\triangle}h)$, fifteen coefficients of every quartic $p$ have fixed strict signs. Using concatenated coordinate indices, they are:

- positive: $\widehat p(\varnothing)$, $\widehat p(2345)$, $\widehat p(0145)$, $\widehat p(0123)$, $\widehat p(135)$, $\widehat p(025)$, $\widehat p(034)$, and $\widehat p(124)$;

- negative: $\widehat p(01)$, $\widehat p(23)$, $\widehat p(45)$, $\widehat p(035)$, $\widehat p(125)$, $\widehat p(134)$, and $\widehat p(024)$.

This is a strict coefficient orthant, but the coefficients also satisfy cut-cone inequalities.

## Quotient cut cone

Translate the quotient $\mathbb{F}_2^6/U$ so that $C$ is its zero element. For every nonzero quotient coset $Q$, define

$$ \beta_Q=\sum_{z\in Q}r(z)>0. $$

For $0\neq h\in H$, put

$$ w_h=-32\eta_h\widehat r(h). $$

If $\psi_h(Q)$ is the common value of $\eta_h\chi_h$ on $Q$, then

$$ w_h=\sum_{Q:\psi_h(Q)=-1}\beta_Q>0. $$

Thus the fifteen rigid coefficient magnitudes are precisely weighted cuts of the four-dimensional quotient group. Fourier inversion gives, for every nonzero quotient coset,

$$ \beta_Q=-\frac{1}{8}\sum_{0\neq h\in H}\psi_h(Q)w_h>0. $$

These are fifteen strict linear inequalities among the fixed-sign coefficients. The verifier checks the cut identities and their inverse exactly for the displayed quartic certificate.

## Four-head tangent condition

Suppose a four-head representation exists. After clearing its positive affine denominators and absorbing the global intercept into one numerator, its quartic has the form

$$ P=\sum_{h=1}^4A_h\prod_{j\neq h}B_j, $$

where every $A_h$ and $B_h$ is affine. In sign coordinates, each denominator satisfies

$$ B_h(z)=\beta_{h,0}+\sum_{i=0}^5\beta_{h,i+1}z_i, \qquad \beta_{h,0}>\sum_{i=0}^5\lvert\beta_{h,i+1}\rvert, $$

and its six slopes have one common strict sign.

Let $p$ be the unique multilinear reduction of $P$ modulo the Boolean relations $z_i^2=1$. The polynomials $P$ and $p$ agree on the sign cube, so $p$ belongs to the strict balance and quotient-cut cone above.

Separately, homogenize the unreduced affine-product polynomial $P$ and let $I=(B_1,B_2,B_3,B_4)$. Every summand of $P$ contains three denominator factors, so

$$ P\in I^3. $$

Consequently, the common projective zero set of the four denominators is a linear space of dimension at least two and is a zero of multiplicity at least three for $P$. Equivalently, $P$ and all of its derivatives of order at most two vanish on that linear space. This statement concerns the unreduced polynomial $P$; Boolean multilinearization need not preserve the off-cube zero space.

The exact lower-bound problem has therefore been reduced to the following statement:

> No unreduced quartic $P\in I^3$, for an ideal generated by four admissible oriented denominator forms, has a Boolean multilinearization in the strict balance and quotient-cut cone above.

The existing numerical searches support this statement but do not prove it. A rigorous completion must separate these two semialgebraic sets, derive a forced boundary denominator, or provide an exact Positivstellensatz or Gordan certificate.
