# Blueprint — Head Complexity $H^{*}(f)$

> Single source of truth for the research, **reconciled with `lemmas.md`**. The
> foundation (Lemmas 1–12) is already proved AND Lean-verified in
> `lemmas/01_foundations_and_normal_form/` + `head-complexity/`; those nodes are
> `done`, do not re-prove them. The real work is the FRONTIER section, organized
> around the route L10 → cleared-denominator polynomial invariant ($\mathrm{MFdeg}_{\pm}$)
> → tangential-Chow comparison, cross-checked against an independent decomposition.
> Keep this file and `lemmas.md` consistent after every change. See
> `informal_decomposition.md` for the loop; budgets Simple 20 / Medium 35 / Complex 50.

## Progress Summary

- **Foundation (done, Lean-verified):** 12 / 12
- **Frontier (open):** 0 done / 11 todo
- **First core question** (exact/approx invariant for $H^{*}$): OPEN for nonsymmetric $f$.

What the foundation already settles: one-head level = linear threshold functions
(L11); exact model-native invariant via the linear-fractional normal form (L10);
lower bound $\deg_{\pm}(f)\le H^{*}(f)$ (L6); upper bound $H^{*}(f)\le M_{+}(f)-1$
from positive weighted-sum image cardinality (L9); **symmetric functions solved
exactly** by the sign-change count $H^{*}(f)=C(F)$ (L12), incl. $H^{*}(\mathrm{XOR}_n)=n$.
The gap: for general (nonsymmetric) $f$ there is no exact invariant between the
$\deg_{\pm}$ lower bound and the weighted-sum upper bound. The frontier attacks
this by sharpening L10 into a cleared-denominator polynomial invariant
$\mathrm{MFdeg}_{\pm}$ (provably equal to $H^{*}$) and comparing it, via the
tangent space of the Chow variety of products of linear forms, to a known-flavored
tangential-Chow threshold degree.

---

# Foundation (proved + Lean-verified — DONE)

| node | statement (short) | uses | proof |
|---|---|---|---|
| `L1:additive_decomposition` | one-head 2-coord restriction: $N,D$ split additively | — | `lemmas/01_foundations_and_normal_form/001_checkerboard_additive_decomposition.md` |
| `L2:antipode_identities` | $N(00)+N(11)=N(01)+N(10)$, same for $D$ | L1 | `.../002_antipode_identities.md` |
| `L3:checkerboard_obstruction` | a 2-bit checkerboard restriction forces $H^{*}\ge 2$ | L2 | `.../003_checkerboard_obstruction.md` |
| `L4:symmetric_thresholds` | $H^{*}(T_{n,t})=1$; so AND/OR/MAJ $=1$ | — | `.../004_symmetric_thresholds.md` |
| `L5:family_consequences` | $H^{*}(\mathrm{PARITY}_n)\ge2$, $H^{*}(\mathrm{EXACT}_{n,k})\ge2$ | L3, L4 | `.../005_family_consequences.md` |
| `L6:threshold_degree_lower_bound` | $\deg_{\pm}(f)\le H^{*}(f)$ | — | `.../006_threshold_degree_head_complexity_bound.md` |
| `L7:parity_threshold_degree` | $\deg_{\pm}(\mathrm{PARITY}_n)=n$ | — | `.../007_parity_threshold_degree.md` |
| `L8:exact_parity_complexity` | $H^{*}(\mathrm{XOR}_n)=n$ | L6, L7 | `.../008_exact_parity_complexity.md` |
| `L9:weighted_sum_upper_bound` | $H^{*}(f)\le M_{+}(f)-1$ (weighted-sum image) | — | `.../009_weighted_sum_upper_bound.md` |
| `L10:linear_fractional_normal_form` | $H^{*}(f)=L_{\mathrm{frac}}(f)$ (exact normal form) | — | `.../010_linear_fractional_normal_form.md` |
| `L11:one_head_characterization` | $H^{*}=0$ iff constant; $H^{*}=1$ iff nonconstant LTF | L10 | `.../011_one_head_characterization.md` |
| `L12:symmetric_sign_changes` | symmetric: $H^{*}(f)=C(F)$ (sign-change count) | L6, L10 | `.../012_symmetric_sign_changes.md` |

> NOTE: my earlier generated nodes (incl. $H^{*}(\mathrm{XOR}_2)=2$ in
> `informal_xor2_solution.md`) are all subsumed by the above (that one is L8 at
> $n=2$). They were a pipeline check, not new math.

---

# Frontier (open — the actual work)

Build on the foundation. Each node is a concrete provable target; prove via
`informal_prover_codex.py`, record into `lemmas/` + `lemmas.md` on `\boxed{1}`.
The spine (F1 → F2 → F3 → F4 → first core question) turns the L10 normal form
into a cleared-denominator polynomial invariant and compares it to a known
algebraic invariant; F5–F7 supply equality/separation results and lower-bound
certificates, F8 the upper-bound route, and the two function-family nodes are
concrete stress tests.

# frontier:atom_dictionary
- **uses**: `[[L10:linear_fractional_normal_form]]`
- **status**: `todo` | **difficulty**: Medium | **attempts**: `0 / 35`
- **statement**: (F1) Rewrite each one-head L10 atom as $\phi(x)=N(x)/D(x)$ with
  $N,D$ affine on the cube and $D>0$, by expanding $\alpha^{x_i}=1+(\alpha-1)x_i$.
  Characterize exactly which positive affine denominators $D$ arise from
  $\gamma+\sum_i\rho_i\alpha^{x_i}$ (the admissible atom dictionary). Difficulty
  is the converse direction, especially the $\alpha=1$ and zero-coefficient
  boundary cases.

