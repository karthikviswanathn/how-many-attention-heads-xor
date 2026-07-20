## Survey: the cleared-denominator invariant $\mathrm{MFdeg}_\pm(f)$

**Bottom line up front.** This target is not a new theorem — it is the **cleared-denominator restatement of Lemma 10 (linear-fractional normal form), made into a strict two-sided sign-representation, with the atom dictionary supplied by Lemma 13.** Both prerequisites are already in the verified stack (Lemma 13 was committed in autoresearch iter 1, "verified"). Lemma 13's own *Consequence* section already writes down the exact clearing identity in the target and labels it "the dictionary input for the cleared-denominator invariant frontier node." So the heavy lifting (softmax → linear-fractional atom; affine dictionary; denominator trichotomy; converse realizability) is **done**. The lead should treat this as a corollary, not re-derive Lemma 10. Confidence: high.

### What the target actually is

$\mathrm{MFdeg}_\pm(f)$ is the minimum $H$ for which a **structured rational sign-representation**
$$\theta + \sum_{h=1}^H \frac{N_h(x)}{D_h(x)} \;>\;0 \iff f(x)=1$$
exists with admissible $(N_h,D_h)$, written after clearing the common denominator $\prod_h D_h$. The polynomial $P(x)=\theta\prod_h D_h+\sum_h N_h\prod_{g\ne h}D_g$ is exactly the numerator of that expression over the common denominator — standard partial-fraction/common-denominator recombination, with the $\prod_{g\ne h}D_g$ playing the role of cofactors. Nothing exotic in the algebra.

The equivalence with $H^*$ runs entirely through internal lemmas:
- **$\mathrm{MFdeg}_\pm(f)\le H^*(f)$:** Lemma 10 gives $H^*$ atoms $\phi_h=N_h/D_h$ + constant $c$ with $f=1\iff c+\sum\phi_h>0$; Lemma 13 certifies each $(N_h,D_h)$ admissible; clear denominators (Lemma 13 *Consequence*); perturb $c$ to get strictness on the $0$-side.
- **$H^*(f)\le\mathrm{MFdeg}_\pm(f)$:** divide $P$ by the positive $\prod_h D_h$ to recover Lemma 10's normal form; Lemma 13's converse realizes each admissible atom by one head.

### The known mathematics that does the gluing

Only three elementary facts are load-bearing, and none requires external literature:

1. **Product of positives is positive ⇒ sign-invariance of clearing.** $\prod_h D_h(x)>0$ on the cube because each $D_h(x)>0$ (admissibility). Multiplying/dividing the threshold expression by it cannot flip any sign. This is the single mathematical engine. **Mathlib: `Finset.prod_pos`** (`Mathlib.Algebra.Order.BigOperators.Ring.Finset`) is exactly this; `sign_mul` (`Mathlib.Data.Sign.Basic`, $\mathrm{sign}(xy)=\mathrm{sign}(x)\mathrm{sign}(y)$) is the supporting sign-bookkeeping lemma. (`finprod_nonneg` is the non-strict variant — less apt, you want strict.)

2. **Strict separation on a finite set via a margin.** Lemma 10 gives a *one-sided* `iff` ($f=0\Rightarrow$ score $\le 0$); the target wants strict $P<0$. Standard fix: the cube is finite, so the positive scores have a minimum margin $m>0$; perturbing the constant $c\to c-\epsilon$ with $0<\epsilon<m$ makes the $0$-side strictly negative without flipping any $1$-point. This is folklore (the same $\epsilon$-margin argument behind "a weak separator on a finite set can be strengthened to a strict one"). Perturbing only the global constant leaves every $(N_h,D_h)$ — hence admissibility and the shape of $P$ — untouched.

3. **Common-denominator algebra.** The recombination $\sum_h N_h/D_h \to (\sum_h N_h\prod_{g\ne h}D_g)/\prod_h D_h$ is just partial fractions in reverse; the cleared numerator has the exact stated form.

### External landscape (orientation only — the proof needs none of it)

