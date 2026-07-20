# Lemmas Toward The First Core Question

## Goal

We want a step-by-step route to the first core question in [problem_statement.md](problem_statement.md):

> Can $H^{\ast}(f)$ be expressed, exactly or approximately, in terms of a known invariant of $f$?

This file is the statement ledger. It records the current lemma statements, how they fit together, and where each proof lives under `lemmas/`.

For nearby literature and context, see [literature_survey.md](literature_survey.md).

## Current Status

The main-branch lemma stack uses the numbered foundation files in `lemmas/01_foundations_and_normal_form/` (Lemmas 1 to 12, Lean-verified) plus the autonomous-run extensions in `lemmas/02_upper_bounds/`, `lemmas/03_lower_bounds/`, and `lemmas/04_closure_and_structure/` (Lemmas 13 and up, verified by the informal-prover oracle).

These notes give: the linear-fractional normal form (L10) and atom dictionary (L13); the exact cleared-denominator (tangential-Chow) invariant $H^{\ast} = \mathrm{MFdeg}_{\pm}$ (L16); the sandwich $\deg_{\pm} \leq \mathrm{tChow}_{\pm} \leq H^{\ast} \leq M_{+}-1$ (L18, L9); the exact 0/1-head and symmetric characterizations (L11, L12); upper-bound routes (weighted sum L9, monotone-term DNF L14, calibrated interpolation L19, sparse threshold density L20, weighted-score sign changes L25, the simple alternation invariant $A_{+}$ L26); lower-bound routes (threshold degree L6, restriction/planted parity L17, flattening sign-rank L22, Warren counting L23); structural closures (L15, L21, L28); and the partial answer to the positivity (F4) question (free at level 1, symmetric, and wherever $\deg_{\pm} = H^{\ast}$: L30, L31, L32).

Headline results: **$H^{\ast}$ is strictly finer than threshold degree** (L23/L24), so it is a genuinely new measure; the **simple L12-style characterization** is $A_{+}$ (min positive-order alternation, exact for symmetric); **positivity is free wherever $\deg_{\pm} = H^{\ast}$** and empirically everywhere. The stack still does **not** give an exact closed-form characterization of $H^{\ast}(f)$ for general nonsymmetric $f$; see `claude-comments/h_star_knowledge_map.md` for the full map and open problems.

## Main Lemma Stack

### Lemma 1. One-head two-coordinate restrictions split additively

Fix a single-head model and freeze all but two input coordinates. Then the softmax numerator and denominator at the query token can be written as

$$ N(a,b) = A(a) + B(b) + C, \qquad D(a,b) = \alpha(a) + \beta(b) + \gamma $$

for suitable functions $A, B, \alpha, \beta$ and constants $C, \gamma$.

**Proof.** [lemmas/01_foundations_and_normal_form/001_checkerboard_additive_decomposition.md](lemmas/01_foundations_and_normal_form/001_checkerboard_additive_decomposition.md)

### Lemma 2. Antipode identities on a restricted 2-cube

Under the same setup,

$$ N(0,0) + N(1,1) = N(0,1) + N(1,0) $$

and

$$ D(0,0) + D(1,1) = D(0,1) + D(1,0). $$

**Proof.** [lemmas/01_foundations_and_normal_form/002_antipode_identities.md](lemmas/01_foundations_and_normal_form/002_antipode_identities.md)

### Lemma 3. Checkerboard obstruction for one head

If $f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$ has a 2-bit checkerboard restriction, then

$$ H^{\ast}(f) \geq 2. $$

> **Equivalently.** One head cannot separate one diagonal of a restricted 2-cube from the other diagonal.

**Proof.** [lemmas/01_foundations_and_normal_form/003_checkerboard_obstruction.md](lemmas/01_foundations_and_normal_form/003_checkerboard_obstruction.md)

### Lemma 4. One head computes every symmetric threshold

For

$$ T_{n,t}(x) = \mathbf{1} \left[ \lvert x\rvert \geq t \right], \qquad 1 \leq t \leq n, $$

where $\lvert x\rvert$ is the Hamming weight of $x$, namely the number of coordinates of $x$ equal to $1$.

we have

$$ H^{\ast}(T_{n,t}) = 1. $$

In particular,

$$ H^{\ast}(\mathrm{OR}_n) = H^{\ast}(\mathrm{AND}_n) = H^{\ast}(\mathrm{MAJORITY}_n) = 1. $$

**Proof.** [lemmas/01_foundations_and_normal_form/004_symmetric_thresholds.md](lemmas/01_foundations_and_normal_form/004_symmetric_thresholds.md)

### Lemma 5. Family consequences from the checkerboard obstruction

For $n \geq 2$,

$$ H^{\ast}(\mathrm{PARITY}_n) \geq 2. $$

For $1 \leq k \leq n - 1$,

$$ H^{\ast}(\mathrm{EXACT}_{n,k}) \geq 2. $$

Together with Lemma 4, this gives a first split inside symmetric functions:

- monotone symmetric thresholds have head complexity $1$,
- parity and internal exact-count predicates need at least $2$ heads.

**Proof.** [lemmas/01_foundations_and_normal_form/005_family_consequences.md](lemmas/01_foundations_and_normal_form/005_family_consequences.md)

### Lemma 6. Threshold degree is bounded by head complexity

If a Boolean function $f$ is computable in the model from [model.md](model.md), then

$$ \deg_{\pm}(f) \leq H^{\ast}(f). $$

Here $\deg_{\pm}(f)$ denotes the threshold degree of $f$, namely the minimum degree of a real polynomial that sign-represents $f$ on the Boolean cube.

**Proof.** [lemmas/01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md](lemmas/01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md)

### Lemma 7. Parity has threshold degree exactly n

For

$$ \mathrm{PARITY}_n(x) = x_1 \oplus \cdots \oplus x_n, $$

we have

$$ \deg_{\pm}(\mathrm{PARITY}_n) = n. $$

**Proof.** [lemmas/01_foundations_and_normal_form/007_parity_threshold_degree.md](lemmas/01_foundations_and_normal_form/007_parity_threshold_degree.md)

### Lemma 8. Exact parity complexity

For every $n \geq 1$,

$$ H^{\ast}(\mathrm{XOR}_n) = n. $$

> **Equivalently.** In this one-layer attention model, parity needs exactly one head per input bit.

**Proof.** [lemmas/01_foundations_and_normal_form/008_exact_parity_complexity.md](lemmas/01_foundations_and_normal_form/008_exact_parity_complexity.md)

### Lemma 9. Weighted-sum interpolation upper bound

Suppose there exist positive real numbers

$$ \lambda_1, \ldots, \lambda_n > 0 $$

and a function

$$ F : \mathrm{Im}(t) \to \lbrace0,1\rbrace, $$

where

$$ t(x) = \sum_{i=1}^{n} \lambda_i x_i, $$

such that

$$ f(x) = F(t(x)). $$

Let

