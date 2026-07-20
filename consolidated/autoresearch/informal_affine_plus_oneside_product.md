# Problem: sign(A·B + g) with A one-sided has head complexity at most two

## Background and definitions (self-contained)

Work on $\lbrace 0,1\rbrace^n$. An **affine** form is $C(x) = c_0 + \sum_i c_i x_i$, slopes $(c_1,\dots,c_n)$; it is **one-sided** if its slopes are all $\geq 0$ or all $\leq 0$. An affine $E$ is **admissible** if $E(x) > 0$ on the whole cube and its slopes are one-sided. An **order-2 tangent form** is $E_1 K_1 + E_2 K_2$ for affine $E_1,E_2,K_1,K_2$ (equivalently $\theta E_1 E_2 + N_1 E_2 + N_2 E_1$). $H^{*}(f) \leq 2$ iff some order-2 tangent form with $E_1,E_2$ **admissible** strictly sign-represents $f$ ($f(x)=1\iff P(x)>0$, $f(x)=0\iff P(x)<0$, $P\neq0$ on the cube).

## Claim to prove

Let $A$ be a **one-sided** affine form, $B$ and $g$ arbitrary affine forms, and suppose $q := A B + g$ satisfies $q(x)\neq 0$ for all $x\in\lbrace0,1\rbrace^n$. Let $f = \mathbf 1[\,q>0\,]$. Then

$$
H^{*}(f) \leq 2.
$$

(This extends "sign of a product of two affine forms has $H^{*}\leq2$" by an arbitrary affine perturbation $g$, at the cost of requiring $A$ one-sided; equivalently it covers order-2 witnesses whose pencil is $\lbrace A, 1\rbrace$.)

## Guidance (prove every step rigorously)

Write $A = a_0 + \sum_i a_i x_i$ with all $a_i$ of one sign; WLOG (negate $A$ and $B$ together, which leaves $AB$ unchanged) assume all $a_i \geq 0$. The goal is to exhibit admissible $E_1, E_2$ and affine $K_1, K_2$ with $E_1 K_1 + E_2 K_2 = q = AB + g$ on the cube.

1. **Two proportional one-sided denominators differing by $A$.** Fix a parameter $\nu > 0$ and constants to be chosen; set
   $$
   E_1 = c_1 + (1+\nu)\sum_i a_i x_i, \qquad E_2 = c_2 + \nu\sum_i a_i x_i,
   $$
   so both have slopes $\geq 0$ (one-sided), and $E_1 - E_2 = (c_1 - c_2) + \sum_i a_i x_i = A$ provided $c_1 - c_2 = a_0$. Choosing $c_2 > 0$ large enough (and $c_1 = c_2 + a_0$) makes $E_1, E_2 > 0$ on the cube, hence **admissible**. *(justification: a $\geq0$-slope affine attains its cube-minimum at $x=0$, equal to its constant term.)*

2. **Match the target with affine numerators.** Seek $K_1, K_2$ affine with $E_1 K_1 + E_2 K_2 = AB + g$. Write $K_1 = B + u$, $K_2 = -B + w$ for affine corrections $u, w$ to be determined (so the leading $B$-parts give $(E_1 - E_2)B = AB$):
   $$
   E_1 K_1 + E_2 K_2 = (E_1 - E_2)B + E_1 u + E_2 w = AB + (E_1 u + E_2 w).
   $$
   It remains to solve $E_1 u + E_2 w = g$ for affine $u, w$. *(justification: substitute and use $E_1 - E_2 = A$.)*

3. **Solve $E_1 u + E_2 w = g$.** Since $g$ is affine and $E_1, E_2$ are positive affine forms, take $u = \lambda$, $w = \mu$ to be **constants** first: $E_1\lambda + E_2\mu = \lambda(c_1 + (1+\nu)S) + \mu(c_2 + \nu S)$ where $S = \sum_i a_i x_i$. This equals $(\lambda c_1 + \mu c_2) + (\lambda(1+\nu)+\mu\nu)S$. To represent a general affine $g = g_0 + \sum_i g_i x_i$, note $g$ need not be a multiple of $S$; therefore allow $u, w$ to be **affine** (not just constant): the map $(u,w)\mapsto E_1 u + E_2 w$ from pairs of affine forms ($2(n+1)$ parameters) to affine forms ($n+1$ outputs) is **surjective** — e.g. since $E_2$ has a nonzero constant ($c_2>0$), $w = g/c_2$-style adjustment plus $u$ corrects the slopes; give the explicit linear-algebra argument that this map is onto the space of affine forms (it suffices that $E_1, E_2$ are not proportional as affine forms, OR that one of them is a positive constant-dominated form so $E_2 w$ alone can hit any affine $g$ up to a correction absorbable by $E_1 u$). Conclude affine $u, w$ exist with $E_1 u + E_2 w = g$.
   *(Be careful and rigorous here: state precisely why $E_1 u + E_2 w$ ranges over all affine forms as $u, w$ range over affine forms. If $E_1, E_2$ are proportional affine forms the map is not surjective — so ensure the chosen $E_1, E_2$ are non-proportional; with $c_1\neq$ a scalar multiple making them proportional, e.g. pick $\nu$ and $c_2$ so that $E_1, E_2$ are linearly independent affine forms, which holds generically.)*

4. **Assemble.** With such $u, w$, $E_1 K_1 + E_2 K_2 = AB + g = q$ on the cube, $E_1, E_2$ admissible, $K_1 = B+u$, $K_2 = -B+w$ affine. Since $q\neq0$ on the cube, this order-2 admissible tangent form strictly sign-represents $f$. Hence $H^{*}(f)\leq2$. $\blacksquare$

## Pitfalls

- The reduction $E_1 - E_2 = A$ needs $A$ **one-sided** so that $E_1, E_2$ (which carry $A$'s slopes scaled by $1+\nu$ and $\nu$) are both one-sided; this is exactly where the hypothesis is used. (For two-sided $A$ this proportional construction fails — that is the genuine open case.)
- The crux is Step 3: prove rigorously that $\lbrace E_1 u + E_2 w : u,w \text{ affine}\rbrace$ is all affine forms, i.e. the two admissible denominators are chosen linearly independent as affine forms. Verify non-proportionality.
- Numerators $K_1, K_2$ are affine; no quadratic numerator is needed (order-2 is genuine).
- Use $q\neq0$ on the cube for strictness.
