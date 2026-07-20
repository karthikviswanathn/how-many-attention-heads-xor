# Lemmas Toward The First Core Question

## Goal

We want a step-by-step route to the first core question in [problem_statement.md](problem_statement.md):

> Can $H^{\ast}(f)$ be expressed, exactly or approximately, in terms of a known invariant of $f$?

This file is the statement ledger. It records the current lemma statements, how they fit together, and where each proof lives under `lemmas/`.

For nearby literature and context, see [literature_survey.md](literature_survey.md).

## Current Status

The current main-branch lemma stack uses the numbered foundation files in `lemmas/01_foundations_and_normal_form/`, through Lemma 12.

These notes give:

- a structural one-head lower bound via checkerboard restrictions,
- exact one-head upper bounds for symmetric thresholds,
- exact head complexity for parity and all symmetric Boolean functions,
- the threshold-degree lower-bound route,
- a constructive weighted-sum upper-bound route,
- an exact linear-fractional normal form for head complexity,
- an exact characterization of the zero-head and one-head levels.

The stack still does **not** give an exact characterization of $H^{\ast}(f)$ for all nonsymmetric Boolean functions.

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

## What This Currently Says About The First Core Question

The current evidence suggests that one-head complexity is governed by linear threshold structure, while upper bounds come from constructive embeddings of low-cardinality positive weighted sums and from the linear-fractional normal form.

That is not yet a full invariant. It is only a partial answer:

- checkerboard structure certifies $H^{\ast}(f) \geq 2$,
- threshold degree certifies $\deg_{\pm}(f) \leq H^{\ast}(f)$,
- the linear-fractional normal form gives an exact model-native definition of $H^{\ast}$,
- positive weighted-sum image structure certifies $H^{\ast}(f) \leq M_{+}(f) - 1$,
- for symmetric functions, the sign-change count gives the exact value.

### Lemma 13. Affine atom dictionary for one head. Every one-head atom from Lemma 10 is $\phi=N/D$ with $N,D$ affine and $D>0$; the admissible denominators are exactly the constant-positive, all-positive-coefficient, and all-negative-coefficient with positive all-ones value classes; nonconstant denominators allow arbitrary affine numerators, while constant denominators force sign-uniform coordinate numerator coefficients. **Proof.** [lemmas/01_foundations_and_normal_form/013_affine_atom_dictionary.md](lemmas/01_foundations_and_normal_form/013_affine_atom_dictionary.md)

### Lemma 14. Cleared-denominator polynomial invariant. If $\mathrm{MFdeg}_{\pm}(f)$ is defined using the admissible affine pairs from Lemma 13 and the cleared polynomial $\theta\prod_h D_h+\sum_h N_h\prod_{g\neq h}D_g$, then $H^{\ast}(f)=\mathrm{MFdeg}_{\pm}(f)$. **Proof.** [lemmas/01_foundations_and_normal_form/014_cleared_denominator_invariant.md](lemmas/01_foundations_and_normal_form/014_cleared_denominator_invariant.md)

### Lemma 15. Tangential-Chow reformulation of the cleared-denominator invariant. Homogenizing Lemma 14's cleared polynomial identifies it with an admissibility-restricted parameter tangent vector to the degree-$H$ Chow cone of products of linear forms, and every such restricted tangent vector dehomogenizes back to a Lemma 14 cleared polynomial. Consequently $H^{\ast}(f)$ is the least $H$ admitting a strict Boolean-cube sign-representer from this restricted tangential-Chow form. **Proof.** [lemmas/01_foundations_and_normal_form/015_tangential_chow_reformulation.md](lemmas/01_foundations_and_normal_form/015_tangential_chow_reformulation.md)

### Lemma 16. Unrestricted tangential-Chow sandwich bound. Defining $\mathrm{tChow}_{\pm}(f)$ by dropping the attention admissibility and positivity restrictions from the tangential-Chow form, one has $\deg_{\pm}(f)\leq \mathrm{tChow}_{\pm}(f)\leq H^{\ast}(f)$ for every Boolean function $f$. **Proof.** [lemmas/01_foundations_and_normal_form/016_tchow_sandwich_lower_bound.md](lemmas/01_foundations_and_normal_form/016_tchow_sandwich_lower_bound.md)

