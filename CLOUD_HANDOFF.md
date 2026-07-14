# Cloud Task Handoff

## Stop state

This handoff was prepared on 2026-07-14 after the user asked the local task to stop and transfer its state to a new Codex cloud task.

- Goal status: paused.
- Git branch: `codex/sprint-1`.
- Git commit at handoff: `20b75eeafb64bd9f744ed90699149de66aa0ba24`.
- The worktree is heavily dirty and contains many valuable untracked certificate files. Do not run `git clean`, `git reset --hard`, or discard changes.
- All three subagents have stopped.
- The long five-bit exact-cover process was terminated only after writing a complete iteration-624 checkpoint.
- No research process is intentionally left running.

The commit above does not contain most of the current work. The working tree is the authoritative state.

## Original goal

Find the smallest number of input bits for which there is an explicit Boolean function $f$ satisfying

$$ \deg_{\pm}(f)\neq H^{\ast}(f), $$

give an explicit construction, determine the relevant exact values, and prove that no smaller dimension works.

## Definitions and conventions

For a Boolean function, use signs $s(x)\in\lbrace-1,1\rbrace$, with sign $+1$ for output $1$.

**Threshold degree.** $\deg_{\pm}(f)$ is the minimum degree of a real polynomial $P$ such that $s(x)P(x)>0$ on every Boolean input.

**Head complexity.** $H^{\ast}(f)$ is the minimum number $H$ for which the target is the sign of a score

$$ c+\sum_{h=1}^{H}\frac{A_h(x)}{B_h(x)}, $$

where every $A_h$ is affine, every $B_h$ is affine and strictly positive on the cube, and all nonzero slopes of each $B_h$ have one common sign in the model-faithful orientation class.

Clearing the positive denominators gives a polynomial of degree at most $H$. Therefore

$$ \deg_{\pm}(f)\leq H^{\ast}(f). $$

**Sign coordinates.** Set $z_i=(-1)^{x_i}$. Six-bit parity is

$$ p(z)=\prod_{i=0}^{5}z_i. $$

**Truth masks.** A truth mask stores the output at vertex code $c$ in bit $c$. Coordinate $0$ is the least significant bit.

**Gordan multipliers.** A Gordan multiplier for a signed row matrix $M$ is a nonzero vector $q\geq0$ with $M^{\top}q=0$. Such a multiplier rules out a strict primal separator.

Treat exact integer or rational verifiers as proofs. Treat floating LP, nonlinear optimization, random screens, and finite sampling as evidence only unless an accompanying exact verifier reconstructs the result.

For Markdown under `lemmas/` and for `writeup.md`, follow the repository `AGENTS.md` rules. In particular, use GitHub-safe LaTeX, `\lbrace` and `\rbrace`, `H^{\ast}`, single-line display math, and no em dash characters.

## Executive status

The completed exact example is the eight-bit Hamming-threshold function

$$ f_8(x,y)=1\quad\Longleftrightarrow\quad d_H(x,y)\geq2, \qquad x,y\in\lbrace0,1\rbrace^4. $$

It satisfies the exact equality

$$ \deg_{\pm}(f_8)=2<3=H^{\ast}(f_8). $$

The current certified smallest-dimension bracket is

$$ 5\leq n_{\mathrm{sep}}\leq8. $$

Equality is proved for every function on at most four bits. On five bits, exact equality is proved in threshold degrees $0,1,2,4,5$. The only unresolved five-bit case is threshold degree $3$. A large exact-cover computation for that case is safely checkpointed but has not reached UNSAT.

A promising six-bit candidate has exact threshold degree $4$, but its four-head impossibility is not proved. The strongest surviving lower-bound route is a full-cube cleared degree-five multiplier cone. Its exact reductions and extensive corner and edge audits are saved below.

## Completed eight-bit separation

For $x,y\in\lbrace0,1\rbrace^4$, define

$$ \Delta(x,y)=\sum_{i=1}^{4}(x_i+y_i-2x_iy_i). $$

Then $f_8=1$ exactly when $\Delta\geq2$.

The proof has three exact parts.

1. The polynomial $\Delta-3/2$ gives $\deg_{\pm}(f_8)\leq2$, and a two-bit XOR restriction gives the matching lower bound.

