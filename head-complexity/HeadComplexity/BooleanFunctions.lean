import HeadComplexity.OneHead
import HeadComplexity.TwoHeads

/-!
# Boolean-function examples in the head-complexity model.

This file packages the existing XOR results into a more general
`computesBool` predicate and proves explicit upper bounds for the
2-bit functions `OR` and `AND` using a single head. Together with the
one-head XOR impossibility and the two-head XOR construction, this
gives a small library of formalized examples for the problem statement.
-/

namespace HeadComplexity

open scoped InnerProductSpace

variable {d : ℕ}

/-- A vector-valued function on Boolean pairs computes a Boolean target
    under a linear readout when some probe and threshold classify the
    four inputs exactly. -/
def computesBool (f : Bool × Bool → Bool) (g : Bool × Bool → Vec d) : Prop :=
  ∃ (w : Vec d) (τ : ℝ), ∀ ab : Bool × Bool,
    ⟪w, g ab⟫_ℝ > τ ↔ f ab = true

/-- Named versions of the standard 2-bit Boolean functions. -/
def falseFn : Bool × Bool → Bool := fun _ => false
def trueFn : Bool × Bool → Bool := fun _ => true
def orFn : Bool × Bool → Bool := fun ab => ab.1 || ab.2
def andFn : Bool × Bool → Bool := fun ab => ab.1 && ab.2
def xorFn : Bool × Bool → Bool := fun ab => xor ab.1 ab.2
def norFn : Bool × Bool → Bool := fun ab => !(orFn ab)
def nandFn : Bool × Bool → Bool := fun ab => !(andFn ab)
def xnorFn : Bool × Bool → Bool := fun ab => !(xorFn ab)

/-- The 2-bit symmetric Boolean function determined by its values on
    Hamming weights `0`, `1`, and `2`. -/
def symmFn (c0 c1 c2 : Bool) : Bool × Bool → Bool
  | (false, false) => c0
  | (false, true)  => c1
  | (true, false)  => c1
  | (true, true)   => c2

/-- A family of `H` attention heads sharing the same ambient vector space. -/
abbrev HeadFamily (d H : ℕ) : Type := Fin H → Head d

/-- The summed attention update of an `H`-head family. This is the
    multi-head quantity used for the exact-complexity examples below. -/
noncomputable def headFamilyAttnUpdate {H : ℕ} (Hs : HeadFamily d H) :
    Bool × Bool → Vec d :=
  fun ab => ∑ i, (Hs i).attnUpdate ab

/-- A Boolean function is computable with `H` heads if some embedding
    dimension and some `H`-head family realize it via a linear readout
    from the summed attention update. -/
def computableWithHeads (f : Bool × Bool → Bool) (H : ℕ) : Prop :=
  ∃ d, ∃ Hs : HeadFamily d H, computesBool f (headFamilyAttnUpdate Hs)

/-- Exact head complexity for the present formalization: realizable with
    `k` heads and unrealizable with any smaller number. -/
def exactHeadComplexity (f : Bool × Bool → Bool) (k : ℕ) : Prop :=
  computableWithHeads f k ∧ ∀ h < k, ¬ computableWithHeads f h

/-- Explicit head complexity value, defaulting to `0` only when a
    function is unrealizable in the current formalization. -/
noncomputable def HStar (f : Bool × Bool → Bool) : ℕ :=
  by
    classical
    exact if h : ∃ k, computableWithHeads f k then Nat.find h else 0

@[simp] lemma headFamilyAttnUpdate_zero {Hs : HeadFamily d 0} (ab : Bool × Bool) :
    headFamilyAttnUpdate Hs ab = 0 := by
  simp [headFamilyAttnUpdate]

@[simp] lemma headFamilyAttnUpdate_one {Hs : HeadFamily d 1} (ab : Bool × Bool) :
    headFamilyAttnUpdate Hs ab = (Hs 0).attnUpdate ab := by
  simp [headFamilyAttnUpdate]

@[simp] lemma computesXor_iff_computesBool_xor (g : Bool × Bool → Vec d) :
    computesXor g ↔ computesBool xorFn g := by
  rfl

@[simp] lemma falseFn_apply (ab : Bool × Bool) : falseFn ab = false := rfl
@[simp] lemma trueFn_apply (ab : Bool × Bool) : trueFn ab = true := rfl
@[simp] lemma norFn_apply (ab : Bool × Bool) : norFn ab = !(orFn ab) := rfl
@[simp] lemma nandFn_apply (ab : Bool × Bool) : nandFn ab = !(andFn ab) := rfl
@[simp] lemma xnorFn_apply (ab : Bool × Bool) : xnorFn ab = !(xorFn ab) := rfl

