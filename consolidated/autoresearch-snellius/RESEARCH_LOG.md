# Research Log — Head Complexity $H^{*}(f)$

> Append-only log for the autonomous research run (see the `/goal` prompt). One
> entry per attempted target: what was tried, the outcome **grounded in a verifier
> result or Lean build**, the key idea, and the next target. Never record a result
> as proved without `verification == "correct"` (Claude-Opus verifier) or a clean
> Lean build.

## Starting state (set by setup, before the autonomous run)

- **Proved + Lean-verified stack:** Lemmas 1–12 in `lemmas/01_foundations_and_normal_form/`
  (ledger: `lemmas.md`; Lean: `head-complexity/`). Highlights: exact linear-fractional
  normal form (L10), exact 0/1-head characterization (L11), threshold-degree lower bound
  (L6) + exact parity (L7, L8), weighted-sum upper bound (L9), exact symmetric
  characterization $H^{*}(f)=C(F)$ (L12).
- **Open frontier:** no exact characterization of $H^{*}(f)$ for general (nonsymmetric)
  Boolean functions.
- **Toolkit in place (subscription, no API keys):** `informal_prover_codex.py` (Codex gen +
  Claude-Opus-max verify + refine), `discussion_partner_codex.py` (strategy), `BLUEPRINT.md`
  (reconciled with `lemmas.md`: L1-12 foundation `done`, frontier targets open), `informal_decomposition.md`,
  `informal_solution_template.md`. See `INFORMAL_TOOLKIT.md`.
- **Loop smoke test:** $H^{*}(\mathrm{XOR}_2)=2$ re-proved through the toolkit and verified
  `correct` on attempt 1 (`informal_xor2_solution.md`). Confirms the generate→verify loop works
  on this problem. (This duplicates stack content; it is a pipeline check, not new math.)

## Log

<!-- The autonomous run appends entries below this line. Format:

### <ISO date> — <target label>
- **Target:** <statement>
- **Outcome:** verified | failed | blocked
- **Evidence:** <verification==correct, or Lean build result; cite the file>
- **Key idea:** <one or two sentences>
- **Recorded in:** <lemmas/ file, lemmas.md, BLUEPRINT.md updates>
- **Next:** <next target>
-->

### Iter 1: PROVED `affine_atom_dictionary` -> lemmas/01_foundations_and_normal_form/013_affine_atom_dictionary.md. This is the leaf on the critical path from the verified linear-fractional normal form to the cleared-denominator invariant. It isolates the exact positivity and boundary conditions that F2 must preserve, so later algebraic reformulations do not silently enlarge the model. (attempts=1)

### Iter 2: PROVED `cleared_denominator_invariant` -> lemmas/01_foundations_and_normal_form/014_cleared_denominator_invariant.md. This is the next critical-path leaf: Lemma 13 has now supplied the exact affine atom dictionary, so the linear-fractional normal form can be converted into a polynomial threshold invariant by clearing positive denominators. It unlocks the tangential-Chow reformulation and gives a sharper nonsymmetric invariant than the current normal-form restatement. (attempts=1)

### Iter 3: PROVED `tangential_chow_reformulation` -> lemmas/01_foundations_and_normal_form/015_tangential_chow_reformulation.md. Lemmas 13 and 14 have already done the model-specific work, so the next critical-path step is a clean algebraic identification of the cleared polynomial with a restricted tangential-Chow form. This unlocks the comparison with the unrestricted tangential-Chow invariant and possible standard-invariant connections. (attempts=2)

### Iter 4: PROVED `tchow_sandwich_lower_bound` -> lemmas/01_foundations_and_normal_form/016_tchow_sandwich_lower_bound.md. After Lemma 15, the full tangential-Chow comparison is too broad as one step, but this sandwich is an immediate leaf with all dependencies proved. It turns the new reformulation into a usable standard-flavored lower bound before attacking equality, positivity normalization, or separations. (attempts=1)

### Iter 5: PROVED `same_polarity_dnf_upper_bound` -> lemmas/01_foundations_and_normal_form/017_same_polarity_dnf_upper_bound.md. This is the safest constructive leaf under the calibrated positive-sum frontier: Lemmas 13 and 14 make the one-polarity subcube bump provable immediately, while the mixed-literal DNF claim needs a new gadget because admissible denominators cannot count violations of both signs in one head. It gives a genuine nonsymmetric sparse upper bound and clarifies how F8 should be split. (attempts=1)

### Iter 6: PROVED `same_polarity_sparse_threshold_density_upper_bound` -> lemmas/01_foundations_and_normal_form/018_same_polarity_sparse_threshold_density_upper_bound.md. This is the next calibrated strengthening of Lemma 17: it upgrades same-polarity DNF ORs to arbitrary sparse threshold densities using the same reciprocal bump gadget plus a finite margin argument. It advances F8 while keeping the mixed-literal DNF obstruction isolated. (attempts=1)

