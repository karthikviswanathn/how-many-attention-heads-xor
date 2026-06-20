import HeadComplexity.Head
import HeadComplexity.Softmax

set_option linter.style.header false

/-!
# Structural decomposition of the attention update.

The key observation powering the one-head impossibility result: on a
sequence `(a, b, =)`, the attention weights and value vectors split
into an `a`-only part (position 0), a `b`-only part (position 1), and
a constant part (position 2). Summing the attention numerator over the
antipodal pairs `{(false,false), (true,true)}` and `{(false,true),
(true,false)}` therefore gives the same vector.
-/

namespace HeadComplexity

namespace Head

variable {d : ℕ} (H : Head d)

/-! ### "Depends only" lemmas

Because `seqTok (a, b) 0 = cond a 1 0` is independent of `b`, and
`seqTok (a, b) 2 = 2` is constant, the attention ingredients at each
position depend only on the relevant bit. All six equalities are
definitionally true, so `rfl` suffices. -/

lemma sigma_at_0 (a b : Bool) : H.sigma (a, b) 0 = H.sigma (a, false) 0 := rfl

lemma sigma_at_1 (a b : Bool) : H.sigma (a, b) 1 = H.sigma (false, b) 1 := rfl

lemma sigma_at_2 (a b : Bool) : H.sigma (a, b) 2 = H.sigma (false, false) 2 := rfl

lemma value_at_0 (a b : Bool) : H.value (a, b) 0 = H.value (a, false) 0 := rfl

lemma value_at_1 (a b : Bool) : H.value (a, b) 1 = H.value (false, b) 1 := rfl

lemma value_at_2 (a b : Bool) : H.value (a, b) 2 = H.value (false, false) 2 := rfl

/-! ### Positivity of the denominator -/

/-- Every summand `H.sigma ab j` is strictly positive (as an exponential). -/
lemma sigma_pos (ab : Bool × Bool) (j : Fin 3) : 0 < H.sigma ab j :=
  Real.exp_pos _

/-- The attention denominator is strictly positive. -/
lemma denominator_pos (ab : Bool × Bool) : 0 < H.denominator ab := by
  unfold Head.denominator
  apply Finset.sum_pos
  · intro j _
    exact H.sigma_pos ab j
  · exact Finset.univ_nonempty

lemma denominator_ne_zero (ab : Bool × Bool) : H.denominator ab ≠ 0 :=
  (H.denominator_pos ab).ne'

/-! ### Antipode identities -/

/-- The antipode identity for the attention numerator: summing `N(a,b)`
over the diagonal `{(ff,ff), (tt,tt)}` equals summing over the off-diagonal
`{(ff,tt), (tt,ff)}`. Both totals collect exactly one copy of each
"a-only" contribution and one copy of each "b-only" contribution,
plus two copies of the constant contribution. -/
theorem numerator_antipode :
    H.numerator (false, false) + H.numerator (true, true)
    = H.numerator (false, true) + H.numerator (true, false) := by
  simp only [Head.numerator, Fin.sum_univ_three]
  -- Each term at position 0 depends only on the first bit, each term at
  -- position 1 depends only on the second bit, each term at position 2 is
  -- constant. The equalities are `rfl` so rewriting is trivial; `abel`
  -- then closes the rearrangement.
  rw [show H.sigma (false, true) 0 • H.value (false, true) 0
        = H.sigma (false, false) 0 • H.value (false, false) 0 from rfl,
      show H.sigma (true, false) 0 • H.value (true, false) 0
        = H.sigma (true, true) 0 • H.value (true, true) 0 from rfl,
      show H.sigma (true, false) 1 • H.value (true, false) 1
        = H.sigma (false, false) 1 • H.value (false, false) 1 from rfl,
      show H.sigma (false, true) 1 • H.value (false, true) 1
        = H.sigma (true, true) 1 • H.value (true, true) 1 from rfl,
      show H.sigma (true, true) 2 • H.value (true, true) 2
        = H.sigma (false, false) 2 • H.value (false, false) 2 from rfl,
      show H.sigma (false, true) 2 • H.value (false, true) 2
        = H.sigma (false, false) 2 • H.value (false, false) 2 from rfl,
      show H.sigma (true, false) 2 • H.value (true, false) 2
        = H.sigma (false, false) 2 • H.value (false, false) 2 from rfl]
  abel

/-- The antipode identity for the attention denominator: summing `D(a,b)`
across the diagonal equals summing across the off-diagonal. -/
theorem denominator_antipode :
    H.denominator (false, false) + H.denominator (true, true)
    = H.denominator (false, true) + H.denominator (true, false) := by
  simp only [Head.denominator, Fin.sum_univ_three]
  rw [show H.sigma (false, true) 0 = H.sigma (false, false) 0 from rfl,
      show H.sigma (true, false) 0 = H.sigma (true, true) 0 from rfl,
      show H.sigma (true, false) 1 = H.sigma (false, false) 1 from rfl,
      show H.sigma (false, true) 1 = H.sigma (true, true) 1 from rfl,
      show H.sigma (true, true) 2 = H.sigma (false, false) 2 from rfl,
      show H.sigma (false, true) 2 = H.sigma (false, false) 2 from rfl,
      show H.sigma (true, false) 2 = H.sigma (false, false) 2 from rfl]
  ring

end Head

end HeadComplexity
