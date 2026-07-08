import HeadComplexity.Examples.Head
import HeadComplexity.Model.NHead

set_option linter.style.header false

/-!
# Bridge from the two-bit example model to the generalized model.

This file keeps the legacy `Head` API usable for the examples while
preserving the dependency direction: examples may import the generalized
model, but `Model.NHead` does not import example-only definitions.
-/

namespace HeadComplexity

/-- Convert a Boolean pair into a 2-bit input function. -/
def pairToBits (ab : Bool × Bool) : Fin 2 → Bool
  | 0 => ab.1
  | 1 => ab.2

/-- The three positions of the old `(a, b, =)` model, viewed inside the
    generalized `n = 2` position type. -/
def seqPosToFin3 : SeqPos 2 → Fin 3
  | some 0 => 0
  | some 1 => 1
  | none => 2

namespace Head

variable {d : ℕ}

/-- Reinterpret the original 2-bit `Head` model as a generalized
    `NHead 2`. -/
def toNHead (H : Head d) : NHead 2 d where
  tokenEmbed := H.tokenEmbed
  posEmbed := H.posEmbed ∘ seqPosToFin3
  WQ := H.WQ
  WK := H.WK
  WV := H.WV

@[simp] lemma toNHead_posEmbed (H : Head d) (p : SeqPos 2) :
    H.toNHead.posEmbed p = H.posEmbed (seqPosToFin3 p) := rfl

@[simp] lemma seqTok_pairToBits (ab : Bool × Bool) (p : SeqPos 2) :
    NHead.seqTok (pairToBits ab) p = HeadComplexity.seqTok ab (seqPosToFin3 p) := by
  cases p with
  | none =>
      rfl
  | some i =>
      fin_cases i <;> rfl

@[simp] lemma toNHead_x_pair (H : Head d) (ab : Bool × Bool) (p : SeqPos 2) :
    H.toNHead.x (pairToBits ab) p = H.x ab (seqPosToFin3 p) := by
  cases p with
  | none =>
      simp [Head.toNHead, NHead.x, Head.x, seqTok_pairToBits, seqPosToFin3]
  | some i =>
      fin_cases i <;> simp [Head.toNHead, NHead.x, Head.x, seqTok_pairToBits, seqPosToFin3]

@[simp] lemma toNHead_sigma_pair (H : Head d) (ab : Bool × Bool) (p : SeqPos 2) :
    H.toNHead.sigma (pairToBits ab) p = H.sigma ab (seqPosToFin3 p) := by
  unfold NHead.sigma Head.sigma
  rw [toNHead_x_pair, toNHead_x_pair]
  rfl

@[simp] lemma toNHead_value_pair (H : Head d) (ab : Bool × Bool) (p : SeqPos 2) :
    H.toNHead.value (pairToBits ab) p = H.value ab (seqPosToFin3 p) := by
  unfold NHead.value Head.value
  rw [toNHead_x_pair]
  rfl

@[simp] lemma toNHead_numerator_pair (H : Head d) (ab : Bool × Bool) :
    H.toNHead.numerator (pairToBits ab) = H.numerator ab := by
  simp [NHead.numerator, Head.numerator, Fin.sum_univ_three, seqPosToFin3, add_assoc, add_comm]

@[simp] lemma toNHead_denominator_pair (H : Head d) (ab : Bool × Bool) :
    H.toNHead.denominator (pairToBits ab) = H.denominator ab := by
  simp [NHead.denominator, Head.denominator, Fin.sum_univ_three, seqPosToFin3, add_assoc, add_comm]

@[simp] lemma toNHead_attnUpdate_pair (H : Head d) (ab : Bool × Bool) :
    H.toNHead.attnUpdate (pairToBits ab) = H.attnUpdate ab := by
  simp [NHead.attnUpdate, Head.attnUpdate]

@[simp] lemma toNHead_residual_pair (H : Head d) (ab : Bool × Bool) :
    H.toNHead.residual (pairToBits ab) = H.residual ab := by
  simp [NHead.residual, Head.residual, seqPosToFin3]

@[simp] lemma toNHead_attnUpdate_bits (H : Head d) (bits : Fin 2 → Bool) :
    H.toNHead.attnUpdate bits = H.attnUpdate (bits 0, bits 1) := by
  change H.toNHead.attnUpdate (pairToBits (bits 0, bits 1)) = H.attnUpdate (bits 0, bits 1)
  exact H.toNHead_attnUpdate_pair (bits 0, bits 1)

@[simp] lemma toNHead_residual_bits (H : Head d) (bits : Fin 2 → Bool) :
    H.toNHead.residual bits = H.residual (bits 0, bits 1) := by
  change H.toNHead.residual (pairToBits (bits 0, bits 1)) = H.residual (bits 0, bits 1)
  exact H.toNHead_residual_pair (bits 0, bits 1)

end Head

end HeadComplexity
