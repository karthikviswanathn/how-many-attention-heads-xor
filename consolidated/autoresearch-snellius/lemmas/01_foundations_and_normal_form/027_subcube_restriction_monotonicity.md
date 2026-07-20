# Subcube Restriction Monotonicity

## Statement

Let $f : \{0,1\}^{n} \to \{0,1\}$ be a Boolean function. Let $g : \{0,1\}^{m} \to \{0,1\}$ be obtained from $f$ by fixing any subset of the input coordinates to constants in $\{0,1\}$ and relabeling the remaining $m$ free coordinates.

Here $H^{\ast}(h)$ denotes the minimum number of heads needed to compute $h$ in the one-layer attention model of [model.md](../../model.md). Equivalently, by Lemma 10, $H^{\ast}(h)=L_{\mathrm{frac}}(h)$.

Then

$$
H^{\ast}(g) \leq H^{\ast}(f).
$$

In particular, every subcube restriction of $f$ gives a valid lower-bound certificate for $f$: if $H^{\ast}(g) \geq r$, then $H^{\ast}(f) \geq r$.

## Proof

For $q\geq 0$, write

$$
[q] := \{1,\ldots,q\},
\qquad
[0] := \varnothing.
$$

Let $S\subseteq [n]$ be the set of free coordinates, so $|S|=m$. Let $\sigma : [m]\to S$ be a bijection giving the relabeling of the free coordinates. Let

$$
F := [n]\setminus S
$$

be the set of fixed coordinates, and let $a : F\to \{0,1\}$ assign the fixed Boolean value to each fixed coordinate.

Define the subcube embedding $\iota : \{0,1\}^{m}\to \{0,1\}^{n}$ by

$$
\iota(y)_i :=
\begin{cases}
y_j, & \text{if } i=\sigma(j) \text{ for some } j\in [m],\\
a_i, & \text{if } i\in F.
\end{cases}
$$

By definition of the restricted function,

$$
g(y)=f(\iota(y))
$$

for every $y\in \{0,1\}^{m}$.

Set

$$
K := L_{\mathrm{frac}}(f).
$$

By Lemma 10, $K=H^{\ast}(f)$. By the definition of $L_{\mathrm{frac}}(f)$, there are $K$ fractional atoms $A_1,\ldots,A_K$ and a threshold constant $\theta\in\mathbb{R}$ such that, for every $x\in\{0,1\}^{n}$,

$$
f(x)=1
\qquad\Longleftrightarrow\qquad
\theta+\sum_{\ell=1}^{K} A_\ell(x)>0.
$$

For each $\ell\in [K]$, write the atom in the Lemma 10 normal form as

$$
A_\ell(x)
=
\frac{
\eta_\ell+
\sum_{i=1}^{n}
\rho_{\ell,i}\alpha_\ell^{x_i}(m_{\ell,i}+\delta_\ell x_i)
}{
\gamma_\ell+
\sum_{i=1}^{n}\rho_{\ell,i}\alpha_\ell^{x_i}
},
$$

where $\eta_\ell,\delta_\ell,m_{\ell,i}\in\mathbb{R}$, $\gamma_\ell>0$, $\rho_{\ell,i}>0$, and $\alpha_\ell>0$.

### Lemma 1. Frozen coordinates preserve atoms

For each $\ell\in [K]$, define

$$
\gamma'_\ell
:=
\gamma_\ell+
\sum_{i\in F}\rho_{\ell,i}\alpha_\ell^{a_i},
$$

and

$$
\eta'_\ell
:=
\eta_\ell+
\sum_{i\in F}
\rho_{\ell,i}\alpha_\ell^{a_i}(m_{\ell,i}+\delta_\ell a_i).
$$

For $j\in [m]$, define

$$
\rho'_{\ell,j}:=\rho_{\ell,\sigma(j)},
\qquad
m'_{\ell,j}:=m_{\ell,\sigma(j)},
\qquad
\alpha'_\ell:=\alpha_\ell,
\qquad
\delta'_\ell:=\delta_\ell.
$$

Then

$$
A'_\ell(y)
:=
\frac{
\eta'_\ell+
\sum_{j=1}^{m}
\rho'_{\ell,j}(\alpha'_\ell)^{y_j}(m'_{\ell,j}+\delta'_\ell y_j)
}{
\gamma'_\ell+
\sum_{j=1}^{m}\rho'_{\ell,j}(\alpha'_\ell)^{y_j}
}
$$

