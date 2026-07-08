import HeadComplexity.Examples.Head
import HeadComplexity.Examples.OneHead

set_option linter.style.header false

/-!
# Theorem 2: two attention heads suffice to compute XOR.

We give an explicit two-head construction matching the table in
`writeup.md`. Both heads work in `Vec 3` with token embeddings
`e_0 = (1,0,0)`, `e_1 = (0,1,0)`, `e_= = (0,0,1)` and no positional
embeddings. Head 0 attends preferentially to token `0` and writes in
the `e_0` direction; Head 1 attends preferentially to token `1` and
writes in the `e_1` direction. Their sum places the four attention
outputs into a configuration where the linear probe `e_0 + e_1`
separates the XOR-positive inputs from the XOR-negative inputs.
-/

namespace HeadComplexity

open scoped InnerProductSpace

/-- Outer product of two vectors as a linear map: `(u v^T)(w) = ⟨v, w⟩ u`. -/
noncomputable def outerProduct {n : ℕ} (u v : Vec n) : Vec n →ₗ[ℝ] Vec n where
  toFun w := ⟪v, w⟫_ℝ • u
  map_add' x y := by
    simp only [inner_add_right, add_smul]
  map_smul' c x := by
    simp only [inner_smul_right, RingHom.id_apply, smul_smul]

@[simp] lemma outerProduct_apply {n : ℕ} (u v w : Vec n) :
    outerProduct u v w = ⟪v, w⟫_ℝ • u := rfl

namespace Head

/-- The standard token embedding for the construction:
    `e_0 = (1,0,0)`, `e_1 = (0,1,0)`, `e_= = (0,0,1)`. -/
noncomputable def stdTokenEmbed : Fin 3 → Vec 3 := fun i => EuclideanSpace.single i 1

/-- **Head 0**: attends to token `0`, writes in the `e_0` direction. -/
noncomputable def head0 : Head 3 where
  tokenEmbed := stdTokenEmbed
  posEmbed := fun _ => 0
  WQ := LinearMap.id
  WK := outerProduct (EuclideanSpace.single 2 1) (EuclideanSpace.single 0 1)
  WV := outerProduct (EuclideanSpace.single 0 1) (EuclideanSpace.single 0 1)

/-- **Head 1**: attends to token `1`, writes in the `e_1` direction. -/
noncomputable def head1 : Head 3 where
  tokenEmbed := stdTokenEmbed
  posEmbed := fun _ => 0
  WQ := LinearMap.id
  WK := outerProduct (EuclideanSpace.single 2 1) (EuclideanSpace.single 1 1)
  WV := outerProduct (EuclideanSpace.single 1 1) (EuclideanSpace.single 1 1)

/-- The combined two-head attention update used in the `computesXor`
target. -/
noncomputable def twoHeadUpdate (ab : Bool × Bool) : Vec 3 :=
  head0.attnUpdate ab + head1.attnUpdate ab

/-! ### Helper unfolding lemmas

These let `simp` chew through the head construction without unfolding
the record itself. -/

@[simp] lemma stdTokenEmbed_apply (i : Fin 3) :
    stdTokenEmbed i = EuclideanSpace.single i 1 := rfl

@[simp] lemma head0_tokenEmbed : head0.tokenEmbed = stdTokenEmbed := rfl
@[simp] lemma head0_posEmbed : head0.posEmbed = (fun _ : Fin 3 => (0 : Vec 3)) := rfl
@[simp] lemma head0_WQ : head0.WQ = LinearMap.id := rfl
@[simp] lemma head0_WK :
    head0.WK = outerProduct (EuclideanSpace.single 2 1) (EuclideanSpace.single 0 1) := rfl
@[simp] lemma head0_WV :
    head0.WV = outerProduct (EuclideanSpace.single 0 1) (EuclideanSpace.single 0 1) := rfl

@[simp] lemma head1_tokenEmbed : head1.tokenEmbed = stdTokenEmbed := rfl
@[simp] lemma head1_posEmbed : head1.posEmbed = (fun _ : Fin 3 => (0 : Vec 3)) := rfl
@[simp] lemma head1_WQ : head1.WQ = LinearMap.id := rfl
@[simp] lemma head1_WK :
    head1.WK = outerProduct (EuclideanSpace.single 2 1) (EuclideanSpace.single 1 1) := rfl
