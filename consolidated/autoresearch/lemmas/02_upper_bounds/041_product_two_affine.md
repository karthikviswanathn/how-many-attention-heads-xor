# The Sign of a Product of Two Affine Forms Has Head Complexity at Most Two

## Statement

Let $A, B$ be affine forms on $\lbrace 0,1\rbrace^n$ with $A(x)B(x) \neq 0$ for all $x$, and let $f(x) = \mathbf 1[\,A(x)B(x) > 0\,]$ (equivalently, $f = 1$ iff $A$ and $B$ agree in sign). Then

$$
H^{*}(f) \leq 2.
$$

> The "agreement of two halfspaces" functions are computed by two heads. The construction is a **difference split**: one of the two affine factors is written as a difference of two *admissible* (positive, one-sided) denominators, turning the single product $AB$ into an order-2 admissible tangent form with affine numerators $B$ and $-B$. This is the matching upper bound to the checkerboard-type lower bounds (e.g. $\mathrm{XOR}_2 = \mathbf 1[(x_1-\tfrac12)(x_2-\tfrac12)>0]$ has $H^{*}=2$, by L3 and this lemma), and a reusable construction tool.

## Proof

Write $A = a_0 + \sum_i a_i x_i$. Split its slopes by sign:
$$
A^{+} = \sum_{i:\,a_i>0} a_i x_i, \qquad A^{-} = \sum_{i:\,a_i<0}(-a_i)x_i,
$$
both affine with nonnegative (hence one-sided) slopes, and $A^{+} - A^{-} = \sum_i a_i x_i$ on the cube. Fix $c = |a_0| + 1 > 0$ and set
$$
E_1 = (a_0 + c) + A^{+}, \qquad E_2 = c + A^{-}.
$$
Each $E_h$ has nonnegative slopes (one-sided) and, since a nonnegative-slope affine form on $\lbrace 0,1\rbrace^n$ attains its minimum at $x = 0$, $E_1 \geq a_0 + c > 0$ and $E_2 \geq c > 0$ on the cube; so $E_1, E_2$ are **admissible** denominators. Moreover $E_1 - E_2 = a_0 + (A^{+} - A^{-}) = A$.

Take numerators $K_1 = B$, $K_2 = -B$ (both affine) and form the order-2 tangent form
$$
P = E_1 K_1 + E_2 K_2 = E_1 B - E_2 B = (E_1 - E_2)\,B = A\,B .
$$
Since $AB \neq 0$ on the cube, $P = AB$ is nonzero everywhere, and $f(x) = 1 \iff A(x)B(x) > 0 \iff P(x) > 0$, $f(x) = 0 \iff P(x) < 0$. Thus $P$ strictly sign-represents $f$, and it is an order-2 tangent form with admissible denominators $E_1, E_2$. By the definition of head complexity, $H^{*}(f) \leq 2$. $\blacksquare$

## Consequence

The difference split $A = E_1 - E_2$ (two admissible denominators differing by $A$) is the order-2 construction underlying the positivity-free analysis (L40): it shows a *single* product is admissibly representable without the order-1 free-numerator trick (which fails at order 2 because clearing $E_1 E_2$ would need a quadratic numerator). Combined with $H^{*}(f) \geq 2$ for non-LTF $f$ (L11), every non-LTF $f$ of the form $\mathbf 1[AB>0]$ has $H^{*}(f) = 2$ exactly. The general order-2 case ($f$ from a *sum* $D_1L_1 + D_2L_2$ of two products, not a single product) does not reduce to this — splitting both products yields four, which is not an order-2 tangent form — and remains the open residual of the order-2 F4 question (proved for $n \leq 4$; the $n \geq 5$ joint off-diagonal/affine covering is open, empirically true for $n \leq 6$).