### Lemma 17. Same-polarity DNF subcube upper bound. For a fixed polarity $\zeta$ and nonempty coordinate sets $A_1,\ldots,A_s$, the DNF $f(x)=\bigvee_{r=1}^{s}\bigwedge_{i\in A_r}\mathbf{1}[x_i=\zeta]$ satisfies $H^{\ast}(f)\leq s$; equivalently, a union of $s$ coordinate subcubes anchored at one Boolean vertex is computable with at most one head per subcube. **Proof.** [lemmas/01_foundations_and_normal_form/017_same_polarity_dnf_upper_bound.md](lemmas/01_foundations_and_normal_form/017_same_polarity_dnf_upper_bound.md)

### Lemma 18. Same-polarity sparse threshold-density upper bound. For a fixed polarity $\zeta$ and nonempty coordinate sets $A_1,\ldots,A_s$, every strict threshold $f(x)=\mathbf{1}[\theta+\sum_{r=1}^{s}c_r\mathbf{1}[x_i=\zeta\text{ for all }i\in A_r]>0]$ with positive margin satisfies $H^{\ast}(f)\leq s$; equivalently, strict signed thresholds of $s$ same-vertex coordinate-subcube indicators need at most one head per subcube. **Proof.** [lemmas/01_foundations_and_normal_form/018_same_polarity_sparse_threshold_density_upper_bound.md](lemmas/01_foundations_and_normal_form/018_same_polarity_sparse_threshold_density_upper_bound.md)

### Lemma 19. Warren counting bound for low head complexity. For all $n\geq 1$ and $H\geq 1$, the class $\mathcal{F}_{n,H}=\{f:\{0,1\}^{n}\to\{0,1\}:H^{\ast}(f)\leq H\}$ satisfies $\log_2|\mathcal{F}_{n,H}|\leq C H n(n+\log_2(H+1))$ for an absolute constant $C$; equivalently, at most $2^{C H n(n+\log_2(H+1))}$ Boolean-cube sign patterns are realizable with $H$ heads. **Proof.** [lemmas/01_foundations_and_normal_form/019_warren_head_count_upper_bound.md](lemmas/01_foundations_and_normal_form/019_warren_head_count_upper_bound.md)

### Lemma 20. Quadratic threshold functions can require linearly many heads. There is an absolute constant $c>0$ such that for all sufficiently large $n$ there is $f_n:\{0,1\}^{n}\to\{0,1\}$ with $\deg_{\pm}(f_n)=2$ and $H^{\ast}(f_n)\geq c n$; this gives a linear separation between head complexity and ordinary threshold degree inside quadratic threshold functions. **Proof.** [lemmas/01_foundations_and_normal_form/020_quadratic_ptf_head_separation.md](lemmas/01_foundations_and_normal_form/020_quadratic_ptf_head_separation.md)

### Lemma 21. Warren counting bound for unrestricted tangential-Chow complexity. For all $n\geq 1$ and $H\geq 1$, the class $\mathcal T_{n,H}=\{f:\{0,1\}^{n}\to\{0,1\}:\mathrm{tChow}_{\pm}(f)\leq H\}$ satisfies $\log_2|\mathcal T_{n,H}|\leq C H n(n+\log_2(H+1))$ for an absolute constant $C$; equivalently, unrestricted tangential-Chow forms of order $H$ realize at most $2^{C H n(n+\log_2(H+1))}$ strict Boolean-cube sign patterns. **Proof.** [lemmas/01_foundations_and_normal_form/021_tchow_warren_count_upper_bound.md](lemmas/01_foundations_and_normal_form/021_tchow_warren_count_upper_bound.md)

### Lemma 22. Quadratic threshold functions can require linearly many heads. There are absolute constants $c>0$ and $n_0$ such that for every $n\geq n_0$ there is a quadratic threshold function $f_n:\{0,1\}^{n}\to\{0,1\}$ with $\deg_{\pm}(f_n)=2$ and $H^{\ast}(f_n)\geq c n$; this duplicates the quadratic counting separation already recorded as Lemma 20. **Proof.** [lemmas/01_foundations_and_normal_form/022_quadratic_ptf_head_separation.md](lemmas/01_foundations_and_normal_form/022_quadratic_ptf_head_separation.md)

### Lemma 23. Quadratic threshold functions can require linearly large unrestricted tangential-Chow complexity. There are absolute constants $c>0$ and $n_0$ such that for every sufficiently large $n$ there is $f_n:\{0,1\}^{n}\to\{0,1\}$ with $\deg_{\pm}(f_n)=2$ and $\mathrm{tChow}_{\pm}(f_n)\geq c n$; thus unrestricted tangential-Chow complexity can be linearly larger than ordinary threshold degree. **Proof.** [lemmas/01_foundations_and_normal_form/023_quadratic_ptf_tchow_separation.md](lemmas/01_foundations_and_normal_form/023_quadratic_ptf_tchow_separation.md)