2. Every quadratic sign representative has a nonsingular mixed coefficient matrix with negative-definite symmetric part. The fourteen exact checkerboard rectangles and the column-max spectral argument exclude every admissible two-head factorization.

3. An explicit integer three-denominator dictionary and cleared-score vector give a strict three-head representation.

Authoritative files:

- `lemmas/06_strict_separations/189_eight_bit_hamming_threshold_strict_separation.md`
- `artifacts/calculations/verify_eight_bit_hamming_threshold_separation.py`
- `artifacts/calculations/verify_f8_three_head_upper.py`
- `artifacts/calculations/f8_three_head_upper_search.json`

Verification:

```bash
python3 artifacts/calculations/verify_eight_bit_hamming_threshold_separation.py
python3 artifacts/calculations/verify_f8_three_head_upper.py
```

Both commands passed at handoff time. The first verifies the quadratic lower-bound geometry and the exact value $H^{\ast}(f_8)>2$. The second verifies denominator positivity and the exact three-head score, giving $H^{\ast}(f_8)\leq3$.

## Exact lower-dimensional results

### Through four bits

Every Boolean function on at most four bits satisfies

$$ H^{\ast}(f)=\deg_{\pm}(f). $$

The four-bit step is a complete exact computer-assisted classification.

Files:

- `lemmas/06_strict_separations/183_small_dimension_exact_classification.md`
- `artifacts/calculations/verify_small_n4_exact_classification.py`
- `artifacts/calculations/small_n4_exact_classification_certificate.npz`

Verification:

```bash
python3 artifacts/calculations/verify_small_n4_exact_classification.py
```

### Five-bit degrees already completed

The following cases are exact.

| Threshold degree | Status | Main files |
|---:|:---|:---|
| 0 | Equality | Constant classification |
| 1 | Equality | One-head characterization |
| 2 | $H^{\ast}=2$ | `lemmas/06_strict_separations/187_five_bit_degree_two_exact.md` |
| 4 | $H^{\ast}=4$ | `lemmas/06_strict_separations/186_five_bit_degree_four_exact.md` |
| 5 | Equality | Exact parity theorem |

The only possible five-bit strict separation has threshold degree $3$.

Representative exact verification commands for the completed five-bit cases are:

```bash
python3 artifacts/calculations/verify_n5_k5_stress_reduction.py
python3 artifacts/calculations/verify_n5_c5_cocircuit_inventory.py
python3 artifacts/calculations/verify_n5_c5_cocircuit_tangent_cover.py artifacts/calculations/n5_c5_tangent_clause_cover.json
python3 artifacts/calculations/verify_n5_c5_fixed_chord_extremizer.py --incidence artifacts/calculations/n5_c5_locked_extreme_ray_incidence.json

python3 artifacts/calculations/verify_n5_degree4_reduction.py
python3 artifacts/calculations/search_n5_degree4_family_shattering.py --verify-only
python3 artifacts/calculations/verify_n5_degree4_other_residuals.py
python3 artifacts/calculations/classify_n5_degree4_face_family.py
```

## Five-bit degree-three exact-cover checkpoint

Assigned question: prove that every five-bit function with threshold degree at most $3$ has a three-head representation.

The search was stopped safely after iteration $624$. The universal cover is not complete.

- Exact families: `13973`.
- Learned certificates: `834`.
- Singleton orbits: `834`.
- Base dictionary entries: `98`.
- Active CNF clauses: `6641832`.
- Last eliminated candidate: `0x16e0e054`.
- Last outcome: exact fixed-dictionary hit.
- Every candidate from iteration $590$ through iteration $624$ was a direct exact dictionary hit.
- `final_dpll` is `None`.
- No PicoSAT UNSAT, compiled watched-literal UNSAT, or independent Python UNSAT verification has occurred.

Authoritative checkpoint:

`artifacts/calculations/n5_cubic_dictionary_active_checkpoint.json`

SHA-256:

```text
abb7dbc60725904e41926542426b87b71b549db26d94c36990201747d70f6bd0
```

Relevant files:

- `artifacts/calculations/search_n5_cubic_dictionary_milp.py`
- `artifacts/calculations/verify_n5_cubic_dictionary_cover.py`
- `artifacts/calculations/solve_n5_clause_cnf.cpp`
- `artifacts/calculations/n5_cubic_dictionary_active_checkpoint.json`
- `artifacts/calculations/n5_cubic_pocket13_cocircuit_sweep.json`

