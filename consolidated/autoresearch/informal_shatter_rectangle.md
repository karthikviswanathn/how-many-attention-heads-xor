# Problem: A reusable head-complexity lower bound from a shatter-rectangle

## Background and definitions (self-contained)

Work on $\lbrace 0,1\rbrace^N$ with coordinate set $[N]$. A function $A(z) = a_0 + \sum_{v\in[N]} a_v z_v$ is **affine**. For $H \geq 1$, $\mathrm{tChow}_{\pm}(g) \leq H$ means there are affine $N_1,D_1,\dots,N_H,D_H$ (arbitrary; no positivity) and $\theta\in\mathbb{R}$ such that the **tangent form** $P = \theta\prod_{h=1}^H D_h + \sum_{h=1}^H N_h\prod_{g\neq h}D_g$ strictly sign-represents $g$ ($g(z)=1\iff P(z)>0$). The head complexity obeys $\mathrm{tChow}_{\pm}(g)\leq H^{*}(g)$ (the sandwich), so a lower bound on $\mathrm{tChow}_{\pm}$ lower-bounds $H^{*}$.

**Definition (shatter-rectangle).** A function $g:\lbrace 0,1\rbrace^N\to\lbrace 0,1\rbrace$ **admits a shatter-rectangle of order $s$** if the coordinates partition as $[N] = V_{\mathrm{row}} \sqcup V_{\mathrm{col}}$ and there exist
- row assignments $\rho_S \in \lbrace 0,1\rbrace^{V_{\mathrm{row}}}$ for every $S\subseteq[s]$, and
- column assignments $\kappa_j \in \lbrace 0,1\rbrace^{V_{\mathrm{col}}}$ for every $j\in[s]$,

such that for all $S\subseteq[s]$ and $j\in[s]$, writing $(\rho_S,\kappa_j)$ for the full assignment that uses $\rho_S$ on $V_{\mathrm{row}}$ and $\kappa_j$ on $V_{\mathrm{col}}$,

$$
g(\rho_S,\kappa_j) = [\, j\in S\,].
$$

**External theorem (Warren; given).** There is an absolute $C\geq 1$ such that any $m\geq 1$ real polynomials in $p\geq 1$ variables of degree $\leq d$ realize at most $(Cdm/p)^p$ distinct sign vectors over $\mathbb{R}^p$, provided $m\geq p$.

## Claim to prove

There is an absolute constant $c>0$ such that: if $g$ admits a shatter-rectangle of order $s$ (with $s$ large), then

$$
H^{*}(g) \;\geq\; \mathrm{tChow}_{\pm}(g) \;\geq\; \frac{c\,s}{\log_2 s}.
$$

## Guidance (prove every step rigorously)

Fix a sign-representing tangent form of order $H=\mathrm{tChow}_{\pm}(g)$ with affine $N_h(z)=a_h+\sum_v p_{h,v}z_v$, $D_h(z)=b_h+\sum_v r_{h,v}z_v$, and scalar $\theta$.

**Case A: $2H+1\leq s$.**

1. **Each affine form splits into a row part and a column part.** For any affine $A(z)=a_0+\sum_v a_v z_v$,
   $$
   A(\rho_S,\kappa_j) = a_0 + \sum_{v\in V_{\mathrm{row}}} a_v (\rho_S)_v + \sum_{v\in V_{\mathrm{col}}} a_v (\kappa_j)_v,
   $$
   because $(\rho_S,\kappa_j)$ takes value $(\rho_S)_v$ on $V_{\mathrm{row}}$ and $(\kappa_j)_v$ on $V_{\mathrm{col}}$. The first two terms depend only on $S$; the last only on $j$. *(justification: $V_{\mathrm{row}}, V_{\mathrm{col}}$ partition $[N]$, so the affine sum splits.)*

2. **Row/column decomposition of the atoms.** Define $\alpha_{h,S} = a_h + \sum_{v\in V_{\mathrm{row}}} p_{h,v}(\rho_S)_v$ and $\mu_{h,j} = \sum_{v\in V_{\mathrm{col}}} p_{h,v}(\kappa_j)_v$; then $N_h(\rho_S,\kappa_j) = \alpha_{h,S} + \mu_{h,j}$. Likewise $\beta_{h,S} = b_h + \sum_{v\in V_{\mathrm{row}}} r_{h,v}(\rho_S)_v$ and $\nu_{h,j} = \sum_{v\in V_{\mathrm{col}}} r_{h,v}(\kappa_j)_v$ give $D_h(\rho_S,\kappa_j) = \beta_{h,S} + \nu_{h,j}$. *(justification: Step 1 applied to $N_h$ and $D_h$.)*

