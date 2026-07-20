# Mixed-Literal DNF Subcube Upper Bound

Let $f : \{0,1\}^{n} \to \{0,1\}$ be an $s$-term DNF whose terms are arbitrary coordinate-subcube indicators. Thus for each $r \in \{1,\ldots,s\}$ there are disjoint sets $P_r,N_r \subseteq \{1,\ldots,n\}$, with $P_r\cup N_r \neq \emptyset$, and

$$
\chi_{P_r,N_r}(x)=\mathbf{1}[x_i=1\text{ for all }i\in P_r\text{ and }x_j=0\text{ for all }j\in N_r],
$$

such that

$$
f(x)=\bigvee_{r=1}^{s}\chi_{P_r,N_r}(x).
$$

In the one-layer attention model of `model.md`, let $H^{\ast}(f)$ denote the least number of attention heads whose summed scalar head outputs, after a final affine threshold, compute $f$ on the Boolean cube. Then

$$
H^{\ast}(f)\leq s.
$$

Equivalently, a union of $s$ arbitrary signed coordinate subcubes is computable with at most one head per subcube.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads
1. **Cleared-denominator construction (Lemma 14)**: build a degree-$s$ sign-representer $P=\theta\prod_r D_r+\sum_r N_r\prod_{g\ne r}D_g$ directly for the union — the product of sign-uniform $D_r$ escapes the single-atom parallelogram obstruction.
2. **Target OR-subadditivity $H^{*}(f\vee g)\le H^{*}(f)+H^{*}(g)$** as a standalone lemma; it implies this target via Lemma 36 and yields $H^{*}\le\min(\mathrm{DNF},\mathrm{CNF})$ size — but first stress-test it on small ORs of LTFs for a possible counterexample.
3. **Do not retry the Lemma-17/29 reciprocal-bump gadget per term**: the antipode law (Lemma 2) provably forbids a single atom from $\ell_\infty$-approximating a mixed-corner bump — this is the lead's own "both-sign violation" obstruction, now made rigorous.
4. **Prove the easier $H^{*}\le 2s$ first** (split each mixed term into positive- and negative-violation single-polarity detectors), but note the OR still won't linearize trivially — use it to expose what aggregation mechanism is actually needed.
5. **Decision-list / "first true term" telescoping** (Rivest 1987) over the $s$ subcubes, realized in the linear-fractional normal form, as an alternative to symmetric bump-summation.
