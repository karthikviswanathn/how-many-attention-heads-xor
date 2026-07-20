# Counting Separation: Head Complexity is Strictly Finer than Threshold Degree

## Statement

**(a) Counting upper bound.** There is an absolute constant $c_1$ such that for every $H \geq 1$ and all large $n$,

$$
\#\lbrace\, f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace \;\mid\; H^{*}(f) \leq H \,\rbrace \;\leq\; 2^{c_1 H n^2}.
$$

**(b) Separation.** For all large $n$ there exists $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$ with

$$
\deg_{\pm}(f) \leq 2 \qquad\text{and}\qquad H^{*}(f) = \Omega(n).
$$

Hence $H^{*}$ is **not bounded by any function of threshold degree alone**: it is a genuinely new complexity measure, strictly finer than $\deg_{\pm}$.

> This is a nonconstructive but unconditional separation. It is much stronger than the flattening bound [022_flattening_lower_bound.md](022_flattening_lower_bound.md) ($\Omega(\log\mathrm{sr})$, hence $\Omega(\log n)$ for constant-degree functions): here a $\deg_{\pm}=2$ function needs $\Omega(n)$ heads.

## External inputs (standard theorems, used as given)

- **Warren's sign-pattern bound** (H. E. Warren, *Trans. AMS* 133 (1968), 167-178): the number of distinct sign vectors in $\lbrace -1,0,1\rbrace^m$ realized by $m$ real polynomials of degree $\leq d$ in $p$ variables, $m \geq p$, is at most $(C\,d\,m/p)^{p}$ for an absolute constant $C$.
- **Degree-2 PTF count** (P. Baldi, R. Vershynin, *SIAM J. Math. Data Sci.* 1 (2019), 699-729, arXiv:1803.10868, Thm 1.1 / Cor 1.2): the number $T(n,2)$ of degree-$\leq 2$ polynomial threshold functions on $\lbrace 0,1\rbrace^n$ satisfies $\log_2 T(n,2) = (1-o(1))\,n^3/6 = \Theta(n^3)$. In particular $T(n,2) \geq 2^{c_0 n^3}$ for an absolute $c_0 > 0$ and large $n$. (The $d=1$ case is Zuev's $2^{\Theta(n^2)}$ count of linear threshold functions.)

## Proof

### Part (a)

By the cleared normal form [016_cleared_denominator_invariant.md](../01_foundations_and_normal_form/016_cleared_denominator_invariant.md), every $f$ with $H^{*}(f) \leq H$ is realized by a parameter vector $w \in \mathbb{R}^p$ collecting the coefficients of the $H$ affine pairs $(N_h, D_h)$ and the scalar $\theta$, with $p = 2H(n+1) + 1 = \Theta(Hn)$. (Admissibility restricts $w$ to a subset, which only decreases the count.)

For each cube point $x \in \lbrace 0,1\rbrace^n$, the value $q_x(w) := \theta\prod_h D_h(x) + \sum_h N_h(x)\prod_{g\neq h}D_g(x)$ is a polynomial in $w$ of degree $\leq H+1$ (for fixed $x$, each $D_h(x), N_h(x)$ is degree $1$ in $w$; the products have degree $\leq H+1$). By the normal form, $f(x) = 1 \iff q_x(w) > 0$, so $f$ is determined by the sign vector $(\mathrm{sgn}\,q_x(w))_{x}$. Hence

$$
\#\lbrace f : H^{*}(f) \leq H\rbrace \leq \#\lbrace\text{sign vectors of } (q_x)_{x}\rbrace .
$$

Apply Warren with $m = 2^n$ polynomials, degree $d = H+1$, and $p = \Theta(Hn)$ variables (and $m \geq p$ for large $n$): the count is at most $(C(H+1)2^n/p)^p$, so

$$
\log_2 \#\lbrace f : H^{*}(f) \leq H\rbrace \leq p\log_2\!\big(C(H+1)2^n/p\big) = \Theta(Hn)\cdot\big(n - \Theta(\log(Hn))\big) = O(Hn^2).
$$

### Part (b)

Let $\mathcal T_n = \lbrace f : \deg_{\pm}(f) \leq 2\rbrace$, so $|\mathcal T_n| = T(n,2) \geq 2^{c_0 n^3}$. Suppose for contradiction that every $f \in \mathcal T_n$ had $H^{*}(f) \leq H_n := \lfloor \gamma n\rfloor$ with $\gamma = c_0/(2c_1)$. Then by part (a),

$$
2^{c_0 n^3} \leq |\mathcal T_n| \leq \#\lbrace f : H^{*}(f) \leq H_n\rbrace \leq 2^{c_1 H_n n^2} \leq 2^{(c_1\gamma) n^3} = 2^{(c_0/2)n^3},
$$

a contradiction for large $n$. Hence some $f \in \mathcal T_n$ has $H^{*}(f) > \lfloor\gamma n\rfloor$, so $H^{*}(f) \geq \gamma n = \Omega(n)$ while $\deg_{\pm}(f) \leq 2$. $\blacksquare$

## Consequence

Together with $\deg_{\pm}(f) \leq H^{*}(f)$ (L6) and the exact identity $H^{*} = \mathrm{MFdeg}_{\pm}$ (L16), this settles the qualitative half of the first core question: **head complexity is a strictly finer measure than threshold degree.** There exist functions of threshold degree $2$ requiring linearly many heads, so no bound $H^{*}(f) \leq g(\deg_{\pm}(f))$ holds. The exact location of $H^{*}$ between $\deg_{\pm}$ and the model (the $\mathrm{tChow}_{\pm}$ comparison) remains open. The argument is nonconstructive; producing an explicit $\deg_{\pm}=2$, $H^{*}=\Omega(n)$ family is open (the flattening bound gives explicit but only $\Omega(\log n)$ separations).
