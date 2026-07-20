# Tangential-Chow Reformulation of the Cleared-Denominator Invariant

Let $f : \{0,1\}^n \to \{0,1\}$ and let $H \geq 1$. An affine pair $(N_h,D_h)$ is admissible if it is one of the affine atom pairs from Lemma 13, with $D_h(x)>0$ on $\{0,1\}^n$. Let

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x)
$$

be a cleared-denominator sign-representer from Lemma 14, so $f(x)=1$ exactly when $P(x)>0$ on the Boolean cube.

Homogenize affine forms by writing

$$
\widetilde D_h(x_0,x)=x_0D_h(x/x_0), \qquad \widetilde N_h(x_0,x)=x_0N_h(x/x_0),
$$

and define the homogeneous degree-$H$ form

$$
\widetilde P(x_0,x)=\theta\prod_{h=1}^{H}\widetilde D_h(x_0,x)+\sum_{h=1}^{H}\widetilde N_h(x_0,x)\prod_{g\neq h}\widetilde D_g(x_0,x).
$$

Then $\widetilde P$ lies in the affine tangent space at $\prod_h \widetilde D_h$ to the degree-$H$ Chow variety of products of $H$ linear forms. Conversely, every homogeneous form in such a tangent space, whose base factors dehomogenize to admissible positive denominators and whose tangent directions dehomogenize to admissible numerators, restricts at $x_0=1$ to a polynomial of the cleared-denominator form in Lemma 14.

Consequently $H^{*}(f)$ is exactly the least $H$ for which $f$ has a strict Boolean-cube sign-representer obtained by dehomogenizing an admissibility-restricted tangent vector to the degree-$H$ Chow variety.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Prove forward in one line via Leibniz**: set base $\ell_h=\widetilde D_h$, direction $\delta_h=\widetilde N_h+\tfrac{\theta}{H}\widetilde D_h$; then $\widetilde P=d\mu(\delta)$ exactly — no genericity needed.
2. **Define the tangent space as $\mathrm{im}\,d\mu=\sum_h(F/\widetilde D_h)\,V_1$** (equivalently restrict to reduced/squarefree base cycles); this is the choice that makes the converse hold and sidesteps singular-point pathology of the split variety.
3. **Invoke Lemma 14 as a black box** for $H^{*}(f)=\mathrm{MFdeg}_{\pm}(f)$; the target reduces to a homogenize/dehomogenize dictionary plus sign-preservation on the $x_0=1$ chart (where the cube lives).
4. **Cite the standard tangent-space-of-an-image fact** ($\mathrm{im}\,d\mu\subseteq T_{\mu(a)}X$, equality at smooth points — Harris/Shafarevich; Terracini 1911) and the cone/Euler identity to absorb the $\theta\prod\widetilde D_h$ term; this plus Brill/GKZ for naming the object is all the AG you need.
5. **Use $\widetilde P$'s termwise definition, not "homogenization of $P$"** — they differ when $P$'s top degree drops below $H$; `MvPolynomial.IsHomogeneous.mul` certifies degree-$H$ homogeneity of the termwise object.

*Confidence flags: object-naming and the differential computation are textbook (high). Specific modern split-variety/tangential-variety papers (Arrondo–Bernardi, Abo, Oeding, Torrance) are from memory — verify exact titles/years before citing. GKZ chapter number and "Brill's equations" placement are medium confidence.*
