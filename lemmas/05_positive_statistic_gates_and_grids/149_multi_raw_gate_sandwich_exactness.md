# Multi-Raw Gate Sandwich And Single-Slice Exactness

## Statement

Let

$$
T(y)=F(t(y)),
\qquad
t(y)=\sum_{i=1}^{m}\lambda_i y_i,
\qquad
\lambda_i>0,
$$

be a nonconstant positive-statistic feature. Write the image of $t$ as

$$
\tau_0<\tau_1<\cdots<\tau_{M-1},
$$

and let $C$ be the sign-change count of $F$ along this image. Put

$$
e_{\min}:=F(\tau_0),
\qquad
e_{\max}:=F(\tau_{M-1}).
$$

For a Boolean gate

$$
G:\{0,1\}^{k}\times\{0,1\}\to\{0,1\},
$$

define

$$
H_G(z,y):=G(z,T(y)),
$$

and write

$$
g_e(a):=G(a,e)
\qquad
\text{for }e\in\{0,1\}.
$$

Let

$$
N_G:=\left\lvert\{a\in\{0,1\}^{k}:g_0(a)\neq g_1(a)\}\right\rvert.
$$

Then the following sandwich holds:

$$
\max\left\{
\mathbf{1}_{N_G>0}H^{*}(T),
H^{*}(g_0),
H^{*}(g_1)
\right\}
\leq
H^{*}(H_G)
\leq
N_GC+B_{+}(g_{e_{\max}},g_{e_{\min}}).
$$

Here $\mathbf{1}_{N_G>0}H^{*}(T)$ means $0$ if $N_G=0$ and $H^{*}(T)$ otherwise.

In particular, if

$$
H^{*}(T)=C,
\qquad
N_G=1,
\qquad
B_{+}(g_{e_{\max}},g_{e_{\min}})=0,
$$

then

$$
H^{*}(H_G)=C.
$$

> **Interpretation.** Multi-raw gates over one positive-statistic feature have a usable two-sided bracket. If exactly one raw slice depends on the feature and the endpoint boundary can be made silent, the upper bound is exact whenever the feature itself is exact.

## Proof

The upper bound is exactly the positive mixed boundary gate bound [145_positive_mixed_boundary_gate_bound.md](145_positive_mixed_boundary_gate_bound.md).

For the lower bounds, use restriction monotonicity from Lemma 28. Since $T$ is nonconstant, it attains both values $0$ and $1$ on the finite cube.

Fix $e\in\{0,1\}$ and choose $y^{(e)}$ such that

$$
T(y^{(e)})=e.
$$

Restricting $H_G$ to this value of $y$ gives the raw function

$$
z\mapsto G(z,e)=g_e(z).
$$

Therefore

$$
H^{*}(g_e)\leq H^{*}(H_G)
$$

for $e=0,1$.

If $N_G>0$, choose a raw assignment $a$ with

$$
g_0(a)\neq g_1(a).
$$

Then the one-variable slice

$$
y\mapsto G(a,T(y))
$$

is either $T(y)$ or $1-T(y)$. Complement invariance and restriction monotonicity give

$$
H^{*}(T)\leq H^{*}(H_G).
$$

Combining these lower bounds with the upper bound proves the sandwich.

Under the final hypotheses, the upper bound becomes

$$
H^{*}(H_G)\leq C.
$$

The lower bound from the dependent raw slice gives

$$
H^{*}(H_G)\geq H^{*}(T)=C.
$$

Thus $H^{*}(H_G)=C$. $\blacksquare$

## Consequence

This theorem turns the ordered-slice upper bounds into exact theorems whenever the feature is already solved and the raw gate has only one feature-dependent slice with no endpoint jump.
