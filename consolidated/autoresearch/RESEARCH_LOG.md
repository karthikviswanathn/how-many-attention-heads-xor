# Research Log — Head Complexity $H^{*}(f)$

> Append-only log for the autonomous research run (see the `/goal` prompt). One
> entry per attempted target: what was tried, the outcome **grounded in a verifier
> result or Lean build**, the key idea, and the next target. Never record a result
> as proved without `verification == "correct"` (Claude-Opus verifier) or a clean
> Lean build.

## Starting state (set by setup, before the autonomous run)

- **Proved + Lean-verified stack:** Lemmas 1–12 in `lemmas/01_foundations_and_normal_form/`
  (ledger: `lemmas.md`; Lean: `head-complexity/`). Highlights: exact linear-fractional
  normal form (L10), exact 0/1-head characterization (L11), threshold-degree lower bound
  (L6) + exact parity (L7, L8), weighted-sum upper bound (L9), exact symmetric
  characterization $H^{*}(f)=C(F)$ (L12).
- **Open frontier:** no exact characterization of $H^{*}(f)$ for general (nonsymmetric)
  Boolean functions.
- **Toolkit in place (subscription, no API keys):** `informal_prover_codex.py` (Codex gen +
  Claude-Opus-max verify + refine), `discussion_partner_codex.py` (strategy), `BLUEPRINT.md`
  (reconciled with `lemmas.md`: L1-12 foundation `done`, frontier targets open), `informal_decomposition.md`,
  `informal_solution_template.md`. See `INFORMAL_TOOLKIT.md`.
- **Loop smoke test:** $H^{*}(\mathrm{XOR}_2)=2$ re-proved through the toolkit and verified
  `correct` on attempt 1 (`informal_xor2_solution.md`). Confirms the generate→verify loop works
  on this problem. (This duplicates stack content; it is a pipeline check, not new math.)

## Log

<!-- The autonomous run appends entries below this line. Format:

### <ISO date> — <target label>
- **Target:** <statement>
- **Outcome:** verified | failed | blocked
- **Evidence:** <verification==correct, or Lean build result; cite the file>
- **Key idea:** <one or two sentences>
- **Recorded in:** <lemmas/ file, lemmas.md, BLUEPRINT.md updates>
- **Next:** <next target>
-->

### 2026-06-25 — Re-plan (Codex) of the open frontier
- **Target:** Re-decompose/re-prioritize the frontier given the model's monotone bias (each head's denominator has one-sided slopes).
- **Outcome:** plan updated (not a theorem).
- **Evidence:** Codex re-plan independently confirmed: the general mixed-literal DNF bound is FALSE; the correct version is the single-polarity (monotone-term) DNF bound; F1 atom dictionary and F2 cleared-denominator two-line proof are clean. Added targets: restriction monotonicity, calibrated positive-sum interpolation, tChow containment.
- **Key idea:** A single head's denominator $\gamma + \sum_i \rho_i \alpha^{x_i}$ has slopes $\rho_i(\alpha-1)$, all of one sign; so per-term reciprocal bumps are valid one-head atoms only for single-polarity terms.
- **Recorded in:** `BLUEPRINT.md` (frontier rewrite).
- **Next:** F1, F8a, closure (wave 1); then F2, restriction (wave 2).

### 2026-06-25 — L13 Atom dictionary (F1)
- **Target:** One-head atom $\iff$ affine ratio $N/D$, $D > 0$ on the cube with slopes all of one common sign; converse for strictly one-sided $D$ and arbitrary affine $N$.
- **Outcome:** VERIFIED.
- **Evidence:** `informal_prover_codex.py` returned `verification == "correct"` on attempt 1 (`informal_proofs/results.jsonl`; source `informal_atom_dictionary.md`).
- **Key idea:** Expand $\alpha^{x_i} = 1 + (\alpha-1)x_i$ to read off affine coefficients; realize arbitrary $N$ by $\delta = 0$, $m_i = e_i/(\rho_i(\alpha-1))$, and choose $\alpha$ extreme to keep $\gamma > 0$.
- **Recorded in:** `lemmas/01_foundations_and_normal_form/013_atom_dictionary.md`; `lemmas.md` (L13).
- **Next:** F2 cleared-denominator invariant builds directly on this.

### 2026-06-25 — L14 Monotone-term DNF upper bound (F8a)
- **Target:** $f$ an OR of $s$ single-polarity terms $\Rightarrow H^{*}(f) \leq s$; corollary monotone $f$ bounded by its prime-implicant count.
- **Outcome:** VERIFIED.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_monotone_dnf.md`).
- **Key idea:** Per-term reciprocal subcube bump $b_r = 1/(1 + \lambda v_r)$ with $\varepsilon$-spread strictly one-sided slopes; choose $\lambda = 2s$, $\varepsilon < 1/(2sn)$ to separate satisfied ($> 1/2$) from unsatisfied ($< 1/2$). First exact-flavored nonsymmetric upper bound.
- **Recorded in:** `lemmas/02_upper_bounds/014_monotone_term_dnf.md`; `lemmas.md` (L14).
- **Next:** generalize to calibrated positive-sum interpolation (F8) for additive composition.

### 2026-06-25 — L15 Negation and permutation closure
- **Target:** $H^{*}(1 - f) = H^{*}(f)$ and $H^{*}(f^{\pi}) = H^{*}(f)$.
- **Outcome:** VERIFIED.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_closure.md`).
- **Key idea:** $-\phi$ is an atom (negate numerator params, keep positive denominator); a finite-cube threshold shift $\mu \in (0, s_{\min})$ converts the non-strict $f = 0$ side into a strict one. Permutation reindexes $\rho_i, m_i$.
- **Recorded in:** `lemmas/04_closure_and_structure/015_negation_permutation_closure.md`; `lemmas.md` (L15).
- **Next:** infrastructure for canonicalizing later arguments.

### 2026-06-25 — L17 Restriction monotonicity
- **Target:** $H^{*}(f|_{x_k=c_0}) \leq H^{*}(f)$; iterate for any sub-cube; planted $\mathrm{XOR}_m \Rightarrow H^{*}(f) \geq m$.
- **Outcome:** VERIFIED.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_restriction.md`).
- **Key idea:** Fixing $x_k = c_0$ folds the $k$-th atom terms into the constants $\gamma' = \gamma + \rho_k\alpha^{c_0} > 0$ and $\eta'$, so a restricted atom is again an atom on the smaller cube. First general nonsymmetric lower-bound transfer.
- **Recorded in:** `lemmas/03_lower_bounds/017_restriction_monotonicity.md`; `lemmas.md` (L17).
- **Next:** combine with monotone-DNF (L14) to sandwich nonsymmetric families; await F2.

### 2026-06-25 — L16 Cleared-denominator (tangential) sign-rank (F2)
- **Target:** $H^{*}(f) = \mathrm{MFdeg}_{\pm}(f)$, the least $H$ for which $f$ is sign-represented by $P = \theta\prod_h D_h + \sum_h N_h\prod_{g\neq h}D_g$ with admissible affine pairs $(N_h, D_h)$.
- **Outcome:** VERIFIED (centerpiece of the frontier spine F1 -> F2).
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_cleared_denominator.md`; 22 KB proof).
- **Key idea:** Forward, multiply the atom-sum threshold by $\prod_h D_h > 0$ (sign-faithful). Reverse, divide by $\prod_h D_h > 0$, create a two-sided margin by a threshold shift $\nu = q_+/3$, then perturb zero denominator slopes to $\pm\varepsilon$ (strictly admissible) with $\varepsilon$ small relative to the margin; Lemma 2 of the dictionary reads each summand off as a one-head atom. The verified proof also exhibits $P = \frac{d}{dt}\big|_{0}(1+t\theta)\prod_h(D_h + tN_h)$, making the tangent-to-Chow-variety interpretation precise.
- **Recorded in:** `lemmas/01_foundations_and_normal_form/016_cleared_denominator_invariant.md`; `lemmas.md` (L16); `BLUEPRINT.md` (F1, F2 done).
- **Next:** tChow containment (drop positivity/one-sided constraints) -> connect to a known algebraic invariant; calibrated positive-sum interpolation (F8); then the deg_pm equality/separation question.

### 2026-06-25 — L18 Tangential-Chow sandwich
- **Target:** $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$, where $\mathrm{tChow}_{\pm}$ drops positivity/one-sided constraints from $\mathrm{MFdeg}_{\pm}$.
- **Outcome:** VERIFIED.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_tchow_sandwich.md`).
- **Key idea:** Left: the tChow polynomial has degree $\leq H$, so it witnesses $\deg_{\pm} \leq \mathrm{tChow}_{\pm}$. Right: clearing positive denominators of an $H$-head model gives a tChow witness (special case of arbitrary affine factors), so $\mathrm{tChow}_{\pm} \leq H^{*}$. The positivity/one-sided-slope constraints are the entire gap.
- **Recorded in:** `lemmas/01_foundations_and_normal_form/018_tchow_sandwich.md`; `lemmas.md` (L18); `BLUEPRINT.md`.
- **Next:** the hard open core (F4) is whether this gap is strict; assessed BLOCKED (mixed-slope factors can't be perturbed one-sided; strictness needs an $H^{*}$ lower bound beyond $\deg_{\pm}$).

### 2026-06-25 — L19 Calibrated positive-weighted-sum interpolation (F8)
- **Target:** Any real table on $\mathrm{Im}(t)$ ($t$ a positive weighted sum, $M$ values) equals a constant plus $M-1$ one-head atoms; corollary $H^{*}(f) \leq \sum_r(|\mathrm{Im}(t_r)|-1)$ for calibrated decompositions.
- **Outcome:** VERIFIED.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_calibrated_interpolation.md`).
- **Key idea:** Kernels $1/(\beta_j + t)$ are one-head atoms (positive-slope denominator); the $M \times M$ "ones + Cauchy" interpolation matrix is invertible by a rational-function degree argument (a degree-$\leq M-1$ numerator with $M$ roots is zero). Upgrades L9 from sign to exact real representation, enabling additive composition.
- **Recorded in:** `lemmas/02_upper_bounds/019_calibrated_interpolation.md`; `lemmas.md` (L19); `BLUEPRINT.md`.
- **Next:** sparse single-polarity threshold-density bound (L20) as a corollary; concrete nonsymmetric family.

### 2026-06-25 — L20 Sparse single-polarity threshold-density upper bound
- **Target:** $f = \mathbf 1[\theta + \sum_{j=1}^s c_j \mathbf 1_{T_j} > 0]$, $T_j$ single-polarity subcubes, strict margin $\Rightarrow H^{*}(f) \leq s$.
- **Outcome:** VERIFIED.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_sparse_threshold_density.md`).
- **Key idea:** Replace each indicator by a one-head reciprocal bump $b_j$ with $\varepsilon$-spread strict slopes; $b_j \to \mathbf 1_{T_j}$ uniformly ($\varepsilon = \lambda^{-2}$, $\lambda \to \infty$); finite-cube margin $\mu = \min|\Sigma| > 0$ absorbs the total error. Generalizes L14 to real coefficients.
- **Recorded in:** `lemmas/02_upper_bounds/020_sparse_threshold_density.md`; `lemmas.md` (L20); `BLUEPRINT.md`.
- **Next:** lower-bound frontier (see brainstorm below).

### 2026-06-25 — L21 Junta invariance
- **Target:** $f(x) = g(x_1,\dots,x_k) \Rightarrow H^{*}(f) = H^{*}(g)$.
- **Outcome:** VERIFIED.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_junta_invariance.md`). The prover corrected a minor spec imprecision (the $\delta \neq 0$ padded-numerator term is $O(\epsilon)$, not zero) and handled it.
- **Key idea:** Lower bound by restricting padded coords to $0$ (L17); upper bound by padding each atom with $\varepsilon$-weight irrelevant coords, uniform convergence + margin.
- **Recorded in:** `lemmas/04_closure_and_structure/021_junta_invariance.md`; `lemmas.md` (L21).

