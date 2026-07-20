I have what I need. The two files confirm exactly where this target sits, so I can ground the survey precisely rather than guess.

# Literature survey: Same-polarity sparse threshold-density upper bound

## 1. Framing — this is a margin-robust generalization of an already-proved lemma

The target is **not new territory**; it is the signed, arbitrary-threshold, margin-quantified generalization of **Lemma 17** (`017_same_polarity_dnf_upper_bound.md`), which is already verified on the main branch. Lemma 17 proves exactly the special case

$$c_r = +1,\quad \theta = -\tfrac{7}{12}\ \text{(an OR-threshold)},\qquad f=\bigvee_r q_r .$$

The target replaces the disjunction by an **arbitrary strict linear threshold** $\theta+\sum_r c_r q_r>0$ with signed reals $c_r$ and a stated margin $\mu>0$. The bound $H^\ast(f)\le s$ (one head per subcube) is identical; only the readout combination and the rounding analysis change. **The lead should reuse Lemma 17's gadget, not rebuild it.**

The machinery Lemma 17 already supplies:
- **Lemma 10** (linear-fractional normal form): $H^\ast(f)\le H$ iff $f$ is a strict threshold of a constant plus $H$ one-head atoms $\phi_h=N_h/D_h$.
- **Lemma 13** (affine atom dictionary): each $D_h$ is a positive affine form in one of three classes; crucially, **for a nonconstant admissible denominator *any* affine numerator is realizable** (its Lemma 5). This is the hook for signed coefficients — see below.
- Lemma 17's **"one-sided bump" atom** $\phi_r=1/D_r$ with $D_r=1+\sum_i\beta_{r,i}\nu_i(x)$, where $\nu_i$ is the polarity-violation indicator. It is $\ge 2/3$ on subcube $A_r$ and $\le 1/(2s+1)$ off it.

## 2. The technique that applies: saturated bumps + margin-robust sign preservation

The whole content of the generalization is a standard **ε-approximation-under-a-margin** argument layered on the existing bump:

1. **Per-head bump rescaled by $c_r$.** Replace $\phi_r=1/D_r$ by $\phi_r=c_r/D_r$. By Lemma 13's numerator-freedom clause, a constant numerator $N_r\equiv c_r$ (any sign) is admissible with the same nonconstant $D_r$, so **negative coefficients need no special handling** — they do not have to be pushed into $W_O$/$w$. This is the single most useful fact for the lead.
2. **Sharpen the bump to any tolerance.** Lemma 17 fixed $\lambda=2s$, $\mu_{\text{out}}=1/(2n)$. Here, make the in-set weight $\lambda\to\infty$ and the out-of-set weight $\mu_{\text{out}}\to0$ so that $\phi_r$ approximates $c_r q_r$ uniformly: on-subcube value $\to c_r$, off-subcube value $\to 0$. These two limits are independent (different coordinates), so $|\phi_r-c_rq_r|\le\varepsilon_r$ for any prescribed $\varepsilon_r$.
3. **Absorb total error into the margin.** Choose weights so $\sum_r\varepsilon_r<\mu$. Then $\theta+\sum_r\phi_r$ has the same sign as $\theta+\sum_r c_rq_r$ at every cube point, because the latter has magnitude $\ge\mu$ everywhere. Threshold at $\theta$; conclude by Lemma 10.

This is the same "**finite cube + positive margin ⇒ finite parameters suffice**" principle already used in Lemma 4 (symmetric thresholds, exact at finite logits) and throughout the upper-bound stack. No genuine limit/closure argument is needed; a large-enough finite $\lambda$ works.

**Two points worth flagging to the lead:**
- **Role of $\mu>0$.** The hypothesis is exactly a non-degeneracy condition: it forbids $\theta+\sum_r c_rq_r$ from being *exactly* $0$ at any cube point (which the iff would otherwise permit on the $f=0$ side, since $0\not>0$). Over the finite cube, "vanishes nowhere" already gives $\mu=\min|\cdot|>0$ automatically — so $\mu$ is not an extra quantitative knob, just the statement that the representing form is sign-definite with a gap. The construction *needs* this gap to round correctly at the boundary.
- This is a pure **upper-bound** contribution; it feeds the "what $s$ heads can compute" side and is independent of the exact-characterization frontier (Lemmas 14–16, cleared-denominator / tangential-Chow). It does not interact with those.

## 3. External landscape — what known mathematics this instantiates

**(a) Polynomial threshold functions (PTFs) and "density"/sparsity.** Set $\zeta=1$: then $q_r(x)=\prod_{i\in A_r}x_i$ is a monotone monomial, so $\theta+\sum_r c_rq_r$ is a **multilinear polynomial with $\le s$ monomials** and $f=\mathbf 1[P>0]$ is a PTF. The target therefore reads: *head complexity $\le$ the number of same-polarity terms in a margin-bounded threshold representation.* The "number of monomials/terms" parameter is the classical **density** (also called **sparsity**, **length**, or **PTF size**; the exact word varies by author — mild uncertainty on which is canonical). This is precisely the project's title phrase "threshold-density." For $\zeta=0$ the monomials are anti-monotone $\prod_{i\in A_r}(1-x_i)$, i.e. $s$-sparse in the shifted basis anchored at $0^n$. The "**same polarity / common anchor vertex $\zeta^n$**" restriction means all terms are conjunctions simultaneously true at one vertex — a structured subclass of depth-2 **threshold-of-AND** ($\mathrm{LT}\circ\mathrm{AND}$) circuits.

