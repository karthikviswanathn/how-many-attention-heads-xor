import HeadComplexity.UpperBound
import HeadComplexity.PartialFraction
import Mathlib.LinearAlgebra.Lagrange

/-!
# Lemma 9 — weighted-sum interpolation upper bound.

If `f(x) = F(t(x))` for a positive weighted sum `t(x) = ∑ λ_i x_i` with image of
size `M`, then `H*(f) ≤ M - 1`.

The head construction generalizes `atomHead`: with `d = 2`, `W_Q = W_K = W_V = id`,
score channel `0`, value channel `1`, and `s = √(log (a - Λ))` (`Λ = ∑ λ_i`):

* `posEmbed (some i) = single 0 (log λ_i / s)` injects `log λ_i` into position `i`'s
  logit, so the softmax weight there is `λ_i` (bit 0) or `2 λ_i` (bit 1);
* the query token has logit `s² = log (a - Λ)`, weight `a - Λ`.

Hence the denominator is `∑_i (λ_i + λ_i x_i) + (a - Λ) = t(x) + a`, and the readout
`⟪e₁, ·⟫` of the numerator is the constant `b`, so `⟪e₁, attnUpdate x⟫ = b/(t(x)+a)`.
Reusing `real_partial_fraction` and a Lagrange sign polynomial gives the `M-1` heads.
-/

namespace HeadComplexity

open MvPolynomial Finset NHead
open scoped BigOperators InnerProductSpace

variable {n : ℕ}

/-- Total weight `Λ = ∑ λ_i`. -/
noncomputable def wLam (lam : Fin n → ℝ) : ℝ := ∑ i, lam i

/-- Weighted statistic `t(x) = ∑_{i : x_i} λ_i`. -/
noncomputable def wT (lam : Fin n → ℝ) (bits : Fin n → Bool) : ℝ := ∑ i, if bits i then lam i else 0

/-- Score scale `s = √(log (a - Λ))`. -/
noncomputable def wScore (lam : Fin n → ℝ) (a : ℝ) : ℝ := Real.sqrt (Real.log (a - wLam lam))

/-- Token embedding of the weighted atom head. -/
noncomputable def wTok (lam : Fin n → ℝ) (a b : ℝ) : Fin 3 → Vec 2 :=
  ![ EuclideanSpace.single 1 (b / wLam lam),
     EuclideanSpace.single 0 (Real.log 2 / wScore lam a)
       + EuclideanSpace.single 1 (b / (2 * wLam lam)),
     EuclideanSpace.single 0 (wScore lam a) ]

/-- Positional embedding: position `i` carries `log λ_i / s` in the score channel. -/
noncomputable def wPos (lam : Fin n → ℝ) (a : ℝ) : SeqPos n → Vec 2
  | some i => EuclideanSpace.single 0 (Real.log (lam i) / wScore lam a)
  | none => 0

/-- The weighted atom head over `n` bits. -/
noncomputable def weightedAtomHead (lam : Fin n → ℝ) (a b : ℝ) : NHead n 2 where
  tokenEmbed := wTok lam a b
  posEmbed := wPos lam a
  WQ := LinearMap.id
  WK := LinearMap.id
  WV := LinearMap.id

section
variable (lam : Fin n → ℝ) (a b : ℝ)

@[simp] lemma wTok_zero_coord0 : wTok lam a b 0 0 = 0 := by simp [wTok]
@[simp] lemma wTok_one_coord0 : wTok lam a b 1 0 = Real.log 2 / wScore lam a := by simp [wTok]
@[simp] lemma wTok_two_coord0 : wTok lam a b 2 0 = wScore lam a := by simp [wTok]
@[simp] lemma wTok_zero_coord1 : wTok lam a b 0 1 = b / wLam lam := by simp [wTok]
@[simp] lemma wTok_one_coord1 : wTok lam a b 1 1 = b / (2 * wLam lam) := by simp [wTok]
@[simp] lemma wTok_two_coord1 : wTok lam a b 2 1 = 0 := by simp [wTok]

