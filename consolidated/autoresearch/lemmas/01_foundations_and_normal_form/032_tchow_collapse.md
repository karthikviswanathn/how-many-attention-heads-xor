# Positivity Can Only Cost Where Head Complexity Exceeds Threshold Degree

## Statement

For every $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$,

$$
\deg_{\pm}(f) = H^{*}(f) \;\Longrightarrow\; \mathrm{tChow}_{\pm}(f) = H^{*}(f).
$$

Equivalently (contrapositive): if positivity strictly costs a head, $\mathrm{tChow}_{\pm}(f) < H^{*}(f)$, then $\deg_{\pm}(f) < H^{*}(f)$ (a strict separation of head complexity from threshold degree).

> So the F4 question "does positivity cost?" is **confined to the separation regime** $\deg_{\pm}(f) < H^{*}(f)$. On every function where threshold degree already equals head complexity — constants, LTFs (L11), symmetric functions (L12, L31), parity (L8) — positivity is free. This single principle subsumes the level-one and symmetric base cases.

## Proof

By the sandwich [018_tchow_sandwich.md](018_tchow_sandwich.md), $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$. If $\deg_{\pm}(f) = H^{*}(f)$, both inequalities are equalities, so $\mathrm{tChow}_{\pm}(f) = H^{*}(f)$. The contrapositive is immediate: $\mathrm{tChow}_{\pm}(f) < H^{*}(f)$ forces $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) < H^{*}(f)$. $\blacksquare$

## Consequence

Combined with the empirical observation that $\mathrm{tChow}_{\pm} = H^{*}$ even on the separation candidate $\neg\mathrm{DISJ}_4$ (where $\deg_{\pm} = 2 < 3 = H^{*}$), there is currently **no known function on which positivity costs anything**. Whether positivity is free in general ($\mathrm{tChow}_{\pm} = H^{*}$ everywhere, which would identify $H^{*}$ with the standard unconstrained tangential-Chow rank) is the open F4 question; by this lemma, any counterexample must first be a separation $\deg_{\pm}(f) < H^{*}(f)$.