lemma HStar_eq_of_exact {f : Bool × Bool → Bool} {k : ℕ}
    (hk : exactHeadComplexity f k) : HStar f = k := by
  classical
  unfold HStar
  split_ifs with hExists
  · apply le_antisymm
    · exact Nat.find_min' hExists hk.1
    · by_contra hlt
      exact (hk.2 (Nat.find hExists) (Nat.lt_of_not_ge hlt)) (Nat.find_spec hExists)
  · exfalso
    exact hExists ⟨k, hk.1⟩

/-- Adding a constant vector only shifts the probe threshold. -/
lemma computesBool_iff_of_add_const
    (f : Bool × Bool → Bool) (g : Bool × Bool → Vec d) (c : Vec d) :
    computesBool f g ↔ computesBool f (fun ab => c + g ab) := by
  constructor
  · rintro ⟨w, τ, h⟩
    refine ⟨w, τ + ⟪w, c⟫_ℝ, fun ab => ?_⟩
    simp only [inner_add_right]
    constructor
    · intro hgt
      exact (h ab).mp (by linarith)
    · intro hf
      have := (h ab).mpr hf
      linarith
  · rintro ⟨w, τ, h⟩
    refine ⟨w, τ - ⟪w, c⟫_ℝ, fun ab => ?_⟩
    have key := h ab
    simp only [inner_add_right] at key
    constructor
    · intro hgt
      exact key.mp (by linarith)
    · intro hf
      have := key.mpr hf
      linarith

/-- Generic skip-connection reduction for Boolean classification. -/
lemma computesBool_residual_iff_attnUpdate
    (f : Bool × Bool → Bool) (H : Head d) :
    computesBool f H.residual ↔ computesBool f H.attnUpdate := by
  have hconst : H.residual = fun ab => H.x (false, false) 2 + H.attnUpdate ab := by
    funext ab
    change H.x ab 2 + H.attnUpdate ab = H.x (false, false) 2 + H.attnUpdate ab
    rfl
  rw [hconst]
  exact (computesBool_iff_of_add_const f H.attnUpdate (H.x (false, false) 2)).symm

namespace Head

noncomputable def oneProbe : Vec 3 := EuclideanSpace.single (1 : Fin 3) 1

private lemma exp_one_add_two_pos : (0 : ℝ) < Real.exp 1 + 2 := by
  have : (0 : ℝ) < Real.exp 1 := Real.exp_pos _
  linarith

private lemma exp_one_div_exp_one_add_two_pos :
    (0 : ℝ) < Real.exp 1 / (Real.exp 1 + 2) := by
  exact div_pos (Real.exp_pos _) exp_one_add_two_pos

private lemma exp_one_div_exp_one_add_two_lt_two_exp_one_div_two_exp_one_add_one :
    Real.exp 1 / (Real.exp 1 + 2) < 2 * Real.exp 1 / (2 * Real.exp 1 + 1) := by
  have he : (1 : ℝ) < Real.exp 1 := Real.one_lt_exp_iff.mpr one_pos
  have hden1 : (0 : ℝ) < Real.exp 1 + 2 := exp_one_add_two_pos
  have hden2 : (0 : ℝ) < 2 * Real.exp 1 + 1 := by
    have : (0 : ℝ) < Real.exp 1 := Real.exp_pos _
    linarith
  rw [div_lt_div_iff₀ hden1 hden2]
  nlinarith

@[simp] lemma oneProbe_apply :
    oneProbe = EuclideanSpace.single (1 : Fin 3) 1 := rfl

noncomputable def twoProbe : Vec 3 :=
  EuclideanSpace.single (0 : Fin 3) 1 + EuclideanSpace.single (1 : Fin 3) 1

private lemma head1_score_ff_ff :
    ⟪oneProbe, head1.attnUpdate (false, false)⟫_ℝ = 0 := by
  rw [head1_attnUpdate_ff_ff]
  simp [oneProbe]

private lemma head1_score_ff_tt :
    ⟪oneProbe, head1.attnUpdate (false, true)⟫_ℝ
      = Real.exp 1 / (Real.exp 1 + 2) := by
  rw [head1_attnUpdate_ff_tt]
  rw [inner_smul_right, oneProbe_apply, inner_single_single]
  simp [div_eq_mul_inv]

private lemma head1_score_tt_ff :
    ⟪oneProbe, head1.attnUpdate (true, false)⟫_ℝ
      = Real.exp 1 / (Real.exp 1 + 2) := by
  rw [head1_attnUpdate_tt_ff]
  rw [inner_smul_right, oneProbe_apply, inner_single_single]
  simp [div_eq_mul_inv]

