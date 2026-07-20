I have permission to use web search denied, so I'll produce the survey from my own knowledge of the transformer-expressivity and Boolean-complexity literature (cutoff Jan 2026), flagging attributions I can't re-verify. The mathematical content of this target is clear enough that the survey doesn't hinge on a web lookup.

---

# Literature survey: same-polarity DNF subcube upper bound

## 0. What the target is, in standard terms

The function $f=\bigvee_{r=1}^{s}\bigwedge_{i\in A_r}\mathbf 1[x_i=\zeta]$ is a **same-polarity (read-once-free) DNF**: a union of $s$ axis-aligned subcubes, all anchored at a common vertex (all-ones if $\zeta=1$, all-zeros if $\zeta=0$). For $\zeta=1$ this is exactly a **monotone DNF** with $s$ terms; for $\zeta=0$ it is its order-dual (monotone-decreasing). The claim $H^{\ast}(f)\le s$ is therefore:

> **head complexity of a monotone (or anti-monotone) Boolean function is at most its DNF term count** — "one head per subcube."

This is an *upper-bound / constructive* statement. The matching lower bound (when is $H^\ast=s$ exactly?) is **not** part of the target and is genuinely harder.

## 1. What the project stack already gives you (so the lead doesn't redo it)

- **The $s=1$ case is fully settled.** A single term $\bigwedge_{i\in A_r}\mathbf 1[x_i=\zeta]$ is a linear threshold function ($\mathbf 1[\sum_{i\in A_r}(\pm x_i)\ge t]$), so $H^\ast=1$ by **Lemma 4** (one head computes every symmetric threshold) and **Lemma 11** ($H^\ast(f)=1\iff f$ is a nonconstant LTF). The target is the $\bigvee$-combination of $s$ such facts.
- **Lemma 9 (weighted-sum interpolation) does *not* directly cover this.** It needs $f=F(t(x))$ for a *single* positive weighted sum $t(x)=\sum\lambda_i x_i$; a general union of subcubes is not a level set of one weighted sum. So Lemma 9 gives the $s=1$ case and the symmetric cases, but the general $s$-term DNF is outside it. **The target is not currently in the stack** — it is a new upper bound.
- **Cleanest formal route is via Lemmas 10/13, not raw attention parameters.** Lemma 10 says $H^\ast(f)=L_{\mathrm{frac}}(f)$, the least number of linear-fractional atoms whose constant-plus-sum sign-represents $f$. So it suffices to exhibit **$s$ atoms (one per term)** in that normal form. Lemma 13's "affine atom dictionary" (admissible $D>0$ denominators: all-positive-coefficient / all-negative-coefficient / constant-positive) is exactly the regime a saturated subcube-detector lives in. This avoids re-deriving the attention$\to$atom reduction.
- **Consistency / lower-bound levers already present:** Lemma 6 gives $\deg_\pm(f)\le H^\ast(f)$ and Lemma 16 the tangential-Chow sandwich. Combined with the target you'd get $\deg_\pm(f)\le H^\ast(f)\le s$ for these $f$ — consistent (a monotone $s$-term DNF has $\deg_\pm\le\max_r|A_r|$, often $\ll s$, so the target's term-count bound is the *resource-counting* bound, not the tightest possible).

## 2. The proof technique that applies — and the one pitfall

The standard and correct technique is a **per-head one-sided "soft subcube indicator" (bump), summed and strictly thresholded**:

1. **Polarity reduction.** WLOG $\zeta=1$: swapping the (freely chosen) token embeddings $e_0\leftrightarrow e_1$ flips all bits, so the $\zeta=0$ case is symmetric.
2. **Each head $\to$ a scalar one-sided bump.** Compose the readout $w$ with $W_O^{(h)}$ (model.md, Notes 2–3) so head $r$ contributes a *scalar* $c_r(x)=w^\top W_O^{(r)}\widetilde y^{(r)}(x)$, a softmax-weighted average $\sum_j\alpha_j\nu_j$ of scalar values $\nu_j$. Configure head $r$ (one per term $A_r$) so that **a single violated literal pulls attention onto a $\nu=0$ position**, while a default position — naturally the **query token itself** (it is always present and attendable, model.md masking convention) — carries value $\nu=B$ and wins whenever *no* literal of $A_r$ is violated. With logit scale $L\to\infty$ this gives $c_r(x)\approx B\cdot\mathbf 1[\text{term }r\text{ active}]+O(e^{-L})$, **uniformly nonnegative and one-sided**.
3. **OR by summation + strict threshold.** $S(x)=\sum_r c_r(x)-\tau$. With $\ge 1$ active $\Rightarrow S\ge B-s\epsilon$; with $0$ active $\Rightarrow S\le s\epsilon$. Pick $L$ large enough that $s\epsilon<B/2$ and $\tau=B/2$; the strict threshold then computes $f$ exactly. **Finiteness of $\{0,1\}^n$ means you never need exact hard attention — a single large $L$ separates all $2^n$ values.** Absorb the constant query-skip term into $\tau$ (Note 3).

