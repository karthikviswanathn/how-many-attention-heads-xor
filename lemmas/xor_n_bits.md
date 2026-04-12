# $n$-Bit XOR In One-Layer Attention

This note proves, carefully and without hidden steps, the following claim.

## Theorem

In the one-layer attention-only model from [problem_statement.md](../problem_statement.md), the $n$-bit parity / XOR function

$$\mathrm{XOR}_n(x_1, \ldots, x_n) = x_1 \oplus \cdots \oplus x_n$$

has exact head complexity

$$H^{*}(\mathrm{XOR}_n) = n.$$

The proof has two parts.

1. Every $H$-head classifier in this model has threshold degree at most $H$.
2. $n$-bit parity has threshold degree exactly $n$.
3. There is an explicit construction with $n$ heads.

The lower bound and the upper bound then match.

## Model Reminder

We work with inputs $x \in \{0,1\}^n$, encoded as the sequence

$$(x_1, \ldots, x_n, =).$$

There is:

1. one self-attention layer,
2. $H$ parallel heads,
3. no MLP,
4. a linear readout from the residual stream at the query token.

The query token embedding is constant across all inputs, so any constant contribution to the readout can be absorbed into the threshold.

## What Threshold Degree Means

Before starting the proof, we record the complexity measure used in the
lower bound.

### Definition

Let $f : \{0,1\}^n \to \{0,1\}$ be a Boolean function.

A real polynomial $P(x_1, \ldots, x_n)$ **sign-represents** $f$ on the
Boolean cube if

$$P(x) > 0 \quad \text{whenever } f(x) = 1,$$

and

$$P(x) < 0 \quad \text{whenever } f(x) = 0.$$

The **threshold degree** of $f$, denoted $\deg_{\pm}(f)$, is the minimum
degree of a real polynomial that sign-represents $f$.

### Why This Is The Right Notion Here

The classifier in our attention model has the form

$$\text{score}(x) > \tau.$$

After subtracting the threshold, this becomes

$$\text{score}(x) - \tau > 0.$$

So if we can turn the score function into a polynomial without changing
its sign on the Boolean cube, then we obtain a polynomial sign
representation of the computed Boolean function.

That is exactly why threshold degree is the right lower-bound notion for
this argument.

### Equivalent $\{-1,1\}$ Form

Sometimes it is cleaner to work with the sign-valued version of $f$:

$$\widetilde f(x) := \begin{cases}
+1 & \text{if } f(x)=1, \\
-1 & \text{if } f(x)=0.
\end{cases}$$

Then $P$ sign-represents $f$ if and only if

$$\widetilde f(x)\,P(x) > 0 \qquad \text{for all } x \in \{0,1\}^n.$$

We will use this reformulation when proving that parity has threshold
degree at least $n$.

## Part I: Lower Bound

We will prove:

> If a Boolean function is computable with $H$ heads in this model, then it has threshold degree at most $H$.

Then we will use the classical fact that parity has threshold degree exactly $n$.

### Lemma 1: On a finite domain, exact classification can be made strict

Let $X$ be a finite set, and let $f : X \to \{0,1\}$ be nonconstant. Suppose a real-valued score function $S$ and threshold $\tau$ satisfy

$$S(x) > \tau \quad \text{iff} \quad f(x) = 1.$$

Then there exists another threshold $\tau'$ such that

$$S(x) - \tau' > 0 \text{ when } f(x) = 1,$$

$$S(x) - \tau' < 0 \text{ when } f(x) = 0.$$

#### Proof

Define

$$m_{-} := \max \{ S(x) : f(x) = 0 \}, \qquad m_{+} := \min \{ S(x) : f(x) = 1 \}.$$

These quantities exist because $X$ is finite and both classes are nonempty.

From the hypothesis,

$$m_{-} \le \tau < m_{+}.$$

In particular $m_{-} < m_{+}$. Choose any $\tau'$ with

$$m_{-} < \tau' < m_{+}.$$

Then:

1. if $f(x) = 0$, then $S(x) \le m_{-} < \tau'$, so $S(x) - \tau' < 0$;
2. if $f(x) = 1$, then $S(x) \ge m_{+} > \tau'$, so $S(x) - \tau' > 0$.

