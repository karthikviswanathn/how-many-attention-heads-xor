# Cloud Task Handoff

## Continuation update

The user resumed the task after the original handoff. On 2026-07-17, the active branch was `codex/sprint-1` at commit `5a9ae507282ce7ad2781b879cce9f57fd297bb97`. The worktree then contained uncommitted certified-estimator code, documentation, and the new six-head certificate described below. Inspect `git status --short` before treating the earlier clean-checkout language as current. The latest concrete six-bit result is the rigorous interval $4\leq H^{\ast}(f_6)\leq6$. The active objective is now a scalable certified methodology for general $H^{\ast}(f)$, not only the six-bit candidate.

## Stop state

This handoff was prepared on 2026-07-14 after the user asked the local task to stop and transfer its state to a new Codex cloud task. It was refreshed on 2026-07-15 after the research snapshot was reviewed, committed, and pushed.

- Historical goal status at the original handoff: paused. Current general-methodology continuation: active.
- Git branch: `codex/sprint-1`.
- Reviewed research snapshot: `8e2f8a4f2a01edcfca138396de016033818dffc4`.
- The cloud environment files were added after that research snapshot on the same branch. The cloud task should check out the current branch tip and record `git rev-parse HEAD` before doing work.
- The formerly untracked certificate files are committed. Start from a clean checkout, and do not run `git clean`, `git reset --hard`, or discard later work without inspecting it.
- All three subagents have stopped.
- The long five-bit exact-cover process was terminated only after writing a complete iteration-624 checkpoint.
- No research process is intentionally left running.

The reviewed research snapshot contains the completed theorem files, exact certificates, exploratory records, and active five-bit checkpoint. The current branch tip is authoritative because it also contains the cloud environment manifest.

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

## Cloud Python environment

The repository root contains a `uv` project for the Python research scripts:

- `pyproject.toml` declares Python `3.12` and the dependency groups.
- `.python-version` asks `uv` to use Python `3.12`.
- `uv.lock` pins the resolved packages for reproducible cloud setup.
- `[tool.uv] package = false` keeps this as a script environment. It does not build or install the repository as a Python package.

Create the minimal handoff environment with:

```bash
uv sync --frozen
```

This default environment includes NumPy, SciPy, pycosat, and threadpoolctl. It is sufficient for the exact certificate verifiers, the active five-bit degree-three cover, and the main six-bit multiplier scripts.

The broader symbolic, graph, and Z3 scripts use the optional research dependencies:

```bash
uv sync --frozen --extra research
```

PyTorch is isolated because its wheels are large and only two exploratory scripts import it. Install it only when those searches are needed:

```bash
uv sync --frozen --extra torch
```

Use both optional groups only if the cloud task needs every Python route:

```bash
uv sync --frozen --all-extras
```

After synchronization, every command below can replace `python` or `python3` with `uv run python`. For example:

```bash
uv run python artifacts/calculations/verify_eight_bit_hamming_threshold_separation.py
uv run python artifacts/calculations/verify_f8_three_head_upper.py
```

The experimental package under `src/hstar/` is not installed by the script environment. If it is needed, invoke it explicitly with:

```bash
PYTHONPATH=src uv run python -m hstar.cli --help
```

Lean is intentionally out of scope for this cloud handoff. Do not install Lean or run `lake`. A C++17 compiler is still useful for the independent watched-literal solver in `artifacts/calculations/solve_n5_clause_cnf.cpp`.

Environment preparation on the local handoff machine was metadata-only. `uv lock` resolved the dependency graph with an existing bundled Python `3.12.13`, but `uv sync` was deliberately not run, no `.venv` was created, and no package was installed. The first cloud task should perform the frozen sync and then run the two eight-bit smoke verifiers shown above before resuming a long search.

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

Under the repository mask convention this is even parity with the three vertices flipped. Odd parity with the same flips has complementary mask `0x6996942996496996`. Complement invariance gives the same threshold degree and head complexity.

The exact verifier gives an integer quartic sign polynomial and a positive degree-three Gordan circuit, proving

