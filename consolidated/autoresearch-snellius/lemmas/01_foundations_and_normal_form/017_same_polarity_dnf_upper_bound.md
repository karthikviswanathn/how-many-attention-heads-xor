# Same-Polarity DNF Subcube Upper Bound

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), and let $H^{\ast}(f)$ be the least number of attention heads needed to compute $f : \{0,1\}^{n} \to \{0,1\}$ with a final strict threshold at the query token.

Let $s\geq 1$, fix a polarity $\zeta\in\{0,1\}$, and let $A_1,\ldots,A_s\subseteq\{1,\ldots,n\}$ be nonempty coordinate sets. Define

$$
f(x)=\bigvee_{r=1}^{s}\bigwedge_{i\in A_r}\mathbf{1}[x_i=\zeta].
$$

Then

$$
H^{\ast}(f)\leq s.
$$

Equivalently, any union of $s$ coordinate subcubes all anchored at the all-ones vertex, or all anchored at the all-zeros vertex, is computable with at most one head per subcube.

## Proof

Let

$$
Q:=\{0,1\}^{n}.
$$

By Lemma 10, it is enough to construct $s$ one-head atoms $\phi_1,\ldots,\phi_s$ and a constant $c$ such that

$$
f(x)=1 \qquad\Longleftrightarrow\qquad c+\sum_{r=1}^{s}\phi_r(x)>0
$$

for every $x\in Q$.

For each coordinate, define the violation indicator

$$
\nu_i(x)=
\begin{cases}
x_i, & \zeta=0,\\
1-x_i, & \zeta=1.
\end{cases}
$$

Thus $\nu_i(x)=0$ exactly when $x_i=\zeta$. For each term, define

$$
V_r(x):=\sum_{i\in A_r}\nu_i(x).
$$

The $r$th DNF term is true exactly when $V_r(x)=0$.

Since some $A_r$ is nonempty, $n\geq 1$. Set

$$
\lambda:=2s,
\qquad
\mu:=\frac{1}{2n}.
$$

For each $r$ and $i$, define

$$
\beta_{r,i}:=
\begin{cases}
\lambda, & i\in A_r,\\
\mu, & i\notin A_r.
\end{cases}
$$

Finally set

$$
D_r(x):=1+\sum_{i=1}^{n}\beta_{r,i}\nu_i(x),
\qquad
\phi_r(x):=\frac{1}{D_r(x)}.
$$

### Lemma 1. The fractions are one-head atoms

**Claim.** For each $r$, the function $\phi_r$ is a valid one-head atom.

**Proof.** All coefficients $\beta_{r,i}$ are positive. If $\zeta=0$, then

$$
D_r(x)=1+\sum_{i=1}^{n}\beta_{r,i}x_i.
$$

This is an affine denominator with positive constant coefficient and strictly positive coordinate coefficients.

If $\zeta=1$, then

$$
D_r(x)=1+\sum_{i=1}^{n}\beta_{r,i}(1-x_i)
=1+\sum_{i=1}^{n}\beta_{r,i}-\sum_{i=1}^{n}\beta_{r,i}x_i.
$$

This is an affine denominator with strictly negative coordinate coefficients and all-ones value $1>0$.

In either case, Lemma 13 says that $D_r$ is an admissible nonconstant one-head denominator. Lemma 13 also says that, for a nonconstant admissible denominator, any affine numerator is allowed. Taking the constant numerator $N_r(x)=1$ gives the one-head atom

$$
\phi_r(x)=\frac{N_r(x)}{D_r(x)}.
$$

$\blacksquare$

### Lemma 2. True terms give large bumps

**Claim.** If the $r$th DNF term is true at $x$, then

$$
\phi_r(x)\geq \frac{2}{3}.
$$

**Proof.** If the $r$th term is true, then $V_r(x)=0$, so all violated-literal indicators inside $A_r$ vanish. Therefore

$$
D_r(x)=1+\mu\sum_{i\notin A_r}\nu_i(x).
$$

Since each $\nu_i(x)$ is Boolean,

$$
\sum_{i\notin A_r}\nu_i(x)\leq n.
$$

Hence

$$
D_r(x)\leq 1+\mu n=1+\frac{1}{2}=\frac{3}{2}.
$$

The denominator is positive, so

$$
\phi_r(x)=\frac{1}{D_r(x)}\geq \frac{2}{3}.
$$

$\blacksquare$

### Lemma 3. False terms give small bumps

**Claim.** If the $r$th DNF term is false at $x$, then

$$
\phi_r(x)\leq \frac{1}{2s+1}.
$$

**Proof.** If the $r$th term is false, then $V_r(x)\geq 1$ because $V_r(x)$ is an integer violation count. Since the outside summands in $D_r$ are nonnegative,

$$
D_r(x)\geq 1+\lambda V_r(x)\geq 1+\lambda=2s+1.
$$

The denominator is positive, so

$$
\phi_r(x)=\frac{1}{D_r(x)}\leq \frac{1}{2s+1}.
$$

$\blacksquare$

### Lemma 4. The sum computes the disjunction

Define

$$
S(x):=\sum_{r=1}^{s}\phi_r(x)-\frac{7}{12}.
$$

**Claim.** For every $x\in Q$,

$$
f(x)=1 \qquad\Longleftrightarrow\qquad S(x)>0.
$$

**Proof.** If $f(x)=1$, then at least one DNF term is true. For such an index $r$, Lemma 2 and positivity of all $\phi_q$ give

$$
\sum_{q=1}^{s}\phi_q(x)\geq \phi_r(x)\geq \frac{2}{3}>\frac{7}{12}.
$$

Thus $S(x)>0$.

If $f(x)=0$, then every DNF term is false. By Lemma 3,

$$
\sum_{r=1}^{s}\phi_r(x)
\leq \sum_{r=1}^{s}\frac{1}{2s+1}
=\frac{s}{2s+1}.
$$

Also

$$
\frac{s}{2s+1}<\frac{7}{12},
$$

because multiplying by the positive quantity $12(2s+1)$ gives $12s<14s+7$. Hence $S(x)<0$.

The two cases prove the claimed strict threshold representation. $\blacksquare$

### Conclusion

The score $S$ is a constant plus a sum of $s$ one-head atoms. By Lemma 10, the one-layer attention model computes $f$ with at most $s$ heads. Therefore

$$
H^{\ast}(f)\leq s.
$$

$\blacksquare$

## Consequence

For a fixed polarity $\zeta$, every union of $s$ coordinate subcubes anchored at the corresponding Boolean vertex has an $s$-head construction. The construction uses one head per subcube and a final strict threshold on the sum of the resulting one-sided bump atoms.
