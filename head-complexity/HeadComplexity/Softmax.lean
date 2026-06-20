import HeadComplexity.Basic

set_option linter.style.header false

/-!
# The three-term softmax.

A minimal local definition of softmax on `Fin 3 → ℝ`, used in the
two-head construction. The one-head impossibility proof does not
require this definition; it works directly with the unnormalized
numerator and denominator.
-/

namespace HeadComplexity

open Finset

/-- The three-term softmax: `softmax3 s i = exp(s i) / (∑ j, exp(s j))`. -/
noncomputable def softmax3 (s : Fin 3 → ℝ) : Fin 3 → ℝ :=
  fun i => Real.exp (s i) / ∑ j, Real.exp (s j)

/-- The softmax denominator is strictly positive. -/
lemma softmax3_denom_pos (s : Fin 3 → ℝ) : 0 < ∑ j, Real.exp (s j) := by
  apply Finset.sum_pos
  · intro i _
    exact Real.exp_pos _
  · exact Finset.univ_nonempty

/-- Each softmax weight is strictly positive. -/
lemma softmax3_pos (s : Fin 3 → ℝ) (i : Fin 3) : 0 < softmax3 s i :=
  div_pos (Real.exp_pos _) (softmax3_denom_pos s)

/-- Softmax weights are nonnegative. -/
lemma softmax3_nonneg (s : Fin 3 → ℝ) (i : Fin 3) : 0 ≤ softmax3 s i :=
  (softmax3_pos s i).le

/-- Softmax weights sum to one. -/
lemma softmax3_sum_one (s : Fin 3 → ℝ) : ∑ i, softmax3 s i = 1 := by
  simp only [softmax3, ← Finset.sum_div]
  exact div_self (softmax3_denom_pos s).ne'

end HeadComplexity