@[simp] lemma head1_WV :
    head1.WV = outerProduct (EuclideanSpace.single 1 1) (EuclideanSpace.single 1 1) := rfl

@[simp] lemma head0_x_apply (ab : Bool × Bool) (j : Fin 3) :
    head0.x ab j = EuclideanSpace.single (seqTok ab j) 1 := by
  change head0.tokenEmbed (seqTok ab j) + head0.posEmbed j = _
  simp

@[simp] lemma head1_x_apply (ab : Bool × Bool) (j : Fin 3) :
    head1.x ab j = EuclideanSpace.single (seqTok ab j) 1 := by
  change head1.tokenEmbed (seqTok ab j) + head1.posEmbed j = _
  simp

/-- Inner product of two standard basis vectors of `Vec n`: `1` on the
diagonal and `0` off-diagonal. -/
@[simp] lemma inner_single_single {n : ℕ} (i j : Fin n) :
    ⟪(EuclideanSpace.single i (1 : ℝ)), EuclideanSpace.single j (1 : ℝ)⟫_ℝ
    = if i = j then (1 : ℝ) else 0 := by
  rw [← EuclideanSpace.basisFun_apply (Fin n) ℝ i,
      ← EuclideanSpace.basisFun_apply (Fin n) ℝ j]
  exact (EuclideanSpace.basisFun (Fin n) ℝ).inner_eq_ite i j

/-! ### Per-head attention updates on each of the four inputs -/

private lemma exp_pos' : (0 : ℝ) < Real.exp 1 := Real.exp_pos _

private lemma two_exp_one_add_one_pos : (0 : ℝ) < 2 * Real.exp 1 + 1 := by
  have := exp_pos'
  linarith

private lemma exp_one_add_two_pos : (0 : ℝ) < Real.exp 1 + 2 := by
  have := exp_pos'
  linarith

/-- `head0.attnUpdate (false, false) = (2e/(2e+1)) • e_0`. -/
lemma head0_attnUpdate_ff_ff :
    head0.attnUpdate (false, false) =
    (2 * Real.exp 1 / (2 * Real.exp 1 + 1)) • EuclideanSpace.single (0 : Fin 3) 1 := by
  have hD : head0.denominator (false, false) = 2 * Real.exp 1 + 1 := by
    unfold Head.denominator Head.sigma
    simp [Fin.sum_univ_three, seqTok]; ring
  have hN : head0.numerator (false, false)
      = (2 * Real.exp 1) • EuclideanSpace.single (0 : Fin 3) 1 := by
    unfold Head.numerator Head.sigma Head.value
    simp [Fin.sum_univ_three, seqTok]
    module
  unfold Head.attnUpdate
  rw [hD, hN, smul_smul]
  congr 1
  rw [div_eq_mul_inv, mul_comm]

/-- `head0.attnUpdate (false, true) = (e/(e+2)) • e_0`. -/
lemma head0_attnUpdate_ff_tt :
    head0.attnUpdate (false, true) =
    (Real.exp 1 / (Real.exp 1 + 2)) • EuclideanSpace.single (0 : Fin 3) 1 := by
  have hD : head0.denominator (false, true) = Real.exp 1 + 2 := by
    unfold Head.denominator Head.sigma
    simp [Fin.sum_univ_three, seqTok]; ring
  have hN : head0.numerator (false, true)
      = (Real.exp 1) • EuclideanSpace.single (0 : Fin 3) 1 := by
    unfold Head.numerator Head.sigma Head.value
    simp [Fin.sum_univ_three, seqTok]
  unfold Head.attnUpdate
  rw [hD, hN, smul_smul]
  congr 1
  rw [div_eq_mul_inv, mul_comm]

/-- `head0.attnUpdate (true, false) = (e/(e+2)) • e_0`. -/
lemma head0_attnUpdate_tt_ff :
    head0.attnUpdate (true, false) =
    (Real.exp 1 / (Real.exp 1 + 2)) • EuclideanSpace.single (0 : Fin 3) 1 := by
  have hD : head0.denominator (true, false) = Real.exp 1 + 2 := by
    unfold Head.denominator Head.sigma
    simp [Fin.sum_univ_three, seqTok]; ring
  have hN : head0.numerator (true, false)
      = (Real.exp 1) • EuclideanSpace.single (0 : Fin 3) 1 := by
    unfold Head.numerator Head.sigma Head.value
    simp [Fin.sum_univ_three, seqTok]
  unfold Head.attnUpdate
  rw [hD, hN, smul_smul]
  congr 1
  rw [div_eq_mul_inv, mul_comm]

