# Subcube Restriction Monotonicity

## Statement

Let $f : \{0,1\}^{n} \to \{0,1\}$ be a Boolean function. Let $g : \{0,1\}^{m} \to \{0,1\}$ be obtained from $f$ by fixing any subset of the input coordinates to constants in $\{0,1\}$ and relabeling the remaining $m$ free coordinates.

Let $H^{\ast}(h)$ denote the least number of heads needed to compute $h$ in the one-layer attention model of [model.md](../../model.md). Equivalently, by Lemma 10, $H^{\ast}(h)=L_{\mathrm{frac}}(h)$.

Then

$$
H^{\ast}(g) \leq H^{\ast}(f).
$$

In particular, every subcube restriction of $f$ gives a valid lower-bound certificate for $f$: if $H^{\ast}(g) \geq r$, then $H^{\ast}(f) \geq r$.

## Proof

For an integer $q\geq 0$, write

$$
[q] := \{1,\ldots,q\},
\qquad
[0] := \varnothing.
$$

Let $S\subseteq [n]$ be the set of free coordinates. Let $\beta : [m]\to S$ be a bijection from the relabeled coordinates to the free coordinates. For each frozen coordinate $i\in [n]\setminus S$, let $a_i\in \{0,1\}$ be the fixed value.

Define the subcube embedding $R : \{0,1\}^{m}\to \{0,1\}^{n}$ by

$$
R(y)_i :=
\begin{cases}
y_j, & \text{if } i=\beta(j) \text{ for some } j\in [m],\\
a_i, & \text{if } i\in [n]\setminus S.
\end{cases}
$$

By the definition of the restricted function,

$$
g(y)=f(R(y))
$$

for every $y\in \{0,1\}^{m}$.

Set

$$
K := H^{\ast}(f).
$$

By Lemma 10, $H^{\ast}(f)=L_{\mathrm{frac}}(f)$. Hence there are a constant $c\in\mathbb{R}$ and $K$ one-head linear-fractional atoms $\phi_1,\ldots,\phi_K$ such that

$$
f(x)=1
\qquad\Longleftrightarrow\qquad
c+\sum_{h=1}^{K}\phi_h(x)>0
$$

for every $x\in \{0,1\}^{n}$. For each $h\in [K]$, write

$$
\phi_h(x)
=
\frac{
\eta_h+\sum_{i=1}^{n}\rho_{h,i}\alpha_h^{x_i}(\mu_{h,i}+\delta_h x_i)
}{
\gamma_h+\sum_{i=1}^{n}\rho_{h,i}\alpha_h^{x_i}
},
$$

where

$$
\gamma_h>0,
\qquad
\rho_{h,i}>0,
\qquad
\alpha_h>0,
$$

and

$$
\eta_h,\delta_h,\mu_{h,i}\in\mathbb{R}.
$$

### Lemma 1. Frozen coordinates preserve atoms

For each $h\in [K]$, define

$$
\gamma'_h
:=
\gamma_h+\sum_{i\in [n]\setminus S}\rho_{h,i}\alpha_h^{a_i},
$$

$$
\eta'_h
:=
\eta_h+\sum_{i\in [n]\setminus S}\rho_{h,i}\alpha_h^{a_i}(\mu_{h,i}+\delta_h a_i),
$$

and, for $j\in [m]$,

$$
\rho'_{h,j}:=\rho_{h,\beta(j)},
\qquad
\mu'_{h,j}:=\mu_{h,\beta(j)},
\qquad
\alpha'_h:=\alpha_h,
\qquad
\delta'_h:=\delta_h.
$$

Then