### 2026-06-25 — Direction brainstorm (Codex): lower-bound frontier UNBLOCKED
- **Target:** Challenge my assessment that the $H^{*}$ lower-bound frontier (separation from $\deg_{\pm}$) is blocked.
- **Outcome:** plan correction (not a theorem). Two verifiable lower-bound routes that do NOT factor through $\deg_{\pm}$, both surfaced by Codex:
  1. **Flattening / sign-rank:** a product of $H$ affine forms has $A|B$-matrix rank $\leq 2^H$ (Hadamard submultiplicativity); the cleared numerator has rank $\leq (H+1)2^H$, so $\mathrm{sr}_{A|B}(f) \leq (H^{*}+1)2^{H^{*}} + 1$, i.e. $H^{*} = \Omega(\log \mathrm{sr}(f))$. Explicit, self-contained.
  2. **Warren counting:** $H$-head functions number $\leq 2^{O(Hn^2)}$ (Warren over $O(Hn)$ parameters, $2^n$ degree-$O(H)$ sign conditions); against $2^{\Theta(n^3)}$ degree-2 PTFs this forces some $\deg_{\pm}=2$ function to have $H^{*} = \Omega(n)$, a separation.
- **Evidence:** brainstorm reasoning only; both being run through the verifier now (`informal_flattening_lower_bound.md`, `informal_counting_separation.md`). Codex also independently confirmed the monotone-chain sign-change lower bound is FALSE (LTF with alternating weights), matching my own counterexample.
- **Recorded in:** `BLUEPRINT.md` (F6/F7 reopened as flattening + counting nodes); `RESEARCH_LOG.md`.
- **Next:** verify flattening (L22) and counting separation (L23); if both pass, the first core question gains a definitive "strictly finer than $\deg_{\pm}$" answer.

### 2026-06-25 — L22 Flattening (sign-rank) lower bound
- **Target:** $\mathrm{sr}_{A|B}(f) \leq (H^{*}+1)2^{H^{*}}+1$, hence $H^{*}(f) = \Omega(\log \mathrm{sr}_{A|B}(f))$.
- **Outcome:** VERIFIED. The first $H^{*}$ lower bound that does NOT factor through threshold degree.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_flattening_lower_bound.md`).
- **Key idea:** Clear denominators (L16) to a degree-bounded $P$ sign-representing $f$; an affine form has cut-matrix rank $\leq 2$; Hadamard rank submultiplicativity gives $\mathrm{rank}(M_{\prod D_h}) \leq 2^H$ and $\mathrm{rank}(M_P) \leq (H+1)2^H$; a margin shift by $\nu J$ makes a strict sign-rank matrix (rank $+1$). Does not use positivity, so it also lower-bounds $\mathrm{tChow}_{\pm}$. Separates $H^{*}$ from $\deg_{\pm}$ on any function with sign-rank super-polynomial in the threshold-degree monomial count.
- **Recorded in:** `lemmas/03_lower_bounds/022_flattening_lower_bound.md`; `lemmas.md` (L22); `BLUEPRINT.md` (F7' done, first core question answer emerging).
- **Next:** Warren counting separation (L23, in flight) for the stronger $\deg_{\pm}=2$, $H^{*}=\Omega(n)$ form.

### 2026-06-25 — L23 Counting separation from threshold degree
- **Target:** (a) $\#\lbrace f : H^{*}(f) \leq H\rbrace \leq 2^{O(Hn^2)}$; (b) for large $n$, some $f$ has $\deg_{\pm}(f)=2$ and $H^{*}(f)=\Omega(n)$.
- **Outcome:** VERIFIED (reduction), with both external inputs source-confirmed. Settles the qualitative first core question: $H^{*}$ is strictly finer than $\deg_{\pm}$.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_counting_separation.md`). The verifier checks the *reduction* given two external theorems; both are real: Warren 1968 (verified verbatim by the lit-survey agent against the AMS source) and the degree-2 PTF count $2^{\Theta(n^3)}$ (Baldi-Vershynin 2019, arXiv:1803.10868 Thm 1.1/Cor 1.2, $\log_2 T(n,2)=(1-o(1))n^3/6$; independently triangulated by a Codex consult citing Kahn-Saks-Smyth).
- **Audit note:** the lit survey's *intro* mis-stated the degree-2 count as $2^{\Theta(n^2)}$ (the LTF/weight-2 number); its own verified section 4.4 and the Codex consult both correct this to $2^{\Theta(n^3)}$, which is what the proof uses. The survey's $H$-head bound "$2^{O(Hn\log n)}$" is also a slip (correct is $2^{O(Hn^2)}$, used here), which only makes the honest separation $\Omega(n)$ rather than the survey's over-strong $\Omega(n^2/\log n)$.
- **Key idea:** Cleared form (L16) makes an $H$-head function a sign pattern of $2^n$ degree-$O(H)$ polynomials in $O(Hn)$ parameters; Warren bounds the realizable functions by $2^{O(Hn^2)}$; richness of degree-2 PTFs forces $H=\Omega(n)$.
- **Recorded in:** `lemmas/03_lower_bounds/023_counting_separation.md`; `lemmas.md` (L23); `BLUEPRINT.md` (F6 done, first core question qualitative answer settled); `claude-comments/lit_survey_round1.md`.
- **Next:** exact $\mathrm{tChow}_{\pm}$ vs $H^{*}$ (F4); tighten the per-function separation; a closed-form nonsymmetric invariant.

---

## Session summary (2026-06-25 autonomous run)

**Newly proved this run (11 frontier lemmas, each accepted by the Claude-Opus verifier with `verification == "correct"`; source specs `informal_*.md`, proofs in `lemmas/`):**

| # | result | evidence |
|---|---|---|
| L13 | atom dictionary: one head $\iff$ affine ratio $N/D$, $D>0$ on cube with one-sided slopes (the monotone bias) | `013_atom_dictionary.md` |
| L14 | monotone-term DNF: single-polarity $s$-term DNF $\Rightarrow H^{*}\le s$ | `014_monotone_term_dnf.md` |
| L15 | $H^{*}$ invariant under output negation and input permutation | `015_negation_permutation_closure.md` |
| L16 | $H^{*}(f)=\mathrm{MFdeg}_{\pm}(f)$, the cleared-denominator (tangential-Chow) sign-rank | `016_cleared_denominator_invariant.md` |
| L17 | restriction monotonicity; planted $\mathrm{XOR}_m \Rightarrow H^{*}\ge m$ | `017_restriction_monotonicity.md` |
| L18 | sandwich $\deg_{\pm}\le\mathrm{tChow}_{\pm}\le H^{*}$ | `018_tchow_sandwich.md` |
| L19 | calibrated positive-weighted-sum interpolation; additive composition | `019_calibrated_interpolation.md` |
| L20 | sparse single-polarity threshold density $\Rightarrow H^{*}\le s$ | `020_sparse_threshold_density.md` |
| L21 | junta invariance: $H^{*}$ ignores irrelevant variables | `021_junta_invariance.md` |
| L22 | flattening: $H^{*}(f)=\Omega(\log \mathrm{sr}_{A|B}(f))$, first lower bound independent of $\deg_{\pm}$ | `022_flattening_lower_bound.md` |
| L23 | counting separation: some $\deg_{\pm}=2$ function has $H^{*}=\Omega(n)$ | `023_counting_separation.md` |

**Answer to the first core question (verified, partial):**

1. **Exact model-native invariant.** $H^{*}(f) = \mathrm{MFdeg}_{\pm}(f)$ (L16): the least degree of a sign-representing polynomial that is a tangent vector, at a product of $H$ positive one-sided-slope affine forms, to the variety of products of affine forms. Equivalently $H^{*}$ is a positivity/monotone-restricted tangential-Chow sign-rank.
2. **Sandwich with classical invariants.** $\deg_{\pm}(f) \le \mathrm{tChow}_{\pm}(f) \le H^{*}(f) = \mathrm{MFdeg}_{\pm}(f) \le M_{+}(f)-1$ (L6, L18, L9).
3. **Comparison to threshold degree: strictly finer.** $H^{*}$ is not bounded by any function of $\deg_{\pm}$: there are $\deg_{\pm}=2$ functions with $H^{*}=\Omega(n)$ (L23, counting), and $H^{*}=\Omega(\log\mathrm{sr})$ in general (L22, flattening). So head complexity is a genuinely new Boolean-complexity measure.
4. **Symmetric functions, exact.** $H^{*}(f)=C(F)$ (L12, prior).
5. **Upper-bound toolkit (nonsymmetric).** monotone-term DNF (L14), sparse single-polarity threshold density (L20), calibrated positive-sum composition (L19), weighted-sum image (L9).
6. **Structure.** closure under negation/permutation (L15), junta invariance (L21), restriction monotonicity (L17).

**What is still open:**
- An **exact closed-form** characterization of $H^{*}(f)$ for general nonsymmetric $f$ (a clean invariant strictly between $\deg_{\pm}$ and $M_{+}-1$).
- The exact comparison $\mathrm{tChow}_{\pm}$ vs $H^{*}$ (F4): does dropping the positivity/one-sided-slope constraints change the value? The literature has **no flattening/rank obstruction for the Chow rank or the tangential variety $\tau(\mathrm{Ch}_H)$ at $H\ge 2$** (lit survey, verified gap), so this is genuinely open research, not overnight-verifiable.
- Tightening the separation (per-function $\Omega(\log n)$ flattening vs. nonconstructive $\Omega(n)$ counting); an explicit $\deg_{\pm}=2$, $H^{*}=\Omega(n)$ family.

**Best next targets (for a future run):**
1. Build a Chow-rank / tangential-Chow flattening obstruction (lit survey Route B; sandbox = coincident-root loci at $n=1$) for a per-function constructive lower bound.
2. A rational-sign-degree or dual-polynomial invariant sensitive to the *number of one-sided positive denominators*, to attack F4 (does positivity cost extra heads?).
3. An exact $H^{*}$ for one concrete nonsymmetric family with matching bounds (the upper-bound toolkit is strong; the gap is a matching lower bound beyond planted parity).

**Method note:** All results were produced via `informal_prover_codex.py` (Codex `xhigh` generate/refine + Claude-Opus-`max` verify), driven by Codex re-planning / direction brainstorms and a background literature-survey agent (`claude-comments/lit_survey_round1.md`). Every "proved" claim above is grounded in a `\boxed{1}` verifier pass from this session; external inputs to L23 (Warren 1968, Baldi-Vershynin 2019) were triangulated against primary sources.

---

## Continuation (goal: exact closed-form / simple characterization; F4 positivity question)

### 2026-06-25 — L24 Positivity is not the source of the separation
- **Target:** $\#\lbrace f : \mathrm{tChow}_{\pm}(f) \leq H\rbrace \leq 2^{O(Hn^2)}$; hence some $\deg_{\pm}=2$ function has $\mathrm{tChow}_{\pm}=\Omega(n)$, so $H^{*}=\Omega(n)$.
- **Outcome:** VERIFIED. First concrete F4 progress: the $\deg_{\pm}$-to-$H^{*}$ separation already holds at the positivity-free $\mathrm{tChow}_{\pm}$ level, so the attention positivity/one-sided-slope constraints are NOT its cause.
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_tchow_separation.md`). Same Warren counting as L23 but without admissibility (the proof never used $D_h>0$).
- **Recorded in:** `lemmas/03_lower_bounds/024_tchow_separation.md`; `lemmas.md` (L24).
- **Open part of F4:** whether positivity adds any FURTHER cost, i.e. $\mathrm{tChow}_{\pm}(f) < H^{*}(f)$ for some $f$. Likely research-hard (needs an $H^{*}$ lower bound exceeding the tChow value).

### 2026-06-25 — Debate with Codex (per user instruction): converged
- **Point 1 (a lower bound I claimed was flawed):** Codex CONCEDED. The "restrict to a monotone chain, univariate degree $\geq C$" argument for $\deg_{\pm}(F(t)) \geq C(F)$ is invalid (no three distinct cube points are collinear, and a Hamming staircase is not a univariate restriction). Codex strengthened it to a counterexample: with superincreasing weights $t = \sum 2^{i-1}x_i$ and $F(k) = (-1)^k$, $f = (-1)^{x_1}$ is a dictator with $\deg_{\pm} = 1$ but $C(F) = 2^n - 1$. So $H^{*} = C(F)$ does NOT generalize to unequal weights; "factors through one positive weighted sum" is vacuous for generic weights.
- **Point 2 (simple L12-style characterization):** converged that a clean EXACT general characterization is genuinely open; the best simple candidate $A_{+}(f) = \min_{w>0}$ (alternations of $f$ along the order $t_w$) is an UPPER bound, exact for symmetric, not exact in general (my mixed-LTF example $f = \mathbf 1[x_1 \geq x_2]$: $H^{*} = 1 < 2 = A_{+}$, because a head's numerator can be any mixed-sign affine form).

### 2026-06-25 — L25 Sign-change upper bound for one positive weighted sum
- **Target:** $f = F(t)$, $t$ positive weighted sum, $\Rightarrow H^{*}(f) \leq C(F)$.
- **Outcome:** VERIFIED (upper bound; exact only for equal weights, per the debate).
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_weighted_score_upper.md`).
- **Key idea:** Sign-represent $F$ by a degree-$C$ univariate $q(t)$ (roots in the gaps at each sign change); partial-fraction $q(t)/\prod_r(\beta_r + t) = \theta + \sum_r A_r/(\beta_r + t)$ into $C$ Cauchy-kernel atoms; positivity of $\prod(\beta_r + t)$ makes it sign-faithful.
- **Recorded in:** `lemmas/02_upper_bounds/025_weighted_score_upper.md`; `lemmas.md` (L25).
- **Next:** $A_{+}$ invariant (L26): $H^{*} \leq A_{+}$, exact for symmetric.

