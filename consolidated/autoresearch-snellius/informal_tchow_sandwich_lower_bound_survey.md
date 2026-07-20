I've now confirmed the key internal facts. Here is the survey.

---

# Literature survey: Unrestricted Tangential‑Chow Sandwich Bound

## Bottom line up front (is this already proved?)

**This target is essentially a two‑line corollary of your own already‑verified stack, not a new theorem requiring fresh machinery.** Do not re‑derive the hard linear‑fractional / clearing infrastructure.

- The middle object $\mathrm{tChow}_{\pm}(f)$ is *literally* the cleared‑denominator polynomial of **Lemma 14** (`014_cleared_denominator_invariant.md`),
$$P=\theta\textstyle\prod_h D_h+\sum_h N_h\prod_{g\ne h}D_g,$$
with the **admissibility constraints dropped** ($D_h,N_h$ now arbitrary affine, $\theta$ arbitrary real, no denominator‑class / positivity requirement).
- **Upper inequality $\mathrm{tChow}_\pm(f)\le H^*(f)$ = pure relaxation.** Lemma 14 proves $H^*(f)=\mathrm{MFdeg}_\pm(f)$, where $\mathrm{MFdeg}_\pm$ minimizes $H$ over *admissible* witnesses of exactly this form. Every admissible witness is in particular an unrestricted witness, so the feasible set only grows and the min can only drop: $\mathrm{tChow}_\pm(f)\le \mathrm{MFdeg}_\pm(f)=H^*(f)$.
- **Lower inequality $\deg_\pm(f)\le \mathrm{tChow}_\pm(f)$ = degree counting**, and this exact argument is *already written down* in Lemma 14's "Consequence" (lines 299–309): each summand is a product of $\le H$ affine forms, so $\deg P\le H$; a tChow witness at level $H_0=\mathrm{tChow}_\pm(f)$ is therefore a degree‑$\le H_0$ strict sign‑representer, giving $\deg_\pm(f)\le H_0$. (Use multilinearization on the cube if you want a multilinear representer; degree doesn't increase.)

So the only genuinely new content versus the existing stack is *making the middle term explicit and observing it is sandwiched*. The "fully rigorous proof" the lead must write is short; the bookkeeping that needs care is just the $H=0$ degenerate case (empty product $=1$, $P=\theta$, both ends $\Leftrightarrow f$ constant) and finiteness of $\mathrm{tChow}_\pm$ (immediate from $\le H^*\le 2^n-1$, Lemma 9).

## What the two invariants are, in the literature

**(1) $\deg_\pm(f)$ — threshold degree (the floor).** This is the classical *threshold degree* / *sign degree* / *strong degree* of a Boolean function. Origin: **Minsky & Papert, _Perceptrons_ (1969)**, who introduced it and the **symmetrization** technique (averaging over $S_n$ to reduce multivariate sign‑representation to a univariate polynomial in the Hamming weight). Modern lower‑bound toolkit: the **method of dual polynomials** (LP duality), developed by **Sherstov** and others (e.g. "The intersection of two halfspaces has high threshold degree," ~2009/2013; survey treatment in **Bun–Thaler** on approximate degree / dual polynomials); foundational degree lower bounds in **Aspnes–Beigel–Furst–Rudich, "The expressive power of voting polynomials," _Combinatorica_ 1994**, and **O'Donnell–Servedio, "New degree bounds for polynomial threshold functions"** (~2003/2010). Your Lemmas 6–7 already use this layer ($\deg_\pm(f)\le H^*(f)$; $\deg_\pm(\mathrm{XOR}_n)=n$).

> **Key tightness observation (focuses the search).** For **symmetric** $f(x)=F(|x|)$, Minsky–Papert symmetrization + univariate interpolation gives $\deg_\pm(f)=C(F)$, the number of sign changes of $F$ — which is *exactly* your Lemma 12 value $H^*(f)=C(F)$. Hence **on every symmetric function the sandwich collapses: $\deg_\pm=\mathrm{tChow}_\pm=H^*=C(F)$.** In particular parity ($n$), thresholds ($1$), $\mathrm{EXACT}_{n,k}$ ($2$) are all tight on both sides simultaneously. **Any function separating $\mathrm{tChow}_\pm$ from $\deg_\pm$ or from $H^*$ must be nonsymmetric** — precisely the regime your stack does not yet pin down.