### Iter 7: PROVED `warren_head_count_upper_bound` -> lemmas/01_foundations_and_normal_form/019_warren_head_count_upper_bound.md. This is the cleanest leaf under the counting-separation frontier: Lemma 14 gives an $O(Hn)$-parameter polynomial sign representation, and Warren's theorem should immediately bound the number of realizable cube labelings. It unlocks the next step comparing against known counts of quadratic threshold functions to force a degree-$2$ versus head-complexity separation. (attempts=1)

### Iter 8: PROVED `quadratic_ptf_head_separation` -> lemmas/01_foundations_and_normal_form/020_quadratic_ptf_head_separation.md. Lemma 19 gives the low-head counting upper bound; the standard count of quadratic PTFs should now force a genuine separation from threshold degree. This directly advances the nonsymmetric frontier by showing $H^{\ast}$ is strictly finer than $\deg_{\pm}$. (attempts=1)

### Iter 9: PROVED `tchow_warren_count_upper_bound` -> lemmas/01_foundations_and_normal_form/021_tchow_warren_count_upper_bound.md. This is the clean leaf after Lemma 16: it applies the same Warren parameter-counting method as Lemma 19, but to the unrestricted tangential-Chow model. It unlocks a direct quadratic-PTF separation showing that $\deg_{\pm}(f)\leq \mathrm{tChow}_{\pm}(f)$ can be strict. (attempts=1)

### Iter 1: PROVED `quadratic_ptf_head_separation` -> lemmas/01_foundations_and_normal_form/022_quadratic_ptf_head_separation.md. Lemma 19 gives the needed upper bound on the number of low-head sign patterns, so the next leaf is to compare it with the known $2^{\Omega(n^3)}$ count of quadratic threshold functions. Proving this separates $H^{\ast}$ from ordinary threshold degree and gives a strong nonsymmetric obstruction. (attempts=2)

### Iter 2: PROVED `quadratic_ptf_tchow_separation` -> lemmas/01_foundations_and_normal_form/023_quadratic_ptf_tchow_separation.md. This is the immediate leaf unlocked by Lemma 21 and the already used quadratic PTF counting lower bound. It completes the strictness of the lower inequality in $\deg_{\pm}(f)\leq \mathrm{tChow}_{\pm}(f)\leq H^{\ast}(f)$, clarifying that tangential-Chow complexity is genuinely finer than threshold degree. (attempts=1)

### Iter 10: PROVED `quadratic_ptf_tchow_separation` -> lemmas/01_foundations_and_normal_form/023_quadratic_ptf_tchow_separation.md. Lemma 21 gives the counting upper bound for low unrestricted tangential-Chow complexity, so the same fixed-degree PTF counting argument used for Lemma 20 should now yield the clean separation. This directly clarifies the tangential-Chow comparison by proving that the lower sandwich inequality is genuinely strict. (attempts=3)

### Iter 3: PROVED `almost_all_head_lower_bound` -> lemmas/01_foundations_and_normal_form/024_almost_all_head_lower_bound.md. All dependencies are proved: Lemma 19 gives the low-head counting upper bound, and Lemma 9 gives the universal $2^n-1$ upper bound. This converts the counting machinery into a near-tight worst-case and random-function scale for $H^{\ast}$, clarifying how large the invariant can be outside structured families. (attempts=1)

### Iter 11: PROVED `almost_all_head_lower_bound` -> lemmas/01_foundations_and_normal_form/025_almost_all_head_lower_bound.md. Lemma 19 already bounds the number of functions computable with $H$ heads, so choosing $H=\Theta(2^n/n^2)$ makes the low-head class exponentially smaller than all $2^{2^n}$ Boolean functions. This gives a near-global scale for $H^{\ast}$ and a benchmark for future explicit lower-bound certificates. (attempts=1)

### Iter 5: PROVED `subcube_restriction_monotonicity` -> lemmas/01_foundations_and_normal_form/026_subcube_restriction_monotonicity.md. This is the cleanest generic lower-bound certificate still missing from the ledger: every hard subcube restriction immediately lower-bounds the original function. It unlocks explicit nonsymmetric targets such as address/indexing by reducing them to parity or other already proved hard restrictions. (attempts=1)

### Iter 12: PROVED `subcube_restriction_monotonicity` -> lemmas/01_foundations_and_normal_form/027_subcube_restriction_monotonicity.md. This is the cleanest new leaf with all dependencies already proved. It converts known exact lower bounds, especially parity via Lemma 8, into restriction certificates for asymmetric families such as address and indexing functions. (attempts=1)

