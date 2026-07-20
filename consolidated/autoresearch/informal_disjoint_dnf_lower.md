# Problem: A near-linear lower bound on the head complexity of any disjoint monotone DNF

## Background and definitions (self-contained)

Let $s \geq 1$ and let $B_1, \dots, B_s$ be pairwise-disjoint nonempty sets of Boolean variables with $|B_r| \geq 2$ for every $r$. The **disjoint monotone DNF** they define is the function on $N = \sum_r |B_r|$ bits

$$
f = \bigvee_{r=1}^s T_r, \qquad T_r = \bigwedge_{v \in B_r} v ,
$$

so $T_r = 1$ iff every variable in block $B_r$ is $1$, and $f = 1$ iff some term is fully satisfied. (Set intersection $\mathrm{INT}_n$ is the special case of $s = n$ blocks each of size $2$.)

**The tangent-form normal form (established, L16/L18).** A function $A = a_0 + \sum_v a_v z_v$ over the $N$ variables $z$ is **affine**. For $H \geq 1$, $\mathrm{tChow}_{\pm}(g) \leq H$ means there are affine $N_1, D_1, \dots, N_H, D_H$ (arbitrary, no positivity) and $\theta \in \mathbb{R}$ with the **tangent form** $P = \theta\prod_{h=1}^H D_h + \sum_{h=1}^H N_h \prod_{g \neq h} D_g$ **strictly sign-representing** $g$ ($g = 1 \iff P > 0$). The sandwich gives $\mathrm{tChow}_{\pm}(g) \leq H^{*}(g)$, so any lower bound on $\mathrm{tChow}_{\pm}$ bounds $H^{*}$.

**External theorem (Warren; given).** There is an absolute $C \geq 1$ such that any $m \geq 1$ real polynomials in $p \geq 1$ variables of degree $\leq d$ realize at most $(Cdm/p)^p$ distinct sign vectors over $\mathbb{R}^p$, provided $m \geq p$.

## Claim to prove

There is an absolute constant $c > 0$ such that for every disjoint monotone DNF $f$ on $s$ terms each of width $\geq 2$, with $s$ large,

$$
H^{*}(f) \;\geq\; \mathrm{tChow}_{\pm}(f) \;\geq\; \frac{c\,s}{\log_2 s}.
$$

(Together with the monotone-term DNF upper bound $H^{*}(f) \leq s$, this pins $H^{*}(f) = \widetilde{\Theta}(s)$: the head complexity of a disjoint monotone DNF is its term count, up to a logarithmic factor.)

## Guidance (prove every step rigorously)

Fix a sign-representing tangent form of order $H = \mathrm{tChow}_{\pm}(f)$ with affine $N_h(z) = a_h + \sum_v p_{h,v} z_v$, $D_h(z) = b_h + \sum_v r_{h,v} z_v$, and scalar $\theta$. In each block $B_r$ pick a distinguished **pivot** variable $\pi_r \in B_r$ and let $R_r = B_r \setminus \lbrace \pi_r\rbrace$ be the **rest** ($|R_r| = |B_r| - 1 \geq 1$, nonempty since width $\geq 2$).

**The slice.** For $S \subseteq [s]$ and $j \in [s]$ define the input $z = z_{S,j}$ by:
- for every $r$ and every $v \in R_r$: set $z_v = 1$ if $r \in S$, else $z_v = 0$;
- for every $r$: set the pivot $z_{\pi_r} = 1$ if $r = j$, else $z_{\pi_r} = 0$.

**Case A: $2H + 1 \leq s$.** (Case B below handles $2H+1 > s$.)

1. **Value of $f$ on the slice.** $T_r(z_{S,j}) = \big(\bigwedge_{v \in R_r} z_v\big) \wedge z_{\pi_r}$. The pivot factor $z_{\pi_r} = [r = j]$, so $T_r = 0$ for $r \neq j$. For $r = j$, $\bigwedge_{v \in R_j} z_v = [j \in S]$ (all rest variables of block $j$ are $1$ iff $j \in S$), so $T_j = [j \in S]$. Hence $f(z_{S,j}) = \bigvee_r T_r = [j \in S]$. *(justification: a disjunction equals the single possibly-nonzero term; the AND of the rest equals $1$ iff all its bits are $1$.)*

