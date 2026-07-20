# The Head Complexity of a Disjoint Monotone DNF Equals Its Term Count up to a Log Factor

## Statement

Let $f = \bigvee_{r=1}^s T_r$ where $T_r = \bigwedge_{v \in B_r} v$ are monotone ANDs on pairwise-disjoint variable blocks $B_1,\dots,B_s$, each of width $|B_r| \geq 2$. Then there is an absolute constant $c > 0$ such that for large $s$,

$$
H^{*}(f) \;\geq\; \mathrm{tChow}_{\pm}(f) \;\geq\; \frac{c\,s}{\log_2 s}.
$$

Combined with the monotone-term DNF upper bound $H^{*}(f) \leq s$ ([014_monotone_term_dnf.md](../02_upper_bounds/014_monotone_term_dnf.md)), this gives $H^{*}(f) = \widetilde{\Theta}(s)$: **the head complexity of a disjoint monotone DNF is its number of terms, up to a logarithmic factor.**

> Generalizes the near-linear bound for set intersection ([035_int_nearlinear_lower.md](035_int_nearlinear_lower.md), the width-$2$, $s = n$ case) and the exact value $H^{*} = 2$ for two disjoint $2$-ANDs ([027_intersection2_exact.md](../02_upper_bounds/027_intersection2_exact.md), $s = 2$). It pairs the monotone-DNF *upper* bound (L14) with a matching *lower* bound, pinning the head complexity of an entire nonsymmetric family. Positivity-free (the bound is on $\mathrm{tChow}_{\pm}$); when the widths are $O(1)$, $\deg_{\pm}(f) = O(1)$ and this is an explicit polynomial separation from threshold degree.

## Proof

Fix a sign-representing tangent form of order $H = \mathrm{tChow}_{\pm}(f)$ with affine $N_h(z) = a_h + \sum_v p_{h,v} z_v$, $D_h(z) = b_h + \sum_v r_{h,v} z_v$, and scalar $\theta$. In each block $B_r$ fix a **pivot** $\pi_r \in B_r$ and let $R_r = B_r \setminus \lbrace \pi_r\rbrace$ be the **rest**, nonempty since $|B_r| \geq 2$.

**The slice.** For $S \subseteq [s]$ and $j \in [s]$ define the input $z_{S,j}$: each rest variable $v \in R_r$ is set to $[r \in S]$, and each pivot $\pi_r$ is set to $[r = j]$.

**Case A: $2H+1 \leq s$.**

**Value of $f$.** $T_r(z_{S,j}) = (\bigwedge_{v\in R_r} z_v)\wedge z_{\pi_r}$. The pivot factor is $[r=j]$, killing all $r \neq j$; for $r = j$ the rest conjunction is $[j \in S]$. By disjointness no variable is shared, so $f(z_{S,j}) = T_j(z_{S,j}) = [j \in S]$.

**Additive parametrization.** Splitting the affine sum into rest and pivot parts, $N_h(z_{S,j}) = \alpha_{h,S} + p_{h,\pi_j}$ with $\alpha_{h,S} = a_h + \sum_{r\in S} P_{h,r}$, $P_{h,r} = \sum_{v\in R_r} p_{h,v}$; and $D_h(z_{S,j}) = \beta_{h,S} + r_{h,\pi_j}$ with $\beta_{h,S} = b_h + \sum_{r\in S} R_{h,r}$, $R_{h,r} = \sum_{v\in R_r} r_{h,v}$. The only $S$-dependence is through the $2H+1$ numbers $(\theta, \alpha_{h,S}, \beta_{h,S})$.

**Parametric polynomials and Warren.** Let $w = (\theta, \alpha_1,\dots,\alpha_H, \beta_1,\dots,\beta_H) \in \mathbb{R}^{2H+1}$ and $Q_j(w) = \theta\prod_h(\beta_h + r_{h,\pi_j}) + \sum_h(\alpha_h + p_{h,\pi_j})\prod_{g\neq h}(\beta_g + r_{g,\pi_j})$, of degree $\leq H+1$ in $w$ (the constants $p_{h,\pi_j}, r_{h,\pi_j}$ are fixed). Then $Q_j(w_S) = P(z_{S,j})$ for $w_S = (\theta, \alpha_{h,S}, \beta_{h,S})$, so by strict sign-representation $\mathrm{sgn}\,Q_j(w_S) = [j\in S]$ ($\pm 1$). All $2^s$ subset-indicator sign vectors are realized over $\mathbb{R}^{2H+1}$. By Warren with $m = s$, $p = 2H+1$, $d = H+1$ ($m \geq p$ in Case A),

$$
2^s \leq \left(\frac{C(H+1)s}{2H+1}\right)^{2H+1}.
$$

Since $(H+1)/(2H+1) \leq 1$, taking $\log_2$ gives $s \leq (2H+1)\log_2(Cs) \leq (2H+1)\cdot 2\log_2 s$ for large $s$, so $H \geq s/(8\log_2 s)$.

**Case B: $2H+1 > s$.** Then $H > (s-1)/2 \geq s/(8\log_2 s)$ for large $s$.

In both cases $\mathrm{tChow}_{\pm}(f) = H \geq s/(8\log_2 s)$ (take $c = 1/8$), and $\mathrm{tChow}_{\pm} \leq H^{*}$ gives the same for $H^{*}$. $\blacksquare$

## Consequence

The bound is positivity-free and width-independent: only the number of terms $s$ and the disjoint, width-$\geq 2$ structure matter. Two readings:

- **A near-tight characterization.** For disjoint monotone DNFs, $s/(8\log_2 s) \leq H^{*}(f) \leq s$, so $H^{*}(f) = \widetilde{\Theta}(s)$. The monotone-DNF upper bound (L14) is essentially tight; the only slack is the $\log s$ factor. This is, after symmetric functions (L12), the second large nonsymmetric family whose head complexity is pinned down (here up to a $\log$).
- **The reusable technique.** The proof is the L35 "counting localized by a structured restriction" applied to a general disjoint DNF: choose a slice on which the row $S$ acts through $O(H)$ additive parameters yet must shatter $s$ columns, then invoke Warren. The same template will bound $H^{*}$ from below for any target admitting such a slice.
- **Open:** whether the $\log s$ factor is removable (is $H^{*}(f) = \Theta(s)$, e.g. for $\mathrm{INT}_n$?). The parameters $(\alpha_{h,S}, \beta_{h,S})$ are additive in $S$, a structure stronger than the bare $2H+1$-dimensional parametrization Warren uses; exploiting it is the route to closing the gap.