### Iter 13: PROVED `address_indexing_parity_lower_bound` -> lemmas/01_foundations_and_normal_form/028_address_indexing_parity_lower_bound.md. This is the clean next leaf after subcube restriction monotonicity: all dependencies are proved, and it turns the new certificate into an explicit asymmetric lower bound. It advances the `address_indexing` frontier while avoiding the still-open mixed-literal DNF upper-bound gadget. (attempts=1)

### Iter 14: PROVED `two_polarity_sparse_threshold_density_upper_bound` -> lemmas/01_foundations_and_normal_form/029_two_polarity_sparse_threshold_density_upper_bound.md. This is the clean next upper-bound leaf after Lemmas 17 and 18: it removes the unnecessary global same-polarity restriction while still avoiding the genuinely hard mixed-literal subcube gadget. It strengthens the calibrated positive-sum route and gives a broader sparse nonsymmetric family with verified small head complexity. (attempts=1)

### Iter 15: PROVED `weighted_sum_sign_change_upper_bound` -> lemmas/01_foundations_and_normal_form/030_weighted_sum_sign_change_upper_bound.md. This is the cleanest proved-dependency leaf after Lemma 29: it sharpens the existing weighted-sum upper route without touching the hard mixed-literal subcube gadget. It also gives a reusable nonsymmetric upper bound controlled by one-dimensional sign changes rather than full image size. (attempts=2)

### Iter 17: PROVED `irrelevant_variable_invariance` -> lemmas/01_foundations_and_normal_form/031_irrelevant_variable_invariance.md. This completes Lemma 26's restriction monotonicity into an exact ambient-dimension invariance, so later upper bounds can be proved only on the active variables of a junta and then lifted without paying for irrelevant coordinates. It is a clean proved-dependency leaf using Lemma 10 plus the finite strict margin of any representation. (attempts=1)

### Iter 18: PROVED `active_junta_weighted_sum_upper_bound` -> lemmas/01_foundations_and_normal_form/032_active_junta_weighted_sum_upper_bound.md. Lemma 31 makes dummy coordinates free, so Lemma 30 can now be lifted cleanly from full-support weighted sums to active-variable weighted sums. The $k$-junta corollary gives a reusable ambient-dimension-independent upper bound for sparse and asymmetric families. (attempts=1)

### Iter 19: PROVED `active_junta_support_size_upper_bound` -> lemmas/01_foundations_and_normal_form/033_active_junta_support_size_upper_bound.md. This is the clean next corollary after Lemma 32: choose injective positive binary weights on the active variables and count sign changes by the number of one-runs or zero-runs. It sharpens the ambient-dimension-free junta upper bound and gives a reusable sparse or cosparse active-truth-table estimate. (attempts=1)

### Iter 20: PROVED `positive_minor_monotonicity` -> lemmas/01_foundations_and_normal_form/034_positive_minor_monotonicity.md. This is a clean lower-bound certificate leaf with all dependencies already proved: Lemma 10 makes the substitution directly inside each linear-fractional atom, and Lemma 31 handles unused target variables. It strengthens subcube restriction monotonicity by adding variable identification and duplication, useful for transferring hard minors into asymmetric families. (attempts=1)

### Iter 21: PROVED `homogeneous_polarity_minor_monotonicity` -> lemmas/01_foundations_and_normal_form/035_homogeneous_polarity_minor_monotonicity.md. This is the next clean lower-bound-certificate leaf after positive minor monotonicity. It captures the only input-negation symmetry that preserves the admissible one-head denominator structure and extends minor-transfer tools without touching the hard mixed-literal case. (attempts=1)

### Iter 22: PROVED `coordinate_subcube_one_head_exact` -> lemmas/01_foundations_and_normal_form/036_coordinate_subcube_one_head_exact.md. This is the cleanest leaf after the minor-monotonicity results: it is an immediate but useful exact mixed-literal subcube fact from the one-head LTF characterization. It clarifies that the remaining mixed-literal DNF obstacle is calibration and aggregation of subcube indicators, not recognition of a single mixed subcube. (attempts=1)

### Iter 23: BLOCKED `mixed_literal_dnf_upper_bound` after 35 attempts. Lemma 36 proves every mixed-literal subcube indicator is individually one-head; the remaining natural leaf is to calibrate those one-head features so a final threshold can aggregate a DNF. This directly closes the mixed-literal DNF gap left after Lemmas 17, 18, and 29, and strengthens the calibrated positive-sum upper-bound frontier. Next: decompose or switch.


## Autoresearch run summary

Finished after iteration loop: 21 new lemma(s) verified this run; -7.10h of the 10h budget remaining. See lemmas.md / BLUEPRINT.md for the updated state.
