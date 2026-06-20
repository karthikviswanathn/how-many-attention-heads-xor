# Checkerboard Restriction Lower Bound

## Statement

Fix the one-layer attention-only model from [../model.md](../../model.md), with a single head and a linear readout from the query token.

Let $f : \{0,1\}^n \to \{0,1\}$. Suppose there exist distinct coordinates $i \neq j$ and a base assignment to all other coordinates such that, restricted to the two free bits $(a,b)$ in positions $i, j$, the function looks like

$$
f(0,0) = c, \qquad f(1,1) = c, \qquad f(0,1) = 1 - c, \qquad f(1,0) = 1 - c
$$

for some $c \in \{0,1\}$.

Then $f$ cannot be computed with one head.

> **Equivalently.** Any function containing a 2-bit checkerboard restriction has head complexity at least $2$.

## Why This Is The Right Generalization Of XOR

The usual 2-bit XOR truth table is exactly the special case $c = 0$:

$$
0, \; 1, \; 1, \; 0.
$$

So the single-head XOR impossibility is just the first instance of a more general obstruction: *one head cannot separate one diagonal of a 2-cube from the other diagonal*.

## Proof

Fix all coordinates except $i$ and $j$. Write the restricted input as $x^{(a,b)}$.

In the notation of [../model.md](../../model.md), let $\widetilde y(a,b)$ be the unprojected one-head output at the query token, and let

$$
z(a,b) := W_O \widetilde y(a,b)
$$

be the projected contribution of that head to the query residual.

Then we may write

$$
z(a,b) = \frac{N(a,b)}{D(a,b)}
$$

where

$$
N(a,b) := \sum_{t \in \{1,\ldots,n,=\}} \exp\bigl(\ell_t(a,b)\bigr)\, \widehat v_t(a,b),
$$

$$
D(a,b) := \sum_{t \in \{1,\ldots,n,=\}} \exp\bigl(\ell_t(a,b)\bigr),
$$

and

$$
\widehat v_t(a,b) := W_O v_t(a,b).
$$

So $N(a,b)$ is the vector-valued softmax numerator after the output projection, and $D(a,b) > 0$ is the scalar denominator.

### Lemma 1. Additive decomposition on a 2-coordinate restriction

On the restricted 2-cube, both $N$ and $D$ decompose as

$$
N(a,b) = A(a) + B(b) + C, \qquad D(a,b) = \alpha(a) + \beta(b) + \gamma
$$

for suitable functions $A, B, \alpha, \beta$ and constants $C, \gamma$.

**Reason.** Each sequence position belongs to exactly one of three types:

1. The $i$-th input position depends only on $a$.
2. The $j$-th input position depends only on $b$.
3. Every other position, including the query token, is fixed across the restriction and contributes a constant.

Since the attention numerator is a sum over positions of per-position terms

$$
\exp\bigl(\ell_t(a,b)\bigr)\, \widehat v_t(a,b),
$$

and the denominator is the same sum without the projected value vectors, the dependence splits coordinatewise.

### Lemma 2. Antipode identities

From the decomposition above,

$$
N(0,0) + N(1,1) = N(0,1) + N(1,0)
$$

and

$$
D(0,0) + D(1,1) = D(0,1) + D(1,0).
$$

**Proof.** Expand both sides using the formulas from Lemma 1:

$$
\begin{aligned}
N(0,0) + N(1,1) &= \bigl(A(0) + B(0) + C\bigr) + \bigl(A(1) + B(1) + C\bigr) \\
&= A(0) + A(1) + B(0) + B(1) + 2C,
\end{aligned}
$$

which is symmetric in the same way as $N(0,1) + N(1,0)$. The proof for $D$ is identical.

### Lemma 3. The same-class segments intersect

Define

$$
P := \frac{N(0,0) + N(1,1)}{D(0,0) + D(1,1)}.
$$

By Lemma 2 this is also

$$
P = \frac{N(0,1) + N(1,0)}{D(0,1) + D(1,0)}.
$$

Since each $D(a,b)$ is strictly positive, both expressions are convex combinations:

$$
P \in \bigl[z(0,0),\, z(1,1)\bigr] \quad\text{and}\quad P \in \bigl[z(0,1),\, z(1,0)\bigr].
$$

So the segment joining one diagonal intersects the segment joining the other diagonal.

### Conclusion

Assume there were an affine functional $L(z) = w^\top z - \tau$ separating the two classes.

- If $c = 0$, then $L$ must be nonpositive on $z(0,0), z(1,1)$ and positive on $z(0,1), z(1,0)$. By convexity it is nonpositive on the entire segment $[z(0,0), z(1,1)]$ and positive on the entire segment $[z(0,1), z(1,0)]$.

But those two segments intersect at $P$, so $L(P)$ would have to be both nonpositive and positive. Contradiction.

The case $c = 1$ is the same argument with the signs reversed.

Therefore no single head can realize a checkerboard restriction. $\blacksquare$

## Consequence

Any function with such a restriction must satisfy

$$
H^{*}(f) \;\geq\; 2.
$$

This is the core lower-bound mechanism currently available in the softmax-attention model.
