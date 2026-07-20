# Feed-Forward One-Head Universality

## Statement

Use the feed-forward model from [model_feedforward.md](model_feedforward.md), with query-token feed-forward hidden width fixed to $2d_{\mathrm{model}}$.

For every Boolean function

$$ f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace, $$

we have

$$ H_{\mathrm{ff}}^{\ast}(f) = \begin{cases} 0 & \text{if } f \text{ is constant}, \\ 1 & \text{otherwise}. \end{cases} $$

> **Interpretation.** Once feed-forward computation is allowed at the query token, attention-head count no longer measures sign-change complexity. One head can encode the input injectively, and the width $2d_{\mathrm{model}}$ feed-forward block can perform the finite lookup after choosing the model dimension large enough.

## Proof

We prove the zero-head case and the one-head upper bound separately.

For the one-head upper bound, $d_{\mathrm{model}}$ is part of the construction. We choose it large enough to support both the attention code and the feed-forward interpolation.

### Lemma 1. Zero heads compute exactly constant functions

If $H = 0$, then

$$ r_{\mathrm{attn}}(x) = u_= $$

is independent of $x$. Therefore every feed-forward score $S_{\mathrm{ff}}(x)$ is constant on the Boolean cube, so a zero-head model computes only constant functions.

Conversely, either constant Boolean function is computed with zero heads by placing the threshold on the appropriate side of the constant score.

Thus

$$ H_{\mathrm{ff}}^{\ast}(f) = 0 \qquad \Longleftrightarrow \qquad f \text{ is constant}. $$

### Lemma 2. One head can injectively encode the Boolean input

Assume $n \geq 1$. Choose parameters

$$ \alpha > 0, \qquad \alpha \neq 1, \qquad \gamma > 0, $$

and

$$ \rho_1,\ldots,\rho_n > 0. $$

Let

$$ o_1,\ldots,o_n $$

be linearly independent output directions. If $d_{\mathrm{model}}$ is large enough to contain the directions used below, a single attention head can be chosen so that its projected query-token output is

$$ z(x) = \frac{\sum_{i=1}^{n} \rho_i \alpha^{x_i} o_i} {\gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i}}. $$

Here is one explicit construction. Take model-space directions

$$ q,k,v_1,\ldots,v_n,o_1,\ldots,o_n $$

and head-space directions

$$ \widetilde q,\widetilde o_1,\ldots,\widetilde o_n. $$

Set

$$ e_0 := 0, \qquad e_1 := (\log \alpha) k, $$

$$ p_i := (\log \rho_i) k + v_i \qquad 1 \leq i \leq n, $$

and choose the query-token embedding and position so that

$$ u_= := q + (\log \gamma) k. $$

Choose the head maps so that $W_Q q = \widetilde q$, $W_K k = \widetilde q$, $W_V v_i = \widetilde o_i$, and $W_O \widetilde o_i = o_i$, with the other listed basis directions annihilated when not specified.

Then the input-position logits are

$$ \log \rho_i + x_i \log \alpha, $$

so their unnormalized attention weights are $\rho_i \alpha^{x_i}$. The query token has unnormalized attention weight $\gamma$ and zero value. Therefore the projected head output is exactly $z(x)$.

We claim that $x \mapsto z(x)$ is injective on $\lbrace0,1\rbrace^n$.

Write

$$ D(x) := \gamma + \sum_{i=1}^{n} \rho_i \alpha^{x_i}. $$

