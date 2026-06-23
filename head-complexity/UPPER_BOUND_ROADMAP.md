# L12 upper bound — proof roadmap (elementary, no analysis)

Goal: prove `hub : computableWithHeadsN n (signChanges n F) (symmetricFn F)`, which
combined with `HStarN_symmetricFn_eq_signChanges` gives the FULL unconditional L12
equality `HStarN n (symmetricFn F) = signChanges n F`.

Source: Codex consult (2026-06-23) + paper lemma 010 (linear-fractional normal form).
Key fact established: the construction is **finite and analysis-free** (no exp→∞ limits).

## The construction (on the Hamming-weight axis, k = |x|)

1. Sign changes of `F` on `{0..n}` occur between `t_j-1` and `t_j` (j=1..C, C = signChanges).
   Roots `ρ_j := t_j - 1/2`. Set `P(k) := s · ∏_j (k - ρ_j)`, sign `s = ±1` chosen so
   `P(k) > 0 ⟺ F(k) = true` for k ∈ {0..n}. (P has degree C.)
2. Pick C distinct reals `a_1,…,a_C > n`. `Q(k) := ∏_i (k + a_i) > 0` on {0..n}. (deg C.)
3. Partial fractions: `P(k)/Q(k) = A + ∑_{i=1}^C b_i/(k + a_i)` with `b_i = P(-a_i)/Q'(-a_i)`,
   `A = leading_P/leading_Q = s`. Holds as a polynomial identity after ×Q.
4. `P/Q` has the same sign as `P` on {0..n} (Q>0). So `∑_i b_i/(k+a_i) = P/Q − A` and
   `⟨w,Σ⟩ > τ ⟺ P/Q > 0 ⟺ F(k)` with `τ := −A`.

## Per-head realization (one head = one atom `b/(k+a)`)

Head with d = 3, posEmbed ≡ 0, tokenEmbed t = e_t (standard basis of Vec 3):
- WQ e_2 = e_2 (query embed maps to itself in the score-target channel);
- WK: e_0 ↦ 0, e_1 ↦ (log 2)·e_2, e_2 ↦ (log(a−n))·e_2  (via `Basis.constr`).
  Then σ at a bit-position = exp⟨WK e_token, e_2⟩ = 1 (bit 0) or 2 (bit 1); query σ = a−n.
- denominator = (n−k)·1 + k·2 + (a−n) = **k + a**.
- WV: e_0,e_1 ↦ 0, e_2 ↦ e_0 (value of query token = e_0; bit values = 0).
- numerator = σ_query · e_0 = (a−n)·e_0; attnUpdate = ((a−n)/(k+a))·e_0.
- readout component along e_0 with weight `b/(a−n)` ⇒ ⟨w, attnUpdate⟩ = **b/(k+a)**.

For C heads sharing one readout: give head i its value in coordinate `e_{c_i}` distinct
per head (use d = 3 + C or a per-head block; simplest: d = 3·C blocks, or shared score
channels + distinct value coords). w sums the per-head reads.

## Lean lemma chain (each independently checkable)

- [ ] `Vec`/`EuclideanSpace` inner-product & `Basis.constr` API warmup (single-coord facts).
- [ ] **`head_realizes_atom`** (CRUX): for `a > n`, `b : ℝ`, ∃ NHead n 3 (or shared d) with
      `⟨w, attnUpdate bits⟩ = b / (hammingWeight bits + a)`. De-risks everything.
- [ ] **`exists_family_atoms`**: combine C atoms into one NHeadFamily with shared readout,
      `⟨w, Σ_h attnUpdate_h bits⟩ = ∑_i b_i/(k+a_i)`.
- [ ] **`partial_fraction`**: `P(k)/Q(k) = A + ∑_i b_i/(k+a_i)` on {0..n} (polynomial identity).
- [ ] **`sign_poly`**: build P with `P(k) > 0 ⟺ F(k)` from `signChanges` data (half-integer roots).
- [ ] **assembly** `upper_bound : computableWithHeadsN n (signChanges n F) (symmetricFn F)`.
- [ ] feed into `HStarN_symmetricFn_eq_signChanges` ⇒ unconditional L12.

## Status
Starting with `head_realizes_atom` (the crux). Constant case (C=0) is immediate
(0 heads, g=0, τ=∓1) and is a free corollary.