private lemma head1_score_tt_tt :
    ⟪oneProbe, head1.attnUpdate (true, true)⟫_ℝ
      = 2 * Real.exp 1 / (2 * Real.exp 1 + 1) := by
  rw [head1_attnUpdate_tt_tt]
  rw [inner_smul_right, oneProbe_apply, inner_single_single]
  simp [div_eq_mul_inv]

private lemma neg_head1_score_ff_ff :
    ⟪-oneProbe, head1.attnUpdate (false, false)⟫_ℝ = 0 := by
  simpa [inner_neg_left] using congrArg Neg.neg head1_score_ff_ff

private lemma neg_head1_score_ff_tt :
    ⟪-oneProbe, head1.attnUpdate (false, true)⟫_ℝ
      = -(Real.exp 1 / (Real.exp 1 + 2)) := by
  simpa [inner_neg_left] using congrArg Neg.neg head1_score_ff_tt

private lemma neg_head1_score_tt_ff :
    ⟪-oneProbe, head1.attnUpdate (true, false)⟫_ℝ
      = -(Real.exp 1 / (Real.exp 1 + 2)) := by
  simpa [inner_neg_left] using congrArg Neg.neg head1_score_tt_ff

private lemma neg_head1_score_tt_tt :
    ⟪-oneProbe, head1.attnUpdate (true, true)⟫_ℝ
      = -(2 * Real.exp 1 / (2 * Real.exp 1 + 1)) := by
  simpa [inner_neg_left] using congrArg Neg.neg head1_score_tt_tt

/-- Head 1 separates `OR` on the bare attention update. -/
theorem head1_computes_or_attnUpdate :
    computesBool orFn head1.attnUpdate := by
  let τ : ℝ := (Real.exp 1 / (Real.exp 1 + 2)) / 2
  have hτ_pos : 0 < τ := by
    dsimp [τ]
    linarith [exp_one_div_exp_one_add_two_pos]
  have hτ_lt_mid : τ < Real.exp 1 / (Real.exp 1 + 2) := by
    dsimp [τ]
    linarith [exp_one_div_exp_one_add_two_pos]
  refine ⟨oneProbe, τ, ?_⟩
  rintro ⟨a, b⟩
  cases a <;> cases b
  · rw [head1_score_ff_ff]
    have hnot : ¬ 0 > τ := by linarith
    simp [orFn, τ, hnot]
  · rw [head1_score_ff_tt]
    have hgt : Real.exp 1 / (Real.exp 1 + 2) > τ := by linarith
    simp [orFn, τ, hgt]
  · rw [head1_score_tt_ff]
    have hgt : Real.exp 1 / (Real.exp 1 + 2) > τ := by linarith
    simp [orFn, τ, hgt]
  · rw [head1_score_tt_tt]
    have hgt : 2 * Real.exp 1 / (2 * Real.exp 1 + 1) > τ := by
      linarith [hτ_lt_mid, exp_one_div_exp_one_add_two_lt_two_exp_one_div_two_exp_one_add_one]
    simp [orFn, τ, hgt]

/-- Head 1 also separates `AND` on the bare attention update. -/
theorem head1_computes_and_attnUpdate :
    computesBool andFn head1.attnUpdate := by
  let lo : ℝ := Real.exp 1 / (Real.exp 1 + 2)
  let hi : ℝ := 2 * Real.exp 1 / (2 * Real.exp 1 + 1)
  let τ : ℝ := (lo + hi) / 2
  have hgap : lo < hi := by
    dsimp [lo, hi]
    exact exp_one_div_exp_one_add_two_lt_two_exp_one_div_two_exp_one_add_one
  have hlo : lo < τ := by
    dsimp [τ]
    linarith
  have hhi : τ < hi := by
    dsimp [τ]
    linarith
  have hzero : (0 : ℝ) < τ := by
    linarith [exp_one_div_exp_one_add_two_pos, hlo]
  refine ⟨oneProbe, τ, ?_⟩
  rintro ⟨a, b⟩
  cases a <;> cases b
  · rw [head1_score_ff_ff]
    have hnot : ¬ 0 > τ := by linarith
    simp [andFn, τ, hnot]
  · rw [head1_score_ff_tt]
    have hnot : ¬ lo > τ := by linarith
    simp [andFn, lo, τ, hnot]
  · rw [head1_score_tt_ff]
    have hnot : ¬ lo > τ := by linarith
    simp [andFn, lo, τ, hnot]
  · rw [head1_score_tt_tt]
    have hgt : hi > τ := by linarith
    simp [andFn, hi, τ, hgt]