$$ \deg_{\pm}(f_6)=4. $$

Files:

- `artifacts/calculations/verify_n6_parity_midlayer_triple_candidate.py`
- `artifacts/calculations/n6_parity_midlayer_triple_rigidity.md`
- `artifacts/calculations/n6_parity_midlayer_triple_slice_poset.md`
- `artifacts/calculations/n6_parity_midlayer_triple_h6_certificate.json`
- `artifacts/calculations/verify_n6_parity_midlayer_triple_h6.py`

A continuous oriented-denominator search found an exact six-head upper certificate with orientations $(-,-,-,+,+,+)$. Its minimum signed cleared score is `11861735510772`, and its maximum is `1053462090324445872`. Therefore the current unconditional interval is

$$ 4\leq H^{\ast}(f_6)\leq6. $$

Verification:

```bash
python3 artifacts/calculations/verify_n6_parity_midlayer_triple_candidate.py
python3 artifacts/calculations/verify_n6_parity_midlayer_triple_slice_poset.py
python3 artifacts/calculations/verify_n6_parity_midlayer_triple_h6.py
PYTHONPATH=src python3 -m hstar.certified_cli verify --dimension 6 --mask 0x96696bd669b69669 --certificate artifacts/calculations/n6_parity_midlayer_triple_h6_certificate.json
```

No exact four-head or five-head representation has been found, and no universal obstruction excludes either count. Therefore this function is a candidate only. Do not call it a separation, and do not claim that the exact head count is six.

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

$$ \sum&#95;{z\in S&#95;{56}}s(z)Q(z)T(z)=-\sum&#95;{z\in K}p(z)Q(z)T(z). $$

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

$$ \Phi(B,A)=\sum&#95;{h=0}^{3}A&#95;h\prod&#95;{j\neq h}B&#95;j $$

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

## Current general-methodology continuation

The current active objective is broader than the six-bit case: construct a scalable, certified methodology for estimating lower and upper bounds on $H^{\ast}(f)$ for an arbitrary truth table.

The main new research artifact is:

- `artifacts/calculations/general_hstar_scalable_research_program.md`

The updated implementation architecture is:

- `artifacts/calculations/scalable_hstar_bound_methodology.md`

The formal slice-rank theorem is:

- `lemmas/02_complexity_measure_upper_bounds/190_slice_rank_two_obstruction.md`

Its exact Boolean-cube limitation is:

- `lemmas/02_complexity_measure_upper_bounds/191_boolean_cube_slice_relaxation_ceiling.md`

The exact multiway tensor limitation is:

- `lemmas/02_complexity_measure_upper_bounds/192_multiway_sign_tensor_rank.md`

The high-head and weighted-matrix designs are:

- `artifacts/calculations/high_head_hstar_methodology.md`
- `artifacts/calculations/weighted_tau_hard_core_scheduler.md`

New established results and directions recorded there include:

1. Every homogeneous cleared $H$-head form is a Chow tangent and lies in the second Chow secant closure.

2. For $H\geq2$, every cleared form has polynomial slice rank at most two:

$$ P=L_1Q_1+L_2Q_2. $$

One slice generator can be chosen from an admissible denominator cone. The fixed-plane inner problem is an LP, while the outer Grassmannian has dimension $2(n-1)$, independent of $H$. Choosing a largest Plücker pivot gives a complete bounded atlas with $\binom{n+1}{2}$ boxes and chart entries in $[-1,1]$. On maximal-rank cells, the selected evaluation rows are affine in the chart variables, so exact inradius and row-motion certificates can cover whole cells.

Boolean evaluation sharply limits this route. With $D&#95;d=\sum_{j=0}^{d}\binom nj$, the maximum fixed-plane evaluation rank is $\min\lbrace D&#95;H,2D&#95;{H-1}-D&#95;{H-2}\rbrace$. For $H\geq\lceil(n+1)/2\rceil$, one fixed plane containing an admissible denominator spans every degree at most $H$ cube polynomial. The slice relaxation is then exactly threshold degree. In particular, it cannot improve the four-head lower bound for the six-bit parity triple flip.