$$ M := \lvert\mathrm{Im}(t)\rvert. $$

Then

$$ H^{\ast}(f) \leq M - 1. $$

In particular:

- every symmetric Boolean function satisfies $H^{\ast}(f) \leq n$,
- every Boolean function satisfies $H^{\ast}(f) \leq 2^n - 1$.

**Proof.** [lemmas/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md](lemmas/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md)

### Lemma 10. Exact linear-fractional normal form

Define a one-head atom to be a function of the form

$$ \phi(x) = \frac{ \eta + \sum_{i=1}^{n} \rho_i \alpha^{x_i}(m_i + \delta x_i) }{ \gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i} }, $$

where

$$ \gamma > 0, \qquad \rho_1, \ldots, \rho_n > 0, \qquad \alpha > 0. $$

Let $L_{\mathrm{frac}}(f)$ be the least $H$ such that $f$ is computed by thresholding a constant plus a sum of $H$ such atoms. Then

$$ H^{\ast}(f) = L_{\mathrm{frac}}(f). $$

> **Interpretation.** The exact model-native invariant is the minimum number of one-head linear-fractional atoms needed before the final threshold.

**Proof.** [lemmas/01_foundations_and_normal_form/010_linear_fractional_normal_form.md](lemmas/01_foundations_and_normal_form/010_linear_fractional_normal_form.md)

### Lemma 11. Exact one-head characterization

The first two levels of head complexity are:

$$ H^{\ast}(f) = 0 \qquad \Longleftrightarrow \qquad f \text{ is constant}, $$

and

$$ H^{\ast}(f) = 1 \qquad \Longleftrightarrow \qquad f \text{ is a nonconstant linear threshold function}. $$

In particular, every non-linear-threshold Boolean function has

$$ H^{\ast}(f) \geq 2. $$

This strictly strengthens the checkerboard obstruction as a one-head lower bound.

**Proof.** [lemmas/01_foundations_and_normal_form/011_one_head_characterization.md](lemmas/01_foundations_and_normal_form/011_one_head_characterization.md)

### Lemma 12. Exact symmetric sign-change characterization

Let $f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$ be symmetric, so

$$ f(x) = F(\lvert x\rvert) $$

for some

$$ F : \lbrace0,\ldots,n\rbrace \to \lbrace0,1\rbrace. $$

Define

$$ \sigma_k := \begin{cases} +1 & \text{if } F(k) = 1, \\ -1 & \text{if } F(k) = 0, \end{cases} $$

and let $C(F)$ be the number of indices $t \in \lbrace1,\ldots,n\rbrace$ with

$$ \sigma_{t-1} \neq \sigma_t. $$

Then

$$ H^{\ast}(f) = C(F). $$

> **Interpretation.** For symmetric functions, one head buys exactly one sign change along the Hamming-weight axis.

In particular:

- monotone symmetric thresholds have $H^{\ast} = 1$,
- parity has $H^{\ast}(\mathrm{XOR}_n) = n$,
- internal exact-count predicates have $H^{\ast}(\mathrm{EXACT}_{n,k}) = 2$ for $1 \leq k \leq n - 1$.

**Proof.** [lemmas/01_foundations_and_normal_form/012_symmetric_sign_changes.md](lemmas/01_foundations_and_normal_form/012_symmetric_sign_changes.md)

### Lemma 13. Atom dictionary

Every one-head atom equals $N/D$ with $N, D$ affine, $D$ positive on the cube, and the slopes of $D$ all of one common sign (the sign of $\alpha - 1$). Conversely, for any affine $N$ and any affine $D$ positive on the cube with all slopes strictly of one common sign, $N/D$ is a one-head atom. Hence the one-head atoms with no zero denominator slope are exactly the affine ratios with a one-sided strictly-monotone positive denominator.

**Proof.** [lemmas/01_foundations_and_normal_form/013_atom_dictionary.md](lemmas/01_foundations_and_normal_form/013_atom_dictionary.md)

### Lemma 14. Monotone-term DNF upper bound

If $f$ is an OR of $s$ monotone terms (each term a conjunction of literals of a single polarity), then

$$ H^{\ast}(f) \leq s. $$

In particular every monotone Boolean function has $H^{\ast}(f) \leq$ (its number of prime implicants).

**Proof.** [lemmas/02_upper_bounds/014_monotone_term_dnf.md](lemmas/02_upper_bounds/014_monotone_term_dnf.md)

### Lemma 15. Negation and permutation closure

For every $f$, $H^{\ast}(1 - f) = H^{\ast}(f)$, and $H^{\ast}(f^{\pi}) = H^{\ast}(f)$ for every input permutation $\pi$.

**Proof.** [lemmas/04_closure_and_structure/015_negation_permutation_closure.md](lemmas/04_closure_and_structure/015_negation_permutation_closure.md)

### Lemma 16. Cleared-denominator (tangential) sign-rank

Define $\mathrm{MFdeg}_{\pm}(f)$ as the least $H$ for which $f$ is sign-represented by a polynomial

$$ P(x) = \theta \prod_{h=1}^{H} D_h(x) + \sum_{h=1}^{H} N_h(x) \prod_{g \neq h} D_g(x) $$

with each $(N_h, D_h)$ an admissible affine pair ($D_h$ positive on the cube with one-sided slopes, $N_h$ arbitrary affine). Then

$$ H^{\ast}(f) = \mathrm{MFdeg}_{\pm}(f). $$

Equivalently, $H^{\ast}(f)$ is the least degree of a sign-representing polynomial that is a tangent vector, at a product of $H$ one-sided positive affine forms, to the variety of products of $H$ affine forms. This recovers $\deg_{\pm}(f) \leq H^{\ast}(f)$ and is the sharp restatement of the gap to ordinary threshold degree.

**Proof.** [lemmas/01_foundations_and_normal_form/016_cleared_denominator_invariant.md](lemmas/01_foundations_and_normal_form/016_cleared_denominator_invariant.md)

### Lemma 17. Restriction monotonicity

Fixing any coordinate cannot increase head complexity: for every $f$, coordinate $k$, and value $c_0$,

$$ H^{\ast}\big(f|_{x_k = c_0}\big) \leq H^{\ast}(f). $$

Iterating, any sub-cube restriction $g$ of $f$ has $H^{\ast}(g) \leq H^{\ast}(f)$. Consequently a planted $\mathrm{XOR}_m$ restriction forces $H^{\ast}(f) \geq m$ (the checkerboard obstruction is $m = 2$).

**Proof.** [lemmas/03_lower_bounds/017_restriction_monotonicity.md](lemmas/03_lower_bounds/017_restriction_monotonicity.md)

### Lemma 18. Tangential-Chow sandwich

Let $\mathrm{tChow}_{\pm}(f)$ be the least $H$ for which $f$ is sign-represented by $\theta \prod_h D_h + \sum_h N_h \prod_{g \neq h} D_g$ with $N_h, D_h$ arbitrary affine (no positivity). Then