3. **Restricted tangent value.** Substituting Step 2 into $P$,
   $$
   P(\rho_S,\kappa_j) = \theta\prod_h(\beta_{h,S}+\nu_{h,j}) + \sum_h (\alpha_{h,S}+\mu_{h,j})\prod_{g\neq h}(\beta_{g,S}+\nu_{g,j}).
   $$
   *(justification: definition of $P$.)*

4. **A family of $s$ polynomials in $2H+1$ parameters.** Let $w=(\theta,\alpha_1,\dots,\alpha_H,\beta_1,\dots,\beta_H)\in\mathbb{R}^{2H+1}$ and, for each $j\in[s]$,
   $$
   Q_j(w) = \theta\prod_h(\beta_h+\nu_{h,j}) + \sum_h(\alpha_h+\mu_{h,j})\prod_{g\neq h}(\beta_g+\nu_{g,j}),
   $$
   where $\mu_{h,j},\nu_{h,j}$ are fixed constants. Then $\deg Q_j\leq H+1$: the term $\theta\prod_h(\beta_h+\nu_{h,j})$ is a product of the variable $\theta$ and $H$ degree-$1$ factors (degree $H+1$); each other summand is a product of $H$ degree-$1$ factors (degree $H$). *(justification: degree of a product; the $\mu,\nu$ are constants.)*

5. **All $2^s$ sign patterns are realized.** Put $w_S=(\theta,\alpha_{1,S},\dots,\alpha_{H,S},\beta_{1,S},\dots,\beta_{H,S})\in\mathbb{R}^{2H+1}$. Then $Q_j(w_S)=P(\rho_S,\kappa_j)$, so by the shatter-rectangle property and strict sign-representation, $\mathrm{sgn}\,Q_j(w_S)=+1$ if $j\in S$ and $-1$ if $j\notin S$. As $S$ ranges over all subsets of $[s]$, the sign vectors $(\mathrm{sgn}\,Q_j(w_S))_{j\in[s]}$ are the $2^s$ distinct $\pm 1$ indicators of subsets, all realized over $w\in\mathbb{R}^{2H+1}$. *(justification: distinct subsets give distinct indicator vectors; each is realized by its $w_S$.)*

6. **Warren.** With $m=s$ polynomials, $p=2H+1$ variables, degree $d=H+1$, and $m\geq p$ (Case A), at most $(C(H+1)s/(2H+1))^{2H+1}$ sign vectors occur. Hence $2^s\leq(C(H+1)s/(2H+1))^{2H+1}$. Since $(H+1)/(2H+1)\leq 1$, taking $\log_2$ gives $s\leq(2H+1)\log_2(Cs)$, and for large $s$, $\log_2(Cs)\leq 2\log_2 s$, so $2H+1\geq s/(2\log_2 s)$ and $H\geq s/(8\log_2 s)$. *(justification: Warren, logarithm, rearrangement.)*

**Case B: $2H+1>s$.** Then $H>(s-1)/2\geq s/(8\log_2 s)$ for large $s$.

7. **Conclude.** In both cases $\mathrm{tChow}_{\pm}(g)=H\geq s/(8\log_2 s)$; take $c=1/8$. Since $\mathrm{tChow}_{\pm}\leq H^{*}$, the same holds for $H^{*}(g)$. $\blacksquare$

## Pitfalls to address explicitly

- **The partition is what makes it work.** Because $V_{\mathrm{row}}$ and $V_{\mathrm{col}}$ partition the coordinates, every affine form splits into an $S$-only part plus a $j$-only part (Step 1); no additive/subset-sum structure on $\rho_S$ is needed — $\alpha_{h,S}$ is simply whatever real number the row part evaluates to. This is the minimal hypothesis.
- The row parameters collapse to $2H+1$ numbers $(\theta,\alpha_{h,S},\beta_{h,S})$ regardless of $|V_{\mathrm{row}}|$ or $s$; that bounded parameter count, against $s$ shattered columns, is the crux.
- Warren needs $m\geq p$ (Case A, $s\geq 2H+1$); the complement (Case B) is immediate.
- Sign-representation is strict, so all $2^s$ realized patterns are in $\lbrace -1,+1\rbrace^s$ (no zeros), and they are pairwise distinct.
- **No positivity** is used: the bound is on $\mathrm{tChow}_{\pm}$, hence on $H^{*}$. (Instances: $\mathrm{INT}_n$ with $V_{\mathrm{row}}=$ the $x$-coordinates, $\rho_S=\mathbf 1_S$, $V_{\mathrm{col}}=$ the $y$-coordinates, $\kappa_j=e_j$ gives order-$n$; a disjoint monotone DNF with $V_{\mathrm{row}}=$ the rests and $V_{\mathrm{col}}=$ the pivots gives order-$s$.)