This is exactly the desired strict sign separation.

### Lemma 2: The scalar contribution of one head is a ratio of affine functions

Fix one attention head $h$ and a linear probe vector $w$ on the final residual space.

Let $s_h(x)$ be the contribution of head $h$ to the final probe score on input $x \in \{0,1\}^n$.

Then there exist affine functions $a_h, b_h : \mathbb{R}^n \to \mathbb{R}$ such that on the Boolean cube:

$$s_h(x) = \frac{a_h(x)}{b_h(x)}$$

and

$$b_h(x) > 0 \quad \text{for every } x \in \{0,1\}^n.$$

#### Proof

Fix the head $h$.

For each input position $i$ and bit value $b \in \{0,1\}$, define:

$$\lambda_{i,b} := \exp(\text{logit of the query against position } i \text{ when } x_i = b).$$

This is a positive real number depending only on the head, the position, and the local token value.

Also define:

$$\mu_{i,b} := \langle w, \text{value written by position } i \text{ when } x_i = b \rangle.$$

This is again a fixed real number depending only on the head, the position, and the local token value.

Finally, for the query position `=`, define constants

$$\lambda_{=} > 0, \qquad \mu_{=} \in \mathbb{R}.$$

Now write the head's scalar score as

$$s_h(x) = \frac{N_h(x)}{D_h(x)}$$

where

$$D_h(x) = \lambda_{=} + \sum_{i=1}^{n} \lambda_{i,x_i},$$

$$N_h(x) = \lambda_{=} \, \mu_{=} + \sum_{i=1}^{n} \lambda_{i,x_i} \, \mu_{i,x_i}.$$

Because $x_i \in \{0,1\}$, each local term can be written as

$$\lambda_{i,x_i} = \lambda_{i,0}(1 - x_i) + \lambda_{i,1} x_i,$$

$$\lambda_{i,x_i} \, \mu_{i,x_i} = (\lambda_{i,0} \, \mu_{i,0})(1 - x_i) + (\lambda_{i,1} \, \mu_{i,1}) x_i.$$

So both $D_h$ and $N_h$ are affine functions of the variables $x_1, \ldots, x_n$.

Set

$$b_h := D_h, \qquad a_h := N_h.$$

Then $s_h(x) = a_h(x) / b_h(x)$ on the Boolean cube.

Also, every term in $D_h(x)$ is strictly positive, so $b_h(x) > 0$ for every Boolean input.

### Lemma 3: Any $H$-head classifier has threshold degree at most $H$

Let $f : \{0,1\}^n \to \{0,1\}$ be computed by an $H$-head model in the one-layer architecture.

Then there exists a real polynomial $P(x_1, \ldots, x_n)$ of degree at most $H$ such that

$$P(x) > 0 \text{ exactly on the inputs where } f(x) = 1,$$

$$P(x) < 0 \text{ exactly on the inputs where } f(x) = 0.$$

In other words, $f$ has threshold degree at most $H$.

#### Proof

If $f$ is constant, then its threshold degree is $0$, so there is nothing to prove. We therefore assume $f$ is nonconstant.

Let the raw readout score be

$$U(x) = c + \sum_{h=1}^{H} s_h(x)$$

where $c$ is the constant contribution from the query residual and the readout threshold has not yet been absorbed.

Because the model computes $f$, there exists some threshold $\tau$ such that

$$U(x) > \tau \quad \text{iff} \quad f(x) = 1.$$

By Lemma 1, because $f$ is nonconstant, there exists another threshold $\tau'$ such that

$$U(x) - \tau' > 0 \text{ on positive examples},$$

$$U(x) - \tau' < 0 \text{ on negative examples}.$$

Now set

$$S(x) := U(x) - \tau'.$$

Then

$$S(x) = c' + \sum_{h=1}^{H} s_h(x)$$

for the constant $c' := c - \tau'$.

Also

$$S(x) > 0 \text{ on positive examples}, \qquad S(x) < 0 \text{ on negative examples}.$$