$$ \deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{\ast}(f). $$

Head complexity equals the same tangential-Chow rank with the attention constraints that each $D_h$ be positive on the cube with one-sided slopes; those constraints are the whole gap to the unconstrained algebraic invariant.

**Proof.** [lemmas/01_foundations_and_normal_form/018_tchow_sandwich.md](lemmas/01_foundations_and_normal_form/018_tchow_sandwich.md)

### Lemma 19. Calibrated positive-weighted-sum interpolation

For $t(x) = \sum_i \lambda_i x_i$ with $\lambda_i > 0$ and $M = \lvert\mathrm{Im}(t)\rvert$, every real table $G : \mathrm{Im}(t) \to \mathbb{R}$ is exactly $a_0 + \sum_{j=1}^{M-1} \psi_j(x)$ for one-head atoms $\psi_j$ (Cauchy-kernel interpolation). Hence calibrated decompositions $f = \mathbf{1}[\theta + \sum_r a_r G_r(t_r(x)) > 0]$ satisfy

$$ H^{\ast}(f) \leq \sum_r \big(\lvert\mathrm{Im}(t_r)\rvert - 1\big). $$

**Proof.** [lemmas/02_upper_bounds/019_calibrated_interpolation.md](lemmas/02_upper_bounds/019_calibrated_interpolation.md)

### Lemma 20. Sparse single-polarity threshold-density upper bound

If $f(x) = 1 \iff \theta + \sum_{j=1}^s c_j \mathbf{1}_{T_j}(x) > 0$ with each $T_j$ a single-polarity subcube and a strict margin, then

$$ H^{\ast}(f) \leq s. $$

This generalizes the monotone-term DNF bound (Lemma 14) to arbitrary real coefficients via uniformly-approximating calibrated bumps.

**Proof.** [lemmas/02_upper_bounds/020_sparse_threshold_density.md](lemmas/02_upper_bounds/020_sparse_threshold_density.md)

### Lemma 21. Junta invariance

If $f(x) = g(x_1,\dots,x_k)$ depends only on the first $k$ coordinates, then

$$ H^{\ast}(f) = H^{\ast}(g). $$

Head complexity depends only on the relevant variables; padding with irrelevant coordinates changes nothing.

**Proof.** [lemmas/04_closure_and_structure/021_junta_invariance.md](lemmas/04_closure_and_structure/021_junta_invariance.md)

### Lemma 22. Flattening (sign-rank) lower bound

For every bipartition $A | B$ of the coordinates,

$$ \mathrm{sr}_{A|B}(f) \leq \big(H^{\ast}(f)+1\big)\,2^{H^{\ast}(f)} + 1, \qquad\text{hence}\qquad H^{\ast}(f) = \Omega\big(\log \mathrm{sr}_{A|B}(f)\big), $$

where $\mathrm{sr}_{A|B}(f)$ is the sign-rank of $f$ across the cut. This is the first $H^{\ast}$ lower bound that does not pass through threshold degree (a product of $H$ affine forms has cut-rank $\leq 2^{H}$), and it certifies $H^{\ast}(f) > \deg_{\pm}(f)$ whenever the sign-rank is super-polynomial in the threshold-degree monomial count.

**Proof.** [lemmas/03_lower_bounds/022_flattening_lower_bound.md](lemmas/03_lower_bounds/022_flattening_lower_bound.md)

### Lemma 23. Counting separation from threshold degree

The number of $H$-head functions is small, $\#\lbrace f : H^{\ast}(f) \leq H\rbrace \leq 2^{O(Hn^2)}$ (Warren over the $O(Hn)$ cleared-form parameters). Against the $2^{\Theta(n^3)}$ degree-2 polynomial threshold functions (Baldi-Vershynin), this forces a separation: for large $n$ there is $f$ with

$$ \deg_{\pm}(f) \leq 2 \qquad\text{and}\qquad H^{\ast}(f) = \Omega(n). $$

So $H^{\ast}$ is not bounded by any function of $\deg_{\pm}$; head complexity is a strictly finer measure than threshold degree. (Uses Warren 1968 and Baldi-Vershynin 2019 as external inputs; the novel content is the reduction. Nonconstructive.)

**Proof.** [lemmas/03_lower_bounds/023_counting_separation.md](lemmas/03_lower_bounds/023_counting_separation.md)

### Lemma 24. Positivity is not the source of the separation

The counting bound holds without positivity: $\#\lbrace f : \mathrm{tChow}_{\pm}(f) \leq H\rbrace \leq 2^{O(Hn^2)}$, so some $\deg_{\pm}=2$ function has $\mathrm{tChow}_{\pm}(f)=\Omega(n)$, hence $H^{\ast}(f)=\Omega(n)$. The $\deg_{\pm}$-to-$H^{\ast}$ separation already appears at the positivity-free tangential-Chow level; the attention positivity/one-sided constraints are not its cause (relevant to the open F4 question of whether positivity adds any further cost).

**Proof.** [lemmas/03_lower_bounds/024_tchow_separation.md](lemmas/03_lower_bounds/024_tchow_separation.md)

### Lemma 25. Sign-change upper bound for functions of one positive weighted sum

If $f(x) = F(t(x))$ for a positive weighted sum $t = \sum_i w_i x_i$ ($w_i > 0$), and $C(F)$ is the number of sign changes of $F$ along the increasing values of $t$, then

$$ H^{\ast}(f) \leq C(F). $$

Generalizes the symmetric sign-change result (L12) from equal to arbitrary positive weights, via a partial-fraction (Cauchy-kernel) construction. The matching lower bound holds only for equal weights; for unequal weights $C(F)$ can vastly overcount (a dictator has $C(F) = 2^n - 1$ but $H^{\ast} = 1$).

**Proof.** [lemmas/02_upper_bounds/025_weighted_score_upper.md](lemmas/02_upper_bounds/025_weighted_score_upper.md)

### Lemma 26. Minimized positive-order alternation number (simple characterization)

Let $A_{+}(f) = \min_{w > 0 \text{ generic}}$ (number of times $f$ alternates along the order of the cube by $t_w = \sum_i w_i x_i$). Then

$$ H^{\ast}(f) \leq A_{+}(f), \qquad\text{and}\qquad A_{+}(f) = C(F) = H^{\ast}(f) \text{ for symmetric } f. $$

So $A_{+}$ is a simple, computable, L12-style invariant: the minimum number of alternations of $f$ along a positive linear ordering of the cube. It upper-bounds $H^{\ast}$ in general and equals it for symmetric functions. With $\deg_{\pm}(f) \leq H^{\ast}(f) \leq A_{+}(f)$, the three coincide whenever $\deg_{\pm}(f) = A_{+}(f)$ (the broadest class on which the simple invariant is exact). $A_{+}$ is *not* exact for general $f$ (the free numerator lets one head realize any mixed-sign LTF), and no linear-order alternation count equals $H^{\ast}$ in general; the exact invariant is the tangential-Chow rank (L16).

