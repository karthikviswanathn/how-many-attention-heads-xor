# Active-Junta Support-Size Upper Bound

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), with a final strict linear readout at the query token. A Boolean function $f : \{0,1\}^{n} \to \{0,1\}$ is computable with $H$ heads if some choice of embeddings, attention parameters, and final strict linear readout computes it on the Boolean cube. Let $H^{\ast}(f)$ be the least such $H$.

Let $f$ depend only on a coordinate set $I\subseteq\{1,\ldots,n\}$ with $|I|=k$. Thus there is an induced function $g:\{0,1\}^{I}\to\{0,1\}$ such that

$$
f(x)=g(x_I)
$$

for every $x\in\{0,1\}^{n}$. Define

$$
a=|\{u\in\{0,1\}^{I}:g(u)=1\}|,
\qquad
b=2^k-a.
$$

Then

$$
H^{\ast}(f)\leq \min\{2a,2b,2^k-1\}.
$$

In particular, if the active truth table of $f$ has at most $r$ ones or at most $r$ zeros, then

$$
H^{\ast}(f)\leq 2r.
$$

## Proof

The two fibers of $g$ partition $\{0,1\}^{I}$, so

$$
a+b=2^k.
$$

If $k=0$, then $\{0,1\}^{I}$ has one element and $f$ is constant. A constant Boolean function is computable with $0$ heads by a constant strict readout score, so

$$
H^{\ast}(f)=0.
$$

Also $2^k-1=0$, hence the desired bound holds in this case.

Assume from now on that $k\geq1$. Enumerate

$$
I=\{i_1,\ldots,i_k\}.
$$

Define positive active weights

$$
\lambda_{i_r}=2^{r-1}
\qquad
\text{for } r\in\{1,\ldots,k\},
$$

and define

$$
t_I(u)=\sum_{r=1}^{k}2^{r-1}u_{i_r}.
$$

### Lemma 1. Binary weights are injective

The map $t_I:\{0,1\}^{I}\to\mathbb{R}$ is injective, and its image is exactly $\{0,\ldots,2^k-1\}$.

**Proof.** Let $u\neq v$ in $\{0,1\}^{I}$. Let $m$ be the largest index such that $u_{i_m}\neq v_{i_m}$. Then

$$
t_I(u)-t_I(v)
=
2^{m-1}(u_{i_m}-v_{i_m})
+
\sum_{r=1}^{m-1}2^{r-1}(u_{i_r}-v_{i_r}).
$$

The first term has absolute value $2^{m-1}$. The remaining sum has absolute value at most

$$
\sum_{r=1}^{m-1}2^{r-1}=2^{m-1}-1.
$$

By the reverse triangle inequality,

$$
|t_I(u)-t_I(v)|\geq 2^{m-1}-(2^{m-1}-1)=1.
$$

Thus $t_I(u)\neq t_I(v)$, so $t_I$ is injective.

For every $u\in\{0,1\}^{I}$, the value $t_I(u)$ is an integer between $0$ and

$$
\sum_{r=1}^{k}2^{r-1}=2^k-1.
$$

Since $t_I$ injects a set of size $2^k$ into the set $\{0,\ldots,2^k-1\}$, its image is all of $\{0,\ldots,2^k-1\}$. This proves the lemma. $\blacksquare$

Define $G:\operatorname{Im}(t_I)\to\{0,1\}$ by

$$
G(t_I(u))=g(u).
$$

This is well-defined because $t_I$ is injective. Also $g(u)=G(t_I(u))$ for every $u\in\{0,1\}^{I}$. Therefore Lemma 32, the active-junta weighted-sum sign-change upper bound, applies and gives

$$
H^{\ast}(f)\leq C_{t_I}(G),
$$

where $C_{t_I}(G)$ is the number of sign changes of $G$ along the ordered image of $t_I$.

Let

$$
N=2^k,
$$

and define the binary string

$$
w_j=G(j)
\qquad
\text{for } j\in\{0,\ldots,N-1\}.
$$

By Lemma 1, $t_I$ is a bijection from $\{0,1\}^{I}$ to $\{0,\ldots,N-1\}$. Hence the string $w_0,\ldots,w_{N-1}$ has exactly $a$ ones and exactly $b$ zeros.

Define the transition set

$$
T=\{j\in\{1,\ldots,N-1\}:w_{j-1}\neq w_j\}.
$$

Because the ordered image of $t_I$ is $0<1<\cdots<N-1$,

$$
C_{t_I}(G)=|T|.
$$

### Lemma 2. Transition count from support size

For the binary string $w_0,\ldots,w_{N-1}$ with $a$ ones and $b$ zeros,

$$
|T|\leq \min\{2a,2b,N-1\}.
$$

**Proof.** First, $T\subseteq\{1,\ldots,N-1\}$, so

$$
|T|\leq N-1.
$$

Next count transitions by their one endpoints. For every $j\in T$, exactly one of $w_{j-1}$ and $w_j$ is equal to $1$. Thus each transition contributes exactly one incident one endpoint. A fixed position $s$ with $w_s=1$ can be incident to at most two transitions, namely $j=s$ and $j=s+1$ when those indices lie in $\{1,\ldots,N-1\}$. Since there are $a$ positions with value $1$,

$$
|T|\leq 2a.
$$

The same argument with zero endpoints gives

$$
|T|\leq 2b,
$$

because every transition has exactly one incident zero endpoint and each zero position is incident to at most two transitions. Combining the three bounds proves the lemma. $\blacksquare$

Combining Lemma 32 with Lemma 2 gives

$$
H^{\ast}(f)
\leq C_{t_I}(G)
=|T|
\leq \min\{2a,2b,N-1\}
=\min\{2a,2b,2^k-1\}.
$$

This proves the support-size upper bound.

## Consequence

If the active truth table has at most $r$ ones, then $a\leq r$, and the bound above gives

$$
H^{\ast}(f)\leq 2a\leq 2r.
$$

If the active truth table has at most $r$ zeros, then $b\leq r$, and the same bound gives

$$
H^{\ast}(f)\leq 2b\leq 2r.
$$

Therefore every active truth table with at most $r$ ones or at most $r$ zeros satisfies $H^{\ast}(f)\leq 2r$. $\blacksquare$