# frontier:cleared_denominator_invariant
- **uses**: `[[L10:linear_fractional_normal_form], [frontier:atom_dictionary]]`
- **status**: `todo` | **difficulty**: Complex | **attempts**: `0 / 50`
- **statement**: (F2) Define $\mathrm{MFdeg}_{\pm}(f)$ as the least $H$ for which
  $f$ is sign-represented by
  $P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\ne h}D_g(x)$,
  with admissible affine pairs $(N_h,D_h)$ from the atom dictionary and each
  $D_h>0$ on the cube. Prove $H^{*}(f)=\mathrm{MFdeg}_{\pm}(f)$ by clearing the
  (positive) denominators of the L10 normal form and reversing by division,
  preserving strict classification margins and handling degenerate heads. This
  is the sharp restatement of the gap.

# frontier:tangential_chow_reformulation
- **uses**: `[[frontier:cleared_denominator_invariant]]`
- **status**: `todo` | **difficulty**: Complex | **attempts**: `0 / 50`
- **statement**: (F3) Homogenize with $x_0=1$ and identify the polynomials $P$
  above with elements of the tangent space at $\prod_h D_h$ to the degree-$H$
  Chow variety of products of $H$ linear forms ($P$ is exactly the standard
  tangent-space form $\theta\prod_h D_h+\sum_h N_h\prod_{g\ne h}D_g$). Keep the
  attention positivity/admissibility constraints explicit throughout.

# frontier:tchow_comparison
- **uses**: `[[frontier:tangential_chow_reformulation]]`
- **status**: `todo` | **difficulty**: Complex | **attempts**: `0 / 50`
- **statement**: (F4) Define $\mathrm{tChow}_{\pm}(f)$ by dropping the
  attention-specific positivity restrictions in the tangential-Chow form (a
  known-flavored algebraic invariant). Prove either $H^{*}(f)=\mathrm{tChow}_{\pm}(f)$,
  a tight sandwich, or exhibit a separating family. Key obstruction: whether
  arbitrary affine factors can be normalized or perturbed positive on the cube
  without breaking the final threshold. This is the route connecting $H^{*}$ to
  a standard invariant.

# frontier:deg_pm_equality_stress_test
- **uses**: `[[L6:threshold_degree_lower_bound], [L11:one_head_characterization], [L12:symmetric_sign_changes], [frontier:cleared_denominator_invariant], [frontier:tangential_chow_reformulation]]`
- **status**: `todo` | **difficulty**: Complex | **attempts**: `0 / 50`
- **statement**: (F5) Decide whether $H^{*}(f)=\deg_{\pm}(f)$ beyond the known
  LTF (L11), symmetric (L12), and parity (L8) cases, starting with all quadratic
  threshold functions. Analyze the $H=2$ coefficient matrix/tensor forced by the
  cleared-denominator form; the hard part is non-uniqueness of sign-representing
  polynomials. (Equality half of the old `deg_pm_separation`.)

# frontier:counting_separation
- **uses**: `[[frontier:cleared_denominator_invariant], [frontier:tangential_chow_reformulation]]`
- **status**: `todo` | **difficulty**: Complex | **attempts**: `0 / 50`
- **statement**: (F6) Upper-bound the number of realizable $H$-head sign patterns
  via Warren / Milnor-Thom bounds over the $O(Hn)$ atom parameters, and compare
  against counts of quadratic PTFs to exhibit (if true) some $f$ with
  $\deg_{\pm}(f)=2$ but $H^{*}(f)=\Omega(n)$, a separation. Main work: controlling
  parameter redundancy and strict inequalities. (Separation half of the old
  `deg_pm_separation`.)

# frontier:lower_bound_certificates
- **uses**: `[[frontier:tangential_chow_reformulation]]`
- **status**: `todo` | **difficulty**: Complex | **attempts**: `0 / 50`
- **statement**: (F7) Derive checkable obstructions to $H^{*}(f)\le H$ from the
  tangential-Chow form, such as flattening-rank, catalecticant, or
  restriction-based certificates, converting "no admissible sign-representer
  exists" into finite algebraic/rank tests. Difficulty: quantifying over all
  sign-representing polynomials.

# frontier:calibrated_positive_sum_upper_bound
- **uses**: `[[L9:weighted_sum_upper_bound], [frontier:cleared_denominator_invariant]]`
- **status**: `todo` | **difficulty**: Medium | **attempts**: `0 / 35`
- **statement**: (F8) Extend L9 from one positive weighted sum to calibrated
  decompositions $f(x)=\mathbf 1[\theta+\sum_{r=1}^{s} a_r F_r(t_r(x))>0]$ with
  $t_r(x)=\sum_i\lambda_{ri}x_i$, $\lambda_{ri}>0$, aiming for
  $H^{*}(f)\le\sum_r(|\mathrm{Im}(t_r)|-1)$. Each block must emit a calibrated
  real feature for linear combination, not merely separate signs. Concrete
  instances to settle first: the DNF bound ($s$ terms $\Rightarrow H^{*}(f)\le s$
  via subcube-bump heads $r_T(x)=\frac{1}{1+\lambda v_T(x)}$, $\lambda>s$) and the
  sparse threshold-density bound ($\theta+\sum_j c_j\mathbf 1_{T_j}$ with positive
  margin $\Rightarrow H^{*}(f)\le s$). (Subsumes the old `general_dnf_upper_bound`
  and `sparse_threshold_density_upper_bound`.)

