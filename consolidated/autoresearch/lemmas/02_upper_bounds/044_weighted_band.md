# The Head Complexity of a Weighted Band Is Exactly Two

## Statement

Fix $w_1,\dots,w_n > 0$, let $t(x) = \sum_i w_i x_i$, and for $\theta_1 \leq \theta_2$ let the **weighted band** be $f(x) = \mathbf 1[\theta_1 \leq t(x) \leq \theta_2]$.

**(a)** $H^{*}(f) \leq 2$ for every weighted band.

**(b)** If there exist coordinates $i \neq j$ and an assignment of the others such that the four restricted values $t_{00} \leq t_{01}, t_{10} \leq t_{11}$ satisfy $t_{00} < \theta_1$, $\theta_1 \leq t_{01}, t_{10} \leq \theta_2$, and $t_{11} > \theta_2$, then $H^{*}(f) = 2$.

> The positive-weight, **nonsymmetric** generalization of the symmetric exact-count band $\mathrm{EXACT}_{n,k} = \mathbf 1[\lvert x\rvert = k]$ (which has $H^{*}=2$ by L12). A band is a function of one positive weighted sum with two sign changes, so two heads suffice (L25); and a proper band carries a checkerboard restriction — the two *middle* restricted values land in the band while the two *extremes* fall outside — forcing $H^{*} \geq 2$ (L3). This is a clean exact value for a nonsymmetric family, and the first exact value obtained by pairing the weighted-score upper bound (L25) with the checkerboard lower bound (L3).

## Proof

**(a)** $f(x) = F(t(x))$ with $F(s) = \mathbf 1[\theta_1 \leq s \leq \theta_2]$ and $t$ a positive weighted sum. Along the increasing order of $\mathrm{Im}(t)$, $F$ goes $0 \to 1 \to 0$ (or fewer pieces), so its sign-change count is $C(F) \leq 2$. By the weighted-score bound [025_weighted_score_upper.md](025_weighted_score_upper.md), $H^{*}(f) \leq C(F) \leq 2$.

**(b)** Restrict to $i, j$ with the others fixed as given. Since $w_i, w_j > 0$, $t_{00} \leq t_{01}, t_{10} \leq t_{11}$, and by the antipode identity ([002_antipode_identities.md](../01_foundations_and_normal_form/002_antipode_identities.md)) $t_{00} + t_{11} = t_{01} + t_{10}$. The hypotheses give $f(0,0) = \mathbf 1[t_{00}\in[\theta_1,\theta_2]] = 0$ (as $t_{00}<\theta_1$), $f(1,1) = 0$ (as $t_{11}>\theta_2$), and $f(0,1) = f(1,0) = 1$ (as $t_{01}, t_{10} \in [\theta_1,\theta_2]$). So the restriction is a 2-bit checkerboard ($0$ on $\lbrace(0,0),(1,1)\rbrace$, $1$ on $\lbrace(0,1),(1,0)\rbrace$); by the checkerboard obstruction ([003_checkerboard_obstruction.md](../01_foundations_and_normal_form/003_checkerboard_obstruction.md)), $H^{*}(f) \geq 2$. With (a), $H^{*}(f) = 2$. $\blacksquare$

## Consequence

Because $t$ is additive, only the *anti-diagonal-in-band* checkerboard can occur: an interval $[\theta_1,\theta_2]$ containing both extremes $t_{00}, t_{11}$ would contain everything between, so the band can never realize the diagonal pattern — the obstruction is intrinsic to bands. The condition in (b) holds for any band that excludes a low and a high value while including two incomparable middle ones, i.e. every "proper" weighted band; degenerate cases (empty band, half-line, or full cube) are linear-threshold ($H^{*}\leq 1$). This adds a nonsymmetric family to the exact-value catalog (after symmetric $f$, L12; single/perturbed products, L41/L42) and illustrates the upper-toolkit (L25) meeting the lower-toolkit (L3) at a tight value.
