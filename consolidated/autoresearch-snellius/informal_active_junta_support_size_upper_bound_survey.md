I have what I need; both reference lemmas confirm the landscape. Here is the survey.

## Literature survey: Active-junta support-size upper bound

### Bottom line up front
This target is **not new hard mathematics** — it is an immediate corollary of your already-verified **Lemma 32** (active-junta weighted-sum sign-change bound), with one crude estimate sharpened. Lemma 32's consequence already picks injective weights $\lambda_{i_r}=2^{r-1}$, gets $M=|\mathrm{Im}(t_I)|=2^k$, and then bounds $C_{t_I}(G)\le M-1=2^k-1$. The target replaces that last line with the support-sensitive count
$$C_{t_I}(G)\le \min\{2a,\,2b,\,2^k-1\}.$$
So the lead should **not re-derive Lemma 32**; the only new content is a one-line combinatorial inequality about sign changes of a binary string. I'm highly confident in this reduction (I read both `032_...md` and `030_...md`).

### The single fact that does the work
With injective positive weights, $t_I$ is a bijection $\{0,1\}^I\to\mathrm{Im}(t_I)$, so the sorted image $\tau_0<\cdots<\tau_{2^k-1}$ carries a binary label sequence $\sigma_0,\dots,\sigma_{2^k-1}$ with exactly $a$ ones and $b=2^k-a$ zeros. $C_{t_I}(G)$ is the number of adjacent **unequal** pairs (run boundaries) in this sequence. Elementary run-counting: if the ones form $p\le a$ maximal runs and zeros form $q\le b$ runs, then (runs alternate, $|p-q|\le1$) the number of transitions is $p+q-1\le 2\min(a,b)=\min(2a,2b)$, and trivially $\le 2^k-1$. Hence $C_{t_I}(G)\le\min\{2a,2b,2^k-1\}$.

Two things worth flagging to the lead:
- **No weight optimization is needed.** The inequality holds for *every* arrangement of $a$ ones and $b$ zeros, so any injective positive weights (powers of two suffice) give it. You do not need to choose weights to control the sorted order.
- **The single inequality delivers all three terms of the `min` at once**, and it is symmetric in ones/zeros — so you do **not** even need complementation. (If you prefer, the $2b$ term is also `Lemma 31`'s $H^{\ast}(1-f)=H^{\ast}(f)$ applied to the $2a$ bound, but that's redundant here.)

### Where this sits in the proved stack
- **Lemma 32** — the engine. Gives $H^{\ast}(f)\le C_{t_I}(G)$ for any positive active weights; the target is its support-sensitive specialization.
- **Lemma 30** — the constructive core under Lemma 32 (sign polynomial → partial fractions → shifted-reciprocal one-head atoms via Lemma 10).
- **Lemma 31** — irrelevant-variable / permutation / complement invariance (gives the $a\leftrightarrow b$ symmetry for free).
- **Lemma 29** (two-polarity sparse threshold-density) and **Lemma 17/18** — an *alternative* route: write $g$ as the OR of its $a$ minterms; each minterm is a single point = AND of one $\vec 1$-anchored subcube (its 1-coordinates) and one $\vec 0$-anchored subcube (its 0-coordinates), i.e. **2 anchored subcubes per minterm**, giving $2a$ terms. This is where the factor 2 "wants" to come from structurally, but turning OR-of-(AND-of-2) into one flat strict threshold of subcube indicators requires a margin/weighting argument; the Lemma 32 + run-count route is strictly cleaner and avoids that bookkeeping. I'd recommend it as primary.
- **Lemma 12** — the symmetric analog ($H^{\ast}=$ number of Hamming-weight sign changes) is the conceptual template the whole sign-change technique generalizes.