@[simp] lemma weightedAtomHead_WK : (weightedAtomHead lam a b).WK = LinearMap.id := rfl
@[simp] lemma weightedAtomHead_WQ : (weightedAtomHead lam a b).WQ = LinearMap.id := rfl
@[simp] lemma weightedAtomHead_WV : (weightedAtomHead lam a b).WV = LinearMap.id := rfl

/-- The query embedding equals `tokenEmbed 2` (positional part is zero). -/
lemma wHead_x_none (bits : Fin n → Bool) :
    (weightedAtomHead lam a b).x bits none = wTok lam a b 2 := by
  simp [NHead.x, NHead.seqTok, weightedAtomHead, wPos]

/-- Score-channel coordinate of position `i`. -/
lemma wHead_x_some_coord0 (bits : Fin n → Bool) (i : Fin n) :
    ((weightedAtomHead lam a b).x bits (some i)) 0
      = wTok lam a b (cond (bits i) 1 0) 0 + Real.log (lam i) / wScore lam a := by
  simp only [NHead.x, NHead.seqTok, weightedAtomHead, wPos]
  rw [PiLp.add_apply, PiLp.single_apply]
  simp

/-- Value-channel coordinate of position `i` (unaffected by `posEmbed`). -/
lemma wHead_x_some_coord1 (bits : Fin n → Bool) (i : Fin n) :
    ((weightedAtomHead lam a b).x bits (some i)) 1
      = wTok lam a b (cond (bits i) 1 0) 1 := by
  simp only [NHead.x, NHead.seqTok, weightedAtomHead, wPos]
  rw [PiLp.add_apply, PiLp.single_apply]
  simp

/-- Readout `⟪e₁, ·⟫` reads the value channel (coordinate `1`). -/
lemma wReadout_inner (v : Vec 2) : ⟪atomReadout, v⟫_ℝ = v 1 := by
  rw [atomReadout, vec2_inner]; simp

end

section
variable (lam : Fin n → ℝ) (a b : ℝ) (hn : 1 ≤ n) (hlam : ∀ i, 0 < lam i)
  (ha : wLam lam + 1 < a)

include hn hlam in
private lemma wLam_pos : 0 < wLam lam := by
  unfold wLam
  obtain ⟨i⟩ := Fin.pos_iff_nonempty.mp hn
  exact Finset.sum_pos (fun i _ => hlam i) ⟨i, Finset.mem_univ i⟩

include ha in
private lemma wa_sub_pos : 0 < a - wLam lam := by linarith

include ha in
private lemma wlog_pos : 0 < Real.log (a - wLam lam) := by
  apply Real.log_pos; linarith

include ha in
private lemma wScore_ne : wScore lam a ≠ 0 := by
  have := wlog_pos lam a ha
  unfold wScore; positivity

include ha in
private lemma wScore_sq : wScore lam a * wScore lam a = Real.log (a - wLam lam) := by
  unfold wScore
  exact Real.mul_self_sqrt (le_of_lt (wlog_pos lam a ha))

include ha in
/-- Softmax weight at the query token is `a - Λ`. -/
lemma wHead_sigma_none (bits : Fin n → Bool) :
    (weightedAtomHead lam a b).sigma bits none = a - wLam lam := by
  unfold NHead.sigma
  rw [wHead_x_none]
  simp only [weightedAtomHead_WK, weightedAtomHead_WQ, LinearMap.id_coe, id_eq]
  rw [vec2_inner]
  simp only [wTok_two_coord0, wTok_two_coord1, mul_zero, add_zero]
  rw [wScore_sq lam a ha, Real.exp_log (wa_sub_pos lam a ha)]

