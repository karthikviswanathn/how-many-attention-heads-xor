# One Head Computes Symmetric Thresholds

## Statement

For `n >= 1` and `1 <= t <= n`, define the symmetric threshold function

`T_{n,t}(x) = 1[|x| >= t]`

where `|x|` is the Hamming weight.

Then `T_{n,t}` is computable with one head.

Since `T_{n,t}` is nonconstant for `1 <= t <= n`, it follows that

`H*(T_{n,t}) = 1`.

This includes:

- `OR_n`, which is `T_{n,1}`
- `AND_n`, which is `T_{n,n}`
- `MAJORITY_n`, which is `T_{n,ceil(n/2)}`

## Construction

Work in dimension `d = 2` with basis vectors `u = (1,0)` and
`v = (0,1)`.

Choose token embeddings

`e_0 = (0,0)`

`e_1 = (1,1)`

`e_= = (1,0)`

and set all positional embeddings to zero.

Choose linear maps

`W_Q = W_K = [[1,0],[0,0]]`

`W_V = [[0,0],[0,1]]`.

## What This Does

For an input-bit position:

1. If the bit is `0`, then its embedded vector is `(0,0)`.
   - Its attention logit against the query is `0`, so its softmax weight
     numerator is `exp(0) = 1`.
   - Its value vector is `0`.

2. If the bit is `1`, then its embedded vector is `(1,1)`.
   - Its attention logit against the query is `1`, so its softmax weight
     numerator is `exp(1) = e`.
   - Its value vector is `v`.

For the query token itself:

- its embedded vector is `(1,0)`
- its attention logit is also `1`, so its softmax numerator is `e`
- its value vector is `0`

Thus if the input has Hamming weight `k`, the query update is

`z(k) = s(k) v`

with

`s(k) = (e k) / (e k + (n-k) + e)`.

So the entire head output lies on a single ray, and the only thing that
matters is the scalar score `s(k)`.

## Monotonicity Lemma

The function `s(k)` is strictly increasing in `k`.

### Proof

Write

`s(k) = (e k) / ((e-1)k + n + e)`.

For integer `0 <= k < n`,

`s(k+1) - s(k)`

`= e(n+e) / (((e-1)k + n + e) ((e-1)(k+1) + n + e))`

which is strictly positive.

Hence

`s(0) < s(1) < ... < s(n)`.

## Readout

Take the linear probe `w = v`.

Then the probe score on an input of Hamming weight `k` is exactly

`<w, z(k)> = s(k)`.

Because `s(k)` is strictly increasing, for every threshold index
`t in {1, ..., n}` we can choose any

`tau` with `s(t-1) < tau < s(t)`.

Then

`<w, z(x)> > tau`

holds exactly when `|x| >= t`.

So the head computes `T_{n,t}`.

## Exact Complexity

Zero heads only give a constant query residual, so no nonconstant
function can be computed with zero heads.

Since each `T_{n,t}` with `1 <= t <= n` is nonconstant, we conclude

`H*(T_{n,t}) = 1`.

## Why This Matters

This is a broad upper bound family:

- one head already computes all monotone symmetric threshold functions
- therefore one head is not merely capable of `OR` and `AND`
- it already reaches `MAJORITY` and every other Hamming-weight threshold

So the interesting gap is not between linear threshold functions and
attention heads. The gap appears when the target needs a "middle band" or
"alternating" dependence on Hamming weight, such as parity or exact-count
predicates.