### External known mathematics (context, with confidence)
- **Canonical DNF / minterms** (Boole 1854; Shannon, *A Symbolic Analysis of Relay and Switching Circuits*, 1938): a function with $a$ true points has a sum-of-products with exactly $a$ minterms. "$a$ ones $\Rightarrow$ complexity $\lesssim a$" is the classical version of a support-size bound; the model's factor 2 reflects each mixed-polarity minterm costing two anchored/monotone pieces. (High confidence.)
- **Polynomial threshold functions — degree, sparsity, weight**: Minsky & Papert, *Perceptrons* (1969, threshold "order"); Bruck (1990, harmonic analysis of PTFs); Saks, "Slicing the hypercube" survey (1993); later Klivans–Servedio, O'Donnell–Servedio. Your "sparse threshold-density" lemmas are the model-native cousins of PTF **density** (number of monomials/terms). (Moderate confidence on exact attributions.)
- **Juntas**: Friedgut's junta theorem (1998); textbook treatment in O'Donnell, *Analysis of Boolean Functions* (2014). The only junta fact used here is the trivial one — a $k$-junta is determined by its $2^k$-entry active truth table. (High confidence.)
- **Sign-change / alternation reductions**: reducing a symmetric (or weighted-symmetric) function to a univariate step function and counting sign changes is standard in symmetric-function complexity; for *approximate/threshold degree* of symmetric functions see Paturi (1992). The exact "threshold complexity = number of value-sign-changes" statement is folklore in that line and is exactly your Lemma 12. (Moderate confidence on Paturi attribution.)
- **Distinct subset sums / Sidon sets**: the injective-weights step is just "powers of two give distinct subset sums" — no deep reference needed.
- **Decision lists / subcube covers**: Rivest (1987) — context for "represent the 1-set by few subcubes."

### Is it tight? (so the lead doesn't over-claim)
This is purely an **upper** bound and is generally loose: for parity $a=b=2^{k-1}$, it gives $2^k-1$ while $H^{\ast}=k$ (Lemmas 8/12); for a single minterm $a=1$ it gives $2$ while a conjunction is an LTF with $H^{\ast}=1$ (Lemma 11). Matching lower bounds for small-support functions would need the threshold-degree route (Lemmas 6–7) or Warren-counting (Lemmas 19/24), not this argument.

### Mathlib hits
- **Relevant (mild, bookkeeping only):** `Finset.card_compl` / `Finset.card_compl_add_card` formalize $b=2^k-a$; `Finset.sum_boole` formalizes $a=\#\{u:g(u)=1\}$ as an indicator sum; `min_le_left/right`, `le_min` assemble the three-way `min`. `Finset.indicator_biUnion_eq_sum_powerset` (inclusion–exclusion) is the right tool only if you take the alternative union-of-subcubes route.
- **Irrelevant (false positives):** the `Equiv.Perm.sign_eq_prod_prod_*` and `Fin.sign_cycleIcc` hits are about **permutation sign**, not sign-changes of a step function. Mathlib has no off-the-shelf "number of sign changes of a binary sequence" lemma, so that counting step would be proved from scratch — but it's elementary. (All proofs here are informal markdown anyway, so Mathlib relevance is secondary.)

## Actionable leads
1. **Primary route:** invoke Lemma 32 with any injective positive active weights (powers of two), then replace its `≤ 2^k−1` line with the run-count `C_{t_I}(G) ≤ min{2a, 2b, 2^k−1}`.
2. **The whole new content** is one combinatorial inequality: a binary string with $a$ ones and $b$ zeros has $\le \min\{2a,2b,2^k-1\}$ adjacent-unequal pairs (runs argument: $p\le a$ one-runs, $q\le b$ zero-runs, transitions $=p+q-1\le2\min(a,b)$).
3. **No complementation / no weight tuning needed** — the inequality is symmetric in ones/zeros and arrangement-independent; it yields all three `min` terms simultaneously.
4. **Backup route** (if a non-sign-change proof is wanted): minterm DNF, each point = AND of a $\vec1$-anchored and a $\vec0$-anchored subcube (2 per minterm), assembled via Lemma 29 — but expect extra margin bookkeeping to flatten OR-of-ANDs.
5. **State it as an upper bound only**; cite parity ($a=b=2^{k-1}$, $H^{\ast}=k$) as the witness that $\min\{2a,2b,2^k-1\}$ is far from tight.
