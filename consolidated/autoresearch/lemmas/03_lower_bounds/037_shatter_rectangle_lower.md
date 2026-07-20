# A Reusable Head-Complexity Lower Bound from a Shatter-Rectangle

## Statement

Call a function $g : \lbrace 0,1\rbrace^N \to \lbrace 0,1\rbrace$ admitting of a **shatter-rectangle of order $s$** if the coordinates partition as $[N] = V_{\mathrm{row}} \sqcup V_{\mathrm{col}}$ and there are row assignments $\rho_S \in \lbrace 0,1\rbrace^{V_{\mathrm{row}}}$ ($S \subseteq [s]$) and column assignments $\kappa_j \in \lbrace 0,1\rbrace^{V_{\mathrm{col}}}$ ($j \in [s]$) with

$$
g(\rho_S, \kappa_j) = [\, j \in S\,] \qquad \text{for all } S \subseteq [s],\ j \in [s],
$$

where $(\rho_S, \kappa_j)$ is the assignment using $\rho_S$ on $V_{\mathrm{row}}$ and $\kappa_j$ on $V_{\mathrm{col}}$.

**Theorem.** There is an absolute constant $c > 0$ such that any $g$ admitting a shatter-rectangle of order $s$ (with $s$ large) has

$$
H^{*}(g) \;\geq\; \mathrm{tChow}_{\pm}(g) \;\geq\; \frac{c\,s}{\log_2 s}.
$$

> **The session's lower-bound technique, abstracted into a tool.** It is a *localized* counting bound: where the Warren counting separation ([023_counting_separation.md](023_counting_separation.md)) counts over all Boolean functions nonconstructively, this counts over the $2H+1$ row-parameters of a *single* function on a structured slice, and so certifies a near-linear lower bound for a *named* $g$. It is positivity-free (bounds $\mathrm{tChow}_{\pm}$) and subsumes the explicit separations: $\mathrm{INT}_n$ ([035_int_nearlinear_lower.md](035_int_nearlinear_lower.md)) and disjoint monotone DNFs ([036_disjoint_dnf_lower.md](036_disjoint_dnf_lower.md)) are instances.

## Proof

Fix a sign-representing tangent form of order $H = \mathrm{tChow}_{\pm}(g)$ with affine $N_h(z) = a_h + \sum_v p_{h,v} z_v$, $D_h(z) = b_h + \sum_v r_{h,v} z_v$, and scalar $\theta$.

**Case A: $2H+1 \leq s$.**

**Affine forms split across the rectangle.** For any affine $A(z) = a_0 + \sum_v a_v z_v$, since $V_{\mathrm{row}}, V_{\mathrm{col}}$ partition $[N]$,

$$
A(\rho_S, \kappa_j) = \underbrace{a_0 + \sum_{v \in V_{\mathrm{row}}} a_v (\rho_S)_v}_{\text{depends only on } S} + \underbrace{\sum_{v \in V_{\mathrm{col}}} a_v (\kappa_j)_v}_{\text{depends only on } j}.
$$

Applying this to $N_h$ and $D_h$: $N_h(\rho_S, \kappa_j) = \alpha_{h,S} + \mu_{h,j}$ and $D_h(\rho_S, \kappa_j) = \beta_{h,S} + \nu_{h,j}$, where $\alpha_{h,S} = a_h + \sum_{v\in V_{\mathrm{row}}} p_{h,v}(\rho_S)_v$, $\beta_{h,S} = b_h + \sum_{v\in V_{\mathrm{row}}} r_{h,v}(\rho_S)_v$ depend only on $S$, and $\mu_{h,j}, \nu_{h,j}$ depend only on $j$.

**A parametric family.** Let $w = (\theta, \alpha_1, \dots, \alpha_H, \beta_1, \dots, \beta_H) \in \mathbb{R}^{2H+1}$, and for each column $j$ set

$$
Q_j(w) = \theta\prod_h(\beta_h + \nu_{h,j}) + \sum_h(\alpha_h + \mu_{h,j})\prod_{g\neq h}(\beta_g + \nu_{g,j}),
$$

