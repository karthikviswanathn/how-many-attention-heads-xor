# The all-branches consolidation

This branch consolidates every proved lemma and every clearly stated hypothesis
from all research lines of this project: the local branches and worktrees, and
the two research clones on the Snellius cluster (fetched 2026-07-20). It was
assembled on 2026-07-20.

**Inclusion policy.** A result is included if its source branch treats it as
established: a complete informal proof, an exact integer certificate with a
passing verification script, or a Lean formalization. Clearly stated
conjectures and open problems are included as hypotheses. Excluded: every file
whose only purpose was an attempt at a statement that was never proved, in
particular the five-bit degree-three exact-cover search and the six-bit
parity-triple four-head-impossibility program. Nothing is lost: every excluded
file remains on its source branch in this repository's git history.

## Source map

| Source ref | Tip | Disposition |
|---|---|---|
| `codex/sprint-1` + its working tree | 5a9ae50 + uncommitted | **Base of this branch.** The full numbered ledger `lemmas.md` with proof files `lemmas/001-197`, exact certificates, `src/hstar` tooling. |
| `main` | 675506f | **Merged with history.** Lean-formalized foundational stack (Lemmas 1-12) in `head-complexity/`, corrected three-bit hierarchy, `research/head_hierarchy_pattern.md`. |
| `writeup` | 8a699ae | **Merged with history.** The public write-up under `writeups/xor/`. |
| `origin/lean-proofs` | b70c95a | **Merged with history.** `head-complexity/HeadComplexity/Sandwich.lean`, `OPEN_PROBLEM_Hstar_2block.md`, codex theory workflow. |
| `codex/sprint-symmetric` | bc13311 | **Curated import** to `variants/feedforward/` (distinct model variant, see below). |
| `autoresearch` | 82fee4e | **Curated import** to `consolidated/autoresearch/` (88 files). |
| `snellius/autoresearch` | 8323482 | **Curated import** to `consolidated/autoresearch-snellius/` (78 files). |
| `snellius/jul15` | de76caf | **Subsumed.** Its ledger and `informal_proofs/results.jsonl` are identical to or older than the spine's; its unique additions are the excluded f6 program (including its own alternate lemmas 190/191, common-multiplier cell obstructions, left on the branch). |
| `snellius/codexwork` | 20b75ee | Ancestor of `codex/sprint-1`; nothing unique. |
| `autoresearch-bak` | 78ff726 | **Excluded.** Its single unique lemma (L13, mixed-literal DNF upper bound) is a false overclaim; see Hypotheses below. |
| `informal-prover`, `codex/informal-proof-2`, `codex/public-lemmas-through-012`, `codex/inverted-problem-statement` | | Ancestors of `main`; nothing unique. |

## Where the proved material lives

- **The ledger.** [lemmas.md](lemmas.md) is the master statement list; proofs are
  one file per lemma under [lemmas/](lemmas/) in six thematic folders, numbered
  001-197. Highlights: the exact normal form `H* = L_frac` (010), the exact
  symmetric characterization (012), universal upper bounds through twelve bits
  (017-020 and successors), the strict separations folder
  [lemmas/06_strict_separations/](lemmas/06_strict_separations/) with the
  twelve-bit separation (182), exact classification through four bits (183),
  the five-bit degree-two and degree-four exact classifications (187, 186), and
  the eight-bit strict separation `deg_pm(f_8) = 2 < 3 = H*(f_8)` (189).
- **Machine-checked foundations.** [head-complexity/](head-complexity/) is the
  Lean 4 formalization of Lemmas 1-12 plus the threshold-degree sandwich
  (`Sandwich.lean`), axiom-clean per its build gate.
- **Exact tChow certificates.**
  [claude-comments/tchow_certificates/](claude-comments/tchow_certificates/)
  holds exact integer certificates for `tChow_pm(f_6) = 4` and
  `tChow_pm(f_8) = 2`, and
  [claude-comments/hstar_mfdeg_tchow.md](claude-comments/hstar_mfdeg_tchow.md)
  proves the chain `H* = MFdeg_pm`, the sandwich
  `deg_pm <= tChow_pm <= H*`, and the strictness `tChow_pm(f_8) = 2 < 3 = H*(f_8)`
  (so the tangential-Chow relaxation is not equal to `H*`; this settles the
  autoresearch frontier question F4 negatively).
