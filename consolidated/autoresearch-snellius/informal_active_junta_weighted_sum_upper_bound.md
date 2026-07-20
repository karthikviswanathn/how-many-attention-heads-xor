# Active-Junta Weighted-Sum Sign-Change Upper Bound

Work in the one-layer attention model of `model.md`, and let $H^{\ast}(f)$ be the minimum number of attention heads needed to compute $f$ with a final strict threshold at the query token.

Let $f : \{0,1\}^{n}\to\{0,1\}$ depend only on a coordinate set $I\subseteq\{1,\ldots,n\}$ with $|I|=k$. Thus there is a function $g:\{0,1\}^{I}\to\{0,1\}$ such that $f(x)=g(x_I)$.

Suppose there are positive weights $\lambda_i>0$ for $i\in I$, a statistic

$$
t_I(u)=\sum_{i\in I}\lambda_i u_i,
$$

and a function $G:\operatorname{Im}(t_I)\to\{0,1\}$ such that $g(u)=G(t_I(u))$ for every $u\in\{0,1\}^{I}$. List the distinct values of $t_I$ as $\tau_0<\tau_1<\cdots<\tau_{M-1}$, set

$$
\sigma_j=\begin{cases}+1,&G(\tau_j)=1,\\-1,&G(\tau_j)=0,
\end{cases}
$$

and define

$$
C_{t_I}(G)=\left|\{j\in\{1,\ldots,M-1\}:\sigma_{j-1}\neq\sigma_j\}\right|.
$$

Then

$$
H^{\ast}(f)\leq C_{t_I}(G).
$$

In particular, every $k$-junta satisfies

$$
H^{\ast}(f)\leq 2^k-1.
$$

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Just compose:** $H^{\ast}(f)=H^{\ast}(g)\le C_{t_I}(G)$ via **Lemma 31** (dummy + permutation invariance) then **Lemma 30** applied to $g$ on $\{0,1\}^{I}$ — no new construction needed.
2. **For $2^k-1$:** pick **injective positive weights** (superincreasing $\lambda_{i_r}=2^{r-1}$, distinct subset sums) so $M=2^k$, then a $\pm1$ sequence on $M$ ordered points has $\le M-1$ sign changes — this is **Lemma 9** localized by Lemma 31.
3. **Sanity-check the one bookkeeping point:** confirm $t_I(\vec0)=0$ so Lemma 30's $\tau_0=0$ normalization carries over to $g$; the $\{0,1\}^I\to\{0,1\}^k$ relabel is a Lemma 31 permutation.
4. **Do not attempt a lower bound:** the matching $H^{\ast}\ge C_{t_I}(G)$ is the weighted generalization of **Lemma 12** and does not follow from this route; leave it as a separate (likely harder) target.
5. **Mathlib framing if formalizing:** state the hypothesis with `DependsOn`/`dependsOn_iff_exists_comp`, and the sign-change count against `Polynomial.signVariations` / Descartes (`roots_countP_pos_le_signVariations`).
