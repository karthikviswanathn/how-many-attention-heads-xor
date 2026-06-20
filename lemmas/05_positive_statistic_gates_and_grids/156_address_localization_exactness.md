# Address Localization Exactness

## Statement

Let

$$
T(y)=F(t(y)),
\qquad
t(y)=\sum_{i=1}^{m}\lambda_i y_i,
\qquad
\lambda_i>0,
$$

have sign-change count $C$ along the ordered image of $t$. Let

$$
d:=\deg_{\pm}(T),
$$

and let

$$
e_0:=F(\tau_0),
\qquad
e_1:=F(\tau_{M-1})
$$

be the two endpoint labels. For a raw address $a\in\{0,1\}^{k}$, write

$$
M_a(z):=\mathbf{1}[z=a].
$$

If

$$
e_0=e_1=0,
$$

then

$$
d
\leq
H^{*}\bigl(M_a(z)\wedge T(y)\bigr)
\leq
C.
$$

If

$$
e_0=e_1=1,
$$

then

$$
d
\leq
H^{*}\bigl((1-M_a(z))\vee T(y)\bigr)
\leq
C.
$$

Consequently, in either case, if $\deg_{\pm}(T)=C$, then the corresponding localized gate has exact head complexity $C$.

More generally, if $R:\{0,1\}^{k}\to\{0,1\}$ is any raw mask with $r_1=\lvert R^{-1}(1)\rvert>0$ and $e_0=e_1=0$, then

$$
d
\leq
H^{*}\bigl(R(z)\wedge T(y)\bigr)
\leq
r_1C.
$$

If $r_0=\lvert R^{-1}(0)\rvert>0$ and $e_0=e_1=1$, then

$$
d
\leq
H^{*}\bigl(R(z)\vee T(y)\bigr)
\leq
r_0C.
$$

> **Interpretation.** A solved positive-statistic feature can be localized to one raw address at no extra head cost, provided the feature's endpoints match the inactive background label.

## Proof

Assume first that $e_0=e_1=0$. Apply the raw-mask endpoint bound [154_raw_mask_gate_endpoint_bounds.md](154_raw_mask_gate_endpoint_bounds.md) to $R=M_a$. Since

$$
\lvert M_a^{-1}(1)\rvert=1,
$$

the theorem gives

$$
H^{*}\bigl(M_a\wedge T\bigr)\leq C.
$$

For the lower bound, restrict the raw block to $z=a$. The restricted function is exactly $T(y)$. By restriction monotonicity and the threshold-degree lower bound,

$$
H^{*}\bigl(M_a\wedge T\bigr)
\geq
H^{*}(T)
\geq
\deg_{\pm}(T)
=d.
$$

This proves the first bracket.

Now assume that $e_0=e_1=1$. Apply Lemma 154 to the raw mask

$$
R=1-M_a.
$$

Here

$$
\lvert R^{-1}(0)\rvert=1,
$$

so

$$
H^{*}\bigl(R\vee T\bigr)\leq C.
$$

Restricting to $z=a$ again gives $T(y)$, and the same lower-bound argument gives

$$
d\leq H^{*}\bigl((1-M_a)\vee T\bigr).
$$

If $\deg_{\pm}(T)=C$, then the two inequalities match in the relevant case, proving exactness.

For a general raw mask $R$ with $r_1>0$ and $e_0=e_1=0$, Lemma 154 gives

$$
H^{*}(R\wedge T)\leq r_1C.
$$

Choose any raw assignment $a$ with $R(a)=1$. The restriction $z=a$ is $T$, so the same lower bound gives

$$
d\leq H^{*}(R\wedge T).
$$

The disjunction case is identical: if $r_0>0$ and $e_0=e_1=1$, Lemma 154 gives the upper bound $r_0C$, and any raw assignment with $R(a)=0$ restricts $R\vee T$ to $T$. $\blacksquare$

## Consequence

For every threshold-degree-tight positive-statistic feature with equal zero endpoints, a single-address conjunction preserves the exact value $H^{*}=C$. The dual statement holds for equal one endpoints and a single-address exception inside a disjunction.
