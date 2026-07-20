## Survey: Subcube Restriction Monotonicity of $H^{\ast}$

### What kind of statement this is

The target is a **restriction-closure (restriction-monotonicity) property of a complexity measure**: fixing input coordinates to constants (passing to a subcube) cannot increase the measure. This is one of the most universal structural facts in Boolean-function complexity, and the "in particular" clause — a hard restriction certifies a lower bound — is the standard reason one cares about it. The content here is entirely about the *specific* invariant $H^{\ast}=L_{\mathrm{frac}}$; the general phenomenon is folklore.

### Known mathematics in the external literature

**Restriction monotonicity is essentially universal.** For every natural Boolean complexity measure $M$, one has $M(f|_\rho)\le M(f)$ for any partial assignment (restriction) $\rho$. This holds for circuit size, formula size, decision-tree depth, certificate/sensitivity/block-sensitivity, real degree, **threshold (sign) degree**, approximate degree, sign-rank, and PAC/communication-derived measures. The proof is always the same trivial *substitution* argument: take any object representing $f$ (polynomial, circuit, protocol, normal form), substitute the fixed constants, and observe the resource does not grow. This is so standard it is usually asserted without proof; see O'Donnell, *Analysis of Boolean Functions* (2014), the material on restrictions.

**The closest analogue — threshold degree — is already in your stack.** Lemma 6 gives $\deg_\pm(f)\le H^{\ast}(f)$, and $\deg_\pm$ is itself restriction-monotone by exactly the substitution argument (plug the fixed values into a sign-representing polynomial; degree only drops). Restrictions are in fact *the* canonical lower-bound tool for threshold degree: you prove $\deg_\pm(f)$ is large by exhibiting a restriction equal to a known-hard function (parity, ODD-MAX-BIT). Canonical references: Minsky & Papert, *Perceptrons* (1969); Aspnes–Beigel–Furst–Rudich, "The expressive power of voting polynomials" (Combinatorica 1994); Sherstov's threshold-degree / pattern-matrix papers (≈2008–2013). So restriction-monotonicity of $H^{\ast}$ is fully consistent with — and strictly upstream of — the route you already use.

**The "method of restrictions" is the broader context.** Subbotovskaya (1961, formula shrinkage) and the AC$^0$ switching-lemma line — Ajtai (1983), Furst–Saxe–Sipser (1984), Håstad (1986) — are about *random* restrictions causing complexity to collapse; the trivial per-restriction monotonicity is the underpinning that makes "restrict to simplify, then lower-bound the restriction" sound. Not needed for the proof, but it is the genealogy of the "in particular" clause.

**(Lower confidence, tangential.)** In universal algebra, restriction is a special case of the *minor* quasi-order on finite functions (substitute variables by variables/constants); measures monotone under minors are studied by Pippenger, "Galois theory for minors of finite functions" (Discrete Math. 2002) and Couceiro–Pouzet. Probably too abstract to use here; mentioned only for completeness.

**Is the target itself in the literature?** Almost certainly not — the model and $H^{\ast}$ are bespoke to this project. The transformer-expressivity literature (Merrill–Sabharwal, Hahn, et al. on what one-layer / bounded attention can compute) studies different questions and does not give this. Treat the external literature as supplying *analogy and technique*, not the result.

### Status inside the project (most important)

The target is **not separately proved** in Lemmas 1–25, but it is an **immediate corollary of Lemma 10** (the linear-fractional normal form), which is exactly why the statement is phrased via $L_{\mathrm{frac}}$. The mechanism: each one-head atom
$$\phi(x)=\frac{\eta+\sum_i \rho_i\,\alpha^{x_i}(m_i+\delta x_i)}{\gamma+\sum_i \rho_i\,\alpha^{x_i}},\qquad \gamma>0,\ \rho_i>0,\ \alpha>0,$$
under fixing $x_i=c_i$ has its $i$-th terms become *constants* ($\alpha^{x_i}\!\to\!\alpha^{c_i}$), which fold into $\eta$ and $\gamma$. The new $\gamma'=\gamma+\sum_{i\in S}\rho_i\alpha^{c_i}>0$ and the surviving $\rho_i>0$ are preserved, so each atom restricts to a *valid atom on the $m$ free coordinates*, the atom count is unchanged, and the threshold is unchanged. Hence $L_{\mathrm{frac}}(g)\le L_{\mathrm{frac}}(f)$. Lemma 13's dictionary is the clean way to confirm the one thing that must be checked: the admissible denominator classes (constant-positive / all-positive-coeff / all-negative-coeff-with-positive-all-ones) are each **closed under coordinate-fixing**.