$$
\psi_h(y)
:=
\frac{
\eta'_h+\sum_{j=1}^{m}\rho'_{h,j}(\alpha'_h)^{y_j}(\mu'_{h,j}+\delta'_h y_j)
}{
\gamma'_h+\sum_{j=1}^{m}\rho'_{h,j}(\alpha'_h)^{y_j}
}
$$

is a valid one-head linear-fractional atom on $\{0,1\}^{m}$.

**Proof.** Since $a_i\in \{0,1\}$ and $\alpha_h>0$, each factor $\alpha_h^{a_i}$ is positive. Therefore each product $\rho_{h,i}\alpha_h^{a_i}$ is positive, and the finite sum

$$
\sum_{i\in [n]\setminus S}\rho_{h,i}\alpha_h^{a_i}
$$

is nonnegative. Hence

$$
\gamma'_h
=
\gamma_h+\sum_{i\in [n]\setminus S}\rho_{h,i}\alpha_h^{a_i}
>0.
$$

Also, for every $j\in [m]$,

$$
\rho'_{h,j}=\rho_{h,\beta(j)}>0,
\qquad
\alpha'_h=\alpha_h>0.
$$

All other displayed parameters are real. Thus $\psi_h$ has exactly the one-head atom form required in the definition of $L_{\mathrm{frac}}$ on $m$ variables. $\blacksquare$

### Lemma 2. Restricted atoms agree on the subcube

For every $h\in [K]$ and every $y\in \{0,1\}^{m}$,

$$
\psi_h(y)=\phi_h(R(y)).
$$

**Proof.** Expand the numerator of $\phi_h(R(y))$ and split the finite sum over the disjoint partition $[n]=S\cup([n]\setminus S)$. Since $S=\beta([m])$, we get

$$
\begin{aligned}
&\eta_h+\sum_{i=1}^{n}\rho_{h,i}\alpha_h^{R(y)_i}(\mu_{h,i}+\delta_h R(y)_i) \\
&=\eta_h+
\sum_{i\in [n]\setminus S}\rho_{h,i}\alpha_h^{a_i}(\mu_{h,i}+\delta_h a_i)
+
\sum_{j=1}^{m}\rho_{h,\beta(j)}\alpha_h^{y_j}(\mu_{h,\beta(j)}+\delta_h y_j) \\
&=\eta'_h+
\sum_{j=1}^{m}\rho'_{h,j}(\alpha'_h)^{y_j}(\mu'_{h,j}+\delta'_h y_j).
\end{aligned}
$$

The denominator is the same calculation without the value factor:

$$
\begin{aligned}
\gamma_h+\sum_{i=1}^{n}\rho_{h,i}\alpha_h^{R(y)_i}
&=
\gamma_h+
\sum_{i\in [n]\setminus S}\rho_{h,i}\alpha_h^{a_i}
+
\sum_{j=1}^{m}\rho_{h,\beta(j)}\alpha_h^{y_j} \\
&=
\gamma'_h+
\sum_{j=1}^{m}\rho'_{h,j}(\alpha'_h)^{y_j}.
\end{aligned}
$$

These are exactly the numerator and denominator defining $\psi_h(y)$, so $\psi_h(y)=\phi_h(R(y))$. $\blacksquare$

Now fix $y\in \{0,1\}^{m}$. Using the definition of $g$, the $K$-atom representation of $f$, and Lemma 2,

$$
\begin{aligned}
g(y)=1
&\Longleftrightarrow f(R(y))=1 \\
&\Longleftrightarrow c+\sum_{h=1}^{K}\phi_h(R(y))>0 \\
&\Longleftrightarrow c+\sum_{h=1}^{K}\psi_h(y)>0.
\end{aligned}
$$

By Lemma 1, each $\psi_h$ is a valid one-head atom on $m$ variables. Therefore $g$ has a $K$-atom linear-fractional representation, with the same threshold constant $c$. Hence

$$
L_{\mathrm{frac}}(g)\leq K.
$$

Applying Lemma 10 again gives

$$
H^{\ast}(g)
=
L_{\mathrm{frac}}(g)
\leq K
=
H^{\ast}(f).
$$

This proves the monotonicity inequality.

## Consequence

If $H^{\ast}(g)\geq r$, then the inequality just proved gives

$$
r\leq H^{\ast}(g)\leq H^{\ast}(f).
$$

By transitivity, $H^{\ast}(f)\geq r$. Thus every subcube restriction of $f$ supplies a valid lower-bound certificate for $f$. $\blacksquare$