/-- `head0.attnUpdate (true, true) = 0`. -/
lemma head0_attnUpdate_tt_tt :
    head0.attnUpdate (true, true) = (0 : Vec 3) := by
  have hN : head0.numerator (true, true) = (0 : Vec 3) := by
    unfold Head.numerator Head.sigma Head.value
    simp [Fin.sum_univ_three, seqTok]
  unfold Head.attnUpdate
  rw [hN, smul_zero]

/-- `head1.attnUpdate (false, false) = 0`. -/
lemma head1_attnUpdate_ff_ff :
    head1.attnUpdate (false, false) = (0 : Vec 3) := by
  have hN : head1.numerator (false, false) = (0 : Vec 3) := by
    unfold Head.numerator Head.sigma Head.value
    simp [Fin.sum_univ_three, seqTok]
  unfold Head.attnUpdate
  rw [hN, smul_zero]

/-- `head1.attnUpdate (false, true) = (e/(e+2)) • e_1`. -/
lemma head1_attnUpdate_ff_tt :
    head1.attnUpdate (false, true) =
    (Real.exp 1 / (Real.exp 1 + 2)) • EuclideanSpace.single (1 : Fin 3) 1 := by
  have hD : head1.denominator (false, true) = Real.exp 1 + 2 := by
    unfold Head.denominator Head.sigma
    simp [Fin.sum_univ_three, seqTok]; ring
  have hN : head1.numerator (false, true)
      = (Real.exp 1) • EuclideanSpace.single (1 : Fin 3) 1 := by
    unfold Head.numerator Head.sigma Head.value
    simp [Fin.sum_univ_three, seqTok]
  unfold Head.attnUpdate
  rw [hD, hN, smul_smul]
  congr 1
  rw [div_eq_mul_inv, mul_comm]

/-- `head1.attnUpdate (true, false) = (e/(e+2)) • e_1`. -/
lemma head1_attnUpdate_tt_ff :
    head1.attnUpdate (true, false) =
    (Real.exp 1 / (Real.exp 1 + 2)) • EuclideanSpace.single (1 : Fin 3) 1 := by
  have hD : head1.denominator (true, false) = Real.exp 1 + 2 := by
    unfold Head.denominator Head.sigma
    simp [Fin.sum_univ_three, seqTok]; ring
  have hN : head1.numerator (true, false)
      = (Real.exp 1) • EuclideanSpace.single (1 : Fin 3) 1 := by
    unfold Head.numerator Head.sigma Head.value
    simp [Fin.sum_univ_three, seqTok]
  unfold Head.attnUpdate
  rw [hD, hN, smul_smul]
  congr 1
  rw [div_eq_mul_inv, mul_comm]

/-- `head1.attnUpdate (true, true) = (2e/(2e+1)) • e_1`. -/
lemma head1_attnUpdate_tt_tt :
    head1.attnUpdate (true, true) =
    (2 * Real.exp 1 / (2 * Real.exp 1 + 1)) • EuclideanSpace.single (1 : Fin 3) 1 := by
  have hD : head1.denominator (true, true) = 2 * Real.exp 1 + 1 := by
    unfold Head.denominator Head.sigma
    simp [Fin.sum_univ_three, seqTok]; ring
  have hN : head1.numerator (true, true)
      = (2 * Real.exp 1) • EuclideanSpace.single (1 : Fin 3) 1 := by
    unfold Head.numerator Head.sigma Head.value
    simp [Fin.sum_univ_three, seqTok]
    module
  unfold Head.attnUpdate
  rw [hD, hN, smul_smul]
  congr 1
  rw [div_eq_mul_inv, mul_comm]

/-! ### Combined two-head outputs -/

/-- The combined update on `(ff, ff)`: only Head 0 contributes. -/
lemma twoHead_ff_ff :
    twoHeadUpdate (false, false) =
    (2 * Real.exp 1 / (2 * Real.exp 1 + 1)) • EuclideanSpace.single (0 : Fin 3) 1 := by
  unfold twoHeadUpdate
  rw [head0_attnUpdate_ff_ff, head1_attnUpdate_ff_ff, add_zero]