Suppose $z(x) = z(x')$. Comparing coefficients in the independent directions $o_i$ gives

$$ \frac{\rho_i \alpha^{x_i}}{D(x)} = \frac{\rho_i \alpha^{x'_i}}{D(x')} \qquad \text{for every } i. $$

After canceling $\rho_i > 0$,

$$ \frac{D(x')}{D(x)} = \alpha^{x'_i - x_i} \qquad \text{for every } i. $$

If some coordinate is unchanged and another coordinate is changed, then the same positive ratio would have to equal both $1$ and either $\alpha$ or $\alpha^{-1}$, impossible since $\alpha \neq 1$.

If two changed coordinates move in opposite directions, then the same positive ratio would have to equal both $\alpha$ and $\alpha^{-1}$, also impossible since $\alpha > 0$ and $\alpha \neq 1$.

Thus either $x' = x$, or every coordinate changes in the same direction. The latter means either $x = (0,\ldots,0)$ and $x' = (1,\ldots,1)$, or the reverse.

In the first case, the displayed ratio condition requires

$$ D(x') = \alpha D(x). $$

But then

$$ \gamma + \alpha \sum_{i=1}^{n} \rho_i = \alpha \gamma + \alpha \sum_{i=1}^{n} \rho_i, $$

which implies $\gamma = \alpha \gamma$, contradicting $\gamma > 0$ and $\alpha \neq 1$. The reverse case similarly requires $D(x) = \alpha D(x')$ and gives the same contradiction.

Therefore $z(x) = z(x')$ implies $x = x'$, so the one-head attention output is injective.

### Lemma 3. Width twice model dimension ReLU feed-forward separates the codebook

Let

$$ Z := \lbrace z(x) : x \in \lbrace0,1\rbrace^n \rbrace. $$

By Lemma 2, all points in $Z$ are distinct. Choose a vector $v$ such that the scalars

$$ t_x := v^\top z(x) $$

are all distinct. Such a $v$ exists because the bad choices lie in a finite union of proper hyperplanes.

Order the inputs as

$$ t_{x^{(1)}} < t_{x^{(2)}} < \cdots < t_{x^{(2^n)}}. $$

Set target signs

$$ \sigma_j := \begin{cases} +1 & \text{if } f(x^{(j)}) = 1, \\ -1 & \text{if } f(x^{(j)}) = 0. \end{cases} $$

There is a continuous piecewise-linear function $g : \mathbb{R} \to \mathbb{R}$ with

$$ g(t_{x^{(j)}}) = \sigma_j \qquad \text{for every } j. $$

For example, linearly interpolate between consecutive points and extend linearly outside the interval they span.

The interpolation can be chosen with at most $2^n$ breakpoints. Every continuous piecewise-linear function with finitely many breakpoints has a representation

$$ g(t) = \beta_0 + \beta_1 t + \sum_{\ell=1}^{M} c_\ell \mathrm{ReLU}(t - \kappa_\ell) $$

for the real coefficients and breakpoints shown in the display.

Now choose $d_{\mathrm{model}}$ large enough that

$$ 2d_{\mathrm{model}} \geq M $$

and large enough to support the one-head construction from Lemma 2. This is allowed because the model dimension is not fixed by the head-count definition. If $M < 2d_{\mathrm{model}}$, set the remaining hidden-unit output coefficients to zero.

Therefore

$$ S_{\mathrm{ff}}(x) := g(v^\top z(x)) $$

is a valid one-hidden-layer ReLU feed-forward score, after absorbing the constant query residual into the feed-forward bias. It satisfies

$$ S_{\mathrm{ff}}(x) > 0 \qquad \Longleftrightarrow \qquad f(x) = 1. $$

Thus every Boolean function is computable with one head in the feed-forward model.

### Conclusion

Lemma 1 gives the exact zero-head level. Lemmas 2 and 3 show that every nonconstant Boolean function has

$$ H_{\mathrm{ff}}^{\ast}(f) \leq 1. $$

Since nonconstant functions cannot have feed-forward head complexity $0$, they have feed-forward head complexity exactly $1$.

Therefore

$$ H_{\mathrm{ff}}^{\ast}(f) = \begin{cases} 0 & \text{if } f \text{ is constant}, \\ 1 & \text{otherwise}. \end{cases} $$

$\blacksquare$

## Consequences

Lemma 12 from the attention-only stack does not persist under this model change. In particular, every nonconstant symmetric Boolean function, including parity and every exact-count predicate, has feed-forward head complexity $1$.

To get a nontrivial invariant in a model with feed-forward computation, fixing width proportional to the model dimension is not enough when the model dimension is free. Natural options are fixing the model dimension, charging for the model dimension, bounding feed-forward width independently, bounding depth, restricting the activation family, or using a joint complexity measure counting both heads and feed-forward units.