**(b) Minsky–Papert and threshold-of-masks.** *Perceptrons* (Minsky & Papert, 1969; expanded 1988) studies a predicate as a linear threshold of "**masks**" — partial predicates that are exactly subcube/conjunction indicators — and defines **order** as the max mask support. The target's representation is precisely a positive/signed linear threshold of masks; the bound counts masks (density) rather than order (degree). High confidence on the conceptual match; this is the canonical historical reference for "threshold of conjunctions."

**(c) Sparse-PTF complexity literature** (for context, not directly needed): Bruck, "Harmonic analysis of polynomial threshold functions" (SIAM J. Discrete Math, 1990); Bruck–Smolensky (1992); Aspnes–Beigel–Furst–Rudich, "The expressive power of voting polynomials" (Combinatorica, 1994); Saks, "Slicing the hypercube" survey (1993). These concern degree/weight/sparsity tradeoffs for sign-representation. They are the right *neighborhood* but none gives this attention-model statement — the result is **model-internal**, so the operative "known result" really is Lemma 17 plus the dictionary.

**(d) Attention-expressivity / saturation.** The bump construction is the project's concrete instance of **saturated / hard attention**: as logits scale, softmax concentrates and a head acts as a near-indicator. Relevant: Hahn, "Theoretical Limitations of Self-Attention" (TACL 2020); Merrill & Sabharwal et al. on **saturated attention** and "saturated transformers are constant-depth threshold circuits" ($\mathrm{TC}^0$), ~2022 (title/date from memory — verify); Sanford–Hsu–Telgarsky, "Representational Strengths and Limitations of Transformers" (NeurIPS 2023), where a single head selects a sparse pattern. These motivate "one head detects one sparse same-polarity conjunction," though they prove asymptotic separations, not exact per-head counts like this project.

## 4. Mathlib hits — which are actually useful

Mostly low-level formalization aids (this is an informal target), but several are genuinely on-point:
- **`Set.indicator_pi_one_apply`** and **`Profinite.NobelingProof.Products.eval_eq`** — indicator of a product set = product of coordinate indicators, and "eval = 1 iff all listed coords true, else 0." These *are* the subcube indicator $q_r$; the right primitives if any of this is ever formalized.
- **`PMF.normalize_apply` / `PMF.tsum_coe`** — softmax = normalize of a positive vector; attention weights form a PMF summing to 1. The denominator-clearing in Lemma 13/17 is exactly this normalization.
- **`AkraBazziRecurrence.tendsto_zero_sumCoeffsExp` / `tendsto_atTop_sumCoeffsExp`** — limits of $\sum_i a_i b_i^{p}$ as $p\to\pm\infty$. This is the **saturation limit** ($b_i=e^{\text{logit}_i}$, $p$ = inverse temperature); the available tool if a true limit (rather than a large finite $\lambda$) were wanted.
- `sign_apply` / `Real.sign` — the final strict threshold.

Ignore the `MvPolynomial.indicator` (finite-field) and `Polynomial.signVariations` hits; they are off-target here.

## 5. Established vs. open; confidence

- **Established (in-project):** Lemma 17 (DNF/OR special case, $H^\ast\le s$) is verified. The normal form (10) and dictionary (13, incl. numerator freedom) are verified. **High confidence** the target follows from these by the margin argument in §2 — I checked the bump rescaling and error budget close.
- **Open (in-project):** the signed, arbitrary-$\theta$, margin version stated here is **not yet in the stack**; that is what this target adds.
- **External:** no published result states this attention-model bound; it is a model-native upper bound. The *type* of statement (heads ↔ term-sparsity of a threshold-of-conjunctions) is classical in spirit (Minsky–Papert masks; PTF density). Confidence high on the conceptual lineage, medium on exact author/word attributions flagged above.

## Actionable leads
- **Reuse Lemma 17's bump verbatim**, replacing numerator $1$ by the constant $c_r$ (Lemma 13's numerator-freedom for nonconstant denominators handles negative $c_r$ — no $W_O$ trickery needed).
- **Drive the bump tolerance with the margin:** pick in-set weight $\lambda$ large / out-of-set weight small so $\sum_r|\phi_r-c_rq_r|<\mu$; sign is then preserved everywhere. Same "finite cube + margin ⇒ finite logits" move as Lemma 4.
- **Use $\mu>0$ only as non-degeneracy** (form vanishes nowhere on the cube); note $\mu=\min|\cdot|$ is then automatic — state this so the hypothesis isn't over-read as a quantitative assumption.
- **Conclude via Lemma 10:** constant $\theta$ + sum of $s$ atoms ⇒ $H^\ast(f)\le s$; no need to touch the tangential-Chow frontier (14–16).
- **Framing for the writeup:** present it as "head complexity ≤ same-polarity subcube-threshold density," the signed generalization of the DNF (OR) bound — the natural sparsity analogue of the degree bound (Lemma 6).
