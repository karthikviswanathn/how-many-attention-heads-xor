import HeadComplexity.Basic

/-!
# Segment crossing obstruction.

If a point `P` lies on the segment `[p, q]` and also on the segment
`[r, s]`, then no linear functional can place `p, q` strictly below
a threshold `τ` while placing `r, s` strictly above it. This is the
geometric core of the one-head XOR impossibility argument.
-/

namespace HeadComplexity

/-- A convex combination of two reals, both at most `τ`, is at most `τ`. -/
private lemma convex_sum_le {a b τ x y : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : a + b = 1)
    (hx : x ≤ τ) (hy : y ≤ τ) : a * x + b * y ≤ τ := by
  have hτ : a * τ + b * τ = τ := by linear_combination τ * hab
  have h1 : a * x ≤ a * τ := mul_le_mul_of_nonneg_left hx ha
  have h2 : b * y ≤ b * τ := mul_le_mul_of_nonneg_left hy hb
  linarith

/-- A convex combination of two reals, both strictly greater than `τ`,
is strictly greater than `τ`. -/
private lemma lt_convex_sum {a b τ x y : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : a + b = 1)
    (hx : τ < x) (hy : τ < y) : τ < a * x + b * y := by
  have hτ : a * τ + b * τ = τ := by linear_combination τ * hab
  have h1 : a * τ ≤ a * x := mul_le_mul_of_nonneg_left hx.le ha
  have h2 : b * τ ≤ b * y := mul_le_mul_of_nonneg_left hy.le hb
  rcases eq_or_lt_of_le ha with ha' | ha'
  · have hb' : 0 < b := by linarith
    have : b * τ < b * y := mul_lt_mul_of_pos_left hy hb'
    linarith
  · have : a * τ < a * x := mul_lt_mul_of_pos_left hx ha'
    linarith

/-- **Segment crossing obstruction.** If a point `P` lies simultaneously on
the segments `[p, q]` and `[r, s]`, then no linear functional `L` can place
`L p, L q` weakly below a threshold `τ` while placing `L r, L s` strictly
above `τ`. The asymmetry (weak `≤` on one side, strict `<` on the other) is
exactly what the XOR-impossibility application needs. -/
theorem segment_cross_not_separable
    {V : Type*} [AddCommGroup V] [Module ℝ V]
    {p q r s : V} (L : V →ₗ[ℝ] ℝ) {τ : ℝ}
    (hp : L p ≤ τ) (hq : L q ≤ τ) (hr : τ < L r) (hs : τ < L s)
    {P : V} (hPpq : P ∈ segment ℝ p q) (hPrs : P ∈ segment ℝ r s) : False := by
  obtain ⟨a, b, ha, hb, hab, hP1⟩ := hPpq
  obtain ⟨c, e, hc, he, hce, hP2⟩ := hPrs
  have hLP_le : L P ≤ τ := by
    rw [← hP1, map_add, L.map_smul, L.map_smul, smul_eq_mul, smul_eq_mul]
    exact convex_sum_le ha hb hab hp hq
  have hLP_gt : τ < L P := by
    rw [← hP2, map_add, L.map_smul, L.map_smul, smul_eq_mul, smul_eq_mul]
    exact lt_convex_sum hc he hce hr hs
  linarith

end HeadComplexity
