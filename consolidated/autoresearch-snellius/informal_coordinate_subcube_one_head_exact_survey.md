Verified. Both linchpins confirm my analysis. Now the survey.

---

# Literature survey: Coordinate subcube indicators have one head

## Bottom line up front

**This target is an immediate corollary of an already-proved lemma in your own stack (Lemma 11), not new mathematics.** A coordinate subcube indicator $\chi_{P,N}$ is exactly a *single term/monomial* (a conjunction of signed literals), and the two facts you need are both elementary:

1. **It is a nonconstant linear threshold function** when $P\cup N\neq\emptyset$.
2. **Nonconstant LTF $\iff H^\ast=1$** is exactly Lemma 11 (verified biconditional, `lemmas/01_foundations_and_normal_form/011_one_head_characterization.md`).

So $H^\ast(\chi_{P,N})=1$ for $P\cup N\neq\emptyset$, and $\chi_{\emptyset,\emptyset}\equiv 1$ is constant so $H^\ast=0$ by the zero-head clause of the same lemma. **Flag for the lead: the heavy machinery is done; this is a one-paragraph corollary.** Confidence: high (I read the lemma file).

## Why $\chi_{P,N}$ is an LTF (the only nontrivial check)

The max of $\sum_{i\in P} x_i - \sum_{j\in N} x_j$ over the cube is $|P|$, attained iff all $P$-coords are $1$ and all $N$-coords are $0$. Hence
$$
\chi_{P,N}(x)=\mathbf 1\!\left[\sum_{i\in P} x_i-\sum_{j\in N} x_j>|P|-\tfrac12\right],
$$
a halfspace with integer weights $\pm1/0$, bias $\beta_0=\tfrac12-|P|$, and **margin $1/2$** on the cube. Nonconstant whenever $P\cup N\neq\emptyset$ (the anchor vertex gives $1$; flipping one relevant bit gives $0$). This is the classical fact that *any term/monomial is a threshold gate* — Minsky & Papert, *Perceptrons* (1969); Muroga, *Threshold Logic and Its Applications* (1971); and standard in O'Donnell, *Analysis of Boolean Functions* (2014, §ch. on LTFs/restrictions, where such a set is a "subcube"). Mixed polarity is not a complication here: signed weights are allowed in an LTF.

## What in the stack applies (and what to avoid citing)

- **Lemma 11 — the right tool.** Its "$\Leftarrow$" direction builds *one* linear-fractional atom for an **arbitrary** affine $L(x)=\beta_0+\sum\beta_i x_i$ (take $\alpha=2,\gamma=1,\rho_i=1,\delta=0,m_i=\beta_i,\eta=\beta_0-\sum\beta_i$; numerator collapses to $L(x)$, denominator $1+\sum 2^{x_i}>0$). Arbitrary signs $\beta_i$ are handled, so mixed $P,N$ is automatic. If a *self-contained* proof is wanted rather than a citation, this is the construction to instantiate with $\beta_i=+1$ on $P$, $-1$ on $N$, $\beta_0=\tfrac12-|P|$.
- **Lemma 6 + threshold degree.** $\deg_\pm(\chi_{P,N})=1$ (it is a nonconstant LTF), which via Lemma 6 also gives $H^\ast\ge1$ — but nonconstancy already gives that more cheaply.
- **Do NOT route through Lemmas 17 / 18 / 29 for the mixed case.** Those cover *same-polarity-within-a-term* subcubes (each $A_r$ fixed to a single $\zeta_r$). With $s=1$ they give only single-polarity subcubes; Lemma 29 even ends with the explicit caveat *"does not cover general subcubes with mixed literal polarities inside a single term."* They are upper-bound tools that miss precisely this target's generality, so $s=1$ there is a near-miss, not a proof.
- **Do NOT try to reduce $N$ to $P$ by negating coordinates.** A *selective per-coordinate* bit-flip is **not** free in this model: with shared token embeddings $e_0,e_1$, realizing $\tilde e_0-\tilde e_1=\pm(e_0-e_1)$ simultaneously on flipped/unflipped coordinates is contradictory. This is exactly why the stack has only the *full* antipodal invariance (Lemma 35) and positive minors (Lemma 34), not selective negation. (Confidence: medium-high — straightforward linear-algebra obstruction, but I did not formally write it out.)

## Mathlib hits

Largely irrelevant — this is an informal proof resting on internal lemmas. Two are only thematically related: `PMF.normalize_apply` mirrors the softmax normalization $f(a)/\sum_x f(x)$, and `sign_apply`/`Real.sign` mirror the final threshold readout. Neither is needed.

## Actionable leads

1. **Cite Lemma 11 directly:** $\chi_{P,N}$ is a nonconstant LTF $\Rightarrow H^\ast=1$; empty case is constant $\Rightarrow H^\ast=0$. One paragraph, done.
2. **The only lemma-worthy content** is the elementary "$\chi_{P,N}=\mathbf 1[\sum_P x_i-\sum_N x_j>|P|-\tfrac12]$, margin $1/2$" — state and verify this halfspace form, then invoke Lemma 11.
3. **For a from-scratch upper bound**, instantiate Lemma 11's "$\Leftarrow$" atom with $\beta=(+1\text{ on }P,-1\text{ on }N,0)$, $\beta_0=\tfrac12-|P|$; the single atom equals $L(x)$ over positive denominator.
4. **Lower bound** $H^\ast\ge1$: nonconstancy alone (zero-head $\iff$ constant), no need for threshold degree.
5. **Skip** Lemmas 17/18/29 and any selective-negation reduction for the mixed-polarity case — both are dead ends here.
