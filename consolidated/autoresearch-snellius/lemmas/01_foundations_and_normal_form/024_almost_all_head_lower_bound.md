# Almost All Boolean Functions Need Exponentially Many Heads

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md). Let $H^{\ast}(f)$ denote the least number of heads needed to compute a Boolean function $f : \{0,1\}^{n} \to \{0,1\}$ with final strict thresholding at the query token.

There is an absolute constant $c>0$ such that, for a uniformly random Boolean function $f : \{0,1\}^{n} \to \{0,1\}$,

$$
\Pr\left[H^{\ast}(f) \geq c\frac{2^n}{n^2}\right] \to 1
$$

as $n\to\infty$.

Consequently, for all sufficiently large $n$,

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f) \geq c\frac{2^n}{n^2}.
$$

On the other hand, Lemma 9 gives the universal upper bound

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f) \leq 2^n-1.
$$

## Proof

Let $\mathcal B_n$ be the set of all Boolean functions $\{0,1\}^{n}\to\{0,1\}$. Since the Boolean cube has $2^n$ inputs, a Boolean function is an arbitrary assignment of one bit to each input, so

$$
|\mathcal B_n|=2^{2^n}.
$$

For $H\geq 1$, define

$$
\mathcal F_{n,H}:=\{f:\{0,1\}^{n}\to\{0,1\}:H^{\ast}(f)\leq H\}.
$$

By Lemma 19, there is an absolute constant $C_0>0$ such that, for all $n\geq 1$ and $H\geq 1$,

$$
\log_2 |\mathcal F_{n,H}|\leq C_0Hn\bigl(n+\log_2(H+1)\bigr).
$$

Increasing the constant if necessary, assume this bound holds with an absolute constant $C\geq 1$. Set

$$
a:=\frac{1}{6C}
$$

and, for each $n$, put

$$
H_n:=\left\lfloor a\frac{2^n}{n^2}\right\rfloor.
$$

Since $2^n/n^2\to\infty$, there is $n_0$ such that $H_n\geq 1$ for all $n\geq n_0$. For such $n$,

$$
H_n\leq a\frac{2^n}{n^2}.
$$

Also $a\leq 1$, so $H_n\leq 2^n$ and therefore

$$
H_n+1\leq 2^n+1\leq 2^{n+1}.
$$

Thus

$$
\log_2(H_n+1)\leq n+1.
$$

Applying Lemma 19 with $H=H_n$ gives, for $n\geq n_0$,

$$
\begin{aligned}
\log_2 |\mathcal F_{n,H_n}|
&\leq C H_n n\bigl(n+\log_2(H_n+1)\bigr) \\
&\leq C\left(a\frac{2^n}{n^2}\right)n(2n+1) \\
&= Ca2^n\left(2+\frac{1}{n}\right) \\
&\leq 3Ca2^n \\
&= \frac{1}{2}2^n.
\end{aligned}
$$

Hence

$$
|\mathcal F_{n,H_n}|\leq 2^{2^{n-1}}.
$$

If $f$ is uniformly random in $\mathcal B_n$, then

$$
\Pr[H^{\ast}(f)\leq H_n]
=
\frac{|\mathcal F_{n,H_n}|}{|\mathcal B_n|}
\leq
\frac{2^{2^{n-1}}}{2^{2^n}}
=
2^{-2^{n-1}}.
$$

The last quantity tends to $0$. Therefore

$$
\Pr[H^{\ast}(f)>H_n]\to 1.
$$

Since $H^{\ast}(f)$ is integer-valued and $H_n=\lfloor a2^n/n^2\rfloor$, the implication

$$
H^{\ast}(f)>H_n
\quad\Longrightarrow\quad
H^{\ast}(f)\geq a\frac{2^n}{n^2}
$$

holds. Consequently,

$$
\Pr\left[H^{\ast}(f)\geq a\frac{2^n}{n^2}\right]\to 1.
$$

This proves the probabilistic lower bound with the absolute constant $c=a=1/(6C)>0$.

For the worst-case lower bound, the probability in the last display is eventually positive. Hence, for all sufficiently large $n$, at least one Boolean function $f : \{0,1\}^{n}\to\{0,1\}$ satisfies

$$
H^{\ast}(f)\geq c\frac{2^n}{n^2}.
$$

Taking the maximum over all Boolean functions gives

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f)
\geq
c\frac{2^n}{n^2}
$$

for all sufficiently large $n$.

Finally, Lemma 9 gives, for every Boolean function $f : \{0,1\}^{n}\to\{0,1\}$,

$$
H^{\ast}(f)\leq 2^n-1.
$$

Taking the maximum over $f$ gives the stated universal upper bound. Thus almost every Boolean function requires $\Omega(2^n/n^2)$ heads, while every Boolean function is computable with at most $2^n-1$ heads. $\blacksquare$

## Consequence

The low-head classes occupy a vanishing fraction of all Boolean functions at the scale $H\asymp 2^n/n^2$:

$$
\frac{|\mathcal F_{n,\lfloor c\frac{2^n}{n^2}\rfloor}|}{2^{2^n}}\to 0.
$$

Thus the worst-case head complexity satisfies

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f)=\Omega\left(\frac{2^n}{n^2}\right),
$$

and Lemma 9 gives the complementary universal upper bound

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f)\leq 2^n-1.
$$