/-- Negating the probe for Head 1 separates `NOR`. -/
theorem head1_computes_nor_attnUpdate :
    computesBool norFn head1.attnUpdate := by
  let lo : ℝ := Real.exp 1 / (Real.exp 1 + 2)
  let τ : ℝ := -(lo / 2)
  have hlo : 0 < lo := exp_one_div_exp_one_add_two_pos
  have hτneg : τ < 0 := by
    dsimp [τ]
    linarith
  have hlow : -lo ≤ τ := by
    dsimp [τ]
    linarith
  have hhigh : -(2 * Real.exp 1 / (2 * Real.exp 1 + 1)) ≤ τ := by
    dsimp [τ]
    linarith [exp_one_div_exp_one_add_two_lt_two_exp_one_div_two_exp_one_add_one]
  refine ⟨-oneProbe, τ, ?_⟩
  rintro ⟨a, b⟩
  cases a <;> cases b
  · rw [neg_head1_score_ff_ff]
    have hgt : (0 : ℝ) > τ := by linarith
    simp [norFn, orFn, τ, hgt]
  · rw [neg_head1_score_ff_tt]
    have hnot : ¬ -lo > τ := by linarith
    simp [norFn, orFn, lo, τ, hnot]
  · rw [neg_head1_score_tt_ff]
    have hnot : ¬ -lo > τ := by linarith
    simp [norFn, orFn, lo, τ, hnot]
  · rw [neg_head1_score_tt_tt]
    have hnot : ¬ -(2 * Real.exp 1 / (2 * Real.exp 1 + 1)) > τ := by linarith
    simp [norFn, orFn, τ, hnot]

/-- Negating the probe for Head 1 separates `NAND`. -/
theorem head1_computes_nand_attnUpdate :
    computesBool nandFn head1.attnUpdate := by
  let lo : ℝ := Real.exp 1 / (Real.exp 1 + 2)
  let hi : ℝ := 2 * Real.exp 1 / (2 * Real.exp 1 + 1)
  let τ : ℝ := -((lo + hi) / 2)
  have hgap : lo < hi := exp_one_div_exp_one_add_two_lt_two_exp_one_div_two_exp_one_add_one
  have hτ0 : τ < 0 := by
    dsimp [τ]
    linarith [exp_one_div_exp_one_add_two_pos]
  have hmixed : τ < -lo := by
    dsimp [τ]
    linarith
  have htt : -(hi) ≤ τ := by
    dsimp [τ]
    linarith
  refine ⟨-oneProbe, τ, ?_⟩
  rintro ⟨a, b⟩
  cases a <;> cases b
  · rw [neg_head1_score_ff_ff]
    have hgt : (0 : ℝ) > τ := by linarith
    simp [nandFn, andFn, τ, hgt]
  · rw [neg_head1_score_ff_tt]
    have hgt : -lo > τ := by linarith
    simp [nandFn, andFn, lo, τ, hgt]
  · rw [neg_head1_score_tt_ff]
    have hgt : -lo > τ := by linarith
    simp [nandFn, andFn, lo, τ, hgt]
  · rw [neg_head1_score_tt_tt]
    have hnot : ¬ -hi > τ := by linarith
    simp [nandFn, andFn, hi, τ, hnot]

/-- The skip connection does not change `OR` computability for Head 1. -/
theorem head1_computes_or_residual :
    computesBool orFn head1.residual := by
  rw [computesBool_residual_iff_attnUpdate]
  exact head1_computes_or_attnUpdate

/-- The skip connection does not change `AND` computability for Head 1. -/
theorem head1_computes_and_residual :
    computesBool andFn head1.residual := by
  rw [computesBool_residual_iff_attnUpdate]
  exact head1_computes_and_attnUpdate

/-- The skip connection does not change `NOR` computability for Head 1. -/
theorem head1_computes_nor_residual :
    computesBool norFn head1.residual := by
  rw [computesBool_residual_iff_attnUpdate]
  exact head1_computes_nor_attnUpdate

/-- The skip connection does not change `NAND` computability for Head 1. -/
theorem head1_computes_nand_residual :
    computesBool nandFn head1.residual := by
  rw [computesBool_residual_iff_attnUpdate]
  exact head1_computes_nand_attnUpdate

end Head

/-- The 0-head model computes the constantly-false function. -/
theorem false_computable_with_zero_heads :
    computableWithHeads falseFn 0 := by
  refine ⟨1, Fin.elim0, ?_⟩
  refine ⟨0, 0, ?_⟩
  intro ab
  simp [falseFn, headFamilyAttnUpdate]

/-- The 0-head model also computes the constantly-true function. -/
theorem true_computable_with_zero_heads :
    computableWithHeads trueFn 0 := by
  refine ⟨1, Fin.elim0, ?_⟩
  refine ⟨0, -1, ?_⟩
  intro ab
  simp [trueFn, headFamilyAttnUpdate]