### Lemma 23. Quadratic threshold functions can require linearly large unrestricted tangential-Chow complexity. There are absolute constants $c>0$ and $n_0$ such that for every $n\geq n_0$ there is $f_n:\{0,1\}^{n}\to\{0,1\}$ with $\deg_{\pm}(f_n)=2$ and $\mathrm{tChow}_{\pm}(f_n)\geq c n$; thus unrestricted tangential-Chow complexity can be linearly larger than ordinary threshold degree. **Proof.** [lemmas/01_foundations_and_normal_form/023_quadratic_ptf_tchow_separation.md](lemmas/01_foundations_and_normal_form/023_quadratic_ptf_tchow_separation.md)

### Lemma 24. Almost all Boolean functions need exponentially many heads. There is an absolute constant $c>0$ such that a uniformly random $f:\{0,1\}^{n}\to\{0,1\}$ satisfies $\Pr[H^{\ast}(f)\geq c\frac{2^n}{n^2}]\to 1$; consequently $\max_{f:\{0,1\}^{n}\to\{0,1\}}H^{\ast}(f)=\Omega(2^n/n^2)$, while Lemma 9 gives the universal upper bound $2^n-1$. **Proof.** [lemmas/01_foundations_and_normal_form/024_almost_all_head_lower_bound.md](lemmas/01_foundations_and_normal_form/024_almost_all_head_lower_bound.md)

### Lemma 25. Almost all Boolean functions need exponentially many heads. With probability tending to $1$, a uniformly random $f : \{0,1\}^{n} \to \{0,1\}$ satisfies $H^{\ast}(f) \geq c\frac{2^n}{n^2}$ for an absolute $c>0$; hence $\max_f H^{\ast}(f) \geq c\frac{2^n}{n^2}$, while Lemma 9 gives $\max_f H^{\ast}(f) \leq 2^n-1$. **Proof.** [lemmas/01_foundations_and_normal_form/025_almost_all_head_lower_bound.md](lemmas/01_foundations_and_normal_form/025_almost_all_head_lower_bound.md)

### Lemma 26. Subcube restriction monotonicity. If $g$ is obtained from $f$ by fixing coordinates and relabeling the remaining inputs, then $H^{\ast}(g)\leq H^{\ast}(f)$; consequently any restricted subcube lower bound for $g$ is a lower bound for $f$. **Proof.** [lemmas/01_foundations_and_normal_form/026_subcube_restriction_monotonicity.md](lemmas/01_foundations_and_normal_form/026_subcube_restriction_monotonicity.md)

### Lemma 27. Subcube restriction monotonicity. If $g$ is obtained from $f$ by fixing coordinates and relabeling the remaining inputs, then $H^{\ast}(g)\leq H^{\ast}(f)$; consequently any restricted subcube lower bound for $g$ is a lower bound for $f$. **Proof.** [lemmas/01_foundations_and_normal_form/027_subcube_restriction_monotonicity.md](lemmas/01_foundations_and_normal_form/027_subcube_restriction_monotonicity.md)

### Lemma 28. Indexing functions have parity restriction lower bounds. For $m\geq 1$, fixing the data table of $\mathrm{IND}_m(a,y)=y_a$ to the truth table of any $g:\{0,1\}^{m}\to\{0,1\}$ gives $g$ as a subcube restriction, so $H^{\ast}(\mathrm{IND}_m)\geq \max_g H^{\ast}(g)$; in particular $H^{\ast}(\mathrm{IND}_m)\geq m$ by Lemma 8, and Lemma 24 or 25 gives $H^{\ast}(\mathrm{IND}_m)=\Omega(2^m/m^2)$. **Proof.** [lemmas/01_foundations_and_normal_form/028_address_indexing_parity_lower_bound.md](lemmas/01_foundations_and_normal_form/028_address_indexing_parity_lower_bound.md)

### Lemma 29. Two-polarity sparse threshold-density upper bound. For nonempty coordinate sets $A_1,\ldots,A_s$ and term polarities $\zeta_r\in\{0,1\}$, every strict threshold $f(x)=\mathbf{1}[\theta+\sum_{r=1}^{s}c_r\mathbf{1}[x_i=\zeta_r\text{ for all }i\in A_r]>0]$ with positive Boolean-cube margin satisfies $H^{\ast}(f)\leq s$; equivalently, strict signed thresholds of $s$ coordinate subcubes anchored termwise at $\vec 0$ or $\vec 1$ need at most one head per subcube. **Proof.** [lemmas/01_foundations_and_normal_form/029_two_polarity_sparse_threshold_density_upper_bound.md](lemmas/01_foundations_and_normal_form/029_two_polarity_sparse_threshold_density_upper_bound.md)

