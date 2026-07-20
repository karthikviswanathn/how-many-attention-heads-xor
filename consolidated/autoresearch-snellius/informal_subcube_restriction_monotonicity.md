# Subcube Restriction Monotonicity

Let $f : \{0,1\}^{n} \to \{0,1\}$ be a Boolean function, and let $g : \{0,1\}^{m} \to \{0,1\}$ be obtained from $f$ by fixing any subset of the input coordinates to constants in $\{0,1\}$ and relabeling the remaining $m$ free coordinates. Here $H^{\ast}(h)$ denotes the minimum number of heads needed to compute $h$ in the one-layer attention model of `model.md`, equivalently the invariant $L_{\mathrm{frac}}(h)$ from Lemma 10. Then

$$
H^{\ast}(g) \leq H^{\ast}(f).
$$

In particular, every subcube restriction of $f$ gives a valid lower bound certificate for $f$: if $H^{\ast}(g) \geq r$, then $H^{\ast}(f) \geq r$.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Prove it as a corollary of Lemma 10**: restrict each atom, fold frozen terms into $\eta,\gamma$; the whole proof reduces to checking $\gamma'=\gamma+\sum_{i\notin S}\rho_i\alpha^{a_i}>0$. (Lowest-risk route.)
2. **State the abstract skeleton explicitly** ($\mathcal H(f)\subseteq\mathcal H(g)$, then min-over-superset) so the lemma reads as restriction-monotonicity, not an ad hoc computation; mirror Mathlib `Finset.min'_subset`/`IsMinOn.on_subset` if formalizing.
3. **Cross-check via Lemma 14** (cleared-denominator $D_h$ stays positive/admissible under fixing variables) for an independent confirmation that doesn't go through the fractional atoms.
4. **If a direct softmax proof is wanted**, use a dedicated query-token subspace to reproduce the frozen tokens' constant softmax contributions on the shorter $m{+}1$ sequence — but prefer lead #1.
5. **Frame as folklore**: cite restriction-monotonicity of $\deg_\pm$ (Minsky–Papert 1969; Sherstov) and the random-restriction method (Håstad 1986) as the standard analogues; note no prior work defines $H^\ast$, so this is an internal lemma, not a re-proof of known work.

## Known results to build on (from literature survey)

## Actionable leads

- **Prove it as a one-paragraph corollary of Lemma 10:** restrict each atom, fold fixed-coordinate terms into $\eta,\gamma$, check $\gamma'>0$ and surviving $\rho_i>0$ — atom count and threshold unchanged.
- **Use Lemma 13 as the bookkeeping** that the admissible denominator classes are closed under coordinate-fixing (the only nontrivial closure check).
- **Flag explicitly** that the raw softmax model resists a direct token-dropping simulation (fixed tokens carry constant normalization mass); $\gamma>0$ in the normal form is the slot that absorbs it — this is the crux, not the atom count.
- **Cash out the lower-bound corollary via parity:** combined with Lemma 8/12, $H^{\ast}(f)\ge k$ whenever some restriction of $f$ equals $\mathrm{XOR}_k$ — the model-native analogue of the Minsky–Papert "embed parity" threshold-degree bound, and a strict generalization of the Lemma 3 checkerboard obstruction.
- **Sanity-anchor on threshold degree:** $\deg_\pm$ is restriction-monotone by the same substitution argument, so the result is consistent with Lemma 6 and needs no new technique beyond it.
