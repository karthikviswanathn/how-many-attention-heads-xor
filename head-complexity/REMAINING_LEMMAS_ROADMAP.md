# Roadmap — finishing the 12-lemma stack in Lean

Status as of 2026-06-23 (branch `lean-proofs`), combining a per-lemma inventory
sweep and a Codex strategy consult. The L12 push built reusable lower- and
upper-bound machinery; several remaining lemmas are now near-corollaries of it.

## Status table

| # | Lemma | Status | Lean |
|---|-------|--------|------|
| 1 | One-head 2-coord additive split | ✅ general-`n` | `AdditiveSplit.lean` |
| 2 | Antipode identities | ✅ general-`n` | `BooleanFunctions.lean` (pre-existing) |
| 3 | Checkerboard obstruction `H*≥2` | ✅ general-`n` | `Generalized.lean` |
| 4 | `H*(T_{n,t}) = 1` (symmetric thresholds) | ❌ missing | — |
| 5 | Family consequences (`PARITY,EXACT ≥ 2`) | ◑ lower bounds only | `SymmetricFamilies.lean` |
| 6 | `deg±(f) ≤ H*(f)` | ✅ general-`n` | `ModelToPolynomial.lean` |
| 7 | `deg±(parity) = n` | ❌ missing | — |
| 8 | `H*(XOR_n) = n` | ◑ blocks done | — (1-line corollary) |
| 9 | Weighted-sum upper bound `H* ≤ M−1` | ❌ missing (symmetric case only) | — |
| 10 | Linear-fractional normal form `H* = L_frac` | ❌ missing | — |
| 11 | Level 0/1: const / LTF | ◑ `n=2` only | `BooleanFunctions.lean` |
| 12 | Symmetric sign-change `H* = C(F)` | ✅ general-`n` | `L12Upper.lean` |

## Reusable machinery already proven (axiom-clean)

* **Lower-bound chain:** `signReprDegLe_of_computableWithHeadsN` (L6: `H` heads →
  degree-`≤H` sign-representing `MvPolynomial`) → `exists_strictSignRep` →
  `symmetrize` → `exists_univariate_of_symmetric` → `signChanges_le_natDegree`.
  Currently exposed only end-to-end as `signChanges_le_of_computableWithHeadsN`.
* **Upper-bound construction:** `exists_sign_poly` → `real_partial_fraction` →
  `atomHead : NHead n 2` (one real softmax head = one `b/(k+a)` atom) →
  `atomFamily_readout` → `symmetricFn_computable`.
* **Glue facts:** `PARITY n = symmetricFn (fun k => decide (Odd k))` (rfl),
  `EXACT n k = symmetricFn (fun m => decide (m = k))` (rfl), `signChanges_parity = n`,
  `HStarN_symmetricFn : HStarN n (symmetricFn F) = signChanges n F`.

## Plan (dependency-ordered)

### Tier A — corollaries of L12 (easy; one new file, e.g. `ExactComplexity.lean`)

* **L8** `HStarN n (PARITY n) = n`:
  `rw [PARITY_eq_symmetricFn, HStarN_symmetricFn, signChanges_parity]`.
* **L4** `HStarN n (THRESHOLD n t) = 1` for `1 ≤ t ≤ n`, where
  `THRESHOLD n t := symmetricFn (fun k => decide (t ≤ k))`. New content: a Finset
  proof that `signChanges n (fun k => decide (t ≤ k)) = 1` (the only change index
  in `range n` is `t−1`).
* **L5 exact values / EXACT** `HStarN n (EXACT n k) = 2` for `1 ≤ k ≤ n−1`. New
  content: `signChanges n (fun m => decide (m = k)) = 2` (changes at `k−1` and `k`).
  Assemble the three exact-value theorems Lemma 5 advertises.

### Tier B — threshold degree of parity (medium; reuses the chain)

* **L7** `deg±(parity) = n`. Steps:
  1. Refactor out `signChanges_le_of_ThresholdDegLE (h : ThresholdDegLE (symmetricFn F) H) : signChanges n F ≤ H` from `signChanges_le_of_computableWithHeadsN` (it is the same proof past the L6 line).
  2. Define `thresholdDeg f := Nat.find` over `ThresholdDegLE f ·` (the exact `deg±`).
  3. Lower bound `n ≤ deg±(parity)`: apply (1) to parity + `signChanges_parity`.
  4. Upper bound `deg±(parity) ≤ n`: witness `P := -∏ i, (C 1 - C 2 * X i)`,
     which evaluates to `-(-1)^{|x|}` (positive iff odd weight), `totalDegree ≤ n`.

### Tier C — general upper bound (medium-hard)

* **L9** `H*(f) ≤ M−1` for `f = F(t(x))`, `t(x) = ∑ λ_i x_i`, `λ_i > 0`,
  `M = |Im(t)|`. Generalize the L12 upper bound from `t = |x|` to arbitrary
  positive weighted sums: finite-image sign polynomial on the real nodes `Im(t)`
  (Lagrange / manual Finset product), `real_partial_fraction`, and a **weighted**
  fractional atom (generalize `atomHead`'s key channel from `|x|` to `∑ λ_i x_i`).
  Corollaries: symmetric `f` ⇒ `H* ≤ n`; any `f` ⇒ `H* ≤ 2ⁿ−1`.

### Tier D — exact structural characterizations (hard)

* **L10** `H*(f) = L_frac(f)`. Define `FracAtom` and `fracComputableWithAtomsN`;
  prove `computableWithHeadsN n H f ↔ fracComputableWithAtomsN n H f` per head
  count (forward: any scalar-read head normalizes to an atom via
  `σ_i = ρ_i α^{x_i}`, `σ_q = γ`, scalar value `m_i + δ x_i`; backward: realize an
  atom with a `d=3` head using `log ρ_i, log α, log γ`), then a `Nat.find`
  equality. No serious mathlib gap; the algebra is implicit in `ModelToPolynomial`
  + `UpperBound`.
* **L11** `H*(f)=0 ⟺ f const`, `H*(f)=1 ⟺ f nonconstant LTF`. `H*=0 ⟺ const`
  from `computableWithHeadsN n 0 f` (empty family ⇒ constant readout). `H*=1`:
  lower via L6 (`H*=1 ⇒ ThresholdDegLE f 1`), upper via L10's one-atom
  realization; needs a universal upper bound (L9) so `HStarN` never falls to its
  default `0`. Define `isLTF f := ThresholdDegLE f 1` (or coefficient form).

## Recommended execution order

`L8 → L4 → L5(exact) → L7 → FracAtom+atom realization → L9 → L10 → L11`.

Tier A/B are high-confidence and reuse existing results; Tier C/D are genuine new
developments (Tier D, especially L10, is the largest). Each lemma is verified on a
Snellius compute node (`sbatch build.slurm`; see `BUILDING.md`) — axiom-clean,
zero warnings — before commit.