# frontier:address_indexing
- **uses**: `[[L10:linear_fractional_normal_form], [frontier:calibrated_positive_sum_upper_bound], [frontier:lower_bound_certificates]]`
- **status**: `todo` | **difficulty**: Medium | **attempts**: `0 / 35`
- **statement**: Determine $H^{*}$ for address / indexing functions (a canonical
  asymmetric family), exactly or up to constants. A concrete test of the
  upper-bound (F8) and certificate (F7) machinery against an explicit
  nonsymmetric target.

# frontier:threshold_intersection
- **uses**: `[[frontier:calibrated_positive_sum_upper_bound], [L6:threshold_degree_lower_bound]]`
- **status**: `todo` | **difficulty**: Medium | **attempts**: `0 / 35`
- **statement**: Bound $H^{*}$ for intersections of $k$ threshold functions in
  terms of $k$, and compare to $\deg_{\pm}$. Another concrete asymmetric family
  stress-testing the gap.

# open:first_core_question
- **uses**: `[[frontier:tchow_comparison], [frontier:deg_pm_equality_stress_test], [frontier:counting_separation], [frontier:lower_bound_certificates], [frontier:calibrated_positive_sum_upper_bound], [L12:symmetric_sign_changes]]`
- **status**: `todo` | **difficulty**: Complex (research) | **attempts**: `0 / 50`
- **statement**: (F9) Assemble the exact identity $H^{*}=\mathrm{MFdeg}_{\pm}$
  (F2), the tangential-Chow comparison (F4), the $\deg_{\pm}$ equality/separation
  results (F5, F6), the lower-bound certificates (F7), and the positive-sum upper
  bounds (F8) into a precise answer to the first core question of
  `problem_statement.md`: is $H^{*}(f)$ a known invariant or a strictly finer
  refinement? Symmetric case is settled (L12). Key risk: avoid a mere renaming of
  $L_{\mathrm{frac}}$, i.e. the final invariant must connect to standard
  polynomial-threshold, rational, density, or Chow-rank notions.

---

## Critical path

`L10:linear_fractional_normal_form` → `frontier:atom_dictionary` (F1) →
`frontier:cleared_denominator_invariant` (F2) →
`frontier:tangential_chow_reformulation` (F3) → `frontier:tchow_comparison` (F4) →
`open:first_core_question` (F9): translate $L_{\mathrm{frac}}$ into a positive
tangential-Chow threshold invariant, then decide whether the positivity-restricted
version equals a standard known invariant or defines a strict new refinement.

## Pitfalls (carry into every node)

- One head is **not** nonlinear after thresholding (multiply by its positive
  denominator → it collapses to a linear threshold function; this is L11).
- The attention positivity/admissibility constraints (each $D_h>0$ on the cube)
  are the whole difficulty of the tangential-Chow comparison; never silently drop
  them, since dropping them yields $\mathrm{tChow}_{\pm}$, a possibly strictly
  different invariant (F4).
- Never use vanishing denominators; softmax denominators are strictly positive,
  keep positive slack.
- Do not confuse exact feature representation with exact classification; gadgets
  need only a strict classification margin on the finite cube.

### Frontier refinement: affine atom dictionary

Strengthen `frontier:atom_dictionary` to prove the full affine pair dictionary, not only the denominator dictionary. The nonconstant denominator cases allow arbitrary affine numerators; the constant denominator case has a same-sign numerator-coefficient boundary that must be tracked before `frontier:cleared_denominator_invariant`.

# frontier:atom_dictionary
- **status**: `done` as Lemma 13, [013_affine_atom_dictionary.md](lemmas/01_foundations_and_normal_form/013_affine_atom_dictionary.md)
- **uses**: `[[L10:linear_fractional_normal_form]]`
- **unlocks**: `[[frontier:cleared_denominator_invariant]]`

Update frontier progress to record `frontier:atom_dictionary` as done via Lemma 13. Promote `frontier:cleared_denominator_invariant` as the active next node, with dependencies `L10:linear_fractional_normal_form` and `L13:affine_atom_dictionary` now satisfied.

# frontier:cleared_denominator_invariant
- **status**: `done` as Lemma 14, [014_cleared_denominator_invariant.md](lemmas/01_foundations_and_normal_form/014_cleared_denominator_invariant.md)
- **uses**: `[[L10:linear_fractional_normal_form], [L13:affine_atom_dictionary]]`
- **unlocks**: `[[frontier:tangential_chow_reformulation], [frontier:deg_pm_equality_stress_test], [frontier:counting_separation], [frontier:lower_bound_certificates], [frontier:calibrated_positive_sum_upper_bound]]`

Update frontier progress to record `frontier:cleared_denominator_invariant` as done via Lemma 14. Promote `frontier:tangential_chow_reformulation` as the active next critical-path node, with dependencies `L10:linear_fractional_normal_form`, `L13:affine_atom_dictionary`, and `frontier:cleared_denominator_invariant` now satisfied.

### Frontier update: active tangential-Chow reformulation

Reconcile progress after Lemmas 13 and 14: `frontier:atom_dictionary` and `frontier:cleared_denominator_invariant` are done. The active leaf is now `frontier:tangential_chow_reformulation`, which should prove the exact equivalence between Lemma 14's cleared-denominator polynomials and admissibility-restricted tangent vectors to the degree-$H$ Chow variety.

