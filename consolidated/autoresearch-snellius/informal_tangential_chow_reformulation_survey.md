Web search wasn't permitted, so I'll attribute from my own knowledge and mark confidence levels explicitly. I have what I need: the precise admissibility classes (Lemma 13) and the exact `MFdeg`±/$H^*$ equivalence (Lemma 14) that this target repackages. Here is the survey.

---

# Literature survey: the tangential-Chow reformulation

## 0. Orientation — what this target actually is

The deep analytic content is **already proved**: Lemma 14 establishes $H^{*}(f)=\mathrm{MFdeg}_{\pm}(f)$, i.e. $H^{*}(f)$ equals the least $H$ for which a cleared-denominator polynomial $P=\theta\prod_h D_h+\sum_h N_h\prod_{g\neq h}D_g$ (admissible affine pairs) strictly sign-represents $f$ on the cube. The target does **not** re-establish any equivalence about $H^{*}$. It is a **change of coordinates**: homogenize the affine forms, observe that $P$'s homogenization is a *tangent vector to the variety of split forms*, and read $\mathrm{MFdeg}_{\pm}$ off that geometry. So the genuinely new work is (i) one Leibniz/product-rule identity, (ii) the homogenize/dehomogenize bookkeeping, (iii) pinning down *which* tangent space is meant. None of it is hard; the value is conceptual, and there is one definitional subtlety (§3) that is the only place rigor can slip.

The conceptual heart, worth stating early: $\widetilde P$ is generically **not** a product of linear forms — it is a *first-order deformation* of the product $\prod_h\widetilde D_h$. The base point lives on the Chow variety (the denominators); the tangent direction encodes the numerators. That is precisely why a tangent vector sign-represents richer $f$ than any split form could.

## 1. The object: Chow variety / variety of products of linear forms

The "degree-$H$ Chow variety of products of $H$ linear forms" in the target is the classical **variety of completely decomposable (a.k.a. split, factorable) forms**: the image of the multiplication (Chow) map

$$\mu:\ \underbrace{V_1\times\cdots\times V_1}_{H}\longrightarrow \mathrm{Sym}^H V_1,\qquad (\ell_1,\dots,\ell_H)\mapsto \prod_{h=1}^H\ell_h,$$

where $V_1=\langle x_0,\dots,x_n\rangle$. Projectivized, its image is the **Chow variety of degree-$H$, dimension-0 cycles** in $\mathbb{P}^n$ (each $\ell_h$ ↔ a hyperplane ↔ a point of the dual). Generic dimension is $nH$. For $n=1$ (binary forms) every form splits, so the map is essentially onto and you are in the world of **coincident-root loci**; for $n\ge 2$ the split locus is a proper, highly singular subvariety.

Key references (confidence noted):
- **Chow & van der Waerden (1937)**, *Math. Ann.* 113 — origin of Chow forms / Chow coordinates / the Chow variety of cycles. *(High confidence.)*
- **Gelfand–Kapranov–Zelevinsky**, *Discriminants, Resultants, and Multidimensional Determinants* (Birkhäuser, 1994), the **"Chow varieties"** chapter (Ch. 4 in my recollection), including **Brill's equations** — explicit set-theoretic defining equations for the split locus. *(High confidence on book/topic; medium on chapter number.)*
- **Brill's equations** (A. Brill, late 19th c.; related work of Gordan/Hadamard): the classical equations cutting out products-of-linear-forms inside $\mathrm{Sym}^H$. *(Medium-high.)*
- Modern study of the split variety, its **secant varieties and (non)defectivity**: **Arrondo–Bernardi**, "On the variety parametrizing completely decomposable polynomials," *J. Pure Appl. Algebra* 215 (2011); **Abo**, "Varieties of completely decomposable forms and their secants," *J. Algebra* (~2014); related work by **Catalisano–Geramita–Gimigliano** and **Torrance** on Chow/“split” rank. *(Medium confidence on exact authors/years — flag as "verify before citing.")*

**Caveat the lead should internalize:** classical Chow-variety theory is over an algebraically closed field. The target works over $\mathbb{R}$ with **positivity** ($D_h>0$ on the cube) and the sign-uniform coefficient classes of Lemma 13. So the relevant locus is a **real semialgebraic slice** of (the real points of) these varieties, not the full complex variety. The deep Chow-variety machinery (defining ideal, defectivity, dimension) is *context*, not on the proof's critical path — the proof only needs the parametrization and its differential.

## 2. The needed tool: tangent space to the image of a parametrization

This is the only algebraic-geometry fact actually used, and it is elementary. For a parametrization $\mu$, the **embedded (Zariski) tangent space at $\mu(a)$ contains the image of the differential $d\mu_a$**, with equality at smooth points (standard; Harris, *Algebraic Geometry: A First Course*; Shafarevich). For the multiplication map the differential is the **product/Leibniz rule**:

