import HeadComplexity.Model.AdditiveSplit

set_option linter.style.header false

/-!
# Result-facing lower bounds from two-coordinate restrictions.

This module is the public entry point for the result statements whose proofs live
in the generalized attention model. The implementation modules keep the algebraic
lemmas close to `Head`; this file gives the theorem layer a `Results.*` import.
-/

namespace HeadComplexity

/-- **Lemma 1.** The numerator, restricted to two coordinates, splits additively. -/
alias restricted_numerator_additive_split := Head.numerator_additive_split

/-- **Lemma 2.** Antipode identity for the restricted numerator. -/
alias restricted_numerator_antipode := Head.restricted_numerator_antipode

/-- **Lemma 3.** A checkerboard restriction forces `H* ≥ 2`. -/
alias checkerboard_restriction_HStarN_ge_two := parity_restriction_HStarN_ge_two

end HeadComplexity