**Proof.** [lemmas/02_upper_bounds/026_alternation_upper_bound.md](lemmas/02_upper_bounds/026_alternation_upper_bound.md)

### Lemma 27. A 2-by-2 intersection function has $H^{\ast} = 2$

$f = (x_1 \wedge x_2) \vee (x_3 \wedge x_4)$ satisfies $H^{\ast}(f) = 2$ (upper by L14, lower by non-LTF via a weighted-threshold infeasibility). A concrete nonsymmetric monotone exact value; the $s=2$ case of $\neg\mathrm{DISJ}_s$.

**Proof.** [lemmas/02_upper_bounds/027_intersection2_exact.md](lemmas/02_upper_bounds/027_intersection2_exact.md)

### Lemma 28. Full-input complement invariance

For $f^{c}(x) := f(\mathbf{1} - x)$, $H^{\ast}(f^{c}) = H^{\ast}(f)$. Complementing all inputs is free (global $0 \leftrightarrow 1$ symmetry, via $\alpha \mapsto 1/\alpha$ uniformly). Single-bit-negation invariance is a separate open question (it holds for $n \leq 4$ and would follow from $\mathrm{tChow}_{\pm} = H^{\ast}$); the monotone bias only obstructs the naive same-atom proof.

**Proof.** [lemmas/04_closure_and_structure/028_full_complement_invariance.md](lemmas/04_closure_and_structure/028_full_complement_invariance.md)

### Lemma 29. Flattening bound holds without positivity

