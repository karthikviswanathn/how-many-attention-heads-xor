# Homogeneous Polarity Boolean Minors Do Not Increase Head Complexity

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), with a final strict threshold at the query token. Let $H^{\ast}(f)$ be the least number of heads needed to compute a Boolean function $f$.

For

$$
f : \{0,1\}^{n} \to \{0,1\},
$$

define the antipodal input complement

$$
f^{\dagger}(x_1,\ldots,x_n)=f(1-x_1,\ldots,1-x_n).
$$

Then

$$
H^{\ast}(f^{\dagger})=H^{\ast}(f).
$$

Consequently, let

$$
g : \{0,1\}^{m} \to \{0,1\}
$$

be obtained from $f$ by a homogeneous-polarity Boolean minor. This means that each input coordinate of $f$ is replaced either by a constant in $\{0,1\}$ or by an unnegated coordinate $y_j$, with repetitions allowed, or else each nonconstant input coordinate is replaced by a negated coordinate $1-y_j$, again with repetitions allowed. Then

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

For $x\in\{0,1\}^{n}$ define

$$
\bar x=(1-x_1,\ldots,1-x_n).
$$

### Lemma 1. Antipodal input complement preserves head complexity

**Claim.** For every Boolean function $f:\{0,1\}^{n}\to\{0,1\}$,

$$
H^{\ast}(f^{\dagger})=H^{\ast}(f).
$$

**Proof.** Let

$$
K:=H^{\ast}(f).
$$

Choose a $K$-head model $M$ computing $f$. Write its token embeddings as

$$
e_0,e_1,e_=,
$$

its positional embeddings as

$$
p_1,\ldots,p_n,p_=,
$$

and its score as

$$
S(x)=w^{\top}r(x)-\tau.
$$

Thus, for every $x\in\{0,1\}^{n}$,

$$
S(x)>0 \Longleftrightarrow f(x)=1.
$$

Construct a new $K$-head model $M^{\dagger}$ with the same dimensions, positional embeddings, head matrices, output projections, readout vector, and threshold as $M$, but with token embeddings

$$
e^{\dagger}_0=e_1,
\qquad
e^{\dagger}_1=e_0,
\qquad
e^{\dagger}_=e_=.
$$

We compare the computation of $M^{\dagger}$ on $x$ with the computation of $M$ on $\bar x$. For every input coordinate $i\in[n]$,

$$
u_i^{\dagger}(x)=e^{\dagger}_{x_i}+p_i=e_{1-x_i}+p_i=u_i(\bar x).
$$

At the query token,

$$
u_=^{\dagger}(x)=e^{\dagger}_=+p_==e_=+p_==u_=(\bar x),
$$

because $u_=$ is independent of the input bits. Therefore, for every head $h$,

$$
q^{\dagger,(h)}(x)=q^{(h)}(\bar x).
$$

Also, for every position $j\in\{1,\ldots,n,=\}$ and every head $h$,

$$
k_j^{\dagger,(h)}(x)=k_j^{(h)}(\bar x),
\qquad
v_j^{\dagger,(h)}(x)=v_j^{(h)}(\bar x).
$$

Hence the attention logits agree:

$$
\ell_j^{\dagger,(h)}(x)
=
\bigl(q^{\dagger,(h)}(x)\bigr)^{\top}k_j^{\dagger,(h)}(x)
=
\bigl(q^{(h)}(\bar x)\bigr)^{\top}k_j^{(h)}(\bar x)
=
\ell_j^{(h)}(\bar x).
$$

The softmax weights are functions of the whole logit vector, so

$$
\alpha_j^{\dagger,(h)}(x)=\alpha_j^{(h)}(\bar x)
$$

for every $j$ and $h$. Combining this with the equality of value vectors gives

$$
\widetilde y^{\dagger,(h)}(x)=\widetilde y^{(h)}(\bar x),
\qquad
y^{\dagger,(h)}(x)=y^{(h)}(\bar x).
$$

Therefore the query residual streams agree:

$$
\begin{aligned}
r^{\dagger}(x)
&=u_=^{\dagger}(x)+\sum_{h=1}^{K}y^{\dagger,(h)}(x) \\
&=u_=(\bar x)+\sum_{h=1}^{K}y^{(h)}(\bar x) \\
&=r(\bar x).
\end{aligned}
$$