# frontier:tangential_chow_reformulation
- **status**: `done` as Lemma 15, [015_tangential_chow_reformulation.md](lemmas/01_foundations_and_normal_form/015_tangential_chow_reformulation.md)
- **uses**: `[[L13:affine_atom_dictionary], [L14:cleared_denominator_invariant]]`
- **unlocks**: `[[frontier:tchow_comparison], [frontier:deg_pm_equality_stress_test], [frontier:counting_separation], [frontier:lower_bound_certificates]]`

### Frontier refinement: unrestricted tangential-Chow sandwich

Add `frontier:tchow_sandwich_lower_bound` as the first leaf under `frontier:tchow_comparison`.

- **uses**: `[[L15:tangential_chow_reformulation], [L6:threshold_degree_lower_bound]]`
- **status**: `todo`
- **statement**: Define unrestricted $\mathrm{tChow}_{\pm}(f)$ by dropping all attention positivity and admissibility restrictions from Lemma 15's tangential-Chow form. Prove the unconditional sandwich $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$.
- **unlocks**: `[[frontier:tchow_comparison], [frontier:lower_bound_certificates], [frontier:counting_separation]]`

### Frontier update: unrestricted tangential-Chow sandwich

# frontier:tchow_sandwich_lower_bound
- **status**: `done` as Lemma 16, [016_tchow_sandwich_lower_bound.md](lemmas/01_foundations_and_normal_form/016_tchow_sandwich_lower_bound.md)
- **uses**: `[[L14:cleared_denominator_invariant], [L15:tangential_chow_reformulation]]`
- **unlocks**: `[[frontier:tchow_comparison], [frontier:lower_bound_certificates], [frontier:counting_separation]]`

This records the first completed leaf under `frontier:tchow_comparison`. The remaining comparison work is to decide whether either inequality in $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{\ast}(f)$ can be strict.

### Frontier refinement: same-polarity DNF upper bound

Add `frontier:same_polarity_dnf_upper_bound` as the first proved-ready leaf under `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L10:linear_fractional_normal_form], [L13:affine_atom_dictionary], [L14:cleared_denominator_invariant]]`
- **status**: `todo`
- **statement**: For any fixed polarity $\zeta\in\{0,1\}$, an $s$-term DNF whose terms only require literals $x_i=\zeta$ satisfies $H^{\ast}(f)\leq s$ via calibrated reciprocal subcube bumps.
- **unlocks**: calibrated positive-sum upper bounds for sparse monotone and sparse anti-monotone DNF families, and isolates the remaining mixed-literal DNF case as a separate gadget problem.

### Frontier update: same-polarity DNF subcube upper bound

# frontier:same_polarity_dnf_upper_bound
- **status**: `done` as Lemma 17, [017_same_polarity_dnf_upper_bound.md](lemmas/01_foundations_and_normal_form/017_same_polarity_dnf_upper_bound.md)
- **uses**: `[[L10:linear_fractional_normal_form], [L13:affine_atom_dictionary]]`
- **unlocks**: `[[frontier:calibrated_positive_sum_upper_bound]]`

### Frontier refinement: same-polarity sparse threshold density

Add `frontier:same_polarity_sparse_threshold_density_upper_bound` under `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L10:linear_fractional_normal_form], [L13:affine_atom_dictionary], [L17:same_polarity_dnf_upper_bound]]`
- **status**: `todo`
- **statement**: Any strict linear threshold of $s$ same-polarity coordinate-subcube indicators has $H^{\ast}\leq s$, by uniformly approximating each indicator with an admissible reciprocal bump and preserving the finite margin.
- **unlocks**: calibrated positive-sum upper bounds for sparse monotone and sparse anti-monotone threshold-density functions.

### Frontier update: same-polarity sparse threshold-density upper bound

# frontier:same_polarity_sparse_threshold_density_upper_bound
- **status**: `done` as Lemma 18, [018_same_polarity_sparse_threshold_density_upper_bound.md](lemmas/01_foundations_and_normal_form/018_same_polarity_sparse_threshold_density_upper_bound.md)
- **uses**: `[[L10:linear_fractional_normal_form], [frontier:same_polarity_dnf_upper_bound]]`
- **unlocks**: `[[frontier:calibrated_positive_sum_upper_bound]]`

### Frontier refinement: Warren counting bound for low head complexity\n\nAdd `frontier:warren_head_count_upper_bound` under `frontier:counting_separation`.\n\n- **uses**: `[[L14:cleared_denominator_invariant]]`\n- **status**: `todo`\n- **statement**: Use the cleared-denominator parameterization and Warren's theorem to prove $\log_2 |\{f:H^{\ast}(f)\leq H\}| \leq C H n(n+\log(H+1))$.\n- **unlocks**: counting separations from large families of low threshold-degree functions, especially quadratic PTFs.

### Frontier update: Warren counting bound for low head complexity

# frontier:warren_head_count_upper_bound
- **status**: `done` as Lemma 19, [019_warren_head_count_upper_bound.md](lemmas/01_foundations_and_normal_form/019_warren_head_count_upper_bound.md)
- **uses**: `[[L14:cleared_denominator_invariant]]`
- **unlocks**: `[[frontier:counting_separation]]`

This records the Warren counting upper bound under `frontier:counting_separation`. It supplies the low-head counting estimate needed for future separation arguments against large low-degree threshold families.

### Frontier refinement: quadratic PTF head separation

Add `frontier:quadratic_ptf_head_separation` under `frontier:counting_separation`.

- **uses**: `[[L11:one_head_characterization], [L19:warren_head_count_upper_bound]]` plus the surveyed fixed-degree PTF counting lower bound for degree $2$.
- **status**: `todo`
- **statement**: Prove that for all sufficiently large $n$ some quadratic threshold function $f_n : \{0,1\}^{n} \to \{0,1\}$ has $\deg_{\pm}(f_n)=2$ but $H^{\ast}(f_n) \geq c n$ for an absolute constant $c>0$.
- **unlocks**: `[[frontier:tchow_comparison], [open:first_core_question]]` by separating head complexity from ordinary threshold degree.