### 2026-06-25 — L26 Minimized positive-order alternation number (the simple characterization)
- **Target:** $A_{+}(f) = \min_{w>0}$ (alternations of $f$ along the $t_w$-order). Prove $H^{*}(f) \leq A_{+}(f)$, and $A_{+}(f) = C(F) = H^{*}(f)$ for symmetric $f$.
- **Outcome:** VERIFIED. This is the requested L12-style simple characterization: a computable invariant, exact for symmetric functions, generalizing "sign changes along the Hamming axis" to "min alternations along a positive linear ordering."
- **Evidence:** `verification == "correct"` on attempt 1 (`informal_alternation_upper.md`).
- **Key idea:** Upper bound from L25 (generic $w$ makes $f$ a function of $t_w$). Symmetric exactness: the Hamming chain is $t_w$-increasing for every positive $w$, so it is an increasing subsequence with exactly $C(F)$ alternations, forcing $A_w \geq C(F)$; a near-uniform $w$ achieves $C(F)$.
- **Exact corollary (added):** since $\deg_{\pm} \leq H^{*} \leq A_{+}$, all three coincide whenever $\deg_{\pm}(f) = A_{+}(f)$ — the broadest class on which the simple invariant is exact.
- **Negative finding (rigorous):** no linear-order alternation count equals $H^{*}$ in general. Positive-order $A_{+}$ over-counts (free numerator: $\mathbf 1[x_1\ge x_2]$ has $A_{+}=2 > 1 = H^{*}$); signed-order $B = \min_L$ alternations only bounds $\deg_{\pm}$ (its degree-$B$ representer uses inadmissible mixed-slope factors), and $H^{*}$ is strictly finer than $\deg_{\pm}$ (L23). So the exact $H^{*}$ is intrinsically the tangential-Chow rank (L16) — no simpler closed form by alternations.
- **Recorded in:** `lemmas/02_upper_bounds/026_alternation_upper_bound.md`; `lemmas.md` (L26); `BLUEPRINT.md`.

### Bottom line for the "simple characterization" goal
- **Symmetric $f$:** $H^{*}(f) = C(F) = A_{+}(f)$ — simple, exact (L12, L26).
- **General $f$:** $\deg_{\pm}(f) \leq H^{*}(f) \leq A_{+}(f)$, with equality throughout when $\deg_{\pm} = A_{+}$. The simple upper bound is $A_{+}$ (min positive-order alternations).
- **No simple exact closed form exists for general nonsymmetric $f$** (rigorous evidence above): $H^{*}$ is a genuinely new measure, exactly the positivity-restricted tangential-Chow sign-rank (L16), strictly finer than threshold degree (L23, L24).

### 2026-06-25 — Empirical exploration (computational, not proofs)
- **Target:** map $\deg_{\pm}$, $A_{+}$, $H^{*}\le2$ (admissible) and $\mathrm{tChow}_{\pm}\le2$ (arbitrary) for all $f$ on $n\le4$ (up to perm+complement), to locate the first separation / first F4 gap.
- **Outcome (computational evidence; scripts + raw output in `claude-comments/exploration/`, write-up `claude-comments/empirical_findings.md`):**
  - $H^{*}(f) = \deg_{\pm}(f)$ for ALL $f$ on $n\le3$ (40 classes, lower=upper everywhere).
  - Every $\deg_{\pm}=2$ function on $n\le4$ (1619 classes at $n=4$) is realizable with both an admissible and an arbitrary 2-atom form: $H^{*}=\mathrm{tChow}_{\pm}=\deg_{\pm}=2$. So **no separation and no positivity (F4) gap for $n\le4$**.
  - $A_{+}$ over-counts already at small $n$ (17/40 classes at $n=3$).
- **Key inference:** the first $\deg_{\pm}$-vs-$H^{*}$ separation (L23 is asymptotic) and the first $\mathrm{tChow}_{\pm}<H^{*}$ gap (F4), if any, both require $n\ge5$. Small-$n$ search cannot exhibit them; a rigorous resolution needs an oriented-matroid / catalecticant (tangential-Chow rank) argument with the minimal sign-representer pinned down (the genuine open difficulty, per the round-2 lit survey and the Codex lower-bound brainstorm).
- **Reliability:** realizability verdicts are backed by explicitly found + sign-verified representations (reliable); non-realizability would be only suggestive (none occurred).

### 2026-06-25 — L27 exact $H^{*}=2$ for the 2-by-2 intersection
- **Target:** $f = (x_1\wedge x_2)\vee(x_3\wedge x_4)$ has $H^{*}=2$.
- **Outcome:** VERIFIED (concrete nonsymmetric monotone exact value).
- **Evidence:** `verification == "correct"` attempt 1 (`informal_intersection2_exact.md`). Upper L14 (2 terms), lower non-LTF via summing 4 zero-constraints vs 2 one-constraints.
- **Recorded in:** `lemmas/02_upper_bounds/027_intersection2_exact.md`; `lemmas.md` (L27).

### 2026-06-25 — L28 full-input-complement invariance
- **Target:** $H^{*}(f(\mathbf 1 - x)) = H^{*}(f)$.
- **Outcome:** VERIFIED.
- **Evidence:** `verification == "correct"` attempt 1 (`informal_full_complement.md`). $x \mapsto \bar x$ maps an atom to an atom via $\alpha \mapsto 1/\alpha$, $\rho_i \mapsto \rho_i\alpha$ uniformly. (Correction: I initially wrote that single-bit negation is "not free" — that is an overclaim. The monotone bias only breaks the naive same-atom proof; $H^{*}$ is single-bit-negation invariant for $n\le4$ and would be invariant in general iff $\mathrm{tChow}_{\pm}=H^{*}$. So single-bit-negation invariance is OPEN, not false.)
- **Recorded in:** `lemmas/04_closure_and_structure/028_full_complement_invariance.md`; `lemmas.md` (L28).

### 2026-06-25 — $\neg\mathrm{DISJ}_s$: candidate EXPLICIT SEPARATION (corrected; not F4-strict)
- **Target:** test $\neg\mathrm{DISJ}_s = \mathbf 1[\langle u,v\rangle \geq 1]$ (OR of $s$ disjoint 2-ANDs, $n=2s$, $\deg_{\pm}=2$) for a separation and/or an F4 (positivity) gap.
- **METHODOLOGICAL CORRECTION:** my first checks used a margin objective requiring strict separation on BOTH sides, but the model only needs $P>0$ on $f^{-1}(1)$ and $P\leq 0$ (can be $0$) on $f^{-1}(0)$. The corrected LP (max $t$: $P\geq t$ on $f{=}1$, $P\leq 0$ on $f{=}0$, per fixed denominators, hill-climbing the denominators) is reliable; it flipped the earlier muddled conclusion. (The $n\le4$ sweeps are unaffected: there everything was strictly realizable.)
- **Corrected findings (two independent runs agree):** $s=2,3$: clear positive slack for BOTH admissible and arbitrary 2-atoms $\Rightarrow H^{*}=\mathrm{tChow}_{\pm}=2$. $s=4$ ($n=8$) and $s=5$ ($n=10$): slack $\approx 10^{-11}$ (numerically zero) for BOTH admissible AND arbitrary 2-atoms $\Rightarrow$ no strict 2-atom of either kind; an admissible 3-atom exists $\Rightarrow H^{*}=3$.
- **Conclusions (computational, not proven):**
  1. $\neg\mathrm{DISJ}_4$ is a candidate **explicit separation**: $\deg_{\pm}=2$ but $\mathrm{tChow}_{\pm}=H^{*}=3$. The separation comes from the **tangent structure** (the rank-8 quadratic $\sum_r u_rv_r$ is not a 2-tangent form), NOT positivity — consistent with L24. This would be the first *explicit* (not counting-based) separation, at $n=8$.
  2. **F4 (does positivity cost?) found NO witness**: in every computed case $\mathrm{tChow}_{\pm}=H^{*}$. The data leans toward positivity being *free* ($\mathrm{tChow}_{\pm}=H^{*}$), though unproven.
- **Rigorous proof open:** $H^{*}(\neg\mathrm{DISJ}_4)\geq 3$ needs a $\tau(\mathrm{Ch}_2)$ rank obstruction (lit survey round 2, P1: Guan flattening on the CGGHMNS tangent vector); flattening alone gives only $H^{*}\geq 2$ here ($\mathrm{sr}\leq 6 \leq 13=(2{+}1)2^2{+}1$). Scripts in `claude-comments/exploration/`.
- **Caveat:** numerical (slack $\approx 0$ at $s\geq4$ is a boundary, strong but not a proof); explicitly NOT claimed as a theorem. Supersedes the earlier "F4-strict candidate" note, which was an artifact of the too-strict objective.

### 2026-06-25 — F4 (positivity) consolidated: free at level 1 + symmetric; general open
- **Proved:** $\mathrm{tChow}_{\pm} = H^{*}$ at level $\leq 1$ (L30) and for all symmetric $f$ (L31, sandwich collapse since $\deg_{\pm}=H^{*}$ there); flattening (L29) and counting (L24) lower bounds need no positivity. So positivity is free wherever $\deg_{\pm}=H^{*}$.
- **Empirical:** $\mathrm{tChow}_{\pm}=H^{*}$ in EVERY computed case ($n\le4$ exhaustive; $\neg\mathrm{DISJ}_s$ up to $s=5$, including the $\deg_{\pm}=2$/$H^{*}=3$ separation candidate) — strong evidence positivity is free in general.
- **Open at $H\geq 2$:** the level-1 free-numerator trick does not extend. Confirmed (Codex + me): fixing $D_1=D_2$ collapses the tangent form to an affine sign $\mathrm{sign}(\theta D + N_1 + N_2)$ (only LTFs; e.g. XOR$_2=(x_1-x_2)^2$ genuinely needs two different denominators). So a general positivity-free construction needs two distinct admissible denominators realizing the same sign pattern — the open Comon-Lim-Qi / Baldi-Slot Positivstellensatz program (`lit_survey_round2.md` P2).
- **Net:** if $H^{*}=\mathrm{tChow}_{\pm}$ in general (evidence strong), then $H^{*}$ equals the standard unconstrained tangential-Chow rank and the monotone-bias positivity constraints cost nothing — a clean potential characterization, currently open.