3. The same tangent has a positive-secant compactification with $2Hn+1$ parameters and balanced block splits with coefficient scale $O(n^{\lceil H/2\rceil})$.

4. Every cleared form satisfies $\mathrm{rank}(\mathrm{Cat}_k(P))\leq2\binom{H}{k}$, with first catalecticant rank at most $2H$. For cubic slice rank two in seven variables, a concrete $210\times196$ Jacobian Macaulay matrix has rank at most $169$.

5. For candidate count $H=2$, the real second-secant relaxation strengthens rank at most four to the exact inertia conditions $n&#95;+(M&#95;P)\leq2$ and $n&#95;-(M&#95;P)\leq2$.

6. The optimized Linial, Mendelson, Schechtman, and Shraibman quantity

$$ \tau(S)=\min\left\lbrace\gamma_2^{\ast}(W):S\circ W\geq\mathbf1\right\rbrace $$

gives a certifiable partition sign-rank backend that dominates the literal $\gamma&#95;2^{\ast}$ bound. Product average margin with nonuniform row and column weights can strengthen it further. Rational feasible PSD witnesses have the safe certificate direction.

7. Cost-aware Walsh and monotone-monomial column generation prices all features in $O(n2^n)$ time. Affine-cylinder branch-and-price and direct denominator-group boosting give complementary constructive upper searches. Only exact refitting and full-cube verification change the upper endpoint.

8. Full-dimensional robust Gordan obstructions have positive-spanning supports of at most $2(1+Hn)$ rows. A centered inball plus the exact telescoping row-motion bound certifies a whole denominator cell without cofactors.

9. Exact infeasibility on any sampled truth-table subset is a valid global lower certificate. Feasibility on a subset is not an upper certificate.

10. Positive-denominator rational sign degree is only threshold degree. The tangent shared-factor constraint is the model-specific information.

11. The strengthened Fourier lemma aggregates the constant and singleton-character portion into at most one head, then charges $\lvert S\rvert$ only for each active Walsh character with $\lvert S\rvert\geq2$.

12. Average sensitivity gives a cheap exact $O(n2^n)$ degree presolve from bichromatic cube edges, but it was weak on the first small benchmarks.

13. For $k$ coordinate blocks, every $H$-head sign tensor has sign CP rank at most $k(k^H-(k-1)^H)$. The ambient CP-rank ceiling proves that rank size alone cannot improve the balanced matrix screen $n\geq2H+2$, regardless of the block count.

14. The full tangent and positive-secant closures can remain proper above the matrix and slice midpoint ceilings. The high-head route therefore uses positive-secant pair inequalities, low-degree adjustable Gordan policies, and robust positive-basis cells rather than more flattening rank.

15. The public estimator now implements optional transform-priced sparse PTF column generation. On equality of two six-bit strings it returned a verified $7$-head certificate from $80$ generated columns, using at most $712704$ restricted-master entries instead of a $16777216$-entry full matrix. Weighted $\ell_1$ remains only a support heuristic.

16. The weighted $\tau$ pilot verifies exact rational Gram-plus-residual certificates on Sylvester matrices and on a hard eight-by-eight block padded to order sixteen. Zero-supported product weights preserve certified sign-rank at least three on the padded instance.

17. The public estimator also exposes the exact absolute Fourier-tail knapsack behind vertex and transition budgets. On mask `0xb1e41b4e278d72d8`, it improves exhaustive positive projection from $15$ heads to $8$ using $20$ dynamic-program transitions. The exact certificate is `artifacts/calculations/six_bit_optimal_fourier_tail_h8_certificate.json`.

The next general implementation priorities are:

1. implement rational McCormick and RLT signed-secant cell certificates with exact probability-vector leaves;

2. prototype output-normalized atomic boosting with fixed-denominator numerator pricing;

3. promote the weighted $\tau$ pilot into the library, then add rational product-weight optimization and hard-core scheduling;

4. implement a degree-one adjustable Gordan-policy LP on mined supports with exact coefficient and positivity checking;