By Lemma 2, for each head $h$ we can write

$$s_h(x) = \frac{a_h(x)}{b_h(x)}$$

with $a_h, b_h$ affine and $b_h(x) > 0$ on the Boolean cube.

Therefore

$$S(x) = c' + \sum_{h=1}^{H} \frac{a_h(x)}{b_h(x)}.$$

Now multiply by the positive common denominator

$$B(x) := \prod_{h=1}^{H} b_h(x).$$

Since $B(x) > 0$ on the Boolean cube, the sign of $S(x)$ is the same as the sign of

$$P(x) := B(x) \, S(x) = c' \prod_{h=1}^{H} b_h(x) + \sum_{h=1}^{H} a_h(x) \prod_{g \neq h} b_g(x).$$

Each $a_h$ and $b_h$ is affine, so every summand has degree at most $H$.

Hence $P$ is a polynomial of degree at most $H$.

Because $B(x) > 0$, $P$ has exactly the same sign pattern as $S$.

So $P$ sign-represents the Boolean function $f$ on $\{0,1\}^n$.

### Lemma 4: $n$-bit parity has threshold degree at least $n$

Let $\mathrm{PARITY}_n(x)$ be $1$ when $\sum_i x_i$ is odd and $0$ when it is even.

Then no real polynomial of degree less than $n$ can sign-represent this function on $\{0,1\}^n$.

#### Proof

It is more convenient to pass to $\{-1,1\}$ variables. Define

$$z_i := 1 - 2 x_i.$$

Then $z_i = 1$ when $x_i = 0$ and $z_i = -1$ when $x_i = 1$.

The parity sign function is

$$\pi(z) := -\prod_{i=1}^{n} z_i.$$

Indeed, $\prod_i z_i = (-1)^{x_1 + \cdots + x_n}$, which is $+1$ on even parity and $-1$ on odd parity, so multiplying by $-1$ makes $\pi(z)$ positive exactly on odd inputs.

Now suppose, toward a contradiction, that there were a polynomial $Q(z_1, \ldots, z_n)$ of degree less than $n$ such that

$$Q(z) > 0 \text{ whenever } \pi(z) = 1,$$

$$Q(z) < 0 \text{ whenever } \pi(z) = -1.$$

Equivalently,

$$\pi(z) \, Q(z) > 0$$

for every $z \in \{-1,1\}^n$.

Since the cube is finite, averaging gives

$$\mathbb{E}[\pi(z) \, Q(z)] > 0.$$

We now show that this expectation must in fact be zero.

For each subset $S \subseteq \{1, \ldots, n\}$, define the Walsh character

$$\chi_S(z) := \prod_{i \in S} z_i.$$

Every real-valued function on $\{-1,1\}^n$ can be written uniquely as a linear combination of these characters. In particular, every polynomial of degree less than $n$, restricted to the cube, has an expansion

$$Q(z) = \sum_{S \subsetneq [n]} c_S \, \chi_S(z),$$

where only subsets $S$ of size strictly less than $n$ occur.

This is because on the cube $z_i^2 = 1$, so every monomial reduces to a squarefree monomial without increasing degree, and squarefree monomials are exactly the Walsh characters.

Also,

$$\pi(z) = -\chi_{[n]}(z).$$

Using orthogonality of the Walsh characters,

$$\mathbb{E}[\chi_{[n]}(z) \, \chi_S(z)] = 0$$

for every proper subset $S \subsetneq [n]$.

The reason is that

$$\chi_{[n]}(z) \, \chi_S(z) = \chi_{[n] \,\triangle\, S}(z),$$

and $[n] \,\triangle\, S$ is nonempty when $S \neq [n]$. The expectation of a nontrivial character over the uniform cube is zero, because if $T$ is nonempty then

$$\mathbb{E}[\chi_T(z)] = \prod_{i \in T} \mathbb{E}[z_i] = 0.$$

Therefore

$$\mathbb{E}[\pi(z) \, Q(z)] = -\sum_{S \subsetneq [n]} c_S \, \mathbb{E}[\chi_{[n]}(z) \, \chi_S(z)] = 0.$$