$\mathrm{sr}_{A|B}(f) \leq (\mathrm{tChow}_{\pm}(f)+1)\,2^{\mathrm{tChow}_{\pm}(f)} + 1$, hence $\mathrm{tChow}_{\pm}(f) = \Omega(\log \mathrm{sr}_{A|B}(f))$. The sign-rank obstruction bounds even the positivity-free invariant (L22's argument never uses positivity), like the counting separation (L24).

**Proof.** [lemmas/03_lower_bounds/029_tchow_flattening.md](lemmas/03_lower_bounds/029_tchow_flattening.md)

### Lemma 30. Positivity is free at level one

$\mathrm{tChow}_{\pm}(f) \leq 1 \iff H^{\ast}(f) \leq 1 \iff f$ is constant or an LTF, so $\mathrm{tChow}_{\pm}(f) = H^{\ast}(f)$ when either is $\leq 1$. The rigorous base case of "do the positivity constraints ever cost a head?" (answer at level one: no).

**Proof.** [lemmas/01_foundations_and_normal_form/030_tchow_level1.md](lemmas/01_foundations_and_normal_form/030_tchow_level1.md)

### Lemma 31. Positivity is free for symmetric functions

For symmetric $f$, $\mathrm{tChow}_{\pm}(f) = H^{\ast}(f) = \deg_{\pm}(f) = C(F)$ (the sandwich collapses since L12 gives $\deg_{\pm} = H^{\ast} = C(F)$). So positivity costs nothing on the whole symmetric class, extending the level-one base case (L30).

**Proof.** [lemmas/01_foundations_and_normal_form/031_tchow_symmetric.md](lemmas/01_foundations_and_normal_form/031_tchow_symmetric.md)

### Lemma 32. Positivity can only cost where $H^{\ast} > \deg_{\pm}$

If $\deg_{\pm}(f) = H^{\ast}(f)$ then $\mathrm{tChow}_{\pm}(f) = H^{\ast}(f)$ (sandwich collapse). So any F4 gap $\mathrm{tChow}_{\pm} < H^{\ast}$ requires a strict separation $\deg_{\pm} < H^{\ast}$; positivity is free on constants, LTFs, symmetric functions, and parity. Subsumes L30 and L31.

**Proof.** [lemmas/01_foundations_and_normal_form/032_tchow_collapse.md](lemmas/01_foundations_and_normal_form/032_tchow_collapse.md)

### Lemma 33. An explicit function separating head complexity from threshold degree

For the set-intersection function $\mathrm{INT}_n(x,y) = \bigvee_{i=1}^n (x_i \wedge y_i)$ on $2n$ bits: $\deg_{\pm}(\mathrm{INT}_n) = 2$ for $n \geq 2$, and $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$ (a self-contained homogeneous-shattering / VC argument). Hence by the flattening bound (L22), $n \geq 14$ forces $H^{\ast}(\mathrm{INT}_n) \geq 3 > 2 = \deg_{\pm}$. The first explicit (non-counting, non-numerical) separation, on a named function; positivity-free via L29, superseding the numerical $\neg\mathrm{DISJ}_4$ candidate.

**Proof.** [lemmas/03_lower_bounds/033_int_explicit_separation.md](lemmas/03_lower_bounds/033_int_explicit_separation.md)

### Lemma 34. An explicit unbounded separation

$H^{\ast}(\mathrm{INT}_n) \geq \tfrac12\log_2 n$ for $n \geq 6$ (from $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$ and $(H{+}1)2^H{+}1 \leq 4^H$ for $H \geq 2$). Since $\deg_{\pm}(\mathrm{INT}_n) = 2$ always, the gap diverges: an explicit family with $H^{\ast} \to \infty$ at threshold degree $2$. Moreover $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \in \lbrace n, n+1\rbrace$ (the rank-$(n{+}1)$ matrix $\sum_i x_iy_i - \tfrac12$ sign-represents), so flattening is pinned at $\Theta(\log n)$; a polynomial explicit gap needs a non-flattening obstruction.

**Proof.** [lemmas/03_lower_bounds/034_int_logarithmic_separation.md](lemmas/03_lower_bounds/034_int_logarithmic_separation.md)

### Lemma 35. A near-linear lower bound on the head complexity of set intersection

$H^{\ast}(\mathrm{INT}_n) \geq \mathrm{tChow}_{\pm}(\mathrm{INT}_n) \geq c\,n/\log_2 n$ for an absolute $c>0$ and large $n$. Proved by a non-flattening obstruction: on the singleton-column slice ($x = \mathbf 1_S$, $y = e_j$) the row $\mathbf 1_S$ acts through only $2H{+}1$ parameters $(\theta, \alpha_{h,S}, \beta_{h,S})$ via a degree-$(H{+}1)$ map, yet must shatter $n$ columns, so Warren forces $2^n \leq (C(H{+}1)n/(2H{+}1))^{2H+1}$. Positivity-free; supersedes L34's $\Omega(\log n)$ and gives the first explicit polynomial (near-linear) separation from threshold degree, nearly matching the nonconstructive $\Omega(n)$ of L23/L24. With $H^{\ast} \leq n$ (L14), $H^{\ast}(\mathrm{INT}_n) = \widetilde{\Theta}(n)$.

**Proof.** [lemmas/03_lower_bounds/035_int_nearlinear_lower.md](lemmas/03_lower_bounds/035_int_nearlinear_lower.md)

### Lemma 36. Head complexity of a disjoint monotone DNF equals its term count up to a log factor

For $f = \bigvee_{r=1}^s T_r$ with $T_r$ monotone ANDs on pairwise-disjoint blocks of width $\geq 2$: $H^{\ast}(f) \geq \mathrm{tChow}_{\pm}(f) \geq c\,s/\log_2 s$. With $H^{\ast}(f) \leq s$ (L14), $H^{\ast}(f) = \widetilde{\Theta}(s)$. Same singleton-column Warren technique as L35, generalized: pivot + rest per block, row $S$ sets the rests (additively, needs width $\geq 2$), column $j$ sets pivot $j$, so $f(z_{S,j}) = [j\in S]$ shatters $s$ columns through $2H{+}1$ parameters. Positivity-free; pins an entire nonsymmetric family (after symmetric, L12), pairing L14's upper bound with a matching lower bound.

**Proof.** [lemmas/03_lower_bounds/036_disjoint_dnf_lower.md](lemmas/03_lower_bounds/036_disjoint_dnf_lower.md)

### Lemma 37. A reusable head-complexity lower bound from a shatter-rectangle

If $g$ admits a **shatter-rectangle of order $s$** — a coordinate partition $[N] = V_{\mathrm{row}} \sqcup V_{\mathrm{col}}$ and assignments $\rho_S, \kappa_j$ with $g(\rho_S, \kappa_j) = [j\in S]$ for all $S\subseteq[s]$, $j\in[s]$ — then $H^{\ast}(g) \geq \mathrm{tChow}_{\pm}(g) \geq c\,s/\log_2 s$. Abstracts the L35/L36 technique into a tool: the row acts through $2H{+}1$ parameters (any affine form splits into an $S$-part plus a $j$-part across the partition) yet must shatter $s$ columns, so Warren applies. Purely combinatorial hypothesis; positivity-free; L35 ($\mathrm{INT}_n$) and L36 (disjoint DNF) are instances.

**Proof.** [lemmas/03_lower_bounds/037_shatter_rectangle_lower.md](lemmas/03_lower_bounds/037_shatter_rectangle_lower.md)

### Lemma 38. Equal denominators collapse to a linear threshold function

An order-$H$ tangent form with all denominators equal ($D_1 = \cdots = D_H = D$, $D>0$ on the cube) factors as $D^{H-1}(\theta D + \sum_h N_h)$, whose sign equals that of an affine form; so it computes only LTFs. Hence any $f$ with $H^{\ast}(f) \geq 2$ needs at least two **distinct** denominators (attention patterns): the model's power comes from denominator diversity, not head count alone.

**Proof.** [lemmas/04_closure_and_structure/038_distinct_denominators.md](lemmas/04_closure_and_structure/038_distinct_denominators.md)

### Lemma 39. The head complexity of INT_3 is exactly two

$H^{\ast}(\mathrm{INT}_3) = 2$: lower bound by non-LTF (L11); upper bound by an explicit admissible 2-atom tangent form ($D_1 = 2-y_3$, $D_2 = 6-x_3-2y_2-2y_3$, verified on all 64 points). The first rigorous proof that $\mathrm{INT}_n$ beats its DNF bound (3 terms, 2 heads), confirming the conjecture $H^{\ast}(\mathrm{INT}_n)=n-1$ at $n=3$.

**Proof.** [lemmas/02_upper_bounds/039_int3_exact.md](lemmas/02_upper_bounds/039_int3_exact.md)

### Lemma 40. Gauge invariance of order-2 tangent forms; product-positivity is free

Order-2 tangent forms have a $\mathrm{GL}_2$ gauge freedom: $(E_1,E_2)=G(D_1,D_2)$, $(M_1,M_2)=G^{-\top}(L_1,L_2)$ give $E_1M_1+E_2M_2 = D_1L_1+D_2L_2$ identically. Consequently the product sign $\mathrm{sign}(D_1D_2)$ is always removable (some $G$ makes $E_1E_2>0$ on the cube, since $v_x=(D_1(x),D_2(x))\neq 0$), and $H^{\ast}(f)\leq 2$ whenever the denominator pencil contains an admissible basis. Isolates the residual order-2 F4 obstruction to *individual* positivity + one-sidedness of the pencil (a gauge-invariant condition), the product-sign twist being free.

**Proof.** [lemmas/04_closure_and_structure/040_gauge_transfer.md](lemmas/04_closure_and_structure/040_gauge_transfer.md)

### Lemma 41. The sign of a product of two affine forms has head complexity at most two

For affine $A, B$ with $AB \neq 0$ on the cube, $f = \mathbf 1[AB>0]$ (agreement of two halfspaces) has $H^{\ast}(f) \leq 2$, via the **difference split** $A = E_1 - E_2$ (both admissible), giving $AB = E_1 B + E_2(-B)$, an order-2 admissible tangent form. With L11, non-LTF such $f$ have $H^{\ast} = 2$ exactly. A reusable order-2 construction tool (underlies L40); the general 2-product-sum case stays open.

**Proof.** [lemmas/02_upper_bounds/041_product_two_affine.md](lemmas/02_upper_bounds/041_product_two_affine.md)

### Lemma 42. A one-sided product plus an affine perturbation has head complexity at most two

For $A$ one-sided affine, $B, g$ affine, with $AB+g \neq 0$ on the cube, $f = \mathbf 1[AB+g>0]$ has $H^{\ast}(f) \leq 2$. Construction: $E_1 - E_2 = A$ with $E_1, E_2$ non-proportional admissible (slopes $\propto$ $A$'s, scaled by $1{+}\nu$ and $\nu$), and affine numerators $K_1 = B+u$, $K_2 = -B+w$ with $E_1 u + E_2 w = g$ (solvable since $E_1, E_2$ independent). Extends L41 by an affine perturbation; disposes of the same-sign-regime pencil $\lbrace A, 1\rbrace$ for all $n$ (a rigorous piece of order-2 F4).

**Proof.** [lemmas/02_upper_bounds/042_affine_plus_oneside_product.md](lemmas/02_upper_bounds/042_affine_plus_oneside_product.md)

### Lemma 43. The indexing (multiplexer) function is an explicit near-linear separation

$\mathrm{IDX}_k(a,m)=m_a$ on $N=2^k+k$ bits has $\deg_{\pm} \leq k+1 = O(\log N)$ (exact multilinear $m_a = \sum_b \mathrm{eq}_b(a) m_b$) but $H^{\ast}(\mathrm{IDX}_k) \geq c\,2^k/k = \Omega(N/\log N)$ (a shatter-rectangle of order $2^k$: rows $=$ memory $m_b=[b\in S]$, columns $=$ address $j$, value $m_j=[j\in S]$; apply L37). A second canonical explicit separation, with logarithmic threshold degree; its terms share the address bits (not a disjoint DNF), so it shows L37 needs only the coordinate partition, not disjointness.

**Proof.** [lemmas/03_lower_bounds/043_indexing_separation.md](lemmas/03_lower_bounds/043_indexing_separation.md)

### Lemma 44. The head complexity of a weighted band is exactly two

For $t = \sum_i w_i x_i$ ($w_i>0$), the weighted band $f = \mathbf 1[\theta_1 \leq t \leq \theta_2]$ has $H^{\ast}(f) \leq 2$ (L25, two sign changes of an interval indicator), and $H^{\ast}(f) = 2$ for proper bands (a checkerboard restriction: the middle values $t_{01},t_{10}$ in-band, extremes $t_{00},t_{11}$ out, so L3 gives $\geq 2$). The nonsymmetric generalization of $\mathrm{EXACT}_{n,k}$; the upper toolkit (L25) meeting the lower (L3) at a tight value.

**Proof.** [lemmas/02_upper_bounds/044_weighted_band.md](lemmas/02_upper_bounds/044_weighted_band.md)

### Lemma 45. ORing a disjoint monotone term costs at most one head

For $f$ on $Z$ and a monotone term $T=\bigwedge_{i\in A}w_i$ on $A$ disjoint from $Z$, $H^{\ast}(f) \leq H^{\ast}(f\vee T) \leq H^{\ast}(f)+1$. The new head is one *summed admissible atom* $\psi=M/D$, $D=\gamma+\rho\sum_{i\in A}\alpha^{w_i}$ ($\alpha\in(0,1)$): a "monotone corner detector" that is $\geq 0$, spikes on the all-ones corner $T{=}1$ and is $\approx 0$ off it, so it adds $T$ without disturbing $f$'s margins (lower side is restriction, L17). Flagship: $H^{\ast}(\mathrm{INT}_n)\leq n-1$ (induct from $H^{\ast}(\mathrm{INT}_3)=2$, L39), closing the upper side of the $\mathrm{INT}_n$ rate ($n/(8\log_2 n)\leq H^{\ast}\leq n-1$, L35). Generalizes to $H^{\ast}(f\vee g)\leq H^{\ast}(f)+s$ for a disjoint monotone DNF $g$ of $s$ terms (re-derives L14) and dually to AND-with-CNF (L15). The monotone bias is essential: a single head spikes only at an extreme corner, so mixed-polarity terms (parities, addressing) do not compose for free, and $\mathrm{INT}_n$'s saving is irreducibly multiplicative ($A_{+}=2^n-1$ kills the weighted-score route).

**Proof.** [lemmas/02_upper_bounds/045_disjoint_term_composition.md](lemmas/02_upper_bounds/045_disjoint_term_composition.md)

### Lemma 46. Bitwise equality has head complexity exactly two

$\mathrm{EQ}_n(x,y)=\mathbf 1[x=y]=\bigwedge_i\overline{(x_i\oplus y_i)}$ (an AND of $n$ disjoint XNORs) has $H^{\ast}(\mathrm{EQ}_n)=2$ for all $n$. *String equality linearizes:* super-increasing weights $w_i=2^{i-1}$ give distinct subset sums, so $x=y \iff I(x)=I(y)$; after flipping the $y$-inputs (L15), $\mathrm{EQ}_n=\mathbf 1[t=2^n-1]$ for a single *positive* weighted sum $t$, a degenerate single-value weighted band, so $H^{\ast}\leq 2$ (L25/L44); the XNOR checkerboard restriction gives $\geq 2$ (L3). **Taxonomy:** any function of the integer difference $d=I(x)-I(y)$ is cheap (GT $=1[d>0]$ has $H^{\ast}=1$; integer/approx-equality bands $\leq 2$), whereas the set-theoretic predicates are $\widetilde\Theta(n)$ (intersection $\mathrm{INT}_n$, and subset $x\subseteq y=\neg\mathrm{INT}_n(x,\bar y)$). The dividing line: a single linear comparison of the two strings vs an irreducibly multiplicative coordinate-wise conjunction-across-an-OR.

**Proof.** [lemmas/02_upper_bounds/046_equality_exact.md](lemmas/02_upper_bounds/046_equality_exact.md)

### Lemma 47. Any function of an integer comparison is cheap

With the integer value $I(x)=\sum_i 2^{i-1}x_i$ (distinct subset sums), every integer-comparison predicate $f(x,y)=G(I(x)-I(y))$ has $H^{\ast}(f)\leq C(G)$ and $\mathrm{sr}_{x|y}(f)\leq (C(G)+1)2^{C(G)}+1$, where $C(G)$ counts sign changes of $G$. Proof: flip $y$ (L15) so $d=I(x)-I(y)=t-(2^n-1)$ for the *positive* weighted sum $t=\sum_i 2^{i-1}(x_i+z_i)$, whose image is the full interval $[0,2(2^n-1)]$ (redundant binary); then L25 gives $H^{\ast}\leq C(G)$ and L22 the sign-rank bound. This is the **easy-side delineator** (counterpart to the L37 lower-bound certificate): it unifies GT ($H^{\ast}=1$), EQ ($2$, L46), and integer/approximate-equality bands ($\leq2$), and explains why integer-comparison predicates can never separate $H^{\ast}$ from threshold degree (bounded $H^{\ast}$ forces bounded sign-rank). The complementary hard class is the *membership/addressing* predicates (intersection $\mathrm{INT}_n$, subset) whose OR/addressing structure embeds $[j\in S]$ (a shatter-rectangle, L37); a lone bilinear coincidence (interior Hamming) is *not* enough — it has only linear sign-rank ($\le n+2$) and no shatter-rectangle.

**Proof.** [lemmas/02_upper_bounds/047_integer_comparison_upper.md](lemmas/02_upper_bounds/047_integer_comparison_upper.md)

### Lemma 48. Every output bit of integer addition has head complexity at most three

For $S=I(x)+I(y)$ ($I(x)=\sum_i 2^i x_i$), the $j$-th output bit $\mathrm{ADD}_{n,j}=\lfloor S/2^j\rfloor\bmod 2$ has $H^{\ast}\leq 3$ for every $n$ and $0\leq j\leq n$ (carry-out $=1$, LSB $=2$, interior bits $\in\{2,3\}$). **The carry chain is free:** bit $j$ depends only on the low bits (a junta), and equals $\lfloor A'/2^j\rfloor\bmod 2$ for the *positive weighted sum* $A'=I(x_{\leq j})+I(y_{\leq j})$, a function of one score with $\leq 3$ sign changes ($\lfloor A'/2^j\rfloor$ runs $0,1,2,3$ over four half-periods), so L25 gives $\leq 3$; the XOR checkerboard gives $\geq2$ for non-carry bits. Addition thus sits with EQ (L46) and integer comparison (L47) on the easy weighted-score side (contrast multiplication, whose bits are not functions of one weighted sum). *Caution reinforced:* the heuristic admissible-form search over-reports ($5,6,7$ at $n{=}4$); the bit's bounded sign-rank ($\leq3$, a diagonal-conjugated comparison matrix) is the reliable tell of bounded $H^{\ast}$.

**Proof.** [lemmas/02_upper_bounds/048_addition_bits.md](lemmas/02_upper_bounds/048_addition_bits.md)

### Lemma 49. The bits of the minimum/maximum of two integers have head complexity two

$\mathrm{MIN}_{n,j}=\lfloor\min(I(x),I(y))/2^j\rfloor\bmod 2$ (and $\mathrm{MAX}$) has $H^{\ast}=2$ for $0\leq j\leq n-2$ (top bit $=x_{n-1}\wedge y_{n-1}$ resp. $\vee$, an LTF, $H^{\ast}=1$). Since the $j$-th digit of $I(z)$ is $z_j$, $\mathrm{MIN}_{n,j}=x_j$ if $I(x)\leq I(y)$ else $y_j$ — a comparison-gated bit selection. The quadratic $V=(x_j-y_j)(\tfrac12-d)+(x_j+y_j-1)$ ($d=I(x)-I(y)$, disjoint-support summands) sign-represents it, and $V=AB+g$ with $A=x_j-y_j$ one-sided after flipping $y_j$ (L15), so L42 gives $\leq2$; an affine-parallelogram crossing certificate (generalized checkerboard, L2) shows it is not an LTF, so $\geq2$. Places $\min/\max$ with comparison (L47) and addition (L48) on the easy side. The boundary is sharp: gate = one comparison, choices = single literals keeps it quadratic, whereas an intersection of two *general* halfspaces (AND of two LTFs) has $\deg_{\pm}=\Omega(n)$ (Sherstov), hence $H^{\ast}=\Omega(n)$.

**Proof.** [lemmas/02_upper_bounds/049_minmax_bits.md](lemmas/02_upper_bounds/049_minmax_bits.md)

### Lemma 50. The median bit: an order-3 tangent witness with inadmissible denominators (an F4 probe)

The median bit $\mathrm{MED}_j$ of three integers has $\mathrm{tChow}_{\pm}(\mathrm{MED}_j)=3$ via the explicit symmetric cubic $P_j=s_x(B{-}C)^2+s_y(A{-}C)^2+s_z(A{-}B)^2$ ($A{=}I(x),B{=}I(y){+}\tfrac14,C{=}I(z){+}\tfrac12$, $s_x{=}2x_j{-}1$), which sign-represents $\mathrm{MED}_j$ (the median's $(u{+}v)^2$ term dominates) and regroups as a tangent form $\sum_h N_h\prod_{k\ne h}D_k$ with $D_h$ the pairwise differences $A{-}B,A{-}C,B{-}C$. **But those denominators form a mixed-sign triangle that no input flip makes simultaneously one-sided**, so the clean witness does *not* certify $H^{\ast}\leq3$. This makes the median the sharpest concrete **F4 probe** (does positivity cost?): $H^{\ast}=3=\mathrm{tChow}$ with healthy margin for $2$-bit integers (F4-free there), but two heavy admissible-form searches **fail** at $3$-bit integers (margin $\approx0$) — a suggestive-but-inconclusive signal of either F4-freeness via non-obvious denominators or the **first positivity gap** $H^{\ast}>\mathrm{tChow}$. Complements the order-2 covering reduction (L40) at order 3. (Cubic via a Codex consult.)

**Proof.** [lemmas/02_upper_bounds/050_median_tchow.md](lemmas/02_upper_bounds/050_median_tchow.md)

## Dependency Order

The current dependency structure is:

1. Lemma 1 gives the additive decomposition.
2. Lemma 2 converts that decomposition into antipode identities.
3. Lemma 3 turns the antipode identities into a one-head lower bound.
4. Lemma 4 gives an independent one-head upper bound family.
5. Lemma 5 combines Lemmas 3 and 4 to answer standard-family cases.
6. Lemma 6 converts head complexity into a threshold-degree upper bound.
7. Lemma 7 computes the threshold degree of parity exactly.
8. Lemma 8 combines Lemmas 6 and 7 with an explicit $n$-head construction for parity.
9. Lemma 9 gives a broader constructive upper-bound route by interpolating over the image of a positive weighted sum.
10. Lemma 10 gives the exact linear-fractional normal form for $H^{\ast}$.
11. Lemma 11 uses Lemma 10 to characterize the zero-head and one-head levels exactly.
12. Lemma 12 uses Lemmas 6 and 10 to characterize every symmetric Boolean function exactly.
13. Lemma 13 refines Lemma 10 into the exact one-head atom dictionary (affine ratio, one-sided positive denominator).
14. Lemma 14 uses Lemma 10 to give the monotone-term DNF upper bound (one head per single-polarity term).
15. Lemma 15 uses Lemma 10 to prove closure under output negation and input permutation.
16. Lemma 16 uses Lemmas 10 and 13 to clear denominators, giving the exact tangential polynomial invariant $H^{\ast}(f) = \mathrm{MFdeg}_{\pm}(f)$.
17. Lemma 17 uses Lemma 10 to prove restriction monotonicity, giving the first nonsymmetric lower-bound transfer (planted parity).
18. Lemma 18 uses Lemmas 13, 16, and 6 to place $H^{\ast}$ in the sandwich $\deg_{\pm} \leq \mathrm{tChow}_{\pm} \leq H^{\ast}$, connecting to a known-flavored algebraic invariant.
19. Lemma 19 uses Lemmas 10 and 9 to give calibrated real interpolation over a positive weighted sum, enabling additive composition of upper bounds.
20. Lemma 20 uses Lemmas 10 and 14 to give the sparse single-polarity threshold-density upper bound via uniformly-approximating calibrated bumps.
21. Lemma 21 uses Lemmas 10 and 17 to prove junta invariance (head complexity ignores irrelevant variables).
22. Lemma 22 uses Lemma 16 (cleared form) with affine cut-rank and Hadamard submultiplicativity to give the sign-rank lower bound, the first lower bound independent of threshold degree.
23. Lemma 23 uses Lemma 16 with Warren sign-pattern counting and the degree-2 PTF count to separate $H^{\ast}$ from $\deg_{\pm}$: some $\deg_{\pm}=2$ function has $H^{\ast}=\Omega(n)$.
24. Lemma 24 runs the same counting without positivity (on $\mathrm{tChow}_{\pm}$), showing the separation is not caused by the attention positivity constraints.
25. Lemma 25 uses Lemma 10 (partial fractions) to bound $H^{\ast}(F(t)) \leq C(F)$ for one positive weighted sum.
26. Lemma 26 uses Lemmas 25, 12, 6 for the simple alternation invariant $A_{+}$ (exact for symmetric).
27. Lemma 27 uses Lemmas 14 and 11 for the exact value $H^{\ast} = 2$ of the 2-by-2 intersection function.
28. Lemma 28 uses Lemma 10 to prove full-input-complement invariance.
29. Lemma 29 reruns the flattening argument (Lemma 22) without positivity, bounding $\mathrm{tChow}_{\pm}$.
30. Lemma 30 uses Lemma 11 to show $\mathrm{tChow}_{\pm} = H^{\ast}$ at level $\leq 1$ (positivity free, base case).
31. Lemma 31 uses Lemmas 12 and 18 (sandwich collapse) to show $\mathrm{tChow}_{\pm} = H^{\ast}$ for all symmetric $f$.
32. Lemma 32 generalizes L30/L31: the sandwich collapse gives $\mathrm{tChow}_{\pm}=H^{\ast}$ whenever $\deg_{\pm}=H^{\ast}$, confining any F4 gap to the separation regime.
33. Lemma 33 combines L22 (flattening) with an explicit sign-rank lower bound $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$ to give the first explicit, rigorously-proved $\deg_{\pm} < H^{\ast}$ separation (on $\mathrm{INT}_{14}$).
34. Lemma 34 sharpens L33 via $(H{+}1)2^H{+}1 \leq 4^H$: $H^{\ast}(\mathrm{INT}_n) \geq \tfrac12\log_2 n$, an explicit unbounded separation, and notes $\mathrm{sr}_{x|y}(\mathrm{INT}_n) = \Theta(n)$ caps flattening at $\Theta(\log n)$.
35. Lemma 35 applies Warren to the singleton-column slice of $\mathrm{INT}_n$ (row acts through $2H{+}1$ parameters, shatters $n$ columns) to get a non-flattening, positivity-free bound $H^{\ast}(\mathrm{INT}_n) = \Omega(n/\log n)$, the first explicit near-linear separation; supersedes L34's $\log$ bound.
36. Lemma 36 generalizes L35's slice technique to any disjoint monotone DNF (width $\geq 2$ terms): $H^{\ast} = \Omega(s/\log s)$, so with L14 ($\leq s$) the head complexity is $\widetilde{\Theta}(s)$ — a near-tight characterization of a nonsymmetric family.
37. Lemma 37 abstracts L35/L36 into a reusable tool: any $g$ with a shatter-rectangle of order $s$ has $\mathrm{tChow}_{\pm}(g) = \Omega(s/\log s)$; L35 and L36 are instances.
38. Lemma 38 (structure): an order-$H$ tangent form with all denominators equal collapses to an LTF, so $H^{\ast} \geq 2$ requires distinct attention patterns — the model's power is denominator diversity, not head count.
39. Lemma 39 gives the first rigorous exact value beating the DNF bound: $H^{\ast}(\mathrm{INT}_3)=2$ via an explicit admissible 2-atom form (uses two distinct denominators, per L38), confirming $H^{\ast}(\mathrm{INT}_n)=n-1$ at $n=3$.
40. Lemma 40 (F4 progress): order-2 tangent forms have a $\mathrm{GL}_2$ gauge freedom; the product-sign twist is always removable, so the residual order-2 positivity obstruction is exactly whether the denominator pencil contains an admissible basis.
41. Lemma 41: the difference split realizes any single product $\mathrm{sign}(AB)$ admissibly, so $H^{\ast}(\mathbf 1[AB>0]) \leq 2$; the order-2 construction tool behind L40.
42. Lemma 42: a one-sided product plus an affine perturbation, sign(AB+g) with A one-sided, has H*<=2; disposes of the same-sign pencil {A,1} for all n.
43. Lemma 43: the indexing/multiplexer IDX_k is an explicit separation (deg_pm=O(log N), H*=Omega(N/log N)) via a shatter-rectangle of order 2^k; canonical, overlapping-term (not disjoint DNF).
44. Lemma 44: the weighted band 1[theta_1<=w.x<=theta_2] (w>0) has H*=2 (L25 upper + checkerboard L3 lower); a nonsymmetric exact value generalizing EXACT_{n,k}.
25. Lemma 25 uses Lemma 10 with a partial-fraction construction to bound $H^{\ast}(F(t)) \leq C(F)$ for one positive weighted sum, generalizing L12's upper direction.
26. Lemma 26 uses Lemmas 25, 12, 6 to give the simple invariant $A_{+}$: $H^{\ast} \leq A_{+}$, exact for symmetric (and whenever $\deg_{\pm} = A_{+}$); the L12-style characterization.

## What This Currently Says About The First Core Question

The current evidence suggests that one-head complexity is governed by linear threshold structure, while upper bounds come from constructive embeddings of low-cardinality positive weighted sums and from the linear-fractional normal form.

That is not yet a full invariant. It is only a partial answer:

- checkerboard structure certifies $H^{\ast}(f) \geq 2$,
- threshold degree certifies $\deg_{\pm}(f) \leq H^{\ast}(f)$,
- the linear-fractional normal form gives an exact model-native definition of $H^{\ast}$,
- positive weighted-sum image structure certifies $H^{\ast}(f) \leq M_{+}(f) - 1$,
- for symmetric functions, the sign-change count gives the exact value,
- the atom dictionary pins the one-head atoms to affine ratios with a one-sided positive denominator (the model's monotone bias),
- the cleared-denominator identity $H^{\ast}(f) = \mathrm{MFdeg}_{\pm}(f)$ gives an exact polynomial (tangential-Chow) normal form sitting between $\deg_{\pm}$ and the model,
- the sandwich $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{\ast}(f)$ connects head complexity to the unconstrained tangential-Chow rank, isolating the positivity/monotone constraints as the gap,
- calibrated positive-weighted-sum interpolation makes upper bounds additively composable,
- monotone-term DNF size certifies $H^{\ast}(f) \leq s$ for the first nonsymmetric family,
- restriction monotonicity transfers any planted-parity lower bound into nonsymmetric $f$,
- the simple invariant $A_{+}(f)$ (min positive-order alternations) gives $H^{\ast} \leq A_{+}$, exact for symmetric functions, the L12-style characterization (and exact whenever $\deg_{\pm} = A_{+}$),
- the flattening sign-rank bound $H^{\ast}(f) = \Omega(\log \mathrm{sr}_{A|B}(f))$ is the first lower bound independent of threshold degree, certifying $H^{\ast} > \deg_{\pm}$ for high-sign-rank functions,
- the counting separation settles the qualitative question: $H^{\ast}$ is strictly finer than $\deg_{\pm}$, with $\deg_{\pm}=2$ functions requiring $H^{\ast}=\Omega(n)$ heads,
- the set-intersection function $\mathrm{INT}_n$ makes that separation explicit and near-linear: $\deg_{\pm}=2$ yet $H^{\ast}(\mathrm{INT}_n) = \Omega(n/\log n)$ (L35, via Warren on the singleton-column slice, positivity-free) and $= \widetilde{\Theta}(n)$ overall — the first explicit polynomial separation, nearly matching the nonconstructive counting bound,
- $H^{\ast}$ is invariant under output negation and input permutation.
