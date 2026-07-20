# Problem: The sign of a product of two affine forms has head complexity at most two

## Background and definitions (self-contained)

Work on $\lbrace 0,1\rbrace^n$. An **affine** form is $A(x) = a_0 + \sum_i a_i x_i$, with **slopes** $(a_1,\dots,a_n)$. An affine $D$ is **admissible** if $D(x) > 0$ for all $x \in \lbrace 0,1\rbrace^n$ and its slopes are all of one sign (all $\geq 0$ or all $\leq 0$; the all-zero slope vector counts as one-sided). An **order-2 tangent form** is $P = \theta D_1 D_2 + N_1 D_2 + N_2 D_1$ with $\theta\in\mathbb{R}$ and $D_1,D_2,N_1,N_2$ affine; equivalently $P = D_1 K_1 + D_2 K_2$ for affine $K_1,K_2$ (take $\theta=0$, $N_1=K_1$, $N_2=K_2$). $H^{*}(f) \leq 2$ holds iff some order-2 tangent form with $D_1,D_2$ **admissible** strictly sign-represents $f$ ($f(x)=1 \iff P(x)>0$, $f(x)=0 \iff P(x)<0$, $P\neq0$ on the cube).

## Claim to prove

Let $A, B$ be affine forms such that the product $A(x)B(x) \neq 0$ for every $x \in \lbrace 0,1\rbrace^n$, and let $f(x) = \mathbf 1[\,A(x)B(x) > 0\,]$ (so $f(x)=1$ iff $A(x)$ and $B(x)$ have the same sign). Then

$$
H^{*}(f) \leq 2 .
$$

## Guidance (prove every step rigorously)

The idea is a **difference split** of one affine factor into two admissible denominators.

1. **Split $A$ into one-sided parts.** Write $A = a_0 + \sum_i a_i x_i$. Let $A^{+} = \sum_{i : a_i > 0} a_i x_i$ (slopes $\geq 0$) and $A^{-} = \sum_{i : a_i < 0} (-a_i) x_i$ (slopes $\geq 0$); both have one-sided (nonnegative) slopes, and $A^{+}(x) - A^{-}(x) = \sum_i a_i x_i$ on the cube. *(justification: split the sum by sign of $a_i$.)*

2. **Shift to make them positive.** Choose a constant $c > 0$ large enough that $a_0 + c > 0$ (e.g. $c = |a_0| + 1$), and set
   $$
   E_1 = (a_0 + c) + A^{+}, \qquad E_2 = c + A^{-}.
   $$
   Then $E_1, E_2$ are affine with nonnegative slopes (one-sided), and on the cube $E_1(x) \geq a_0 + c > 0$ and $E_2(x) \geq c > 0$ (each is its positive constant plus a nonnegative-slope sum evaluated at $\geq 0$ inputs), so $E_1, E_2$ are **admissible**. *(justification: a nonnegative-slope affine form on $\lbrace0,1\rbrace^n$ attains its minimum at $x=0$, equal to its constant term.)*

3. **The split reconstructs $A$.** $E_1 - E_2 = (a_0 + c + A^{+}) - (c + A^{-}) = a_0 + (A^{+} - A^{-}) = a_0 + \sum_i a_i x_i = A$ on the cube. *(justification: Step 1 identity; the $c$'s cancel.)*

3. **Form the order-2 tangent form.** Put $K_1 = B$ and $K_2 = -B$ (both affine), and
   $$
   P = E_1 K_1 + E_2 K_2 = E_1 B - E_2 B = (E_1 - E_2)\,B = A\,B .
   $$
   So $P = AB$ as functions on the cube. *(justification: Step 3 and distributivity.)*

4. **$P$ strictly sign-represents $f$ and the denominators are admissible.** By hypothesis $AB \neq 0$ on the cube, so $P = AB$ is nonzero everywhere, and $f(x)=1 \iff A(x)B(x)>0 \iff P(x)>0$, while $f(x)=0 \iff A(x)B(x)<0 \iff P(x)<0$. Thus $P$ strictly sign-represents $f$. $P = E_1 K_1 + E_2 K_2$ is an order-2 tangent form (with $\theta=0$) whose denominators $E_1, E_2$ are admissible (Step 2). By the definition of $H^{*}$, $H^{*}(f) \leq 2$. $\blacksquare$

## Pitfalls

- Admissibility needs BOTH positivity on the cube and one-sided slopes. The shift by $c$ secures positivity; the sign-split secures one-sidedness; address both for each $E_h$.
- The two added constants must be equal up to the $a_0$ offset so they cancel in $E_1 - E_2 = A$ (Step 3). Verify the cancellation.
- The numerators $K_1 = B$, $K_2 = -B$ are affine; no quadratic numerator is needed. (This is why the construction stays at order 2 rather than clearing a quadratic.)
- The hypothesis $AB \neq 0$ on the cube is what makes the sign-representation strict; state where it is used.