is a valid fractional atom on $m$ variables.

**Proof.** Since $a_i\in\{0,1\}$ and $\alpha_\ell>0$, each factor $\alpha_\ell^{a_i}$ is positive. Since $\rho_{\ell,i}>0$, each product $\rho_{\ell,i}\alpha_\ell^{a_i}$ is positive. Hence the finite sum over $F$ is nonnegative, and

$$
\gamma'_\ell
=
\gamma_\ell+
\sum_{i\in F}\rho_{\ell,i}\alpha_\ell^{a_i}
>0.
$$

For each $j\in [m]$, the definitions give

$$
\rho'_{\ell,j}>0,
\qquad
\alpha'_\ell>0.
$$

All remaining displayed parameters are real. Therefore $A'_\ell$ satisfies the same admissibility conditions as a Lemma 10 fractional atom on $m$ variables. $\blacksquare$

### Lemma 2. Restricted atoms agree on the subcube

For every $\ell\in [K]$ and every $y\in \{0,1\}^{m}$,

$$
A'_\ell(y)=A_\ell(\iota(y)).
$$

**Proof.** Substitute $x=\iota(y)$ into the denominator of $A_\ell$ and split the sum over the disjoint union $[n]=F\cup S$:

$$
\begin{aligned}
\gamma_\ell+
\sum_{i=1}^{n}\rho_{\ell,i}\alpha_\ell^{\iota(y)_i}
&=
\gamma_\ell+
\sum_{i\in F}\rho_{\ell,i}\alpha_\ell^{a_i}
+
\sum_{j=1}^{m}\rho_{\ell,\sigma(j)}\alpha_\ell^{y_j} \\
&=
\gamma'_\ell+
\sum_{j=1}^{m}\rho'_{\ell,j}(\alpha'_\ell)^{y_j}.
\end{aligned}
$$

The numerator is the same substitution with the linear value factors included:

$$
\begin{aligned}
&\eta_\ell+
\sum_{i=1}^{n}
\rho_{\ell,i}\alpha_\ell^{\iota(y)_i}(m_{\ell,i}+\delta_\ell\iota(y)_i) \\
&=\eta_\ell+
\sum_{i\in F}
\rho_{\ell,i}\alpha_\ell^{a_i}(m_{\ell,i}+\delta_\ell a_i)
+
\sum_{j=1}^{m}
\rho_{\ell,\sigma(j)}\alpha_\ell^{y_j}(m_{\ell,\sigma(j)}+\delta_\ell y_j) \\
&=\eta'_\ell+
\sum_{j=1}^{m}
\rho'_{\ell,j}(\alpha'_\ell)^{y_j}(m'_{\ell,j}+\delta'_\ell y_j).
\end{aligned}
$$

These are exactly the denominator and numerator defining $A'_\ell(y)$. Thus $A'_\ell(y)=A_\ell(\iota(y))$. $\blacksquare$

Now fix $y\in \{0,1\}^{m}$. Using the definition of $g$, the $K$-atom representation of $f$, and Lemma 2,

$$
\begin{aligned}
g(y)=1
&\Longleftrightarrow f(\iota(y))=1 \\
&\Longleftrightarrow \theta+\sum_{\ell=1}^{K}A_\ell(\iota(y))>0 \\
&\Longleftrightarrow \theta+\sum_{\ell=1}^{K}A'_\ell(y)>0.
\end{aligned}
$$

By Lemma 1, each $A'_\ell$ is a valid fractional atom on $m$ variables. Therefore $g$ has a $K$-atom fractional representation, so

$$
L_{\mathrm{frac}}(g)\leq K=L_{\mathrm{frac}}(f).
$$

Applying Lemma 10 to both $f$ and $g$ gives

$$
H^{\ast}(g)\leq H^{\ast}(f).
$$

## Consequence

If $H^{\ast}(g)\geq r$, then the monotonicity inequality gives

$$
r\leq H^{\ast}(g)\leq H^{\ast}(f).
$$

By transitivity, $H^{\ast}(f)\geq r$. Thus every subcube restriction of $f$ supplies a valid lower-bound certificate for $f$. $\blacksquare$
