import HeadComplexity.Atoms.WeightedAtom

set_option linter.style.header false

/-!
# Result-facing weighted upper bounds.

The atom module contains the construction. This module is the public result layer
for the weighted-sum and universal upper bounds on `H*`.
-/

namespace HeadComplexity

/-- **Lemma 9.** Weighted-sum upper bound `H* ≤ M - 1`. -/
alias HStarN_le_weighted_sum := HStarN_le_weighted

/-- **Lemma 9.** Universal upper bound `H* ≤ 2^n - 1`. -/
alias HStarN_le_universal_boolean := HStarN_le_universal

end HeadComplexity
