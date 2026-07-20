# Blueprint — Head Complexity $H^{*}(f)$

> Single source of truth for the research, **reconciled with `lemmas.md`**. The
> foundation (Lemmas 1–12) is proved AND Lean-verified in
> `lemmas/01_foundations_and_normal_form/` + `head-complexity/`. The autonomous
> run adds informal-verified frontier lemmas (L13+), each accepted by the
> Claude-Opus verifier inside `informal_prover_codex.py` ($\boxed{1}$). Those
> nodes are `done`; do not re-prove them. The real work is the remaining FRONTIER.
> Keep this file and `lemmas.md` consistent after every change. See
> `informal_decomposition.md` for the loop; budgets Simple 20 / Medium 35 / Complex 50.

## Progress Summary

> For the full current state see `claude-comments/h_star_knowledge_map.md` (consolidated
> reference) and `RESEARCH_LOG.md` (per-lemma log + the empirical/F4 investigations).

- **Foundation (done, Lean-verified):** 12 / 12.
- **Frontier (done, informal-verified):** 38 — L13 atom dictionary (F1), L16
  cleared-denominator invariant (F2), L14 monotone-term DNF, L15 negation/permutation
  closure, L17 restriction monotonicity, L18 tangential-Chow sandwich, L19 calibrated
  interpolation, L20 sparse threshold density, L21 junta invariance, L22 flattening
  lower bound, L23 Warren counting separation, L24 separation is positivity-free,
  L25 weighted-score sign-change bound, L26 minimized alternation invariant $A_{+}$,
  L27 intersection $H^{*}=2$, L28 full-input-complement closure, L29 flattening for
  $\mathrm{tChow}_{\pm}$, L30 positivity free at level 1, L31 positivity free for symmetric,
  L32 positivity costs only where $H^{*}>\deg_{\pm}$, L33 explicit $\mathrm{INT}_n$ separation,
  L34 explicit unbounded ($\log$) separation, L35 explicit near-linear ($\Omega(n/\log n)$) separation,
  L36 disjoint monotone DNF head complexity is $\widetilde{\Theta}(\text{terms})$,
  L37 shatter-rectangle lower-bound certificate (abstracts L35/L36),
  L38 equal denominators collapse to LTF (head power = attention-pattern diversity),
  L39 $H^{*}(\mathrm{INT}_3)=2$ exactly (beats DNF bound; $n-1$ conjecture at $n=3$),
  L40 GL_2 gauge invariance of order-2 forms (product-sign twist is free; F4 progress),
  L41 sign(AB) has H*<=2 via difference split,
  L42 sign(AB+g), A one-sided, has H*<=2 (order-2 F4 piece),
  L43 indexing IDX_k explicit separation (deg_pm=O(log N), H*=Omega(N/log N)),
  L44 weighted band 1[theta_1<=w.x<=theta_2] has H*=2 (nonsymmetric exact value),
  L45 ORing a disjoint monotone term costs <=1 head (monotone corner detector);
  closes the upper side H*(INT_n)<=n-1 (so n/(8 log n)<=H*(INT_n)<=n-1),
  L46 bitwise equality EQ_n has H*=2 (equality linearizes via distinct subset sums;
  taxonomy: integer-comparison predicates cheap, set-theoretic ones ~Theta(n)),
  L47 any function of an integer comparison G(I(x)-I(y)) has H*<=C(G) and bounded
  sign-rank (the easy-side delineator; counterpart to the L37 lower-bound certificate),
  L48 every output bit of integer addition has H*<=3 (the carry chain is free;
  weighted-score on the low-bit sum),
  L49 the bits of min/max of two integers have H*=2 (comparison-gated bit
  selection; sign(AB+g) with A one-sided, L42),
  L50 the median bit: tChow_pm=3 via an explicit symmetric cubic whose natural
  denominators are intrinsically inadmissible -- the sharpest concrete F4 probe
  (F4-free at 2-bit ints; admissible-form search fails at 3-bit ints, possible gap).
  **Settled qualitatively:** $H^{*}$ is **strictly finer than threshold degree** (L23/L24);
  the **simple L12-style invariant** is $A_{+}$ (min positive-order alternation, exact for
  symmetric, L26); **positivity (F4) is provably free at level 1, for symmetric $f$, and
  wherever $\deg_{\pm}=H^{*}$** (L30/L31/L32) and empirically free everywhere. The
  **explicit separation is now a theorem, and near-linear** (L33/L34/L35): $\mathrm{INT}_n$
  (set intersection) has $\deg_{\pm}=2$ but $H^{*}(\mathrm{INT}_n)=\widetilde\Theta(n)$ — flattening
  gives $\ge\tfrac12\log_2 n$ (L34), and a singleton-column Warren obstruction (L35) pushes it to
  $\Omega(n/\log n)$, positivity-free, nearly matching the nonconstructive counting $\Omega(n)$.
  The first named, non-numerical, *polynomial-rate* witness (supersedes the old numerical
  $\neg\mathrm{DISJ}_4$ candidate, same family).