/-- A single head suffices to compute `OR` in the query residual. -/
theorem or_computable_with_one_head :
    ∃ H : Head 3, computesBool orFn H.residual := by
  exact ⟨Head.head1, Head.head1_computes_or_residual⟩

/-- A single head suffices to compute `AND` in the query residual. -/
theorem and_computable_with_one_head :
    ∃ H : Head 3, computesBool andFn H.residual := by
  exact ⟨Head.head1, Head.head1_computes_and_residual⟩

/-- A single head suffices to compute `NOR` in the query residual. -/
theorem nor_computable_with_one_head :
    ∃ H : Head 3, computesBool norFn H.residual := by
  exact ⟨Head.head1, Head.head1_computes_nor_residual⟩

/-- A single head suffices to compute `NAND` in the query residual. -/
theorem nand_computable_with_one_head :
    ∃ H : Head 3, computesBool nandFn H.residual := by
  exact ⟨Head.head1, Head.head1_computes_nand_residual⟩

/-- `OR` is computable with one head in the uniform multi-head model. -/
theorem or_computable_with_one_head_count :
    computableWithHeads orFn 1 := by
  refine ⟨3, (fun _ => Head.head1), ?_⟩
  convert Head.head1_computes_or_attnUpdate using 1
  funext ab
  simp [headFamilyAttnUpdate]

/-- `AND` is computable with one head in the uniform multi-head model. -/
theorem and_computable_with_one_head_count :
    computableWithHeads andFn 1 := by
  refine ⟨3, (fun _ => Head.head1), ?_⟩
  convert Head.head1_computes_and_attnUpdate using 1
  funext ab
  simp [headFamilyAttnUpdate]

/-- `NOR` is computable with one head in the uniform multi-head model. -/
theorem nor_computable_with_one_head_count :
    computableWithHeads norFn 1 := by
  refine ⟨3, (fun _ => Head.head1), ?_⟩
  convert Head.head1_computes_nor_attnUpdate using 1
  funext ab
  simp [headFamilyAttnUpdate]

/-- `NAND` is computable with one head in the uniform multi-head model. -/
theorem nand_computable_with_one_head_count :
    computableWithHeads nandFn 1 := by
  refine ⟨3, (fun _ => Head.head1), ?_⟩
  convert Head.head1_computes_nand_attnUpdate using 1
  funext ab
  simp [headFamilyAttnUpdate]

/-- A `0`-head model has constant output, so it cannot realize a target
    that is false on one input and true on another. -/
lemma not_computableWithHeads_zero_of_false_true
    (f : Bool × Bool → Bool) (abFalse abTrue : Bool × Bool)
    (hFalse : f abFalse = false) (hTrue : f abTrue = true) :
    ¬ computableWithHeads f 0 := by
  rintro ⟨d, Hs, w, τ, h⟩
  have h0 : (0 : ℝ) > τ ↔ f abFalse = true := by
    simpa [headFamilyAttnUpdate] using (h abFalse)
  have h1 : (0 : ℝ) > τ ↔ f abTrue = true := by
    simpa [headFamilyAttnUpdate] using (h abTrue)
  have hs : f abFalse = true ↔ f abTrue = true := h0.symm.trans h1
  have hF : f abFalse = true := hs.mpr hTrue
  exact Bool.false_ne_true (hFalse.symm.trans hF)

/-- `OR` is not computable with zero heads. -/
theorem or_not_computable_with_zero_heads :
    ¬ computableWithHeads orFn 0 := by
  exact not_computableWithHeads_zero_of_false_true orFn
    (false, false) (false, true) rfl rfl

/-- `AND` is not computable with zero heads. -/
theorem and_not_computable_with_zero_heads :
    ¬ computableWithHeads andFn 0 := by
  exact not_computableWithHeads_zero_of_false_true andFn
    (false, false) (true, true) rfl rfl

/-- `NOR` is not computable with zero heads. -/
theorem nor_not_computable_with_zero_heads :
    ¬ computableWithHeads norFn 0 := by
  exact not_computableWithHeads_zero_of_false_true norFn
    (false, true) (false, false) rfl rfl

/-- `NAND` is not computable with zero heads. -/
theorem nand_not_computable_with_zero_heads :
    ¬ computableWithHeads nandFn 0 := by
  exact not_computableWithHeads_zero_of_false_true nandFn
    (true, true) (false, false) rfl rfl

/-- No single head computes `XOR` in this model. -/
theorem xor_not_computable_with_one_head :
    ¬ ∃ (d : ℕ) (H : Head d), computesBool xorFn H.residual := by
  rintro ⟨d, H, hH⟩
  rw [← computesXor_iff_computesBool_xor] at hH
  exact one_head_cannot_xor_residual H hH