5. benchmark the integrated upper portfolio across parity, majority, juntas, random targets, DNF and CNF families, address functions, and sparse parity perturbations;

6. run a bounded slice Grassmann atlas only on instances that pass the implemented Boolean collapse screen;

7. add exact infeasible witness subsets as a shared certificate type;

8. implement inradius-oriented positive-basis extraction, exact row-motion cells, and the coupled upper-feature and lower-scenario exchange loop;

9. add direct denominator-group boosting with fixed-denominator exactification.

Latest verification commands:

```bash
UV_CACHE_DIR=/tmp/hstar-uv-cache PYTHONPATH=src uv run --offline python artifacts/calculations/verify_sparse_ptf_prototype.py
UV_CACHE_DIR=/tmp/hstar-uv-cache PYTHONPATH=src uv run --offline python artifacts/calculations/verify_certified_hstar_estimator.py
UV_CACHE_DIR=/tmp/hstar-uv-cache PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --offline python artifacts/calculations/weighted_tau_partition_pilot.py
UV_CACHE_DIR=/tmp/hstar-uv-cache PYTHONPATH=src uv run --offline python artifacts/calculations/verify_boolean_cube_slice_rank_and_n6_cubic_dominance.py
```

All four commands exited successfully on 2026-07-17.

## Latest general-methodology update

The general research state is now consolidated in:

- [adaptive_general_hstar_estimator.md](artifacts/calculations/adaptive_general_hstar_estimator.md), the adaptive proof portfolio, mathematical gates, certificate schemas, access modes, scheduler, cost guide, and benchmark program;

- [scalable_hstar_bound_methodology.md](artifacts/calculations/scalable_hstar_bound_methodology.md), the complete anytime hierarchy;

- [general_hstar_scalable_research_program.md](artifacts/calculations/general_hstar_scalable_research_program.md), the analytic derivations and broader research map;

- [high_head_hstar_methodology.md](artifacts/calculations/high_head_hstar_methodology.md), the model-native high-head route;

- [literature_survey.md](literature_survey.md), the primary-source literature synthesis.

The main conclusion is that no single surrogate should estimate $H^{\ast}$. Maintain an interval

$$ L(f)\leq H^{\ast}(f)\leq U(f) $$

and admit an endpoint change only after an independent exact verifier accepts its certificate. Upper and lower engines should exchange hard vertices and dual weights, while keeping all floating discovery data outside the proof graph.

### Theorem 194. Signed-secant compactification

[Theorem 194](lemmas/02_complexity_measure_upper_bounds/194_signed_secant_diagonal_blowup.md) retains the positive-secant mixture scalar and writes

$$ \theta^{(1)}=\theta+tv,\qquad 2s-1=ta,\qquad \max\lbrace\lVert v\rVert&#95;{\infty},\lvert a\rvert\rbrace=1. $$

The signed score is exactly divisible by $t$. Strict quotient feasibility on the closed compact chart domain is equivalent to strict signed-secant feasibility, including at $t=0$. The proof moves a boundary base point into the product-simplex interior before opening a short ray, so no face implication is required.

The signed formulation has:

- one inequality per truth-table vertex;

- $2H(n+1)+2$ raw charts;

- at most $4(n+1)+2$ chart types per orientation-count branch after head symmetry;

- scalar degree at most $H$ and total degree at most $2H+1$;

- joint head-block multidegree one.

For $n=6$ and $H=3$, this is $64$ signed inequalities instead of $1024$ balanced pair gaps, with $44$ raw charts and at most $30$ symmetry types per orientation branch.

The factor graph uses the exact recurrence

$$ P&#95;h=P&#95;{h-1}b&#95;h,\qquad R&#95;h=R&#95;{h-1}c&#95;h+P&#95;{h-1}d&#95;h. $$

The standalone verifier is [verify_signed_secant_diagonal_blowup.py](artifacts/calculations/verify_signed_secant_diagonal_blowup.py). It passed $1600$ endpoint-to-chart checks, $2400$ factor-recurrence checks, $200$ scalar-elimination checks, and exact boundary examples.