**(2) The tangential‑Chow form — Chow varieties and their tangent spaces.** Your Lemma 15 correctly identifies the homogenized top‑degree part as a *tangent vector to the Chow cone of split forms*: $\sum_h \delta_h\prod_{g\ne h}\ell_g=\frac{d}{dt}\big|_0\prod_h(\ell_h+t\delta_h)$. The relevant known mathematics is the geometry of:
- the **Chow variety / variety of completely decomposable (split) forms** $\mathrm{Split}_H$ — classical; see **Gel'fand–Kapranov–Zelevinsky, _Discriminants, Resultants, and Multidimensional Determinants_ (1994)** for Chow forms, and **Landsberg, _Tensors: Geometry and Applications_ (GSM 128, 2012)** for secant/tangential varieties;
- its **secant and tangential varieties** and their dimensions/defectivity — **Arrondo–Bernardi** on completely decomposable polynomials (~2011, year approximate), work of **Catalisano–Geramita–Gimigliano** and **Abo** on secants of Chow varieties, and "Chow rank" papers (e.g. **Torrance**; exact citations uncertain — mark these as recollections). Apolarity / catalecticant tools: **Iarrobino–Kanev**.

The one quantitative fact worth extracting: $\dim \tau(\mathrm{Chow}_H)\sim 2H(n+1)$, versus ambient degree‑$\le H$ space of dimension $\binom{n+H}{H}$. For fixed $H$ and $n\to\infty$ the tangential‑Chow forms are a *thin* subvariety. So as **polynomials** the tChow form is a real restriction — but sign‑representation is an open condition on only $2^n$ points, so thinness does **not** by itself force $\mathrm{tChow}_\pm>\deg_\pm$. That is the open question (next section).

