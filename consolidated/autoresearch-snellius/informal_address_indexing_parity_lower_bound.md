# Indexing Functions Have Parity Restriction Lower Bounds

Let $m \geq 1$. Let

$$
\mathrm{IND}_m : \{0,1\}^{m} \times \{0,1\}^{\{0,1\}^{m}} \to \{0,1\}
$$

be the indexing function

$$
\mathrm{IND}_m(a,y)=y_a,
$$

where $a \in \{0,1\}^{m}$ is the address and $y=(y_b)_{b\in\{0,1\}^{m}}$ is the data table. Let $H^{\ast}(f)$ denote the minimum number of heads needed to compute $f$ in the one-layer attention model of `model.md`, equivalently the invariant characterized by the linear-fractional normal form in Lemma 10.

Then

$$
H^{\ast}(\mathrm{IND}_m) \geq m.
$$

More generally, for every Boolean function $g:\{0,1\}^{m}\to\{0,1\}$, if the data table is fixed to $y_b=g(b)$ for all $b\in\{0,1\}^{m}$, then the corresponding subcube restriction of $\mathrm{IND}_m$ is exactly $g$. Hence

$$
H^{\ast}(\mathrm{IND}_m) \geq \max_{g:\{0,1\}^{m}\to\{0,1\}} H^{\ast}(g),
$$

and choosing $g=\mathrm{XOR}_m$ gives the stated bound by the exact parity lemma.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Write the proof via Lemma 26/27 + Lemma 8**, using the one-line universality fact "$\mathrm{IND}_m$ restricted to $y=\text{truth table of }g$ is exactly $g$." This is the whole proof; it matches the target's sketch.
2. **State the stronger bound for free:** swap the witness to a hard $g$ from **Lemma 24/25** to get $H^\ast(\mathrm{IND}_m)=\Omega(2^m/m^2)$ — same argument, exponentially stronger conclusion.
3. **Record the separation:** $\deg_\pm(\mathrm{IND}_m)\le m+1$ (exact multilinear extension) vs. $H^\ast(\mathrm{IND}_m)=\tilde\Omega(2^m)$ — an exponential $H^\ast$-vs-$\deg_\pm$ gap, strictly stronger than Lemmas 20/22/23.
4. **Verify the one hinge:** that Lemma 26/27's "fix coordinates + relabel" legitimately produces $g$ on the $m$ address positions out of the $n=m+2^m$ positions (identity relabel; should be immediate).
5. **Note as open:** a non-trivial upper bound on $H^\ast(\mathrm{IND}_m)$ — Lemma 17/18 do not apply (mixed-polarity subcube anchors), so $\tilde O(2^m)$ is not yet in hand.
