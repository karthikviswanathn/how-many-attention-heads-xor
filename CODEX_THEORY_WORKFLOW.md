# Working with Codex on *theory* — discovering lemmas before formalizing

A companion to [`CODEX_WORKFLOW.md`](CODEX_WORKFLOW.md). That file is about turning
a *known* statement into verified Lean. **This** file is about the step before:
using Codex as a mathematical sparring partner to *find* a statement worth proving
— an interesting, general lemma of the form `H*(f) = I(f)` (or `≍ I(f)`) in the
spirit of the symmetric `H* = signChanges` result. Only once a candidate survives
scrutiny do we hand it to the formalization workflow.

> **This file is a living scoreboard, not a fixed recipe.** The division of labor
> between Claude and Codex below is *current best*, inferred from what each has
> actually done well (and badly) on this project — not a law. Every round, revise
> it: when a prompt shape surfaces a good candidate, when one of us catches an
> error the other missed, when a conjecture dies, when a tool interaction fails —
> record it in the [Scoreboard](#scoreboard--changelog) and move the labor to
> whoever did it better. Optimize the *collaboration*, empirically, the same way
> we optimize the proofs. If a section here is contradicted by what just worked,
> change the section.

The two modes are opposite in temperament:

| | formalization (`CODEX_WORKFLOW.md`) | theory (this file) |
|---|---|---|
| question shape | ONE tight obstacle | open-ended "what could be true?" |
| breadth | narrow — broad questions make Codex loop | broad — you *want* several candidates |
| oracle | the Lean build (`CHECK_RC=0`) | small-case brute force + counterexample hunts |
| failure mode | a tactic that doesn't compile | a *conjecture that is false* (far costlier) |
| rounds | few | many — propose → critique → refine |

## Division of labor (current best — revise as you learn)

Assign each task to whoever has empirically done it better. This table is the
heart of "keep it dynamic": when the [Scoreboard](#scoreboard--changelog) shows a
reassignment is warranted, edit this table.

| task | owner (now) | why (evidence) |
|---|---|---|
| Propose candidate invariants `I(f)` | **Codex** | strong recall of the classical complexity zoo (threshold/rational degree, decision lists, Fourier) |
| Recall a relevant theorem / prior art | **Codex** | breadth; but verify the citation, it paraphrases loosely |
| **Numeric checking & brute-force counterexample hunts** | **Claude** | Codex *cannot* run them under a `</dev/null` background consult — closed stdin kills it the instant it execs a checker (observed 2026-06-23). Claude has full Bash + can enumerate `2^(2^n)`. |
| Re-verify each candidate against the known values | **Claude** | Codex over-claims matches; the unit tests are non-negotiable filters |
| **Pin/refute H\* numerically** (the "numeric sandwich") | **Claude** | `deg±` via an LP (proven lower bound) + a model-faithful atom optimizer that *constructs* a ≤K-head sign-rep (upper bound). When the two meet, H\* is pinned; when the optimizer beats a candidate invariant, the equality is **refuted** (see Scoreboard 2026-06-23). Decisive, and Codex can't run it. |
| Independent corroboration of a counterexample | **Codex** | a second, reasoning-only derivation of the same separation raises confidence a lot (it nailed the exact De Morgan-dual counterexample) |
| Proof sketch, both directions | **both** | Codex drafts; Claude checks each step against the actual machinery |
| Identify hardest step / counterexample risk | **both** | round-trip — they flag different risks |
| Final formal proof | hand to `CODEX_WORKFLOW.md` | — |

**Consequence of the brute-force row:** keep theory consults *reasoning-only*. Tell
Codex explicitly *"do not run shell commands; reason from the definitions and the
known values; I will run the numeric checks."* Then the `</dev/null` background
pattern stays safe and Codex never dies mid-investigation trying to compute. The
computation comes back to Claude — which is where it belongs anyway, since Claude
can enumerate all functions on small `n` directly.

## The loop

```
1. State the target shape + ALL known values (the "unit tests" of any conjecture).
2. Codex (exploratory, REASONING-ONLY consult): propose 3–6 candidate invariants
   I(f); for each, define precisely and CHECK against every known value — by
   reasoning, NOT by running code (it can't, under </dev/null).
3. Claude verifies Codex's checks by BRUTE FORCE — it WILL mis-assert (claim a
   match that fails a test case). The known values are non-negotiable filters.
4. Adversarial counterexample hunt (Claude scripts it; Codex suggests where to
   look): try to BREAK each surviving candidate on small n. A false conjecture
   sunk into Lean wastes the whole formalization.
5. For the survivor: round-trip a proof sketch (both directions) with Codex,
   identify the hardest step and the counterexample risk.
6. Only then: hand the statement + sketch to CODEX_WORKFLOW.md and formalize.
7. Append what happened to the Scoreboard — what worked, what died, any labor
   reassignment.
```

## The unit tests (this project)

Every candidate `I(f)` must reproduce the already-proven values, or it's dead:

- `f` constant ⟹ `0`
- `f` a nonconstant linear threshold function ⟹ `1`
- internal exact-count `EXACT_{n,k}` ⟹ `2`
- symmetric `f = F(|x|)` ⟹ `#sign-changes of F` along `0..n`
- parity ⟹ `n`
- and the proven sandwich `deg±(f) ≤ H*(f) ≤ 2ⁿ−1` must hold.

Also exploit the *exact* model-native invariant we already have: `H*(f) = L_frac(f)`
(least number of one-head linear-fractional atoms). A good "classical" `I(f)`
is really a clean handle on `L_frac` — so candidates phrased as rational
sign-representation complexity, #poles, or 1-D sign structure are natural.

## What Codex is good / bad at here

- **Good:** generating candidate invariants, recalling the classical complexity
  zoo (threshold degree, rational degree, decision-list length, Fourier
  sparsity), and sketching why a characterization should hold.
- **Bad / verify-everything:** it over-claims that a candidate matches the known
  values — *always re-check each test case yourself*. It is shaky on whether a
  conjecture is actually true (vs. merely plausible); treat every "this works" as
  "this needs a counterexample hunt." Small hand/brute-force checks beat its
  assurances.
- **Cannot:** run a brute-force checker inside a `</dev/null` background consult.
  Don't ask it to "verify on small n by enumerating" — it will try, and die. Ask
  it to reason; Claude enumerates.

## Counterexample hunting

Before formalizing, brute-force the conjecture on small `n` (e.g. `n ≤ 4`,
all `2^(2^n)` functions or a sampled subset) — **Claude runs this**, by script or
hand reasoning. **A false conjecture is the single most expensive mistake** here:
it can swallow a multi-day Lean effort. Spend cheap effort up front to kill bad
conjectures.

## Hand-off

A candidate is ready for `CODEX_WORKFLOW.md` (formalization) when it has: a precise
statement, agreement with every unit test, no counterexample after a real hunt,
and a both-directions proof sketch with the hardest step identified. Then it
becomes a focused Lean task (delegate big pieces, verify via build).

## Scoreboard / changelog

Append-only. One entry per round of real theory work. Record the prompt shape that
worked, the conjecture's fate, and any labor reassignment — so the next round
starts smarter and the [division of labor](#division-of-labor-current-best--revise-as-you-learn)
above stays evidence-based.

- **2026-06-23 — template established.** The symmetric `H*(f) = signChanges(F)`
  result is the shape to generalize: `H* = (a 1-D sign-change count along a
  linear form's image)`.
- **2026-06-23 — Codex theory consult died trying to compute.** A `</dev/null`
  background brainstorm asking Codex to "check each candidate against the known
  values" ended at *"Shell cwd was reset"* — it tried to exec a checker and the
  closed stdin killed it before producing any candidates. **Fix / lesson:** make
  theory consults *reasoning-only* and move all numeric checking to Claude (see
  the brute-force row in the division-of-labor table). This is the first concrete
  "what works best among the both of you" reassignment.
- **2026-06-23 — leading candidate (Claude, pre-Codex).** For `f = F(L(x))` with
  `L = ∑ λᵢ xᵢ`, `λᵢ > 0`: `H*(f) ≤ signChanges(F over the sorted image of L)`,
  tightening L9's `M−1`; exact when `f` is symmetric (`L = |x|`). Caveat already
  found by hand: naive "`H* = signChanges` of *any* `L`" is **false** — an
  injective `L` gives `2ⁿ−1` for parity but `H*(parity) = n`, so the invariant
  must *minimize* the sign-change count over valid linear forms `L`. **→ refined,
  then refuted as an equality below.**
- **2026-06-23 — candidate sharpened: positive → SIGNED weights (Claude brute force).**
  Unit-testing `S(f) = min over forms L of signChanges(f over Im(L))`: the
  *positive*-weight version FAILS the LTF test (mixed-sign LTF `2x₀−x₁+x₂−1>0`
  has H\*=1 but `S_pos=3`). The **signed** version `S_sgn` (λᵢ∈ℝ) passes every unit
  test: const=0, LTF=1 (incl. mixed sign), EXACT=2, parity=n, symmetric=signChanges,
  and signed weights *never* undercut signChanges on symmetric f (checked to K=14).
  Lesson: unit-test the *exact* form of an invariant — a sign convention can sink it.
- **2026-06-23 — EQUALITY `H*(f) = S_sgn(f)` REFUTED (the costly-mistake catch).**
  Counterexample `f = (x₀∨x₁)∧(x₂∨x₃)` (and its De Morgan dual `(x₀&x₁)∨(x₂&x₃)`,
  Codex's proposal): `deg±=2` and a brute-forced explicit **2-atom certificate**
  (16 margins all ≥ +2.1) give `H*=2`, but `S_sgn=3` (stable to K=14). So a single
  shared linear form is *strictly* suboptimal — two heads exploit two different
  block-forms. **Both lanes agreed**: Claude's atom-optimizer found the 2-head rep;
  Codex independently derived the same separation by a "one near-pole head per
  block" argument. We killed the natural L12-generalization *before* any Lean work —
  exactly the workflow's purpose. Full n=3 sweep (256 fns): `S_pos≥S_sgn≥deg±`
  always (upper bound consistent), 232/256 pinned, gap only where n≥4 blocks exist.
- **2026-06-23 — what SURVIVES as a theorem.** `H*(f) ≤ S(f)` holds as an UPPER
  bound (Codex gave a clean partial-fraction construction for positive forms;
  generalizes BOTH L9's `M−1` and L12's symmetric equality). The matching lower
  bound / exact classical invariant is **open** — equality holds for symmetric f
  (L12) but not in general. Codex's pointer for the exact direction: a
  "positive-denominator factored polynomial-threshold" obstruction refining `deg±`.
- **2026-06-23 — exact head normal form pinned down (Claude algebra + Codex).**
  Since `x_i∈{0,1}`, `a^{x_i}=1+(a−1)x_i`, so each head is EXACTLY
  `φ_h(x)=A_h(x)/D_h(x)` with `A_h` an *arbitrary* affine form and
  `D_h=β_h+s_h(u_h·x)` a *positive one-signed* affine form (`u_i≥0`, `D_h>0` on the
  cube). Thus `H*(f)` = least `H` with `f` sign-rep'd by `c+Σ A_h/D_h` — a
  "positive-pole affine rational threshold degree" (`R₊`). Clearing denominators:
  `H` heads ⟹ a degree-`≤H` PTF of the special factored form
  `P=c∏D_h+Σ_h A_h∏_{k≠h}D_k`. (This IS `H*=L_frac` re-derived cleanly; no known
  classical name — exact classical characterization stays open.)
- **2026-06-23 — `H*(f) = deg±(f)` is FALSE (Codex counting proof) — the real
  shape of the open problem.** Mined data: `H*=deg±` for ALL 20 curated n=4
  functions (and the n=3 structure) — `deg±` is the sharp quantity, which is WHY
  the single-form `S` was loose (e.g. IP2: `deg±=H*=2`, `S=4`). BUT equality can't
  hold for large `n`: the `H`-head model has `O(Hn)` params ⟹ ≤ `2^{O(Hn²)}`
  functions with `H*≤H` (Warren), while degree-2 PTFs number `2^{Θ(n³)}`. So most
  `deg±=2` functions have `H*>2`; the n≤4 tightness is a small-`n` artifact.
  The threshold-degree lower bound is provably NOT tight — a genuine answer to
  core-question #4. **Candidate smallest EXPLICIT separation:** `f_k=⋀_{j}(x_{2j-1}∨x_{2j})`
  (intersection of `k` 2-ORs): Codex proved `deg±(f_k)=2` (k≥2) and `2≤H*(f_k)≤k`;
  so `f_3` (n=6) has `deg±=2, H*∈{2,3}`. Resolving `H*(f_3)` (numeric run + the
  hard "rule out a 2-pole certificate" lower bound) is the live frontier task.
- **2026-06-23 — `f_3` is NOT a separation (numeric verdict).** Two heads compute
  `AND of 3 disjoint ORs` (K=2 found, margin +1.17; K=1 fails robustly at 600
  restarts), and likewise its dual `OR of 3 ANDs`. So `H*(f_3)=2=deg±` — the
  "one positive-pole head per block" intuition is **wrong** (2 heads cover 3
  blocks). Intersections of disjoint 2-ORs collapse to `H*=2` for all tested `k`;
  they are not a separating family. **Lesson:** the counting argument *guarantees*
  separations exist at larger `n` but gives no explicit witness, and the natural
  small candidates keep being tight — explicit `H*>deg±` witnesses are genuinely
  hard (the usual counting-vs-explicit gap). Next frontier options: (a) hunt
  separations on n=5–6 by robust K=deg± search failure; (b) the rank lower bound
  on the cleared quadratic; (c) bank the provable `H*≤S` generalization instead.
- **2026-06-23 — restricted-class hunt: partition-symmetric `H*=δ(G)` ALSO refuted
  (the disk / NAE₃∧NAE₃).** Chasing a clean L12-style equality on a *small* class
  (partition-symmetric `f=G(|x_{B_1}|,…)`, where counting can't force separation):
  Codex proved the lower bound `deg±(f)=δ(G)` (bivariate grid threshold degree) but
  warned the upper bound `H*≤δ(G)` is NOT automatic — 1D partial fractions (single
  poles) realize any degree-`d` univariate poly, but 2D needs mixed `1/(ΛᵢΛⱼ)` poles
  a single-pole head lacks. Stress test on the (3,3) grid (n=6) confirmed it:
  **`f = NAE₃(x_A) ∧ NAE₃(x_B)` has `deg±=2` but `H*=3`** (K=2 fails ~thousands of
  restarts, K=3 succeeds). Structural reason (clean!): the degree-2 separator is an
  **irreducible conic** (`disk`, quad part `s²+t²`, positive-definite, no real linear
  factors), whereas heads build separators from *products/sums of affine poles* — so
  the **saddle** `MAJ₃⊕MAJ₃` (quad part `(s−c)(t−c)`, factors into 2 lines) is tight
  `H*=2`, but the disk needs 3. So the L12 equality is special to 1 block / reducible
  separators; it does NOT generalize. **Bonus:** this is an EXPLICIT `deg± < H*`
  witness (complements Codex's nonconstructive counting). Rigorous lower bound in
  progress: a 2-head clear has quadratic part in the ideal `(d₁,d₂)` of its pole
  lines, which can't equal the positive-definite `s²+t²` — the path to a real theorem.
- **2026-06-24 — disk entry CORRECTED (false negative); `δ=2 ⟹ H*=2` is
  PARTIAL, not unconditional (a pedantry catch).** The bullet above claiming
  `H*(disk)=3` was an **optimizer false negative**: `disk = ¬antidisk`, the
  antidisk's conic is realized at K=2, and by negation symmetry
  `H*(disk)=H*(antidisk)=2`. The K=2 "failure" was the heuristic searcher missing
  a real certificate. **Load-bearing lesson:** a searcher *failure* (CAND) is NOT
  evidence of `H*>δ`; only searcher *successes* (explicit certificates) and `deg±`
  lower bounds are trustworthy. **δ=2 case, stated correctly:** (a) if the conic
  separator `q(s,t)` has a real zero **off** the grid rectangle reachable by
  cube-positive lines (reducible "saddle", or a hyperbola/parabola/ellipse
  crossing outside), then `P = B1·D1 + B2·D2` (two positive lines through that
  zero) ⟹ explicit 2-head rep, `H*=2`. (b) BUT if `q`'s real zero set lies
  **entirely inside** the grid rectangle — the *interior disk*, e.g. the point
  function `G(1,1)=1` = `(x0⊕x1)∧(x2⊕x3)` on (2,2) — NO cube-positive line passes
  through a zero, the elementary construction FAILS, and `H*=2` (seen numerically
  on (2,2)) already requires the **Boolean-quotient freedom**, i.e. it is a
  special case of the open problem, not elementary. **So the interior disk on a
  LARGE grid is the leading counterexample candidate to `H*(2-block)=δ`.** Earlier
  "δ=2⟹H*=2 unconditional" was an overstatement.
- **2026-06-24 — Codex unrestricted-heads proof attempt: STRATEGY REFUTED, problem
  re-shaped (session 019ef671, robust auto-resume).** Asked for the upper bound
  `H*(2-block) ≤ δ(G)` via "full-bit freedom dissolves the 2D star obstruction."
  Verdict: that idea is **false**. Exact condition for `d` heads: the homogenized
  cleared numerator `Q~ ∈ J_D = <∏_{j≠i} D~_j>` (the star ideal); in general
  position this means `Q~` vanishes **scheme-theoretically** on every codim-2 flat
  `{D_i=D_j=0}` — far stronger than "flats off the cube." **Killer step:** if the
  separator is the lift of an *irreducible* bivariate `p(S,T)`, then `P~∈J_D`
  forces **all** `D_i ∈ span{1,S,T}` — full-bit heads collapse back to the
  restricted (s,t)-star problem (which counting kills on large grids). So the lift
  ansatz is dead. **But the lemma may still hold** via a *non-symmetric* cleared
  numerator `Q = P + Σ(x_i²−x_i)g_i` (deg `g_i ≤ δ−2`) agreeing in sign on the
  cube while its homogenization escapes the lift — the **"Boolean-quotient
  freedom"** is the real open hard step. **3+ blocks: equality is FALSE** by
  counting (`exp(Θ(m^k))` functions vs `exp(O(m² log m))` representable) ⟹
  `H*>deg±` for almost all `k≥3` block functions; `k=2` is the genuine borderline
  (the `log m` factor). This *reconciles* with the n=4 numerics: the (2,2)
  successes use non-symmetric `Q`, not the lift.
- **2026-06-24 — 5-agent adversarial verification of the four claims (workflow
  `verify-2block-result`).** Each claim independently re-derived & stress-tested
  (exact linear algebra over F_101, Grassmannian dim counts, an explicit pencil
  counterexample). Verdicts: **Claim B (`Q~∈J_D` star-ideal condition): CONFIRMED
  0.90** — precise hypothesis is *linear general position* (not vague
  "star-general"); `J_D` generated in degree `d−1`, membership tested in degree
  `d`; equivalence to scheme-theoretic vanishing on pairwise flats verified, and
  its necessity confirmed (pencil config: dim 13 < 19). Parity illustration correct
  and does **not** claim `H*(parity)>4`. **Claim C (3-block separation): CONFIRMED
  0.90** — clean Warren/Milnor-Thom count, k=2 borderline numerically confirmed;
  strongest *unconditional* new result. **Claim A (irreducible-lift collapse):
  minor_gap 0.83** — two repairable holes (the "ALL `D_i` collapse" needs every
  pairwise flat **nonempty** — parallel disjoint poles escape; precise hypothesis
  is "`p≠0`, no real linear factor", `δ≥2`). **Critically Claim A does NOT
  lower-bound `H*`** — it only kills the irreducible-lift *ansatz*; a generic
  minimal rep's `Q` need not be a lift. **Claim D (reconciliation): minor_gap
  0.80** — sound, but star-ideal membership is tested on the *homogenization*
  (keeps the non-multilinear cube part), and **a heuristic search miss is NOT a
  certified counterexample** (the disk false-negative, exactly). **Ready to
  formalize now:** `deg±≤H*` (already have it); **`δ=2 ⟹ H*=2`** (clean conic
  sub-lemma — best near-term Lean target); Claim B & Claim C are rigorous but need
  Warren/AG machinery likely absent from mathlib. **NOT ready:** the full
  `H*(2-block)=δ` equality — its upper bound is the open sign-chamber question
  ("every 2-block threshold-degree sign chamber meets a positive star family mod
  the cube relations").