- **First core question** (exact/approx invariant for $H^{*}$): **partial answer.**
  $H^{*}$ is now pinned between two algebraic invariants,
  $$ \deg_{\pm}(f) \;\le\; \mathrm{tChow}_{\pm}(f) \;\le\; H^{*}(f) = \mathrm{MFdeg}_{\pm}(f) \;\le\; M_{+}(f)-1, $$
  where $\mathrm{MFdeg}_{\pm}$ is the cleared-denominator (tangential) sign-rank with
  attention positivity/monotone constraints (L16), and $\mathrm{tChow}_{\pm}$ is the
  same without those constraints. Symmetric $f$ is solved exactly (L12); monotone $f$
  is sandwiched by $\deg_{\pm}$ and the prime-implicant count (L14, L6).

What the foundation settles: one-head level = linear threshold functions (L11);
exact model-native invariant via the linear-fractional normal form (L10); lower
bound $\deg_{\pm}(f)\le H^{*}(f)$ (L6); upper bound $H^{*}(f)\le M_{+}(f)-1$ (L9);
symmetric exact value $H^{*}(f)=C(F)$ (L12).

What the autonomous run adds: the **atom dictionary** (L13) makes the model's
**monotone bias** precise (each head's denominator is affine, positive, one-sided
slopes); clearing those positive denominators gives the exact polynomial normal
form $H^{*}=\mathrm{MFdeg}_{\pm}$ (L16), a tangent vector at a product of affine
forms; this recovers $\deg_{\pm}\le H^{*}$ and isolates the positivity/monotone
constraints as the entire gap to a standard polynomial-threshold invariant. On the
upper side, the corrected DNF bound (L14, single-polarity terms only) is the first
nonsymmetric family bound; on the lower side, restriction monotonicity (L17) is the
first nonsymmetric lower-bound transfer (planted parity). Closure (L15) canonicalizes.

The remaining gap: whether the positivity/monotone constraints make $H^{*}$
**strictly** exceed $\deg_{\pm}$ / $\mathrm{tChow}_{\pm}$. A Codex direction
brainstorm supplied two lower-bound methods that do NOT factor through $\deg_{\pm}$
(both being verified now): a **flattening / sign-rank** bound
$\mathrm{sr}_{A|B}(f) \le (H^{*}+1)2^{H^{*}}+1$, giving $H^{*} = \Omega(\log\mathrm{sr}(f))$;
and a **Warren counting** bound $\#\lbrace H^{*}\le H\rbrace \le 2^{O(Hn^2)}$, which
against the $2^{\Theta(n^3)}$ degree-2 PTFs forces some $\deg_{\pm}=2$ function to need
$H^{*}=\Omega(n)$. If verified, these answer the first core question's hard half:
$H^{*}$ is **strictly finer** than threshold degree. (The monotone-chain sign-change
lower bound was checked and is FALSE; an LTF with alternating-sign weights has many
chain sign changes but $H^{*}=1$.)

---

# Foundation (proved + Lean-verified — DONE)