This contradicts the earlier inequality $\mathbb{E}[\pi(z) \, Q(z)] > 0$.

So no degree-$(<n)$ polynomial sign-represents parity.

### Lower-bound conclusion

If $\mathrm{XOR}_n$ were computable with fewer than $n$ heads, then by Lemma 3 it would have threshold degree less than $n$, contradicting Lemma 4.

Hence

$$H^{*}(\mathrm{XOR}_n) \ge n.$$

## Part II: Upper Bound

We now construct an explicit $n$-head network computing parity.

### Shared ambient space and embeddings

Work in dimension $d = n + 2$.

Choose an orthonormal basis

$$q, u, e_1, \ldots, e_n.$$

Use shared token embeddings

$$\mathrm{token}(0) = 0, \qquad \mathrm{token}(1) = u, \qquad \mathrm{token}(=) = q,$$

and set all positional embeddings to zero.

So the query token always carries the constant vector $q$, every `0` token is the zero vector, and every `1` token is the vector $u$.

### Head $j$

Fix distinct parameters $\alpha_1, \ldots, \alpha_n$, all greater than $1$. For concreteness one may take

$$\alpha_j = 2^j.$$

For head $j$, define linear maps as follows.

1. $W_Q^{(j)}$ sends $q$ to $q$ and annihilates the orthogonal complement of $q$.
2. $W_K^{(j)}$ sends $u$ to $(\log \alpha_j) \, q$ and annihilates $q, e_1, \ldots, e_n$.
3. $W_V^{(j)}$ sends $u$ to $e_j$ and annihilates $q, e_1, \ldots, e_n$.

These maps are linear, so they define a valid attention head.

### Lemma 5: The output of head $j$ depends only on Hamming weight

Let $k = x_1 + \cdots + x_n$ be the Hamming weight of the input.

Then head $j$ outputs

$$y_j(x) = g_j(k) \, e_j$$

where

$$g_j(k) = \frac{k \, \alpha_j}{n + 1 + (\alpha_j - 1) \, k}.$$

#### Proof

We compute the logits first.

1. If an input token is `1`, its embedding is $u$. So $W_K^{(j)} u = (\log \alpha_j) \, q$. The query vector is $q$, and $W_Q^{(j)} q = q$, so the raw logit is $\langle (\log \alpha_j) \, q, q \rangle = \log \alpha_j$.
2. If an input token is `0`, its embedding is $0$, so its key is $0$ and its logit is $0$.
3. The query token itself has embedding $q$, but $W_K^{(j)} q = 0$, so its self-logit is also $0$.

Therefore:

1. each `1`-token contributes unnormalized attention weight $\alpha_j$,
2. each `0`-token contributes unnormalized attention weight $1$,
3. the query token contributes unnormalized attention weight $1$.

Now compute the values.

1. A `1`-token has embedding $u$, and $W_V^{(j)} u = e_j$.
2. A `0`-token has embedding $0$, so its value is $0$.
3. The query token has embedding $q$, and $W_V^{(j)} q = 0$.

So if the input has Hamming weight $k$, then:

1. the numerator vector is $k \, \alpha_j \, e_j$,
2. the denominator scalar is $(n - k) \cdot 1 + k \cdot \alpha_j + 1$.

Hence

$$y_j(x) = \frac{k \, \alpha_j}{(n - k) + k \, \alpha_j + 1} \, e_j = \frac{k \, \alpha_j}{n + 1 + (\alpha_j - 1) \, k} \, e_j.$$

This proves the formula.

### Lemma 6: The functions $1, g_1, \ldots, g_n$ are linearly independent on $\{0, \ldots, n\}$

Consider the $n + 1$ real-valued functions on the set $\{0, \ldots, n\}$

$$1, \; g_1, \; \ldots, \; g_n.$$

These functions are linearly independent.

#### Proof

Assume

$$c_0 + \sum_{j=1}^{n} c_j \, g_j(k) = 0$$

for every $k = 0, 1, \ldots, n$.

At $k = 0$, every $g_j(0) = 0$, so $c_0 = 0$.

For $k = 1, \ldots, n$, divide by $k$ to obtain

