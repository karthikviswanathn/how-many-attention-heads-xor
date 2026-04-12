# Consequences For Standard Function Families

This note packages the lower bound from
[01_checkerboard_restriction.md](/Users/karthikviswanathan/Desktop/fair_stuff.nosync/how-many-attention-heads-xor/lemmas/01_checkerboard_restriction.md)
and the upper bound from
[02_symmetric_thresholds.md](/Users/karthikviswanathan/Desktop/fair_stuff.nosync/how-many-attention-heads-xor/lemmas/02_symmetric_thresholds.md).

We write `H*(f)` for the minimum number of heads needed to compute
`f : {0,1}^n -> {0,1}` in the one-layer attention model.

## Theorem 1: Symmetric Thresholds Have Exact Head Complexity 1

For `1 <= t <= n`,

`T_{n,t}(x) = 1[|x| >= t]`

satisfies

`H*(T_{n,t}) = 1`.

### Special cases

1. `H*(OR_n) = 1`
2. `H*(AND_n) = 1`
3. `H*(MAJORITY_n) = 1`

The proof is exactly the one-head construction from the previous note,
together with the trivial fact that zero heads only produce constant
outputs.

## Theorem 2: Parity Has Head Complexity At Least 2

For `n >= 2`, define

`PARITY_n(x) = x_1 xor x_2 xor ... xor x_n`.

Then

`H*(PARITY_n) >= 2`.

### Proof

Fix coordinates `i != j`, and fix every other coordinate to `0`.

On the remaining two free bits `(a,b)`, the parity function becomes

`PARITY_n(...,a,...,b,...) = a xor b`.

So the restricted truth table is

`0, 1, 1, 0`

which is exactly the checkerboard pattern.

By the checkerboard restriction lower bound, one head is impossible.

Since parity is nonconstant, zero heads are also impossible.

Hence `H*(PARITY_n) >= 2`.

## Theorem 3: Internal Exact-Count Functions Need At Least 2 Heads

For `0 <= k <= n`, define

`EXACT_{n,k}(x) = 1[|x| = k]`.

Then for every internal count `1 <= k <= n-1`,

`H*(EXACT_{n,k}) >= 2`.

### Proof

Fix two free coordinates `i != j`.

Set exactly `k-1` of the remaining coordinates to `1` and the rest to
`0`. This is possible because `1 <= k <= n-1`.

Now evaluate `EXACT_{n,k}` on the two free bits:

1. `(0,0)` gives total weight `k-1`, so the output is `0`.
2. `(0,1)` gives total weight `k`, so the output is `1`.
3. `(1,0)` gives total weight `k`, so the output is `1`.
4. `(1,1)` gives total weight `k+1`, so the output is `0`.

Thus the restriction is again

`0, 1, 1, 0`.

So one head is impossible by the checkerboard lower bound, and therefore
`H*(EXACT_{n,k}) >= 2`.

## Edge Cases Of Exact Count

The edge cases are different:

1. `EXACT_{n,0}` is the predicate "all bits are zero".
   This is a threshold of Hamming weight from below, so it is computable
   with one head by flipping the probe sign in the symmetric-threshold
   construction.
2. `EXACT_{n,n}` is exactly `AND_n`, so it has head complexity `1`.

So the internal exact-count predicates are the first genuinely different
cases.

## Interim Picture For Symmetric Families

The current math gives the following picture.

1. Constant functions have head complexity `0`.
2. Symmetric threshold functions have head complexity `1`.
3. Parity and internal exact-count functions have head complexity at
   least `2`.

This already answers part of the "natural families" question from the
problem statement.

## What Remains Open

These notes do not determine:

1. the exact value of `H*(PARITY_n)` for `n > 2`
2. the exact value of `H*(EXACT_{n,k})` for internal `k`
3. whether there is a single invariant that captures all these cases

So the current evidence is enough to identify a real divide between
threshold-like symmetric functions and checkerboard-like symmetric
functions, but not yet enough to characterize the whole hierarchy.
