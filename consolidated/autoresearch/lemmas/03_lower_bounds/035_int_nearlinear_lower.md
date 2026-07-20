# A Near-Linear Lower Bound on the Head Complexity of Set Intersection

## Statement

There is an absolute constant $c > 0$ such that for all large $n$, the set-intersection function $\mathrm{INT}_n(x,y) = \bigvee_{i=1}^n (x_i \wedge y_i)$ on $2n$ bits satisfies

$$
H^{*}(\mathrm{INT}_n) \;\geq\; \mathrm{tChow}_{\pm}(\mathrm{INT}_n) \;\geq\; \frac{c\,n}{\log_2 n}.
$$

Since $\deg_{\pm}(\mathrm{INT}_n) = 2$ ([033_int_explicit_separation.md](033_int_explicit_separation.md)), this is an **explicit near-linear separation** of head complexity from threshold degree, requiring no positivity.

> **The first explicit separation at a polynomial rate.** The flattening bound is capped at $\Omega(\log n)$ on any constant-degree function (L34), and the counting separation [023_counting_separation.md](023_counting_separation.md) that reaches $\Omega(n)$ is nonconstructive. This lemma reaches $\Omega(n/\log n)$ on a *named* function, by localizing the counting argument to $\mathrm{INT}_n$: restrict to the singleton-column slice, where the row $\mathbf 1_S$ acts through only $2H+1$ parameters, and apply Warren. It supersedes the logarithmic lower bound of L34 (whose $\mathrm{sr}_{x|y}(\mathrm{INT}_n) = \Theta(n)$ remains the reason flattening alone cannot do better here). The bound is positivity-free, so it also separates $\deg_{\pm}$ from $\mathrm{tChow}_{\pm}$ explicitly.

## Proof

Fix a sign-representing tangent form of order $H = \mathrm{tChow}_{\pm}(\mathrm{INT}_n)$,

$$
P = \theta\prod_{h=1}^H D_h + \sum_{h=1}^H N_h\prod_{g\neq h} D_g, \qquad
\begin{aligned}
N_h(x,y) &= a_h + \textstyle\sum_i p_{hi}x_i + \sum_i q_{hi}y_i,\\
D_h(x,y) &= b_h + \textstyle\sum_i r_{hi}x_i + \sum_i s_{hi}y_i,
\end{aligned}
$$

with $P > 0 \iff \mathrm{INT}_n = 1$. (No positivity assumed; the bound on $\mathrm{tChow}_{\pm}$ transfers to $H^{*}$ via the sandwich [018_tchow_sandwich.md](../01_foundations_and_normal_form/018_tchow_sandwich.md).)

**Case A: $2H+1 \leq n$.**

**Singleton-column restriction.** For $S \subseteq [n]$, $j \in [n]$, set $\alpha_{h,S} = a_h + \sum_{i\in S} p_{hi}$ and $\beta_{h,S} = b_h + \sum_{i\in S} r_{hi}$. Since $(\mathbf 1_S)_i = [i\in S]$ and $(e_j)_i = [i=j]$, $N_h(\mathbf 1_S, e_j) = \alpha_{h,S} + q_{hj}$ and $D_h(\mathbf 1_S, e_j) = \beta_{h,S} + s_{hj}$, so

$$
P(\mathbf 1_S, e_j) = \theta\prod_{h}(\beta_{h,S}+s_{hj}) + \sum_h (\alpha_{h,S}+q_{hj})\prod_{g\neq h}(\beta_{g,S}+s_{gj}).
$$

As $\mathrm{INT}_n(\mathbf 1_S, e_j) = [j\in S]$, strict sign-representation gives $\mathrm{sgn}\,P(\mathbf 1_S, e_j) = +1$ iff $j\in S$.

**A parametric family.** Let $w = (\theta, \alpha_1,\dots,\alpha_H, \beta_1,\dots,\beta_H) \in \mathbb{R}^{2H+1}$ and, for each $j$, define the polynomial $Q_j(w) = \theta\prod_h(\beta_h+s_{hj}) + \sum_h(\alpha_h+q_{hj})\prod_{g\neq h}(\beta_g+s_{gj})$, where $q_{hj}, s_{hj}$ are the fixed constants of $P$. Then $\deg Q_j \leq H+1$ (the term $\theta\prod_h(\beta_h+s_{hj})$ has degree $1+H$; the others degree $H$). Putting $w_S = (\theta, \alpha_{h,S}, \beta_{h,S})$ gives $Q_j(w_S) = P(\mathbf 1_S, e_j)$, so the sign vector $(\mathrm{sgn}\,Q_j(w_S))_{j\in[n]}$ is the $\pm 1$ indicator of $S$. Distinct subsets give distinct vectors, so **at least $2^n$ distinct sign vectors** of $(Q_1,\dots,Q_n)$ occur over $w \in \mathbb{R}^{2H+1}$.

**Warren.** With $m = n$ polynomials, $p = 2H+1$ variables, degree $d = H+1$, and $m \geq p$ (Case A), Warren's bound gives at most $(C(H+1)n/(2H+1))^{2H+1}$ sign vectors. Hence

$$
2^n \leq \left(\frac{C(H+1)n}{2H+1}\right)^{2H+1}.
$$

Since $(H+1)/(2H+1) \leq 1$, taking $\log_2$ yields $n \leq (2H+1)\log_2(Cn)$. For large $n$, $\log_2(Cn) \leq 2\log_2 n$, so $2H+1 \geq n/(2\log_2 n)$, giving $H \geq n/(8\log_2 n)$.

**Case B: $2H+1 > n$.** Then $H > (n-1)/2 \geq n/(8\log_2 n)$ for large $n$.

In both cases $\mathrm{tChow}_{\pm}(\mathrm{INT}_n) = H \geq n/(8\log_2 n)$; take $c = 1/8$. Since $\mathrm{tChow}_{\pm} \leq H^{*}$, the same bound holds for $H^{*}(\mathrm{INT}_n)$. $\blacksquare$

## Consequence

- **The rate of $H^{*}(\mathrm{INT}_n)$ is near-linear:** $n/(8\log_2 n) \leq H^{*}(\mathrm{INT}_n) \leq n$ (the upper bound is the monotone-term DNF count, L14). So $\mathrm{INT}_n$ needs $\widetilde{\Theta}(n)$ heads at threshold degree $2$ — the explicit separation is almost as strong as the nonconstructive $\Omega(n)$ of L23/L24. The remaining gap is the single $\log n$ factor.
- **A reusable technique.** The method is "counting localized by a structured restriction": pick a slice (here, rows $= \mathbf 1_S$, columns $= e_j$) on which (i) the target shatters many points and (ii) each row acts through few ($O(H)$) parameters; then Warren forces $H = \Omega(\#\text{points}/\log)$. This is the first per-function lower bound beyond $\deg_{\pm}$, flattening, and restriction, and it is positivity-free.
- **Open:** closing the $\log n$ gap (is $H^{*}(\mathrm{INT}_n) = \Theta(n)$?). Codex's suggested route uses the additive subset-sum structure of $(\alpha_{h,S}, \beta_{h,S})$ in $S$, not just the parameter count, to push toward $\Omega(n)$.
