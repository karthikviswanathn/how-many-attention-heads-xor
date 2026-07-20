# Weighted-Sum Sign-Change Upper Bound

Let $H^{\ast}(f)$ be the minimum number of one-layer attention heads needed to compute $f : \{0,1\}^{n} \to \{0,1\}$ in the model of `model.md`, with a final strict threshold and with $H^{\ast}(f)=0$ allowed only for constants.

Suppose there are positive weights $\lambda_1,\ldots,\lambda_n>0$, a statistic

$$
t(x)=\sum_{i=1}^{n}\lambda_i x_i,
$$

and a function $F:\operatorname{Im}(t)\to\{0,1\}$ such that $f(x)=F(t(x))$. List the distinct values of $t$ as

$$
\tau_0<\tau_1<\cdots<\tau_{M-1}.
$$

Define signs $\sigma_j=+1$ if $F(\tau_j)=1$ and $\sigma_j=-1$ if $F(\tau_j)=0$, and let

$$
C_t(F)=\left|\left\{j\in\{1,
\ldots,M-1\}:\sigma_{j-1}\neq\sigma_j\right\}\right|.
$$

Then

$$
H^{\ast}(f)\leq C_t(F).
$$

In particular Lemma 9 follows as the weaker bound $H^{\ast}(f)\leq M-1$.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Lift Lemma 12's "Lemma 3" verbatim with $|x|\rightsquigarrow t(x)$** (`012_symmetric_sign_changes.md:135–179`) — this is the entire proof skeleton.
2. **Reuse Lemma 9's "Head $j$" as the weighted shifted-reciprocal atom** (`009_weighted_sum_upper_bound.md:73–130`): its $g_j(t)=\frac{\alpha_j t}{1+\Lambda+(\alpha_j-1)t}$ is the Möbius/$\frac{d_j}{t+r_j}$ gadget, with $r_j=\frac{1+\Lambda}{\alpha_j-1}>0$.
3. **Build the degree-$C$ sign-representer** $P(s)=\sigma_0\prod_{j:\,\sigma_{j-1}\neq\sigma_j}(m_j-s)$ with $m_j\in(\tau_{j-1},\tau_j)$, then **partial-fraction $P/\prod(s+r_j)$** into $c+\sum_{j=1}^{C}\frac{d_j}{s+r_j}$ (one head each) — steps (i)–(ii) above.
4. **Invoke Lemma 13 class-2/3 (nonconstant denominator ⇒ arbitrary affine numerator)** to certify each $d_j$ is realizable, and finish with one strict threshold using the finite-cube positive margin (cf. Lemmas 18/29).
5. **Do not attempt a matching lower bound** — symmetrization breaks for non-unit weights, so only $\le$ is provable here.