$$d\mu_{(\ell_1,\dots,\ell_H)}(\delta_1,\dots,\delta_H)=\sum_{h=1}^{H}\delta_h\prod_{g\neq h}\ell_g,$$

so the tangent space at $F=\prod_h\ell_h$ is $\ \sum_h (F/\ell_h)\cdot V_1$. The forward direction of the target is then a one-liner: with $\ell_h=\widetilde D_h$ and direction $\delta_h=\widetilde N_h+\tfrac{\theta}{H}\widetilde D_h$,

$$d\mu(\delta)=\sum_h\Big(\widetilde N_h+\tfrac{\theta}{H}\widetilde D_h\Big)\prod_{g\neq h}\widetilde D_g=\theta\prod_h\widetilde D_h+\sum_h\widetilde N_h\prod_{g\neq h}\widetilde D_g=\widetilde P.$$

The $\tfrac{\theta}{H}\widetilde D_h$ piece reproduces $\theta\prod_h\widetilde D_h=\theta F$, which is in the tangent space anyway because the Chow variety is a **cone** and **Euler's identity** $\sum_i x_i\partial_i F=H\cdot F$ puts the apex direction $F$ inside every (smooth) tangent space. So the whole of $\widetilde P$ is literally in the image of $d\mu$ — no genericity needed for the forward direction.

## 3. "Tangential-Chow" and the one subtlety that needs care

The title phrase = the **tangential variety** $\tau(X)=\overline{\bigcup_{p\in X^{sm}}\widehat T_pX}$, the union of embedded tangent spaces of the Chow variety $X$. Background and techniques:
- **Terracini's lemma** (Terracini, *Rend. Circ. Mat. Palermo* 31, **1911**) — the foundational tool for tangent spaces of secant/tangential varieties. *(High confidence.)*
- **Landsberg**, *Tensors: Geometry and Applications* (AMS GSM 128, 2012) — modern treatment of tangential and secant varieties of classical varieties (Veronese/Segre/Chow). *(High confidence.)*
- **Tangential varieties of classical varieties**: Landsberg–Weyman and **Oeding** computed defining equations of tangential varieties of Segre/Veronese; the Chow case is the analogous program. *(Medium confidence on exact titles — verify.)*

**The subtlety (flag this prominently to the lead).** "Affine tangent space" is ambiguous at singular points, and the split variety is singular exactly where factors coincide (repeated $\ell_h$ ↔ non-reduced cycles):
- The **forward** direction holds for *any* reasonable reading (image of $d\mu$ ⊆ Zariski tangent space, always).
- The **converse** ("*every* form in the tangent space dehomogenizes to cleared form") requires the tangent space to equal the **image of $d\mu$**, namely $\{\sum_h\delta_h\prod_{g\neq h}\widetilde D_g\}$. At a *smooth* point (the $\widetilde D_h$ pairwise non-proportional, i.e. squarefree product / reduced cycle) the Zariski tangent space *equals* this image; at singular points it is strictly larger and the converse can fail.

So the clean, exactly-bijective statement defines the tangent space as **the image of the multiplication map's differential** (equivalently restricts to reduced base cycles), not the abstract Zariski tangent space. The lead should pin this down — it is the only real definitional choice in the whole target, and choosing "image of $d\mu$" makes both directions tight without any smoothness side-conditions.

## 4. Homogenization bookkeeping (and a small trap)

The operation $\widetilde{(\cdot)}$ sends an affine form (degree $\le 1$ in $x_1,\dots,x_n$) to a genuine **linear form** in $x_0,\dots,x_n$, and product-of-homogenizations = homogenization-of-product when degrees add. Dehomogenizing ($x_0=1$) inverts it, and the Boolean cube sits inside the affine chart $x_0=1$, so sign-representation transfers verbatim: $\widetilde P(1,x)=P(x)$.

**Trap to note:** the target *defines* $\widetilde P$ **termwise** (sum of $H$ products of linear forms, each of total degree exactly $H$), so it is homogeneous of degree $H$ by construction. This is **not** in general the homogenization of the abstract polynomial $P$ — if the top-degree part of $P$ cancels, $\deg P<H$ and the two differ. The termwise definition is the correct one (it is the one that lands in $\tau(X)$); the proof should use it and not silently identify $\widetilde P$ with "the homogenization of $P$."

## 5. The real/semialgebraic + sign-representation context

The admissibility restriction (Lemma 13: positive constant / all-positive-coeff / all-negative-coeff-with-positive-all-ones denominators; sign-uniform numerators when the denominator is constant) carves a **real semialgebraic cone** inside $\tau(X)(\mathbb{R})$. Translating Lemma 13 into the homogenized picture: each $\widetilde D_h$ is a real linear form whose coordinate coefficients are sign-uniform, and each direction $\widetilde N_h+\tfrac\theta H\widetilde D_h$ is constrained accordingly. This is pure bookkeeping but is where the converse's hypotheses ("base factors dehomogenize to admissible positive denominators, tangent directions to admissible numerators") do their work.

