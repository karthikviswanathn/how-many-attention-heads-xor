# Two-Polarity Sparse Threshold-Density Upper Bound

Let $f : \{0,1\}^{n} \to \{0,1\}$ be computed in the one-layer attention model of `model.md`, and let $H^{\ast}(f)$ denote the least number of attention heads needed to compute $f$ with a strict final threshold.

For each $r \in \{1,\ldots,s\}$, fix a nonempty coordinate set $A_r \subseteq \{1,\ldots,n\}$ and a polarity $\zeta_r \in \{0,1\}$. Define the coordinate-subcube indicator

$$
I_r(x) := \mathbf{1}\bigl[x_i = \zeta_r \text{ for every } i \in A_r\bigr].
$$

Suppose there are real coefficients $c_1,\ldots,c_s$ and a threshold $\theta$ such that

$$
f(x) = \mathbf{1}\left[\theta + \sum_{r=1}^{s} c_r I_r(x) > 0\right]
$$

with positive margin on the Boolean cube, meaning

$$
\theta + \sum_{r=1}^{s} c_r I_r(x) \neq 0
\qquad \text{for every } x \in \{0,1\}^{n}.
$$

Then

$$
H^{\ast}(f) \leq s.
$$

Equivalently, strict signed thresholds of $s$ coordinate-subcube indicators, where each subcube is anchored either at the all-zero vertex or at the all-one vertex but the polarity may vary with the term, need at most one head per subcube.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads
1. **Reuse Lemma 18 verbatim with a term-indexed violation indicator** $\nu_{r,i}$ keyed to $\zeta_r$; its existing $\zeta\in\{0,1\}$ case split already proves atom validity for both anchors — this *is* the proof. (Highest-value lead by far.)
2. **Cite Lemma 10** for the reduction "$s$ admissible atoms $+$ one strict threshold $\Rightarrow H^*\le s$," and **Lemma 13** to license both all-positive and all-negative-coefficient denominators.
3. **Keep the same margin pass** ($\varepsilon=\mu/(4(B+1))$, $\Lambda$ large, $\kappa$ small): it uses only $\nu_{r,i}\in\{0,1\}$ and $\nu_{r,i}=0\iff x_i=\zeta_r$, both per-term, so it transfers unchanged.
4. **Record the two-anchor restriction explicitly:** terms are conjunctions through $\vec0$ or $\vec1$ only; a genuinely new step would be needed for general-vertex subcubes (mixed literals within one term), which this target does *not* cover.
5. **Optionally state Lemma 17's two-polarity DNF analogue as an immediate corollary** ($\theta<0$, $c_r$ large $\Rightarrow f=\bigvee_r I_r$), to close that gap in the same write-up.
