import HeadComplexity.Model.Head

set_option linter.style.header false

/-!
# Additive decomposition of a restricted one-head attention map (Theorem 1).

Theorem 1 states that, after freezing all but two input coordinates `i, j`, the
softmax numerator and denominator of a single head split additively:

$$ N(a,b) = A(a) + B(b) + C, \qquad D(a,b) = \alpha(a) + \beta(b) + \gamma. $$

For a two-valued domain `Bool × Bool` this additive form is *equivalent* to the
antipode (balance) identity `N(0,0)+N(1,1) = N(0,1)+N(1,0)`, which is already
established for the general `n`-bit model in `Model/Head.lean`
(`restricted_numerator_antipode` / `restricted_denominator_antipode`, proved
directly by a per-position case analysis). We therefore obtain the additive
split with the explicit witnesses

`A a = N(a, 0)`, `B b = N(0, b)`, `C = -N(0, 0)`

(and likewise for `D`), the only non-trivial corner `(1,1)` being discharged by
the antipode identity. This is a faithful Lean formalization of Theorem 1's
statement; the per-position content it rests on lives in the antipode theorems.
-/

namespace HeadComplexity

namespace Head

variable {n d : ℕ}

/-- **Theorem 1 (numerator).** On a two-coordinate restriction, the softmax
numerator of a single head decomposes additively as `A a + B b + C`, with `A`
depending only on `a`, `B` only on `b`, and `C` constant. -/
theorem numerator_additive_split (H : Head n d) (base : Fin n → Bool)
    (i j : Fin n) (hij : i ≠ j) :
    ∃ (A B : Bool → Vec d) (C : Vec d), ∀ a b : Bool,
      H.numerator (restrictBits base i j (a, b)) = A a + B b + C := by
  refine ⟨fun a => H.numerator (restrictBits base i j (a, false)),
          fun b => H.numerator (restrictBits base i j (false, b)),
          - H.numerator (restrictBits base i j (false, false)), ?_⟩
  have hanti := H.restricted_numerator_antipode base i j hij
  intro a b
  cases a <;> cases b <;> dsimp only
  · abel
  · abel
  · abel
  · have hsum : H.numerator (restrictBits base i j (true, true))
          + H.numerator (restrictBits base i j (false, false))
          = H.numerator (restrictBits base i j (false, true))
          + H.numerator (restrictBits base i j (true, false)) := by
      rw [add_comm (H.numerator (restrictBits base i j (true, true)))]; exact hanti
    rw [eq_sub_of_add_eq hsum]; abel

/-- **Theorem 1 (denominator).** On a two-coordinate restriction, the softmax
denominator decomposes additively as `α a + β b + γ`. -/
theorem denominator_additive_split (H : Head n d) (base : Fin n → Bool)
    (i j : Fin n) (hij : i ≠ j) :
    ∃ (α β : Bool → ℝ) (γ : ℝ), ∀ a b : Bool,
      H.denominator (restrictBits base i j (a, b)) = α a + β b + γ := by
  refine ⟨fun a => H.denominator (restrictBits base i j (a, false)),
          fun b => H.denominator (restrictBits base i j (false, b)),
          - H.denominator (restrictBits base i j (false, false)), ?_⟩
  have hanti := H.restricted_denominator_antipode base i j hij
  intro a b
  cases a <;> cases b <;> dsimp only <;> linarith

end Head

end HeadComplexity