| node | statement (short) | proof |
|---|---|---|
| `L1:additive_decomposition` | one-head 2-coord restriction $N,D$ split additively | `lemmas/01_.../001_*` |
| `L2:antipode_identities` | $N(00)+N(11)=N(01)+N(10)$, same for $D$ | `.../002_*` |
| `L3:checkerboard_obstruction` | a 2-bit checkerboard forces $H^{*}\ge 2$ | `.../003_*` |
| `L4:symmetric_thresholds` | $H^{*}(T_{n,t})=1$; AND/OR/MAJ $=1$ | `.../004_*` |
| `L5:family_consequences` | $H^{*}(\mathrm{PARITY}_n)\ge2$, $H^{*}(\mathrm{EXACT}_{n,k})\ge2$ | `.../005_*` |
| `L6:threshold_degree_lower_bound` | $\deg_{\pm}(f)\le H^{*}(f)$ | `.../006_*` |
| `L7:parity_threshold_degree` | $\deg_{\pm}(\mathrm{PARITY}_n)=n$ | `.../007_*` |
| `L8:exact_parity_complexity` | $H^{*}(\mathrm{XOR}_n)=n$ | `.../008_*` |
| `L9:weighted_sum_upper_bound` | $H^{*}(f)\le M_{+}(f)-1$ | `.../009_*` |
| `L10:linear_fractional_normal_form` | $H^{*}(f)=L_{\mathrm{frac}}(f)$ | `.../010_*` |
| `L11:one_head_characterization` | $H^{*}=0$ iff constant; $=1$ iff nonconstant LTF | `.../011_*` |
| `L12:symmetric_sign_changes` | symmetric: $H^{*}(f)=C(F)$ | `.../012_*` |

# Frontier (informal-verified — DONE)

| node | statement (short) | uses | proof |
|---|---|---|---|
| `L13:atom_dictionary` (F1) | one head $\iff$ affine ratio $N/D$, $D>0$ one-sided slopes | L10 | `lemmas/01_.../013_atom_dictionary.md` |
| `L16:cleared_denominator_invariant` (F2) | $H^{*}(f)=\mathrm{MFdeg}_{\pm}(f)$ (tangential poly normal form) | L10, L13 | `lemmas/01_.../016_cleared_denominator_invariant.md` |
| `L14:monotone_term_dnf` (F8a) | single-polarity $s$-term DNF $\Rightarrow H^{*}\le s$ | L10 | `lemmas/02_upper_bounds/014_monotone_term_dnf.md` |
| `L15:negation_permutation_closure` | $H^{*}(1-f)=H^{*}(f)$; permutation-invariant | L10 | `lemmas/04_closure_and_structure/015_*` |
| `L17:restriction_monotonicity` | fixing coords can't increase $H^{*}$; planted $\mathrm{XOR}_m\Rightarrow H^{*}\ge m$ | L10 | `lemmas/03_lower_bounds/017_*` |

---

# Frontier (open — the actual work)

# frontier:tchow_sandwich — DONE (L18)
- **uses**: `[[L16:cleared_denominator_invariant], [L6:threshold_degree_lower_bound]]`
- **status**: `done` | proof `lemmas/01_.../018_tchow_sandwich.md`
- **statement**: $\deg_{\pm}(f)\le\mathrm{tChow}_{\pm}(f)\le H^{*}(f)$, where
  $\mathrm{tChow}_{\pm}$ drops the positivity/one-sided constraints from $\mathrm{MFdeg}_{\pm}$.
  Connects $H^{*}$ to a known-flavored algebraic invariant (tangent to the Chow
  variety of products of linear forms).

# frontier:calibrated_positive_sum_interpolation (F8) — DONE (L19)
- **uses**: `[[L9:weighted_sum_upper_bound], [L13:atom_dictionary]]`
- **status**: `done` | proof `lemmas/02_upper_bounds/019_calibrated_interpolation.md`
- **statement**: For $t(x)=\sum_i\lambda_i x_i$, $\lambda_i>0$, any real table on
  $\mathrm{Im}(t)$ is exactly $a_0+\sum_{j=1}^{M-1}\psi_j$ for one-head atoms $\psi_j$
  (calibrated real feature, via Cauchy-kernel interpolation $1/(\beta_j+t)$). Corollary:
  calibrated decompositions $f=\mathbf 1[\theta+\sum_r a_r G_r(t_r)>0]$ give
  $H^{*}(f)\le\sum_r(|\mathrm{Im}(t_r)|-1)$.

