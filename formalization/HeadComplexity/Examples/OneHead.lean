import HeadComplexity.Foundation.SegmentCrossing
import HeadComplexity.Model.AdditiveSplit
import HeadComplexity.Model.NHead
import HeadComplexity.Examples.HeadToNHead
import HeadComplexity.Examples.SkipConnection

set_option linter.style.header false

/-!
# Theorem 1: one attention head cannot compute XOR.

The four attention outputs `z(a,b)` satisfy a segment-crossing obstruction:
the midpoint `𝒟⁻¹ • 𝒩` (with `𝒟 = D(ff,ff) + D(tt,tt)`,
`𝒩 = N(ff,ff) + N(tt,tt)`) lies simultaneously on the diagonal segment
`[z(ff,ff), z(tt,tt)]` and on the off-diagonal segment
`[z(ff,tt), z(tt,ff)]`. No linear probe can place the diagonal outputs
below a threshold and the off-diagonal outputs above it.
-/

namespace HeadComplexity

open scoped InnerProductSpace

namespace Head

variable {d : ℕ} (H : Head d)

/-- The attention denominator is strictly positive. -/
lemma denominator_pos (ab : Bool × Bool) : 0 < H.denominator ab := by
  simpa using NHead.denominator_pos H.toNHead (pairToBits ab)

lemma denominator_ne_zero (ab : Bool × Bool) : H.denominator ab ≠ 0 :=
  (H.denominator_pos ab).ne'

private lemma restrictBits_pairToBits (ab : Bool × Bool) :
    NHead.restrictBits (fun _ : Fin 2 => false) 0 1 ab = pairToBits ab := by
  funext k
  fin_cases k <;> simp [NHead.restrictBits, pairToBits]

/-- The two-bit numerator split, obtained by specializing the generalized model. -/
theorem numerator_additive_split :
    ∃ (A B : Bool → Vec d) (C : Vec d), ∀ a b : Bool,
      H.numerator (a, b) = A a + B b + C := by
  have h01 : (0 : Fin 2) ≠ 1 := by decide
  rcases NHead.numerator_additive_split H.toNHead (fun _ : Fin 2 => false) 0 1 h01 with
    ⟨A, B, C, h⟩
  refine ⟨A, B, C, ?_⟩
  intro a b
  simpa [restrictBits_pairToBits] using h a b

/-- The two-bit denominator split, obtained by specializing the generalized model. -/
theorem denominator_additive_split :
    ∃ (α β : Bool → ℝ) (γ : ℝ), ∀ a b : Bool,
      H.denominator (a, b) = α a + β b + γ := by
  have h01 : (0 : Fin 2) ≠ 1 := by decide
  rcases NHead.denominator_additive_split H.toNHead (fun _ : Fin 2 => false) 0 1 h01 with
    ⟨α, β, γ, h⟩
  refine ⟨α, β, γ, ?_⟩
  intro a b
  simpa [restrictBits_pairToBits] using h a b

/-- The antipode identity for the attention numerator: summing `N(a,b)`
over the diagonal equals summing over the off-diagonal. -/
theorem numerator_antipode :
    H.numerator (false, false) + H.numerator (true, true)
    = H.numerator (false, true) + H.numerator (true, false) := by
  rcases H.numerator_additive_split with ⟨A, B, C, h⟩
  rw [h false false, h true true, h false true, h true false]
  abel

/-- The antipode identity for the attention denominator: summing `D(a,b)`
across the diagonal equals summing across the off-diagonal. -/
theorem denominator_antipode :
    H.denominator (false, false) + H.denominator (true, true)
    = H.denominator (false, true) + H.denominator (true, false) := by
  rcases H.denominator_additive_split with ⟨α, β, γ, h⟩
  rw [h false false, h true true, h false true, h true false]
  abel

/-- Multiplying the attention update by the denominator recovers the numerator. -/
lemma denom_smul_attn (ab : Bool × Bool) :
    H.denominator ab • H.attnUpdate ab = H.numerator ab := by
  unfold Head.attnUpdate
  rw [smul_inv_smul₀ (H.denominator_ne_zero ab)]

/-- A two-term convex combination written with explicit divisions equals
the inverse-scaled sum of its weighted summands. -/
private lemma combo_eq_scaled_sum {V : Type*} [AddCommGroup V] [Module ℝ V]
    (a b : ℝ) (u v : V) :
    (a / (a + b)) • u + (b / (a + b)) • v = (a + b)⁻¹ • (a • u + b • v) := by
  rw [smul_add, smul_smul, smul_smul]
  congr 1
  · rw [div_eq_mul_inv, mul_comm]
  · rw [div_eq_mul_inv, mul_comm]

/-- The **midpoint** `P` of the four attention outputs: `𝒟⁻¹ • 𝒩`. -/
noncomputable def midpoint : Vec d :=
  (H.denominator (false, false) + H.denominator (true, true))⁻¹
  • (H.numerator (false, false) + H.numerator (true, true))

