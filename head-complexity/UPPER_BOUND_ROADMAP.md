# L12 upper bound — proof roadmap (elementary, no analysis)  ✅ COMPLETED

**STATUS: DONE.** Full unconditional L12 verified (axiom-clean) as
`HStarN_symmetricFn` in `HeadComplexity/L12Upper.lean`. Every lemma below is proven.


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

## Lean lemma chain (all proven — final symbol names in parentheses)

- [x] `Vec`/`EuclideanSpace` inner-product warmup (`vec2_inner`, `UpperBound.lean`).
- [x] **head realizes one atom** (CRUX): for `a > n`, `b : ℝ`, a real `NHead n 2` with
      `⟨w, attnUpdate bits⟩ = b / (hammingWeight bits + a)` (`atomHead`, `atomHead_readout`,
      `UpperBound.lean`).
- [x] **family of atoms**: combine `C` atoms into one `NHeadFamily` with a shared readout,
      `⟨w, Σ_h attnUpdate_h bits⟩ = ∑_i b_i/(k+a_i)` (`atomFamily_readout`, `UpperBound.lean`).
- [x] **partial fraction**: `P(k)/∏(k+a_i) = A + ∑_i b_i/(k+a_i)` (`real_partial_fraction`,
      `PartialFraction.lean`).
- [x] **sign polynomial**: build `P` with `P(k) > 0 ⟺ F(k)` from `signChanges` data
      (half-integer roots) (`exists_sign_poly`, `SignPolynomial.lean`).
- [x] **assembly** `symmetricFn_computable : computableWithHeadsN n (signChanges n F) (symmetricFn F)`
      (`L12Upper.lean`, via `exists_rational_atoms`).
- [x] feed into `HStarN_symmetricFn_eq_signChanges` ⇒ unconditional `HStarN_symmetricFn` (`L12Upper.lean`).

## Status
**DONE.** The crux `atomHead_readout` realizes one `b/(k+a)` atom with a genuine
`NHead n 2` (`d = 2`, not 3 — the score and value channels share `Vec 2`). The
`n = 0` / constant case is handled directly in `symmetricFn_computable` (0 heads,
readout 0, `τ = ∓1`). Whole chain machine-checked, axiom-clean
(`[propext, Classical.choice, Quot.sound]`); see `BUILDING.md` to reproduce.
