I have what I need. The full Lemma 18 proof is decisive here, so let me write the survey rather than spend effort on web search — the key finding is internal and the external references I can cite from knowledge with confidence markers.

## Literature / landscape survey for: Two-Polarity Sparse Threshold-Density Upper Bound

### Headline: this is essentially already proved — it is a routine re-indexing of Lemma 18

**Confidence: very high.** The target is the per-term-polarity generalization of **Lemma 18** (`018_same_polarity_sparse_threshold_density_upper_bound.md`), which I just read in full. Lemma 18 fixes one global polarity $\zeta$ shared by all $s$ subcubes; the target lets each term carry its own $\zeta_r\in\{0,1\}$. **The fixed-polarity hypothesis is not used in any essential way in the existing proof**, so the lead should not treat this as new mathematics. Concretely:

- Lemma 18 builds $s$ *independent* one-head atoms $\phi_r(x)=c_r/D_r(x)$ with $D_r(x)=1+\sum_i\beta_{r,i}\nu_i(x)$, where the "violation indicator" $\nu_i$ satisfies $\nu_i\in\{0,1\}$ and $\nu_i=0\iff x_i=\zeta$. The atoms never interact; the polarity enters *only* through $\nu$.
- The atom-validity step (Lemma 18's internal "Lemma 1") **already does a full case split** "First suppose $\zeta=0$ … Now suppose $\zeta=1$ …", giving valid Lemma-10 atoms in *both* polarities with different $(\alpha_r,\rho_{r,i},\gamma_r)$.
- To get the two-polarity target: replace the global $\nu_i$ by a **per-term** violation indicator $\nu_{r,i}(x)=x_i$ if $\zeta_r=0$, $=1-x_i$ if $\zeta_r=1$ (so $\nu_{r,i}=0\iff x_i=\zeta_r$). Then atom-validity for term $r$ is *exactly* the existing $\zeta=\zeta_r$ branch. The approximation step ("Lemma 2", $|\phi_r-c_rq_r|\le|c_r|\varepsilon$) and the margin step ("Lemma 3", $|S-T|<\mu/4$ via finitely-many-inputs + positive margin) use only $\nu_{r,i}\in\{0,1\}$ and $\nu_{r,i}=0\iff x_i=\zeta_r$ — both per-term true — so they transfer verbatim.

So the target is **true and provable with zero new ideas**; flag it to the lead as a 1-paragraph extension, not a research step. The only "new" content is bookkeeping (term-indexed $\nu$).

### The supporting internal scaffolding (all already proved)

- **Lemma 10 (linear-fractional normal form):** $H^*(f)=L_{\mathrm{frac}}(f)$ — the reduction that turns "$\theta+\sum_r(\text{one-head atoms})$, one strict threshold" into a head count. This is the engine; it is what makes "$s$ atoms $\Rightarrow H^*\le s$" rigorous, and it is exactly how Lemma 18 concludes.
- **Lemma 13 (affine atom dictionary):** certifies that reciprocal-bump atoms $c_r/D_r$ with all-positive or all-negative-coefficient affine denominators are admissible. This is the precise place where "both anchors ($\vec0$ and $\vec1$) are individually legal" is licensed.
- **Lemma 9 (weighted-sum interpolation upper bound):** the additivity-of-heads / superposition principle (heads add in the residual stream, one final threshold) that underlies the construction.
- **Lemma 17 (same-polarity DNF subcube upper bound):** the OR-aggregation special case of Lemma 18; the two-polarity *DNF* analogue ($f=\bigvee_r I_r$ with mixed anchors) would follow as a corollary of the target by taking $\theta<0$, $c_r$ large.
- **Lemma 11 / Lemma 8:** each $I_r$ is *individually* a one-head function — $\prod_{i\in A_r}x_i=\mathrm{AND}$ and $\prod_{i\in A_r}(1-x_i)=\mathrm{NOR}$ are linear threshold functions, so $H^*(I_r)=1$. (Not directly used — the construction needs the *real-valued* atom $\approx c_rI_r$, not its Boolean threshold — but it's a useful sanity check that the per-subcube cost of 1 is tight.)

### What the object is, in standard terms

Each $I_r$ is a **monochromatic conjunction** (all positive literals or all negative literals): a subcube through the all-$0$ or all-$1$ vertex. It is *not* a general term $x_1\wedge\bar x_2$ (a subcube through an arbitrary vertex) — that case is genuinely outside this target. The expression $\theta+\sum_r c_rI_r$ is then a **real linear combination of $s$ such conjunctions**, and $f=\mathrm{sign}(\cdot)$ is a **sparse polynomial threshold function in the term (DNF-monomial) basis**, sparsity $s$, with the subcubes restricted to two anchor vertices. The quantity $s$ is a **"threshold density"** (number of terms) measure. The target says: *head complexity $\le$ this two-anchor threshold density.*

### External known mathematics (context; confidence marked)

- **Sparse PTFs / "threshold-of-terms" / PTF density.** Thresholds of conjunctions are a classical depth-2 model: top linear-threshold gate over AND gates = a $\mathsf{TC}^0\circ\mathsf{AND}$ circuit, equivalently a real-weighted *threshold over DNF terms*. The number of terms ($s$ here) is the standard sparsity/density parameter. Related: Bruck (1990) and Bruck–Smolensky on polynomial threshold representations; Saks' survey "Slicing the hypercube" (1993); Beigel's survey on PTFs; O'Donnell, *Analysis of Boolean Functions* (2014), Ch. 5 for PTFs/threshold degree. *Confidence: high on the framing, medium on exact attributions of the density-specific results.*
- **DNF size / subcube covers.** $\bigvee_r I_r$ is a subcube cover; the minimum number of subcubes is "DNF size"/"cover number." Standard combinatorics-of-Boolean-functions material (Jukna, *Boolean Function Complexity*, 2012). The target's $s$ upper-bounds head complexity by a cover-type quantity. *Confidence: high.*
- **Transformer expressivity via soft→hard ("saturated") attention.** The mechanism "scale logits so softmax concentrates, realizing AND/OR over a selected coordinate set" is the standard hard-attention-as-a-limit idea. Closest references: Pérez–Marinković–Barceló (2019/2021) on attention and Turing-completeness; **Merrill–Sabharwal–Smith, "Saturated transformers are constant-depth threshold circuits"** ($\sim$2022) tying saturated attention to $\mathsf{TC}^0$; Hahn, "Theoretical Limitations of Self-Attention" (2020, Lipschitz lower bounds — relevant to *lower* bounds, not this); **Sanford–Hsu–Telgarsky, "Representational Strengths and Limitations of Transformers"** (NeurIPS 2023, single heads computing sparse functions); Likhosherstov–Choromanski–Weller on the expressive power of self-attention matrices. *Note:* the project's actual construction does **not** invoke hard attention — it uses the project's own **reciprocal-bump linear-fractional atoms (Lemma 10/13)** plus a **margin/robustness pass** (finitely many inputs + positive margin ⇒ finite sharpness suffices). The external literature is analogy, not a load-bearing citation. *Confidence: medium-high on names, low on exact dates — treat as pointers to verify.*
- **Margin / robustness to pass from soft to exact** is the universal technique here (and in Lemma 18): standard "finite domain + strictly-signed margin ⇒ a sufficiently sharp continuous surrogate realizes the same Boolean function." No special citation needed.

### Mathlib hits triage

The target is *informal*, so these are only relevant if the lead later formalizes:
- **Relevant primitives:** `Set.indicator_pi_one_apply` and `prod_indicator_const_apply` (subcube indicator $=$ product of per-coordinate indicators — the right way to define $I_r$); `Set.indicator_prod_one` (same idea, binary product). `PMF.tsum_coe` / `PMF.hasSum_coe_one` / `PMF.normalize_apply` (attention weights as a normalized PMF summing to 1) if attention is ever modeled measure-theoretically.
- **Irrelevant (ignore):** all `Affine.Simplex.*touchpointWeights*` / `excenterWeights` hits (simplex geometry), `evalBoundingSieveWeights` (Selberg sieve), and both `ProbabilityTheory.Fernique.*` hits (Gaussian-measure tail bounds — the "geometric weighting" match is spurious). `Set.boolIndicator` is only marginally useful.

### Actionable leads
1. **Reuse Lemma 18 verbatim with a term-indexed violation indicator** $\nu_{r,i}$ keyed to $\zeta_r$; its existing $\zeta\in\{0,1\}$ case split already proves atom validity for both anchors — this *is* the proof. (Highest-value lead by far.)
2. **Cite Lemma 10** for the reduction "$s$ admissible atoms $+$ one strict threshold $\Rightarrow H^*\le s$," and **Lemma 13** to license both all-positive and all-negative-coefficient denominators.
3. **Keep the same margin pass** ($\varepsilon=\mu/(4(B+1))$, $\Lambda$ large, $\kappa$ small): it uses only $\nu_{r,i}\in\{0,1\}$ and $\nu_{r,i}=0\iff x_i=\zeta_r$, both per-term, so it transfers unchanged.
4. **Record the two-anchor restriction explicitly:** terms are conjunctions through $\vec0$ or $\vec1$ only; a genuinely new step would be needed for general-vertex subcubes (mixed literals within one term), which this target does *not* cover.
5. **Optionally state Lemma 17's two-polarity DNF analogue as an immediate corollary** ($\theta<0$, $c_r$ large $\Rightarrow f=\bigvee_r I_r$), to close that gap in the same write-up.