The final archive `artifacts/calculations/n5_cubic_dictionary_cover.json` does not yet exist.

Resume command:

```bash
python artifacts/calculations/search_n5_cubic_dictionary_milp.py \
  --resume \
  --iterations 1000 \
  --dpll-solver pycosat \
  --dpll-node-limit 5000000 \
  --family-attempts 512 \
  --families-per-hit 32 \
  --spaces-per-hit 1 \
  --existing-families-per-hit 4 \
  --inner-lp-restarts 4 \
  --inner-lp-max-iterations 180 \
  --continuous-restarts 64 \
  --continuous-max-iterations 8000 \
  --output artifacts/calculations/n5_cubic_dictionary_active_checkpoint.json \
  --final-output artifacts/calculations/n5_cubic_dictionary_cover.json
```

When PicoSAT first reports UNSAT, let the search code confirm it with the compiled watched-literal solver. Then run the independent verifier:

```bash
python artifacts/calculations/verify_n5_cubic_dictionary_cover.py \
  artifacts/calculations/n5_cubic_dictionary_cover.json \
  --dpll-node-limit 10000000
```

Do not claim the five-bit theorem until all three UNSAT stages have passed.

One formerly difficult mask, `0x6a83833c`, now has a curated exact T7 certificate with minimum signed cleared score `98295670831783832544`. The checkpoint migration for that certificate is exact and idempotent.

Failed five-bit side route: the exact $13$-vertex pocket cocircuit sweep found no compatible tangent ray. Its no-hit artifact is preserved in `artifacts/calculations/n5_cubic_pocket13_cocircuit_sweep.json`.

## Six-bit candidate

Start with six-bit parity and flip exactly the three weight-three vertices

$$ E=\lbrace21,38,41\rbrace=\lbrace010101,100110,101001\rbrace. $$

The truth mask is

```text
0x96696bd669b69669
```

The exact verifier gives an integer quartic sign polynomial and a positive degree-three Gordan circuit, proving

$$ \deg_{\pm}(f_6)=4. $$

Files:

- `artifacts/calculations/verify_n6_parity_midlayer_triple_candidate.py`
- `artifacts/calculations/n6_parity_midlayer_triple_rigidity.md`
- `artifacts/calculations/n6_parity_midlayer_triple_slice_poset.md`

Verification:

```bash
python3 artifacts/calculations/verify_n6_parity_midlayer_triple_candidate.py
python3 artifacts/calculations/verify_n6_parity_midlayer_triple_slice_poset.py
```

No exact four-head representation has been found, and no universal four-head obstruction has been proved. Therefore this function is a candidate only. Do not call it a separation.

## Strongest surviving six-bit route

For four positive oriented affine denominators, define

$$ F=\prod_{h=0}^{3}B_h, \qquad P_h=F/B_h, $$

and the cleared signed tangent row

$$ G(z)=s(z)\left(F(z),\left(z_iP_h(z)\right)_{0\leq h\leq3,0\leq i\leq5}\right). $$

The degree-at-most-five value space on the full six-cube is

$$ V_5=\lbrace q\in\mathbb{R}^{64}:p^{\top}q=0\rbrace. $$

The strongest surviving conjecture is that every admissible four-denominator dictionary has a nonzero nonnegative, preferably positive, vector satisfying

$$ q\geq0, \qquad G^{\top}q=0, \qquad p^{\top}q=0. $$

If this holds universally, then the six-bit candidate has no four-head representation.

The exact Gordan alternative is a nonzero augmented separator

$$ A(z)=s(z)R(z)+\beta p(z)\geq0, $$

where

$$ R=aF+\sum_{h=0}^{3}\ell_hP_h $$

and every $\ell_h$ is homogeneous linear. The exact moment identity

$$ \sum_zH(z)A(z)=2\sum_{e\in E}H(e)R(e) $$

holds for every affine $H$.

Exact results for this route:

- The common kernel over every literal-corner dictionary has rank data `58 of 64` and dimension `6`.
- Every common-kernel vector is $q=spL$, with $L$ affine and $\sum_{e\in E}L(e)=0$.
- This common kernel has no nonzero nonnegative vector, so one multiplier cannot work at every corner.
- The full-cube uncleared $V_5$ route is structurally impossible because $s^{\top}y=p^{\top}y=0$ would force $2\sum_{e\in E}y(e)=0$.
- The structured subcone $q=(sp)r$ with $\deg(r)\leq3$ is structurally impossible for the same parity-relation reason.