### Frontier update: quadratic PTF head separation

Promote `frontier:quadratic_ptf_head_separation` as the active counting-separation leaf. It should combine Lemma 19 with the fixed-degree PTF counting lower bound for degree $2$ to prove that some quadratic threshold functions have $H^{\ast}(f)\geq c n$ despite $\deg_{\pm}(f)=2$.

### Frontier update: quadratic PTF head separation

# frontier:quadratic_ptf_head_separation
- **status**: `done` as Lemma 20, [020_quadratic_ptf_head_separation.md](lemmas/01_foundations_and_normal_form/020_quadratic_ptf_head_separation.md)
- **uses**: `[[L11:one_head_characterization], [L19:warren_head_count_upper_bound]]`
- **unlocks**: `[[frontier:counting_separation], [frontier:tchow_comparison], [open:first_core_question]]`

This completes the quadratic counting separation: ordinary threshold degree can stay $2$ while $H^{\ast}$ grows linearly.

### Frontier refinement: unrestricted tangential-Chow counting bound

Add `frontier:tchow_warren_count_upper_bound` under `frontier:tchow_comparison`.

- **uses**: `[[L15:tangential_chow_reformulation], [L16:tchow_sandwich_lower_bound]]`
- **status**: `todo`
- **statement**: Use Warren's theorem on the unrestricted tangential-Chow parameterization to prove $\log_2 |\{f:\mathrm{tChow}_{\pm}(f)\leq H\}|\leq C H n(n+\log_2(H+1))$.
- **unlocks**: a quadratic-PTF separation for $\deg_{\pm}(f)$ versus $\mathrm{tChow}_{\pm}(f)$, completing the strictness of the lower inequality in the tangential-Chow sandwich.

### Frontier update: unrestricted tangential-Chow counting bound

# frontier:tchow_warren_count_upper_bound
- **status**: `done` as Lemma 21, [021_tchow_warren_count_upper_bound.md](lemmas/01_foundations_and_normal_form/021_tchow_warren_count_upper_bound.md)
- **uses**: `[[L15:tangential_chow_reformulation], [L16:tchow_sandwich_lower_bound]]`
- **unlocks**: `[[frontier:tchow_comparison], [frontier:quadratic_ptf_tchow_separation]]`

This records the Warren counting estimate for unrestricted tangential-Chow sign-representers and prepares the counting separation between $\deg_{\pm}$ and $\mathrm{tChow}_{\pm}$.

### Frontier refinement: quadratic PTF tangential-Chow separation\n\nAdd `frontier:quadratic_ptf_tchow_separation` under `frontier:tchow_comparison`.\n\n- **uses**: `[[L16:tchow_sandwich_lower_bound], [L21:tchow_warren_count_upper_bound]]` plus the standard fixed-degree PTF counting lower bound for degree $2$.\n- **status**: `todo`\n- **statement**: Prove that for all sufficiently large $n$ there is a quadratic threshold function $f_n : \{0,1\}^{n} \to \{0,1\}$ with $\deg_{\pm}(f_n)=2$ but $\mathrm{tChow}_{\pm}(f_n)\geq c n$ for an absolute constant $c>0$.\n- **unlocks**: `[[frontier:tchow_comparison], [open:first_core_question]]` by proving that unrestricted tangential-Chow complexity is already strictly finer than ordinary threshold degree.

### Frontier note: duplicate quadratic PTF head separation

# frontier:quadratic_ptf_head_separation
- **status**: `done` as Lemma 20, [020_quadratic_ptf_head_separation.md](lemmas/01_foundations_and_normal_form/020_quadratic_ptf_head_separation.md)
- **uses**: `[[L11:one_head_characterization], [L19:warren_head_count_upper_bound]]`
- **duplicate request**: `022_quadratic_ptf_head_separation.md` restates the same result, so no dependency edge changes.

### Frontier update: active quadratic PTF tangential-Chow separation

Promote `frontier:quadratic_ptf_tchow_separation` as the next leaf under `frontier:tchow_comparison`. Lemma 21 supplies the Warren counting upper bound for low $\mathrm{tChow}_{\pm}$ complexity, and the fixed-degree PTF counting lower bound for quadratic threshold functions should force a family with $\deg_{\pm}=2$ but $\mathrm{tChow}_{\pm}=\Omega(n)$.

### Frontier update: quadratic PTF tangential-Chow separation

# frontier:quadratic_ptf_tchow_separation
- **status**: `done` as Lemma 23, [023_quadratic_ptf_tchow_separation.md](lemmas/01_foundations_and_normal_form/023_quadratic_ptf_tchow_separation.md)
- **uses**: `[[L16:tchow_sandwich_lower_bound], [L21:tchow_warren_count_upper_bound]]`
- **unlocks**: `[[frontier:tchow_comparison], [open:first_core_question]]`

This completes the separation between ordinary threshold degree and unrestricted tangential-Chow complexity: $\deg_{\pm}$ can remain $2$ while $\mathrm{tChow}_{\pm}$ grows linearly.

### Frontier refinement: almost-all head lower bound

Add `frontier:almost_all_head_lower_bound` under `frontier:counting_separation`.

