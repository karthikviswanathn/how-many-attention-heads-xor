# Restrictions, Juntas, And Sign-Rank Lower Bounds

## Statement

This note records reusable structural facts.

First, $H^{*}$ is monotone under restrictions. If $g$ is obtained from

$$
f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace
$$

by fixing some input coordinates, then

$$
H^{*}(g) \leq H^{*}(f).
$$

Consequently, if some restriction of $f$ is $k$-bit parity or its complement, then

$$
H^{*}(f) \geq k.
$$

Second, adjoining dummy variables does not change $H^{*}$. If

$$
F(x,y)=f(x)
$$

where $y$ is a block of dummy input bits, then

$$
H^{*}(F)=H^{*}(f).
$$

Consequently, if $f$ is a $k$-junta, then $H^{*}(f)$ is exactly the head complexity of the induced function on its essential $k$ variables.

Third, $H^{*}$ controls sign-rank under every input partition. Let $I\sqcup J=\lbrace1,\ldots,n\rbrace$, and write inputs as $(u,v)\in\lbrace0,1\rbrace^{I}\times\lbrace0,1\rbrace^{J}$. Let $\Sigma_f^{I,J}$ be the sign matrix

$$
\Sigma_f^{I,J}(u,v)
:=
\begin{cases}
+1 & \text{if } f(u,v)=1, \\
-1 & \text{if } f(u,v)=0.
\end{cases}
$$

Let $\mathrm{srank}_{I,J}(f)$ be its sign-rank, namely the minimum rank of a real matrix with the same strict sign pattern as $\Sigma_f^{I,J}$. If $H=H^{*}(f)$, then

$$
\mathrm{srank}_{I,J}(f)
\leq
\sum_{r=0}^{H}
\sum_{i=0}^{r}
\binom{\lvert I\rvert}{i}
\binom{\lvert J\rvert}{r-i},
$$

where binomial coefficients outside their natural range are interpreted as $0$. Equivalently,

$$
H^{*}(f)
\geq
\min\left\lbrace
H :
\mathrm{srank}_{I,J}(f)
\leq
\sum_{r=0}^{H}
\sum_{i=0}^{r}
\binom{\lvert I\rvert}{i}
\binom{\lvert J\rvert}{r-i}
\right\rbrace.
$$

By Vandermonde's identity, the double sum is also

$$
\sum_{r=0}^{H}\binom{n}{r}.
$$

> **Interpretation.** Threshold degree is not the only systematic lower-bound route. Any partition on which $f$ has large sign-rank forces enough heads to supply a polynomial sign matrix of sufficient rank.

## Proof

### Lemma 1. Restriction monotonicity

Let $g$ be obtained from $f$ by fixing coordinates outside a set $K\subseteq\lbrace1,\ldots,n\rbrace$.

Take an optimal $H^{*}(f)$-head linear-fractional representation of $f$:

$$
c+\sum_{h=1}^{H^{*}(f)}\phi_h(x).
$$

Each atom has the form

$$
\phi_h(x)
:=
\frac{
\eta_h+\sum_{i=1}^{n}\rho_{h,i}\alpha_h^{x_i}(m_{h,i}+\delta_h x_i)
}{
\gamma_h+\sum_{i=1}^{n}\rho_{h,i}\alpha_h^{x_i}
}.
$$

After fixing $x_i=\xi_i$ for $i\notin K$, the denominator becomes

$$
\gamma_h'
+\sum_{i\in K}\rho_{h,i}\alpha_h^{x_i},
\qquad
\gamma_h'
:=
\gamma_h+\sum_{i\notin K}\rho_{h,i}\alpha_h^{\xi_i}.
$$

Since $\gamma_h'>0$, this is again a valid atom denominator in the remaining variables. The numerator is transformed in the same way by absorbing the fixed-coordinate contributions into a new constant $\eta_h'$. Thus each restricted atom is still a one-head atom.

Therefore the restricted score computes $g$ using at most $H^{*}(f)$ heads, and

$$
H^{*}(g) \leq H^{*}(f).
$$

If a restriction of $f$ is $k$-bit parity or its complement, then the restricted function has head complexity $k$ by the exact parity theorem and complement invariance from Lemma 3 below. Restriction monotonicity gives $H^{*}(f)\geq k$. $\blacksquare$

### Lemma 2. Dummy variables do not change head complexity

Let $f : \lbrace0,1\rbrace^k \to \lbrace0,1\rbrace$, and define

$$
F(x,y):=f(x)
$$

on $\lbrace0,1\rbrace^{k+r}$. We prove

$$
H^{*}(F)=H^{*}(f).
$$

The lower bound follows from restriction monotonicity by fixing the dummy block $y$ to any value.

For the upper bound, let $H:=H^{*}(f)$. If $H=0$, then $f$ is constant and so is $F$. Assume $H\geq1$.

Take an $H$-atom score for $f$:

$$ S(x) = c+\sum_{h=1}^{H}\phi_h(x), $$

with

$$
f(x)=1
\qquad\Longleftrightarrow\qquad
S(x)>0.
$$

Because the domain is finite and the inequalities are strict, there is a margin

$$
\Delta:=\min_{x\in\lbrace0,1\rbrace^k}\lvert S(x)\rvert>0.
$$

For each atom

$$ \phi_h(x) = \frac{ \eta_h+\sum_{i=1}^{k}\rho_{h,i}\alpha_h^{x_i}(m_{h,i}+\delta_h x_i) }{ \gamma_h+\sum_{i=1}^{k}\rho_{h,i}\alpha_h^{x_i} }, $$