Use this quotient for spatial McCormick and RLT subdivision. Use the original unblown retained-scalar system for CAD, NLSAT, or dense Positivstellensatz residual solving because its total degree is only $H+1$.

### Theorem 195. Atomic-margin sparsification

[Theorem 195](lemmas/02_complexity_measure_upper_bounds/195_atomic_margin_sparsification.md) normalizes genuine one-head score vectors in output space. If a convex atomic score has scale $\Lambda$ and full-cube margin $\gamma$, approximate Carathéodory gives

$$ H^{\ast}(f)\leq C(n+1)\left(\frac{\Lambda}{\gamma}\right)^2. $$

This provides a principled width target for denominator-group boosting. For a fixed positive denominator, normalized affine-numerator pricing is an LP. Denominator pricing remains nonlinear. A finite rational positive-margin atomic decomposition is already a direct upper certificate. Failure to find a good atomic condition number has no lower-bound meaning.

### Theorem 196. Optimal Fourier-tail knapsack

[Theorem 196](lemmas/02_complexity_measure_upper_bounds/196_optimal_fourier_tail_knapsack.md) computes the minimum compiler cost obtainable from the absolute Fourier-tail criterion. Retain the constant coefficient for free, bundle all singleton coefficients into one cost-one item, and give each nonsingleton Walsh coefficient value equal to its absolute unnormalized mass and cost equal to its degree.

Requiring omitted mass below $2^n$ is an exact zero-one knapsack cover. Total compiler cost is at most $n2^n+1$, so dynamic programming takes

$$ O(n4^n)=O(nV^2) $$

integer operations, polynomial in the truth-table length $V=2^n$.

The implementation is [optimal_fourier_tail_upper_bound](src/hstar/sparse_ptf.py). It groups equal-degree characters, sorts their masses, and optimizes over degree-prefix choices. The public estimator exposes it through `--optimal-fourier-tail`, `--optimal-fourier-tail-max-transitions`, and `--optimal-fourier-tail-max-vertices`. Budget misses are diagnostic skips and never lower bounds. The verifier:

- checks greedy Fourier-tail certificates for all $256$ three-bit functions;

- compares the exact dynamic program with brute-force item selection for all $256$ three-bit functions;

- verifies every returned integer score independently;

- improves the fixed six-bit mask <code>0xcc4b244f3c92d063</code> from greedy compiler cost $119$ to the optimal tail cost $117$.

- verifies the archived eight-head certificate [six_bit_optimal_fourier_tail_h8_certificate.json](artifacts/calculations/six_bit_optimal_fourier_tail_h8_certificate.json) for mask <code>0xb1e41b4e278d72d8</code>. Exhaustive positive projection costs $15$ on this example, while the grouped tail program estimates $91$ transitions and executes $20$.

This is optimal only within the absolute Fourier-tail sufficient condition. It does not optimize arbitrary sparse sign polynomials and does not compute $H^{\ast}$.

### Exact signed-secant McCormick discovery and covers

The portable parameter-cell lower stack is implemented in [signed_secant_mccormick.py](src/hstar/signed_secant_mccormick.py) and documented in [signed_secant_mccormick_leaf_format.md](artifacts/calculations/signed_secant_mccormick_leaf_format.md). The checker reconstructs base boxes, simplex-aware affine bounds, product bounds, all four McCormick inequalities per product, simplex and endpoint constraints, the shared $z&#95;{hi}=tv&#95;{hi}$ lift, $\sum&#95;i z&#95;{hi}=0$, the prefix recurrence, and $C&#95;H=P&#95;H+tR&#95;H$.

It verifies nonnegative rational inequality multipliers and free rational equality multipliers against the weighted signed objective. Exact stationarity and a nonpositive exact dual value exclude strict feasibility throughout that cell. Sparse common-margin LPs can propose $\lambda$ and dual supports, but only independently verified rational reconstruction is accepted.

The first archive is [signed_secant_mccormick_leaf_xor1.json](artifacts/calculations/signed_secant_mccormick_leaf_xor1.json). It is a one-cell certificate with $23$ variables, $9$ products, $86$ inequalities, $12$ equalities, and a three-term rational dual. It is not a complete chart cover and does not establish a new global head lower bound.