### Lemma 30. Weighted-sum sign-change upper bound. If $f(x)=F(t(x))$ for a positive weighted sum $t(x)=\sum_i\lambda_i x_i$, then $H^{\ast}(f)\leq C_t(F)$, the number of sign changes of $F$ along the sorted image of $t$; hence Lemma 9 follows as $H^{\ast}(f)\leq M-1$. **Proof.** [lemmas/01_foundations_and_normal_form/030_weighted_sum_sign_change_upper_bound.md](lemmas/01_foundations_and_normal_form/030_weighted_sum_sign_change_upper_bound.md)

### Lemma 31. Irrelevant variables do not change head complexity. If $\widetilde f(x,z)=f(x)$, then $H^{\ast}(\widetilde f)=H^{\ast}(f)$; moreover $H^{\ast}(f\circ\pi)=H^{\ast}(f)$ for coordinate permutations and $H^{\ast}(1-f)=H^{\ast}(f)$. **Proof.** [lemmas/01_foundations_and_normal_form/031_irrelevant_variable_invariance.md](lemmas/01_foundations_and_normal_form/031_irrelevant_variable_invariance.md)

### Lemma 32. Active-junta weighted-sum sign-change upper bound. If $f$ depends only on active coordinates $I$ and the induced active function is a function of a positive weighted sum on $I$, then $H^{\ast}(f)\leq C_{t_I}(G)$; in particular every $k$-junta satisfies $H^{\ast}(f)\leq 2^k-1$. **Proof.** [lemmas/01_foundations_and_normal_form/032_active_junta_weighted_sum_upper_bound.md](lemmas/01_foundations_and_normal_form/032_active_junta_weighted_sum_upper_bound.md)

### Lemma 33. Active-junta support-size upper bound. If $f$ depends only on $k$ active coordinates and the induced active function has $a$ ones and $b=2^k-a$ zeros, then $H^{\ast}(f)\leq \min\{2a,2b,2^k-1\}$; in particular, if the active truth table has at most $r$ ones or at most $r$ zeros, then $H^{\ast}(f)\leq 2r$. **Proof.** [lemmas/01_foundations_and_normal_form/033_active_junta_support_size_upper_bound.md](lemmas/01_foundations_and_normal_form/033_active_junta_support_size_upper_bound.md)

### Lemma 34. Positive Boolean minors do not increase head complexity. If $g$ is obtained from $f$ by a positive Boolean minor, namely by substituting constants or unnegated input coordinates with repetitions allowed, then $H^{\ast}(g)\leq H^{\ast}(f)$; in particular fixing, permuting, duplicating, identifying coordinates, and adding unused coordinates cannot increase head complexity. **Proof.** [lemmas/01_foundations_and_normal_form/034_positive_minor_monotonicity.md](lemmas/01_foundations_and_normal_form/034_positive_minor_monotonicity.md)

### Lemma 35. Homogeneous-polarity Boolean minors do not increase head complexity. The antipodal input complement $f^{\dagger}(x)=f(1-x_1,\ldots,1-x_n)$ satisfies $H^{\ast}(f^{\dagger})=H^{\ast}(f)$; consequently any homogeneous-polarity Boolean minor, using constants and either only unnegated variables or only negated variables with repetitions allowed, satisfies $H^{\ast}(g)\leq H^{\ast}(f)$. **Proof.** [lemmas/01_foundations_and_normal_form/035_homogeneous_polarity_minor_monotonicity.md](lemmas/01_foundations_and_normal_form/035_homogeneous_polarity_minor_monotonicity.md)

### Lemma 36. Coordinate subcube indicators have one head. For disjoint coordinate sets $P,N\subseteq\{1,\ldots,n\}$, the signed coordinate subcube indicator $\chi_{P,N}$ satisfies $H^{\ast}(\chi_{P,N})=0$ when $P\cup N=\emptyset$ and $H^{\ast}(\chi_{P,N})=1$ otherwise; equivalently every nontrivial conjunction of arbitrary signed literals is exactly a one-head function. **Proof.** [lemmas/01_foundations_and_normal_form/036_coordinate_subcube_one_head_exact.md](lemmas/01_foundations_and_normal_form/036_coordinate_subcube_one_head_exact.md)