- **The proved f6 facts.** For the six-bit parity-triple candidate:
  `deg_pm(f_6) = 4` exactly and `4 <= H*(f_6) <= 6`
  (`artifacts/calculations/verify_n6_parity_midlayer_triple_candidate.py`,
  `verify_n6_parity_midlayer_triple_h6.py` with its certificate JSON), the
  LP-certified degree-four rigidity
  (`n6_parity_midlayer_triple_rigidity.md`), and the sign-changing
  common-kernel negative result
  (`verify_n6_parity_triple_full64_common_kernel.py`).
- **Autoresearch runs.** [consolidated/](consolidated/) preserves the two
  autonomous runs with their own ledgers, blueprints, and logs. Headlines:
  the tChow sandwich (local L18, cluster L15/L16), flattening sign-rank and
  shatter-rectangle lower bounds, Warren counting (almost all functions need
  exponentially many heads), the interval family INT with
  `deg_pm = 2` but near-linear `H*`, the indexing family IDX with
  `H* = Omega(N / log N)`, and full-complement invariance (local L28).
- **Model variant.** [variants/feedforward/](variants/feedforward/): with a
  width `2 d_model` ReLU block after attention, every nonconstant Boolean
  function is one-head computable, so head counting degenerates in that model.
- **Three-bit picture.** [three_head_functions_n3.md](three_head_functions_n3.md)
  and [research/head_hierarchy_pattern.md](research/head_hierarchy_pattern.md):
  at `n = 3`, `H*` is 0 for constants, 1 for nonconstant LTFs, 3 for parity and
  its complement, 2 for everything else.
- **Write-up.** [writeups/xor/](writeups/xor/) is the public post.

## Consolidated hypotheses and open problems

Provenance in brackets. Statements live in the linked files; conjectures whose
only artifacts were search programs are stated here directly.

1. **The core question** [main, sprint-1, both autoresearch runs]: characterize
   `H*(f)` exactly or approximately by a known invariant of `f`. See
   [problem_statement.md](problem_statement.md).
2. **H-pole hierarchy** [main]: the `H`-head-computable functions are exactly
   the sign patterns of degree-`H` polynomials admitting a special `H`-pole
   decomposition. See
   [research/head_hierarchy_pattern.md](research/head_hierarchy_pattern.md).
3. **Six-bit separation candidate** [sprint-1, jul15]: `H*(f_6) >= 5` for
   six-bit parity flipped at the three weight-3 vertices 21, 38, 41, which
   would give a strict separation at `n = 6` since `deg_pm(f_6) = 4` is proved.
   See [f6_hstar_gt4_problem.md](f6_hstar_gt4_problem.md). Note: the exact
   certificate `tChow_pm(f_6) = 4` proves that no positivity-free
   (tangential-Chow) argument can settle this; any proof must use the
   admissibility constraints.
4. **Five-bit degree-three class** [sprint-1, jul15]: every five-bit function
   with `deg_pm = 3` has `H* = 3`. This is the only open threshold-degree class
   at `n = 5`; with it, the smallest separating dimension satisfies
   `6 <= n_sep <= 8`, and currently `5 <= n_sep <= 8` (Theorems 183, 186, 187, 189).
5. **Order-2 feasibility** [autoresearch]: does `tChow_pm(f) <= 2` imply
   `H*(f) <= 2` for all `n`? Known for `n <= 4`. (The general order analogue is
   refuted by the f8 certificate; the order-2 case remains open.)
6. **Median-of-three bit** [autoresearch L50]: is `H*(MED_j) = 3`? Its natural
   cubic has an inherently mixed-sign denominator triangle, a concrete probe of
   how positivity constrains head counts. See
   [consolidated/autoresearch/lemmas/02_upper_bounds/050_median_tchow.md](consolidated/autoresearch/lemmas/02_upper_bounds/050_median_tchow.md).