The binary cover-tree checker verifies exact rational splits and derives every child box itself. [signed_secant_subcell_cover_xor1.json](artifacts/calculations/signed_secant_subcell_cover_xor1.json) is a two-leaf proper-subcell cover. [f8_h2_pp_scalar_plus_chart_cover.json](artifacts/calculations/f8_h2_pp_scalar_plus_chart_cover.json) covers the entire $a=1$ chart for the two-positive-orientation branch of the eight-bit separation. Its point mass at vertex $255$ and five-term rational dual give exact upper bound $-1$. This proves that chart infeasible, not that every two-head chart is infeasible.

The full-cube eight-bit discovery LP used sparse matrices with $6200$ variables, $23772$ inequalities, $3590$ equalities, and $2834$ products, then reduced to an $80$-variable portable leaf. [benchmark_signed_secant_mccormick.py](artifacts/calculations/benchmark_signed_secant_mccormick.py) currently finds exact root leaves on $8$ of $16$ raw one-head XOR charts, $2$ of $6$ two-head eight-bit scalar charts, and $2$ of $10$ four-head six-bit scalar charts. Every positive relaxation is recorded as unresolved, not feasible.

[Theorem 197](lemmas/02_complexity_measure_upper_bounds/197_box_sum_greedy_affine_bounds.md) isolates the tightening that made the eight-bit leaves visible. A linear form over a rational box intersected with one sum equality has exact endpoints given by ascending and descending fractional-knapsack allocation. This computes exact bounds for simplex factors, zero-sum directions, and the shared $z$ lift in $O(n\log n)$. The verifier compares the rule with every extreme point of $700$ random rational box-sum polytopes and all $512$ zero-one literal masks on a nine-coordinate simplex.

### Current lower and upper scheduling policy

The recommended lower frontier is:

1. safe restrictions, structural theorems, sensitivity, and exact threshold degree;

2. partition spectral, $\tau$, and weighted $\tau$ only when the side-size gate $n\geq2H+2$ passes;

3. screened slice and coefficient methods below their Boolean midpoint collapse;

4. signed-secant McCormick and RLT cells, adjustable Gordan policies, and robust positive-basis cells;

5. CAD, NLSAT, Positivstellensatz, or SOS only on small residual systems.

The recommended upper frontier is:

1. structural constructions, positive projections, minority support, and archived exact families;

2. greedy and optimal Fourier tails;

3. monotone and Walsh sparse-PTF refitting and transform-priced column generation;

4. output-normalized atomic boosting;

5. direct denominator variable projection, rationalization, and exact full-cube checking.

Important gates and negative results:

- exact black-box determination has a worst-case $\Omega(2^n)$ query barrier;

- a failed numerical upper search never raises the lower endpoint;

- a feasible signed secant is not an upper certificate for the original head model;

- partition rank cannot rule out $H$ heads when $n\leq2H+1$;

- plain and positivity-aware slice rank collapse to threshold degree at the Boolean middle level;

- VC and parameter-count bounds support witness mining but give no Helly theorem for a small deterministic infeasible witness;

- dense SOS is a residual method, not a root solver for the full high-head system.

### Latest verification

These commands passed after the latest update:

