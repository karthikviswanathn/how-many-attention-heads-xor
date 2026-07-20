# Problem: Positivity is free wherever threshold degree meets head complexity

## Background (self-contained)

$\deg_{\pm}(f)$ is the threshold degree; $H^{*}(f)$ is head complexity; $\mathrm{tChow}_{\pm}(f)$ is the tangential-Chow sign-rank with arbitrary affine factors (no positivity).

**Established (cite):** $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$ for every $f$ (the sandwich, L18).

## Claim to prove

For every $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$, if $\deg_{\pm}(f) = H^{*}(f)$ then

$$
\mathrm{tChow}_{\pm}(f) = H^{*}(f).
$$

Equivalently (contrapositive), if $\mathrm{tChow}_{\pm}(f) < H^{*}(f)$ (positivity strictly costs a head) then $\deg_{\pm}(f) < H^{*}(f)$ (a strict separation of head complexity from threshold degree). So **positivity can only ever cost on functions where $H^{*}$ strictly exceeds threshold degree.**

## Guidance (prove rigorously)

By the sandwich, $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$. If $\deg_{\pm}(f) = H^{*}(f)$, then both inequalities are equalities, so $\mathrm{tChow}_{\pm}(f) = H^{*}(f)$. For the contrapositive, if $\mathrm{tChow}_{\pm}(f) < H^{*}(f)$ then in particular $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) < H^{*}(f)$.

State the consequences: this single principle subsumes the level-one (L30) and symmetric (L31) cases (both have $\deg_{\pm} = H^{*}$), and shows the F4 gap question is confined to the separation regime $\deg_{\pm}(f) < H^{*}(f)$.

Give a complete, rigorous proof (it is a short sandwich-collapse argument).