- **uses**: `[[L9:weighted_sum_upper_bound], [L19:warren_head_count_upper_bound]]`
- **status**: `todo`
- **statement**: Prove that almost all Boolean functions satisfy $H^{\ast}(f) = \Omega(2^n/n^2)$, and hence the worst-case value of $H^{\ast}$ lies between $\Omega(2^n/n^2)$ and $2^n-1$.
- **unlocks**: a near-tight global scale for head complexity and a benchmark for future explicit lower-bound certificates.

### Frontier update: quadratic PTF tangential-Chow separation

# frontier:quadratic_ptf_tchow_separation
- **status**: `done` as Lemma 23, [023_quadratic_ptf_tchow_separation.md](lemmas/01_foundations_and_normal_form/023_quadratic_ptf_tchow_separation.md)
- **uses**: `[[L16:tchow_sandwich_lower_bound], [L21:tchow_warren_count_upper_bound]]`
- **unlocks**: `[[frontier:tchow_comparison], [open:first_core_question]]`

This proves that the lower inequality $\deg_{\pm}(f)\leq\mathrm{tChow}_{\pm}(f)$ can be linearly strict, even for quadratic threshold functions.

### Frontier update: active almost-all head lower bound

Promote `frontier:almost_all_head_lower_bound` as the next counting-separation leaf. Lemma 19 supplies the low-head Warren counting upper bound, and Lemma 9 supplies the universal upper bound $H^{\ast}(f)\leq 2^n-1$, so this target should establish the generic scale $H^{\ast}(f)=\Omega(2^n/n^2)$ for almost all Boolean functions.

### Frontier update: almost-all head lower bound

# frontier:almost_all_head_lower_bound
- **status**: `done` as Lemma 24, [024_almost_all_head_lower_bound.md](lemmas/01_foundations_and_normal_form/024_almost_all_head_lower_bound.md)
- **uses**: `[[L19:warren_head_count_upper_bound], [L9:weighted_sum_upper_bound]]`
- **unlocks**: `[[frontier:counting_separation], [open:first_core_question]]`

### Frontier refinement: subcube restriction monotonicity

Add `frontier:subcube_restriction_monotonicity` under `frontier:lower_bound_certificates`.

- **uses**: `[[L10:linear_fractional_normal_form]]`
- **status**: `todo`
- **statement**: Prove that fixing any subset of input coordinates cannot increase $H^{\ast}$: for every subcube restriction $g$ of $f$, $H^{\ast}(g) \leq H^{\ast}(f)$.
- **unlocks**: explicit lower bounds for asymmetric families, especially address/indexing functions via parity restrictions.

# frontier:almost_all_head_lower_bound
- **status**: `done` as Lemma 25, [025_almost_all_head_lower_bound.md](lemmas/01_foundations_and_normal_form/025_almost_all_head_lower_bound.md)
- **uses**: `[[L19:warren_head_count_upper_bound], [L9:weighted_sum_upper_bound]]`
- **unlocks**: `[[frontier:counting_separation], [open:first_core_question]]`

### Frontier update: active subcube restriction monotonicity

Promote `frontier:subcube_restriction_monotonicity` as the next lower-bound-certificate leaf. Lemma 10 should make the proof direct: fixing coordinates in each linear-fractional one-head atom only changes the constants and preserves admissibility, so any representation of $f$ restricts to a representation of the subcube function with the same number of heads.

### Frontier update: subcube restriction monotonicity

# frontier:subcube_restriction_monotonicity
- **status**: `done` as Lemma 26, [026_subcube_restriction_monotonicity.md](lemmas/01_foundations_and_normal_form/026_subcube_restriction_monotonicity.md)
- **uses**: `[[L10:linear_fractional_normal_form]]`
- **unlocks**: `[[frontier:lower_bound_certificates], [frontier:address_indexing]]`

This records restriction monotonicity as a reusable lower-bound certificate: if a subcube restriction has complexity at least $r$, then the original function also has complexity at least $r$.

### Frontier update: subcube restriction monotonicity

# frontier:subcube_restriction_monotonicity
- **status**: `done` as Lemma 27, [027_subcube_restriction_monotonicity.md](lemmas/01_foundations_and_normal_form/027_subcube_restriction_monotonicity.md)
- **uses**: `[[L10:linear_fractional_normal_form]]`
- **unlocks**: `[[frontier:lower_bound_certificates], [frontier:address_indexing]]`

This records restriction monotonicity as a reusable lower-bound certificate: if a subcube restriction has complexity at least $r$, then the original function also has complexity at least $r$.

### Frontier refinement: indexing parity restriction lower bound

Add `frontier:address_indexing_parity_lower_bound` under `frontier:address_indexing`.

- **uses**: `[[L8:exact_parity_complexity], [L26:subcube_restriction_monotonicity]]`
- **status**: `todo`
- **statement**: For the indexing function $\mathrm{IND}_m(a,y)=y_a$, fixing the data table to any Boolean function $g$ restricts $\mathrm{IND}_m$ to $g$ on the address bits. Therefore $H^{\ast}(\mathrm{IND}_m)\geq \max_g H^{\ast}(g)$, and in particular $H^{\ast}(\mathrm{IND}_m)\geq m$ by choosing $g=\mathrm{XOR}_m$.
- **unlocks**: explicit asymmetric lower bounds and the next task of finding matching or improved upper bounds for indexing.

### Frontier update: indexing parity restriction lower bound

# frontier:address_indexing_parity_lower_bound
- **status**: `done` as Lemma 28, [028_address_indexing_parity_lower_bound.md](lemmas/01_foundations_and_normal_form/028_address_indexing_parity_lower_bound.md)
- **uses**: `[[L8:exact_parity_complexity], [L26:subcube_restriction_monotonicity]]`
- **also uses for the stronger consequence**: `[[L24:almost_all_head_lower_bound], [L25:almost_all_head_lower_bound]]`
- **unlocks**: `[[frontier:address_indexing]]`

