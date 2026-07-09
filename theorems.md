# Theorems Toward The First Core Question

## Goal

We want a step-by-step route to the first core question in [problem_statement.md](problem_statement.md):

> Can $H^{\ast}(f)$ be expressed, exactly or approximately, in terms of a known invariant of $f$?

This file is the statement ledger. It records the current theorem statements, how they fit together, and where each proof lives under `theorems/`.

For nearby literature and context, see [literature_survey.md](literature_survey.md).

## Current Status

The current main-branch theorem stack uses the numbered foundation files in `theorems/01_foundations_and_normal_form/`, through Theorem 12.

These notes give:

- a structural one-head lower bound via checkerboard restrictions,
- exact one-head upper bounds for symmetric thresholds,
- exact head complexity for parity and all symmetric Boolean functions,
- the threshold-degree lower-bound route,
- a constructive weighted-sum upper-bound route,
- an exact linear-fractional normal form for head complexity,
- an exact characterization of the zero-head and one-head levels.

The stack still does **not** give an exact characterization of $H^{\ast}(f)$ for all nonsymmetric Boolean functions.

## Main Theorem Stack

### Theorem 1. One-head two-coordinate restrictions split additively

Fix a single-head model and freeze all but two input coordinates. Then the softmax numerator and denominator at the query token can be written as

$$ N(a,b) = A(a) + B(b) + C, \qquad D(a,b) = \alpha(a) + \beta(b) + \gamma $$

for suitable functions $A, B, \alpha, \beta$ and constants $C, \gamma$.

**Proof.** [theorems/01_foundations_and_normal_form/001_checkerboard_additive_decomposition.md](theorems/01_foundations_and_normal_form/001_checkerboard_additive_decomposition.md)

### Theorem 2. Antipode identities on a restricted 2-cube

Under the same setup,

$$ N(0,0) + N(1,1) = N(0,1) + N(1,0) $$

and

$$ D(0,0) + D(1,1) = D(0,1) + D(1,0). $$

**Proof.** [theorems/01_foundations_and_normal_form/002_antipode_identities.md](theorems/01_foundations_and_normal_form/002_antipode_identities.md)

### Theorem 3. Checkerboard obstruction for one head

If $f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$ has a 2-bit checkerboard restriction, then

$$ H^{\ast}(f) \geq 2. $$

> **Equivalently.** One head cannot separate one diagonal of a restricted 2-cube from the other diagonal.

**Proof.** [theorems/01_foundations_and_normal_form/003_checkerboard_obstruction.md](theorems/01_foundations_and_normal_form/003_checkerboard_obstruction.md)

### Theorem 4. One head computes every symmetric threshold

For

$$ T_{n,t}(x) = \mathbf{1} \left[ \lvert x\rvert \geq t \right], \qquad 1 \leq t \leq n, $$

where $\lvert x\rvert$ is the Hamming weight of $x$, namely the number of coordinates of $x$ equal to $1$.

we have

$$ H^{\ast}(T_{n,t}) = 1. $$

In particular,

$$ H^{\ast}(\mathrm{OR}_n) = H^{\ast}(\mathrm{AND}_n) = H^{\ast}(\mathrm{MAJORITY}_n) = 1. $$

**Proof.** [theorems/01_foundations_and_normal_form/004_symmetric_thresholds.md](theorems/01_foundations_and_normal_form/004_symmetric_thresholds.md)

### Theorem 5. Family consequences from the checkerboard obstruction

For $n \geq 2$,

$$ H^{\ast}(\mathrm{PARITY}_n) \geq 2. $$

For $1 \leq k \leq n - 1$,

$$ H^{\ast}(\mathrm{EXACT}_{n,k}) \geq 2. $$

Together with Theorem 4, this gives a first split inside symmetric functions:

- monotone symmetric thresholds have head complexity $1$,
- parity and internal exact-count predicates need at least $2$ heads.

**Proof.** [theorems/01_foundations_and_normal_form/005_family_consequences.md](theorems/01_foundations_and_normal_form/005_family_consequences.md)

### Theorem 6. Threshold degree is bounded by head complexity

If a Boolean function $f$ is computable in the model from [model.md](model.md), then

$$ \deg_{\pm}(f) \leq H^{\ast}(f). $$

Here $\deg_{\pm}(f)$ denotes the threshold degree of $f$, namely the minimum degree of a real polynomial that sign-represents $f$ on the Boolean cube.

**Proof.** [theorems/01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md](theorems/01_foundations_and_normal_form/006_threshold_degree_head_complexity_bound.md)

