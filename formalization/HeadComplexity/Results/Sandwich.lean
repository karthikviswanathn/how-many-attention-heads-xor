import HeadComplexity.Results.ThresholdDegree
import HeadComplexity.Results.WeightedUpperBound
import HeadComplexity.Results.ExactFamilies
import HeadComplexity.Results.LowComplexity

/-!
# Toward the open problem: the threshold-degree / weighted-sum sandwich.

The exact characterization of `H*(f)` for arbitrary Boolean `f` is open. The best
general bounds available — the two sides this project has formalized — sandwich
`H*`:

`deg±(f) ≤ H*(f) ≤ M − 1`,

where `deg±` (= `thresholdDeg`) is the threshold degree (lower bound, Theorems 6/7)
and `M = |Im(t)|` is the image size of any positive weighted sum `t(x) = ∑ λ_i x_i`
through which `f` factors (upper bound, Theorem 9). Closing this gap — pinning `H*`
to a single known invariant `I(f)` with `H*(f) ≍ I(f)` — is the paper's main open
problem (`problem_statement.md`).

This file records the lower side as a clean, general theorem (`H*(f) ≥ deg±(f)`
for **all** `f`, the minimal-head form of Theorem 6) and assembles the sandwich.
-/

namespace HeadComplexity

open Finset

variable {n : ℕ}

/-- **Threshold degree lower-bounds head complexity.** For every Boolean function,
`deg±(f) ≤ H*(f)`. This is Theorem 6 evaluated at the minimal head count; for parity
Theorem 7 makes it tight (`deg±(parity) = n = H*(parity)`), and more generally it is
the lower edge of the head-complexity sandwich. -/
theorem thresholdDeg_le_HStarN (f : (Fin n → Bool) → Bool) :
    thresholdDeg f ≤ HStarN n f := by
  classical
  have hex : ∃ k, computableWithHeadsN n k f := exists_computable f
  have hcomp : computableWithHeadsN n (HStarN n f) f := by
    unfold HStarN; rw [dif_pos hex]; exact Nat.find_spec hex
  have hTD : ThresholdDegLE f (HStarN n f) := signReprDegLe_of_computableWithHeadsN hcomp
  have hexD : ∃ d, ThresholdDegLE f d := ⟨_, hTD⟩
  unfold thresholdDeg; rw [dif_pos hexD]
  exact Nat.find_min' hexD hTD

/-- **The current sandwich on head complexity.** If `f` factors through a positive
weighted sum `t(x) = ∑ λ_i x_i` (`λ_i > 0`) with image size `M`, then
`deg±(f) ≤ H*(f) ≤ M − 1`. The two bounds need not coincide; their gap is the open
problem. -/
theorem thresholdDeg_le_HStarN_le_image_card (f : (Fin n → Bool) → Bool)
    (lam : Fin n → ℝ) (hlam : ∀ i, 0 < lam i) (G : ℝ → Bool)
    (hf : ∀ bits, f bits = G (wT lam bits)) :
    thresholdDeg f ≤ HStarN n f ∧
      HStarN n f ≤ (Finset.univ.image (wT lam)).card - 1 :=
  ⟨thresholdDeg_le_HStarN f, HStarN_le_weighted_sum lam hlam f G hf⟩

/-- Specialized to parity, the lower edge is tight: `H*(XOR_n) = n = deg±(parity)`,
so the threshold-degree bound is attained. -/
example (n : ℕ) : thresholdDeg (PARITY n) = n ∧ HStarN n (PARITY n) = n :=
  ⟨thresholdDeg_parity n, HStarN_parity n⟩

end HeadComplexity