### Frontier refinement: two-polarity sparse threshold density

Add `frontier:two_polarity_sparse_threshold_density_upper_bound` under `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L10:linear_fractional_normal_form], [L13:affine_atom_dictionary], [L18:same_polarity_sparse_threshold_density_upper_bound]]`
- **status**: `todo`
- **statement**: A strict signed threshold of $s$ coordinate-subcube indicators has $H^{\ast}\leq s$ when each term is anchored at either the all-zero or all-one vertex, with the polarity allowed to vary from term to term.
- **unlocks**: broader sparse threshold-density upper bounds and isolates the remaining hard case as subcube terms with mixed literals inside a single term.

### Frontier update: two-polarity sparse threshold density

# frontier:two_polarity_sparse_threshold_density_upper_bound
- **status**: `done` as Lemma 29, [029_two_polarity_sparse_threshold_density_upper_bound.md](lemmas/01_foundations_and_normal_form/029_two_polarity_sparse_threshold_density_upper_bound.md)
- **uses**: `[[L10:linear_fractional_normal_form], [L13:affine_atom_dictionary], [L18:same_polarity_sparse_threshold_density_upper_bound]]`
- **unlocks**: `[[frontier:calibrated_positive_sum_upper_bound]]`

This records the two-anchor extension: each subcube term may be anchored at $\vec 0$ or $\vec 1$, but all literals inside one term still have the same polarity.

### Frontier refinement: weighted-sum sign-change upper bound

Add `frontier:weighted_sum_sign_change_upper_bound` under `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L9:weighted_sum_upper_bound], [L10:linear_fractional_normal_form], [L11:one_head_characterization]]`
- **status**: `todo`
- **statement**: If $f(x)=F(t(x))$ for $t(x)=\sum_i\lambda_i x_i$ with all $\lambda_i>0$, then $H^{\ast}(f)$ is at most the number of sign changes of $F$ along the sorted image of $t$.
- **unlocks**: sharper positive weighted-sum upper bounds and sparse-support corollaries, while preserving the mixed-literal subcube problem as a separate frontier.

### Frontier update: weighted-sum sign-change upper bound

# frontier:weighted_sum_sign_change_upper_bound
- **status**: `done` as Lemma 30, [030_weighted_sum_sign_change_upper_bound.md](lemmas/01_foundations_and_normal_form/030_weighted_sum_sign_change_upper_bound.md)
- **uses**: `[[L10:linear_fractional_normal_form], [L11:one_head_characterization]]`
- **sharpens**: `[[L9:weighted_sum_upper_bound]]`
- **unlocks**: `[[frontier:calibrated_positive_sum_upper_bound]]`

This records the sign-change sharpening of the positive weighted-sum upper bound. Lemma 9 follows by the edge $C_t(F)\leq M-1$.

### Frontier refinement: irrelevant-variable invariance

Add `frontier:irrelevant_variable_invariance` under `frontier:lower_bound_certificates` and `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L10:linear_fractional_normal_form], [L26:subcube_restriction_monotonicity]]`
- **status**: `todo`
- **statement**: Prove that adding dummy input coordinates does not change $H^{\ast}$, and record the companion invariances under coordinate permutations and Boolean complement.
- **unlocks**: junta upper bounds, active-variable versions of Lemmas 9 and 30, and cleaner ambient-dimension handling for indexing and sparse-function upper bounds.

### Frontier update: irrelevant-variable invariance

# frontier:irrelevant_variable_invariance
- **status**: `done` as Lemma 31, [031_irrelevant_variable_invariance.md](lemmas/01_foundations_and_normal_form/031_irrelevant_variable_invariance.md)
- **uses**: `[[L10:linear_fractional_normal_form], [L13:affine_atom_dictionary], [L26:subcube_restriction_monotonicity]]`
- **unlocks**: `[[frontier:lower_bound_certificates], [frontier:calibrated_positive_sum_upper_bound], [frontier:address_indexing]]`

This records invariance under dummy coordinates, coordinate permutations, and Boolean output complement, while excluding input-bit negation.

### Frontier refinement: active-junta weighted-sum upper bound

Add `frontier:active_junta_weighted_sum_upper_bound` under `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L30:weighted_sum_sign_change_upper_bound], [L31:irrelevant_variable_invariance]]`
- **status**: `todo`
- **statement**: If $f$ depends only on active coordinates $I$ and the induced junta is a sign-change function of a positive weighted sum on $I$, then $H^{\ast}(f)$ is at most that active sign-change count. In particular every $k$-junta has $H^{\ast}(f)\leq 2^k-1$.
- **unlocks**: active-variable versions of the weighted-sum upper bounds and ambient-dimension-free junta estimates.

### Frontier update: active-junta weighted-sum upper bound

# frontier:active_junta_weighted_sum_upper_bound
- **status**: `done` as Lemma 32, [032_active_junta_weighted_sum_upper_bound.md](lemmas/01_foundations_and_normal_form/032_active_junta_weighted_sum_upper_bound.md)
- **uses**: `[[L30:weighted_sum_sign_change_upper_bound], [L31:irrelevant_variable_invariance]]`
- **unlocks**: `[[frontier:calibrated_positive_sum_upper_bound]]`

This records the active-variable form of the weighted-sum sign-change upper bound and the ambient-dimension-free estimate $H^{\ast}(f)\leq 2^k-1$ for $k$-juntas.