### 2026-06-25 — L33: FIRST RIGOROUS EXPLICIT SEPARATION (INT_n / set intersection)
- **Target:** prove a *named*, non-numerical separation $\deg_{\pm}(f) < H^{*}(f)$ — the long-open "explicit separation" problem (the $\neg\mathrm{DISJ}_4$ numerics were never a theorem).
- **Function:** $\mathrm{INT}_n(x,y) = \bigvee_{i=1}^n(x_i\wedge y_i)$ on $2n$ bits (set intersection / NOT-disjointness; $\mathrm{INT}_n = \neg\mathrm{DISJ}_n$, same family as the old candidate).
- **Proof route (combines two existing lemmas with a classical sign-rank bound):**
  1. $\deg_{\pm}(\mathrm{INT}_n)=2$ — upper via $\sum_i x_iy_i-\tfrac12$; lower via a 4-point XOR-pattern obstruction ($A(P_1){+}A(P_4)=A(P_2){+}A(P_3)$ but signs disagree).
  2. $\mathrm{sr}_{x|y}(\mathrm{INT}_n)\ge n$ — self-contained homogeneous-shattering/VC argument: restrict columns to $y=e_i$; rows $x=\mathbf 1_S$ give $\mathrm{INT}(\mathbf 1_S,e_i)=[i\in S]$, realizing all $2^n$ dichotomies of the $n$ points $b_{e_i}\in\mathbb{R}^r$ by through-origin halfspaces, forcing $r\ge n$ (linear-dependence/Radon argument).
  3. Flattening (L22): $n\le\mathrm{sr}_{x|y}\le (H^{*}{+}1)2^{H^{*}}{+}1$. Since $\Phi(2)=13$, $n\ge 14\Rightarrow H^{*}(\mathrm{INT}_n)\ge 3$.
- **Outcome:** VERIFIED. `informal_prover_codex.py` returned `verification == "correct"` on attempt 1 (110-step atomic proof). Independently cross-checked by a 5-lens adversarial workflow (5/5 "sound", 0 fatal/fixable; one reviewer read the actual L22 file to rule out circularity).
- **Result:** $\deg_{\pm}(\mathrm{INT}_{14})=2 < 3 \le H^{*}(\mathrm{INT}_{14})$ on $28$ bits — the **first explicit, rigorously-proved separation**. Positivity-free (L29 gives $\mathrm{tChow}_{\pm}(\mathrm{INT}_{14})\ge 3$ too). Supersedes the numerical $\neg\mathrm{DISJ}_4$ candidate.
- **Recorded in:** `lemmas/03_lower_bounds/033_int_explicit_separation.md`; `lemmas.md` (L33); `claude-comments/h_star_knowledge_map.md` (§8.2 SOLVED).
- **Two structural insights banked:**
  1. **Unbounded explicit gap (L34, next):** $(H{+}1)2^H{+}1\le 4^H$ for $H\ge 2$ gives $H^{*}(\mathrm{INT}_n)\ge\tfrac12\log_2 n\to\infty$ while $\deg_{\pm}=2$.
  2. **Flattening saturates logarithmically:** $\deg_{\pm}=O(1)\Rightarrow\mathrm{sr}\le\binom{N}{\le d}=\mathrm{poly}(N)$, so flattening can never prove more than $H^{*}=\Omega(\log N)$ for a constant-degree function. The nonconstructive counting $\Omega(n)$ (L23/L24) is therefore *necessarily* non-flattening; an explicit $\Omega(n)$ separation needs a genuinely new ($\tau(\mathrm{Ch}_2)$ rank) obstruction.