**The one genuinely non-trivial point** — worth flagging to the lead — is *why you must go through the normal form rather than the raw model*. A naive simulation that simply "drops" the fixed tokens fails: those tokens contribute constant mass to each head's softmax **denominator (normalization)**, and removing them changes every attention weight nonlinearly. The raw `model.md` softmax has no constant-bias / extra-token slot to reabsorb that mass. Lemma 10's free positive constant $\gamma$ is *precisely* that slot, which is what makes the restriction argument trivial in normal form and awkward without it. So: route through Lemma 10 (equivalence, both directions, so the restricted normal form re-realizes as an actual $m$-token model), not through a direct embedding.

**Coherence checks.** "Relabeling the $m$ free coordinates" is free: positional embeddings $p_i$ are arbitrary, so $H^{\ast}$ is permutation-invariant in the inputs. Edge case $m=0$: $g$ constant, $H^{\ast}(g)=0$ (Lemma 11) $\le H^{\ast}(f)$. The result also *subsumes the spirit of Lemma 3*: the checkerboard obstruction is the $2$-bit-restriction instance ("some restriction equals $\mathrm{XOR}_2$, and $H^{\ast}(\mathrm{XOR}_2)=2$"), proved there by hand.

### On the Mathlib hits

These are **not on point** and can largely be ignored: `Finset.restrict₂`, `Subtype.restrict`, `Profinite…ProjRestrict`, etc. are generic function-restriction plumbing, and `Composition.monotone_sizeUpTo` / the `@[mono]` attribute are generic monotonicity — none capture a complexity measure or this model. The one mildly relevant pair is `AffineMap.comp` / `Polynomial.natDegree_comp`: they encode "substituting constants is composition that does not raise affine/degree structure," which is the same elementary fact powering the absorption step (affine numerator/denominator stay affine after fixing a coordinate). This is an *analogy*, not a usable lemma — Mathlib has neither the attention model nor $H^{\ast}$.

### Confidence

High that restriction-monotonicity is a universal, near-trivial property for substitution-representable measures and that $H^{\ast}$ inherits it via Lemma 10. High that the target is not pre-proved as a standalone lemma but is a short corollary. Medium-high on the specific external citations/dates (Subbotovskaya 1961, Minsky–Papert 1969, Håstad 1986, ABFR 1994 — standard, but verify exact venues before citing in a write-up). Low/flagged on the universal-algebra "minors" framing.

## Actionable leads

- **Prove it as a one-paragraph corollary of Lemma 10:** restrict each atom, fold fixed-coordinate terms into $\eta,\gamma$, check $\gamma'>0$ and surviving $\rho_i>0$ — atom count and threshold unchanged.
- **Use Lemma 13 as the bookkeeping** that the admissible denominator classes are closed under coordinate-fixing (the only nontrivial closure check).
- **Flag explicitly** that the raw softmax model resists a direct token-dropping simulation (fixed tokens carry constant normalization mass); $\gamma>0$ in the normal form is the slot that absorbs it — this is the crux, not the atom count.
- **Cash out the lower-bound corollary via parity:** combined with Lemma 8/12, $H^{\ast}(f)\ge k$ whenever some restriction of $f$ equals $\mathrm{XOR}_k$ — the model-native analogue of the Minsky–Papert "embed parity" threshold-degree bound, and a strict generalization of the Lemma 3 checkerboard obstruction.
- **Sanity-anchor on threshold degree:** $\deg_\pm$ is restriction-monotone by the same substitution argument, so the result is consistent with Lemma 6 and needs no new technique beyond it.
