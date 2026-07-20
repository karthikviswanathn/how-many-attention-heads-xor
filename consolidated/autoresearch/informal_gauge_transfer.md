# Problem: The gauge-transfer lemma for order-2 tangent forms (product positivity is free)

## Background and definitions (self-contained)

Work on $\lbrace 0,1\rbrace^n$. An **affine** form is $A(x) = a_0 + \sum_i a_i x_i$, with **slopes** $(a_1,\dots,a_n)$. An affine $D$ is **admissible** if $D(x) > 0$ for all $x \in \lbrace 0,1\rbrace^n$ and its slopes are all of one sign (all $\geq 0$ or all $\leq 0$). An **order-2 tangent form** is $P = D_1 L_1 + D_2 L_2$ with $D_1,D_2,L_1,L_2$ affine. $P$ **strictly sign-represents** $f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$ if $f(x)=1 \iff P(x)>0$ and $f(x)=0 \iff P(x)<0$ for all $x$ (so $P \neq 0$ on the cube). $H^{*}(f) \leq 2$ holds iff some order-2 tangent form with $D_1, D_2$ **admissible** strictly sign-represents $f$.

For $x$ on the cube write $v_x = (D_1(x), D_2(x)) \in \mathbb{R}^2$.

## Claim to prove

Let $P = D_1 L_1 + D_2 L_2$ strictly sign-represent $f$ (affine $D_1,D_2,L_1,L_2$).

**(a) Gauge invariance.** For every invertible $2\times2$ real matrix $G$, define affine forms $(E_1, E_2)^{\top} = G\,(D_1, D_2)^{\top}$ and $(M_1, M_2)^{\top} = G^{-\top}(L_1, L_2)^{\top}$ (i.e. $G^{-\top} = (G^{-1})^{\top}$). Then
$$
E_1 M_1 + E_2 M_2 = D_1 L_1 + D_2 L_2 = P
$$
as functions (identically), so $E_1 M_1 + E_2 M_2$ also strictly sign-represents $f$.

**(b) Product positivity is free.** There exists an invertible $G$ such that the resulting $E_1, E_2$ satisfy $E_1(x) E_2(x) > 0$ for **all** $x$ on the cube.

**(c) Sufficient condition for $H^{*}\leq 2$.** If moreover $G$ can be chosen so that $E_1$ and $E_2$ are both **admissible**, then $H^{*}(f) \leq 2$.

## Guidance (prove every step rigorously)

**Part (a) — the gauge identity.** Write $D = (D_1,D_2)^{\top}$, $L = (L_1,L_2)^{\top}$ as column vectors of affine forms, so $P = D^{\top} L = D_1 L_1 + D_2 L_2$ pointwise. With $E = GD$ and $M = G^{-\top}L$,
$$
E^{\top} M = (GD)^{\top}(G^{-\top}L) = D^{\top} G^{\top} G^{-\top} L = D^{\top} (G^{\top}G^{-\top}) L = D^{\top} L = P,
$$
using $G^{\top} G^{-\top} = G^{\top}(G^{\top})^{-1} = I$. Since $E_1, E_2$ are affine (linear combinations of $D_1, D_2$) and $M_1, M_2$ are affine, $E_1 M_1 + E_2 M_2$ is an order-2 tangent form equal to $P$ everywhere; hence it strictly sign-represents the same $f$. *(Verify the matrix identity and that $E_h, M_h$ are affine.)*

**Part (b) — making the product positive.**
1. **No common zero.** For every cube point $x$, $v_x = (D_1(x), D_2(x)) \neq (0,0)$: if $v_x = 0$ then $P(x) = D_1(x)L_1(x) + D_2(x)L_2(x) = 0$, contradicting strict sign-representation ($P \neq 0$ on the cube). *(justification: $P(x)$ is a combination of $D_1(x), D_2(x)$.)*
2. **Choose the first row of $G$.** The set of cube points is finite; for each $x$, $\lbrace u \in \mathbb{R}^2 : u \cdot v_x = 0\rbrace$ is a line through the origin. Pick $u \in \mathbb{R}^2$ off all these finitely many lines, so $u \cdot v_x \neq 0$ for every $x$. Set $E_1 = u_1 D_1 + u_2 D_2$, so $E_1(x) = u \cdot v_x \neq 0$ for all $x$.
3. **Choose the second row.** Pick $q \in \mathbb{R}^2$ not parallel to $u$ (so $G = \begin{psmallmatrix} u \\ u + \varepsilon q\end{psmallmatrix}$ is invertible for $\varepsilon \neq 0$). Let $E_2 = (u_1 + \varepsilon q_1)D_1 + (u_2 + \varepsilon q_2)D_2$, so $E_2(x) = u\cdot v_x + \varepsilon (q \cdot v_x)$. Choose $\varepsilon \neq 0$ small enough that $|\varepsilon (q\cdot v_x)| < |u \cdot v_x|$ for every (finitely many) $x$; this is possible since $\min_x |u\cdot v_x| > 0$. Then $E_2(x)$ has the same sign as $E_1(x) = u\cdot v_x$ for every $x$, so $E_1(x) E_2(x) > 0$ on the whole cube. $G$ has rows $u$ and $u + \varepsilon q$ (linearly independent), hence is invertible. *(justification: a real number within distance $<|t|$ of $t$ shares the sign of $t$.)*

**Part (c) — the corollary.** If $G$ makes $E_1, E_2$ admissible, then by (a) $f$ is strictly sign-represented by the order-2 tangent form $E_1 M_1 + E_2 M_2$ with $E_1, E_2$ admissible, which is exactly the definition of $H^{*}(f) \leq 2$.

## Pitfalls

- $G^{-\top}$ means $(G^{-1})^{\top} = (G^{\top})^{-1}$; the identity $G^{\top}G^{-\top} = I$ is what makes the gauge work. State it explicitly.
- (b) gives only $E_1 E_2 > 0$ (the two denominators share a sign at each point); this is **weaker** than each $E_h > 0$ individually and weaker than admissibility. Do **not** claim (b) yields admissibility — it yields product positivity only. (c) is conditional on $G$ achieving full admissibility, which is a separate (and not always attainable on a fixed pencil) requirement.
- The construction in (b) uses only that the cube is finite and $v_x \neq 0$; no positivity of the original $D_h$ is assumed.
