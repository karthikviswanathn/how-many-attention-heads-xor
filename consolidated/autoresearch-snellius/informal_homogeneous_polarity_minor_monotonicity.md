# Homogeneous Polarity Boolean Minors Do Not Increase Head Complexity

Let $H^{\ast}(f)$ denote the least number of heads in the one-layer attention model of `model.md` that computes $f$ with a strict final threshold. Equivalently, by Lemma 10, $H^{\ast}(f)$ is the least number of one-head linear-fractional atoms needed before the final threshold.

For $f : \{0,1\}^{n} \to \{0,1\}$, define its antipodal input complement by

$$
f^{\dagger}(x_1,\ldots,x_n)=f(1-x_1,\ldots,1-x_n).
$$

Then

$$
H^{\ast}(f^{\dagger})=H^{\ast}(f).
$$

Consequently, if $g : \{0,1\}^{m} \to \{0,1\}$ is obtained from $f$ by a homogeneous-polarity Boolean minor, namely by replacing each input coordinate of $f$ by either a constant in $\{0,1\}$ or by an unnegated coordinate $y_j$, with repetitions allowed, or instead replacing each nonconstant input coordinate by a negated coordinate $1-y_j$, again with repetitions allowed, then

$$
H^{\ast}(g) \leq H^{\ast}(f).
$$

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Prove (1) by the embedding swap $e_0\leftrightarrow e_1$** (all other parameters fixed), then conclude $g$ is a positive minor of $f^{\dagger}$ and invoke **Lemma 34** — the whole target in ~half a page.
2. **Cross-check (1) via Lemma 10/13 atom closure** under $x\mapsto\bar x$ ($\alpha\mapsto\alpha^{-1},\ \rho_i\mapsto\rho_i\alpha$): independent confirmation, no embeddings needed.
3. **Reuse Lemma 31's proof template** (it already does output negation + permutation by relabeling) — input global negation is the same argument with the token-embedding swap substituted in.
4. **State the symmetry group explicitly** in the writeup: $H^{\ast}$ is invariant under $S_n \rtimes \langle x\mapsto\bar x\rangle$ on inputs plus output complement — and flag individual-coordinate negation as the open boundary (motivating the *homogeneous* restriction).
5. **Frame both Lemma 34 and this as one statement** in the minor quasi-order: $H^{\ast}$ is monotone under the constants+unnegated-variables minor relation enlarged by the global reflection — a cleaner ledger entry than two separate lemmas.