# frontier:sparse_threshold_density (F8b) — DONE (L20)
- **uses**: `[[L14:monotone_term_dnf], [L19:calibrated_positive_sum_interpolation]]`
- **status**: `done` | proof `lemmas/02_upper_bounds/020_sparse_threshold_density.md`
- **statement**: If $f=\mathbf 1[\theta+\sum_{j=1}^s c_j\mathbf 1_{T_j}>0]$ with each
  $T_j$ a single-polarity subcube and a strict margin, then $H^{*}(f)\le s$. Generalizes L14.

# frontier:junta_invariance — DONE (L21)
- **uses**: `[[L17:restriction_monotonicity], [L10:linear_fractional_normal_form]]`
- **status**: `done` | proof `lemmas/04_closure_and_structure/021_junta_invariance.md`
- **statement**: $H^{*}(f)=H^{*}(g)$ when $f$ pads $g$ with irrelevant variables.

# frontier:flattening_lower_bound (F7') — DONE (L22)
- **uses**: `[[L16:cleared_denominator_invariant]]`
- **status**: `done` | proof `lemmas/03_lower_bounds/022_flattening_lower_bound.md`
- **statement**: For any bipartition $A|B$, $\mathrm{sr}_{A|B}(f)\le(H^{*}(f)+1)2^{H^{*}(f)}+1$,
  hence $H^{*}(f)=\Omega(\log\mathrm{sr}_{A|B}(f))$. Proof: affine forms have $A|B$ rank
  $\le 2$; Hadamard submultiplicativity gives the cleared numerator rank $\le(H+1)2^H$;
  a margin shift makes it a strict sign-rank matrix. The first $H^{*}$ lower bound not
  passing through $\deg_{\pm}$ (and it lower-bounds $\mathrm{tChow}_{\pm}$ too).

# frontier:tchow_comparison (F4) — the hard open core (partial: L24)
- **uses**: `[[frontier:tchow_sandwich], [frontier:tchow_separation]]`
- **status**: `partial` | **difficulty**: Complex (research)
- **statement**: Decide whether $H^{*}(f)=\mathrm{tChow}_{\pm}(f)$ (positivity free) or
  strict. **Progress (L24):** the $\deg_{\pm}$-to-$H^{*}$ separation already holds at the
  positivity-free $\mathrm{tChow}_{\pm}$ level (same Warren counting, no admissibility),
  so positivity is NOT the source of the separation from threshold degree. **Still open:**
  whether positivity adds any FURTHER cost, i.e. $\mathrm{tChow}_{\pm}(f) < H^{*}(f)$ for
  some $f$. This needs an $H^{*}$ lower bound exceeding the tChow value; a mixed-slope
  factor cannot be shifted one-sided, but a sign-rep may use entirely different factors
  after tangent reparametrization, so the obstruction is not a simple per-factor argument.
  Likely research-hard. **Recalibrated (lit survey round 3):** the earlier "probably free"
  lean is NOT well-supported — (i) every $H^{*}$ lower bound we have is positivity-free, so
  the empirical "no gap" is nearly vacuous (no tool can witness a gap); (ii) nonnegative /
  PSD / symmetric / border rank gaps (Cohen-Rothblum, Shitov, Fawzi et al.) show positivity
  constraints routinely cost, sometimes unboundedly. **Reduced + tested (5-approach workflow
  + sigma-twist experiments):** all generic positivity-aware mechanisms (boundedness, monotone-
  bias, border-rank, Positivstellensatz, rounding) are DEAD; F4's only surviving residue is
  the product-positivity sign-twist $\sigma=\mathrm{sign}\prod_h D_h$ (admissible forces
  $\sigma\equiv+1$; tChow allows a twist). Constructing $f$ from $\sigma$-twisted order-2 and
  order-3 tChow forms and testing for an admissible same-order form: **every such $f$ ($n=5,6$)
  admits one** (the reliable feasibility direction) — so the $\sigma$-twist costs **nothing at
  $H\le3$**, plus $\mathrm{tChow}_{\pm}=H^{*}$ for $\mathrm{INT}_4$ in the separation regime.
  **Net lean: positivity is most likely FREE** ($H^{*}=\mathrm{tChow}_{\pm}=$ the standard
  tangential-Chow rank); the nonnegative-rank analogy does not transfer at testable orders.
  Open only at $H\ge4$; a rigorous proof still needs the perturbation-to-admissible argument
  (fails through the coupled product). See `claude-comments/h_star_knowledge_map.md` §8.3.

