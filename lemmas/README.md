# Lemmas Folder

This folder is the math-first version of the project.

The goal is to write down clean theorem statements and proofs before
deciding which claims are worth formalizing in Lean. The intended scope
matches the model in [problem_statement.md](/Users/karthikviswanathan/Desktop/fair_stuff.nosync/how-many-attention-heads-xor/problem_statement.md):

- one self-attention layer
- `H` parallel heads
- a designated query token
- linear readout from the query residual

## What Is Established Here

The notes in this folder support the following claims.

1. A single head cannot realize any function that contains a 2-bit
   checkerboard restriction.
2. Any symmetric threshold function of Hamming weight is computable with
   one head.
3. Therefore:
   - `OR`, `AND`, and `MAJORITY` have head complexity `1`
     whenever they are nonconstant.
   - `PARITY_n` has head complexity at least `2` for `n >= 2`.
   - `EXACT_k` has head complexity at least `2` for `1 <= k <= n - 1`.

These are useful because they already answer part of the "natural
families" question from the problem statement.

## What Is Not Claimed Here

These notes do not prove:

1. `PARITY_n` requires exactly `n` heads.
2. Polynomial degree controls head complexity in the current softmax
   attention model.
3. Any exact characterization of `H*(f)` for all Boolean functions.

In particular, the current model uses exponentials and normalization, so
polynomial-degree arguments do not automatically apply.

## File Guide

1. [01_checkerboard_restriction.md](/Users/karthikviswanathan/Desktop/fair_stuff.nosync/how-many-attention-heads-xor/lemmas/01_checkerboard_restriction.md)
   proves the general one-head lower bound.
2. [02_symmetric_thresholds.md](/Users/karthikviswanathan/Desktop/fair_stuff.nosync/how-many-attention-heads-xor/lemmas/02_symmetric_thresholds.md)
   proves a broad one-head upper bound.
3. [03_family_consequences.md](/Users/karthikviswanathan/Desktop/fair_stuff.nosync/how-many-attention-heads-xor/lemmas/03_family_consequences.md)
   packages the consequences for standard function families.

## Suggested Formalization Order

1. Formalize the checkerboard restriction lower bound.
2. Formalize the one-head symmetric-threshold construction.
3. Derive the family corollaries for `MAJORITY`, `PARITY`, and
   `EXACT_k`.

That gives a meaningful first formal picture of head complexity on
standard families before attempting harder statements.