Numerical evidence, not proof:

- All `7203` literal-corner dictionaries have a nonzero nonnegative multiplier.
- `6966` corners have a strict multiplier and `237` are boundary-only.
- All `36015` inequivalent simplex edges have a nonzero nonnegative common multiplier.
- `31044` edges are strict and `4971` are boundary-only.
- Five exact hard denominator tuples have positive normalized full-cube margins.
- Twelve adversarial restarts found only boundary-approaching positive margins.

The complete status, exact formulas, corner classifications, edge counts, and hard-tuple margins are saved in:

- `artifacts/calculations/n6_parity_triple_full64_cleared_v5_route.md`
- `artifacts/calculations/verify_n6_parity_triple_full64_common_kernel.py`
- `artifacts/calculations/audit_n6_parity_triple_full64_cleared_v5_corners.py`
- `artifacts/calculations/audit_n6_parity_triple_full64_cleared_v5_edges.py`
- `artifacts/calculations/screen_n6_parity_triple_full64_v5_hard_tuples.py`
- `artifacts/calculations/search_n6_parity_triple_repaired_quartic_multiplier.py`

Commands:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_full64_common_kernel.py
python3 artifacts/calculations/screen_n6_parity_triple_full64_v5_hard_tuples.py
python3 artifacts/calculations/audit_n6_parity_triple_full64_cleared_v5_corners.py
python3 artifacts/calculations/audit_n6_parity_triple_full64_cleared_v5_edges.py
```

The corner and edge scripts use numerical LP internally. Their exhaustive counts are evidence, not exact universal certificates. The saved edge audit was interrupted after two classes during the final checkpoint rerun, but an earlier exploratory run completed all five classes and produced the counts recorded in the route note.

## Exact affine weak-dual reduction

On the repaired support $S_{56}$, the affine weight

$$ Q(z)=2+z_5-z_4 $$

is nonnegative and vanishes at the two retained exceptional points $38,41$. For every quartic $T$,

$$ \sum_{z\in S_{56}}s(z)Q(z)T(z)=-\sum_{z\in K}p(z)Q(z)T(z). $$

The right side is supported on only six omitted points:

$$ \lbrace6,9,21,27,54,57\rbrace. $$

This is an exact reduction, not a completed obstruction. Cancelling this six-point residual is a focused alternative to the full simplex-face induction.

Files:

- `artifacts/calculations/n6_parity_triple_affine_weak_dual_reduction.md`
- `artifacts/calculations/verify_n6_parity_triple_affine_weak_dual_reduction.py`

Verification:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_affine_weak_dual_reduction.py
```

## Quartic tangent image

The cleared four-head quartic tangent map

$$ \Phi(B,A)=\sum_{h=0}^{3}A_h\prod_{j\neq h}B_j $$

has exact Zariski dimension $49$ inside the $57$-dimensional quartic coefficient space. The parameter count is $56$ with seven exact gauge directions, and a positive-orientation integer point has Jacobian rank $49$ modulo $1000003$.

The image spans all $57$ coefficient coordinates linearly. Exact character-block calculations over $\mathbb{F}_{101}$ show that it has no rational algebraic equation in coefficient degrees $2$, $3$, or $4$. A stabilizer-invariant quintic detector also has full rank in every character weight, but that quintic test is not representation-complete.

Files:

- `artifacts/calculations/verify_n6_quartic_tangent_dimension.py`
- `artifacts/calculations/search_n6_quartic_tangent_invariants.py`
- `artifacts/calculations/n6_quartic_tangent_low_degree_invariants.md`

Verification:

```bash
PYTHONPATH=artifacts/calculations python3 artifacts/calculations/verify_n6_quartic_tangent_dimension.py
PYTHONPATH=artifacts/calculations python3 artifacts/calculations/search_n6_quartic_tangent_invariants.py --degree 2
PYTHONPATH=artifacts/calculations python3 artifacts/calculations/search_n6_quartic_tangent_invariants.py --degree 3
```

For degree four, run each weight from $0$ through $6$:

```bash
PYTHONPATH=artifacts/calculations python3 artifacts/calculations/search_n6_quartic_tangent_invariants.py --degree 4 --weight 0 --block-size 128
```

