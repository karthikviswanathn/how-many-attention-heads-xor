# Same-polarity sparse threshold-density upper bound

Let $H^{\ast}(f)$ denote the minimum number of heads needed to compute $f$ in the one-layer attention model of `model.md`, with a final strict threshold. Fix a polarity $\zeta\in\{0,1\}$. Let $A_1,\ldots,A_s\subseteq\{1,\ldots,n\}$ be nonempty coordinate sets, and define

$$
q_r(x)=\mathbf{1}[x_i=\zeta\text{ for every }i\in A_r].
$$

Suppose there are real numbers $\theta,c_1,\ldots,c_s$ such that

$$
f(x)=1 \Longleftrightarrow \theta+\sum_{r=1}^{s} c_r q_r(x)>0
$$

for every $x\in\{0,1\}^n$, with positive margin

$$
\mu=\min_{x\in\{0,1\}^n}\left|\theta+\sum_{r=1}^{s}c_r q_r(x)\right|>0.
$$

Then

$$
H^{\ast}(f)\leq s.
$$

Equivalently, every strict linear threshold of $s$ coordinate-subcube indicators anchored at one Boolean vertex is computable with at most one head per subcube.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads
- **Reuse Lemma 17's bump verbatim**, replacing numerator $1$ by the constant $c_r$ (Lemma 13's numerator-freedom for nonconstant denominators handles negative $c_r$ — no $W_O$ trickery needed).
- **Drive the bump tolerance with the margin:** pick in-set weight $\lambda$ large / out-of-set weight small so $\sum_r|\phi_r-c_rq_r|<\mu$; sign is then preserved everywhere. Same "finite cube + margin ⇒ finite logits" move as Lemma 4.
- **Use $\mu>0$ only as non-degeneracy** (form vanishes nowhere on the cube); note $\mu=\min|\cdot|$ is then automatic — state this so the hypothesis isn't over-read as a quantitative assumption.
- **Conclude via Lemma 10:** constant $\theta$ + sum of $s$ atoms ⇒ $H^\ast(f)\le s$; no need to touch the tangential-Chow frontier (14–16).
- **Framing for the writeup:** present it as "head complexity ≤ same-polarity subcube-threshold density," the signed generalization of the DNF (OR) bound — the natural sparsity analogue of the degree bound (Lemma 6).
