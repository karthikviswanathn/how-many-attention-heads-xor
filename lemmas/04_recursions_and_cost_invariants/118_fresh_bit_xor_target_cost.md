# Fresh-Bit XOR Target Cost

## Statement

For a strict affine-cylinder score

$$
S(y)=A(y)+\sum_{\gamma\in\Gamma}c_{\gamma}C_{\gamma}(y),
\qquad
A(y)=a+\sum_{i=1}^{m}\alpha_i y_i,
$$

define

$$
L(A):=\{i:\alpha_i\neq0\},
$$

$$
K_{0}(\Gamma):=\sum_{\gamma=(P,N)\in\Gamma}\kappa(P,N),
\qquad
K_{+}(\Gamma):=\sum_{\gamma=(P,N)\in\Gamma}\kappa(P\cup\{z\},N),
\qquad
K_{-}(\Gamma):=\sum_{\gamma=(P,N)\in\Gamma}\kappa(P,N\cup\{z\}),
$$

and

$$
\eta_{\oplus}(A)
:=
\mathbf{1}\!\left[
a\neq0
\text{ or }
\exists i,\ \alpha_i\neq0
\right].
$$

Define

$$
\operatorname{xactc}(T)
:=
\min_S
\left(
\eta_{\oplus}(A)
+
\lvert L(A)\rvert
+
K_{0}(\Gamma)
+
\min\{K_{+}(\Gamma),K_{-}(\Gamma)\}
\right),
$$

where the minimum ranges over all strict affine-cylinder scores $S$ for $T$.

Then

$$
\deg_{\pm}(T)+1
\leq
H^{*}(z\oplus T(y))
\leq
\operatorname{xactc}(T),
$$

and the same bounds hold for $1-(z\oplus T(y))$.

Consequently, if

$$
\operatorname{xactc}(T)=\deg_{\pm}(T)+1,
$$

then fresh-bit XOR and XNOR over $T$ have exact head complexity $\deg_{\pm}(T)+1$.

Moreover,

$$
\operatorname{xactc}(T)
\leq
1+m+3\operatorname{actc}(T).
$$

> **Interpretation.** The XOR target cost is the optimized affine-cylinder quantity that must match threshold degree to solve the fresh-bit XOR recursion exactly for a feature.

## Proof

Fix a strict affine-cylinder score $S$ for $T$. The fresh-bit XOR affine-cylinder bound [113_fresh_bit_xor_affine_cylinder_bound.md](113_fresh_bit_xor_affine_cylinder_bound.md) gives

$$
\deg_{\pm}(T)+1
\leq
H^{*}(z\oplus T)
\leq
\eta_{\oplus}(A)
+
\lvert L(A)\rvert
+
K_{0}(\Gamma)
+
K_{+}(\Gamma).
$$

Applying the same bound after flipping the fresh coordinate $z$ gives the same upper bound with $K_{-}(\Gamma)$ in place of $K_{+}(\Gamma)$, because $zC_{P,N}$ is replaced by $(1-z)C_{P,N}=C_{P,N\cup\{z\}}$. Fresh-coordinate bit-flip turns XOR into XNOR, and output complement preserves head complexity, so both orientations are valid for the XOR and XNOR pair.

Hence

$$
\deg_{\pm}(T)+1
\leq
H^{*}(z\oplus T)
\leq
\eta_{\oplus}(A)
+
\lvert L(A)\rvert
+
K_{0}(\Gamma)
+
\min\{K_{+}(\Gamma),K_{-}(\Gamma)\}.
$$

Minimizing the upper bound over $S$ gives

$$
H^{*}(z\oplus T)
\leq
\operatorname{xactc}(T).
$$

The XNOR case follows by the same output-complement argument.

If $\operatorname{xactc}(T)=\deg_{\pm}(T)+1$, the lower and upper bounds meet, proving exactness.

For the comparison with $\operatorname{actc}$, choose a strict affine-cylinder score $S$ for $T$ of optimal affine-cylinder cost and write

$$
K(\Gamma):=\sum_{\gamma=(P,N)\in\Gamma}\kappa(P,N).
$$

Then $K_{0}(\Gamma)=K(\Gamma)\leq\operatorname{actc}(T)$, while

$$
\eta_{\oplus}(A)\leq1,
\qquad
\lvert L(A)\rvert\leq m,
$$

and

$$
\min\{K_{+}(\Gamma),K_{-}(\Gamma)\}
\leq
2K(\Gamma).
$$

Therefore

$$
\operatorname{xactc}(T)
\leq
1+m+3\operatorname{actc}(T).
$$

$\blacksquare$

## Consequences

The two optimized one-bit costs now split the non-XOR and XOR cases:

$$
H^{*}(r\wedge T),\ H^{*}(r\vee T)
\leq
1+\operatorname{lgactc}(T),
$$

while

$$
\deg_{\pm}(T)+1
\leq
H^{*}(z\oplus T)
\leq
\operatorname{xactc}(T).
$$

Thus the exact fresh-bit XOR problem becomes the concrete equality problem

$$
\operatorname{xactc}(T)=\deg_{\pm}(T)+1.
$$