For the sign-representation half of the picture, the relevant known landscape (already partly in the project):
- **Threshold degree / PTFs**: Minsky–Papert, *Perceptrons* (1969) — parity has threshold degree $n$ (your Lemma 7); general PTF theory (Aspnes–Beigel–Furst–Rudich; Sherstov; O'Donnell–Servedio). This is the $\deg_\pm(f)\le H^*(f)$ side (Lemma 6).
- **Rational sign-representation**: your atoms are *ratios* $N_h/D_h$, so the natural cousin is sign-representation by **rational functions / sum of rational atoms**, cf. Newman (1964, rational approx of $|x|$) and Beigel–Reingold–Spielman (PP closed under intersection, 1991/95, via rational functions). The cleared-denominator $P$ is exactly the partial-fractions/common-denominator transform of such a rational score. *(Context for why $\mathrm{MFdeg}_\pm$ is the natural invariant; not needed for the proof.)*

## 6. Relevant vs. irrelevant Mathlib hits

- **Use:** `MvPolynomial.IsHomogeneous.mul` (product of homogeneous forms is homogeneous of summed degree) — directly gives that $\widetilde P$ is homogeneous of degree $H$. `Polynomial.homogenize_finsetProd` (homogenization of a product = product of homogenizations) is the right *statement shape* but is for **univariate→`MvPolynomial (Fin 2)`** only; you need *multivariate* affine→linear homogenization, which these hits do **not** provide ready-made. `splits_iff_exists_multiset'` is the **univariate** ($n=1$/binary) shadow of "product of linear forms" — analogy only.
- **Do NOT use:** `TangentSpace` / `TangentBundle` / `instInhabitedTangentSpace` — these are *differential-geometric* tangent spaces of smooth manifolds modeled on normed spaces. They are the **wrong notion**; the target needs the *algebraic/embedded* tangent space (image of a Jacobian / Zariski tangent space), which is absent from the hits.
- **Ignore:** `Affine.Simplex.*`, `parallelepiped_basisFun`, `convexBodySumFun_nonneg`, `affineCombination_mem_interior_face_iff_pos` (positivity on simplices — loosely echoes "$D_h>0$ on the cube" but not the right tools); `signVariations`/`RuleOfSigns` (Descartes sign-changes — relate to your symmetric Lemma 12, not this target); `ChevalleyThm.*`, `MvPolynomial.indicator` (irrelevant).

## 7. Already-proved? Where the real work is

- **Not** a new fact about $H^*$: the equivalence to a cleared-denominator/admissible-atom degree is **Lemma 14, done**. Do not re-prove it.
- The remaining content is elementary and lives entirely in §2–§4: a Leibniz identity, the cone/Euler observation, and homogenize/dehomogenize bijectivity.
- The **only** place rigor can fail is the §3 definitional choice of "tangent space." Choosing *image of the multiplication-map differential* (reduced base cycles) makes both directions exact; the abstract Zariski tangent space at singular (repeated-factor) points breaks the converse.

## Actionable leads

1. **Prove forward in one line via Leibniz**: set base $\ell_h=\widetilde D_h$, direction $\delta_h=\widetilde N_h+\tfrac{\theta}{H}\widetilde D_h$; then $\widetilde P=d\mu(\delta)$ exactly — no genericity needed.
2. **Define the tangent space as $\mathrm{im}\,d\mu=\sum_h(F/\widetilde D_h)\,V_1$** (equivalently restrict to reduced/squarefree base cycles); this is the choice that makes the converse hold and sidesteps singular-point pathology of the split variety.
3. **Invoke Lemma 14 as a black box** for $H^{*}(f)=\mathrm{MFdeg}_{\pm}(f)$; the target reduces to a homogenize/dehomogenize dictionary plus sign-preservation on the $x_0=1$ chart (where the cube lives).
4. **Cite the standard tangent-space-of-an-image fact** ($\mathrm{im}\,d\mu\subseteq T_{\mu(a)}X$, equality at smooth points — Harris/Shafarevich; Terracini 1911) and the cone/Euler identity to absorb the $\theta\prod\widetilde D_h$ term; this plus Brill/GKZ for naming the object is all the AG you need.
5. **Use $\widetilde P$'s termwise definition, not "homogenization of $P$"** — they differ when $P$'s top degree drops below $H$; `MvPolynomial.IsHomogeneous.mul` certifies degree-$H$ homogeneity of the termwise object.

*Confidence flags: object-naming and the differential computation are textbook (high). Specific modern split-variety/tangential-variety papers (Arrondo–Bernardi, Abo, Oeding, Torrance) are from memory — verify exact titles/years before citing. GKZ chapter number and "Brill's equations" placement are medium confidence.*
