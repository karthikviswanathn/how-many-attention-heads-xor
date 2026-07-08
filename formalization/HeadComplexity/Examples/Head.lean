import HeadComplexity.Foundation.Vec

set_option linter.style.header false

/-!
# Single-head attention parameters and the attention update.

A `Head d` packages the embeddings and parameter matrices of a single
attention head acting on the length-3 input sequence `(a, b, =)`. The
file defines the attention update `z` at the `=` query token, the
full residual `h = x_= + z`, and the `computesXor` predicate used to
state the main theorems.
-/

namespace HeadComplexity

open scoped InnerProductSpace

/-- Parameters of a single attention head at embedding dimension `d`:
    token embeddings for `{0, 1, =}` (indexed by `Fin 3` with `2 = =`),
    positional embeddings for the three positions, and linear maps
    `W_Q`, `W_K`, `W_V` for query, key, and value. -/
structure Head (d : ℕ) where
  tokenEmbed : Fin 3 → Vec d
  posEmbed   : Fin 3 → Vec d
  WQ : Vec d →ₗ[ℝ] Vec d
  WK : Vec d →ₗ[ℝ] Vec d
  WV : Vec d →ₗ[ℝ] Vec d

/-- On input `(a, b)`, the token index at position `j`:
    position 0 holds the bit `a`, position 1 holds the bit `b`, and
    position 2 always holds the `=` token (index 2). -/
def seqTok (ab : Bool × Bool) : Fin 3 → Fin 3
  | 0 => cond ab.1 1 0
  | 1 => cond ab.2 1 0
  | 2 => 2

variable {d : ℕ}

/-- The embedded vector at position `j` on input `ab`:
    token embedding at the token index plus positional embedding. -/
noncomputable def Head.x (H : Head d) (ab : Bool × Bool) (j : Fin 3) : Vec d :=
  H.tokenEmbed (seqTok ab j) + H.posEmbed j

/-- The raw unnormalized attention weight (before softmax normalization):
    `σ_j(a,b) = exp(⟨W_K x_j, W_Q x_=⟩)`. -/
noncomputable def Head.sigma (H : Head d) (ab : Bool × Bool) (j : Fin 3) : ℝ :=
  Real.exp ⟪H.WK (H.x ab j), H.WQ (H.x ab 2)⟫_ℝ

/-- The value vector at position `j`: `v_j(a,b) = W_V x_j`. -/
noncomputable def Head.value (H : Head d) (ab : Bool × Bool) (j : Fin 3) : Vec d :=
  H.WV (H.x ab j)

/-- The attention numerator `N(a,b) = ∑_j σ_j v_j`. -/
noncomputable def Head.numerator (H : Head d) (ab : Bool × Bool) : Vec d :=
  ∑ j, H.sigma ab j • H.value ab j

/-- The attention denominator `D(a,b) = ∑_j σ_j`. -/
noncomputable def Head.denominator (H : Head d) (ab : Bool × Bool) : ℝ :=
  ∑ j, H.sigma ab j

/-- The attention update at the query token `=`:
    `z_=(a,b) = N(a,b) / D(a,b)`. -/
noncomputable def Head.attnUpdate (H : Head d) (ab : Bool × Bool) : Vec d :=
  (H.denominator ab)⁻¹ • H.numerator ab

/-- The full residual stream at the query token after one attention layer:
    skip connection `x_=` plus the attention update. -/
noncomputable def Head.residual (H : Head d) (ab : Bool × Bool) : Vec d :=
  H.x ab 2 + H.attnUpdate ab

/-- A vector-valued function on Boolean pairs **computes XOR** under a
    linear readout when there exist a probe `w` and a threshold `τ` with
    `⟨w, f(a,b)⟩ > τ` iff `a xor b = true`. -/
def computesXor (f : Bool × Bool → Vec d) : Prop :=
  ∃ (w : Vec d) (τ : ℝ), ∀ ab : Bool × Bool,
    ⟪w, f ab⟫_ℝ > τ ↔ (xor ab.1 ab.2) = true

end HeadComplexity