**The pitfall / why "same polarity" is in the hypothesis (important).** A single head has *one* logit direction $\psi^{(r)}$, so the sign of its value-gap $b_0^{(r)}-b_1^{(r)}=\psi^{(r)}\!\cdot(e_0-e_1)$ is fixed; the positional part $a_j=\psi^{(r)}\!\cdot p_j$ shifts both logits equally and cannot flip that sign. Hence one head's saturated detector can host an all-positive **or** all-negative literal-violation flag, **but not both at once** — so the bump gadget needs each *term* to be internally single-polarity. (A *single* mixed-polarity term is still an LTF, so $H^\ast=1$ for it by Lemma 11; what may fail is realizing it as a *composable one-sided bump*.) Note the gadget only needs **within-term** homogeneity — different heads may use opposite polarities — so the target's *common* $\zeta$ across all terms is a clean special case (it additionally makes $f$ globally monotone, via `monotone_or`/`monotone_and`). **Do not drop the same-polarity hypothesis casually: it is exactly what makes each head a one-sided bump that adds without cancellation.**

**Why you cannot shortcut via a generic "OR-subadditivity" lemma.** $H^\ast(f\vee g)\le H^\ast(f)+H^\ast(g)$ is *not* generally available: "$P>0$ or $Q>0$" is not a single threshold of a sum of atoms ($\operatorname{sign}\max(P,Q)\neq\operatorname{sign}(P+Q)$). The subcube case works *only* because each summand is a one-sided bump. So the right factoring is two reusable lemmas: (a) **one head realizes a single same-polarity subcube as a one-sided bump with explicit margin**, and (b) **a strictly-thresholded sum of one-sided bumps computes their OR**.

## 3. Broader literature (context; attributions from memory, flagged where uncertain)

**Transformer expressivity / circuit complexity** (the home of "what one head/layer can compute"):
- **Merrill, Sabharwal & Smith, "Saturated Transformers are Constant-Depth Threshold Circuits," TACL 2022** — introduces *saturated attention* (softmax driven to its saturated/hard limit), the exact mechanism your bump exploits; places such transformers in $TC^0$. Most on-point conceptual reference.
- **Merrill & Sabharwal, "The Parallelism Tradeoff: Limitations of Log-Precision Transformers," TACL 2023** — log-precision transformers $\subseteq$ uniform $TC^0$.
- **Hahn, "Theoretical Limitations of Self-Attention," TACL 2020** — hard-attention can't compute PARITY/Dyck (Lipschitz/influence argument); the *lower-bound* counterpart to your PARITY result, not used here but good contrast.
- **Strobl, Merrill, Weiss, Chiang & Angluin, "What Formal Languages Can Transformers Express? A Survey," TACL 2024** — umbrella survey; best single entry point to the above.
- **Chiang, Cholak & Pillay, "Tighter Bounds on the Expressivity of Transformer Encoders," ICML 2023** *(title approximate)*.

**Single-head capacity / sparse-function representation** (closest to "one head per term"):
- **Sanford, Hsu & Telgarsky, "Representational Strengths and Limitations of Transformers," NeurIPS 2023** — what one head/layer can and cannot represent (sparse averaging / "$q$-sparse" detection); the "one head per primitive" flavor and separation results.
- **Edelman, Goel, Hsu, Malladi & Arora, "Inductive Biases and Variable Creation in Self-Attention Mechanisms," ICML 2022** — a single head can represent sparse interactions; covering-number/capacity bounds.
- **Yun, Bhojanapalli, Rawat, Reddi & Kumar, "Are Transformers Universal Approximators of Sequence-to-Sequence Functions?", ICLR 2020** — *contextual mapping*: attention manufactures distinct codes, the seed of "attention as a selective/indicator detector."
- **Bhattamishra, Ahuja & Goyal, "On the Ability and Limitations of Transformers to Recognize Formal Languages," EMNLP 2020**; and Bhattamishra et al. on learning Boolean functions / sparse parities with transformers *(exact title uncertain)*.
- **Barceló, Kozachinskiy et al., on logical languages / FO-with-counting and (hard-attention) transformer encoders, ~2024** *(attribution uncertain)* — relates attention acceptors to logic, where conjunctions/ANDs are the easy primitives.
- **Pérez, Barceló & Marinkovic, "Attention is Turing-Complete," JMLR 2021** — far end of the expressivity spectrum (arbitrary precision); context only.