7. **INT exactness** [autoresearch]: `H*(INT_n) = n - 1` for `n >= 3` (proved
   bracket: `n / (8 log2 n) <= H*(INT_n) <= n - 1`).
8. **Mixed-literal DNF upper bound** [both autoresearch runs;
   autoresearch-bak's flawed proof]: does an `s`-term DNF with mixed-polarity
   terms satisfy `H*(f) <= s`? Single-polarity terms: proved. Mixed terms:
   open. `autoresearch-bak` commit 78ff726 claims the general bound, but its
   realizability step misapplies the normal-form converse (a one-head
   denominator has uniform-sign slopes, so a mixed-polarity term indicator is
   not a valid atom); the sibling run documents the obstruction in
   [consolidated/autoresearch/informal_mixed_literal_dnf_upper_bound.md](consolidated/autoresearch/informal_mixed_literal_dnf_upper_bound.md)
   and its survey. That is why the bak branch is excluded.
9. **Single-bit negation invariance** [autoresearch]: is `H*` invariant under
   flipping one input bit? (Flipping all bits: proved invariant, local L28.)
10. **Interior Hamming predicates** [autoresearch]: is `H*` of
    `1[Hamming(x,y) = 1]` unbounded? Flattening sign-rank provably cannot show
    more than `O(log n)` here.
11. **Degree-equality frontier F5** [both autoresearch runs]: for which classes
    beyond LTFs, symmetric functions, and small `n` does `H* = deg_pm` hold,
    starting with quadratic threshold functions?
12. **Indexing and threshold intersections** [snellius autoresearch]: exact
    `H*(IND_m)` (only `H*(IND_m) >= m` and an `Omega(2^m / m^2)` bound are
    proved), and bounds for intersections of `k` thresholds.
13. **2-block-symmetric collapse** [lean-proofs]: for
    `f(x) = G(|x_A|, |x_B|)`, is `H*(f)` the bivariate grid threshold degree
    `delta(G)`? See [OPEN_PROBLEM_Hstar_2block.md](OPEN_PROBLEM_Hstar_2block.md).
14. **Feed-forward variant** [sprint-symmetric]: find a restriction of the
    feed-forward model under which head count is again a nontrivial invariant.
    See [variants/feedforward/001_one_head_universality.md](variants/feedforward/001_one_head_universality.md).

## Caveats a reader should know

- **Numbering collisions.** Numeric lemma IDs are only meaningful within one
  namespace. The spine's `lemmas/013-050` differ from the autoresearch runs'
  L13-L50 (both runs forked from the shared Lean-verified L1-L12 base and
  numbered independently, with different folder taxonomies); `snellius/jul15`
  additionally has its own, different lemmas 190/191 (excluded with the f6
  program). The two autoresearch runs also derived some results independently
  under the same numbers (for example Warren counting appears in both).
- **Epistemic tiers.** Lemmas 1-12 are Lean-formalized. The spine ledger
  entries and certificates are exact-arithmetic-verified where a verify script
  is cited. The autoresearch L13+ entries are informally verified by a
  generate-and-verify LLM pipeline: real proofs, but with a weaker check than
  the Lean tier; their ledgers record per-entry status.
- **A known statement variant.** Lemma 028 (restriction sign-rank upper bound)
  appears with two different bounds: the spine file states a minimum-form
  bound, while the spine ledger (and `snellius/jul15`) state a convolution-sum
  form. Both trace to the same restriction argument, but the file and ledger
  entry should be reconciled.
- **What was deleted from this branch's tree** (all still on their source
  branches): the n5 degree-three exact-cover search, the n6 parity-triple
  four-head program (route documents, atlases, SAT/LP searches, audit and
  screen scripts, the Gordan-route conjecture files, jul15's cell-obstruction
  lemmas, and roughly 1,800 untracked search outputs on the cluster), n7/n8
  screening searches, the abandoned hdth4 route, Lean scratch in `.l12-work/`,
  the cloud handoff document for the attempt program, and `autoresearch-bak`'s
  flawed L13.
