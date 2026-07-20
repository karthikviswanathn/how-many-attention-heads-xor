# Positivity Is Free for Symmetric Functions

## Statement

For every symmetric $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$ ($f(x) = F(|x|)$),

$$
\mathrm{tChow}_{\pm}(f) = H^{*}(f) = \deg_{\pm}(f) = C(F),
$$

where $C(F)$ is the sign-change count along the Hamming-weight axis. In particular $\mathrm{tChow}_{\pm}(f) = H^{*}(f)$: **the attention positivity/one-sided-slope constraints cost nothing on symmetric functions.**

> This extends the level-one base case [030_tchow_level1.md](030_tchow_level1.md) to the whole symmetric class, a partial answer to the open question whether positivity ever costs a head ($\mathrm{tChow}_{\pm} < H^{*}$). Combined with the empirical observation that $\mathrm{tChow}_{\pm} = H^{*}$ in every computed nonsymmetric case as well (`claude-comments/empirical_findings.md`), the evidence points toward positivity being free in general, though that remains open.

## Proof

By the symmetric characterization [012_symmetric_sign_changes.md](012_symmetric_sign_changes.md), $\deg_{\pm}(f) = C(F)$ (its Lemma 1) and $H^{*}(f) = C(F)$, so $\deg_{\pm}(f) = H^{*}(f) = C(F)$.

By the sandwich [018_tchow_sandwich.md](018_tchow_sandwich.md), $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$. Substituting gives $C(F) \leq \mathrm{tChow}_{\pm}(f) \leq C(F)$, so $\mathrm{tChow}_{\pm}(f) = C(F)$. Hence all four quantities coincide, and in particular $\mathrm{tChow}_{\pm}(f) = H^{*}(f)$. $\blacksquare$

## Consequence

Positivity is provably free wherever the sandwich $\deg_{\pm} \leq \mathrm{tChow}_{\pm} \leq H^{*}$ collapses, i.e. wherever $\deg_{\pm}(f) = H^{*}(f)$. By L11 (level $\leq 1$), L12 (symmetric), and L8 (parity) this includes a substantial range. The first place a gap $\mathrm{tChow}_{\pm} < H^{*}$ could appear is where $\deg_{\pm}(f) < H^{*}(f)$ strictly (a separation); the candidate $\neg\mathrm{DISJ}_4$ has $\deg_{\pm} = 2 < 3 = H^{*}$ but there $\mathrm{tChow}_{\pm} = H^{*} = 3$ too (computational), so even there positivity appears free. Whether $\mathrm{tChow}_{\pm} = H^{*}$ for all $f$ is the open F4 question.
