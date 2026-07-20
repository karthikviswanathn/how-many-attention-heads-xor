# Indexing Functions Have Parity Restriction Lower Bounds

## Statement

Let $m \geq 1$ and put $A:=\{0,1\}^{m}$. Define the indexing function

$$
\mathrm{IND}_m : A \times \{0,1\}^{A} \to \{0,1\}
$$

by

$$
\mathrm{IND}_m(a,y)=y_a,
$$

where $a\in A$ is the address and $y=(y_b)_{b\in A}$ is the data table.

Let $H^{\ast}(f)$ denote the minimum number of heads needed to compute $f$ in the one-layer attention model of [../../model.md](../../model.md). Equivalently, by Lemma 10, $H^{\ast}$ is the invariant characterized by the linear-fractional normal form.

For every Boolean function $g:A\to\{0,1\}$, fixing the data table to the truth table of $g$ gives a subcube restriction of $\mathrm{IND}_m$ which is exactly $g$ on the address variables. Consequently,

$$
H^{\ast}(\mathrm{IND}_m)
\geq
\max_{g:\{0,1\}^{m}\to\{0,1\}} H^{\ast}(g).
$$

In particular,

$$
H^{\ast}(\mathrm{IND}_m) \geq m.
$$

## Proof

Let $g:A\to\{0,1\}$ be arbitrary. Define the fixed data table $y^{g}\in\{0,1\}^{A}$ by

$$
y^{g}_b:=g(b)
\qquad\text{for every } b\in A.
$$

Define the embedding

$$
r_g:A\to A\times\{0,1\}^{A}
$$

by

$$
r_g(a):=(a,y^{g}).
$$

This embedding leaves all $m$ address coordinates free and fixes every data coordinate $y_b$ to the constant $g(b)$.

### Lemma 1. Truth-table restriction

The subcube restriction of $\mathrm{IND}_m$ along $r_g$ is exactly $g$.

**Proof.** For every $a\in A$,

$$
\begin{aligned}
\mathrm{IND}_m(r_g(a))
&= \mathrm{IND}_m(a,y^{g}) \\
&= y^{g}_a \\
&= g(a).
\end{aligned}
$$

The first equality is the definition of $r_g$, the second is the definition of $\mathrm{IND}_m$, and the third is the definition of $y^{g}$. Thus the restricted function $a\mapsto \mathrm{IND}_m(r_g(a))$ agrees with $g$ at every address $a\in A$. $\blacksquare$

### Lemma 2. Transfer of lower bounds

For every Boolean function $g:A\to\{0,1\}$,

$$
H^{\ast}(g)\leq H^{\ast}(\mathrm{IND}_m).
$$

**Proof.** By Lemma 1, $g$ is obtained from $\mathrm{IND}_m$ by fixing coordinates, namely all data-table coordinates, and using the identity relabeling on the remaining address coordinates. Lemma 26, equivalently Lemma 27, gives subcube restriction monotonicity:

$$
H^{\ast}(g)\leq H^{\ast}(\mathrm{IND}_m).
$$

$\blacksquare$

Since $g:A\to\{0,1\}$ was arbitrary, Lemma 2 implies

$$
H^{\ast}(\mathrm{IND}_m)
\geq
\max_{g:\{0,1\}^{m}\to\{0,1\}} H^{\ast}(g).
$$

Now choose

$$
g=\mathrm{XOR}_m.
$$

By Lemma 8,

$$
H^{\ast}(\mathrm{XOR}_m)=m.
$$

Therefore

$$
m
=
H^{\ast}(\mathrm{XOR}_m)
\leq
H^{\ast}(\mathrm{IND}_m).
$$

This proves

$$
H^{\ast}(\mathrm{IND}_m)\geq m.
$$

$\blacksquare$

## Consequence

The same restriction argument transfers any lower bound for an $m$-variable Boolean function to the indexing function on $m$ address bits. In particular, Lemma 24 or Lemma 25 gives an absolute constant $c>0$ such that, for all sufficiently large $m$,

$$
\max_{g:\{0,1\}^{m}\to\{0,1\}} H^{\ast}(g)
\geq
c\frac{2^m}{m^2}.
$$

Hence

$$
H^{\ast}(\mathrm{IND}_m)
=
\Omega\!\left(\frac{2^m}{m^2}\right).
$$
