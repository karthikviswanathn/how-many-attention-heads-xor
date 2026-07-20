Both load-bearing lemmas confirm what I suspected. Here is the survey.

---

# Literature Survey: Active-Junta Weighted-Sum Sign-Change Upper Bound

## Bottom line up front

**This target is essentially already proved inside your own verified stack.** It is the composition of two lemmas already on `master`:

- **Lemma 30** (`030_weighted_sum_sign_change_upper_bound.md`) gives $H^{\ast}(g)\le C_{t_I}(G)$ *verbatim* when applied to the active function $g:\{0,1\}^{I}\to\{0,1\}$ — its hypotheses (positive weights, a 1-D statistic $t$, sign-change count along the sorted image, $\tau_0=0$ at the all-zeros point) match the target's hypotheses on $g$ exactly, with "$n$" $=k=|I|$.
- **Lemma 31** (`031_irrelevant_variable_invariance.md`) gives $H^{\ast}(f)=H^{\ast}(g)$, since $f(x)=g(x_I)$ is $g$ with dummy coordinates added (and possibly permuted); it proves dummy-variable invariance *and* coordinate-permutation invariance, which is all you need to pass from $\{0,1\}^{I}$ to $\{0,1\}^{n}$.

Chaining them: $H^{\ast}(f)=H^{\ast}(g)\le C_{t_I}(G)$. **The lead should not redraft a from-scratch proof** — the only genuinely new content beyond Lemma 30 is the localization to the active set, and Lemma 31 already supplies that. (Lemma 31 itself invokes Lemma 26 for one direction, so the restriction-monotonicity machinery is also in place.)

The "$2^k-1$ for every $k$-junta" corollary needs one extra elementary observation, not a new lemma: choose **injective positive weights** on the active set — e.g. a superincreasing/powers-of-two sequence $\lambda_{i_r}=2^{r-1}$, the classic distinct-subset-sums trick — so $t_I$ separates all $2^k$ points of $\{0,1\}^{I}$. Then $M=2^k$, and a $\pm1$ sequence on $M$ ordered points has at most $M-1=2^k-1$ sign changes, so $C_{t_I}(G)\le 2^k-1$ for *any* $G$. This is exactly the junta-localized form of your **Lemma 9** ("every Boolean function on $n$ bits has $H^{\ast}\le 2^n-1$"), pushed through Lemma 31.

## How it sits in the proved stack

| Ingredient | Role | Status |
|---|---|---|
| Lemma 30 | sign-change upper bound for a function of one positive weighted sum | proved (iter 15) |
| Lemma 31 | $H^{\ast}$ ignores dummy variables + permutation-invariant | proved (iter 17) |
| Lemma 26 | restriction monotonicity (used inside L31) | proved (iter 12) |
| Lemma 9 | universal $2^n-1$ bound | proved |
| Lemma 12 | *exact* sign-change value $H^{\ast}=C(F)$ for **symmetric** $f$ | proved |

The target is to Lemma 12 what Lemma 30 is to the unweighted symmetric case: it replaces the symmetric Hamming statistic $|x|$ (equal weights) by a general **positive weighted Hamming statistic** $t_I$, and keeps only the **upper-bound** half. Lemma 12's lower-bound half ($H^{\ast}\ge C$) does *not* generalize for free — see "What is open" below.

## Relevant known mathematics

**1. Juntas.** A function depending on at most $k$ of its $n$ coordinates is a **$k$-junta**; the standard reference is O'Donnell, *Analysis of Boolean Functions* (Cambridge, 2014). The structural fact you are using — that any reasonable complexity measure depends only on the relevant coordinates and is blind to dummy ones — is folklore there and is precisely your Lemma 31. The companion literature (Fischer–Kindler–Ron–Safra–Samorodnitsky, "Testing Juntas," JCSS 2004 / FOCS 2002; Blais, "Testing juntas nearly optimally," STOC 2009) is about *testing* the junta property and is not needed for an upper bound, but it is where the term and the $f=g\circ\mathrm{restrict}_I$ formalism live.