extend it to the dummy variables by giving every dummy coordinate a tiny positive weight $\varepsilon>0$ and any fixed real value parameters, for instance $m_{h,j}=0$ for dummy $j$. Keep $\gamma_h,\eta_h,\alpha_h,\delta_h$ and the original active-coordinate parameters unchanged.

For each fixed $h$, the extended atom $\phi_{h,\varepsilon}(x,y)$ converges uniformly to $\phi_h(x)$ on the finite cube as $\varepsilon\to0$. Hence

$$
S_{\varepsilon}(x,y)
:=
c+\sum_{h=1}^{H}\phi_{h,\varepsilon}(x,y)
$$

converges uniformly to $S(x)$.

Choose $\varepsilon$ small enough that

$$
\lvert S_{\varepsilon}(x,y)-S(x)\rvert<\frac{\Delta}{2}
$$

for every $(x,y)$. Then $S_{\varepsilon}(x,y)$ has the same sign as $S(x)$ for every $(x,y)$, so it computes $F$. Therefore

$$
H^{*}(F)\leq H^{*}(f).
$$

Together with the lower bound, this proves equality. $\blacksquare$

### Lemma 3. Complement and global coordinate symmetries

Complements preserve $H^{*}$. If a score $S(x)$ computes $f$ by

$$
f(x)=1
\qquad\Longleftrightarrow\qquad
S(x)>0,
$$

then $-S(x)$ computes $1-f$ with the same heads. Hence

$$
H^{*}(1-f)=H^{*}(f).
$$

Permuting input coordinates also preserves $H^{*}$, because a coordinate permutation just relabels the positional embeddings in the construction.

Global bit flip also preserves $H^{*}$. To see this in the normal form, let

$$
\phi(x)
:=
\frac{
\eta+\sum_{i=1}^{n}\rho_i\alpha^{x_i}(m_i+\delta x_i)
}{
\gamma+\sum_{i=1}^{n}\rho_i\alpha^{x_i}
}
$$

be an atom. Then $\phi(1-y)$ equals

$$
\frac{
\eta+\sum_{i=1}^{n}\rho_i'\thinspace(\alpha')^{y_i}(m_i'+\delta' y_i)
}{
\gamma+\sum_{i=1}^{n}\rho_i'\thinspace(\alpha')^{y_i}
},
$$

where

$$
\alpha':=\alpha^{-1},
\qquad
\rho_i':=\rho_i\alpha,
\qquad
m_i':=m_i+\delta,
\qquad
\delta':=-\delta.
$$

Thus every atom remains an atom after replacing every input bit by its complement. Therefore

$$
H^{*}(x\mapsto f(1-x))=H^{*}(f).
$$

$\blacksquare$

### Lemma 4. Low heads imply low partition sign-rank

Suppose $f$ is computed with $H$ heads. By the threshold-degree lower-bound proof in [006_threshold_degree_head_complexity_bound.md](../01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md), there is a multilinear polynomial $P$ of degree at most $H$ such that

$$
P(x)>0
\qquad\Longleftrightarrow\qquad
f(x)=1
$$

on the Boolean cube.

Split the variables as $(u,v)$ across $I\sqcup J$. Expand

$$ P(u,v) = \sum_{\substack{A\subseteq I,\ B\subseteq J\\ \lvert A\rvert+\lvert B\rvert\leq H}} c_{A,B} \left(\prod_{i\in A}u_i\right) \left(\prod_{j\in B}v_j\right). $$

For fixed $A,B$, the matrix

$$
\left[
\left(\prod_{i\in A}u_i\right)
\left(\prod_{j\in B}v_j\right)
\right]_{u,v}
$$

has rank at most $1$, because it is an outer product of a function of $u$ and a function of $v$. Therefore the real matrix

$$
M_P(u,v):=P(u,v)
$$

has rank at most the number of monomials appearing in the displayed degree bound:

$$
\mathrm{rank}(M_P)
\leq
\sum_{r=0}^{H}
\sum_{i=0}^{r}
\binom{\lvert I\rvert}{i}
\binom{\lvert J\rvert}{r-i}.
$$

Since $M_P$ has the same strict sign pattern as $\Sigma_f^{I,J}$, the definition of sign-rank gives

$$
\mathrm{srank}_{I,J}(f)
\leq
\mathrm{rank}(M_P)
\leq
\sum_{r=0}^{H}
\sum_{i=0}^{r}
\binom{\lvert I\rvert}{i}
\binom{\lvert J\rvert}{r-i}.
$$

Taking $H=H^{*}(f)$ and rearranging gives the claimed lower bound. $\blacksquare$

## Consequence

The restriction part gives a simple exact obstruction:

$$
\text{parity restriction on } k \text{ free bits}
\qquad\Longrightarrow\qquad
H^{*}(f)\geq k.
$$

The dummy-variable part gives exact junta reduction. If $f$ is a $k$-junta and $f_{\mathrm{ess}}$ is its induced function on the essential variables, then

$$
H^{*}(f)=H^{*}(f_{\mathrm{ess}}).
$$

Thus every exact classification or universal upper bound for $k$ input variables applies unchanged to $k$-juntas in any larger ambient cube.

The sign-rank part gives a communication-complexity lower-bound route. For any partition $I\sqcup J$,

$$
H^{*}(f)
\geq
\min\left\lbrace
H :
\mathrm{srank}_{I,J}(f)
\leq
\sum_{r=0}^{H}\binom{n}{r}
\right\rbrace.
$$

This is weaker than the counting lower bound for a random function, but it is constructive: a single explicit high-sign-rank partition matrix certifies a concrete lower bound for that function.
