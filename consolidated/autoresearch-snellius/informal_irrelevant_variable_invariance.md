# Irrelevant Variables Do Not Change Head Complexity

Let $H^{\ast}(f)$ denote the least number of heads in the one-layer attention model of `model.md` that computes $f$ by a strict final threshold. Equivalently, by Lemma 10, $H^{\ast}(f)$ is the least $H$ such that $f$ is sign-represented on the Boolean cube by

$$
\theta + \sum_{h=1}^{H} \phi_h(x),
$$

where each one-head atom has the form

$$
\phi_h(x)=\frac{\eta_h+\sum_{i=1}^{n}\rho_{hi}\alpha_h^{x_i}(m_{hi}+\delta_h x_i)}{\gamma_h+\sum_{i=1}^{n}\rho_{hi}\alpha_h^{x_i}},
$$

with $\gamma_h>0$, $\rho_{hi}>0$, and $\alpha_h>0$.

For any Boolean function $f:\{0,1\}^{n}\to\{0,1\}$ and any $m\geq 0$, define the dummy-variable extension

$$
\widetilde f:\{0,1\}^{n+m}\to\{0,1\},\qquad \widetilde f(x,z)=f(x).
$$

Then

$$
H^{\ast}(\widetilde f)=H^{\ast}(f).
$$

Moreover, for every permutation $\pi$ of the input coordinates,

$$
H^{\ast}(f\circ \pi)=H^{\ast}(f),
$$

and for the Boolean complement $1-f$,

$$
H^{\ast}(1-f)=H^{\ast}(f).
$$

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Permutation invariance + dummy lower bound: cite Lemma 26 directly (twice for permutation, once for dummy-lower) — do not re-prove.**
2. **Dummy upper bound:** strictify $c$ to a positive margin, then add each dummy coordinate to every atom with weight $\rho=\varepsilon$ and let $\varepsilon\to0^+$; uniform continuity on the finite cube preserves all signs.
3. **Complement:** negate the score $c+\sum\phi_h\mapsto -c+\sum(-\phi_h)$; invoke Lemma 13 to confirm each $-\phi_h$ stays an admissible atom; use the same margin perturbation to clear the strict-threshold boundary; finish by involution.
4. **Unifying tool to state once and reuse:** "on a finite cube a strict sign-representation has a positive margin, so small perturbations of $c$, of any $\rho_{hi}$, or of the score are sign-preserving" — this single lemma powers both (2) and (4) and is already implicit in Lemmas 18/29.
5. **Guardrail:** explicitly note that input-bit negation is excluded and is obstructed by the per-head shared $\alpha_h,\delta_h$ — keep it out of the statement and the proof.