### 2026-06-25 — L35: EXPLICIT NEAR-LINEAR separation H*(INT_n) >= c n / log n (non-flattening)
- **Origin:** a Codex direction-brainstorm (per the workflow's "consult Codex on research direction" rule). I asked whether H*(INT_n) is Theta(log n) or Theta(n); Codex produced a NEW obstruction proving Omega(n/log n), which I then verified and banked. Credit: Codex (gpt-5.5, xhigh).
- **Result:** H*(INT_n) >= tChow_pm(INT_n) >= n/(8 log2 n) for large n. Since deg_pm(INT_n)=2, this is the FIRST EXPLICIT POLYNOMIAL (near-linear) separation of head complexity from threshold degree, nearly matching the nonconstructive counting Omega(n) of L23/L24. Positivity-free (bounds tChow_pm directly).
- **Technique (new, reusable):** "counting localized by a structured restriction." Fix a sign-representing tangent form P of order H. Restrict to rows x=1_S, singleton columns y=e_j. Then the row enters only through 2H+1 parameters (theta, alpha_{h,S}=a_h+sum_{i in S}p_hi, beta_{h,S}=b_h+sum_{i in S}r_hi), and P(1_S,e_j)=Q_j(w) is degree H+1 in w in R^{2H+1}. Since INT_n(1_S,e_j)=[j in S], the n columns are shattered: all 2^n sign patterns realized. Warren (m=n, p=2H+1, d=H+1) gives 2^n <= (C(H+1)n/(2H+1))^{2H+1}, hence H=Omega(n/log n). Case split on 2H+1<=n (Warren) vs >n (trivial).
- **Why flattening could not do this:** sr_{x|y}(INT_n)=Theta(n) exactly (L34), so the flattening bound H=Omega(log sr) saturates at Theta(log n). The 2^H flattening rank terms are "not free" on the singleton-column slice: there only 2H+1 row parameters move. THIS is the long-flagged "non-flattening obstruction" that L33/L34 said was needed; L35 provides it.
- **Verification (double-gated, as for L33):** informal_prover_codex.py verification==correct (attempt 1, 42-step atomic proof) AND a 5-lens adversarial workflow returned 5/5 sound, 0 fatal/fixable (lenses: Warren application incl. the relax-to-all-w step, restriction algebra, log arithmetic + constants, positivity-freeness + inequality direction, global/circularity + empirical consistency; one lens ran an independent Codex cross-check).
- **Rate pinned:** with H*<=n (DNF, L14), H*(INT_n)=tilde-Theta(n) (between n/(8 log n) and n). Supersedes L34's log bound for INT_n.
- **Recorded in:** lemmas/03_lower_bounds/035_int_nearlinear_lower.md; lemmas.md (L35); BLUEPRINT.md (F7 resolved); claude-comments/h_star_knowledge_map.md (§5, §8.2).
- **Open follow-ups:** (1) close the log gap to Theta(n) via the additive subset-sum structure of (alpha_{h,S},beta_{h,S}); (2) abstract L35 into a general "slice-shattering certificate": OR of s disjoint terms each of size >=2 has H*=Omega(s/log s), a near-tight nonsymmetric-family characterization (matches L14's <=s).

### 2026-06-25 — L36: disjoint monotone DNF head complexity is tilde-Theta(terms)
- **Target/result:** generalize L35. For f = OR of s pairwise-disjoint monotone ANDs each of width >= 2, H*(f) >= tChow_pm(f) >= s/(8 log2 s). With L14 (H* <= s), H*(f) = tilde-Theta(s).
- **Technique:** L35's singleton-column Warren, generalized. In each block pick a pivot pi_r and rest R_r (nonempty since width >= 2). Slice z_{S,j}: rest of block r set to [r in S], pivot of block r set to [r=j]. By disjointness f(z_{S,j}) = T_j = [j in S]. Affine forms become additive in S (alpha_{h,S}=a_h+sum_{r in S} P_{h,r}) plus a per-column pivot constant, so the row acts through 2H+1 parameters; Warren on the s shattered columns gives s <= (2H+1) log2(Cs), H = Omega(s/log s). Width >= 2 essential (else no rest vars to encode S, and OR-of-singletons is an LTF, H*=1); disjointness lets the block sums split.
- **Verified:** informal_prover_codex.py verification==correct (attempt 1); the solution explicitly discharged width>=2 necessity, disjointness, parameter count, Warren's m>=p split, and positivity-freeness. Reuses the L35 core (double-gated), so banked on the prover gate.
- **Significance:** pins an entire NONSYMMETRIC family up to a log factor (after symmetric, L12) by pairing the monotone-DNF upper bound (L14) with a matching lower bound. INT_n is the width-2 case; L27 (two 2-ANDs) the s=2 case. Positivity-free; an explicit poly-rate separation when widths are O(1).
- **Recorded in:** lemmas/03_lower_bounds/036_disjoint_dnf_lower.md; lemmas.md (L36); BLUEPRINT.md.

### 2026-06-25 — L37: shatter-rectangle, the lower-bound technique abstracted into a tool
- **Result:** if g admits a "shatter-rectangle of order s" (coordinate partition [N]=Vrow|Vcol, row assignments rho_S (S subset [s]) and column assignments kappa_j (j in [s]) with g(rho_S,kappa_j)=[j in S]), then H*(g) >= tChow_pm(g) >= s/(8 log2 s).
- **Why it's the right abstraction:** the Warren argument needs ONLY the row/column coordinate partition, not the subset-sum additivity. Any affine form A(rho_S,kappa_j) splits as (Vrow part, depends on S) + (Vcol part, depends on j), so the row collapses to the 2H+1 numbers (theta, alpha_{h,S}, beta_{h,S}); shattering s columns then triggers Warren. Purely combinatorial hypothesis + Warren.
- **Instances:** INT_n (Vrow=x-coords, rho_S=1_S; Vcol=y-coords, kappa_j=e_j) => L35; disjoint monotone DNF (Vrow=rests, Vcol=pivots) => L36.
- **Verified:** informal_prover_codex.py verification==correct (attempt 1). Reuses the L35 core (double-gated); banked on the prover gate.
- **F4 insight recorded (knowledge map §6):** EVERY H* lower bound in the project (deg_pm L6, flattening L22/L29, counting L23/L24, shatter-rectangle L37) is positivity-free, i.e. actually bounds tChow_pm. So no current technique can witness a positivity gap tChow_pm < H*; the gap, if any, is invisible to all known methods. Strong heuristic (not proof) that positivity is free.
- **Recorded in:** lemmas/03_lower_bounds/037_shatter_rectangle_lower.md; lemmas.md (L37); BLUEPRINT.md (24 frontier); claude-comments/h_star_knowledge_map.md (§5, §6).

### 2026-06-25 — Status: the log gap for H*(INT_n) is hard; empirics lean Theta(n)
- **Question:** is H*(INT_n) = Theta(n) or Theta(n/log n)? (We proved Omega(n/log n) (L35) and have <= n (L14).)
- **Empirics (compute_hstar_int.py, per-H):** H*(INT_n) = 2,2,3,4 for n = 2,3,4,5 — grows ~linearly (increments ~every step for n>=3), leaning toward Theta(n), i.e. the DNF upper bound n is near-tight and the log in L35 is loose. (Small-n, not asymptotic; reliable only as a hint.)
- **Codex direction-brainstorm (loggap_q):** the shatter-rectangle bound is the Goldberg-Jerrum VC bound on a (2H+1)-parameter degree-(H+1) family; the log factor is intrinsic to the pure dimension argument. Closing to Omega(n) "would have to use extra structure of the tangent-form polynomials Q_j, or impose quantitative restrictions (bounded coefficients, margin, conditioning)." So Omega(n) is a hard open problem, not a quick win via the additive structure alone.
- **Disposition:** mark the log gap OPEN/hard; do not over-invest the informal-prover loop on it. The proven, banked result H*(INT_n)=Omega(n/log n) (L35) stands as the explicit near-linear separation.

### 2026-06-25 — Lit survey round 3 + F4 recalibration + the H*(INT_n)=n-1 conjecture
- **Lit survey (round 3, claude-comments/lit_survey_round3.md):** targeted the two open problems.
  - **P1 (log gap):** the log factor in the Warren/Goldberg-Jerrum sign-pattern count is PROVABLY necessary for the abstract sign-family (Bartlett-Maiorov-Meir 1998, matching VC lower bound via bit-extraction). So Omega(n/log n) is the CEILING of the shatter-rectangle method; reaching Omega(n) needs a new argument using tangent-form rigidity (shared theta, tied N_h/D_h, same P on all 2^n columns), not just the dictator slice. Sign-rank of the dictator matrix is exactly n but only for D=1 decoders (the log is a degree->=2 effect). H*(INT_n) itself stays open in [Theta(n/log n), Theta(n)].
  - **P2 (F4) RECALIBRATION:** the earlier "positivity probably free" lean is NOT well-supported. Every adjacent setting shows positivity/one-sidedness can strictly (even unboundedly) raise rank/order: nonnegative rank vs rank (Cohen-Rothblum; Shitov unbounded), symmetric tensor rank (Shitov disproves Comon), PSD rank (Fawzi et al.), and especially BORDER rank (dropping exactness lowers rank via a limit -- the mirror of an F4 cost). Combined with the internal fact that all our lower bounds are positivity-free (so "no gap found" is nearly vacuous), F4 is genuinely open with a strict gap PLAUSIBLE. Updated knowledge map §8.3 accordingly.
- **Conjecture H*(INT_n) = n-1 for n>=3:** per-H sweep gives H*(INT_n) = 2,2,3,4 for n=2,3,4,5, and H*(INT_6) >= 5 (H=4 numerically infeasible, slack ~1e-9; H=5 realizability pending). So 2,3,4,5 = n-1 for n=3,4,5,6. This says the truth is LINEAR Theta(n) (L35's log is loose) and the DNF upper bound n is nearly tight (saves exactly one head). Empirical; proving it needs both an (n-1)-atom construction and a near-tight (>= n-1) lower bound, neither known.

### 2026-06-25 — IDX_k (indexing/multiplexer): a second explicit separation via L37
- **Finding:** the indexing function IDX_k (address a in {0,1}^k, memory m in {0,1}^{2^k}, output m_a) admits a shatter-rectangle of order 2^k: V_row=memory (set m_a=[a in S]), V_col=address (kappa_j=binary(j)), so IDX_k(rho_S,kappa_j)=[j in S]. By L37, H*(IDX_k)=Omega(2^k/k)=Omega(N/log N) on N=2^k+k bits.
- **It's a separation:** m_a = sum_b [a=b] m_b is an exact multilinear polynomial of degree k+1, so deg_pm(IDX_k) <= k+1 = O(log N), while H* = Omega(N/log N). Separation holds for k>=7.
- **Significance:** (i) a SECOND explicit near-linear separation, on a canonical complexity-theory function (the index function); (ii) IDX_k's 2^k terms SHARE the k address bits (not disjoint), so it is OUTSIDE L36's disjoint-DNF family -- demonstrating L37 needs only the row/column coordinate partition, not disjointness, and is strictly more general than L36. Recorded as a third instance in L37's consequence + knowledge map §5.

### 2026-06-25 — F4 reduced to a product-positivity sign-twist (5-approach workflow)
- **Method:** a multi-agent workflow developed 5 approaches to a positivity-AWARE H* lower bound (boundedness/fat-shattering, monotone-bias certificate, border-rank/closure witness, Positivstellensatz degree, free-via-rounding) + a synthesis.
- **Result: all 5 mechanisms are DEAD**, each for a precise reason:
  - Boundedness: gauge invariance N_h->lambda N_h rescales magnitude bound B and margin gamma together, so admissibility pins no B/gamma; admissible atoms are NOT uniformly bounded (D_eps=eps+sum x_i gives |phi|=1/eps).
  - Monotone-bias: at H=1, sign(theta + N/D) = sign(theta D + N), an ARBITRARY affine form (free mixed-sign N absorbs the one-signed apex theta D); one atom realizes every LTF, so no chain-alternation/monotonicity count exceeds tChow. (This is also why A_+ over-counts.)
  - Border-rank: finite-cube strict sign-rep is an OPEN condition; if admissible P_t -> P_* sign-repping f, then min|P_*|>0 over 2^N points forces sgn P_t = sgn P_* for small t. Closure adds no Boolean function at fixed order; order-changing limits give only UPPER bounds. Border rank is the wrong object.
  - Positivstellensatz: D affine and >0 at the 2^N vertices IS its own degree-1 certificate; no SOS multiplier degree can blow up. A grazing denominator makes a head MORE powerful (1/eps range), opposite of a cost.
  - Free-via-rounding: fails, but most diagnostic. Tangent forms are NOT additively closed (appending a head MULTIPLIES by D_g), so the leftover from splitting a mixed-slope factor can't be absorbed by extra heads.
- **The single surviving residue (named by 4/5):** the only positivity-specific fact is the GLOBAL product-positivity sigma(x)=sign(prod_h D_h(x)). Admissible forces sigma == +1; arbitrary tChow lets sigma be a nontrivial product-of-H-halfspaces sign-twist. F4 = "does requiring sigma==+1 strictly raise the minimal order?" -- structurally the nonnegative-rank>rank mechanism.
- **Weight leans toward a GAP being plausible** (not free): "no gap found" is nearly vacuous (all our bounds are positivity-free), and the non-additive-closure exhibits the cost mechanism. Proving a gap needs a sigma-twist dimension invariant (hyperplane-cover / nonnegative-rank-style).
- **Recommended concrete step:** an EXACT (not random-sampling) order-2 search in the regime deg_pm < tChow_pm: CONSTRUCT f as the sign of a sigma-twisted order-2 tChow form (so tChow_pm(f)<=2 by construction), then test whether an admissible 2-atom exists; if not, tChow_pm(f)=2 < 3=H*(f) is a gap candidate. Running this next.
- **Recorded in:** knowledge map §8.3 (the sigma-twist reduction).

### 2026-06-25 — F4 sigma-twist test: positivity is FREE at order 2 (reliable)
- **Experiment (workflow's recommended step, f4_sigma_twist.py):** construct f = sign of a sigma-TWISTED order-2 tChow form (D_1 D_2 changes sign on the cube, so tChow_pm(f)<=2 by construction); then test whether f also has an ADMISSIBLE 2-atom (sigma==+1). Control: sigma==+1 forms.
- **Result (n=5 and n=6):** ALL forms admit an admissible 2-atom -- twisted: 40/40 at each n; control: 25/25. ZERO gap candidates.
- **Why this is solid (not slack~0):** finding an admissible 2-atom is the RELIABLE direction (a representation is found and sign-checked). So "every sigma-twisted f also has an admissible order-2 form" is well-supported, unlike infeasibility claims.
- **Conclusion:** the sigma-twist -- identified by the 5-approach workflow as the ONLY surviving source of an F4 gap -- costs NOTHING at order 2. Admissible (sigma==+1) order-2 forms reach every function a sign-twisted order-2 form reaches. So F4 is FREE at orders <=2; any gap must first appear at H>=3.
- **Net F4 status:** free at H<=1 (L30), symmetric (L31), deg_pm=H* (L32), and now the sigma-twist at H<=2; OPEN at H>=3. This tempers the lit-survey "gap plausible" lean with direct targeted evidence -- the one surviving mechanism, tested where it should first bite, does not bite. A gap remains conceivable at H>=3 (nonnegative-rank analogy) but is now less likely.
- **Recorded in:** knowledge map §8.3.

### 2026-06-25 — F4 sigma-twist FREE at order 3 too; lean reverses toward FREE
- **Experiment (f4_sigma_twist3.py):** construct f = sign of a sigma-TWISTED order-3 tChow form (prod_{h=1..3} D_h changes sign), test admissible 3-atom. Control: sigma==+1 order-3 forms.
- **Result (n=5,6):** ALL forms admit an admissible 3-atom -- twisted 30/30 each, control 14/14 (n=5), 10/10 (n=6). ZERO gap candidates. Reliable (feasibility-based).
- **Combined with the order-2 test:** the sigma-twist -- the ONLY surviving F4 gap mechanism (5-approach workflow) -- is FREE at BOTH order 2 and order 3, tested exactly where a gap should first appear.
- **Lean reverses toward FREE.** The lit-survey "gap plausible" came from analogy to nonnegative/PSD/border rank gaps; the DIRECT sigma-twist test shows that analogy does NOT transfer to the tangent-form setting at orders 2-3. Plus the sharp INT test: tChow_pm=H* for INT_3 and INT_4 (the latter in the separation regime deg_pm=2 < 3=H*, non-vacuous). 
- **Updated F4 status:** free at H<=1 (L30), symmetric (L31), deg_pm=H* (L32), and the sigma-twist at H<=3; open only at H>=4, where a gap is now unlikely. Best reading: positivity is MOST LIKELY FREE (H* = tChow_pm = standard tangential-Chow rank). A rigorous proof still needs the perturbation-to-admissible argument (fails through the coupled product); a gap at H>=4 is not excluded.
- **Net session F4 contribution:** reduced F4 to the sigma-twist (theory) and showed the sigma-twist is free at the first two nontrivial orders (targeted reliable experiment) -- far stronger evidence than the earlier blind "no gap in n<=4" (which was forced-free by L32).
- **Recorded in:** knowledge map §8.3.

### 2026-06-25 — F4 order-2: the n=7 "gap" was a SEARCH ARTIFACT; order-2 is FREE (decisive control)
- **A scare and its resolution.** An n=7 hunt with BALANCED sigma-twists (D_1 D_2 < 0 on ~half the cube) flagged several "F4 GAP CANDIDATES" (f from an order-2 tChow form, so tChow_pm<=2, with NO admissible 2-atom found but an admissible 3-atom => apparent tChow_pm=2 < 3=H*).
- **Smoking gun it's an artifact:** the high-effort re-verify computed an ARBITRARY 2-atom check (search the larger non-positive space) and got realizable=FALSE -- but an arbitrary 2-atom EXISTS BY CONSTRUCTION (f is literally the sign of an order-2 tChow form). The search failed to find a 2-atom it is GUARANTEED to exist. So at n=7 (128 points) the random-restart search is unreliable even in the feasibility direction; its "no admissible 2-atom" verdicts are meaningless.
- **DECISIVE control:** balanced sigma-twists at n=5,6 (where the search IS reliable -- it finds admissible forms with clear margins): 0/30 gap candidates at EACH n. Every balanced-twist f also admits an admissible 2-atom.
- **Conclusion:** order-2 F4 is FREE. The n=7 candidates are search-reliability artifacts (the NON-DISJ_4-style false positive, correctly guarded against this time via a reliable control + the by-construction feasibility check).
- **Methodological boundary (important for future work):** the admissible/tChow random-restart feasibility search is reliable only for n<=6 (<=64 points). At n>=7 it fails to find even known-existing forms; do NOT trust "no form found" at n>=7. Use the by-construction arbitrary-form feasibility as a built-in reliability check.
- **Net F4 status (unchanged, strengthened):** positivity is free at H<=1 (L30), symmetric (L31), deg_pm=H* (L32), and the sigma-twist at H<=3 -- now including BALANCED twists at n=5,6. Best reading: positivity is MOST LIKELY FREE (H* = tChow_pm = standard tangential-Chow rank). Open only at H>=4. A rigorous proof still needs the perturbation-to-admissible argument.

### 2026-06-25 — L40: Gauge invariance of order-2 tangent forms (F4 progress, RIGOROUS)
- **Origin:** extracting a Codex consult I had wrongly written off as "died" (it completed with a valuable result), independently rederived by a workflow agent (TWISTED). User flagged dead workflow agents (same-sign, openness-density, API connection-closed); respawned refined.
- **Lemma (L40):** order-2 tangent forms P=D_1 L_1 + D_2 L_2 have a GL_2 gauge freedom: (E_1,E_2)=G(D_1,D_2), (M_1,M_2)=G^{-T}(L_1,L_2) give E_1 M_1 + E_2 M_2 = D_1 L_1 + D_2 L_2 identically (since G^T G^{-T}=I). Hence (a) gauge invariance, (b) product-positivity is FREE (some G makes E_1 E_2>0 on the cube, since v_x=(D_1(x),D_2(x))!=0 by strict sign-rep), (c) H*(f)<=2 whenever the denominator pencil contains an admissible basis.
- **Verified:** informal_prover_codex.py verification==correct (attempt 1, clean Codex window). [Two earlier runs returned spurious 'incorrect' with null solution due to Codex rc=-15 KILLS from running two provers concurrently -- a contention bug, NOT a refutation. Lesson recorded in CODEX_WORKFLOW.md: run Codex provers sequentially on this machine.]
- **F4 significance:** rigorously isolates the residual order-2 obstruction. The sigma-twist (product sign) -- earlier identified as the only positivity-specific obstruction -- is ALWAYS removable at order 2. What remains is *individual* positivity + one-sidedness of the pencil (gauge-invariant: pencil contains an admissible basis). Single products sign(AB) have H*<=2 (difference split A=E_+-E_-, both admissible via a common added constant; AB=E_+ B + E_-(-B)).
- **Order-2 F4-free status:** empirically TRUE (n<=6 reliable, incl balanced twists), rigorous PARTIAL proof (gauge lemma + positive-functional positivity-free + single-product difference-split + one-sidedness-costs-at-order-1 + finite-cube-absorption-has-no-algebraic-analogue). NOT fully closed: the tangent-form product-coupling resists; open gaps are simultaneous one-sidedness of a 2-product sum and the 0-in-conv-hull new-pencil construction. A respawned agent (new-pencil) is working the latter.
- **Recorded in:** lemmas/04_closure_and_structure/040_gauge_transfer.md; lemmas.md (L40); BLUEPRINT.md (28 frontier); knowledge map §6, §8.3.

### 2026-06-25 — Order-2 F4-free: reduced to an n>=5 feasibility conjecture; L40 banked (+ a git-recovery incident)
- **Multi-agent push** (5-angle workflow + 2 respawned agents, after the user flagged dead agents). Net rigorous results on "tChow_pm(f)<=2 => H*(f)<=2":
  - **L40 (banked, verified):** GL_2 gauge invariance of order-2 forms; product-sign twist always removable; H*<=2 iff the denominator pencil contains an admissible basis. (lemmas/04_.../040_gauge_transfer.md)
  - **Quadratic-reach equality (new-pencil agent, unverified):** on the cube x_i^2=x_i, only the OFF-DIAGONAL multilinear quadratic matrix is the Boolean invariant; the admissible-pencil and tChow order-2 forms have IDENTICAL off-diagonal reach. So the quadratic shape never obstructs; only positivity+one-sidedness of the two denominators can cost.
  - **Proved n<=4** by explicit construction: the off-diagonal-through-positive-slopes map has image dim min(2n-1, C(n,2)), SURJECTIVE for n<=4. (But n<=4 is already L32-free since deg_pm=H* there, so not new.)
  - **n>=5 obstruction pinpointed:** 2n-1 < C(n,2), so the given witness's off-diagonal can't be matched with positive slopes -> the proof must switch to a DIFFERENT sign-representative q' of f -> a genuine feasibility/covering statement (the "Feasibility Conjecture"), open, but empirically TRUE and reliable at n<=6.
  - **Disproved my E_1=1 conjecture:** a constant denominator collapses the off-diagonal to rank-1; explicit n=5 functions are admissibly representable but NOT of the form sign(K_1 + E_2 K_2). The proof genuinely needs two nonconstant admissible denominators.
  - Single products sign(AB): H*<=2 via difference-split A=E_+-E_- (both admissible). One-sidedness costs at order 1 (signed-4-cycle); the freeness mechanism is finite-cube absorption with no algebraic analogue.
- **Status:** order-2 F4-free is proved n<=4, open n>=5 (feasibility conjecture, empirically reliable n<=6). Full write-up (unverified): claude-comments/order2_positivity_free_proof.md.
- **INCIDENT + lesson:** a spawned general-purpose subagent created/checked-out a scratch git branch and committed its writeup; the main-session L40 commit landed on that scratch branch and was orphaned on checkout-back. Recovered via git reflog + cherry-pick (L40 = e4c309c on autoresearch). Lesson recorded in CODEX_WORKFLOW.md: research subagents must NOT run git; verify branch/log after every subagent batch.

### 2026-06-25 — Order-2 F4-free: where the focused swing ENDS (reduced to a topological covering obstruction)
- **Focused swing (5-angle workflow on the crux).** Net: order-2 positivity-freeness is NOT closable with current ideas, but is now reduced to a single sharply-characterized obstruction, and rigorous coverage is extended beyond the n<=4 base.
- **RIGOROUS dimension analysis (valid):** dim(tChow order-2 variety) = min(D, 4n-2), D=C(n,2)+(n+1); full-dimensional in ambient quadratics iff 4n-2 >= D iff n<=6 -- a clean dimension-theoretic explanation of the empirical n<=6 boundary. Crucially V_adm = V_tChow are EQUIDIMENSIONAL (=4n-2) with IDENTICAL tangent structure (admissibility is an open, dimension-neutral condition), so NO dimension/transversality/surjectivity argument can decide n>=7. And R_adm (admissibly-spannable pencils) is NOT dense (a positive-measure open set of pencils misses every one-sided cone for n>=6), so NO perturbation/approximation argument can work either.
- **THE OBSTRUCTION (sharp):** H*(f)<=2 iff Pi(f) ∩ A != empty, where Pi(f) = {2-planes Pi=span{E1,E2} of affine forms whose generated module {E1 K1 + E2 K2} meets f's open sign-cell} (nonempty iff tChow_pm(f)<=2) and A = {admissibly-spannable planes} (open, full-dim, exponentially thin, non-dense). This is a TOPOLOGICAL COVERING statement -- whether a connected component of Pi(f) can be trapped entirely in the non-admissible region -- immune to dimension counting AND to any order-2 algebraic invariant (the sigma-twist is gauge-removable, L40; off-diagonal reach is shared, "Lemma 1"). The balance of evidence (0 failures n<=6, full-dim R_adm, no surviving separating invariant) says order-2-free is TRUE, but a proof needs a genuinely new topological/covering tool.
- **FLAW CAUGHT (do NOT propagate):** the workflow's headline "Theorem A: tChow_pm(f)<=r => H*(f)<=r+1 (all n)" is INVALID. Its construction gives q = sum_{h=1}^{r+1} E_h L_h -- a degree-2 SUM OF PRODUCTS -- and miscalls it an "admissible (r+1)-denominator tangent form." But the H*<=K certificate is the CLEARED form c*prod_{h=1}^K E_h + sum_h N_h prod_{g!=h} E_g, which is DEGREE K (coincides with a sum-of-products only at K=2). The "0/2000 verified" only checked the trivial identity sum E_h L_h = q, not that q's sign equals a degree-(r+1) cleared form. So H*<=r+1 does NOT follow. (Lesson: "sum of K admissible-denominator products" = order-K tangent form ONLY for K=2; for K>=3 the cleared form is higher degree. Agent outputs claiming H* bounds via sum-of-products must be checked against the degree-K cleared form.)
- **Theorem B (verifying):** sign(AB+g) with A one-sided has H*<=2 (order-2 construction, a VALID certificate structure unlike A). Extends L41 by an affine perturbation; covers the same-sign-regime pencil {A,1}. Running through the prover.
- **Net:** order-2 F4-free proved n<=4 (L32-covered), extended by L41 (single products) and (pending) Theorem B; reduced for the general case to the topological covering obstruction above. The full F4 (all orders) and even order-2 n>=5 remain open, now with a precise reason (covering, not dimension/algebra).

### 2026-06-25 — L45 banked: disjoint-term composition closes H*(INT_n) <= n-1 (upper side of the rate)
- **Result (L45, verified, prover attempts=2):** for f on Z and a monotone term T = AND_{i in A} w_i on a DISJOINT set A, H*(f) <= H*(f OR T) <= H*(f)+1. Upper side = add ONE summed admissible atom psi = M/D, D = gamma + rho sum_{i in A} alpha^{w_i} (alpha in (0,1)): a "monotone corner detector" -- psi >= 0 everywhere, spikes (> B = max|V|) on the all-ones corner T=1, and is < mu (the neg margin) off it -- so sign(V + psi) = f OR T with H+1 atoms. Lower side = restriction (set any w_{i0}=0, kill T, recover f; L17). (Prover's one fix over my draft: NORMALIZE to a two-sided margin first -- the def only gives f=0 <=> V<=0, so replace V by V - (1/2)min_{f=1}V to make both implications strict; mu>0 is not free. Folded into the banked file.)
- **Flagship corollary:** H*(INT_n) <= n-1 for n>=3, inducting from the base H*(INT_3)=2 (L39). The single "3 disjoint ANDs in 2 heads" saving lives entirely in the L39 base; every later disjoint pair is a clean +1. Combined with L35: n/(8 log_2 n) <= H*(INT_n) <= n-1 -- the upper side of the rate is now RIGOROUS (was empirical). Matches the exact value n-1 at every reliably computed n (n<=5). Residual gap is only Theta(n) vs Theta(n/log n), BMM-barriered.
- **Generalizations (proved as corollaries in the file):** H*(f OR g) <= H*(f) + s for a disjoint monotone DNF g of s terms (sum s corner detectors -> soft indicator I = sum psi_j, ~0 off g; re-derives L14 at f=false); dually H*(f AND g') <= H*(f) + s for a disjoint monotone CNF g' (via negation L15, all-negative corner detectors at the all-zeros corner).
- **Independent corroboration (multi-angle workflow, 5 agents, ALL Claude no-git/no-Codex):** 3 of 4 angles independently produced the same construction; the OR-lemma was proved TWO structurally different ways and both verified by exact-rational full-cube sign checks through n=6 (256/1024/4096 points, exactly n-1 atoms):
  - **Additive bump** (= my construction): psi = A/E, E = (1+2lambda) - lambda(x+y); pick A > -G_min, lambda with A/(1+lambda) < mu.
  - **Multiplicative cleared form** (DIFFERENT, elegant): P = E*P_f + L*Pi with E = (2+eta) - x - y (eta = delta/M; E nearly VANISHES = eta at the AND-corner) and L = -t + 2t(x+y) (t = delta/2). The vanishing denominator E KILLS f's possibly-wrong contribution at the corner, while L's parallelogram-allowed bump (3t at corner vs +/-t else) supplies positivity -- bypassing the XOR/checkerboard obstruction a single affine numerator faces.
- **Weighted-score route is a DEAD-END (valuable negative result):** A_+(INT_n) = 2^n - 1 (verified exactly n<=4; >=35 at n=5), so the L25 weighted-score upper route gives only H* <= 2^n-1 -- NO polynomial bound. INT_n is pairing-dependent (INT=0 iff supp(x),supp(y) disjoint) while an additive score is pairing-blind, so disjoint-support and intersecting points interleave ~2^n times in any positive linear order. => the n-1 saving is IRREDUCIBLY MULTIPLICATIVE (degree-(n-1) products encoding the pairing), consistent with L36's Omega(n/log n). The optimal weights are NOT all-ones (51 alternations at n=4 vs the min 15); even per-pair-balanced/geometric-scaled weights stay exponential.
- **Conceptual insight (the corner detector):** the model's one-sided (monotone) bias means a single admissible head can sharply spike only at the all-ones (or all-zeros) EXTREME corner of a coordinate block, never at an interior vertex. So a monotone term composes for free (+1 head), but a mixed-polarity term -- a parity, or an addressing/equality match -- does NOT, which is WHY IDX_k (L43) and parities are expensive: each address-match is a mixed-polarity corner no single head can isolate. (A single term in isolation is always an LTF, H*=1; the polarity cost is a COMPOSITION phenomenon, not an isolation one.) Also: the construction provably needs UNBOUNDED coefficients (alpha->0, rho->infinity), so a bounded-coefficient max-margin LP shows only tiny/fragile margins -- an artifact, not an obstruction.
- **Recorded in:** lemmas/02_upper_bounds/045_disjoint_term_composition.md; lemmas.md (L45); BLUEPRINT.md (33 frontier); knowledge map §3/§4; synthesis_and_frontier.md.

### 2026-06-25 — L46 banked: bitwise equality EQ_n has H*=2 (equality linearizes) + a pair-predicate taxonomy
- **Result (L46, verified):** EQ_n(x,y) = 1[x=y] = AND of n disjoint XNORs has H*(EQ_n) = 2 for ALL n. Upper: super-increasing weights w_i = 2^{i-1} have distinct subset sums, so x=y <=> I(x)=I(y); after flipping the y-inputs (L15, free) EQ_n = 1[t = 2^n-1] for ONE positive weighted sum t = sum w_i x_i + sum w_i(1-y_i) -- a degenerate single-value weighted band, so H*<=2 (L25/L44). Lower: fix pairs 2..n to agree, EQ restricts to XNOR(x_1,y_1) = a checkerboard => H*>=2 (L3). Confirmed: EQ_n=1[t=2^n-1] exactly (0 mismatches n=1..6, W=2^n-1 strictly interior); explicit robust 2-atom admissible form found+exactly-checked for EQ_3 (64/64 points, margin 0.399, both denominators one-sided positive).
- **Striking contrast:** on the SAME 2n bits, EQ_n (all pairs equal) = 2 heads (CONSTANT) while INT_n (some pair both-1) = Theta~(n). "All pairs equal" is a single integer comparison; "some pair both-1" is irreducibly multiplicative (A_+(INT_n)=2^n-1).
- **Taxonomy of pair-predicates (the general principle):** any Boolean function of the integer difference d = I(x)-I(y) (super-increasing weights => d ranges over a contiguous interval) has H* <= C(G) where f=G(d), because d is (after the y-flip) a positive weighted sum (L25). So the LINEARIZING (cheap) predicates: GT=1[d>0] (H*=1), EQ=1[d=0] (H*=2), integer bands a<=d<=b (<=2), approximate equality |d|<=k (=2). The MULTIPLICATIVE (Theta~(n)) predicates: INT_n, and subset x<=y = NOT INT_n(x,not y) (so H*(subset)=H*(INT_n) by L15). The dividing line = single linear comparison of the two strings vs a coordinate-wise conjunction-across-an-OR.
- **Empirical scoping (reliable n<=3, scipy upper-bound search):** EQ_n=2 (n=1,2,3); HAM(==0)=2, HAM(==n)=2 (= x=not y, also linearizes); INTERIOR HAM(==k) GROWS (<=4 at n=2, <=7 at n=3) -- a candidate NEW separation family (symmetric in the XOR-pattern x XOR y, NOT a function of d, so doesn't linearize). HAM(<=1) gave <=2,<=3 for n=2,3. [Flagged for a future thrust: is interior-Hamming-distance a clean deg_pm-vs-H* separation? Needs a lower bound.]
- **Note:** EQ is an application of L44/L25 + L3 + L15, but a NAMED fundamental predicate with a surprising constant value; it anchors the taxonomy and adds the distinct-subset-sum linearization as a reusable technique. Joins the nonsymmetric exact-value catalog (INT_2/INT_3, products L41/L42, band L44).
- **Recorded in:** lemmas/02_upper_bounds/046_equality_exact.md; lemmas.md (L46); BLUEPRINT.md (34 frontier); knowledge map §3 (table + insight 5).

### 2026-06-25 — Interior-Hamming as a candidate separation; sign-rank as the dichotomy diagnostic
- **Refined dichotomy (the unifying picture):** a pair-predicate is cheap (constant H*) iff its x|y matrix has BOUNDED sign-rank; expensive (Theta~(n)) iff sign-rank grows. Both directions seen: flattening (L22) gives H* >= Omega(log sr) (so constant H* => bounded sr, NECESSARY); the linearizing predicates achieve constant H* AND bounded sr. Sign-rank growth is thus the diagnostic separating easy from hard.
- **Inner-product location refines linearization:** every pair-predicate considered is a function f(s) of the +-1 inner product s = <chi,xi> = n - 2*Hamming. The EXTREMES linearize and are cheap: s=n (EQ, H*=2, sr bounded <=13 since H*=2), s=-n (x=not y, H*=2). INTERIOR values do NOT: HAM_n^{=1} = 1[s=n-2] (one below max).
- **Sign-rank empirics (heuristic projected-gradient sign-rep search, llmenv):** sr_{x|y}(HAM_n^{=1}) ~ n+1 (found rank 4,5,6 sign-reps for n=3,4,5; failed below) -- GROWING LINEARLY, like INT_n (sr in {n,n+1}). Matrix M = 2*Adj - J (Adj = n-cube adjacency, eigenvalues n-2j). deg_pm(HAM_n^{=1}) <= 4 for all n (p = -(Q-(n-1))^2 + 1/2, Q = #agreements bilinear). So IF sr proven unbounded => explicit constant-deg_pm / unbounded-H* separation (a 3rd, new "inner-product-interior" mechanism, distinct from INT's OR and IDX's addressing).
- **Why the standard lower-bound tools STALL (the obstruction):** (a) Forster trivial -- the all-ones eigenvector gives ||M||_2 ~ 2^n - 2n ~ 2^n, so sr >= 2^n/||M||_2 ~ 1 (the function is spectrally concentrated on the trivial eigenvalue; needs balancing). (b) INT shatter-rectangle gadget FAILS -- HAM^{=1}(1_S, e_j) = 1[|S| = 2[j in S]] depends on |S| globally, not a clean membership [j in S] (Hamming's global distance-count blocks row-shattering). (c) planted-XOR gives only constant -- HAM_2^{=1} = PARITY_4 (H* >= 4) but for n>=3 "exactly one disagreement" != "odd", no growing parity restriction. So H*(HAM_n^{=1}) in [4, growing-search-upper-bound]; whether it truly grows is OPEN (no tractable proof either way with current tools).
- **Status:** launched a focused workflow (forster-after-balancing / IP-sign-rank theory / shattering-via-codes / direct-H*) to settle whether sr (hence H*) is unbounded; result pending. Either way the dichotomy + the obstruction analysis are banked knowledge.

### 2026-06-25 — L47 banked: any function of an integer comparison is cheap (the easy-side delineator)
- **Result (L47, verified):** with I(x)=sum 2^{i-1} x_i (distinct subset sums), every f(x,y)=G(I(x)-I(y)) has H*(f) <= C(G) (sign changes of G) and sr_{x|y}(f) <= (C(G)+1)2^{C(G)}+1. Proof: flip y (L15) => d=I(x)-I(y)=t-(2^n-1) with t=sum 2^{i-1}(x_i+z_i) a positive weighted sum whose image is the FULL interval [0,2(2^n-1)] (redundant binary, digits {0,1,2}; verified n<=8); then L25 (H*<=C) + L22 (sign-rank). Generalizes EQ (L46) and unifies GT (H*=1), integer/approx-equality bands (<=2).
- **Significance:** the clean UPPER-side counterpart to the L37 shatter-rectangle lower-bound certificate. Together they pin the easy/hard boundary: integer-comparison predicates (functions of the linear comparison of the two strings) are cheap with BOUNDED sign-rank => can NEVER separate H* from deg_pm (flattening gives nothing); the complementary hard class is the bilinear predicates (INT, subset, interior Hamming) with growing sign-rank. Third "general tool" after L37 (lower) and L45 (composition).
- **Recorded in:** lemmas/02_upper_bounds/047_integer_comparison_upper.md; lemmas.md (L47); BLUEPRINT.md (35 frontier).

### 2026-06-25 — Interior-Hamming separation DEFLATED (workflow): sr <= n+2, only a log-separation at best, lower bound open
- **Verdict (5-angle workflow on HAM_n^{=1}=1[Hamming=1]=1[<chi,xi>=n-2]):** NOT a strong separation. The hoped-for "constant-deg_pm / unbounded-H*" near-linear separation does not materialize.
- **RIGOROUS (bankable knowledge, verified n<=8):** sr_{x|y}(HAM_n^{=1}) <= n+2. Explicit construction R[x,y]=h(d(x,y)), h(j)=1/2 - j - (3/2)(-1)^j (h(1)=1>0, h(j)<=-1<0 else => sign(R)=M); rank = 1 (const) + n (the form s=<chi,xi>) + 1 (parity chi_{[n]}) = n+2. So sign-rank is LINEAR at most. CONSEQUENCE: any separation via flattening is at most H* >= Omega(log sr) = O(log n) -- never near-linear, never 2^{Omega(n)}. (Bonus rigorous facts: EQ has sign-rank EXACTLY 3, R=eps-(t_x-t_y)^2; "Hamming<=1" is realized in dimension n+1 via sign(<chi,xi>-(n-3)).)
- **All spectral lower-bound tools provably DEAD (O(1)):** M=2*Adj(Q_n)-J has ||M||_2=max(2^n-2n,2n), so Forster N/||M|| <= 2 -> 1. KEY LEMMA (rigorous): for d>=1 componentwise, ||diag(d)M|| >= ||M||, so the FSSS bound's sup over ALL positive diagonal scalings = N/||M|| <= 2 -- row/column balancing provably gains nothing (the rank-1 -J term survives every positive scaling). Submatrix-Forster capped at O(sqrt n) (Q_n is n-regular => every m x m submatrix has +1-density <= n/m, and K_{2,3}-free => can't cancel J).
- **METHODOLOGICAL CAUTION (important, reusable):** the bounded-vs-unbounded question is GENUINELY OPEN, evidence NEUTRAL. The earlier "decisively unbounded" read was WRONG. Two false signals, both caught by an EQ control: (1) the distance-symmetric / Krawtchouk-invariant lower bound "any distance-symmetric sign-rep has rank >= n" does NOT transfer to true sign-rank -- EQ's invariant rank grows 4,5,6,7 (n=3..6) yet EQ's true sign-rank is 3; (2) the hinge-loss factorization optimizer over-reports EQ's min rank as 3,5,6,6 too. So NEITHER invariant-rank growth NOR optimizer "minimal feasible rank" trends are reliable certificates of sign-rank growth. Use an EQ (or other known-bounded) control before trusting any numerical sign-rank-growth claim.
- **Refined dichotomy (the real lesson):** strong H* separations come from MEMBERSHIP / shatter-rectangle structure (INT's OR embeds [j in S], IDX's addressing), NOT from mere bilinearity. HAM_n^{=1} is bilinear (a function of <chi,xi>) but isolates a SINGLE interior inner-product value, which has only LINEAR sign-rank (n+2) and admits NO shatter-rectangle (Hamming's global distance-count blocks the [j in S] gadget; the n-regularity blocks hard-pattern embedding). So "bilinear" was too coarse: the separating ingredient is the OR/addressing/membership combinatorics, which gives the shatter-rectangle (L37); a lone interior level does not.
- **Status:** HAM thread CLOSED as a separation candidate (at most a log-separation, lower bound open with neutral evidence; a proof would need a non-spectral interior-threshold sign-rank bound or a growing orthogonal-row substructure in the distance-1 matrix). Net knowledge gain: the rigorous sr<=n+2 bound, the Forster-dead proof, the EQ-control caveat, and the membership-not-bilinearity refinement of the dichotomy.

### 2026-06-25 — L48 banked: every output bit of integer addition has H* <= 3 (the carry chain is free)
- **Result (L48, verified):** ADD_{n,j} = j-th bit of I(x)+I(y) has H*(ADD_{n,j}) <= 3 for ALL n, j (carry-out j=n: =1, LTF; LSB j=0: =2, XOR_2; interior: in {2,3}). Construction: bit j depends only on the low bits (junta, L21) and equals floor(A'/2^j) mod 2 for the POSITIVE weighted sum A' = I(x_{<=j})+I(y_{<=j}); as a function of A' in [0, 2^{j+2}-2] it runs 0,1,0,1 over four half-periods => C(F) <= 3 sign changes => H* <= 3 by L25. Lower bound >= 2 (non-carry bits) via XOR checkerboard (restrict carry constant). Construction verified exactly n=2..5, all j (bit_j(sum)==bit_j(A'), C(F)=2/3/1 for LSB/interior/carry-out).
- **Significance:** addition is CHEAP for attention -- the carry chain (a sequential dependency of bit j on all j lower bits) costs nothing asymptotically, because the carry is itself a threshold of a positive weighted sum. Places integer addition on the easy weighted-score/comparison side with EQ (L46) and integer comparison (L47). Contrast: multiplication bits are NOT functions of a single weighted sum (expected hard).
- **METHODOLOGICAL VINDICATION (the EQ-control lesson, applied successfully):** the random-restart admissible-form search OVER-REPORTED badly here -- it returned H* upper bounds 2,3,3,4,5,6,7 for n=4 (apparent linear growth, looked like a separation!). But the bit's x|y matrix is a diagonal-conjugated COMPARISON matrix (sign-rank <= 3, bounded), the structural tell that H* is bounded; the clean weighted-score construction then gave the true <= 3. So: do NOT trust the search's growing upper bounds as evidence of a separation; check sign-rank (a comparison/bounded-sr structure predicts bounded H*) and look for a weighted-score/junta construction. This is exactly the caution the HAM thread crystallized, now paying off.
- **Recorded in:** lemmas/02_upper_bounds/048_addition_bits.md; lemmas.md (L48; also fixed L47's stale "interior Hamming has growing sign-rank" clause); BLUEPRINT.md (36 frontier); knowledge map sec 3 table.

### 2026-06-25 — Affine-dimension characterization conjecture: STATED then REFUTED (Sherstov, via Codex consult)
- **The conjecture (crystallizing the dichotomy):** H*(f)=O(1) iff f is a bounded-cell function of O(1) affine forms (f=F(L_1,...,L_k), k=O(1)). For k=1 it is EXACT and proven (L12/L25: H* = sign-changes of F along the one score). Fits the whole catalog: easy = low affine dimension (EQ/bands/comparison/addition k=1; products k=2), hard = omega(1) forms (INT/IDX/disjoint-DNF).
- **REFUTED at k>=2.** Since the cleared H-head form is a degree-H PTF, H*(f) >= deg_pm(f). Sherstov (arXiv:0910.4224, "The intersection of two halfspaces has high threshold degree") constructs two halfspaces whose intersection has threshold degree Omega(n). So AND of two LTFs -- a ONE-cell function of just TWO affine forms -- has H* = Omega(n), UNBOUNDED. The conjecture's <= direction is false: low affine dimension is NECESSARY but NOT SUFFICIENT for low H*.
- **The small-n trap (again):** random and majority-based AND-of-2-LTFs stay at deg_pm=2, H*<=2 through n<=12 (I verified MAJ(x) AND MAJ(y) on disjoint blocks: deg_pm=2 for m<=6). The H*<=2 I saw at n<=6 was the classic small-instance over-confidence -- the hard intersections are special constructions whose Omega(n) growth is asymptotic, beyond brute-force LP range. SAME lesson as EQ/Hamming: do not infer asymptotic boundedness from n<=6.
- **Codex consult (per CODEX_WORKFLOW):** I was genuinely uncertain whether AND-of-2-LTFs is <=2 (a clean construction would have been bankable) or unbounded. Consulted Codex (background, </dev/null); it correctly answered UNBOUNDED with the H* >= deg_pm reduction and the Sherstov citations (0910.1862 for two-majorities, 0910.4224 for the worst-case Omega(n)). A clean example of the consult catching a wrong conjecture before it was over-committed.
- **Clean corollary banked as knowledge:** H*(f AND g) <= H*(f)+H*(g) FAILS even for DISJOINT LTFs (intersection of two halfspaces on disjoint blocks: each LTF has H*=1 but the AND has H*=Omega(n)). So disjoint composition is subadditive only for terms/clauses (L45's monotone corner detector), NOT for general functions -- sharpens the L45 scope and the "composition is not subadditive" map insight 4.
- **Net:** the easy/hard dichotomy (weighted-comparison cheap, membership/addressing hard) is a faithful INTUITION but NOT a clean low-dimension characterization; the only exact invariant is L16/tChow. Recorded in synthesis sec 4.2 (conjecture stated + refuted).

### 2026-06-25 — L49 banked: min/max bits have H*=2 (more tractable knowledge after a premature "saturation")
- **Context (lesson):** I had declared the tractable vein "comprehensively mined" -- WRONG. A reliable deg_pm sweep (LP, no over-reporting) of unmined natural functions found min/max bits have CONSTANT deg_pm=2, leading to a clean new result. Lesson: "needs a new tool for the hard frontiers" does NOT mean "no tractable knowledge remains"; reliable deg_pm + construction-seeking keeps finding clean easy-side results.
- **Result (L49, verified):** MIN_{n,j}=bit_j(min(I(x),I(y))) and MAX have H*=2 for j<=n-2 (top bit = x_{n-1} AND y_{n-1} / OR, an LTF, H*=1). Since bit_j(I(z))=z_j, MIN_{n,j}=x_j if I(x)<=I(y) else y_j -- a COMPARISON-GATED BIT SELECTION (multiplexer). Construction: V=(x_j-y_j)(1/2-d)+(x_j+y_j-1), d=I(x)-I(y) (disjoint-support summands, sign(V)=2*MIN-1 verified n<=5 all j) = AB+g with A=x_j-y_j ONE-SIDED after flipping y_j (L15) => L42 gives <=2. Lower bound: an affine-parallelogram crossing certificate (P00+P11=P01+P10, labels 0,1,1,0; the generalized checkerboard via the antipode identity L2 -- a plain 2-coord checkerboard does NOT exist here) shows it is not an LTF => deg_pm>=2 => H*>=2.
- **deg_pm sweep (reliable LP, the key tool):** min/max bits deg_pm=2 (constant, all n); ADDITION bits small; but MULTIPLICATION middle bit deg_pm=1,3,4 (n=2,3,4) and IP deg_pm=2,3,4 -- both GROW ~n. So the rigorous arithmetic picture: comparison (L47, <=1), addition (L48, <=3), min/max (L49, =2) are EASY (constant deg_pm, weighted-comparison side); multiplication and IP are HARD (deg_pm=Omega(n), threshold-degree source). Clean addition-easy / multiplication-hard contrast.
- **EQ-control applied successfully again:** the admissible-form search over-reported min-bit H* (returned 3 at n=5); the bounded sign-rank (~2, stable, vs the EQ heuristic control which over-reports to >5) correctly flagged bounded H*, and the deg_pm=2 floor + L42 construction pinned the true value 2. The reliable diagnostics (deg_pm LP, sign-rank with EQ control) beat the raw search every time.
- **General principle (noted):** "select between two single literals gated by one affine threshold" has H*<=2 (the V=AB+g construction with one-sided A); min/max is the named instance. The gate being ONE comparison and the choices being SINGLE literals is what keeps it quadratic -- contrast AND-of-2-general-LTFs (Sherstov Omega(n)).
- **Recorded in:** lemmas/02_upper_bounds/049_minmax_bits.md; lemmas.md (L49); BLUEPRINT.md (37 frontier); knowledge map sec 3 table (+ a hard-side row: mult/IP/AND-of-2-LTFs = Omega(n) via deg_pm).

### 2026-06-25 — Arithmetic sub-picture mapped: order statistics cheap, multiplication hard
- **Subtraction (deg_pm sweep):** (x-y) mod 2^n bits have deg_pm <= 3 (LSB 2, interior 3), constant -- cheap like addition (it IS addition of x and ~y). Confirms +/- symmetry; not banked separately (reduces to L48).
- **Median (3-way order statistic), deg_pm=3 CONSTANT (m=2,3 reliable):** bit_j(median(a,b,c)) has deg_pm=3 (interior), 1 (top). H*=3 for m=2 (n=6, search found 3, deg_pm floor 3 => exactly 3). At m=3 (n=9) the search returned ">10" -- a SEARCH ARTIFACT (over-reporting, unreliable at 512 pts; deg_pm=3 constant means true H* is ~3). Structural reason cheap: "a is the median" = 1[(a-b)(a-c)<=0] is a single product-sign (L41, H*<=2); median bit = sum_a a_j * [a is median], degree 3. NOT banked (the general degree-3 construction is involved; H*=3 is well-supported but not yet a clean verified lemma).
- **Order statistics: cheap only for SMALL m (corrected after a reliability check).** min/max (m=2) PROVEN H*=2 (L49); median (m=3) H*=3, deg_pm=3 CONSTANT across 2,3,4 bits-per-integer (n=6,9,12). BUT median of FOUR (m=4) already grows: deg_pm = 3 (2 bits) -> 4 (3 bits), and the asymptotic is beyond brute force (m=4,4-bits = n=16 infeasible). So "k-th-of-m is constant-head" is NOT established for m>=4 and likely FALSE: rank = an exact count of comparison-LTFs, the same LTF-combination structure that makes AND-of-2-LTFs hard (Sherstov). [Caught my over-strong first claim -- same lesson as the affine-dimension conjecture: verify the bits-per-integer scaling with reliable deg_pm before claiming "constant for fixed m".] Net established: m=2 cheap (proven), m=3 cheap (well-supported), m>=4 open/likely-growing.
- **Multiplication & IP HARD (rigorous deg_pm growth):** multiplication's middle bit deg_pm = 1,3,4 (n=2,3,4); IP deg_pm = 2,3,4 -- both grow ~n, so H* = Omega(n) (H*>=deg_pm). These are NOT functions of O(1) comparisons (genuinely bilinear/multiplicative). The arithmetic easy/hard line = additive-and-comparison-based (cheap) vs multiplicative/bilinear (hard), matching the pair-predicate dichotomy.
- **Lesson reinforced:** the reliable diagnostics (deg_pm LP, sign-rank with EQ control) decide cheap-vs-hard; the raw admissible-form search over-reports at every turn (addition 5,6,7; min-bit 3; median >10) and must never be trusted for an asymptotic/hardness claim. Recorded in synthesis sec 2.5 (arithmetic sub-picture).

### 2026-06-25 — L50 banked: the median bit is a concrete F4 probe (tChow=3, natural denominators inadmissible)
- **What started as "is median cheap" became the sharpest concrete F4 test of the session.** Codex consult (per CODEX_WORKFLOW) on a median H*<=3 construction returned a BEAUTIFUL symmetric cubic AND correctly flagged it does NOT certify H*<=3.
- **Result (L50, verified):** tChow_pm(MED_j) = 3 via P_j = s_x(B-C)^2 + s_y(A-C)^2 + s_z(A-B)^2 (A=I(x),B=I(y)+1/4,C=I(z)+1/2, s_x=2x_j-1). sign(P_j)=2*MED_j-1 (verified exact n=2,3): for A<B<C the median term s_y(u+v)^2 dominates since (u+v)^2>u^2+v^2. Regroups (via L3=L2-L1) to a tangent form sum_h N_h prod_{k!=h} D_k with D_h = the pairwise differences L1=A-B,L2=A-C,L3=B-C, N_h=+-(s+s). So tChow_pm<=3; with deg_pm=3, =3.
- **THE F4 SIGNIFICANCE (the point):** the witness's denominators L1,L2,L3 form a MIXED-SIGN TRIANGLE: A-B (+,-,0), A-C (+,0,-), B-C (0,+,-). NO global input flip makes all three one-sided simultaneously (would need 3 blocks pairwise oppositely oriented). span(L1,L2) has no nonzero one-sided affine form. So the clean tChow witness does NOT certify H*<=3 -- positivity is VISIBLY BLOCKED at the natural witness. This is a SINGLE EXPLICIT FUNCTION posing F4 sharply (vs the abstract order-2 covering statement).
- **Numerics (tantalizingly split):** admissible 3-form search -- m=2 (n=6): FOUND, margin up to 2.0 (healthy) => H*=3=tChow, F4-FREE there (via messy denominators unrelated to L_h, all monotone). m=3 (n=9): two heavy searches (restricted all-decreasing AND general oriented denominators) FAILED, best margin ~0.0. INCONCLUSIVE: either optimization failure (F4-free, form exists) OR the FIRST POSITIVITY GAP (H*>tChow=3, refuting F4). Heuristic infeasibility is NOT proof -- the session has repeatedly seen search fail where a construction exists -- so this is a sharp open candidate, not a resolution.
- **Why this matters for "the final proof":** F4 (H*=?tChow_pm) is the gateway to characterizing H*. The median is now the MOST PROMISING CONCRETE HANDLE: resolve H*(MED_j) -- construct the admissible order-3 form for all n (F4-free + a template for admissible constructions when natural denominators are inadmissible), or prove its nonexistence at n=9 (a positivity-aware lower bound, the single missing tool, which would refute F4). The decisive sub-step: a RELIABLE (non-heuristic) feasibility verdict for the admissible 3-form at n=9.
- **Contrast with the cheap order statistics:** min/max (L49, H*=2) use A=x_j-y_j, one-sided after ONE flip; the median's THREE pairwise differences cannot all be flipped one-sided at once -- the obstruction is the three-way coupling, appearing first at order 3.
- **Recorded in:** lemmas/02_upper_bounds/050_median_tchow.md; lemmas.md (L50); BLUEPRINT.md (38 frontier); synthesis sec 3 (the order-3 F4 probe) + sec 5 (most promising F4 handle).
