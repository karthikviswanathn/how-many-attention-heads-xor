# Positive Boolean Minors Do Not Increase Head Complexity

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), with a final strict threshold at the query token. Let $H^{\ast}(f)$ be the least number of heads needed to compute a Boolean function $f$.

Let

$$
f : \{0,1\}^{n} \to \{0,1\}
$$

be a Boolean function. Let $\tau : \{1,\ldots,n\} \to \{\mathbf 0,\mathbf 1\}\sqcup\{1,\ldots,m\}$ be a positive minor map, where $\mathbf 0$ and $\mathbf 1$ denote the two constant symbols. For $y\in\{0,1\}^{m}$ define

$$
z_i(y)=
\begin{cases}
0, & \text{if } \tau(i)=\mathbf 0,\\
1, & \text{if } \tau(i)=\mathbf 1,\\
y_{\tau(i)}, & \text{if } \tau(i)\in\{1,\ldots,m\}.
\end{cases}
$$

Define

$$
g(y)=f(z_1(y),\ldots,z_n(y)).
$$

Then

$$
H^{\ast}(g)\leq H^{\ast}(f).
$$

## Proof

For an integer $q\geq 0$, write

$$
[q]:=\{1,\ldots,q\},
\qquad
[0]:=\varnothing.
$$

We use Lemma 10 in the following form. For every Boolean function $F$, the value $H^{\ast}(F)$ equals $L_{\mathrm{frac}}(F)$, the least number of one-head atoms needed in a strict sign representation. Each atom has the form

$$
\phi_h(x)=
\frac{
\eta_h+\sum_i \rho_{h,i}\alpha_h^{x_i}(m_{h,i}+\delta_h x_i)
}{
\gamma_h+\sum_i \rho_{h,i}\alpha_h^{x_i}
},
$$

where

$$
\gamma_h>0,
\qquad
\rho_{h,i}>0,
\qquad
\alpha_h>0.
$$

Let

$$
C:=\{i\in[n]:\tau(i)\in\{\mathbf 0,\mathbf 1\}\}.
$$

For $i\in C$, let $a_i\in\{0,1\}$ be the constant selected by $\tau(i)$, so $\tau(i)=\mathbf 0$ when $a_i=0$ and $\tau(i)=\mathbf 1$ when $a_i=1$.

Let

$$
J:=\{j\in[m]:\text{there is } i\in[n] \text{ with } \tau(i)=j\}.
$$

These are the active coordinates of $y$ that are actually used by the minor.

If $J=\varnothing$, then every $z_i(y)$ is constant. Hence $g$ is constant. A constant Boolean function is computed with zero heads by a constant strict readout, so

$$
H^{\ast}(g)=0\leq H^{\ast}(f).
$$

This proves the case with no active variables. Assume from now on that $J\neq\varnothing$.

Set $r:=|J|$, and choose a bijection

$$
\nu:[r]\to J.
$$

For each $q\in[r]$, define

$$
G_q:=\{i\in[n]:\tau(i)=\nu(q)\}.
$$

By the definition of $J$, each $G_q$ is nonempty. The sets

$$
C,G_1,\ldots,G_r
$$

are pairwise disjoint and partition $[n]$.

Define the active-variable function

$$
g_0:\{0,1\}^{r}\to\{0,1\}
$$

by

$$
g_0(u)=f(z^0_1(u),\ldots,z^0_n(u)),
$$

where

$$
z^0_i(u)=
\begin{cases}
a_i, & \text{if } i\in C,\\
u_q, & \text{if } i\in G_q.
\end{cases}
$$

Set

$$
K:=H^{\ast}(f).
$$

By Lemma 10, there are $K$ atoms $\phi_1,\ldots,\phi_K$ and a constant $c\in\mathbb R$ such that, for every $x\in\{0,1\}^{n}$,

$$
f(x)=1
\Longleftrightarrow
c+\sum_{h=1}^{K}\phi_h(x)>0.
$$

We will substitute the active minor into each atom and show that the result is still an admissible atom.

### Lemma 1. Merged active coordinates preserve atoms

Fix $h\in[K]$. Define

$$
\gamma'_h:=\gamma_h+\sum_{i\in C}\rho_{h,i}\alpha_h^{a_i},
$$

$$
\eta'_h:=\eta_h+\sum_{i\in C}\rho_{h,i}\alpha_h^{a_i}(m_{h,i}+\delta_h a_i).
$$

For $q\in[r]$, define

$$
\rho'_{h,q}:=\sum_{i\in G_q}\rho_{h,i},
\qquad
m'_{h,q}:=\frac{\sum_{i\in G_q}\rho_{h,i}m_{h,i}}{\rho'_{h,q}}.
$$

Also set

$$
\alpha'_h:=\alpha_h,
\qquad
\delta'_h:=\delta_h.
$$

Then

