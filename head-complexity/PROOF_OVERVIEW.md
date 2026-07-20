# Proof architecture

How the twelve formalized lemmas fit together. See `README.md` for the
lemma→theorem→file map, `HeadComplexity/MainResults.lean` for a verified
table of contents, and `BUILDING.md` to reproduce the build.

## The model (`Basic.lean`, `Generalized.lean`)

A single softmax attention head is `NHead n d`: token embeddings `Fin 3 → Vec d`
(bit-0 / bit-1 / query), positional embeddings `Option (Fin n) → Vec d`, and linear
maps `WQ, WK, WV`. On input `bits`, position `p` has embedding
`x p = tokenEmbed (seqTok bits p) + posEmbed p`; the softmax weight is
`σ p = exp ⟪WK (x p), WQ (x none)⟫`; the head's update is the normalized value
average `attnUpdate = (∑ p σ p)⁻¹ • ∑ p σ p • WV (x p)`. A function is
`computableWithHeadsN n H f` when some `H`-head family's summed update, read by a
linear `⟪w, ·⟫ > τ`, equals `f`. `HStarN n f` (= `H*`) is the least such `H`
(`Nat.find`, `0` if none — but every `f` is computable, so this default never
bites; see Lemma 9 universal bound).

## Two spines

Everything is built from a **lower-bound spine** (you need many heads) and an
**upper-bound spine** (you can build the heads).

### Lower bounds — through threshold degree

```
computableWithHeadsN n H f
  └─ L6  signReprDegLe_of_computableWithHeadsN   (ModelToPolynomial.lean)
        clears each head's softmax ratio to a degree-≤1 affine polynomial;
        H heads ⟹ a degree-≤H real polynomial sign-representing f  (ThresholdDegLE f H)
  └─ for symmetric f:  ThresholdDegLE f H → signChanges ≤ H        (UnivariateReduction.lean)
        strictify → symmetrize over Equiv.Perm → reduce to a univariate
        polynomial in the Hamming weight → count real roots (IVT)
```

This gives the `≥` halves: Lemma 3 (checkerboard, via antipode identities L1/L2 +
segment non-separability), Lemma 5 lower bounds, Lemma 7 (`deg±(parity) = n`,
reusing the symmetric chain), and the `≥` half of Lemma 12.

### Upper bounds — explicit softmax heads

Each construction is one `NHead` whose readout is a prescribed rational/affine
function, proved by clearing the softmax denominator. They form a family, sharing
a value coordinate so one readout sums them.

| gadget | readout | used by |
|--------|---------|---------|
| `atomHead` (`UpperBound.lean`) | `b/(\|x\|+a)` | L12 upper bound |
| `weightedAtomHead` (`Lemma9.lean`) | `b/(∑λᵢxᵢ+a)` | L9 |
| `affineHead` (`AffineHead.lean`) | affine `L(x)`, const absorbed in `τ` | L11 |
| `atomHead'` (`FracAtomHead.lean`) | a full linear-fractional atom | L10 |

The L12 upper bound (`SignPolynomial.lean` → `PartialFraction.lean` →
`UpperBound.lean` → `L12Upper.lean`) builds a degree-`signChanges` sign polynomial,
splits it by partial fractions into `b_h/(k+a_h)` atoms, and realizes one per head.
L9 generalizes `|x|` to a weighted sum (Lagrange interpolation over the image
nodes). L10's two directions show this is tight: *every* head **is** an atom
(`HeadToAtom.lean`, reading the atom parameters off the head's maps) and *every*
atom is realized by a head (`FracAtomHead.lean`), so `H* = L_frac`.

## Capstones

* **L12** (`L12Upper.lean`): `HStarN_symmetricFn` — `≥` from the lower-bound spine,
  `≤` from the upper-bound spine, joined by `le_antisymm` over `Nat.find`.
* **L4, L5, L8** (`ExactComplexity.lean`): corollaries of L12 — the head complexity
  of a standard family is the number of sign changes of its profile.
* **L10** (`Lemma10Main.lean`), **L11** (`Lemma11.lean`): the exact normal form and
  the level-0/1 classification, both using that every `f` is computable.

The same `le_antisymm`-over-two-`Nat.find` shape recurs in L10 and L12: a per-`H`
equivalence between two complexity predicates forces their minima to agree.