/-- General one-head lower bound for checkerboard truth tables. -/
theorem checkerboard_not_computable_with_one_head_attnUpdate
    {d : ℕ} (H : Head d) (f : Bool × Bool → Bool) (c : Bool)
    (h00 : f (false, false) = c)
    (h11 : f (true, true) = c)
    (h01 : f (false, true) = !c)
    (h10 : f (true, false) = !c) :
    ¬ computesBool f H.attnUpdate := by
  intro hComp
  let fN : (Fin 2 → Bool) → Bool := fun bits => f (bits 0, bits 1)
  have hCompN : computableWithHeadsN 2 1 fN := by
    refine ⟨d, fun _ => H.toNHead, ?_⟩
    rcases hComp with ⟨w, τ, hw⟩
    refine ⟨w, τ, ?_⟩
    intro bits
    simpa [fN, nHeadFamilyAttnUpdate] using hw (bits 0, bits 1)
  have h00N : fN (NHead.restrictBits (fun _ => false) 0 1 (false, false)) = c := by
    simpa [fN, NHead.restrictBits] using h00
  have h11N : fN (NHead.restrictBits (fun _ => false) 0 1 (true, true)) = c := by
    simpa [fN, NHead.restrictBits] using h11
  have h01N : fN (NHead.restrictBits (fun _ => false) 0 1 (false, true)) = !c := by
    simpa [fN, NHead.restrictBits] using h01
  have h10N : fN (NHead.restrictBits (fun _ => false) 0 1 (true, false)) = !c := by
    simpa [fN, NHead.restrictBits] using h10
  exact (checkerboard_restriction_not_computable_with_one_head
    fN (fun _ => false) 0 1 (by decide) c h00N h11N h01N h10N) hCompN

/-- Residual-form checkerboard lower bound. -/
theorem checkerboard_not_computable_with_one_head_residual
    {d : ℕ} (H : Head d) (f : Bool × Bool → Bool) (c : Bool)
    (h00 : f (false, false) = c)
    (h11 : f (true, true) = c)
    (h01 : f (false, true) = !c)
    (h10 : f (true, false) = !c) :
    ¬ computesBool f H.residual := by
  rw [computesBool_residual_iff_attnUpdate]
  exact checkerboard_not_computable_with_one_head_attnUpdate H f c h00 h11 h01 h10

/-- `XOR` is not computable with zero heads. -/
theorem xor_not_computable_with_zero_heads :
    ¬ computableWithHeads xorFn 0 := by
  exact not_computableWithHeads_zero_of_false_true xorFn
    (false, false) (false, true) rfl rfl

/-- `XOR` is not computable with a single head in the uniform multi-head model. -/
theorem xor_not_computable_with_one_head_count :
    ¬ computableWithHeads xorFn 1 := by
  rintro ⟨d, Hs, hH⟩
  have hSingle : computesBool xorFn ((headFamilyAttnUpdate Hs)) := hH
  rw [show headFamilyAttnUpdate Hs = (Hs 0).attnUpdate by
    funext ab
    simp [headFamilyAttnUpdate]] at hSingle
  rw [← computesXor_iff_computesBool_xor] at hSingle
  exact one_head_cannot_xor_attnUpdate (Hs 0) hSingle

/-- Two heads suffice to compute `XOR`. -/
theorem xor_computable_with_two_heads :
    computesBool xorFn (Head.twoHeadUpdate : Bool × Bool → Vec 3) := by
  rw [← computesXor_iff_computesBool_xor]
  exact Head.two_heads_suffice