$$\sum_{j=1}^{n} \frac{c_j \, \alpha_j}{n + 1 + (\alpha_j - 1) \, k} = 0.$$

Define

$$r_j := \frac{n + 1}{\alpha_j - 1}, \qquad d_j := \frac{c_j \, \alpha_j}{\alpha_j - 1}.$$

Then the relation becomes

$$\sum_{j=1}^{n} \frac{d_j}{k + r_j} = 0$$

for every $k = 1, \ldots, n$.

Now consider the rational function

$$R(t) := \sum_{j=1}^{n} \frac{d_j}{t + r_j}.$$

Multiply by the common denominator:

$$N(t) := R(t) \prod_{j=1}^{n} (t + r_j).$$

Because $R$ is a sum of simple fractions, $N(t)$ is a polynomial of degree at most $n - 1$.

But $R(k) = 0$ for $k = 1, \ldots, n$, so $N(k) = 0$ for those $n$ distinct values.

A polynomial of degree at most $n - 1$ with $n$ distinct roots must be the zero polynomial. Therefore $N(t) \equiv 0$, and hence $R(t) \equiv 0$.

Now fix $j$. Multiply $R(t)$ by $(t + r_j)$ and set $t = -r_j$. This gives

$$d_j \prod_{m \neq j} (r_m - r_j) = 0.$$

Because the $\alpha_j$ are distinct, the $r_j$ are distinct as well, so the product is nonzero. Therefore $d_j = 0$.

So every $d_j = 0$, hence every $c_j = 0$.

Therefore $1, g_1, \ldots, g_n$ are linearly independent.

### Corollary 7: $1, g_1, \ldots, g_n$ form a basis of all functions on $\{0, \ldots, n\}$

The set $\{0, \ldots, n\}$ has exactly $n + 1$ points, so the vector space of real-valued functions on this set has dimension $n + 1$.

By Lemma 6 we already have $n + 1$ linearly independent functions.

Therefore $1, g_1, \ldots, g_n$ form a basis.

### Lemma 8: $n$ heads can realize parity exactly

Define a target sign pattern on Hamming weights by

$$t_k := +1 \text{ if } k \text{ is odd}, \qquad t_k := -1 \text{ if } k \text{ is even}.$$

By Corollary 7, there exist coefficients $\beta_0, \beta_1, \ldots, \beta_n$ such that

$$\beta_0 + \sum_{j=1}^{n} \beta_j \, g_j(k) = t_k$$

for every $k = 0, \ldots, n$.

Now choose the final linear probe

$$w := \sum_{j=1}^{n} \beta_j \, e_j.$$

Since $w$ is orthogonal to $q$, the constant query skip connection does not affect the probe score.

By Lemma 5, on an input of Hamming weight $k$,

$$\Bigl\langle w, \sum_{j=1}^{n} y_j(x) \Bigr\rangle = \sum_{j=1}^{n} \beta_j \, g_j(k).$$

So the full affine score

$$S(x) := \beta_0 + \Bigl\langle w, \sum_{j=1}^{n} y_j(x) \Bigr\rangle$$

satisfies

$$S(x) = t_k,$$

where $k = |x|$.

Therefore:

1. $S(x) = +1$ on odd-parity inputs,
2. $S(x) = -1$ on even-parity inputs.

So thresholding at $0$ computes $\mathrm{XOR}_n$ exactly.

Hence

$$H^{*}(\mathrm{XOR}_n) \le n.$$

## Final Conclusion

We proved:

1. $H^{*}(\mathrm{XOR}_n) \ge n$ by threshold degree,
2. $H^{*}(\mathrm{XOR}_n) \le n$ by explicit construction.

Therefore

$$H^{*}(\mathrm{XOR}_n) = n.$$

## Remarks

1. The lower bound uses only the one-layer attention structure and the linear readout.
2. The upper bound uses no positional embeddings.
3. The upper-bound construction actually proves more: $n$ heads suffice to realize every symmetric Boolean function of Hamming weight, not just parity, because the basis interpolation works for any target values on $k = 0, \ldots, n$.
