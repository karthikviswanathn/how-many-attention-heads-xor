# Positive Boolean Minors Do Not Increase Head Complexity

Let $f : \{0,1\}^{n} \to \{0,1\}$, and let $H^{\ast}(f)$ be the least number of attention heads needed to compute $f$ in the one-layer model of `model.md`. Let $\tau : \{1,\ldots,n\} \to \{0,1\} \cup \{1,\ldots,m\}$ be a positive minor map. For $y \in \{0,1\}^{m}$ define $z_i(y)$ by $z_i(y)=0$ or $z_i(y)=1$ when $\tau(i)$ is that constant, and $z_i(y)=y_{\tau(i)}$ when $\tau(i) \in \{1,\ldots,m\}$. Define

$$
g(y)=f(z_1(y),\ldots,z_n(y)).
$$

Then

$$
H^{\ast}(g) \leq H^{\ast}(f).
$$

In particular, fixing coordinates, permuting coordinates, duplicating coordinates, and identifying coordinates cannot increase head complexity. If some coordinate of $g$ is unused, the same conclusion is interpreted using irrelevant-variable invariance.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads
- **Prove at the Lemma 10 level, not the model level** — substitute the minor into the $K=H^\ast(f)$ atoms; it follows that $L_{\mathrm{frac}}(g)\le K$.
- **Copy the Lemma 26 proof structure**; the only change is that the variable substitution is non‑injective, so coordinate groups $G_j$ merge.
- **The one new algebraic step is the merge** $\rho'_{h,j}=\sum_{i\in G_j}\rho_{h,i}>0$, $m'_{h,j}=$ ($\rho$‑weighted average of $m_{h,i}$); positivity of $\rho$ is what keeps the atom admissible.
- **Discharge unused $y_j$ via Lemma 31** (irrelevant‑variable invariance) — the lone case the atom argument cannot absorb.
- **State it as the unification** of the $\le$‑directions of Lemmas 26 + 31 plus identification; and note positivity is essential — input‑bit negation (general minors) provably breaks closure, matching Lemma 31's explicit non‑claim.
