# Active-junta support-size upper bound

Work in the one-layer attention model of `model.md`. A Boolean function $f : \{0,1\}^{n} \to \{0,1\}$ is computable with $H$ heads if some choice of embeddings, attention parameters, and final strict linear readout computes it on the Boolean cube, and $H^{\ast}(f)$ is the least such $H$.

Let $f$ depend only on a coordinate set $I\subseteq\{1,\ldots,n\}$ with $|I|=k$, so $f(x)=g(x_I)$ for an induced function $g:\{0,1\}^{I}\to\{0,1\}$. Define

$$
a=|\{u\in\{0,1\}^{I}:g(u)=1\}|,
\qquad
b=2^k-a.
$$

Then

$$
H^{\ast}(f)\leq \min\{2a,\,2b,\,2^k-1\}.
$$

In particular, if the active truth table of $f$ has at most $r$ ones or at most $r$ zeros, then $H^{\ast}(f)\leq 2r$.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads
1. **Primary route:** invoke Lemma 32 with any injective positive active weights (powers of two), then replace its `≤ 2^k−1` line with the run-count `C_{t_I}(G) ≤ min{2a, 2b, 2^k−1}`.
2. **The whole new content** is one combinatorial inequality: a binary string with $a$ ones and $b$ zeros has $\le \min\{2a,2b,2^k-1\}$ adjacent-unequal pairs (runs argument: $p\le a$ one-runs, $q\le b$ zero-runs, transitions $=p+q-1\le2\min(a,b)$).
3. **No complementation / no weight tuning needed** — the inequality is symmetric in ones/zeros and arrangement-independent; it yields all three `min` terms simultaneously.
4. **Backup route** (if a non-sign-change proof is wanted): minterm DNF, each point = AND of a $\vec1$-anchored and a $\vec0$-anchored subcube (2 per minterm), assembled via Lemma 29 — but expect extra margin bookkeeping to flatten OR-of-ANDs.
5. **State it as an upper bound only**; cite parity ($a=b=2^{k-1}$, $H^{\ast}=k$) as the witness that $\min\{2a,2b,2^k-1\}$ is far from tight.