**(Pre‑cleared object — context only.)** Before clearing, an $H$‑head score is $\theta+\sum_h N_h/D_h$, a sum of $H$ affine‑over‑affine rational atoms. This is reminiscent of **rational sign‑representation** (Newman's 1964 rational approximation of $\operatorname{sign}$; **Beigel–Reingold–Spielman, "PP is closed under intersection," 1991/1995**, using rational functions). But the attention atoms are far more constrained (one affine numerator over one sign‑constrained affine denominator, exactly $H$ summands), so I would not equate $\mathrm{tChow}_\pm$ with any standard "rational degree"; treat it as project‑native.

**(Where $H^*$ comes from — context only, keep brief.)** Exact head‑counting for this one‑layer, single‑query, linear‑readout attention model appears to be your own invariant; I know of no prior exact characterization. Nearby expressivity work: **Hahn (TACL 2020)** (hard‑attention can't do parity/Dyck), **Merrill–Sabharwal (2023)** (log‑precision transformers $\subseteq$ uniform $\mathrm{TC}^0$), **Sanford–Hsu–Telgarsky (NeurIPS 2023)** (head/dimension/precision tradeoffs for specific tasks). These motivate "how many heads" but do not give $H^*(f)$.

## Where a gap can appear (the genuinely open / interesting part)

Both inequalities are *proved* once you cite Lemma 14; the research value of this node is whether either is ever **strict**.

- **$\mathrm{tChow}_\pm$ vs $\deg_\pm$ (is the middle invariant new information?).** At $H=1$, the tChow form is $\theta D_1+N_1=$ arbitrary affine, so $\mathrm{tChow}_\pm(f)\le1\iff f$ is an LTF $\iff \deg_\pm(f)\le1$ — they agree (matches Lemma 11). The first possible separation is $H=2$: there the *top‑degree part* of a tChow form is $\theta\bar D_1\bar D_2+\bar N_1\bar D_2+\bar N_2\bar D_1$, a quadratic form of **rank $\le 4$** (a sum of two products of linear forms), whereas a general multilinear degree‑2 sign‑representer can need a **full‑rank** ($\sim n$) quadratic part. So the tChow constraint is genuinely a *low‑rank / low‑Chow‑rank* restriction on the leading form. Whether that ever **forces** a degree increase for sign representation is open; the natural test family is inner‑product / high‑rank‑quadratic predicates.
- **$\mathrm{tChow}_\pm$ vs $H^*$ (does dropping admissibility lose tightness?).** Admissibility (Lemma 13: constant‑positive / all‑positive / all‑negative‑with‑positive‑all‑ones denominators) is a real constraint; whether the unrestricted relaxation is strictly smaller for some $f$ is open. Equivalently: does the denominator‑sign/positivity structure ever cost a head?

Confidence: the sandwich itself — **high** (it's a corollary, I verified Lemmas 13–15 directly). The strictness questions — **genuinely open**, no citation settles them.

## Relevant Mathlib hits

- **Directly on point for $\deg_\pm\le\mathrm{tChow}_\pm$ (the degree‑$\le H$ bound):** `Polynomial.degree_mul`, `Polynomial.degree_prod`, `MvPolynomial.degreeOf_prod_eq`, `MvPolynomial.degreeOf_mul_eq` — "degree of a product of $\le H$ affine forms is $\le H$." `Polynomial.leadingCoeff_mul` / `leadingCoeff_prod` support the leading‑term/rank analysis above.
- **Marginal (symmetric specialization only):** `Polynomial.signVariations`, `signVariations_neg`, `signVariations_C_mul` (Descartes' rule of signs) and `Polynomial.exists_{min,max}_root` connect to the *univariate sign‑change ↔ root‑count* argument behind the symmetric‑tightness observation, **not** to the general multivariate target.
- **Ignore:** `MvPolynomial.indicator` / `restrictDegree` (finite‑field exact interpolation), Weierstrass `exists_polynomial_near…` (approximation, not sign), Pochhammer positivity — none fit sign‑representation over $\mathbb{R}$.

(Caveat: your stack is informal markdown, not Lean, so these are naming/confirmation references, not a formalization target.)

## Actionable leads

1. **Prove the target as a corollary, not from scratch:** cite **Lemma 14** ($H^*=\mathrm{MFdeg}_\pm$) and relax (admissible $\Rightarrow$ unrestricted) for $\mathrm{tChow}_\pm\le H^*$; reuse Lemma 14's own degree‑$\le H$ "Consequence" for $\deg_\pm\le\mathrm{tChow}_\pm$. Only the $H=0$ case needs explicit handling.
2. **Record the symmetric‑tightness collapse** $\deg_\pm=\mathrm{tChow}_\pm=H^*=C(F)$ (Minsky–Papert symmetrization + your Lemma 12) — it certifies the sandwich is sometimes exact and proves any separation must be nonsymmetric.
3. **Hunt for $\mathrm{tChow}_\pm>\deg_\pm$ at $H=2$** using the rank obstruction: a function whose only degree‑2 sign‑representers have full‑rank quadratic part (inner‑product‑type predicates) is the canonical candidate; this is where the Chow‑tangent constraint could bite.
4. **For strictness reasoning, pull dimension facts on $\tau(\mathrm{Chow}_H)$** from Landsberg (GSM 128, 2012) and the completely‑decomposable‑forms secant literature (Arrondo–Bernardi; Catalisano–Geramita–Gimigliano) — $\dim\sim 2H(n+1)$ vs $\binom{n+H}{H}$ is the heuristic that a gap *can* exist.
5. **If you later want to lower‑bound $H^*$ via this sandwich,** the leverage is threshold‑degree lower bounds (Sherstov's dual‑polynomial method, Bun–Thaler survey) feeding $\deg_\pm\le\mathrm{tChow}_\pm\le H^*$.