~~~bash
PYTHONPATH=src:artifacts/calculations python3 artifacts/calculations/verify_positive_secant_diagonal_blowup.py
PYTHONPATH=src:artifacts/calculations python3 artifacts/calculations/verify_signed_secant_diagonal_blowup.py
PYTHONPATH=src python3 artifacts/calculations/verify_sparse_ptf_prototype.py
PYTHONPATH=src python3 artifacts/calculations/verify_certified_hstar_estimator.py
PYTHONPATH=src python3 -m hstar.certified_cli verify --dimension 6 --mask 0xb1e41b4e278d72d8 --certificate artifacts/calculations/six_bit_optimal_fourier_tail_h8_certificate.json
PYTHONPATH=src python3 artifacts/calculations/verify_signed_secant_mccormick_leaf.py
PYTHONPATH=src python3 artifacts/calculations/verify_signed_secant_cell_cover.py
PYTHONPATH=src python3 artifacts/calculations/benchmark_signed_secant_mccormick.py
PYTHONPATH=src python3 artifacts/calculations/verify_box_sum_affine_bounds.py
PYTHONPATH=src python3 -m hstar.certified_cli verify --dimension 1 --mask 0x2 --certificate artifacts/calculations/signed_secant_mccormick_leaf_xor1.json
PYTHONPATH=src python3 -m hstar.certified_cli verify --dimension 8 --mask 0x177f2bbf4ddf8eef71f7b2fbd4fde8fe7f17bf2bdf4def8ef771fbb2fdd4fee8 --certificate artifacts/calculations/f8_h2_pp_scalar_plus_chart_cover.json
~~~

The estimator smoke test again verified the interval $4\leq H^{\ast}(f_6)\leq6$, the exact result $H^{\ast}(f_8)=3$, and the public optimal-tail certificate and both budget-skip paths. The optional exact nonlinear-real backend was not installed.

### Next general tasks

1. Add signed-secant automatic split selection, active-vertex generation, chart symmetry, robust exact basis reconstruction, and a complete global cover manifest.

2. Prototype output-normalized atomic boosting with fixed-denominator numerator pricing.

3. Promote the weighted $\tau$ hard-core scheduler after benchmarking its rational spectral constructor.

4. Add degree-one adjustable Gordan policies on mined supports.

5. Benchmark interval quality, certificate size, verification time, and cross-feeding ablations on the exact small archive, parity, equality, symmetric predicates, random tables, $f_6$, and $f_8$.

6. Add active-set cross-feeding so hard vertices from failed upper searches seed signed-secant lower cells.

No current general-methodology result changes the exact separation claims recorded elsewhere in this handoff.

## Remaining tasks in the original separation program

1. Resume and finish the five-bit degree-three exact cover. Require PicoSAT UNSAT, compiled watched-literal UNSAT, and independent Python UNSAT before claiming the five-bit theorem.

2. For the six-bit candidate, pursue an exact simplex-face induction for the full-cube cleared $V_5$ cone. Start by classifying the `237` boundary-only corner cases and `4971` boundary-only edge classes by exact facial reduction.

3. Determine common nonnegative kernels on higher-dimensional denominator-simplex faces. Show that each face either has a strict common multiplier or reduces to one of the classified boundary types.

4. In parallel only if it remains focused, try to cancel the exact six-point residual from the affine weak-dual reduction.

5. If the multiplier route stalls, test the exact augmented alternative $sR+\beta p\geq0$ directly against denominator orientation. A representation-complete quintic invariant search is a later and more expensive fallback.

6. If a six-bit four-head obstruction is completed, combine it with the finished five-bit theorem. This would prove that six bits is minimal. To determine the exact value of $H^{\ast}(f_6)$, separately decide whether five heads suffice.

7. If the six-bit candidate is refuted by an exact four-head construction, preserve that certificate and return to seven-bit candidate search. Do not infer anything from numerical non-discovery alone.

## Claims that are safe now

- The eight-bit Hamming-threshold function is an explicit exact separation with $\deg_{\pm}=2$ and $H^{\ast}=3$.
- Every Boolean function on at most four bits has equality.
- Five-bit equality is exact outside threshold degree $3$.
- The six-bit parity-triple candidate has exact threshold degree $4$.
- The six-bit parity-triple candidate has a verified six-head representation, so $4\leq H^{\ast}(f_6)\leq6$.
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

The original local investigation produced extensive uncommitted work, but the reviewed snapshot was committed and pushed before this handoff refresh. Before any branch switch, rebase, cleanup, or archive operation, confirm the actual cloud checkout state:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

Preserve the active checkpoint and all exact certificate artifacts. In particular, never overwrite `artifacts/calculations/n5_cubic_dictionary_active_checkpoint.json` with a new run unless the new process is invoked with `--resume` and the current SHA-256 has first been recorded.