**Boolean-function side (the "competing invariant"):**
- **Minsky & Papert, *Perceptrons* (1969/1988)** — threshold-degree lower bounds ($\deg_\pm(\mathrm{PARITY})=n$), the route behind Lemmas 6–7.
- **PTF degree of DNFs:** Klivans–Servedio (learning DNF, ~2001–04) and **Beigel's** rational-approximation / `ODD-MAX-BIT` results give $s$-term DNFs PTF degree $\tilde O(n^{1/3})$-type bounds. These bound *degree*, a different measure than *term count* — useful to note that the target's bound (per-term head cost) is generally incomparable to, and can be far larger than, threshold degree.
- Standard: a monotone DNF's terms $=$ prime implicants $=$ maximal all-ones subcubes; minimal term count $=$ a **subcube cover** of $f^{-1}(1)$. Your construction is literally "one bump per cover element."

I am **not aware of a prior result stating exactly "head complexity $\le$ DNF term count" for this specific one-layer attention model** — the model is the project's own, so the precise statement is plausibly novel. The *construction* (one saturated head per AND-term, summed) is, however, folklore in the expressivity literature above.

## 4. Mathlib hits — which are usable

- **`Profinite.NobelingProof.Products.eval_eq`** — *directly relevant*: it is the AND-of-coordinates / monomial indicator ($\mathrm{eval}=1$ iff all listed coordinates are `true`, else `0`), i.e., the Lean-native single subcube/DNF-term indicator. Good anchor for "term $=$ product indicator."
- **`monotone_or`, `monotone_and`** — *relevant*: formalize that the $\zeta=1$ DNF is a monotone Boolean function (OR of ANDs of positive literals); the structural fact underlying the one-sided-bump construction.
- **`Finset.affineCombination_indicator_subset`, `Finset.centroidWeightsIndicator(_def)`, `weightedVSubOfPoint_indicator_subset`** — *moderately relevant*: an attention output is a convex (affine, weights-sum-to-1) combination of value vectors, and *saturated* attention is precisely an **indicator-weighted** combination (weight supported on the argmax-logit positions). These are the formal home for the convex-combination step if/when this is Lean-ified.
- **`Set.sUnion`, `BoxIntegral.Prepartition.iUnion(_def)`, `squareCylinders_eq_iUnion_image`, `union_C0C1_eq`** — *analogy only*: "union of boxes/cylinders" $=$ union of subcubes; subcube-by-coordinate splitting. No usable lemma.
- The **`Sat.Literal` / `Clause`** hits are just SAT datatypes — **noise**, ignore.

## Actionable leads

1. **Work in the Lemma-10/13 normal form, not raw attention:** exhibit $s$ linear-fractional atoms (one per term) whose constant-plus-sum sign-represents $f$; then $H^\ast\le s$ is immediate from $H^\ast=L_{\mathrm{frac}}$. Cleanest rigorous path.
2. **Factor the proof into two reusable lemmas:** (a) one head realizes a single same-polarity subcube as a *one-sided bump* with explicit margin $[0,\epsilon]$ vs $\ge B$; (b) a strictly-thresholded sum of one-sided bumps computes their OR. Reuse (a) as the $s=1$ refinement of Lemma 4/11.
3. **Saturation gadget:** baseline = the query token carrying the "on" value $B$; any violated literal in $A_r$ pulls attention to a $0$-value position; take logit scale $L$ large — finiteness of the cube makes one $L$ separate all $2^n$ inputs (no exact hard attention needed).
4. **Guard the hypothesis:** the construction needs *within-term* single polarity (the sign of a head's $b_0-b_1$ gap is fixed); the target's common $\zeta$ is the clean monotone special case. Do not state a general "$H^\ast(f\vee g)\le H^\ast(f)+H^\ast(g)$" — it is false in general; one-sidedness is essential.
5. **Cross-check direction with Lemma 6/16:** $\deg_\pm(f)\le H^\ast(f)\le s$ should hold for these $f$ — a quick consistency sanity check, and a reminder that the term-count bound is generally loose versus threshold degree.
