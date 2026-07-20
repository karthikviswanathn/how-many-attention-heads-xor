# Coordinate Subcube Indicators Have One Head

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), with a final strict threshold at the query token. Let $H^{\ast}(f)$ be the least number of heads needed to compute a Boolean function $f$, with $H^{\ast}(f)=0$ allowed exactly for constant functions.

Let $P,N\subseteq\{1,\ldots,n\}$ be disjoint coordinate sets, and define

$$
\chi_{P,N}(x)=\mathbf{1}\left[x_i=1\text{ for all }i\in P\text{ and }x_j=0\text{ for all }j\in N\right].
$$

If $P\cup N=\emptyset$, then

$$
H^{\ast}(\chi_{P,N})=0.
$$

If $P\cup N\neq\emptyset$, then

$$
H^{\ast}(\chi_{P,N})=1.
$$

> **Equivalently.** Every nontrivial conjunction of arbitrary signed literals is exactly a one-head function.

## Proof

We use Lemma 11, the exact one-head characterization:

$$
H^{\ast}(f)=0 \Longleftrightarrow f \text{ is constant},
$$

and

$$
H^{\ast}(f)=1 \Longleftrightarrow f \text{ is a nonconstant linear threshold function}.
$$

Define the affine function

$$
L(x)=\sum_{i\in P}x_i-\sum_{j\in N}x_j-\left(|P|-\frac12\right).
$$

### Lemma 1. The subcube indicator is an affine threshold

**Claim.** For every $x\in\{0,1\}^{n}$,

$$
\chi_{P,N}(x)=1 \Longleftrightarrow L(x)>0.
$$

**Proof.** First suppose the defining subcube condition holds. Then $x_i=1$ for every $i\in P$ and $x_j=0$ for every $j\in N$. Hence

$$
\sum_{i\in P}x_i=|P|,
\qquad
\sum_{j\in N}x_j=0.
$$

Substitution gives

$$
\begin{aligned}
L(x)
&=\sum_{i\in P}x_i-\sum_{j\in N}x_j-\left(|P|-\frac12\right) \\
&=|P|-0-\left(|P|-\frac12\right) \\
&=\frac12.
\end{aligned}
$$

Thus $L(x)>0$.

Conversely, suppose the defining subcube condition fails. Then either there is some $i\in P$ with $x_i=0$, or there is some $j\in N$ with $x_j=1$.

If there is $i\in P$ with $x_i=0$, then all summands are in $\{0,1\}$ and at least one of the $|P|$ summands over $P$ is zero. Therefore

$$
\sum_{i\in P}x_i\leq |P|-1.
$$

Also $\sum_{j\in N}x_j\geq 0$. Hence

$$
\begin{aligned}
L(x)
&=\sum_{i\in P}x_i-\sum_{j\in N}x_j-\left(|P|-\frac12\right) \\
&\leq (|P|-1)-0-\left(|P|-\frac12\right) \\
&=-\frac12.
\end{aligned}
$$

So $L(x)>0$ is false in this case.

If there is $j\in N$ with $x_j=1$, then

$$
\sum_{j\in N}x_j\geq 1,
\qquad
\sum_{i\in P}x_i\leq |P|.
$$

Therefore

$$
\begin{aligned}
L(x)
&=\sum_{i\in P}x_i-\sum_{j\in N}x_j-\left(|P|-\frac12\right) \\
&\leq |P|-1-\left(|P|-\frac12\right) \\
&=-\frac12.
\end{aligned}
$$

Again $L(x)>0$ is false.

Thus the defining condition for $\chi_{P,N}(x)$ holds exactly when $L(x)>0$. This proves the claim. $\blacksquare$

Now consider the two cases.

If $P\cup N=\emptyset$, the defining condition is an empty finite conjunction. It is true for every $x\in\{0,1\}^{n}$. Hence $\chi_{P,N}$ is the constant one function. By Lemma 11,

$$
H^{\ast}(\chi_{P,N})=0.
$$

Assume instead that $P\cup N\neq\emptyset$. Lemma 1 shows that $\chi_{P,N}$ is a linear threshold function. It remains only to check that it is nonconstant.

Choose $k\in P\cup N$. Define $a\in\{0,1\}^{n}$ by setting $a_i=1$ for $i\in P$ and $a_j=0$ for $j\in N$, with arbitrary values outside $P\cup N$. Then

$$
\chi_{P,N}(a)=1.
$$

Define $b\in\{0,1\}^{n}$ by changing the relevant literal at coordinate $k$: if $k\in P$, set $b_k=0$ and keep all other constrained coordinates as in $a$; if $k\in N$, set $b_k=1$ and keep all other constrained coordinates as in $a$. Since $P$ and $N$ are disjoint, this makes one required literal fail. Therefore

$$
\chi_{P,N}(b)=0.
$$

Thus $\chi_{P,N}$ is nonconstant. Since it is also a linear threshold function, Lemma 11 gives

$$
H^{\ast}(\chi_{P,N})=1.
$$

Combining the two cases proves the theorem. $\blacksquare$

## Consequence

Every signed coordinate subcube indicator is at the zero-head or one-head level:

$$
H^{\ast}(\chi_{P,N})=
\begin{cases}
0, & \text{if } P\cup N=\emptyset,\\
1, & \text{if } P\cup N\neq\emptyset.
\end{cases}
$$

In particular, every nontrivial conjunction of arbitrary signed literals is exactly a one-head function.