/-- The combined update on `(ff, tt)`: both heads contribute. -/
lemma twoHead_ff_tt :
    twoHeadUpdate (false, true) =
    (Real.exp 1 / (Real.exp 1 + 2)) •
      (EuclideanSpace.single (0 : Fin 3) 1 + EuclideanSpace.single (1 : Fin 3) 1) := by
  unfold twoHeadUpdate
  rw [head0_attnUpdate_ff_tt, head1_attnUpdate_ff_tt, smul_add]

/-- The combined update on `(tt, ff)`: both heads contribute. -/
lemma twoHead_tt_ff :
    twoHeadUpdate (true, false) =
    (Real.exp 1 / (Real.exp 1 + 2)) •
      (EuclideanSpace.single (0 : Fin 3) 1 + EuclideanSpace.single (1 : Fin 3) 1) := by
  unfold twoHeadUpdate
  rw [head0_attnUpdate_tt_ff, head1_attnUpdate_tt_ff, smul_add]

/-- The combined update on `(tt, tt)`: only Head 1 contributes. -/
lemma twoHead_tt_tt :
    twoHeadUpdate (true, true) =
    (2 * Real.exp 1 / (2 * Real.exp 1 + 1)) • EuclideanSpace.single (1 : Fin 3) 1 := by
  unfold twoHeadUpdate
  rw [head0_attnUpdate_tt_tt, head1_attnUpdate_tt_tt, zero_add]

/-! ### Probe score, gap, and the main theorem -/

/-- The linear probe `e_0 + e_1` evaluated on `twoHeadUpdate ab`:
takes one of two values, separating XOR-positive from XOR-negative
inputs. -/
lemma probe_score (ab : Bool × Bool) :
    ⟪EuclideanSpace.single (0 : Fin 3) 1 + EuclideanSpace.single (1 : Fin 3) 1,
      twoHeadUpdate ab⟫_ℝ =
    if (xor ab.1 ab.2) = true then 2 * Real.exp 1 / (Real.exp 1 + 2)
                              else 2 * Real.exp 1 / (2 * Real.exp 1 + 1) := by
  rcases ab with ⟨a, b⟩
  cases a <;> cases b
  · -- (false, false)
    rw [twoHead_ff_ff]
    simp [inner_add_left, inner_smul_right]
  · -- (false, true)
    rw [twoHead_ff_tt]
    simp [inner_add_left, inner_smul_right, inner_add_right]
    ring
  · -- (true, false)
    rw [twoHead_tt_ff]
    simp [inner_add_left, inner_smul_right, inner_add_right]
    ring
  · -- (true, true)
    rw [twoHead_tt_tt]
    simp [inner_add_left, inner_smul_right]

/-- The strict gap between the two probe values: the off-diagonal value
`2e/(e+2)` strictly exceeds the diagonal value `2e/(2e+1)`. This is
where the inequality `Real.exp 1 > 1` comes in. -/
lemma xor_gap :
    2 * Real.exp 1 / (2 * Real.exp 1 + 1) < 2 * Real.exp 1 / (Real.exp 1 + 2) := by
  have he : (1 : ℝ) < Real.exp 1 := Real.one_lt_exp_iff.mpr one_pos
  rw [div_lt_div_iff₀ two_exp_one_add_one_pos exp_one_add_two_pos]
  nlinarith [exp_pos']

/-- **Theorem 2.** The two-head construction `twoHeadUpdate` computes
XOR with the linear readout `w = e_0 + e_1` and any threshold strictly
between `2e/(2e+1)` and `2e/(e+2)`. -/
theorem two_heads_suffice :
    computesXor (twoHeadUpdate : Bool × Bool → Vec 3) := by
  set τ := (2 * Real.exp 1 / (2 * Real.exp 1 + 1)
            + 2 * Real.exp 1 / (Real.exp 1 + 2)) / 2 with hτ_def
  have hgap := xor_gap
  have h_lo : 2 * Real.exp 1 / (2 * Real.exp 1 + 1) < τ := by
    rw [hτ_def]; linarith
  have h_hi : τ < 2 * Real.exp 1 / (Real.exp 1 + 2) := by
    rw [hτ_def]; linarith
  refine ⟨EuclideanSpace.single (0 : Fin 3) 1 + EuclideanSpace.single (1 : Fin 3) 1,
          τ, fun ab => ?_⟩
  rw [probe_score]
  rcases ab with ⟨a, b⟩
  cases a <;> cases b <;> simp <;> linarith

end Head

end HeadComplexity