For $K=0$, the same displayed equality holds with the empty sum. If $S^{\dagger}$ is the score of $M^{\dagger}$, then

$$
S^{\dagger}(x)=w^{\top}r^{\dagger}(x)-\tau=w^{\top}r(\bar x)-\tau=S(\bar x).
$$

Since $M$ computes $f$,

$$
S^{\dagger}(x)>0
\Longleftrightarrow
S(\bar x)>0
\Longleftrightarrow
f(\bar x)=1
\Longleftrightarrow
f^{\dagger}(x)=1.
$$

Thus $M^{\dagger}$ computes $f^{\dagger}$ with $K$ heads. Hence

$$
H^{\ast}(f^{\dagger})\leq H^{\ast}(f).
$$

Since $\overline{\bar x}=x$ for every Boolean vector $x$, we have

$$
(f^{\dagger})^{\dagger}=f.
$$

Applying the already proved inequality to $f^{\dagger}$ gives

$$
H^{\ast}(f)\leq H^{\ast}(f^{\dagger}).
$$

The two inequalities imply

$$
H^{\ast}(f^{\dagger})=H^{\ast}(f).
$$

This proves the claim. $\blacksquare$

### Lemma 2. Homogeneous negated minors become positive minors after reflection

**Claim.** If $g$ is obtained from $f$ by substituting only constants and negated variables, then $g$ is a positive Boolean minor of $f^{\dagger}$.

**Proof.** Write the given substitution into $f$ as

$$
g(y)=f(s_1(y),\ldots,s_n(y)),
$$

where each $s_i$ is either a constant $c_i\in\{0,1\}$ or a negated variable $1-y_j$.

Define functions $w_i:\{0,1\}^{m}\to\{0,1\}$ by

$$
w_i(y)=
\begin{cases}
1-c_i, & \text{if } s_i(y)=c_i,\\
y_j, & \text{if } s_i(y)=1-y_j.
\end{cases}
$$

Each $w_i$ is either a constant or an unnegated input coordinate. Hence the map $y\mapsto(w_1(y),\ldots,w_n(y))$ is a positive minor substitution into $f^{\dagger}$.

For every coordinate $i$,

$$
1-w_i(y)=s_i(y).
$$

Therefore, for every $y\in\{0,1\}^{m}$,

$$
\begin{aligned}
f^{\dagger}(w_1(y),\ldots,w_n(y))
&=f(1-w_1(y),\ldots,1-w_n(y)) \\
&=f(s_1(y),\ldots,s_n(y)) \\
&=g(y).
\end{aligned}
$$

Thus $g$ is a positive Boolean minor of $f^{\dagger}$. $\blacksquare$

We now finish the proof of the theorem. If $g$ is obtained from $f$ by substituting constants and unnegated variables, then $g$ is a positive Boolean minor of $f$. By Lemma 34,

$$
H^{\ast}(g)\leq H^{\ast}(f).
$$

If $g$ is obtained from $f$ by substituting constants and negated variables, Lemma 2 shows that $g$ is a positive Boolean minor of $f^{\dagger}$. By Lemma 34,

$$
H^{\ast}(g)\leq H^{\ast}(f^{\dagger}).
$$

By Lemma 1,

$$
H^{\ast}(f^{\dagger})=H^{\ast}(f).
$$

Combining these gives

$$
H^{\ast}(g)\leq H^{\ast}(f).
$$

This proves the homogeneous-polarity minor monotonicity statement. $\blacksquare$

## Consequence

The invariant $H^{\ast}$ is unchanged by simultaneous complementation of all input coordinates and is monotone under Boolean minors whose nonconstant substitutions all have one common polarity. Equivalently, Lemma 34 extends from positive minors to the positive-minor relation enlarged by the global reflection

$$
x\mapsto \bar x.
$$

Thus any lower bound proved for a homogeneous-polarity minor $g$ of $f$ is also a lower bound for $f$. This leaves mixed coordinate negations as the separate boundary case not covered by this lemma. $\blacksquare$
