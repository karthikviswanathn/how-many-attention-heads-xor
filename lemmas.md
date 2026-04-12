# Lemmas Toward The First Core Question

## Goal

We want a step-by-step route to the first core question in [problem_statement.md](problem_statement.md):

> Can $H^{*}(f)$ be expressed, exactly or approximately, in terms of a known invariant of $f$?

This file is the statement ledger. It records the current lemma statements, how they fit together, and where each proof lives under `lemmas/`.

## Current Status

The current notes do **not** yet give an exact characterization of $H^{*}(f)$ for all Boolean functions.

What they *do* give is:

- a structural one-head lower bound via checkerboard restrictions,
- a one-head upper bound for symmetric threshold functions,
- exact answers for some standard families, including parity,
- a clean separation between threshold-like behavior and checkerboard-like behavior.

## Main Lemma Stack

### Lemma 1. One-head two-coordinate restrictions split additively

Fix a single-head model and freeze all but two input coordinates. Then the softmax numerator and denominator at the query token can be written as

$$
N(a,b) = A(a) + B(b) + C, \qquad D(a,b) = \alpha(a) + \beta(b) + \gamma
$$

for suitable functions $A, B, \alpha, \beta$ and constants $C, \gamma$.

**Proof.** [lemmas/01_checkerboard_restriction.md](lemmas/01_checkerboard_restriction.md)

### Lemma 2. Antipode identities on a restricted 2-cube

Under the same setup,

$$
N(0,0) + N(1,1) = N(0,1) + N(1,0)
$$

and

$$
D(0,0) + D(1,1) = D(0,1) + D(1,0).
$$

**Proof.** [lemmas/01_checkerboard_restriction.md](lemmas/01_checkerboard_restriction.md)

### Lemma 3. Checkerboard obstruction for one head

If $f : \{0,1\}^n \to \{0,1\}$ has a 2-bit checkerboard restriction, then

$$
H^{*}(f) \geq 2.
$$

> **Equivalently.** One head cannot separate one diagonal of a restricted 2-cube from the other diagonal.

**Proof.** [lemmas/01_checkerboard_restriction.md](lemmas/01_checkerboard_restriction.md)

### Lemma 4. One head computes every symmetric threshold

For

$$
T_{n,t}(x) = \mathbf{1}\!\left[\,|x| \geq t\,\right], \qquad 1 \leq t \leq n,
$$

where $|x|$ is the Hamming weight of $x$, namely the number of coordinates of $x$ equal to $1$.

we have

$$
H^{*}(T_{n,t}) = 1.
$$

In particular,

$$
H^{*}(\mathrm{OR}_n) = H^{*}(\mathrm{AND}_n) = H^{*}(\mathrm{MAJORITY}_n) = 1.
$$

**Proof.** [lemmas/02_symmetric_thresholds.md](lemmas/02_symmetric_thresholds.md)

### Lemma 5. Family consequences from the checkerboard obstruction

For $n \geq 2$,

$$
H^{*}(\mathrm{PARITY}_n) \geq 2.
$$

For $1 \leq k \leq n - 1$,

$$
H^{*}(\mathrm{EXACT}_{n,k}) \geq 2.
$$

Together with Lemma 4, this gives a first split inside symmetric functions:

- monotone symmetric thresholds have head complexity $1$,
- parity and internal exact-count predicates need at least $2$ heads.

**Proof.** [lemmas/03_family_consequences.md](lemmas/03_family_consequences.md)

### Lemma 6. Threshold degree is bounded by head complexity

If a Boolean function $f$ is computable in the model from [model.md](model.md), then

$$
\deg_{\pm}(f) \leq H^{*}(f).
$$

Here $\deg_{\pm}(f)$ denotes the threshold degree of $f$, namely the minimum degree of a real polynomial that sign-represents $f$ on the Boolean cube.

**Proof.** [lemmas/xor_n_bits.md](lemmas/xor_n_bits.md)

### Lemma 7. Parity has threshold degree exactly $n$

For

$$
\mathrm{PARITY}_n(x) = x_1 \oplus \cdots \oplus x_n,
$$

we have

$$
\deg_{\pm}(\mathrm{PARITY}_n) = n.
$$

**Proof.** [lemmas/xor_n_bits.md](lemmas/xor_n_bits.md)

### Lemma 8. Exact parity complexity

For every $n \geq 1$,

$$
H^{*}(\mathrm{XOR}_n) = n.
$$

> **Equivalently.** In this one-layer attention model, parity needs exactly one head per input bit.

**Proof.** [lemmas/xor_n_bits.md](lemmas/xor_n_bits.md)

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

## What This Currently Says About The First Core Question

The current evidence suggests that one-head complexity is governed by a geometric restriction on 2-coordinate slices, while upper bounds come from constructive embeddings of Hamming weight. For parity, the exact answer is captured by threshold degree.

That is not yet a full invariant. It is only a partial answer:

- checkerboard structure certifies $H^{*}(f) \geq 2$,
- symmetric threshold structure certifies $H^{*}(f) = 1$.
- for parity, threshold degree gives the exact value $H^{*}(\mathrm{XOR}_n) = n$.