include hlam ha in
/-- Softmax weight at position `i`: `2 λ_i` if the bit is set, else `λ_i`. -/
lemma wHead_sigma_some (bits : Fin n → Bool) (i : Fin n) :
    (weightedAtomHead lam a b).sigma bits (some i) = if bits i then 2 * lam i else lam i := by
  have hs := wScore_ne lam a ha
  unfold NHead.sigma
  rw [wHead_x_none]
  simp only [weightedAtomHead_WK, weightedAtomHead_WQ, LinearMap.id_coe, id_eq]
  rw [vec2_inner]
  simp only [wTok_two_coord0, wTok_two_coord1, mul_zero, add_zero]
  rw [wHead_x_some_coord0]
  cases bits i with
  | false =>
      simp only [cond_false, wTok_zero_coord0, zero_add]
      rw [div_mul_cancel₀ _ hs, Real.exp_log (hlam i)]
      simp
  | true =>
      simp only [cond_true, wTok_one_coord0]
      rw [← add_div, div_mul_cancel₀ _ hs,
        show Real.log 2 + Real.log (lam i) = Real.log (2 * lam i) from
          (Real.log_mul (by norm_num) (hlam i).ne').symm,
        Real.exp_log (mul_pos (by norm_num) (hlam i))]
      simp

/-- The value vector equals the embedding (since `W_V = id`). -/
lemma wHead_value (bits : Fin n → Bool) (p : SeqPos n) :
    (weightedAtomHead lam a b).value bits p = (weightedAtomHead lam a b).x bits p := by
  simp [NHead.value, weightedAtomHead]

include hlam ha in
/-- Denominator is `t(x) + a`. -/
lemma wHead_denom (bits : Fin n → Bool) :
    (weightedAtomHead lam a b).denominator bits = wT lam bits + a := by
  unfold NHead.denominator
  rw [Fintype.sum_option, wHead_sigma_none lam a b ha]
  have hsome : ∀ i, (weightedAtomHead lam a b).sigma bits (some i)
      = lam i + (if bits i then lam i else 0) := by
    intro i; rw [wHead_sigma_some lam a b hlam ha]; cases bits i <;> simp; ring
  simp_rw [hsome]
  rw [Finset.sum_add_distrib]
  unfold wT wLam
  ring

include hn hlam ha in
/-- Readout `⟪e₁, ·⟫` of the numerator is the constant `b`. -/
lemma wHead_numread (bits : Fin n → Bool) :
    ⟪atomReadout, (weightedAtomHead lam a b).numerator bits⟫_ℝ = b := by
  have hL := (wLam_pos lam hn hlam).ne'
  unfold NHead.numerator
  rw [inner_sum, Fintype.sum_option]
  simp_rw [inner_smul_right, wHead_value]
  have hquery : ⟪atomReadout, (weightedAtomHead lam a b).x bits none⟫_ℝ = 0 := by
    rw [wHead_x_none, wReadout_inner, wTok_two_coord1]
  rw [hquery, mul_zero, zero_add]
  have hbit : ∀ i, (weightedAtomHead lam a b).sigma bits (some i)
        * ⟪atomReadout, (weightedAtomHead lam a b).x bits (some i)⟫_ℝ = b * lam i / wLam lam := by
    intro i
    rw [wHead_sigma_some lam a b hlam ha, wReadout_inner, wHead_x_some_coord1]
    cases bits i <;> simp <;> ring
  rw [Finset.sum_congr rfl (fun i _ => hbit i)]
  rw [← Finset.sum_div, ← Finset.mul_sum, show ∑ i, lam i = wLam lam from rfl,
    mul_div_assoc, div_self hL, mul_one]

include hn hlam ha in
/-- **One weighted head = one atom `b/(t(x)+a)`.** -/
theorem weightedAtom_readout (bits : Fin n → Bool) :
    ⟪atomReadout, (weightedAtomHead lam a b).attnUpdate bits⟫_ℝ = b / (wT lam bits + a) := by
  unfold NHead.attnUpdate
  rw [inner_smul_right, wHead_numread lam a b hn hlam ha, wHead_denom lam a b hlam ha]
  rw [div_eq_mul_inv, mul_comm]

end

end HeadComplexity
