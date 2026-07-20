Web search isn't permitted in this session (same as when the earlier survey was written), so I'll work from the proof I just read plus my own knowledge, flagging confidence on attributions. The most important finding overrides the usual survey framing:

# Survey: quadratic threshold functions can require linearly many heads

## ⚠️ Headline: this target is already proved — do not redo it

The target is **verbatim Lemma 20**, with a complete, *verified* proof at
`lemmas/01_foundations_and_normal_form/020_quadratic_ptf_head_separation.md` (commit `f6a200c`, "verified, autoresearch iter 8"). There is also already a prior survey for it (`informal_quadratic_ptf_head_separation_survey.md`, written *before* the proof existed). **The lead should treat this as closed.** Below I (a) record what route actually closed it, (b) correct the one thing the earlier survey got wrong about difficulty, and (c) ground each ingredient in the known literature so the writeup can cite it.

## What actually closed it (three pillars), and the one correction

The verified proof is a **pure counting / pigeonhole separation**, exactly the regime the earlier survey predicted. Its three pillars:

1. **Upper bound on the cheap class (already in-stack):** Lemma 19 (Warren head-count) gives $\log_2|\mathcal F_{n,H}|\le C\,H\,n\,(n+\log_2(H+1))$, so at $H=cn$ the $\le cn$-head functions number at most $2^{(1+o(1))Cc\,n^3}$.
2. **Lower bound on degree-2 PTFs:** $|\mathcal Q_n|\ge 2^{n^3/243}$, i.e. $2^{\Omega(n^3)}$.
3. **Pigeonhole:** pick $c=\min\{1,a/4C\}$ with $a=1/243$; then $|\mathcal F_{n,cn}|<|\mathcal Q_n|$, so some degree-2 PTF needs $>cn$ heads. The degree is pinned to *exactly* 2 via Lemma 11 ($H^\ast>2\Rightarrow$ not an LTF $\Rightarrow \deg_\pm\ge 2$).

**The correction worth recording.** The earlier survey flagged pillar 2 as "the only real work" and reached for the heavy PTF-counting machinery (Zuev / Baldi–Vershynin) to get $2^{\Omega(n^3)}$. **That machinery was not needed.** The proof gets $2^{\Omega(n^3)}$ elementarily, in two clean steps:
- **An explicit $2^{\Omega(m^2)}$ family of LTFs** (its Lemma 1): binary-weighted forms $L_a(y,z)=\sum_i 2^{i-1}y_i-\sum_j a_jz_j-\tfrac12$ are nonvanishing on the cube and separated by test points $y=\overline{a_j+1},z=e_j$. No Zuev needed.
- **A bilinear "indexing/multiplexer" boost** (its Lemma 2): stack $m$ independently-chosen LTFs as $q(u,v)=t+\sum_{i=1}^m u_i\,\ell_i(v)$. This is **degree 2** (each term is one $u$-variable times an affine form in $v$), and the restriction $u=e_i$ exposes $\ell_i$, so $|\mathcal Q_n|\ge|\mathrm{LTF}_m|^m\ge 2^{\Omega(n^3)}$.

This is the standard "$n^2$ coefficients × $n$ bits of resolution against $2^n$ points $=n^3$ capacity" phenomenon, realized constructively. The earlier survey's *actionable lead #2* sketched exactly this bilinear route, so it pointed the right way — it just over-estimated the difficulty.

## The mathematical crux (for the writeup): $n^2$ vs $n^3$ capacity

The separation is *linear* — not merely $\omega(1)$ — for one clean reason:

| class | capacity (bits) |
|---|---|
| degree-2 PTFs | $\Theta(n^3)$ |
| $\le H$-head functions | $\tilde O(H\,n^2)$ |

Setting $n^3\approx Hn^2$ forces $H\approx n$. Per head buys only $\tilde O(n^2)$ bits of capacity (Warren over $\ell=O(Hn)$ parameters of parameter-degree $\le H{+}1$, via the cleared-denominator form of Lemma 14), while quadratic threshold degree alone buys $\Theta(n^3)$. **This single inequality is why $\deg_\pm\le H^\ast$ (Lemma 6) is loose by a full linear factor at the very bottom of the degree scale.** Note a degree-2-PTF count of only $2^{\Theta(n^2)}$ (the naive "one bit per coefficient" guess) would give merely $H=\Omega(1)$; the extra factor of $n$ is load-bearing.

## Literature grounding, by ingredient (confidence flagged)

**The counting upper bound (pillar 1 / Lemma 19):**
- **Warren (1968)**, "Lower bounds for approximation by nonlinear manifolds," *Trans. AMS* 133 — the sign-pattern count $\le (4edm/\ell)^\ell$ for $m$ degree-$d$ polynomials in $\ell$ variables. This is the exact engine of Lemma 19. *High confidence.*
- **Milnor (1964)** / **Thom (1965)** / **Oleĭnik–Petrovskiĭ (1949)** — sum-of-Betti-number bounds that Warren sharpens into sign-pattern counts. The deep roots. *High confidence.*
- **Goldberg & Jerrum (1995)**, "Bounding the VC dimension of concept classes parameterized by real numbers," *Machine Learning* 18, and **Anthony & Bartlett, *Neural Network Learning: Theoretical Foundations* (1999), Ch. 8** — the canonical "few real parameters ⇒ few dichotomies (via Warren)" packaging. This is the textbook home of Lemma 19's method and the right thing to cite for it. *High confidence.*

