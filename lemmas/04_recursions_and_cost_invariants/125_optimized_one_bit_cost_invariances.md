# Optimized One-Bit Cost Invariances

## Statement

Let

$$
T:\{0,1\}^{m}\to\{0,1\}.
$$

The optimized one-bit costs $\operatorname{lgactc}(T)$ and $\operatorname{xactc}(T)$ have the following structural properties.

1. Output complement does not change either cost:

   $$
   \operatorname{lgactc}(1-T)=\operatorname{lgactc}(T),
   \qquad
   \operatorname{xactc}(1-T)=\operatorname{xactc}(T).
   $$

2. Coordinate permutations do not change either cost. If $\pi$ is a permutation of $\{1,\ldots,m\}$ and

   $$
   T^{\pi}(y_1,\ldots,y_m)
   :=
   T(y_{\pi(1)},\ldots,y_{\pi(m)}),
   $$

   then

   $$
   \operatorname{lgactc}(T^{\pi})=\operatorname{lgactc}(T),
   \qquad
   \operatorname{xactc}(T^{\pi})=\operatorname{xactc}(T).
   $$

3. Global bit-flip on the feature variables does not change either cost. If

   $$
   T^{\mathrm{flip}}(y)
   :=
   T(1-y_1,\ldots,1-y_m),
   $$

   then

   $$
   \operatorname{lgactc}(T^{\mathrm{flip}})=\operatorname{lgactc}(T),
   \qquad
   \operatorname{xactc}(T^{\mathrm{flip}})=\operatorname{xactc}(T).
   $$

4. Restrictions cannot increase either cost. If $R$ is obtained from $T$ by fixing some feature coordinates, then

   $$
   \operatorname{lgactc}(R)\leq\operatorname{lgactc}(T),
   \qquad
   \operatorname{xactc}(R)\leq\operatorname{xactc}(T).
   $$

5. Adding dummy feature variables does not change either cost. If

   $$
   U(y,w)=T(y),
   $$

   then

   $$
   \operatorname{lgactc}(U)=\operatorname{lgactc}(T),
   \qquad
   \operatorname{xactc}(U)=\operatorname{xactc}(T).
   $$

> **Interpretation.** The optimized literal-gating and fresh-XOR costs can be minimized on the same canonical feature representatives as $\operatorname{actc}$. Hard restrictions of the feature remain valid lower-bound witnesses for these optimized one-bit targets.

## Proof

We use the notation of [122_lifted_literal_gating_cost.md](122_lifted_literal_gating_cost.md) and [124_fresh_bit_xor_target_cost.md](124_fresh_bit_xor_target_cost.md). A strict affine-cylinder score for $T$ has the form

$$
S(y)=A(y)+\sum_{\gamma\in\Gamma}c_{\gamma}C_{\gamma}(y),
\qquad
A(y)=a+\sum_{i=1}^{m}\alpha_i y_i,
$$

with

$$
L(A)=\{i:\alpha_i\neq0\}.
$$

For $\gamma=(P,N)$, write

$$
K_{0}(\gamma):=\kappa(P,N),
\qquad
K_{+}(\gamma):=\kappa(P\cup\{z\},N),
\qquad
K_{-}(\gamma):=\kappa(P,N\cup\{z\}).
$$

For a family $\Gamma$, use $K_{0}(\Gamma)$, $K_{+}(\Gamma)$, and $K_{-}(\Gamma)$ for the corresponding sums over $\gamma\in\Gamma$.

### Lemma 1. Output complement

If $S$ strictly represents $T$, then $-S$ strictly represents $1-T$. The affine part changes from $A$ to $-A$, so $L(A)$ and $\eta_{\oplus}(A)$ are unchanged. The cylinder supports are unchanged and only the coefficients change sign.

Thus the $\operatorname{lgactc}$ and $\operatorname{xactc}$ costs of the displayed score are unchanged. This proves

$$
\operatorname{lgactc}(1-T)\leq\operatorname{lgactc}(T),
\qquad
\operatorname{xactc}(1-T)\leq\operatorname{xactc}(T).
$$