/-- The midpoint lies on the diagonal segment `[z(ff,ff), z(tt,tt)]`. -/
lemma midpoint_in_diag_segment :
    H.midpoint ∈ segment ℝ (H.attnUpdate (false, false)) (H.attnUpdate (true, true)) := by
  set D0 := H.denominator (false, false)
  set D1 := H.denominator (true, true)
  have hpos : (0 : ℝ) < D0 + D1 :=
    add_pos (H.denominator_pos _) (H.denominator_pos _)
  refine ⟨D0 / (D0 + D1), D1 / (D0 + D1), ?_, ?_, ?_, ?_⟩
  · exact div_nonneg (H.denominator_pos _).le hpos.le
  · exact div_nonneg (H.denominator_pos _).le hpos.le
  · rw [← add_div, div_self hpos.ne']
  · unfold Head.midpoint
    rw [← H.denom_smul_attn (false, false), ← H.denom_smul_attn (true, true)]
    exact combo_eq_scaled_sum _ _ _ _

/-- The midpoint also lies on the off-diagonal segment `[z(ff,tt), z(tt,ff)]`,
because the denominator and numerator antipode identities make both
representations of the midpoint equal. -/
lemma midpoint_in_offdiag_segment :
    H.midpoint ∈ segment ℝ (H.attnUpdate (false, true)) (H.attnUpdate (true, false)) := by
  set D0 := H.denominator (false, true)
  set D1 := H.denominator (true, false)
  have hpos : (0 : ℝ) < D0 + D1 :=
    add_pos (H.denominator_pos _) (H.denominator_pos _)
  refine ⟨D0 / (D0 + D1), D1 / (D0 + D1), ?_, ?_, ?_, ?_⟩
  · exact div_nonneg (H.denominator_pos _).le hpos.le
  · exact div_nonneg (H.denominator_pos _).le hpos.le
  · rw [← add_div, div_self hpos.ne']
  · unfold Head.midpoint
    rw [H.numerator_antipode, H.denominator_antipode,
        ← H.denom_smul_attn (false, true), ← H.denom_smul_attn (true, false)]
    exact combo_eq_scaled_sum _ _ _ _

end Head

/-- Example of with a separate proof that no single attention head can
compute XOR: for every `H`, the bare attention update `z_=` is not linearly
separable into XOR classes. -/
example {d : ℕ} (H : Head d) :
     ¬ computesXor H.attnUpdate := by
  rintro ⟨w, τ, hw⟩
  -- Diagonal inputs (XOR = false): `⟨w, z⟩ ≤ τ`.
  have h00 : ⟪w, H.attnUpdate (false, false)⟫_ℝ ≤ τ := by
    by_contra h
    exact (Bool.false_ne_true) ((hw (false, false)).mp (lt_of_not_ge h))
  have h11 : ⟪w, H.attnUpdate (true, true)⟫_ℝ ≤ τ := by
    by_contra h
    exact (Bool.false_ne_true) ((hw (true, true)).mp (lt_of_not_ge h))
  -- Off-diagonal inputs (XOR = true): `⟨w, z⟩ > τ`.
  have h01 : τ < ⟪w, H.attnUpdate (false, true)⟫_ℝ :=
    (hw (false, true)).mpr rfl
  have h10 : τ < ⟪w, H.attnUpdate (true, false)⟫_ℝ :=
    (hw (true, false)).mpr rfl
  -- Apply the segment-crossing obstruction.
  exact segment_cross_not_separable (innerLeftLin w) h00 h11 h01 h10
    H.midpoint_in_diag_segment H.midpoint_in_offdiag_segment

/-- **Theorem 1 (attention update form).** No single attention head can
compute XOR: for every `H`, the bare attention update `z_=` is not linearly
separable into XOR classes. -/
theorem one_head_cannot_xor_attnUpdate {d : ℕ} (H : Head d) :
    ¬ computesXor H.attnUpdate := by
  intro hxor
  let f : (Fin 2 → Bool) → Bool := fun bits => xor (bits 0) (bits 1)
  have hcomp : computableWithHeadsN 2 1 f := by
    refine ⟨d, fun _ => H.toNHead, ?_⟩
    rcases hxor with ⟨w, τ, hw⟩
    refine ⟨w, τ, ?_⟩
    intro bits
    simpa [f, nHeadFamilyAttnUpdate] using hw (bits 0, bits 1)
  have h00 : f (NHead.restrictBits (fun _ => false) 0 1 (false, false)) = false := by
    simp [f, NHead.restrictBits]
  have h11 : f (NHead.restrictBits (fun _ => false) 0 1 (true, true)) = false := by
    simp [f, NHead.restrictBits]
  have h01 : f (NHead.restrictBits (fun _ => false) 0 1 (false, true)) = true := by
    simp [f, NHead.restrictBits]
  have h10 : f (NHead.restrictBits (fun _ => false) 0 1 (true, false)) = true := by
    simp [f, NHead.restrictBits]
  exact (parity_restriction_not_computable_with_one_head
    f (fun _ => false) 0 1 (by decide) h00 h11 h01 h10) hcomp

/-- **Theorem 1 (full residual form).** No single attention head can compute
XOR even when reading the full residual stream `h_= = x_= + z_=`. The skip
connection is a constant offset and is absorbed into the readout threshold. -/
theorem one_head_cannot_xor_residual {d : ℕ} (H : Head d) :
    ¬ computesXor H.residual := by
  rw [computesXor_residual_iff_attnUpdate]
  exact one_head_cannot_xor_attnUpdate H

end HeadComplexity
