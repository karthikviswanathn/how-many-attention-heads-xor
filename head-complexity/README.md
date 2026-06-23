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
| 1 | one-head 2-coord additive split | `NHead.numerator_additive_split` | `AdditiveSplit.lean` |
| 2 | antipode identities | `NHead.restricted_numerator_antipode` | `Generalized.lean` |
| 3 | checkerboard obstruction `H*≥2` | `parity_restriction_HStarN_ge_two` | `Generalized.lean` |
| 4 | symmetric thresholds `H*=1` | `HStarN_threshold` | `ExactComplexity.lean` |
| 5 | family exact values | `HStarN_parity`, `HStarN_exact` | `ExactComplexity.lean` |
| 6 | `deg±(f) ≤ H*(f)` | `signReprDegLe_of_computableWithHeadsN` | `ModelToPolynomial.lean` |
| 7 | `deg±(parity) = n` | `thresholdDeg_parity` | `ParityThresholdDegree.lean` |
| 8 | `H*(XOR_n) = n` | `HStarN_parity` | `ExactComplexity.lean` |
| 9 | weighted-sum `H* ≤ M−1`; universal `≤ 2ⁿ−1` | `HStarN_le_weighted`, `HStarN_le_universal` | `Lemma9.lean` |
| 10 | linear-fractional normal form `H*=L_frac` | `HStarN_eq_Lfrac` | `Lemma10Main.lean` |
| 11 | levels 0/1: const / nonconstant LTF | `HStarN_eq_zero_iff`, `HStarN_eq_one_iff` | `Lemma11.lean` |
| 12 | symmetric `H*=C(F)` (sign changes) | `HStarN_symmetricFn` | `L12Upper.lean` |

Depends on [mathlib](https://github.com/leanprover-community/mathlib4) (`v4.29.0`, pinned
in `lakefile.toml`). Build with:

```bash
lake exe cache get   # fetch prebuilt mathlib (first time only)
lake build
```

For **exact, reproducible** build/verify instructions — including the
mathlib-cache `curl` fix, the Snellius SLURM job scripts, and how to confirm the
results are axiom-clean — see [`BUILDING.md`](BUILDING.md).

See the [repository README](../README.md) for the wider project context.