2. **Affine forms are additive in $S$ plus a per-column constant.** Split the variable sum into rest and pivot parts. For the rest part, $\sum_{r}\sum_{v \in R_r} p_{h,v} z_v = \sum_{r \in S}\sum_{v \in R_r} p_{h,v} = \sum_{r \in S} P_{h,r}$ where $P_{h,r} := \sum_{v \in R_r} p_{h,v}$ is a constant. For the pivot part, $\sum_r p_{h,\pi_r} z_{\pi_r} = p_{h,\pi_j}$ (only $r = j$ contributes). So
   $$
   N_h(z_{S,j}) = \alpha_{h,S} + p_{h,\pi_j}, \qquad \alpha_{h,S} := a_h + \sum_{r \in S} P_{h,r},
   $$
   and similarly $D_h(z_{S,j}) = \beta_{h,S} + r_{h,\pi_j}$ with $\beta_{h,S} := b_h + \sum_{r \in S} R_{h,r}$, $R_{h,r} := \sum_{v \in R_r} r_{h,v}$. *(justification: the input is $1$ on the rest of block $r$ iff $r \in S$, and $1$ on pivot $r$ iff $r = j$; substitute into the affine forms.)*

3. **The restricted tangent value.** Therefore
   $$
   P(z_{S,j}) = \theta\prod_h(\beta_{h,S} + r_{h,\pi_j}) + \sum_h (\alpha_{h,S} + p_{h,\pi_j})\prod_{g \neq h}(\beta_{g,S} + r_{g,\pi_j}).
   $$
   *(justification: substitute Step 2 into the tangent form $P$.)*

4. **Parametric polynomials.** Let $w = (\theta, \alpha_1, \dots, \alpha_H, \beta_1, \dots, \beta_H) \in \mathbb{R}^{2H+1}$. For each column $j \in [s]$ define
   $$
   Q_j(w) = \theta\prod_h(\beta_h + r_{h,\pi_j}) + \sum_h (\alpha_h + p_{h,\pi_j})\prod_{g \neq h}(\beta_g + r_{g,\pi_j}),
   $$
   where the $p_{h,\pi_j}, r_{h,\pi_j}$ are fixed constants. Then $\deg Q_j \leq H+1$ (term $\theta\prod_h(\beta_h + \cdot)$ has degree $1 + H$; the others degree $H$). *(justification: degree of a product of affine factors; constants have degree $0$.)*

5. **All $2^s$ sign patterns occur.** Put $w_S = (\theta, \alpha_{h,S}, \beta_{h,S})$. Then $Q_j(w_S) = P(z_{S,j})$, and by Steps 1 and strict sign-representation $\mathrm{sgn}\,Q_j(w_S) = +1$ iff $j \in S$. As $S$ ranges over all subsets of $[s]$, the sign vectors $(\mathrm{sgn}\,Q_j(w_S))_j$ are the $2^s$ distinct $\pm 1$ indicators, all realized over $w \in \mathbb{R}^{2H+1}$. *(justification: distinct subsets give distinct indicator vectors; each realized by $w_S$.)*

6. **Warren.** With $m = s$, $p = 2H+1$, $d = H+1$ and $m \geq p$ (Case A): $2^s \leq (C(H+1)s/(2H+1))^{2H+1}$. Since $(H+1)/(2H+1) \leq 1$, $\log_2$ gives $s \leq (2H+1)\log_2(Cs)$. For large $s$, $\log_2(Cs) \leq 2\log_2 s$, so $2H+1 \geq s/(2\log_2 s)$, giving $H \geq s/(8\log_2 s)$. *(justification: Warren, then logarithm and rearrangement.)*

**Case B: $2H+1 > s$.** Then $H > (s-1)/2 \geq s/(8\log_2 s)$ for large $s$.

7. **Conclude.** In both cases $\mathrm{tChow}_{\pm}(f) = H \geq s/(8\log_2 s)$; take $c = 1/8$. Since $\mathrm{tChow}_{\pm} \leq H^{*}$, the same bound holds for $H^{*}(f)$. $\blacksquare$

## Pitfalls to address explicitly

- **Width $\geq 2$ is essential.** It guarantees each rest set $R_r$ is nonempty, so $\alpha_{h,S}$ genuinely depends on $S$ (via $P_{h,r} = \sum_{v \in R_r} p_{h,v}$). With width $1$, $f$ would be a single OR (an LTF, $H^{*} = 1$) and the slice would not shatter — the construction must use the rest variables to encode $S$.
- **Disjointness of blocks** is what makes $f(z_{S,j}) = [j \in S]$ exact: each $T_r$ sees only its own block, so setting pivot $j$ alone kills all other terms.
- The parameter count $2H+1$ is independent of $s$ and of the block widths: the row $S$ enters $P$ only through $(\theta, \alpha_{h,S}, \beta_{h,S})$. This "coefficient tying" is what makes Warren bite.
- Warren's hypothesis $m \geq s \geq p = 2H+1$ is Case A; the complement (Case B) is dispatched separately.
- **No positivity** is used; the bound is on $\mathrm{tChow}_{\pm}$, hence on $H^{*}$. This is the L35 ($\mathrm{INT}_n$) argument with general disjoint terms; it shows the monotone-term DNF upper bound $H^{*} \leq s$ (L14) is tight up to a $\log s$ factor on disjoint DNFs.