**Counting threshold functions (pillar 2):**
- **Cover (1965)**, "Geometrical and statistical properties of systems of linear inequalities…," *IEEE Trans. EC-14* — the function-counting theorem $C(N,D)=2\sum_{k<D}\binom{N-1}{k}$; gives both the LTF/PTF *upper* counts and the general-position picture. *High confidence.*
- **Zuev (1989)**, "Asymptotics of the logarithm of the number of threshold functions…," *Soviet Math. Dokl.* — $\log_2\#\{\text{LTFs on }m\text{ bits}\}=m^2(1-o(1))$. **Context only:** the proof needs just the elementary $2^{\Omega(m^2)}$ direction, which it builds by hand, so Zuev is *not* a dependency. *High confidence on the statement.*
- **Number of degree-$d$ PTFs $=2^{\Theta(n^{d+1})}$** (so $2^{\Theta(n^3)}$ at $d=2$): I associate the systematic capacity study with **Baldi & Vershynin (2019)**, "Polynomial threshold functions, hyperplane arrangements, and random tensors," *SIAM J. Math. Data Sci.* (and the related "capacity of feedforward networks" line). *Moderate confidence on exact title/venue; high confidence on the $\Theta(n^{d+1})$ value.* Again **context, not a dependency** — the in-repo bilinear construction is self-contained. **Saks, "Slicing the hypercube" (1993 survey)** is the readable entry point for the LTF-counting background.

**Threshold degree and the method:**
- **Minsky & Papert, *Perceptrons* (1969)** — origin of threshold degree (the "order" of a predicate). *High confidence.*
- **Shannon (1949)** counting argument (most Boolean functions need large circuits) — the methodological ancestor: bound the cheap class, conclude something outside it exists, non-constructively. The present proof is this paradigm with "circuit size" replaced by "head count." *High confidence.*

## Where this sits: a "low degree, high size" separation by capacity counting

The result belongs to the classical family of **separations between threshold degree and a size/weight-type measure**, proved non-constructively by counting:
- **Threshold degree vs. threshold weight/density:** functions with low $\deg_\pm$ but exponential integer weight or many monomials — **Beigel (1994)** "Perceptrons, PP, and the polynomial hierarchy," and the **Krause–Pudlák / Goldmann–Håstad–Razborov** weight lower bounds. Same moral: $\deg_\pm$ is a weak certificate for size-type cost. The present theorem is the attention-model instance, with "size" = head count. *Moderate-high confidence on the theme.*
- **Contrast / what to avoid:** **Sherstov (2009/2013)**, "The intersection of two halfspaces has high threshold degree" (*FOCS 2009 / SICOMP*) — composing two halfspaces *raises* $\deg_\pm$ to polynomially large ($\Omega(\sqrt n)$-type). The construction here dodges this precisely because $\sum_i u_i\ell_i(v)$ is **bilinear with a selector**, not a generic AND of two halfspaces, so it *stays* at degree 2. Good to state explicitly in the writeup. *High confidence on the qualitative point; moderate on the exact exponent.*
- **Explicit-witness alternative (not used, not needed):** **Sanford, Hsu, Telgarsky (2023)**, "Representational Strengths and Limitations of Transformers" (*NeurIPS*) — one-layer self-attention lower bounds on heads/embedding-dimension via communication complexity (sparse averaging, triple detection). This is the route to a *named* hard $f_n$ if ever wanted; the existence target needs none of it. *Good confidence.*

## Relevant Mathlib hits

- `Finset.card_shatterer_le_sum_vcDim` (Sauer–Shelah) and `Finset.vcDim` — the formalized VC/shatter-counting machinery, the combinatorial cousin of the Warren bound powering Lemma 19. Closest Mathlib analog to the counting upper bound; the sharper *sign-pattern* (Warren) bound itself is **not** in Mathlib. Useful only as a conceptual cross-check.
- `Polynomial.card_mahlerMeasure_le_prod` — a genuine "count of polynomials under a complexity budget" bound; same flavor as Warren's count, different domain. Tangential.
- The degree hits (`MvPolynomial.degrees_indicator`, `Polynomial.ofFn_degree_lt`, `ChevalleyThm.*`) and the `Bool`/softmax hits are **not** relevant — Mathlib has no notion of threshold degree / sign-representation, worth noting for any future formalization.

## Is it published? 

I do not recognize "$H^\ast\ge cn$ at $\deg_\pm=2$ in a one-layer softmax-attention model" as a published theorem — it reads as original to this project. But the *method* (capacity counting separating degree from a parametric size measure) is entirely classical, which is why it closed in one iteration. *Confidence: high.*

## Actionable leads

1. **Do not reprove it.** It is Lemma 20, verified (iter 8). Point any duplicate request at `020_quadratic_ptf_head_separation.md`.
2. **For the writeup's citations,** attach the *method* to **Warren (1968)** + **Goldberg–Jerrum (1995)** / **Anthony–Bartlett (1999)** (counting) and to the **Shannon (1949)** non-constructive paradigm — the actual proof depends on neither Zuev nor Baldi–Vershynin (cite those as context only).
3. **State the $n^2$-vs-$n^3$ capacity gap explicitly** in the writeup — it is the one-line reason the separation is *linear*, and it tells the reader exactly how far Lemma 6 ($\deg_\pm\le H^\ast$) is from tight.
4. **Natural next target (genuinely open here):** push to higher degree — does $\deg_\pm=d$ admit $H^\ast=\Omega(n)$ (or $\omega(n)$)? The same counting (degree-$d$ PTFs $=2^{\Theta(n^{d+1})}$ vs $\tilde O(Hn^2)$) suggests $H^\ast$ could be forced to $\Omega(n^{d-1})$, which would be a stronger separation — worth handing to Codex as a new conjecture.
5. **If a named witness is ever wanted** (beyond the existence statement), lower-bound $\mathrm{tChow}_\pm$ via the Lemma 16 sandwich, or adapt Sanford–Hsu–Telgarsky's communication-complexity head bounds — real work, and unnecessary for the theorem as stated.
