# A One-Sided Product Plus an Affine Perturbation Has Head Complexity at Most Two

## Statement

Let $A$ be a **one-sided** affine form (all slopes $\geq 0$ or all $\leq 0$), let $B, g$ be arbitrary affine forms, and suppose $q := AB + g$ satisfies $q(x) \neq 0$ for all $x \in \lbrace 0,1\rbrace^n$. Then for $f = \mathbf 1[\,q > 0\,]$,

$$
H^{*}(f) \leq 2.
$$

> Extends [041_product_two_affine.md](041_product_two_affine.md) ($\mathrm{sign}(AB)$, $H^{*}\leq 2$) by an arbitrary affine perturbation $g$, at the cost of one-sidedness of $A$. Equivalently it covers every order-2 $\mathrm{tChow}_{\pm}$ witness whose denominator pencil is $\lbrace A, 1\rbrace$ (which contains the positive form $1$, so it is in the "same-sign" regime $0\notin\mathrm{conv}\lbrace v_x\rbrace$): such witnesses are admissibly realizable for **all** $n$. The construction is the difference split refined so the two admissible denominators are *non-proportional*, letting their numerators absorb the affine perturbation $g$.

## Proof

WLOG (negating $A$ and $B$ together leaves $AB$ unchanged) assume $A = a_0 + \sum_i a_i x_i$ with all $a_i \geq 0$. Fix $\nu > 0$, choose $c_2 > 0$ large, set $c_1 = c_2 + a_0$, and define
$$
E_1 = c_1 + (1+\nu)\textstyle\sum_i a_i x_i, \qquad E_2 = c_2 + \nu\textstyle\sum_i a_i x_i .
$$
Both have nonnegative (one-sided) slopes; their cube-minimum is at $x=0$, equal to $c_1, c_2 > 0$ (for $c_2$ large enough $c_1 = c_2 + a_0 > 0$), so $E_1, E_2$ are **admissible**. Their difference is $E_1 - E_2 = (c_1 - c_2) + \sum_i a_i x_i = a_0 + \sum_i a_i x_i = A$. Choosing $\nu$ so that $E_1, E_2$ are not proportional as affine forms (generic $\nu$; they are proportional only for special parameter coincidences), the linear map $(u,w) \mapsto E_1 u + E_2 w$ from pairs of affine forms to affine forms is **surjective** (its image contains $E_2\cdot\mathrm{affine}$, and $E_1, E_2$ independent affine forms let the pair hit every affine target — a finite linear system that is solvable). So pick affine $u, w$ with $E_1 u + E_2 w = g$.

Set $K_1 = B + u$, $K_2 = -B + w$ (affine). Then on the cube
$$
P := E_1 K_1 + E_2 K_2 = (E_1 - E_2)B + (E_1 u + E_2 w) = AB + g = q .
$$
Since $q \neq 0$ on the cube, $P = q$ is nonzero everywhere and $f(x) = 1 \iff P(x) > 0$, $f(x) = 0 \iff P(x) < 0$. Thus the order-2 tangent form $P = E_1 K_1 + E_2 K_2$, with admissible denominators $E_1, E_2$, strictly sign-represents $f$, giving $H^{*}(f) \leq 2$. $\blacksquare$

## Consequence

With $H^{*}(f) \geq 2$ for non-LTF $f$ (L11), every non-LTF $f = \mathbf 1[AB+g>0]$ with $A$ one-sided has $H^{*}(f) = 2$ exactly. This is a rigorous, all-$n$ piece of the order-2 positivity-free question (F4): it disposes of the same-sign regime for the structured pencil $\lbrace A,1\rbrace$. The genuinely hard residual case is a *two-sided* rank-2 off-diagonal in the $0\in\mathrm{conv}$ regime, where the proportional construction fails and the obstruction is a topological covering statement (see `claude-comments/h_star_knowledge_map.md` §6, L40).
