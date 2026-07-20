# Gauge Invariance of Order-Two Tangent Forms, and Free Product-Positivity

## Statement

Let $f$ be strictly sign-represented by an order-2 tangent form $P = D_1 L_1 + D_2 L_2$ (affine $D_1,D_2,L_1,L_2$; recall the order-2 tangent forms are exactly the sums of two products of affine pairs, $\theta D_1D_2 + N_1D_2 + N_2D_1 = D_1 N_2 + D_2(\theta D_1 + N_1)$).

**(a) Gauge invariance.** For every invertible $G \in \mathrm{GL}_2(\mathbb{R})$, the recombined denominators $(E_1,E_2)^{\top} = G(D_1,D_2)^{\top}$ and numerators $(M_1,M_2)^{\top} = G^{-\top}(L_1,L_2)^{\top}$ satisfy $E_1 M_1 + E_2 M_2 = D_1 L_1 + D_2 L_2 = P$ identically. So $f$ is sign-represented by the gauge-transformed order-2 form for every $G$.

**(b) Product-positivity is free.** Some invertible $G$ makes $E_1(x)E_2(x) > 0$ for all $x$ on the cube.

**(c) Sufficient condition.** If some $G$ makes both $E_1,E_2$ admissible (positive on the cube with one-sided slopes), then $H^{*}(f) \leq 2$. In particular $H^{*}(f)\leq 2$ whenever the denominator pencil $\mathrm{span}\lbrace D_1,D_2\rbrace$ contains an admissible basis.

> The order-2 head-complexity question has a $\mathrm{GL}_2$ gauge freedom acting on the denominator pencil (with the contragredient action on numerators), leaving the represented function fixed. Two consequences for the open F4 question ("does attention positivity cost?"): the **product-sign twist is always removable** at order 2 — the only positivity feature an order-2 $\mathrm{tChow}_{\pm}$ witness cannot already match admissibly is the *individual* positivity + one-sidedness of the two denominators, which is a property of the *pencil* (whether $\mathrm{span}\lbrace D_1,D_2\rbrace$ contains an admissible basis), invariant under the gauge. This isolates the residual order-2 obstruction precisely.

## Proof

**(a)** Write $D=(D_1,D_2)^{\top}$, $L=(L_1,L_2)^{\top}$ (columns of affine forms), so $P = D^{\top}L$ pointwise. With $E = GD$, $M = G^{-\top}L$,
$$
E^{\top}M = (GD)^{\top}(G^{-\top}L) = D^{\top}\big(G^{\top}G^{-\top}\big)L = D^{\top}L = P,
$$
since $G^{\top}G^{-\top} = G^{\top}(G^{\top})^{-1} = I$. Each $E_h$ (a fixed linear combination of the affine $D_1,D_2$) and each $M_h$ are affine, so $E_1M_1+E_2M_2$ is again an order-2 tangent form, equal to $P$ everywhere; it therefore strictly sign-represents the same $f$.

**(b)** For $x$ on the cube put $v_x = (D_1(x),D_2(x))$. If $v_x = 0$ then $P(x) = D_1(x)L_1(x)+D_2(x)L_2(x) = 0$, contradicting strict sign-representation; so $v_x \neq 0$ for all $x$. The cube is finite, so $\lbrace u : u\cdot v_x = 0\rbrace$ is a finite union of lines through $0$; pick $u$ off all of them, giving $u\cdot v_x \neq 0$ for every $x$ and $\min_x|u\cdot v_x| > 0$. Pick $q$ not parallel to $u$ and $\varepsilon \neq 0$ with $|\varepsilon(q\cdot v_x)| < |u\cdot v_x|$ for all $x$. Let $G$ have rows $u$ and $u+\varepsilon q$ (independent, so $G$ invertible). Then $E_1(x) = u\cdot v_x$ and $E_2(x) = u\cdot v_x + \varepsilon(q\cdot v_x)$ share a sign at every $x$, so $E_1(x)E_2(x) > 0$ on the whole cube.

**(c)** If $G$ makes $E_1,E_2$ admissible, then by (a) the order-2 tangent form $E_1M_1+E_2M_2$ with admissible denominators strictly sign-represents $f$, which is the definition of $H^{*}(f)\leq 2$. The pencil $\mathrm{span}\lbrace D_1,D_2\rbrace$ contains an admissible basis exactly when such a $G$ exists. $\blacksquare$

## Consequence

This pins down what positivity can and cannot cost at order two. By (b), the product sign $\mathrm{sign}(D_1D_2)$ — the feature flagged by the F4 reduction as the only positivity-specific obstruction surviving the free numerators — is **always** removable. What is *not* automatically removable is making each denominator individually positive *and* one-sided: this requires the pencil to contain an admissible basis ($0 \notin \mathrm{conv}\lbrace v_x\rbrace$ for individual positivity, plus one-sided slopes), a gauge-invariant condition. When it fails (e.g. $0 \in \mathrm{conv}\lbrace v_x\rbrace$, which happens for genuine non-LTF order-2 witnesses such as $\mathbf 1[x_1=x_2]$), a proof of $H^{*}(f)\leq 2$ must pass to a *different* admissible pencil — the residual content of the (empirically confirmed for $n\leq 6$, still open in general) order-2 case of F4. Single products are already covered: $f = \mathrm{sign}(AB)$ has $H^{*} \leq 2$ via the difference split $A = E_+ - E_-$ (both admissible, equal added constant), giving $AB = E_+B + E_-(-B)$.