### Frontier refinement: active-junta support-size upper bound

Add `frontier:active_junta_support_size_upper_bound` under `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L32:active_junta_weighted_sum_upper_bound]]`
- **status**: `todo`
- **statement**: If $f$ depends only on $k$ active variables and the induced active truth table has $a$ ones and $b=2^k-a$ zeros, then $H^{\ast}(f)\leq \min\{2a,2b,2^k-1\}$.
- **unlocks**: sharper sparse and cosparse junta upper bounds, and a support-size benchmark for asymmetric functions.

### Frontier update: active-junta support-size upper bound

# frontier:active_junta_support_size_upper_bound
- **status**: `done` as Lemma 33, [033_active_junta_support_size_upper_bound.md](lemmas/01_foundations_and_normal_form/033_active_junta_support_size_upper_bound.md)
- **uses**: `[[L32:active_junta_weighted_sum_upper_bound]]`
- **unlocks**: `[[frontier:calibrated_positive_sum_upper_bound]]`

This records the support-size sharpening $H^{\ast}(f)\leq\min\{2a,2b,2^k-1\}$ for active $k$-juntas, giving $H^{\ast}(f)\leq 2r$ for sparse or cosparse active truth tables.

### Frontier refinement: positive Boolean minor monotonicity

Add `frontier:positive_minor_monotonicity` under `frontier:lower_bound_certificates`.

- **uses**: `[[L10:linear_fractional_normal_form], [L31:irrelevant_variable_invariance]]`
- **status**: `todo`
- **statement**: If $g$ is obtained from $f$ by fixing coordinates, permuting coordinates, duplicating coordinates, or identifying coordinates, without coordinate negations, then $H^{\ast}(g) \leq H^{\ast}(f)$.
- **unlocks**: stronger minor-based lower-bound certificates for explicit nonsymmetric families.

### Frontier update: positive Boolean minor monotonicity

# frontier:positive_minor_monotonicity
- **status**: `done` as Lemma 34, [034_positive_minor_monotonicity.md](lemmas/01_foundations_and_normal_form/034_positive_minor_monotonicity.md)
- **uses**: `[[L10:linear_fractional_normal_form], [L31:irrelevant_variable_invariance]]`
- **unlocks**: `[[frontier:lower_bound_certificates]]`

This records monotonicity under positive Boolean minors: fixing, permuting, duplicating, identifying coordinates, and adding unused coordinates cannot increase $H^{\ast}$.

### Frontier refinement: homogeneous-polarity minor monotonicity

Add `frontier:homogeneous_polarity_minor_monotonicity` under `frontier:lower_bound_certificates`.

- **uses**: `[[L10:linear_fractional_normal_form], [L34:positive_minor_monotonicity]]`
- **status**: `todo`
- **statement**: Prove that simultaneous complement of all input coordinates preserves $H^{\ast}$, and hence Boolean minors of one uniform polarity, all unnegated or all negated, cannot increase head complexity.
- **unlocks**: stronger restriction and minor certificates while keeping separate the genuinely hard case of mixed input negations.

### Frontier update: homogeneous-polarity minor monotonicity

# frontier:homogeneous_polarity_minor_monotonicity
- **status**: `done` as Lemma 35, [035_homogeneous_polarity_minor_monotonicity.md](lemmas/01_foundations_and_normal_form/035_homogeneous_polarity_minor_monotonicity.md)
- **uses**: `[[L10:linear_fractional_normal_form], [L34:positive_minor_monotonicity]]`
- **unlocks**: `[[frontier:lower_bound_certificates]]`

This records invariance under simultaneous input complement and monotonicity under homogeneous-polarity Boolean minors, while keeping mixed input negations as the remaining boundary.

### Frontier refinement: coordinate subcube one-head exactness

Add `frontier:coordinate_subcube_one_head_exact` under `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L11:one_head_characterization]]`
- **status**: `todo`
- **statement**: Every nontrivial coordinate subcube indicator, equivalently every conjunction of arbitrary signed literals, has $H^{\ast}=1$, while the empty conjunction is constant and has $H^{\ast}=0$.
- **unlocks**: isolates the remaining mixed-literal DNF problem as a calibration and aggregation problem, since individual mixed-polarity subcube terms are already one-head functions.

### Frontier update: coordinate subcube one-head exactness

# frontier:coordinate_subcube_one_head_exact
- **status**: `done` as Lemma 36, [036_coordinate_subcube_one_head_exact.md](lemmas/01_foundations_and_normal_form/036_coordinate_subcube_one_head_exact.md)
- **uses**: `[[L11:one_head_characterization]]`
- **unlocks**: `[[frontier:calibrated_positive_sum_upper_bound]]`

This records that each individual mixed-literal coordinate subcube indicator is already exactly one head when nontrivial; the remaining mixed-literal DNF work is calibration and aggregation.

### Frontier refinement: mixed-literal DNF upper bound

Add `frontier:mixed_literal_dnf_upper_bound` under `frontier:calibrated_positive_sum_upper_bound`.

- **uses**: `[[L13:affine_atom_dictionary], [L36:coordinate_subcube_one_head_exact]]`
- **status**: `todo`
- **statement**: Any $s$-term DNF of arbitrary signed coordinate-subcube indicators satisfies $H^{\ast}(f)\leq s$ by constructing one calibrated one-head bump per subcube and thresholding their sum.
- **unlocks**: full sparse DNF upper bounds beyond the same-polarity and two-anchor cases, and prepares the general sparse threshold-density aggregation target.