For the incomplete stabilizer-invariant quintic diagnostic, likewise repeat each weight:

```bash
PYTHONPATH=artifacts/calculations python3 artifacts/calculations/search_n6_quartic_tangent_invariants.py --degree 5 --weight 0 --orbit-sums --block-size 128
```

Low-degree algebraic invariants are therefore not a viable shortcut. A representation-complete quintic calculation is possible but substantially larger.

## Important exact negative results

These results rule out proposed proof ansatzes. They do not refute the six-bit candidate.

| Failed route | Exact status | Main verifier or note |
|:---|:---|:---|
| Fixed support $U$ of size $54$ | Exact counterexample | `verify_n6_parity_triple_support54_counterexample.py` |
| Blockwise degree-two dual decomposition | Exact counterexample | `verify_n6_parity_triple_blockwise_degree2_limit.py` |
| Slice-only positive cone | Exact limitation | `verify_n6_parity_triple_slice_cone_limit.py` |
| Edge and quotient-cut cone | Exact limitation | `verify_n6_parity_triple_edge_cut_cone_limit.py` |
| Adaptive antipodal alpha grouping | Exact counterexample | `verify_n6_parity_triple_adaptive_alpha_counterexample.py` |
| Positive cubic $q$ on $U$ | Exact counterexample | `verify_n6_parity_triple_cubic_positive_limit.py` |
| Positive quartic $q$ on $U$ | Exact counterexample | `verify_n6_parity_triple_quartic_positive_limit.py` |
| Uncleared degree-four multiplier on $S_{55}$ | Exact strict augmented separator | `verify_n6_parity_triple_s55_uncleared_degree4_limit.py` |
| Uncleared degree-four multiplier on $S_{56}$ | Exact strict augmented separator | `verify_n6_parity_triple_s56_uncleared_degree4_limit.py` |
| Cleared degree-four multiplier on $S_{56}$ | Exact strict augmented separator, minimum `852046508` | `verify_n6_parity_triple_s56_cleared_degree4_limit.py` |
| One common multiplier over all literal corners | Exact common kernel is sign-changing | `verify_n6_parity_triple_full64_common_kernel.py` |
| Rational invariant through coefficient degree four | Exact nonexistence over $\mathbb{Q}$ | `n6_quartic_tangent_low_degree_invariants.md` |

Useful exact support geometry and complementarity files:

- `artifacts/calculations/verify_n6_parity_triple_support54_geometry.py`
- `artifacts/calculations/verify_n6_parity_triple_repaired_degree4_relations.py`
- `artifacts/calculations/verify_n6_parity_triple_endpoint_complementarity.py`
- `artifacts/calculations/n6_parity_triple_repaired_degree4_relations.md`
- `artifacts/calculations/n6_parity_triple_endpoint_complementarity.md`