### Theorem 7. Parity has threshold degree exactly n

For

$$ \mathrm{PARITY}_n(x) = x_1 \oplus \cdots \oplus x_n, $$

we have

$$ \deg_{\pm}(\mathrm{PARITY}_n) = n. $$

**Proof.** [theorems/01_foundations_and_normal_form/007_parity_threshold_degree.md](theorems/01_foundations_and_normal_form/007_parity_threshold_degree.md)

### Theorem 8. Exact parity complexity

For every $n \geq 1$,

$$ H^{\ast}(\mathrm{XOR}_n) = n. $$

> **Equivalently.** In this one-layer attention model, parity needs exactly one head per input bit.

**Proof.** [theorems/01_foundations_and_normal_form/008_exact_parity_complexity.md](theorems/01_foundations_and_normal_form/008_exact_parity_complexity.md)

### Theorem 9. Weighted-sum interpolation upper bound

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

**Proof.** [theorems/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md](theorems/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md)

### Theorem 10. Exact linear-fractional normal form

Define a one-head atom to be a function of the form

$$ \phi(x) = \frac{ \eta + \sum_{i=1}^{n} \rho_i \alpha^{x_i}(m_i + \delta x_i) }{ \gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i} }, $$

where

$$ \gamma > 0, \qquad \rho_1, \ldots, \rho_n > 0, \qquad \alpha > 0. $$

Let $L_{\mathrm{frac}}(f)$ be the least $H$ such that $f$ is computed by thresholding a constant plus a sum of $H$ such atoms. Then

$$ H^{\ast}(f) = L_{\mathrm{frac}}(f). $$

> **Interpretation.** The exact model-native invariant is the minimum number of one-head linear-fractional atoms needed before the final threshold.

**Proof.** [theorems/01_foundations_and_normal_form/010_linear_fractional_normal_form.md](theorems/01_foundations_and_normal_form/010_linear_fractional_normal_form.md)

### Theorem 11. Exact one-head characterization

The first two levels of head complexity are:

$$ H^{\ast}(f) = 0 \qquad \Longleftrightarrow \qquad f \text{ is constant}, $$

and

$$ H^{\ast}(f) = 1 \qquad \Longleftrightarrow \qquad f \text{ is a nonconstant linear threshold function}. $$

In particular, every non-linear-threshold Boolean function has

$$ H^{\ast}(f) \geq 2. $$

This strictly strengthens the checkerboard obstruction as a one-head lower bound.

**Proof.** [theorems/01_foundations_and_normal_form/011_one_head_characterization.md](theorems/01_foundations_and_normal_form/011_one_head_characterization.md)

### Theorem 12. Exact symmetric sign-change characterization

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

**Proof.** [theorems/01_foundations_and_normal_form/012_symmetric_sign_changes.md](theorems/01_foundations_and_normal_form/012_symmetric_sign_changes.md)

## Dependency Order

The current dependency structure is:

1. Theorem 1 gives the additive decomposition.
2. Theorem 2 converts that decomposition into antipode identities.
3. Theorem 3 turns the antipode identities into a one-head lower bound.
4. Theorem 4 gives an independent one-head upper bound family.
5. Theorem 5 combines Theorems 3 and 4 to answer standard-family cases.
6. Theorem 6 converts head complexity into a threshold-degree upper bound.
7. Theorem 7 computes the threshold degree of parity exactly.
8. Theorem 8 combines Theorems 6 and 7 with an explicit $n$-head construction for parity.
9. Theorem 9 gives a broader constructive upper-bound route by interpolating over the image of a positive weighted sum.
10. Theorem 10 gives the exact linear-fractional normal form for $H^{\ast}$.
11. Theorem 11 uses Theorem 10 to characterize the zero-head and one-head levels exactly.
12. Theorem 12 uses Theorems 6 and 10 to characterize every symmetric Boolean function exactly.

## What This Currently Says About The First Core Question

The current evidence suggests that one-head complexity is governed by linear threshold structure, while upper bounds come from constructive embeddings of low-cardinality positive weighted sums and from the linear-fractional normal form.

That is not yet a full invariant. It is only a partial answer:

- checkerboard structure certifies $H^{\ast}(f) \geq 2$,
- threshold degree certifies $\deg_{\pm}(f) \leq H^{\ast}(f)$,
- the linear-fractional normal form gives an exact model-native definition of $H^{\ast}$,
- positive weighted-sum image structure certifies $H^{\ast}(f) \leq M_{+}(f) - 1$,
- for symmetric functions, the sign-change count gives the exact value.
