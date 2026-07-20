# The Flattening Bound Holds Without Positivity

## Statement

With $\mathrm{sr}_{A|B}(f)$ the cut sign-rank (as in [022_flattening_lower_bound.md](022_flattening_lower_bound.md)) and $\mathrm{tChow}_{\pm}(f)$ the tangential-Chow sign-rank with *arbitrary* affine factors ([018_tchow_sandwich.md](../01_foundations_and_normal_form/018_tchow_sandwich.md)),

$$
\mathrm{sr}_{A|B}(f) \;\leq\; \big(\mathrm{tChow}_{\pm}(f)+1\big)\,2^{\mathrm{tChow}_{\pm}(f)} + 1,
\qquad\text{hence}\qquad
\mathrm{tChow}_{\pm}(f) = \Omega\big(\log \mathrm{sr}_{A|B}(f)\big).
$$

> The flattening / sign-rank lower bound never uses positivity: it bounds the unconstrained $\mathrm{tChow}_{\pm}$, not just $H^{*}$. So, like the counting separation [024_tchow_separation.md](024_tchow_separation.md), the sign-rank obstruction is not caused by the attention positivity/one-sided constraints. Via $\mathrm{tChow}_{\pm} \leq H^{*}$ this re-proves L22.

## Proof

Let $H = \mathrm{tChow}_{\pm}(f)$ with arbitrary affine witnesses $N_h, D_h$, $\theta$, and $P$ sign-representing $f$. An affine form has cut-rank $\leq 2$, and by Hadamard rank submultiplicativity ($M_{gg'} = M_g \circ M_{g'}$, $\mathrm{rank}(M\circ M') \leq \mathrm{rank}(M)\mathrm{rank}(M')$), $M_{\prod_h D_h}$ has rank $\leq 2^H$ and each $M_{N_h\prod_{g\neq h}D_g}$ has rank $\leq 2\cdot 2^{H-1} = 2^H$. So $\mathrm{rank}(M_P) \leq (H+1)2^H$. If $f$ is non-constant, with $p_+ = \min\lbrace P : f=1\rbrace > 0$ and $\nu \in (0, p_+)$, $R = M_P - \nu J$ strictly sign-represents $f$ with rank $\leq (H+1)2^H + 1$. Hence $\mathrm{sr}_{A|B}(f) \leq (H+1)2^H + 1$, and the logarithmic form follows as in L22. $\blacksquare$

## Consequence

Both general lower bounds proved in this project that beat threshold degree — flattening (L22) and counting (L23) — apply already to $\mathrm{tChow}_{\pm}$. Combined with the empirical observation that $\mathrm{tChow}_{\pm} = H^{*}$ in every computed case (see `claude-comments/empirical_findings.md`), this is further evidence that the attention positivity constraints add no lower-bound power, and possibly no power at all (the open F4 question of whether $\mathrm{tChow}_{\pm} = H^{*}$).