# frontier:weighted_score_and_alternation (A) — partial (L25; L26 in flight)
- **uses**: `[[L10], [L12], [frontier:calibrated_positive_sum_interpolation]]`
- **status**: `partial` | **difficulty**: Medium
- **statement**: A simple, L12-style invariant. (L25) $f=F(t)$ for a positive weighted
  sum $\Rightarrow H^{*}\le C(F)$ (sign changes). (L26) $A_{+}(f)=\min_{w>0}$ (alternations
  of $f$ along the order $t_w$) is a general upper bound $H^{*}(f)\le A_{+}(f)$, EXACT for
  symmetric $f$ ($A_{+}=C(F)=H^{*}$, recovering L12). **Not exact in general** (debated and
  agreed with Codex): a dictator via superincreasing weights has $C(F)=2^n-1$ but $H^{*}=1$;
  $f=\mathbf 1[x_1\ge x_2]$ has $A_{+}=2$ but $H^{*}=1$. The gap is the head's free-numerator
  power (any mixed-sign affine form), which a single monotone score cannot mimic. An exact
  general closed-form remains open.

# frontier:deg_pm_equality_stress_test (F5)
- **uses**: `[[L6], [L11], [L12], [L16], [L17]]`
- **status**: `todo` | **difficulty**: Complex
- **statement**: Decide $H^{*}(f)=\deg_{\pm}(f)$ beyond LTF/symmetric/parity, starting
  with quadratic threshold functions; analyze the $H=2$ cleared-denominator form.

# frontier:counting_separation (F6) — DONE (L23)
- **uses**: `[[L16:cleared_denominator_invariant]]`
- **status**: `done` | proof `lemmas/03_lower_bounds/023_counting_separation.md`
- **statement**: $\#\lbrace f : H^{*}(f)\le H\rbrace \le 2^{O(Hn^2)}$ (Warren over the
  $O(Hn)$ cleared-polynomial parameters with $2^n$ degree-$O(H)$ sign conditions).
  Against the $2^{\Theta(n^3)}$ degree-2 PTFs (Baldi-Vershynin 2019 / Kahn-Saks-Smyth;
  the count $2^{\Theta(n^3)}$ triangulated by the lit survey AND a Codex consult, both
  flagging the $2^{\Theta(n^2)}$ value as the wrong, weight-2-only number), some
  $\deg_{\pm}=2$ function needs $H^{*}=\Omega(n)$. The qualitative answer to the first
  core question: **$H^{*}$ is strictly finer than threshold degree.** Nonconstructive.

# frontier:lower_bound_certificates (F7) — explicit near-linear separation DONE (L35)
- **uses**: `[[frontier:flattening_lower_bound], [frontier:counting_separation]]`
- **status**: `near-linear explicit separation done; close the log gap to get Theta(n)` | **difficulty**: Complex (research)
- **statement**: Beyond the flattening (sign-rank) and counting bounds, further
  checkable obstructions to $H^{*}(f)\le H$. **Resolved (L33/L34/L35):** $\mathrm{INT}_n$
  ($\deg_{\pm}=2$) needs $H^{*}=\widetilde\Theta(n)$ heads. Flattening alone is capped at
  $\Omega(\log N)$ on constant-degree functions ($\mathrm{sr}\le\binom{N}{\le d}=\mathrm{poly}$),
  but a **new non-flattening obstruction (L35)** — restrict to a structured slice
  (singleton columns) where the row acts through only $O(H)$ parameters yet must shatter
  many columns, then apply Warren — gives $H^{*}(\mathrm{INT}_n)\ge\Omega(n/\log n)$,
  positivity-free, the first explicit polynomial-rate separation. This is essentially the
  counting separation (L23) *localized* to a named function. **Remaining open:** close the
  $\log n$ gap (is $H^{*}(\mathrm{INT}_n)=\Theta(n)$?) via the additive subset-sum structure
  of the slice parameters $(\alpha_{h,S},\beta_{h,S})$; and abstract L35 into a reusable
  "slice-shattering" certificate for general OR-of-disjoint-terms families.

