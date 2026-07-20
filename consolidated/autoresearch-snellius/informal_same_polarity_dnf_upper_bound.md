# Same-polarity DNF subcube upper bound

Work in the one-layer attention model of `model.md`, and let $H^{\ast}(f)$ be the least number of attention heads needed to compute $f : \{0,1\}^{n} \to \{0,1\}$ with a final strict threshold at the query token.

Fix a polarity $\zeta \in \{0,1\}$ and nonempty coordinate sets $A_1,\ldots,A_s \subseteq \{1,\ldots,n\}$. Define the same-polarity DNF

$$
f(x)=\bigvee_{r=1}^{s}\bigwedge_{i\in A_r}\mathbf{1}[x_i=\zeta].
$$

Then

$$
H^{\ast}(f)\leq s.
$$

Equivalently, any union of $s$ coordinate subcubes all anchored at the all-ones vertex, or all anchored at the all-zeros vertex, is computable with at most one head per subcube.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Work in the Lemma-10/13 normal form, not raw attention:** exhibit $s$ linear-fractional atoms (one per term) whose constant-plus-sum sign-represents $f$; then $H^\ast\le s$ is immediate from $H^\ast=L_{\mathrm{frac}}$. Cleanest rigorous path.
2. **Factor the proof into two reusable lemmas:** (a) one head realizes a single same-polarity subcube as a *one-sided bump* with explicit margin $[0,\epsilon]$ vs $\ge B$; (b) a strictly-thresholded sum of one-sided bumps computes their OR. Reuse (a) as the $s=1$ refinement of Lemma 4/11.
3. **Saturation gadget:** baseline = the query token carrying the "on" value $B$; any violated literal in $A_r$ pulls attention to a $0$-value position; take logit scale $L$ large — finiteness of the cube makes one $L$ separate all $2^n$ inputs (no exact hard attention needed).
4. **Guard the hypothesis:** the construction needs *within-term* single polarity (the sign of a head's $b_0-b_1$ gap is fixed); the target's common $\zeta$ is the clean monotone special case. Do not state a general "$H^\ast(f\vee g)\le H^\ast(f)+H^\ast(g)$" — it is false in general; one-sidedness is essential.
5. **Cross-check direction with Lemma 6/16:** $\deg_\pm(f)\le H^\ast(f)\le s$ should hold for these $f$ — a quick consistency sanity check, and a reminder that the term-count bound is generally loose versus threshold degree.