/-- Negating the two-head probe separates `XNOR`. -/
theorem xnor_computable_with_two_heads :
    computesBool xnorFn (Head.twoHeadUpdate : Bool × Bool → Vec 3) := by
  let lo : ℝ := 2 * Real.exp 1 / (2 * Real.exp 1 + 1)
  let hi : ℝ := 2 * Real.exp 1 / (Real.exp 1 + 2)
  let τ : ℝ := -((lo + hi) / 2)
  have hgap : lo < hi := Head.xor_gap
  refine ⟨-Head.twoProbe, τ, ?_⟩
  rintro ⟨a, b⟩
  cases a <;> cases b
  · have hscore : ⟪-Head.twoProbe, Head.twoHeadUpdate (false, false)⟫_ℝ = -lo := by
      unfold Head.twoProbe
      rw [inner_neg_left]
      rw [Head.probe_score]
      simp [lo]
    rw [hscore]
    have hgt : -lo > τ := by
      dsimp [τ]
      linarith
    simp [xnorFn, xorFn, lo, hi, τ, hgt]
  · have hscore : ⟪-Head.twoProbe, Head.twoHeadUpdate (false, true)⟫_ℝ = -hi := by
      unfold Head.twoProbe
      rw [inner_neg_left]
      rw [Head.probe_score]
      simp [hi]
    rw [hscore]
    have hnot : ¬ -hi > τ := by
      dsimp [τ]
      linarith
    simp [xnorFn, xorFn, lo, hi, τ, hnot]
  · have hscore : ⟪-Head.twoProbe, Head.twoHeadUpdate (true, false)⟫_ℝ = -hi := by
      unfold Head.twoProbe
      rw [inner_neg_left]
      rw [Head.probe_score]
      simp [hi]
    rw [hscore]
    have hnot : ¬ -hi > τ := by
      dsimp [τ]
      linarith
    simp [xnorFn, xorFn, lo, hi, τ, hnot]
  · have hscore : ⟪-Head.twoProbe, Head.twoHeadUpdate (true, true)⟫_ℝ = -lo := by
      unfold Head.twoProbe
      rw [inner_neg_left]
      rw [Head.probe_score]
      simp [lo]
    rw [hscore]
    have hgt : -lo > τ := by
      dsimp [τ]
      linarith
    simp [xnorFn, xorFn, lo, hi, τ, hgt]

/-- A concrete 2-head family realizing the existing XOR construction. -/
noncomputable def xorTwoHeadFamily : HeadFamily 3 2
  | 0 => Head.head0
  | 1 => Head.head1

lemma xorTwoHeadFamily_attnUpdate (ab : Bool × Bool) :
    headFamilyAttnUpdate xorTwoHeadFamily ab = Head.twoHeadUpdate ab := by
  simp [headFamilyAttnUpdate, xorTwoHeadFamily, Head.twoHeadUpdate, Fin.sum_univ_two]

/-- `XOR` is computable with two heads in the uniform multi-head model. -/
theorem xor_computable_with_two_heads_count :
    computableWithHeads xorFn 2 := by
  refine ⟨3, xorTwoHeadFamily, ?_⟩
  convert xor_computable_with_two_heads using 1
  funext ab
  exact xorTwoHeadFamily_attnUpdate ab

/-- `XNOR` is not computable with one head. -/
theorem xnor_not_computable_with_one_head_count :
    ¬ computableWithHeads xnorFn 1 := by
  rintro ⟨d, Hs, hH⟩
  have hSingle : computesBool xnorFn ((headFamilyAttnUpdate Hs)) := hH
  rw [show headFamilyAttnUpdate Hs = (Hs 0).attnUpdate by
    funext ab
    simp [headFamilyAttnUpdate]] at hSingle
  exact (checkerboard_not_computable_with_one_head_attnUpdate
    (Hs 0) xnorFn true rfl rfl rfl rfl) hSingle

/-- `XNOR` is computable with two heads. -/
theorem xnor_computable_with_two_heads_count :
    computableWithHeads xnorFn 2 := by
  refine ⟨3, xorTwoHeadFamily, ?_⟩
  convert xnor_computable_with_two_heads using 1
  funext ab
  exact xorTwoHeadFamily_attnUpdate ab

/-- Exact head complexity of `OR` in the current formalization. -/
theorem exactHeadComplexity_or :
    exactHeadComplexity orFn 1 := by
  constructor
  · exact or_computable_with_one_head_count
  · intro h hk
    have : h = 0 := by omega
    subst this
    exact or_not_computable_with_zero_heads

/-- Exact head complexity of `AND` in the current formalization. -/
theorem exactHeadComplexity_and :
    exactHeadComplexity andFn 1 := by
  constructor
  · exact and_computable_with_one_head_count
  · intro h hk
    have : h = 0 := by omega
    subst this
    exact and_not_computable_with_zero_heads

/-- Exact head complexity of `XOR` in the current formalization. -/
theorem exactHeadComplexity_xor :
    exactHeadComplexity xorFn 2 := by
  constructor
  · exact xor_computable_with_two_heads_count
  · intro h hk
    have hCases : h = 0 ∨ h = 1 := by omega
    rcases hCases with h0 | h1
    · subst h0
      exact xor_not_computable_with_zero_heads
    · subst h1
      exact xor_not_computable_with_one_head_count

/-- Exact head complexity of the constantly-false function. -/
theorem exactHeadComplexity_false :
    exactHeadComplexity falseFn 0 := by
  constructor
  · exact false_computable_with_zero_heads
  · intro h hh
    omega

/-- Exact head complexity of the constantly-true function. -/
theorem exactHeadComplexity_true :
    exactHeadComplexity trueFn 0 := by
  constructor
  · exact true_computable_with_zero_heads
  · intro h hh
    omega

