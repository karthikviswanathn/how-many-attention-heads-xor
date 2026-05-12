# Consequences For Standard Function Families

This note packages the lower bound from [01_checkerboard_restriction.md](01_checkerboard_restriction.md) and the upper bound from [02_symmetric_thresholds.md](02_symmetric_thresholds.md), both in the formal model from [../model.md](../model.md).

We write $H^{*}(f)$ for the minimum number of heads needed to compute $f : \{0,1\}^n \to \{0,1\}$ in the one-layer attention model.

## Theorem 1. Symmetric Thresholds Have Exact Head Complexity 1

For $1 \leq t \leq n$,

$$
T_{n,t}(x) \;=\; \mathbf{1}\!\left[\,|x| \geq t\,\right]
$$

satisfies

$$
H^{*}(T_{n,t}) \;=\; 1.
$$

### Special cases

1. $H^{*}(\mathrm{OR}_n) = 1$,
2. $H^{*}(\mathrm{AND}_n) = 1$,
3. $H^{*}(\mathrm{MAJORITY}_n) = 1$.

The proof is exactly the one-head construction from the previous note, together with the trivial fact that zero heads only produce constant outputs.

## Theorem 2. Parity Has Head Complexity At Least 2

For $n \geq 2$, define

$$
\mathrm{PARITY}_n(x) \;=\; x_1 \oplus x_2 \oplus \cdots \oplus x_n.
$$

Then

$$
H^{*}(\mathrm{PARITY}_n) \;\geq\; 2.
$$

**Proof.** Fix coordinates $i \neq j$, and fix every other coordinate to $0$. On the remaining two free bits $(a,b)$, the parity function becomes

$$
\mathrm{PARITY}_n(\ldots, a, \ldots, b, \ldots) \;=\; a \oplus b.
$$

So the restricted truth table is

$$
0, \; 1, \; 1, \; 0,
$$

which is exactly the checkerboard pattern. By the checkerboard restriction lower bound, one head is impossible. Since parity is nonconstant, zero heads are also impossible. Hence $H^{*}(\mathrm{PARITY}_n) \geq 2$. $\blacksquare$

## Theorem 3. Internal Exact-Count Functions Need At Least 2 Heads

For $0 \leq k \leq n$, define

$$
\mathrm{EXACT}_{n,k}(x) \;=\; \mathbf{1}\!\left[\,|x| = k\,\right].
$$

Then for every internal count $1 \leq k \leq n-1$,

$$
H^{*}(\mathrm{EXACT}_{n,k}) \;\geq\; 2.
$$

**Proof.** Fix two free coordinates $i \neq j$. Set exactly $k - 1$ of the remaining coordinates to $1$ and the rest to $0$. This is possible because $1 \leq k \leq n - 1$.

Now evaluate $\mathrm{EXACT}_{n,k}$ on the two free bits:

1. $(0,0)$ gives total weight $k-1$, so the output is $0$.
2. $(0,1)$ gives total weight $k$, so the output is $1$.
3. $(1,0)$ gives total weight $k$, so the output is $1$.
4. $(1,1)$ gives total weight $k+1$, so the output is $0$.

Thus the restriction is again

$$
0, \; 1, \; 1, \; 0.
$$

So one head is impossible by the checkerboard lower bound, and therefore $H^{*}(\mathrm{EXACT}_{n,k}) \geq 2$. $\blacksquare$

## Edge Cases Of Exact Count

The edge cases are different:

1. $\mathrm{EXACT}_{n,0}$ is the predicate *all bits are zero*. This is a threshold of Hamming weight from below, so it is computable with one head by flipping the probe sign in the symmetric-threshold construction.
2. $\mathrm{EXACT}_{n,n}$ is exactly $\mathrm{AND}_n$, so it has head complexity $1$.

So the internal exact-count predicates are the first genuinely different cases.

## Interim Picture For Symmetric Families

The current math gives the following picture.

1. Constant functions have head complexity $0$.
2. Symmetric threshold functions have head complexity $1$.
3. Parity and internal exact-count functions have head complexity at least $2$.

This already answers part of the *natural families* question from the problem statement.

## What Remains Open

These notes do not determine:

1. the exact value of $H^{*}(\mathrm{PARITY}_n)$ for $n > 2$,
2. the exact value of $H^{*}(\mathrm{EXACT}_{n,k})$ for internal $k$,
3. whether there is a single invariant that captures all these cases.

So the current evidence is enough to identify a real divide between threshold-like symmetric functions and checkerboard-like symmetric functions, but not yet enough to characterize the whole hierarchy.
