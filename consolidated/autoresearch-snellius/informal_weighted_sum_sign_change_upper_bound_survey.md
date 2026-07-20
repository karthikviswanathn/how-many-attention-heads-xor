I have the full picture now. The target is the common generalization of two already-proved results in the stack, and its proof route is essentially assembled from existing pieces. Here is the survey.

---

# Survey: Weighted-Sum Sign-Change Upper Bound

## What this target is, in known terms

$f = F\circ t$ with $t(x)=\sum_i \lambda_i x_i$, $\lambda_i>0$, is a **function of a single positive linear form** — a *weighted (generalized) symmetric function*. The claim $H^\ast(f)\le C_t(F)$ says: head cost is bounded by the number of times the induced univariate predicate $F$ flips value along the ordered level set $\tau_0<\cdots<\tau_{M-1}$. This is the model-specific instance of a classical principle: for functions of one (weighted) sum, the governing complexity parameter is the **number of sign changes / "intervals"** of the level predicate, not the number of levels.

## This is already 90% proved in your own stack — flag before any new work

The target is **exactly the common generalization of Lemma 9 and the upper-bound half of Lemma 12**, and both ingredients already exist:

- **Lemma 12, sub-lemma "Lemma 3" (`012_symmetric_sign_changes.md:135–179`)** proves precisely $H^\ast(f)\le C(F)$ for the *unit-weight* case $t=|x|$. Its proof is: (i) build a degree-$C$ univariate sign-representer $P$ with one root between each sign-change pair; (ii) write $P/B$ with $B=\prod_{j=1}^C(z+r_j)$, $r_j>0$ distinct, and partial-fraction it to $c+\sum_{j=1}^C \frac{d_j}{z+r_j}$; (iii) realize each $\frac{d_j}{|x|+r_j}$ as one head; (iv) sum $C$ heads + offset + strict threshold.
- **Lemma 9 (`009_weighted_sum_upper_bound.md`)** already builds the **weighted** single-head gadget: its "Head $j$" produces readout-direction output $g_j(t(x))=\frac{\alpha_j t}{1+\Lambda+(\alpha_j-1)t}$, a Möbius function of $t(x)=\sum\lambda_i x_i$, via the positional-embedding trick $p_i=(\log\lambda_i)\,r$ so the "1"-bit logit is $\log(\alpha_j\lambda_i)$. A Möbius map $\frac{\alpha t}{A+(\alpha-1)t}$ is affinely equivalent to $c'+\frac{d'}{t+r'}$ with pole $r'=\frac{A}{\alpha-1}>0$ (for $\alpha>1$).

**The target = transport Lemma-12-Lemma-3 from $|x|$ to $t(x)$, using Lemma 9's head as the weighted "shifted reciprocal" atom.** Step (i)'s root-placement works identically because the $\tau_j$ are just an increasing real sequence (put a root in each open interval $(\tau_{j-1},\tau_j)$ at a sign change). Steps (ii)–(iv) are verbatim. So the lower-bound machinery is **not** needed and should not be re-derived; this is a pure reuse/upper-bound assembly. The untracked file `informal_weighted_sum_sign_change_upper_bound.md` currently holds only the problem statement — no proof has been started.

## The core known mathematics (each step has a standard name)

1. **Step function = telescoping sum of monotone Heaviside steps.** A $\{\pm1\}$ step function on an ordered finite set with $C$ sign changes equals $\sigma_0+\sum_{\text{jumps }j}(\sigma_j-\sigma_{j-1})\mathbf 1[s\ge \tau_j]$ — exactly $C$ nonzero terms. Equivalently, it is **sign-represented by a degree-$C$ univariate polynomial** (one linear factor per sign change). Elementary; this is the heart of "one head per sign change."
2. **Univariate sign-interpolation by a product of linear factors** (Lemma 12-Lemma-1's $P(z)=\sigma_0\prod(\text{midpoint}-z)$). Classical Lagrange/sign interpolation.
3. **Partial-fraction decomposition** of a proper rational function with simple real poles → sum of shifted reciprocals. Standard; supplies the per-head atoms.
4. **One attention head = one linear-fractional (Möbius) atom of a positive weighted sum.** This is your Lemma 10 (normal form) + Lemma 13 (affine atom dictionary). Crucially, the shifted reciprocal $\frac{d_j}{t+r_j}$ is a **nonconstant-denominator** atom (Lemma 13, class 2/3, $\alpha\neq1$), which by Lemma 13-Lemma-5 admits an *arbitrary* affine numerator — so realizing any coefficient $d_j$ is unobstructed. Positive weights $\lambda_i>0$ are consistent with the all-positive-coefficient logit structure $\log(\alpha_j\lambda_i)$.
5. **Exact (not approximate) realization via strict threshold on a finite set** — positive margin because the cube is finite. Same care as Lemmas 18/29 ("strict threshold with positive Boolean-cube margin").

## External literature (with confidence)

- **"Number of sign changes / intervals of a symmetric predicate" as the complexity parameter** for threshold circuits / neural nets: Minsky–Papert, *Perceptrons* (1969); Bruck, "Harmonic analysis of polynomial threshold functions," *SIAM J. Discrete Math.* (1990); Siu–Roychowdhury–Kailath line on discrete neural computation (early-mid 1990s). *Medium-high confidence* that sign-change/interval count is the standard parameter; *exact* attributions approximate.
- **Threshold / weighted-threshold (LTF) logic**: Muroga, *Threshold Logic and Its Applications* (1971). "Positive weighted sum then lookup" is a generalized LTF. *High confidence.*
- **Descartes' rule of signs / variation-diminishing / total positivity** (Descartes 1637; Schoenberg; Karlin, *Total Positivity*, 1968): "#sign changes bounds #roots needed." This is the **dual / lower-bound** principle (it underwrites why $C$ is also a lower bound in the symmetric case via Lemma 6/threshold degree), *not* the target's upper-bound direction — but it's the right frame for why the symmetric case achieves equality and why the weighted case may not. *High confidence on the principle.*

## Mathlib hits — triage

- **Relevant (soft-step primitive):** `Real.sigmoid`, `unitInterval.sigmoid`, `unitInterval.sigmoid_le_iff` (monotonicity $\sigma(a)\le\sigma(b)\iff a\le b$). The logistic step is the analytic shadow of your single-head monotone-in-$t$ gadget (cf. Lemma 4's strictly increasing $s(k)$). Useful if/when formalized.
- **Relevant (sign-change counting / Descartes infrastructure):** `Polynomial.signVariations`, `Polynomial.roots_countP_pos_le_signVariations`, and especially `Polynomial.succ_signVariations_le_X_sub_C_mul` (multiplying by $X-\eta$, $\eta>0$, adds a sign variation) — the exact "one factor per sign change" mechanism behind step (2). Pertains to the dual lower-bound side, but it is the natural Lean home for $C_t(F)$.
- **Weakly relevant:** `MeasureTheory.stoppedValue_piecewise_const'` (a two-piece step as a sum of indicators — the 2-level instance of step (1)); `Finset.piecewise_*`; `monotone_stieltjesFunctionAux` (monotone step).
- **Irrelevant:** all `Equiv.Perm.sign*` hits (permutation sign — false match on "sign").

## Caveats to keep the lead honest

- **Upper bound only — no equality**, unlike Lemma 12. The symmetric equality used permutation-symmetrization (Lemma 12-Lemma-1), which **fails for non-unit weights**; so $\deg_\pm(F\circ t)\ne C_t(F)$ in general and the matching lower bound is not available. The target correctly claims only $\le$.
- **$C_t(F)$ is representation-dependent** (depends on $\lambda$ and on how levels collapse), whereas $H^\ast(f)$ is intrinsic. The bound is only as good as the chosen $(\lambda,F)$; the useful invariant is $\min_\lambda C_t(F)$.
- **Consistency check passes:** $C_t(F)\le M-1$ always, so the target dominates Lemma 9 exactly as advertised.

## Actionable leads

1. **Lift Lemma 12's "Lemma 3" verbatim with $|x|\rightsquigarrow t(x)$** (`012_symmetric_sign_changes.md:135–179`) — this is the entire proof skeleton.
2. **Reuse Lemma 9's "Head $j$" as the weighted shifted-reciprocal atom** (`009_weighted_sum_upper_bound.md:73–130`): its $g_j(t)=\frac{\alpha_j t}{1+\Lambda+(\alpha_j-1)t}$ is the Möbius/$\frac{d_j}{t+r_j}$ gadget, with $r_j=\frac{1+\Lambda}{\alpha_j-1}>0$.
3. **Build the degree-$C$ sign-representer** $P(s)=\sigma_0\prod_{j:\,\sigma_{j-1}\neq\sigma_j}(m_j-s)$ with $m_j\in(\tau_{j-1},\tau_j)$, then **partial-fraction $P/\prod(s+r_j)$** into $c+\sum_{j=1}^{C}\frac{d_j}{s+r_j}$ (one head each) — steps (i)–(ii) above.
4. **Invoke Lemma 13 class-2/3 (nonconstant denominator ⇒ arbitrary affine numerator)** to certify each $d_j$ is realizable, and finish with one strict threshold using the finite-cube positive margin (cf. Lemmas 18/29).
5. **Do not attempt a matching lower bound** — symmetrization breaks for non-unit weights, so only $\le$ is provable here.