A batch of representative exact checks is:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_support54_geometry.py
python3 artifacts/calculations/verify_n6_parity_triple_support54_counterexample.py
python3 artifacts/calculations/verify_n6_parity_triple_blockwise_degree2_limit.py
python3 artifacts/calculations/verify_n6_parity_triple_adaptive_alpha_counterexample.py
python3 artifacts/calculations/verify_n6_parity_triple_cubic_positive_limit.py
python3 artifacts/calculations/verify_n6_parity_triple_quartic_positive_limit.py
python3 artifacts/calculations/verify_n6_parity_triple_repaired_degree4_relations.py
python3 artifacts/calculations/verify_n6_parity_triple_s55_uncleared_degree4_limit.py
python3 artifacts/calculations/verify_n6_parity_triple_s56_uncleared_degree4_limit.py
python3 artifacts/calculations/verify_n6_parity_triple_s56_cleared_degree4_limit.py
python3 artifacts/calculations/verify_n6_parity_triple_endpoint_complementarity.py
```

## Seven-bit restriction check

Natural literal restrictions and coordinate identifications of the eight-bit function did not produce a seven-bit separation. In particular, continuous one-oriented-factor searches found exact two-head certificates for the cross-identification masks

```text
0x573f3fab5dcfcfae75f3f3bad5fcfcea
0x3f57ab3fcf5daecff375baf3fcd5eafc
```

and the coordinate restriction was also two-head. The discovery command was based on:

```bash
python3 artifacts/calculations/search_continuous_one_oriented_factor.py
```

This check is now recorded here because it was not promoted to a separate theorem or verifier. It only rules out the most direct seven-bit minors of $f_8$.

## Remaining tasks in priority order

1. Resume and finish the five-bit degree-three exact cover. Require PicoSAT UNSAT, compiled watched-literal UNSAT, and independent Python UNSAT before claiming the five-bit theorem.

2. For the six-bit candidate, pursue an exact simplex-face induction for the full-cube cleared $V_5$ cone. Start by classifying the `237` boundary-only corner cases and `4971` boundary-only edge classes by exact facial reduction.

3. Determine common nonnegative kernels on higher-dimensional denominator-simplex faces. Show that each face either has a strict common multiplier or reduces to one of the classified boundary types.

4. In parallel only if it remains focused, try to cancel the exact six-point residual from the affine weak-dual reduction.

5. If the multiplier route stalls, test the exact augmented alternative $sR+\beta p\geq0$ directly against denominator orientation. A representation-complete quintic invariant search is a later and more expensive fallback.

6. If a six-bit four-head obstruction is completed, combine it with the finished five-bit theorem. This would prove that six bits is minimal. Then determine or bound the exact value of $H^{\ast}$ for the six-bit function if the final theorem is intended to state more than strict inequality.

7. If the six-bit candidate is refuted by an exact four-head construction, preserve that certificate and return to seven-bit candidate search. Do not infer anything from numerical non-discovery alone.

## Claims that are safe now

- The eight-bit Hamming-threshold function is an explicit exact separation with $\deg_{\pm}=2$ and $H^{\ast}=3$.
- Every Boolean function on at most four bits has equality.
- Five-bit equality is exact outside threshold degree $3$.
- The six-bit parity-triple candidate has exact threshold degree $4$.
- The full-cube cleared $V_5$ route is the strongest surviving six-bit obstruction route, but it is not a proof.
- Therefore the only certified minimal-dimension statement is $5\leq n_{\mathrm{sep}}\leq8$.

## Claims that are not safe

- Do not claim that every five-bit cubic threshold has three heads.
- Do not claim that the six-bit candidate is a strict separation.
- Do not claim that the corner or edge LP audits prove the full multiplier conjecture.
- Do not claim that no quintic invariant exists. Only the stabilizer-invariant quintic subspace was checked.
- Do not claim that seven bits is impossible. Only natural minors of the eight-bit example were tested.

## Handoff integrity checks

At handoff time, `git diff --check -- CLOUD_HANDOFF.md` passed. The file has no em dash characters, no math in headings, and none of the unsafe GitHub math macros prohibited by `AGENTS.md`.

The checkpoint SHA-256 was recomputed and matched the value recorded above. A path audit found that every referenced certificate path exists except `artifacts/calculations/n5_cubic_dictionary_cover.json`, which is explicitly documented as not yet created.

The following exact smoke verifiers all exited successfully during the final handoff pass:

```bash
python3 artifacts/calculations/verify_eight_bit_hamming_threshold_separation.py
python3 artifacts/calculations/verify_f8_three_head_upper.py
python3 artifacts/calculations/verify_n6_parity_midlayer_triple_candidate.py
python3 artifacts/calculations/verify_n6_parity_triple_full64_common_kernel.py
python3 artifacts/calculations/verify_n6_parity_triple_affine_weak_dual_reduction.py
python3 artifacts/calculations/verify_n6_parity_triple_s56_cleared_degree4_limit.py
python3 artifacts/calculations/verify_n6_parity_triple_s56_uncleared_degree4_limit.py
python3 artifacts/calculations/verify_n6_quartic_tangent_dimension.py
```

The collaboration manager reports all three subagents completed. Process inspection with `ps` was unavailable in the local sandbox, but the five-bit agent explicitly terminated its search after checkpointing, and the two six-bit agents stopped after writing their artifacts.

## Worktree precautions

The repository contains extensive uncommitted and untracked work from this investigation. Before any branch switch, rebase, cleanup, or archive operation:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

Preserve the active checkpoint and all exact certificate artifacts. In particular, never overwrite `artifacts/calculations/n5_cubic_dictionary_active_checkpoint.json` with a new run unless the new process is invoked with `--resume` and the current SHA-256 has first been recorded.