- **Threshold degree / PTFs — Minsky & Papert, *Perceptrons* (1969).** The ambient notion: minimum degree of a polynomial sign-representing $f$. Relevant because the cleared $P$ is a product of $H$ affine factors per term, so $\deg P\le H$. Thus a degree-$\le H$ polynomial sign-represents $f$, **re-proving Lemma 6 ($\deg_\pm(f)\le H^*(f)$)** as a free consequence. This places the new invariant in the chain $\deg_\pm(f)\le \mathrm{MFdeg}_\pm(f)=H^*(f)$.
- **Rational degree of Boolean functions — Iyer, Jain, Kothari, Kovács-Deák, Kumar, Schaeffer, Wang, Whitmeyer (2023), arXiv:2310.08004** (already in `literature_survey.md`). This is the *closest external invariant*: $\mathrm{MFdeg}_\pm$ is literally sign-representation by a sum of $H$ affine ratios, i.e. a structured rational function of degree $\le H$. Their rational degree $\mathrm{rdeg}_\pm$ is the unstructured single-ratio analogue, so $\mathrm{rdeg}_\pm(f)\le H^*(f)$ — meaning **rational-degree lower bounds transfer to head-complexity lower bounds.** Useful downstream, not for this proof.
- **Sign-representation by rational functions — Beigel, Reingold, Spielman (≈1991, "PP is closed under intersection") and Beigel's PP/rational-function line.** The "sum of fractions over a common denominator, then threshold" pattern is the classical PP/rational-function device. *(Medium confidence on exact titles/dates; flagged as recollection.)*
- **Newman (1964), rational approximation of $|x|$** — origin of "rationals can be more powerful than polynomials of the same degree." Tangential; explains why a *fractional* invariant can sit strictly above $\deg_\pm$ while still equalling $H^*$.

### Caveats / things to verify before formalizing

- **Definitional ambiguity in "admissible" — the most important caveat.** The target's prose says $D$ "has all nonzero coordinate coefficients positive [resp. negative]." Lemma 13's actual classes are stronger: *all* coordinate coefficients positive (class 2) or *all* negative (class 3) — no mixing with zero coefficients. A single head cannot zero out one coordinate's denominator coefficient while keeping another nonzero (it would force the shared $\alpha=1$, killing *all* of them). So a "mixed-zero" denominator is **not** one-head-realizable. If admissibility is read loosely (allowing mixed zeros), the reverse direction $H^*\le\mathrm{MFdeg}_\pm$ can fail. **Bind "admissible" to Lemma 13's exact three classes** (the target's opening clause "exactly one of the affine one-head pairs from Lemma 13" is the intended, correct definition; the elaboration is loose). Under the strict reading the theorem is true.
- **$H=0$ base case.** Empty product $=1$, empty sum $=0$, so $P\equiv\theta$. Strictness forces $\theta\ne 0$; sign of $\theta$ picks the constant function. Matches Lemma 11 ($H^*=0\iff f$ constant). Worth stating $\theta\ne0$ explicitly.
- **Direction of strictness in the reverse implication.** A strict sign-rep gives $P(x)\ne0$ everywhere, so dividing by $\prod D_h>0$ yields a clean two-sided `iff`, matching Lemma 10 exactly — no extra perturbation needed going this way.

### Mathlib hits triage

- **Use:** `Finset.prod_pos` (central — $\prod_h D_h(x)>0$); `sign_mul` (sign-of-product bookkeeping). `mul_pos` for the two-factor base case if induction is preferred over the Finset form.
- **Ignore:** the affine-combination / simplex hits (`fintypeAffineCoords`, `affineCombination_mem_interior_face_iff_pos`, `sign_eq_of_affineCombination_mem_affineSpan_single_lineMap`) — affine *geometry*, not affine functions on the cube. The `Polynomial.signVariations` / Rule-of-Signs hits — relevant to Lemma 12, not here. The `degree`/`degrees_indicator`/Chevalley `degBound` hits — unrelated notions of degree. `CanonicallyOrderedAdd.prod_pos` — canonically-ordered semirings exclude $\mathbb{R}$.

## Actionable leads

1. **Prove as a corollary, not afresh:** chain $H^*(f)\overset{\text{L10}}{=}L_{\mathrm{frac}}(f)\overset{\text{clear}}{=}\mathrm{MFdeg}_\pm(f)$, reusing the clearing identity already written in Lemma 13's *Consequence*.
2. **Positivity engine:** $\prod_h D_h(x)>0$ via `Finset.prod_pos` (each $D_h>0$ from Lemma 13); multiplication/division by it preserves the sign pattern on $\{0,1\}^n$.
3. **Strictness:** upgrade Lemma 10's one-sided `iff` to strict two-sided by perturbing the global constant $c\to c-\epsilon$, $0<\epsilon<$ (min positive margin over the finite cube); leaves all $(N_h,D_h)$ and the shape of $P$ unchanged.
4. **Pin the definition:** read "admissible" as Lemma 13's *exact* three denominator classes (all-zero / all-positive / all-negative coordinate coeffs), not the looser prose — the reverse direction depends on it.
5. **Free consistency check + downstream payoff:** $\deg P\le H$ re-derives Lemma 6 ($\deg_\pm\le H^*$); and via rational degree (Iyer et al. 2023) any $\mathrm{rdeg}_\pm$ lower bound becomes an $H^*$ lower bound.