$$
\psi_h(u):=
\frac{
\eta'_h+\sum_{q=1}^{r}\rho'_{h,q}(\alpha'_h)^{u_q}(m'_{h,q}+\delta'_h u_q)
}{
\gamma'_h+\sum_{q=1}^{r}\rho'_{h,q}(\alpha'_h)^{u_q}
}
$$

is a valid one-head atom on $\{0,1\}^{r}$.

**Proof.** Since each $G_q$ is nonempty and each $\rho_{h,i}>0$,

$$
\rho'_{h,q}=\sum_{i\in G_q}\rho_{h,i}>0.
$$

Since $\alpha_h>0$ and $a_i\in\{0,1\}$, each $\alpha_h^{a_i}$ is positive. Hence each product $\rho_{h,i}\alpha_h^{a_i}$ is positive, and the finite sum over $C$ is nonnegative. Therefore

$$
\gamma'_h=\gamma_h+\sum_{i\in C}\rho_{h,i}\alpha_h^{a_i}>0.
$$

Also $\alpha'_h=\alpha_h>0$. All remaining displayed parameters are real. Thus $\psi_h$ has the required one-head atom form. $\blacksquare$

### Lemma 2. The merged atoms agree with the substituted atoms

For every $h\in[K]$ and every $u\in\{0,1\}^{r}$,

$$
\psi_h(u)=\phi_h(z^0(u)).
$$

**Proof.** Expand the numerator of $\phi_h(z^0(u))$ and split the finite sum using the partition $[n]=C\sqcup G_1\sqcup\cdots\sqcup G_r$:

$$
\begin{aligned}
&\eta_h+\sum_{i=1}^{n}\rho_{h,i}\alpha_h^{z^0_i(u)}(m_{h,i}+\delta_h z^0_i(u)) \\
&=\eta'_h+\sum_{q=1}^{r}\sum_{i\in G_q}\rho_{h,i}\alpha_h^{u_q}(m_{h,i}+\delta_h u_q) \\
&=\eta'_h+\sum_{q=1}^{r}\alpha_h^{u_q}\left(\sum_{i\in G_q}\rho_{h,i}m_{h,i}+\delta_h u_q\sum_{i\in G_q}\rho_{h,i}\right) \\
&=\eta'_h+\sum_{q=1}^{r}\rho'_{h,q}\alpha_h^{u_q}(m'_{h,q}+\delta_h u_q).
\end{aligned}
$$

The denominator satisfies the same partition calculation without the value factor:

$$
\begin{aligned}
\gamma_h+\sum_{i=1}^{n}\rho_{h,i}\alpha_h^{z^0_i(u)}
&=\gamma'_h+\sum_{q=1}^{r}\sum_{i\in G_q}\rho_{h,i}\alpha_h^{u_q} \\
&=\gamma'_h+\sum_{q=1}^{r}\rho'_{h,q}\alpha_h^{u_q}.
\end{aligned}
$$

Since $\alpha'_h=\alpha_h$ and $\delta'_h=\delta_h$, these are exactly the numerator and denominator defining $\psi_h(u)$. Therefore $\psi_h(u)=\phi_h(z^0(u))$. $\blacksquare$

Now fix $u\in\{0,1\}^{r}$. By the definition of $g_0$, the representation of $f$, and Lemma 2,

$$
\begin{aligned}
g_0(u)=1
&\Longleftrightarrow f(z^0(u))=1 \\
&\Longleftrightarrow c+\sum_{h=1}^{K}\phi_h(z^0(u))>0 \\
&\Longleftrightarrow c+\sum_{h=1}^{K}\psi_h(u)>0.
\end{aligned}
$$

By Lemma 1, every $\psi_h$ is a valid one-head atom on the active cube. Hence

$$
L_{\mathrm{frac}}(g_0)\leq K.
$$

Using Lemma 10 again,

$$
H^{\ast}(g_0)=L_{\mathrm{frac}}(g_0)\leq K=H^{\ast}(f).
$$

It remains to return from the active coordinates $J$ to all $m$ coordinates. For $y\in\{0,1\}^{m}$, let

$$
P(y):=(y_{\nu(1)},\ldots,y_{\nu(r)}).
$$

Then

$$
g(y)=g_0(P(y)).
$$

The coordinates in $[m]\setminus J$ are irrelevant, and the order of the active coordinates is just the order chosen by $\nu$. By Lemma 31, adding irrelevant variables and permuting coordinates do not change head complexity. Therefore

$$
H^{\ast}(g)=H^{\ast}(g_0).
$$

Combining this equality with the active-variable bound gives

$$
H^{\ast}(g)\leq H^{\ast}(f).
$$

## Consequence

Fixing coordinates, permuting coordinates, duplicating coordinates, and identifying coordinates are all special cases of positive minor maps. In the atom proof above, fixing coordinates is absorbed into $\gamma'_h$ and $\eta'_h$, while duplicating or identifying coordinates merges the corresponding positive weights into $\rho'_{h,q}$. Unused output coordinates are precisely the variables in $[m]\setminus J$, and Lemma 31 removes them without changing $H^{\ast}$.

Thus positive Boolean minors do not increase head complexity. $\blacksquare$
