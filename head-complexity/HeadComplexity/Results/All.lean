import HeadComplexity.Results.RestrictionLowerBounds
import HeadComplexity.Results.ExactFamilies
import HeadComplexity.Results.ThresholdDegree
import HeadComplexity.Results.WeightedUpperBound
import HeadComplexity.Results.FractionalNormalForm
import HeadComplexity.Results.LowComplexity
import HeadComplexity.Results.SymmetricComplexity

set_option linter.style.header false

/-!
# Main results — the twelve foundational lemmas, in one place.

A machine-checked table of contents.  Each `alias` below names the headline
theorem of one lemma from `lemmas/01_foundations_and_normal_form/`; because the
build elaborates these aliases, this file *verifies* that every result exists with
the meaning claimed.  All are general-`n` and axiom-clean
(`[propext, Classical.choice, Quot.sound]`; the build's `#print axioms` gate
confirms it).  `H*` is `HStarN n f`, the least number of attention heads realizing
`f`; `deg±` is `thresholdDeg`.

See `README.md` for the lemma↔file map and `PROOF_OVERVIEW.md` for the proof
architecture.
-/

namespace HeadComplexity

/-- **Lemma 1.** The numerator, restricted to two coordinates, splits additively. -/
alias lemma1_additive_split := restricted_numerator_additive_split

/-- **Lemma 2.** Antipode identity for the restricted numerator. -/
alias lemma2_antipode := restricted_numerator_antipode

/-- **Lemma 3.** A checkerboard restriction forces `H* ≥ 2`. -/
alias lemma3_checkerboard := checkerboard_restriction_HStarN_ge_two

/-- **Lemma 4.** Every monotone symmetric threshold has `H* = 1`. -/
alias lemma4_threshold := HStarN_threshold

/-- **Lemma 5.** Internal exact-count predicates have `H* = 2`. -/
alias lemma5_exact := HStarN_exact

/-- **Lemma 6.** Threshold degree is bounded by head complexity:
`computableWithHeadsN n H f → ThresholdDegLE f H`. -/
alias lemma6_degree_le := degree_le_of_computableWithHeadsN

/-- **Lemma 7.** Parity has threshold degree exactly `n`. -/
alias lemma7_parity_degree := parity_thresholdDeg

/-- **Lemma 8.** Parity needs one head per bit: `H*(XOR_n) = n`. -/
alias lemma8_parity := HStarN_parity

/-- **Lemma 9.** Weighted-sum upper bound `H* ≤ M − 1` … -/
alias lemma9_weighted := HStarN_le_weighted_sum

/-- … and the universal bound `H* ≤ 2ⁿ − 1`. -/
alias lemma9_universal := HStarN_le_universal_boolean

/-- **Lemma 10.** Exact linear-fractional normal form: `H*(f) = L_frac(f)`. -/
alias lemma10_normal_form := HStarN_eq_Lfrac

/-- **Lemma 11.** `H* = 0` iff `f` is constant … -/
alias lemma11_level0 := HStarN_eq_zero_iff

/-- … and `H* = 1` iff `f` is a nonconstant linear threshold function. -/
alias lemma11_level1 := HStarN_eq_one_iff

/-- **Lemma 12.** Symmetric sign-change characterization:
`H*(symmetricFn F) = signChanges n F`. -/
alias lemma12_symmetric := HStarN_symmetricFn

end HeadComplexity
