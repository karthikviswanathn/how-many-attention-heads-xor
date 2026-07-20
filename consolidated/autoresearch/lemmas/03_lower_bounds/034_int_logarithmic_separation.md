# An Explicit Unbounded Separation of Head Complexity from Threshold Degree

## Statement

Let $\mathrm{INT}_n(x,y) = \bigvee_{i=1}^n (x_i \wedge y_i)$ be the set-intersection function on $2n$ bits. For every $n \geq 6$,

$$
H^{*}(\mathrm{INT}_n) \;\geq\; \tfrac12 \log_2 n .
$$

Since $\deg_{\pm}(\mathrm{INT}_n) = 2$ for all $n \geq 2$ ([033_int_explicit_separation.md](033_int_explicit_separation.md)), the gap $H^{*}(\mathrm{INT}_n) - \deg_{\pm}(\mathrm{INT}_n) \to \infty$: $\mathrm{INT}_n$ is an explicit family realizing an **unbounded** separation of head complexity from threshold degree.

> Where L33 exhibits one named function ($\mathrm{INT}_{14}$) needing a third head, this upgrades it to a divergence: a *single* explicit family on which $H^{*}$ grows without bound while threshold degree stays at $2$. It is the explicit counterpart of the nonconstructive counting separation [023_counting_separation.md](023_counting_separation.md), at the (necessarily) weaker logarithmic rate.

## Proof

Let $H = H^{*}(\mathrm{INT}_n)$ and $\Phi(H) = (H+1)2^H + 1$.

**Combine the two bounds.** By L33, $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$, and by the flattening bound [022_flattening_lower_bound.md](022_flattening_lower_bound.md) on the cut $x|y$, $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \leq \Phi(H)$. Hence

$$
n \;\leq\; \Phi(H) = (H+1)2^H + 1 . \tag{$\ast$}
$$

**$H \geq 2$ once $n \geq 6$.** $\Phi$ is strictly increasing on integers ($\Phi(H+1) - \Phi(H) = 2^H(H+3) > 0$), with $\Phi(1) = 5$. If $H \leq 1$, then $(\ast)$ gives $n \leq \Phi(1) = 5$; so $n \geq 6$ forces $H \geq 2$.

**The inequality $\Phi(H) \leq 4^H$ for integer $H \geq 2$.** First $H + 2 \leq 2^H$ for $H \geq 2$: the base $H = 2$ is $4 \leq 4$, and if $H + 2 \leq 2^H$ then $2^{H+1} = 2\cdot 2^H \geq 2(H+2) = 2H + 4 \geq (H+1) + 2$. Therefore, for $H \geq 2$,

$$
\Phi(H) = (H+1)2^H + 1 \leq (H+1)2^H + 2^H = (H+2)2^H \leq 2^H\cdot 2^H = 4^H ,
$$

using $1 \leq 2^H$ and then $H + 2 \leq 2^H$.

**Solve for $H$.** Fix $n \geq 6$. Then $H \geq 2$, so $(\ast)$ and the previous step give $n \leq \Phi(H) \leq 4^H = 2^{2H}$. Taking $\log_2$, $\log_2 n \leq 2H$, i.e. $H \geq \tfrac12\log_2 n$. Since $\tfrac12\log_2 n \to \infty$ while $\deg_{\pm}(\mathrm{INT}_n) = 2$ for all $n \geq 2$, the separation is unbounded. $\blacksquare$

## Consequence

The logarithmic rate is the exact ceiling of the flattening method on $\mathrm{INT}_n$, and indeed on any constant-degree function:

- **The sign-rank of $\mathrm{INT}_n$ is exactly $\Theta(n)$.** L33 gives $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$; conversely the rank-$(n+1)$ real matrix $R[x,y] = \sum_i x_i y_i - \tfrac12$ strictly sign-represents $\mathrm{INT}_n$ (positive iff some $x_i y_i = 1$), so $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \leq n+1$. Thus $n \leq \mathrm{sr}_{x|y}(\mathrm{INT}_n) \leq n+1$, and the flattening bound $H^{*} = \Omega(\log \mathrm{sr})$ cannot yield more than $\Theta(\log n)$ here.
- **Flattening is logarithmically capped on constant degree.** A degree-$d$ sign-representation gives $\mathrm{sr}_{A|B} \leq \binom{N}{\leq d} = N^{O(d)}$, so for any $f$ on $N$ bits with $\deg_{\pm}(f) = O(1)$ the flattening bound can never certify more than $H^{*}(f) = \Omega(\log N)$. Improving the *explicit* gap to a polynomial rate (matching the nonconstructive $\Omega(n)$ of L23/L24) therefore requires a non-flattening obstruction — which [035_int_nearlinear_lower.md](035_int_nearlinear_lower.md) supplies: a singleton-column Warren argument pushes the bound on $\mathrm{INT}_n$ all the way to $\Omega(n/\log n)$, so the head complexity of $\mathrm{INT}_n$ is $\widetilde{\Theta}(n)$ (between $n/(8\log_2 n)$ and the trivial $O(n)$ DNF bound, L14). This logarithmic bound is thus superseded for $\mathrm{INT}_n$, but the exact tightness of the flattening method (sign-rank $= \Theta(n)$) is the reason the stronger bound needed a different technique.