/-- Exact head complexity of `NOR`. -/
theorem exactHeadComplexity_nor :
    exactHeadComplexity norFn 1 := by
  constructor
  · exact nor_computable_with_one_head_count
  · intro h hk
    have : h = 0 := by omega
    subst this
    exact nor_not_computable_with_zero_heads

/-- Exact head complexity of `NAND`. -/
theorem exactHeadComplexity_nand :
    exactHeadComplexity nandFn 1 := by
  constructor
  · exact nand_computable_with_one_head_count
  · intro h hk
    have : h = 0 := by omega
    subst this
    exact nand_not_computable_with_zero_heads

/-- Exact head complexity of `XNOR`. -/
theorem exactHeadComplexity_xnor :
    exactHeadComplexity xnorFn 2 := by
  constructor
  · exact xnor_computable_with_two_heads_count
  · intro h hk
    have hCases : h = 0 ∨ h = 1 := by omega
    rcases hCases with h0 | h1
    · subst h0
      exact not_computableWithHeads_zero_of_false_true xnorFn
        (false, true) (false, false) rfl rfl
    · subst h1
      exact xnor_not_computable_with_one_head_count

theorem HStar_false : HStar falseFn = 0 := HStar_eq_of_exact exactHeadComplexity_false
theorem HStar_true : HStar trueFn = 0 := HStar_eq_of_exact exactHeadComplexity_true
theorem HStar_or : HStar orFn = 1 := HStar_eq_of_exact exactHeadComplexity_or
theorem HStar_and : HStar andFn = 1 := HStar_eq_of_exact exactHeadComplexity_and
theorem HStar_nor : HStar norFn = 1 := HStar_eq_of_exact exactHeadComplexity_nor
theorem HStar_nand : HStar nandFn = 1 := HStar_eq_of_exact exactHeadComplexity_nand
theorem HStar_xor : HStar xorFn = 2 := HStar_eq_of_exact exactHeadComplexity_xor
theorem HStar_xnor : HStar xnorFn = 2 := HStar_eq_of_exact exactHeadComplexity_xnor

/-- Classification of all symmetric 2-bit Boolean functions by exact
    head complexity. -/
theorem exactHeadComplexity_symmFn (c0 c1 c2 : Bool) :
    exactHeadComplexity (symmFn c0 c1 c2)
      (if c0 = c1 then if c1 = c2 then 0 else 1 else if c0 = c2 then 2 else 1) := by
  cases c0 <;> cases c1 <;> cases c2 <;>
    simp only [Bool.false_eq_true, Bool.true_eq_false, ↓reduceIte]
  · have hs : symmFn false false false = falseFn := by
      funext ab; rcases ab with ⟨a, b⟩; cases a <;> cases b <;> rfl
    rw [hs]
    exact exactHeadComplexity_false
  · have hs : symmFn false false true = andFn := by
      funext ab; rcases ab with ⟨a, b⟩; cases a <;> cases b <;> rfl
    rw [hs]
    exact exactHeadComplexity_and
  · have hs : symmFn false true false = xorFn := by
      funext ab; rcases ab with ⟨a, b⟩; cases a <;> cases b <;> rfl
    rw [hs]
    exact exactHeadComplexity_xor
  · have hs : symmFn false true true = orFn := by
      funext ab; rcases ab with ⟨a, b⟩; cases a <;> cases b <;> rfl
    rw [hs]
    exact exactHeadComplexity_or
  · have hs : symmFn true false false = norFn := by
      funext ab; rcases ab with ⟨a, b⟩; cases a <;> cases b <;> rfl
    rw [hs]
    exact exactHeadComplexity_nor
  · have hs : symmFn true false true = xnorFn := by
      funext ab; rcases ab with ⟨a, b⟩; cases a <;> cases b <;> rfl
    rw [hs]
    exact exactHeadComplexity_xnor
  · have hs : symmFn true true false = nandFn := by
      funext ab; rcases ab with ⟨a, b⟩; cases a <;> cases b <;> rfl
    rw [hs]
    exact exactHeadComplexity_nand
  · have hs : symmFn true true true = trueFn := by
      funext ab; rcases ab with ⟨a, b⟩; cases a <;> cases b <;> rfl
    rw [hs]
    exact exactHeadComplexity_true

/-- Equivalent explicit `HStar` classification for the symmetric 2-bit family. -/
theorem HStar_symmFn (c0 c1 c2 : Bool) :
    HStar (symmFn c0 c1 c2)
      = (if c0 = c1 then if c1 = c2 then 0 else 1 else if c0 = c2 then 2 else 1) := by
  have := exactHeadComplexity_symmFn c0 c1 c2
  exact HStar_eq_of_exact this

end HeadComplexity