Applying the same argument to $1-T$ proves equality.

### Lemma 2. Coordinate permutations

A coordinate permutation relabels the affine slopes and each cylinder support. Hence $\lvert L(A)\rvert$ is unchanged, $\eta_{\oplus}(A)$ is unchanged, and every triple

$$
K_{0}(\gamma),\ K_{+}(\gamma),\ K_{-}(\gamma)
$$

is unchanged. Precomposing a strict score with the permutation gives no larger cost, and applying the inverse permutation gives equality for both optimized costs.

### Lemma 3. Global bit-flip

Under the global feature bit-flip $y\mapsto1-y$, the affine form becomes

$$
A(1-y_1,\ldots,1-y_m),
$$

so $\lvert L(A)\rvert$ and $\eta_{\oplus}(A)$ are unchanged. A cylinder $(P,N)$ becomes $(N,P)$. Therefore

$$
\kappa(N,P)=\kappa(P,N),
\qquad
\kappa(N\cup\{z\},P)=\kappa(P,N\cup\{z\}),
\qquad
\kappa(N,P\cup\{z\})=\kappa(P\cup\{z\},N).
$$

Thus global bit-flip swaps $K_{+}$ and $K_{-}$ for each cylinder. The quantity

$$
\min\{K_{+}(\Gamma),K_{-}(\Gamma)\}
$$

used by $\operatorname{lgactc}$ is unchanged, and the quantity

$$
K_{0}(\Gamma)+\min\{K_{+}(\Gamma),K_{-}(\Gamma)\}
$$

used by $\operatorname{xactc}$ is also unchanged. The transformation is reversible, so both optimized costs are invariant.

### Lemma 4. Restrictions

Let $R$ be obtained by fixing coordinates outside a free set $J$ to values $\xi_i$. Restrict a strict score $S$ for $T$ to this subcube.

The affine part restricts to an affine form $A_J$ on the free coordinates, with

$$
\lvert L(A_J)\rvert\leq\lvert L(A)\rvert
$$

and

$$
\eta_{\oplus}(A_J)\leq\eta_{\oplus}(A).
$$

For a cylinder $C_{P,N}$, if a fixed coordinate conflicts with the cylinder, then the cylinder is identically $0$ on the restriction and can be dropped. Otherwise it restricts to

$$
C_{P\cap J,N\cap J}.
$$

The lifted local costs cannot increase:

$$
\kappa(P\cap J,N\cap J)
\leq
\kappa(P,N),
$$

and

$$
\kappa((P\cap J)\cup\{z\},N\cap J)
\leq
\kappa(P\cup\{z\},N),
$$

and

$$
\kappa(P\cap J,(N\cap J)\cup\{z\})
\leq
\kappa(P,N\cup\{z\}).
$$

Therefore the restricted score gives a feasible strict affine-cylinder score for $R$ whose $\operatorname{lgactc}$ and $\operatorname{xactc}$ costs are no larger than those of the original score for $T$. Minimizing over scores for $T$ proves restriction monotonicity.

### Lemma 5. Dummy feature variables

Let $U(y,w)=T(y)$. Any strict affine-cylinder score for $T$ extends to one for $U$ by giving every dummy coordinate zero affine slope and by using the same cylinders on the $y$ coordinates. The two optimized costs are unchanged, so

$$
\operatorname{lgactc}(U)\leq\operatorname{lgactc}(T),
\qquad
\operatorname{xactc}(U)\leq\operatorname{xactc}(T).
$$

Conversely, restricting the dummy block of $U$ to any fixed value recovers $T$. Lemma 4 gives the reverse inequalities. Hence dummy feature variables do not change either optimized cost.

Combining Lemmas 1 through 5 proves the statement. $\blacksquare$

## Consequences

The exactness target

$$
\operatorname{xactc}(T)=\deg_{\pm}(T)+1
$$

is stable under output complement, feature-coordinate relabeling, global feature bit-flip, and dummy feature extension. It is also restriction-monotone on the upper-bound side, so any feature restriction with large optimized one-bit cost is a valid obstruction to small optimized one-bit cost for the original feature.