a polynomial of degree $\leq H+1$ in $w$ (the $\mu_{h,j}, \nu_{h,j}$ are fixed constants). With $w_S = (\theta, \alpha_{h,S}, \beta_{h,S})$ we have $Q_j(w_S) = P(\rho_S, \kappa_j)$, so by the shatter-rectangle property and strict sign-representation $\mathrm{sgn}\,Q_j(w_S) = +1$ iff $j \in S$. As $S$ ranges over $2^{[s]}$, all $2^s$ distinct $\pm 1$ indicator vectors are realized over $w \in \mathbb{R}^{2H+1}$.

**Warren.** With $m = s$, $p = 2H+1$, $d = H+1$ and $m \geq p$, $2^s \leq (C(H+1)s/(2H+1))^{2H+1}$. As $(H+1)/(2H+1) \leq 1$, $\log_2$ gives $s \leq (2H+1)\log_2(Cs) \leq (2H+1)\cdot 2\log_2 s$ for large $s$, so $H \geq s/(8\log_2 s)$.

**Case B: $2H+1 > s$.** Then $H > (s-1)/2 \geq s/(8\log_2 s)$ for large $s$.

In both cases $\mathrm{tChow}_{\pm}(g) = H \geq s/(8\log_2 s)$ (take $c = 1/8$), and $\mathrm{tChow}_{\pm} \leq H^{*}$ gives the bound for $H^{*}$. $\blacksquare$

## Consequence

The hypothesis is purely combinatorial: a coordinate partition and assignments on which $g$ computes the membership predicate $[j \in S]$. The only analytic input is Warren. Three instances:

- **Set intersection** ($\mathrm{INT}_n$): $V_{\mathrm{row}} = $ the $x$-coordinates with $\rho_S = \mathbf 1_S$, $V_{\mathrm{col}} = $ the $y$-coordinates with $\kappa_j = e_j$; $\mathrm{INT}_n(\mathbf 1_S, e_j) = [j \in S]$. Order $n$, so $H^{*}(\mathrm{INT}_n) = \Omega(n/\log n)$ (L35).
- **Disjoint monotone DNF** (OR of $s$ disjoint width-$\geq 2$ ANDs): $V_{\mathrm{row}} = $ the rests with $\rho_S$ arming block $r$ iff $r \in S$, $V_{\mathrm{col}} = $ the pivots with $\kappa_j$ firing pivot $j$. Order $s$, so $H^{*} = \Omega(s/\log s)$ (L36).
- **Indexing / multiplexer** ($\mathrm{IDX}_k$: address $a \in \lbrace 0,1\rbrace^k$, memory $m \in \lbrace 0,1\rbrace^{2^k}$, output $m_a$): $V_{\mathrm{row}} = $ the memory bits with $\rho_S$ setting $m_a = [a \in S]$ (identifying addresses with $[2^k]$), $V_{\mathrm{col}} = $ the address bits with $\kappa_j = \mathrm{binary}(j)$; then $\mathrm{IDX}_k(\rho_S, \kappa_j) = m_{\,\mathrm{addr}\,j} = [j \in S]$. Order $s = 2^k$, so $H^{*}(\mathrm{IDX}_k) = \Omega(2^k / k) = \Omega(N/\log N)$ on $N = 2^k + k$ bits. Since $m_a = \sum_{b}[a=b]\,m_b$ is an exact multilinear polynomial of degree $k+1$, $\deg_{\pm}(\mathrm{IDX}_k) \leq k+1 = O(\log N)$, so this is a **second explicit separation** ($\deg_{\pm} = O(\log N)$ but $H^{*} = \Omega(N/\log N)$), on a canonical function. **It is outside L36's reach**: the $2^k$ implicit terms of $\mathrm{IDX}_k$ all *share* the $k$ address variables, so they are not disjoint — only the row/column coordinate partition (not disjointness) is needed, which is exactly what makes L37 strictly more general than L36.

Because the certificate bounds $\mathrm{tChow}_{\pm}$, it cannot witness a positivity gap (F4): like every other $H^{*}$ lower bound in this project (threshold degree, flattening, counting), it is positivity-free. The route to a *polynomial* (not near-linear) improvement, or to closing the $\log s$ factor, must exploit structure beyond the bare $2H+1$-parameter count — e.g. that $\rho_S$ is additive in $S$.
