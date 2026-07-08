# head-complexity

Lean 4 formalization of the head-complexity results for one-layer attention. The
definitions and theorems mirror the informal proofs in the top-level `lemmas/` writeups.

## Status — all 12 foundational lemmas formalized

Every lemma in `lemmas/01_foundations_and_normal_form/` (L1–L12) is machine-checked
for **general `n`**, with no `sorry`/`admit`, depending only on the three standard
Lean axioms `[propext, Classical.choice, Quot.sound]` (the full build runs a
`#print axioms` gate). `H*` is `HStarN` (the least number of heads realizing `f`).

| # | Lemma | Headline Lean result | File |
|---|-------|----------------------|------|
| 1 | 2-coordinate numerator additive split | `restricted_numerator_additive_split` | `Results/RestrictionLowerBounds.lean` |
| 2 | restricted numerator antipode identity | `restricted_numerator_antipode` | `Results/RestrictionLowerBounds.lean` |
| 3 | checkerboard obstruction `H*≥2` | `checkerboard_restriction_HStarN_ge_two` | `Results/RestrictionLowerBounds.lean` |
| 4 | symmetric thresholds `H*=1` | `HStarN_threshold` | `Results/ExactFamilies.lean` |
| 5 | family exact values | `HStarN_parity`, `HStarN_exact` | `Results/ExactFamilies.lean` |
| 6 | `deg±(f) ≤ H*(f)` | `degree_le_of_computableWithHeadsN` | `Results/ThresholdDegree.lean` |
| 7 | `deg±(parity) = n` | `parity_thresholdDeg` | `Results/ThresholdDegree.lean` |
| 8 | `H*(XOR_n) = n` | `HStarN_parity` | `Results/ExactFamilies.lean` |
| 9 | weighted-sum `H* ≤ M−1`; universal `≤ 2ⁿ−1` | `HStarN_le_weighted_sum`, `HStarN_le_universal_boolean` | `Results/WeightedUpperBound.lean` |
| 10 | linear-fractional normal form `H*=L_frac` | `HStarN_eq_Lfrac` | `Results/FractionalNormalForm.lean` |
| 11 | levels 0/1: const / nonconstant LTF | `HStarN_eq_zero_iff`, `HStarN_eq_one_iff` | `Results/LowComplexity.lean` |
| 12 | symmetric `H*=C(F)` (sign changes) | `HStarN_symmetricFn` | `Results/SymmetricComplexity.lean` |

Depends on [mathlib](https://github.com/leanprover-community/mathlib4) (version pinned
in `lakefile.toml`). Build with:

```bash
lake exe cache get   # fetch prebuilt mathlib (first time only)
lake build
lake build HeadComplexity.Examples.All   # optional build for just examples
lake build HeadComplexity.Results.All   # optional build for just results
```

For **exact, reproducible** build/verify instructions — including the
mathlib-cache `curl` fix, the Snellius SLURM job scripts, and how to confirm the
results are axiom-clean — see [`BUILDING.md`](BUILDING.md).

See the [repository README](../README.md) for the wider project context.
