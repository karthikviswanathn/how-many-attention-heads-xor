# Almost All Boolean Functions Need Exponentially Many Heads

## Statement

Let $H^{\ast}(f)$ be the least number of heads needed by the one-layer attention model of [model.md](../../model.md) to compute a Boolean function $f : \{0,1\}^{n} \to \{0,1\}$, with final strict thresholding at the query token.

There is an absolute constant $c>0$ such that, for a uniformly random Boolean function $f : \{0,1\}^{n} \to \{0,1\}$,

$$
\Pr\left[H^{\ast}(f) \geq c\frac{2^n}{n^2}\right] \to 1
$$

as $n\to\infty$.

Consequently the worst-case head complexity satisfies

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f) \geq c\frac{2^n}{n^2},
$$

after decreasing $c$ over finitely many initial values of $n$ if one wants the display for every $n \geq 1$. Lemma 9 gives the universal upper bound

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f) \leq 2^n-1.
$$

## Proof

All logarithms are base $2$. Put

$$
Q_n := \{0,1\}^{n}, \qquad \mathcal B_n := \{f : Q_n \to \{0,1\}\}.
$$

Since $\lvert Q_n\rvert=2^n$, we have

$$
\lvert\mathcal B_n\rvert = 2^{2^n}.
$$

For $H\geq 1$, define the class of functions computable with at most $H$ heads by

$$
\mathcal F_{n,H} := \{f\in\mathcal B_n : H^{\ast}(f)\leq H\}.
$$

### Lemma 1. Low-head counting input

**Claim.** There is an absolute constant $C\geq 1$ such that, for all $n\geq 1$ and $H\geq 1$,

$$
\log_2\lvert\mathcal F_{n,H}\rvert
\leq C H n\bigl(n+\log_2(H+1)\bigr).
$$

**Proof.** This is Lemma 19, after replacing its absolute constant by the maximum of that constant and $1$. Enlarging the constant only increases the right-hand side, so the estimate remains valid.

Set

$$
c_0 := \frac{1}{6C}.
$$

Then $0<c_0\leq 1/6$. For each $n$, let

$$
a_n := c_0\frac{2^n}{n^2}, \qquad H_n := \lfloor a_n\rfloor.
$$

Since $2^n/n^2\to\infty$, there is $n_0$ such that $H_n\geq 1$ for all $n\geq n_0$.

Fix $n\geq n_0$. Since $c_0<1$ and $n^2\geq 1$, we have $a_n<2^n$. As $2^n$ is an integer and $H_n=\lfloor a_n\rfloor$, it follows that

$$
H_n\leq 2^n-1.
$$

Thus $H_n+1\leq 2^n$, and hence

$$
\log_2(H_n+1)\leq n.
$$

Applying Lemma 1 with $H=H_n$ gives

$$
\begin{aligned}
\log_2\lvert\mathcal F_{n,H_n}\rvert
&\leq C H_n n\bigl(n+\log_2(H_n+1)\bigr)\\
&\leq C a_n n(n+n)\\
&=2C a_n n^2\\
&=2C\left(c_0\frac{2^n}{n^2}\right)n^2\\
&=2Cc_0\,2^n\\
&=\frac{1}{3}2^n.
\end{aligned}
$$

Let $f$ be uniformly random in $\mathcal B_n$. Then

$$
\Pr[H^{\ast}(f)\leq H_n]
=
\frac{\lvert\mathcal F_{n,H_n}\rvert}{\lvert\mathcal B_n\rvert}
\leq
\frac{2^{(1/3)2^n}}{2^{2^n}}
=
2^{-(2/3)2^n}.
$$

The right-hand side tends to $0$.

Because $H^{\ast}(f)$ is integer-valued, the implication

$$
H^{\ast}(f)<a_n \implies H^{\ast}(f)\leq \lfloor a_n\rfloor = H_n
$$

holds. Therefore

$$
\Pr\left[H^{\ast}(f)<c_0\frac{2^n}{n^2}\right]
\leq
\Pr[H^{\ast}(f)\leq H_n]
\leq
2^{-(2/3)2^n}.
$$

Taking complements gives

$$
\Pr\left[H^{\ast}(f)\geq c_0\frac{2^n}{n^2}\right] \to 1.
$$

This proves the almost-all lower bound.

## Consequence

For all sufficiently large $n$, the event above has positive probability. Hence there is at least one Boolean function $f : \{0,1\}^{n}\to\{0,1\}$ with

$$
H^{\ast}(f)\geq c_0\frac{2^n}{n^2}.
$$

Thus

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f)
\geq
c_0\frac{2^n}{n^2}
$$

for all sufficiently large $n$.

If the displayed worst-case lower bound is required for every $n\geq 1$, shrink the constant over the finite set $1\leq n<n_0$. This preserves a positive absolute constant and does not affect the probability limit.

Finally, Lemma 9 gives, for every Boolean function $f : \{0,1\}^{n}\to\{0,1\}$,

$$
H^{\ast}(f)\leq 2^n-1.
$$

Taking the maximum over all $f$ yields

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f)
\leq
2^n-1.
$$

Therefore almost all Boolean functions require $\Omega(2^n/n^2)$ heads, while every Boolean function is computable with at most $2^n-1$ heads. $\blacksquare$