# frontier:concrete_nonsymmetric_family
- **uses**: `[[L14], [L17], [frontier:calibrated_positive_sum_interpolation]]`
- **status**: `todo` | **difficulty**: Medium
- **statement**: Pin $H^{*}$ exactly (or up to constants) for a clean nonsymmetric
  family where the L14/L17/F8 machinery gives matching upper and lower bounds, e.g.
  monotone read-once / AND-OR trees, tribes, or small explicit functions. Avoid
  mixed-literal address/indexing (terms are not single-polarity; not covered by L14).

# open:first_core_question (F9)
- **uses**: `[[L16], [L18], [frontier:flattening_lower_bound], [frontier:counting_separation], [L12]]`
- **status**: `qualitative answer settled; exact form open` | **difficulty**: Complex (research)
- **statement**: **Verified answer.** (i) Exact model-native form: $H^{*}=\mathrm{MFdeg}_{\pm}$
  (L16), the positivity/monotone-restricted tangential-Chow rank, sandwiched as
  $\deg_{\pm}\le\mathrm{tChow}_{\pm}\le H^{*}=\mathrm{MFdeg}_{\pm}\le M_{+}-1$ (L18, L9).
  (ii) Relation to a classical invariant: $H^{*}$ is **strictly finer than threshold
  degree** — verified two ways: flattening $H^{*}(f)=\Omega(\log\mathrm{sr}_{A|B}(f))$
  (L22), and Warren counting giving a $\deg_{\pm}=2$, $H^{*}=\Omega(n)$ separation (L23).
  No bound $H^{*}\le g(\deg_{\pm})$ exists. (iii) Symmetric $f$ solved exactly $=C(F)$ (L12).
  So head complexity is a genuinely NEW Boolean-complexity measure, equal to a
  monotone-restricted tangential-Chow sign-rank, not captured by threshold degree.
  (iv) Simple intuitive bound: $H^{*}(f)\le A_{+}(f)$ (min positive-order alternation,
  L26), exact for symmetric, recovering L12 in elementary terms. (v) Positivity is not the
  source of the separation from $\deg_{\pm}$ (L24).
  **Still open (exact characterization):** the exact $\mathrm{tChow}_{\pm}$ vs $H^{*}$
  comparison (whether positivity adds cost, F4); the precise separation magnitude (log vs.
  linear per function); and a closed-form invariant for nonsymmetric $f$. The evidence
  (dictator/mixed-LTF gaps in $A_{+}$; $H^{*}$ a positivity-restricted tangential-Chow rank)
  suggests no simple closed form exists — $H^{*}$ is intrinsically a new measure.

---

## Critical path

`L10 → L13 (F1, done) → L16 (F2, done) → frontier:tchow_sandwich (connect to
algebraic invariant) → frontier:tchow_comparison (F4: is the positivity restriction
free or strict?) → open:first_core_question`. The upper-bound branch
`L9 → frontier:calibrated_positive_sum_interpolation → frontier:concrete_nonsymmetric_family`
runs in parallel and supplies tight cases. Separation/certificate nodes (F6, F7) are
blocked pending a new lower-bound method.

## Pitfalls (carry into every node)

- One head is **not** nonlinear after thresholding (multiply by its positive
  denominator → linear threshold function; this is L11).
- The attention positivity/admissibility constraints ($D_h>0$ on the cube with
  one-sided slopes, L13) are the whole difficulty of the tangential-Chow comparison;
  never silently drop them (dropping yields $\mathrm{tChow}_{\pm}$, possibly strictly
  smaller).
- The corrected DNF bound (L14) needs **single-polarity** terms; mixed-literal terms
  are NOT one head each (the broken old claim). Address/indexing is mixed-literal.
- Lower bounds beyond $\deg_{\pm}$: $\deg_{\pm}$ (L6) and planted parity (L17) both also
  lower-bound $\deg_{\pm}$, so neither separates. The genuinely new tools are the
  flattening / sign-rank bound (L22) and Warren counting (L23) — use these for any
  separation. The monotone-chain sign-change lower bound is FALSE (do not use it).
- Never use vanishing denominators; keep strict positive slack. Do not confuse exact
  feature representation with exact classification; gadgets need only a strict
  classification margin on the finite cube (used in L14, L16, F8).
