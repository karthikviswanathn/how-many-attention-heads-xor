import HeadComplexity.Examples.Head

set_option linter.style.header false

/-!
# Skip-connection reduction.

The residual stream at the query token after one attention layer is
`h_= = x_= + z_=`, where `x_=` is the original `=` token embedding and
`z_=` is the attention update. Since `x_=` does not depend on the
input `(a, b)`, it is a constant offset, and any linear probe
`⟨w, h_=⟩ > τ` is equivalent to `⟨w, z_=⟩ > τ − ⟨w, x_=⟩`. This file
records that equivalence and specialises it to
`computesXor H.residual ↔ computesXor H.attnUpdate`.
-/

namespace HeadComplexity

open scoped InnerProductSpace

variable {d : ℕ}

/-- Adding a constant vector to a function does not change whether it
computes XOR under a linear readout: the offset is absorbed into the
threshold. -/
lemma computesXor_iff_of_add_const (f : Bool × Bool → Vec d) (c : Vec d) :
    computesXor f ↔ computesXor (fun ab => c + f ab) := by
  constructor
  · rintro ⟨w, τ, h⟩
    refine ⟨w, τ + ⟪w, c⟫_ℝ, fun ab => ?_⟩
    simp only [inner_add_right]
    constructor
    · intro hgt
      exact (h ab).mp (by linarith)
    · intro hxor
      have := (h ab).mpr hxor
      linarith
  · rintro ⟨w, τ, h⟩
    refine ⟨w, τ - ⟪w, c⟫_ℝ, fun ab => ?_⟩
    have key := h ab
    simp only [inner_add_right] at key
    constructor
    · intro hgt
      exact key.mp (by linarith)
    · intro hxor
      have := key.mpr hxor
      linarith

/-- The skip-connection reduction: a head's full residual `x_= + z_=`
computes XOR iff its bare attention update `z_=` does. The `x_=` term
is constant in the input, so a linear probe can absorb it into its
threshold. -/
lemma computesXor_residual_iff_attnUpdate (H : Head d) :
    computesXor H.residual ↔ computesXor H.attnUpdate := by
  have hconst : H.residual = fun ab => H.x (false, false) 2 + H.attnUpdate ab := by
    funext ab
    change H.x ab 2 + H.attnUpdate ab = H.x (false, false) 2 + H.attnUpdate ab
    rfl
  rw [hconst]
  exact (computesXor_iff_of_add_const H.attnUpdate (H.x (false, false) 2)).symm

end HeadComplexity