**2. Generalized (weighted) symmetric functions.** A function of the form $g(u)=G\!\left(\sum_i\lambda_i u_i\right)$ — constant on the level sets of a single positive linear form — is the natural generalization of a symmetric function (the equal-weights case $\lambda_i\equiv1$). The governing complexity parameter is the number of **alternations / sign changes** of $G$ along the sorted image, which is exactly $C_{t_I}(G)$. That "number of value-changes of a symmetric function controls its complexity" is a recurring theme: e.g. Paturi, "On the degree of polynomials that approximate symmetric Boolean functions" (STOC 1992), characterizes *approximate* degree of symmetric $f$ by where $F$ changes value near the middle (I'm confident on the result, less so that it transfers to threshold-degree, so treat as analogy not citation). Your Lemma 12 is the clean threshold-model instance.

**3. Sign variations / Descartes' rule of signs — the interpolation engine.** The upper-bound mechanism (visible inside Lemma 30) is: a $\{0,1\}$-valued function on $M$ ordered points with $C$ sign changes is sign-represented by a degree-$C$ polynomial (drop one root into each gap where the sign flips), which partial-fractions into $C$ "shifted reciprocals," each realizable by **one head**. This is the constructive dual of **Descartes' rule of signs** (Descartes, *La Géométrie*, 1637): #positive roots $\le$ #sign variations of the coefficients. The "one threshold per breakpoint of a 1-D statistic" construction is also exactly a **1-decision-list** over a sorted score (Rivest, "Learning decision lists," *Machine Learning* 1987) — a useful mental model for why $C$ pieces cost $C$ heads.

**4. The universal $2^k$ bound and distinct subset sums.** Making one positive linear form injective on $\{0,1\}^k$ is the **superincreasing-sequence / distinct-subset-sums** idea (powers of two; Merkle–Hellman knapsack folklore). It converts "$g$ is an arbitrary function on $k$ bits" into "$g$ is a function of one injective statistic with $2^k$ values," giving $\le 2^k-1$ pieces. Identical in spirit to "every Boolean function on $n$ bits has threshold degree $\le n$" and to your Lemma 9.

## Mathlib hits — which are on-target

- **`Polynomial.signVariations`**, **`Polynomial.roots_countP_pos_le_signVariations`** (Descartes), **`signVariations_neg`** (in `Mathlib.Algebra.Polynomial.RuleOfSigns`): the formal analogue of $C_{t_I}(G)$ and of the sign-change↔root-count principle behind Lemma 30's construction. **Most relevant.** The `signVariations_neg` invariance mirrors your complement-invariance ($H^{\ast}(1-f)=H^{\ast}(f)$).
- **`DependsOn`**, **`dependsOn_iff_exists_comp`** (`f` depends on `s` $\iff f=g\circ\mathrm{restrict}_s$), **`dependsOn_iff_factorsThrough`**: the exact formalization of the junta hypothesis $f(x)=g(x_I)$. **Relevant** for stating the target.
- **`LocallyConstant.lift`**, **`Quot.factor_mk_eq`**: "a function constant on level sets factors through the quotient" — i.e. the factorization $g=G\circ t_I$ through the fibers of $t_I$. **Relevant** to the $G$-on-image step.
- **`StrictMonoOn.map_finsetSort`**, **`Finset.val_strictMono`**: sorting the distinct values $\tau_0<\dots<\tau_{M-1}$. **Mildly relevant** (bookkeeping).
- **`Finset.centroidWeightsIndicator` / `sum_centroidWeightsIndicator`**: weighted-indicator sums — **only superficially relevant** (wrong domain); ignore.

## What is established vs. open; confidence

- **Established (high confidence):** the inequality $H^{\ast}(f)\le C_{t_I}(G)$ and the $2^k-1$ corollary. Both follow by composition from your already-*verified* Lemmas 30/31 (+ Lemma 9). I read both proofs; they support the composition with no gap. The only checks are bookkeeping: $g$'s statistic still has $\tau_0=0$ (true, $t_I(\vec0)=0$), and the relabeling $\{0,1\}^I\cong\{0,1\}^k$ is a permutation (covered by Lemma 31).
- **Open / not claimed by the target:** *tightness*. The target is an upper bound only. A matching lower bound $H^{\ast}(f)\ge C_{t_I}(G)$ would be the weighted analogue of Lemma 12's lower half and is **not** automatic — with general positive weights the image can have collisions and the "one head buys exactly one sign change" lower bound can fail; equal weights (Lemma 12) is special. I'd flag a weighted-symmetric *exact* characterization as genuinely harder and currently open in your stack.

## Actionable leads

1. **Just compose:** $H^{\ast}(f)=H^{\ast}(g)\le C_{t_I}(G)$ via **Lemma 31** (dummy + permutation invariance) then **Lemma 30** applied to $g$ on $\{0,1\}^{I}$ — no new construction needed.
2. **For $2^k-1$:** pick **injective positive weights** (superincreasing $\lambda_{i_r}=2^{r-1}$, distinct subset sums) so $M=2^k$, then a $\pm1$ sequence on $M$ ordered points has $\le M-1$ sign changes — this is **Lemma 9** localized by Lemma 31.
3. **Sanity-check the one bookkeeping point:** confirm $t_I(\vec0)=0$ so Lemma 30's $\tau_0=0$ normalization carries over to $g$; the $\{0,1\}^I\to\{0,1\}^k$ relabel is a Lemma 31 permutation.
4. **Do not attempt a lower bound:** the matching $H^{\ast}\ge C_{t_I}(G)$ is the weighted generalization of **Lemma 12** and does not follow from this route; leave it as a separate (likely harder) target.
5. **Mathlib framing if formalizing:** state the hypothesis with `DependsOn`/`dependsOn_iff_exists_comp`, and the sign-change count against `Polynomial.signVariations` / Descartes (`roots_countP_pos_le_signVariations`).
