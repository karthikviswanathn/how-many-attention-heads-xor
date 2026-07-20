# Literature Survey, Round 1: Tools for Lower-Bounding Head Complexity Beyond Threshold Degree

*Author: Claude (research agent). This is an AI-authored write-up placed under `claude-comments/` per repo convention; it does not modify any existing repo file, in particular not `literature_survey.md` (which is upper-bound focused).*

## How this helps

The open problem is to characterize $H^{\ast}(f)$ for nonsymmetric $f$, and the crux is a **lower-bound method that proves $H^{\ast}(f)$ strictly exceeds the threshold degree $\deg&#95;{\pm}(f)$**. The two existing lower bounds (the $\deg&#95;{\pm} \le H^{\ast}$ inequality and planted-parity restriction) both also lower-bound $\deg&#95;{\pm}$, so neither can ever separate the two quantities. This survey collects external tools that *can* in principle break that barrier, organized by the six requested topics, with the two most promising routes first:

- **Route A (sign-pattern / parameter counting, Topic 4).** An $H$-head classifier is described by $N = O(Hn)$ real parameters and a sign test of bounded algebraic degree. Warren / Milnor-Thom / Cover bound the number of *distinct Boolean functions* such a family can realize by $2^{O(Hn \log n)}$. There are $2^{\Theta(n^2)}$ linear threshold functions and $2^{\Theta(n^3)}$ degree-2 PTFs (all of threshold degree $\le 2$), so most of them require $H = \Omega(n/\log n)$ (resp. $\Omega(n^2/\log n)$) heads, a genuine separation $H^{\ast} \gg \deg&#95;{\pm}$. This is the single most promising route: it is *non-constructive but unconditional*, it has an exact published precedent (Alon-Moran-Yehudayoff's count of low-sign-rank matrices is this same argument), and it exploits the one structural fact we have, that head complexity is a low-parameter-count resource. (Note: the brief's "$2^{\Theta(n^2)}$ degree-2 PTFs" is off by a power of $n$; $2^{\Theta(n^2)}$ is the *linear* count, degree-2 is $2^{\Theta(n^3)}$. This only strengthens the separation.)

- **Route B (Chow / tangential-variety rank obstructions, Topic 3).** The normal form makes the sign-representing polynomial $P$ a *tangent vector at a product of $H$ linear forms* to the Chow variety $\mathrm{Ch}&#95;H$. Algebraic geometry has rank-style obstructions (flattenings, catalecticants, Young/Koszul flattenings, Brill's equations) that lower-bound how many linear factors a form needs / whether it lies on a low secant or tangential variety. Transcribing one of these to "minimum number of affine factors of a tangent vector" would give a *constructive, per-function* lower bound on $H^{\ast}$, complementing the counting route.

Topics 1, 2, 5, 6 supply the surrounding map: exact threshold-degree values and the dual-polynomial method (so we know what $\deg&#95;{\pm}$ *is* for candidate separators), sign-rank (a second lower bound on $H^{\ast}$ via the sandwich, and itself parameter-count-bounded), the TC0 ceiling on one-layer attention, and the neuron-counting analogy from one-hidden-layer threshold networks (where exactly this counting route is classical).

**Verification status.** I flag each result as **[verified]** (statement confirmed against a fetched/search-returned primary or authoritative secondary source) or **[recalled]** (standard textbook fact stated from memory, reference is real but exact constants/parameters should be double-checked against the cited source). PDF fetches for several primary sources (AMS, arXiv PDFs, the Bun-Thaler survey) returned 403 or were compression-garbled, so some exact constants are **[recalled]**; the references themselves are real.

---

## Topic 4 (PRIORITY): Sign-pattern counting and the parameter-counting separation route

This is the route most likely to prove $H^{\ast} > \deg&#95;{\pm}$. The logic is a **counting incompatibility**: few parameters can only realize few functions. **Two facts were verified this round against primary PDFs and they sharpen (and correct) the brief's premise:** (a) Warren's constant is $4e$ (Theorem 3, original AMS paper); (b) **degree-2 PTFs number $2^{\Theta(n^3)}$, not $2^{\Theta(n^2)}$ — the $2^{\Theta(n^2)}$ count is the linear ($d=1$) case.** This *strengthens* the separation. And there is a published precedent that is *literally this argument*: Alon-Moran-Yehudayoff's count of low-sign-rank matrices via Warren (Section 4.7).

### 4.1 Warren's theorem (the core counting bound)

**Statement [VERIFIED verbatim against the original AMS PDF].** *(Warren 1968, Theorem 3.)* Let $p_1, \dots, p_m$ be real polynomials in $n$ variables each of degree $\le d \ge 1$, with $m \ge n$. Then the number of distinct **strict sign vectors** $(\mathrm{sgn} p_1(x), \dots, \mathrm{sgn} p_m(x)) \in \lbrace -1,+1 \rbrace^m$ (no zeros) realized over $x \in \mathbb{R}^n$ is at most
$$\left(\frac{4 e d m}{n}\right)^{n}.$$
The constant is exactly $4e$ for strict patterns. Including zeros / all sign conditions in $\lbrace -1,0,+1 \rbrace^m$ gives $\le (8edm/n)^n$ (Ronyai-Babai-Ganapathy Cor. 2.3, by the $g_i = p_i^2 - \varepsilon$ doubling trick). Warren's Theorem 2 also bounds the connected components of $\mathbb{R}^n \setminus \bigcup_i \lbrace p_i = 0 \rbrace$ by $\sum&#95;{k=0}^{n} 2 (2d)^n 2^k \binom{m}{k}$.

**Reference.** Hugh E. Warren, "Lower bounds for approximation by nonlinear manifolds," *Trans. Amer. Math. Soc.* **133** (1968), 167-178, DOI [10.1090/S0002-9947-1968-0226281-1](https://doi.org/10.1090/S0002-9947-1968-0226281-1) (PDF fetched, HTTP 200, Theorem 3 read verbatim). Doubling-trick form: L. Ronyai, L. Babai, M. K. Ganapathy, "On the number of zero-patterns of a sequence of polynomials," *JAMS* **14** (2001), Cor. 2.3.

**How it advances the project.** This is the engine of Route A. Fix a head budget $H$. By the normal form, an $H$-head classifier's decision is $\mathrm{sign}\big(c + \sum&#95;{h} N_h(x)/D_h(x)\big)$ with $N_h, D_h$ affine; clearing the positive denominators, the label of input $x \in \lbrace 0,1 \rbrace^n$ is the sign of one polynomial $P_\theta(x)$ that is **multilinear of degree $\le H$ in $x$** and **polynomial of degree $\le H$ in the $N = O(Hn)$ real head-parameters $\theta$** (each of the $2^n$ cube points gives one polynomial constraint $p_x(\theta) = P_\theta(x)$, viewed as a polynomial in $\theta$). Apply Warren in $\theta$-space with $m = 2^n$ constraints, $N = O(Hn)$ variables, degree $d = O(H)$: the number of distinct sign patterns over $\theta$, i.e. the number of *distinct Boolean functions realizable with $H$ heads*, is at most $\big(4 e  O(H)  2^n / O(Hn)\big)^{O(Hn)} = 2^{O(H n^2)}$. This raw bound (degree taken as $2^n$ worth of monomials) is too lossy; the right tool is the cube-aware region-counting lemma below, which gives $2^{O(Hn\log n)}$.

### 4.2 The separation arithmetic (corrected counting)

**The clean form.** Use the learning-theory region-counting lemma (Section 4.3): an $H$-head family is a concept class with $N = O(Hn)$ real parameters whose label is a sign of a bounded-degree polynomial, so on the $M = 2^n$ cube points it realizes at most $2\big(2 e M D / N\big)^{N} = 2^{O(Hn \log n)}$ distinct functions (with $D = \mathrm{poly}(n)$). Set this against the verified function counts (Section 4.4):
- vs. the $2^{\Theta(n^2)}$ **linear** threshold functions: $2^{O(Hn\log n)} \ge 2^{c n^2}$ forces $H = \Omega(n/\log n)$;
- vs. the $2^{\Theta(n^3)}$ **degree-2** PTFs: forces $H = \Omega(n^2/\log n)$.

**How it advances the project.** Either way **almost every degree-2 PTF (which has $\deg&#95;{\pm} = 2$) requires $H^{\ast} = \omega(1) \gg 2$**, a genuine separation of $H^{\ast}$ from threshold degree. It is non-constructive (does not name the hard function) but unconditional. To make it a theorem one must (i) pin down the exact parameter count $N$ per head in the normal form and (ii) confirm the per-cube-point constraint degree $D$ in $\theta$. The number-of-functions side is fully verified (Cover, Baldi-Vershynin). *This is the highest-leverage item in the survey.* Suggested phrasing for the writeup: "$2^{\Theta(n^2)}$ linear threshold functions already force $H = \Omega(n/\log n)$; the $2^{\Theta(n^3)}$ degree-2 PTFs push this to $\Omega(n^2/\log n)$."

### 4.3 The learning-theory application template (parameter -> labelings)

**Statement [VERIFIED verbatim].** *(Goldberg-Jerrum 1995, Thm 2.2; Anthony-Bartlett 1999, Thm 8.3; clean Warren form: Bartlett-Harvey-Liaw-Mehrabian 2019, Lemma 17.)* If membership "$x$ is labeled 1" is a Boolean formula over $s$ atomic predicates, each a polynomial (in)equality of degree $\le d$ (equivalently $\ell$) in the $k$ real parameters, then
$$\mathrm{VCdim} \le 2k \log_2(8 e d s) = O(k\log(ds)),$$
and (Anthony-Bartlett Thm 8.3, for $m \ge k/ (\text{params})$) the growth function obeys $\Pi(m) \le 2\big(2 e m s d / k\big)^{k}$. The clean Warren restatement (BHLM Lemma 17): the number of sign patterns of $M$ degree-$D$ polynomials in $W \le M$ variables is $\le 2(2 e M D / W)^W$.

**Reference.** P. Goldberg and M. Jerrum, *Machine Learning* **18** (1995), 131-148, Thm 2.2. M. Anthony and P. Bartlett, *Neural Network Learning: Theoretical Foundations*, Cambridge UP (1999), Thm 8.3. P. L. Bartlett, N. Harvey, C. Liaw, A. Mehrabian, "Nearly-tight VC-dimension and pseudodimension bounds for piecewise linear neural networks," *JMLR* **20** (2019), [paper 17-612](https://jmlr.org/papers/volume20/17-612/17-612.pdf), Lemma 17 (= clean Warren) and Thm 19 (= Goldberg-Jerrum).

**How it advances the project.** This is *precisely* the abstraction needed for Route A and it is battle-tested (it is how VC dimension of polynomially-parameterized nets is proved). The $H$-head model is exactly a "concept class parameterized by real numbers": $\theta$ are the $O(Hn)$ head parameters, the predicate is a single sign test of a degree-$O(H)$ polynomial. Plugging $k = N = O(Hn)$, $s = 1$, $M = 2^n$ gives the $2^{O(Hn\log n)}$ count of Section 4.2 and $\mathrm{VCdim}(H\text{-head class}) = O(Hn\log n)$. **Citing BHLM Lemma 17 / Goldberg-Jerrum lets the project reuse a published, refereed counting lemma rather than re-deriving Warren.**

### 4.4 The counting target: 2^Θ(n²) linear and 2^Θ(n³) degree-2 threshold functions

**Statement [VERIFIED verbatim against arXiv:1803.10868].** *(Baldi-Vershynin 2019, Thm 1.1 / Cor. 1.2.)* For $1 \le d \le n^{0.9}$, with $\binom{n}{\le d} := \sum&#95;{i\le d}\binom{n}{i}$,
$$\big(1 - \tfrac{Cd}{\log n}\big) n \binom{n}{\le d} \le \log_2 T(n,d) \le n \binom{n}{\le d},$$
and for $d = o(\log n)$, $\log_2 T(n,d) = (1-o(1)) n^{d+1}/d! = \Theta(n^{d+1})$. Concretely: **$\log_2 T(n,1) = \Theta(n^2)$** (Zuev; Kahn-Komlos-Szemeredi: $n^2 - n\log_2 n \pm O(n)$) and **$\log_2 T(n,2) = (1-o(1)) n^3/6 = \Theta(n^3)$.**

**Reference.** P. Baldi and R. Vershynin, "Polynomial threshold functions, hyperplane arrangements, and random tensors," *SIAM J. Math. Data Sci.* **1** (2019), 699-729, [arXiv:1803.10868](https://arxiv.org/abs/1803.10868), Thm 1.1, Cor. 1.2.

**How it advances the project.** This furnishes the "richness" side of the counting clash, and **corrects the brief**: the right number for $d=2$ is $2^{\Theta(n^3)}$. All these functions have $\deg&#95;{\pm} \le d$ (constant) yet are super-polynomially numerous, so against the $2^{O(Hn\log n)}$ realizable-by-$H$-heads count, a $1-o(1)$ fraction need $H = \Omega(n/\log n)$ (from linear functions) or $\Omega(n^2/\log n)$ (from degree-2). Fully verified against a primary source.

### 4.5 Cover's function-counting theorem (the linear / d=1 base case)

**Statement [VERIFIED].** *(Cover 1965.)* The number of homogeneously linearly separable dichotomies of $M$ points in general position in $\mathbb{R}^N$ is
$$C(M,N) = 2 \sum&#95;{k=0}^{N-1} \binom{M-1}{k}.$$
For $M > N+1$ this is sub-exponential in $M$ (roughly $M^{N}$); applied with $M = 2^n$ points on the cube and $N = n+1$ it gives the $2^{\Theta(n^2)}$ linear-threshold count of Section 4.4.

**Reference.** T. M. Cover, "Geometrical and statistical properties of systems of linear inequalities with applications in pattern recognition," *IEEE Trans. Electronic Computers* **EC-14** (1965), 326-334, DOI [10.1109/PGEC.1965.264137](https://doi.org/10.1109/PGEC.1965.264137).

**How it advances the project.** The exact, constant-free ancestor of Warren for the linear case and the historical seed of the neuron-counting lower bounds (Topic 6). Cleanest illustration of "$N$ parameters -> $\approx M^N$ functions" and the smallest example where the counting clash bites.

### 4.6 Milnor-Thom and the Basu-Pollack-Roy sign-condition count (sharpest constants)

**Statement [VERIFIED verbatim for Milnor; survey-verified for BPR].** *(Milnor 1964, Thm 2.)* A real algebraic set in $\mathbb{R}^N$ cut out by polynomials of degree $\le d$ has sum of Betti numbers (hence number of connected components $b_0$) at most $d(2d-1)^{N-1} = (O(d))^N$; the basic semialgebraic version (Thm 3) is $\tfrac12 (2+d)(1+d)^{N-1}$. *(Basu-Pollack-Roy.)* For $s$ polynomials of degree $\le d$ in $k$ variables, the number of realizable **sign conditions** is $(O(sd/k))^k$, and the number of connected components of all realizable sign conditions, restricted to a variety of dimension $k'$, is bounded (BPR, *Proc. AMS* 2005 = book Thm 7.50) by $\sum&#95;{1 \le j \le k'-i} \binom{s}{j} 4^{j} d(2d-1)^{k-1}$ for the $i$-th Betti number ($i=0$ is the component count); asymptotically tight at $\tfrac{(2d)^k}{k!} s^k + O(s^{k-1})$.

**Reference.** J. Milnor, "On the Betti numbers of real varieties," *Proc. AMS* **15** (1964), 275-280, [DOI](https://doi.org/10.1090/S0002-9939-1964-0161339-9) (PDF fetched, Thm 2/3 verbatim). S. Basu, R. Pollack, M.-F. Roy, "On the Betti numbers of sign conditions," *Proc. AMS* **133** (2005), 965-974, and *Algorithms in Real Algebraic Geometry*, Springer (2006), Thm 7.50.

**How it advances the project.** Tightest version of the region-counting bound, with explicit dependence on the *number* $s$ of polynomials as well as degree. If the basic Warren bound (Section 4.1) is a hair too weak for the exact separation constant, the BPR sign-condition bound is the refinement to reach for. (The single-variety component count $(O(d))^N$ is a *different* object from the realizable-sign-pattern count $\binom{s}{\le k}(O(d))^k$ — for the separation we want the latter, in $\theta$-space.)

### 4.7 The exact precedent: counting low-sign-rank matrices via Warren

**Statement [VERIFIED verbatim against arXiv:1503.07648].** *(Alon-Moran-Yehudayoff 2016, Lemma 22.)* For $r \le N/2$, the number of $N \times N$ sign matrices of sign-rank $\le r$ is at most $(O(N/r))^{2Nr} \le 2^{O(rN\log N)}$, with a matching $2^{\Omega(rN\log N)}$ lower count. The proof: a rank-$r$ factorization $M = M_1 M_2$ makes each entry a quadratic in $2Nr$ real parameters, then *"we deduce the following from Warren's theorem."* Since there are $2^{\Theta(N^2)}$ sign matrices total, **most have sign-rank $\Omega(N/\log N)$.**

**Reference.** N. Alon, S. Moran, A. Yehudayoff, "Sign rank versus VC dimension," *COLT* 2016, [arXiv:1503.07648](https://arxiv.org/abs/1503.07648), Lemma 22. Original counting idea: N. Alon, P. Frankl, V. Rodl, "Geometrical realization of set systems and probabilistic communication complexity," *FOCS* 1985. Related: Paturi-Simon, "Probabilistic communication complexity," *JCSS* **33** (1986), Thm 5 (almost all $f$ have unbounded-error complexity $\ge n/2 - \tfrac12\log n$, via Milnor's bound).

**How it advances the project.** This is **the published template of Route A, with "sign-rank $r$" exactly where "heads $H$" sits**: $2Nr$ parameters there $\leftrightarrow O(Hn)$ parameters here; "most matrices have high sign-rank" there $\leftrightarrow$ "most degree-2 PTFs need many heads" here. The project should cite AMY Lemma 22 as the methodological precedent and mirror its proof structure (factor -> quadratic-in-parameters -> Warren -> compare to total count). Paturi-Simon Thm 5 is the even older "almost all functions are hard" instance of the same counting principle.

---

## Topic 3 (PRIORITY): Chow variety, products of linear forms, tangential/secant varieties, and rank obstructions

This is Route B: per-function, constructive lower bounds via algebraic geometry. Statements below flagged **[verified via ar5iv]** were read from the HTML mirrors of the cited arXiv papers (the raw PDFs were compression-garbled).

### 3.1 The Chow variety of products of linear forms (dimension and secants)

**Statement [verified].** For $V$ of dimension $n+1$, the **Chow variety** (a.k.a. variety of completely decomposable forms / split variety, $\mathrm{Split}&#95;d(\mathbb{P}^n)$, $\mathrm{Ch}&#95;d(V)$) is
$$\mathrm{Ch}&#95;{d}(V) = \overline{\lbrace [\ell_1 \cdots \ell_d] : \ell_i \in V^{\ast} \rbrace} \subset \mathbb{P} S^{d}V^{\ast},$$
the image-closure of $\mathbb{P}(V^{\ast})^{\times d} \to \mathbb{P}(S^d V^{\ast})$. Verified facts (Arrondo-Bernardi, ar5iv text): $\dim \mathrm{Ch}&#95;{d,n} = dn$ projectively; the **affine cone has dimension $dn+1$**; the embedded (affine) tangent space at a general point has dimension $dn+1$. The $s$-th secant has expected projective dimension (standard Terracini form)
$$\mathrm{expdim} \sigma_s(\mathrm{Ch}&#95;{d,n}) = \min\Big\lbrace  s(dn+1),\ \tbinom{n+d}{d}\Big \rbrace - 1,$$
and $\mathrm{Ch}&#95;{d,n}$ is **nondefective** (secants attain this) in broad ranges: Arrondo-Bernardi Prop. 1.8 for $d>2$ and $3(s-1)\le n$; and **all** secants are nondefective for $d=3$ (cubics, any $n$) and $n=3$ (quaternary forms, any $d$).

**Reference [verified via ar5iv].** E. Arrondo and A. Bernardi, "On the variety parametrizing completely decomposable polynomials," *J. Pure Appl. Algebra* **215** (2011), 201-220, [arXiv:0903.2757](https://arxiv.org/abs/0903.2757) (dim $=dn$, Prop. 1.8). D. Torrance and N. Vannieuwenhoven, "All secant varieties of the Chow variety are nondefective for cubics and quaternary forms," *Trans. AMS* **374** (2021), 4815-4838, [arXiv:2005.12436](https://arxiv.org/abs/2005.12436).

**How it advances the project.** The normal-form polynomial $P$ is a **single tangent vector** (a product plus a first-order Leibniz variation), so the governing object is the **tangential variety** $\tau(\mathrm{Ch}&#95;H)$, not $\sigma_2$ (note $\tau(X)\subseteq\sigma_2(X)$, often strictly). The verified dimension $\dim\widehat{\mathrm{Ch}}&#95;{H,n}=Hn+1$, hence $\dim\widehat\tau(\mathrm{Ch}&#95;H)\le 2Hn+1$, is *small* inside the ambient $\binom{n+H}{H}$, which (i) is the geometric shadow of the same parameter count driving Route A, and (ii) already gives the crudest always-valid obstruction: a generic $P\in S^d$ cannot be such a tangent vector unless $2Hn+1 \gtrsim \binom{n+H}{H}$, forcing $H$ large.

### 3.2 Brill's equations (set-theoretic membership test for "is a product of linear forms")

**Statement [verified via ar5iv].** *(Brill, Gordan; modern Guan.)* Brill's map $\mathfrak{B}: S^d V \to S&#95;{(d,d)}V \otimes S^{d^2-d}V$, $\mathfrak{B}(f)=(\pi&#95;{d,d}\otimes\mathrm{Id})[f\otimes Q_d(f)]$ (with $Q_d$ from Newton/Girard power-sum formulas), gives equations of **degree $d+1$** in the coefficients of $f$ with
$$\mathfrak{B}(f)=0 \iff [f]\in\mathrm{Ch}&#95;d(V),$$
i.e. they test set-theoretically "is $f$ a product of $d$ linear forms?". As a $GL(V)$-module the span is $S&#95;{(7,3,2)}V^{\ast}$ for $d=3$, and $\bigoplus&#95;{j=2}^{d}S&#95;{(d^2-j, d, j)}V^{\ast}$ for $d\ne 3$ ($\dim V\ge 3$, $d\ge 2$).

**Reference [verified via ar5iv].** Y. Guan, "Brill's equations as a $GL(V)$-module," *Linear Algebra Appl.* (2018), [arXiv:1508.02293](https://arxiv.org/abs/1508.02293) (Thm 2.12, Thm 1.1); also Landsberg, *Tensors: Geometry and Applications*, AMS GSM 128 (2012), and GKZ Ch. 4. Secant-of-Chow module equations (by prolongation): Y. Guan, [arXiv:1602.04275](https://arxiv.org/abs/1602.04275).

**How it advances the project.** Brill's equations are the prototype exact certificate that "$f$ is NOT a product of $H$ linear forms" (membership in $\mathrm{Ch}&#95;H$). They test products, not the *tangent-to-products* object we need, so the required step is their **secant/tangential prolongation**; Guan supplies module-level secant equations by prolongation but, candidly, notes these are existence results with **no numerical flattening-style rank test**. Still, a tangential analogue (a form vanishing on $\tau(\mathrm{Ch}&#95;H)$ but not on $P$) would directly certify $H^{\ast}(f)>H$, and positivity only shrinks the variety, so any unconstrained equation remains valid.

### 3.3 Tangential variety of the Chow / Segre-Veronese (the exact home of P)

**Statement [verified via ar5iv].** $\tau(X)=\overline{\bigcup&#95;{x\in X}\mathbb{T}&#95;x X}$, with $\dim\tau(X)\le 2\dim X$ (generic equality). Oeding-Raicu give the defining ideals of $\tau$ of Segre-Veronese varieties: **Theorem B** says $I(\tau(X))$ is **generated in degree $\le 4$**, generically in **degree 3** (degree-4 generators only in small cases $\lbrace 3 \rbrace,\lbrace 2,1 \rbrace,\lbrace 1,1,1 \rbrace$; quadrics only for rational normal curves of degree $\ge 5$), proving the Landsberg-Weyman conjecture in the Segre case; **Theorem A** gives the full multiplicity-free $GL$-decomposition of the coordinate ring. The **Veronese case ($n=1$, symmetric forms, the project's setting)** is covered explicitly: minimal generators of $\tau(v_d(\mathbb{P}V))$ in degrees 1-3, weights of shape $(2d-k,k)$.

**Reference [verified via ar5iv].** L. Oeding and C. Raicu, "Tangential varieties of Segre-Veronese varieties," *Collect. Math.* (2014), [arXiv:1111.6202](https://arxiv.org/abs/1111.6202) (Thms A, B).

**How it advances the project.** $P=\theta\prod_h D_h+\sum_h N_h\prod&#95;{g\ne h}D_g$ is *literally* a point of the affine cone over $\tau(\mathrm{Ch}&#95;H)$: the sum is the first-order Leibniz variation of $\prod_h D_h$ and $\theta\prod_h D_h$ is the base scaling. So $H^{\ast}(f)$ (up to the positivity refinement) is the least $H$ with $P\in\widehat\tau(\mathrm{Ch}&#95;H)$. **Two honest caveats:** (1) Oeding-Raicu give equations for $\tau$ of the *Veronese/Segre-Veronese*, which directly handle only the **$H=1$ stratum** ("tangent to a single Veronese point"); the Chow variety is a different ($\mathfrak{S}&#95;d$-symmetrized) image, so these are not drop-in equations for $\tau(\mathrm{Ch}&#95;H)$, $H\ge 2$. (2) A published defining ideal or rank test for $\tau(\mathrm{Ch}&#95;H)$ with $H\ge 2$ was **not located** — building one (e.g. by prolongation, or by the machinery below) is the genuine open research step.

### 3.4 Flattening / catalecticant / Young-Koszul flattening rank obstructions

**Statement [verified via ar5iv].** *(Sylvester catalecticants; Landsberg-Ottaviani Young/Koszul flattenings.)* For $\phi\in S^d V$ and the catalecticant $\phi&#95;{a,d-a}:S^a V^{\ast}\to S^{d-a}V$, membership $\phi\in\sigma_r(v_d(\mathbb{P}V))$ implies $\mathrm{rank} \phi&#95;{a,d-a}\le r$, hence **border Waring rank** $\underline{R}(\phi)\ge\mathrm{rank} \phi&#95;{a,d-a}$ (size-$(r{+}1)$ minors are the equations). The **Young flattening** $YF&#95;{d,n}(\phi):S^\delta V^{\ast}\otimes\Lambda^a V\to S^\delta V\otimes\Lambda^{a+1}V$ (odd $d=2\delta+1$, $a=\lfloor n/2\rfloor$) gives $\underline{R}(\phi)\ge\mathrm{rank} YF&#95;{d,n}(\phi)/\binom{n}{a}$. **Koszul flattenings** yield $\underline{R}(M_n)\ge 2n^2-n$ for matrix multiplication.

**Reference [verified via ar5iv].** J. M. Landsberg and G. Ottaviani, "Equations for secant varieties of Veronese and other varieties," *Ann. Mat. Pura Appl.* (2013), [arXiv:1111.4567](https://arxiv.org/abs/1111.4567) (Prop. 2.2 catalecticant; Thm 1.2.3 Young flattening); and "New lower bounds for the border rank of matrix multiplication," *Theory of Computing* **11** (2015), 285-298, [arXiv:1112.6007](https://arxiv.org/abs/1112.6007) (improved to $2n^2-\log_2 n-1$ by Landsberg-Michalek, [arXiv:1608.07486](https://arxiv.org/abs/1608.07486)).

**How it advances the project.** This is the *mechanism* Route B most wants to import: a computable matrix whose rank certifies a decomposition lower bound. **Honest status [verified negative]:** there is **no published flattening/catalecticant theorem lower-bounding Chow rank or tangential-Chow rank** in the clean "rank of an explicit linear map $\ge$ number of factors" form (Guan's secant-of-Chow equations come only via prolongation, and he says so). Constructing a "Chow/tangential-Chow flattening" — most plausibly by adapting Oeding's monomial Young flattenings (below) or by restricting the Veronese catalecticant to the tangent star — is the key open construction that would give a polynomial-time-checkable per-function lower bound on $H^{\ast}(f)$.

### 3.5 A worked flattening rank bound for a product of linear forms (the template instance)

**Statement [verified].** *(Carlini-Catalisano-Geramita; Oeding; Ranestad-Schreyer apolarity.)* The monomial $x_1 x_2\cdots x_n$ (a product of $n$ distinct linear forms) has Waring rank exactly $2^{n-1}$; generally $R(x_0^{a_0}\cdots x_n^{a_n})=\prod&#95;{i\ge 1}(a_i+1)$ for $a_0\le\cdots\le a_n$. The matching lower bounds use apolarity / the length of the apolar algebra, and **Oeding's "Border ranks of monomials" certifies the border-rank lower bound for powers of $x_1\cdots x_n$ via Young flattenings** — the cleanest existing case of a flattening lower-bounding the rank of a product of linear forms.

**Reference [verified].** E. Carlini, M. V. Catalisano, A. V. Geramita, "The solution to Waring's problem for monomials," *J. Algebra* **370** (2012), [arXiv:1110.0745](https://arxiv.org/abs/1110.0745); L. Oeding, "Border ranks of monomials," [arXiv:1608.02530](https://arxiv.org/abs/1608.02530); K. Ranestad and F.-O. Schreyer, "On the rank of a symmetric form," *J. Algebra* (2011). For the apolar algebra of a product of linear forms (hyperplane-arrangement/star-configuration geometry): M. DiPasquale, Z. Flores, C. Peterson, [arXiv:2002.04818](https://arxiv.org/abs/2002.04818).

**How it advances the project.** This is the existence proof that *a flattening can lower-bound the rank of a product of linear forms*, and thus the concrete template to push toward the $\tau(\mathrm{Ch}&#95;H)$ obstruction. It also exhibits a large "rank gap between decomposition models" ($\prod x_i$ has Chow length $n$ but Waring rank $2^{n-1}$), the phenomenon that, mirrored for Chow vs. tangential-Chow, would separate $H^{\ast}$ from $\deg&#95;{\pm}$; and $\prod x_i$ is itself a natural parity-flavored hard instance on the cube. DiPasquale-Flores-Peterson give the by-hand apolarity machinery to compute these obstructions on small examples.

### 3.6 Coincident-root loci (the n=1 factorization-type stratification sandbox)

**Statement [verified].** *(Chipalkatti.)* For a partition $\lambda\vdash d$, the **coincident-root locus** $X_\lambda\subseteq\mathbb{P}(S^d\mathbb{C}^2)$ of binary forms factoring with root multiplicities $\lambda$ has explicit $SL_2$-equivariant defining equations, realized as a cohomology group of an explicit complex of $SL_2$-representations. This is exactly the "products of $k$ vs $k+1$ linear forms" stratification in two variables.

**Reference [verified].** J. Chipalkatti, "On equations defining coincident root loci," *J. Algebra* (2003), [arXiv:math/0110224](https://arxiv.org/abs/math/0110224).

**How it advances the project.** For $n=1$ (the smallest nontrivial cube of variables) this gives a *fully worked, computable* equation system distinguishing factorization type, i.e. the binary analogue of the $H$-stratification. It is the natural first sandbox to test whether a tangential refinement of these equations can certify $H^{\ast}(f)>H$ on explicit small functions before attacking general $n$.

---

## Topic 1: Threshold degree (PTFs), exact values, and lower-bound methods

These tell us what $\deg&#95;{\pm}(f)$ *is* (the lower endpoint of the sandwich) so we can pick candidate separators and know the floor.

### 1.1 Minsky-Papert: parity and the Ω(n^1/3) DNF

**Statement [verified].** *(Minsky-Papert 1969.)* $\deg&#95;{\pm}(\mathrm{XOR}&#95;n) = n$. There is an explicit polynomial-size constant-depth DNF (the "Minsky-Papert" function, a CNF/DNF of ANDs of fan-in $\approx n^{1/3}$ over ORs) with threshold degree $\Theta(n^{1/3})$.

**Reference.** M. Minsky and S. Papert, *Perceptrons*, MIT Press, 1969 (expanded 1988).

**How it advances the project.** Parity's $\deg&#95;{\pm} = n = H^{\ast}(\mathrm{XOR}&#95;n)$ shows the sandwich is *tight* for parity, so parity cannot be a separator. The Minsky-Papert $n^{1/3}$ function is a natural candidate to test whether $H^{\ast}$ can exceed $\deg&#95;{\pm}$: it is single-polarity-ish DNF, where the project already has an $H^{\ast} \le s$ (terms) upper bound, so comparing $\deg&#95;{\pm} = n^{1/3}$ against the head bound there is a concrete experiment.

### 1.2 The method of dual polynomials (LP duality for threshold degree)

**Statement [verified].** A function $f: \lbrace -1,1 \rbrace^n \to \lbrace -1,1 \rbrace$ has $\deg&#95;{\pm}(f) > d$ iff there exists a "dual witness" $\psi: \lbrace -1,1 \rbrace^n \to \mathbb{R}$, $\psi \not\equiv 0$, with (i) $\psi$ orthogonal to all monomials of degree $\le d$ ($\sum_x \psi(x)\chi_S(x) = 0$ for $|S|\le d$), and (ii) $\psi$ agrees in sign with $f$ everywhere ($\psi(x) f(x) \ge 0$). This LP-duality characterization, and its "one-sided / smooth" refinements, underlie the pattern-matrix method.

**Reference.** A. Sherstov, "The pattern matrix method," *SIAM J. Comput.* (2011); M. Bun and J. Thaler, "Approximate degree in classical and quantum computing," *Foundations and Trends in TCS* / survey (2022), arXiv version (their survey is the canonical modern reference). R. Špalek; Razborov-Sherstov for the smooth-witness version.

**How it advances the project.** Dual witnesses are the standard certificate of a threshold-degree *lower* bound, and the project's $\deg&#95;{\pm} \le H^{\ast}$ inequality means any dual-polynomial lower bound on $\deg&#95;{\pm}(f)$ is automatically a lower bound on $H^{\ast}(f)$. More speculatively, the *positivity/one-sided-slope* constraint in the normal form might admit a strengthened dual object (a witness that must additionally be orthogonal to the cone of monotone-denominator atoms), which would be the dual-side route to $H^{\ast} > \deg&#95;{\pm}$.

### 1.3 Hardness amplification / block composition (Sherstov; Bun-Thaler)

**Statement [verified].** *(Sherstov; Bun-Thaler.)* Threshold degree (and approximate degree) can be *amplified* by block composition with a gadget: e.g. $\deg&#95;{\pm}(\text{ONTO} \circ g)$ and the AC0 constructions give functions with $\deg&#95;{\pm} = \Omega(n^{1-\delta})$ and sign-rank $\exp(\Omega(n^{1-\delta}))$. Razborov-Sherstov gave the first AC0 circuit with sign-rank $\exp(\Omega(n^{1/3}))$.

**Reference.** A. Sherstov, "Breaking the Minsky-Papert barrier for constant-depth circuits," *SIAM J. Comput.* (2018); M. Bun and J. Thaler, "A nearly optimal lower bound on the approximate degree of AC0," (arXiv:1703.05784); "Near-optimal lower bounds on the threshold degree and sign-rank of AC0" (arXiv:1901.00988).

**How it advances the project.** These give a *library of functions with known large $\deg&#95;{\pm}$*, which by the sandwich are also lower bounds for $H^{\ast}$. They also model the "composition boosts complexity" phenomenon; if an analogous composition theorem held for $H^{\ast}$ (does composing $f$ with a gadget multiply the required heads?), it would be a powerful $H^{\ast}$ lower-bound technique. Worth probing whether the normal form composes.

---

## Topic 2: Sign-rank and rational (sign) degree

Sign-rank is a *second* invariant sandwiched with $H^{\ast}$ via $\mathrm{tChow}&#95;{\pm}$, and rational degree is the project's native measure (heads produce sums of ratios of affine forms).

### 2.1 Sign-rank and Forster's spectral lower bound

**Statement [verified].** The **sign-rank** of a sign matrix $M \in \lbrace -1,+1 \rbrace^{m\times n}$ is the least rank of a real matrix $R$ with $\mathrm{sign}(R&#95;{ij}) = M&#95;{ij}$. *(Forster 2002.)* $\mathrm{signrank}(M) \ge \dfrac{\sqrt{mn}}{\lVert M\rVert_2}$, where $\lVert M\rVert_2$ is the spectral norm. For a random/quasirandom $\pm 1$ matrix $\lVert M\rVert_2 \approx \sqrt{m}+\sqrt{n}$, giving sign-rank $\gtrsim \sqrt{n}$ (and $\exp$lower bounds via amplification).

**Reference.** J. Forster, "A linear lower bound on the unbounded error probabilistic communication complexity," *J. Comput. Syst. Sci.* **65** (2002), 612-625.

**How it advances the project.** Sign-rank lower-bounds threshold degree-style quantities and is itself controlled by *dimension* (a sign-rank-$r$ representation is points-and-halfspaces in $\mathbb{R}^r$). If one can show $\mathrm{tChow}&#95;{\pm}(f)$ (the sandwich middle) is at least the sign-rank, then any Forster bound becomes an $H^{\ast}$ lower bound. Conversely, Forster-style spectral arguments are a candidate *technique* for lower-bounding the tangential-Chow sign rank directly.

### 2.2 Sign-rank vs. threshold degree (they can be far apart)

**Statement [verified].** $\mathrm{signrank}(f) \le n^{O(\deg&#95;{\pm}(f))}$ (low threshold degree implies low sign-rank), but the converse fails badly: there are functions with $\deg&#95;{\pm} = \Theta(n)$ yet sign-rank $O(1)$ or small, and AC0 has *both* large, $\deg&#95;{\pm}=\Omega(n^{1-\delta})$ and $\mathrm{signrank}=\exp(\Omega(n^{1-\delta}))$.

**Reference.** A. Razborov and A. Sherstov, "The sign-rank of AC0," *SIAM J. Comput.* **39** (2010); see also Bun-Thaler (arXiv:1901.00988).

**How it advances the project.** This is a *direct precedent for separating two complexity measures that both lower-bound a third*, exactly the methodological shape of separating $H^{\ast}$ from $\deg&#95;{\pm}$. The constructions (AC0 with one measure large, another small) are templates; and the inequality $\mathrm{signrank} \le n^{\deg&#95;{\pm}}$ suggests $H^{\ast}$ might sit "above" sign-rank in a similar layered picture.

### 2.3 Rational sign degree / rational approximation degree

**Statement [verified].** The **rational sign degree** (least degree of a ratio $p/q$ that sign-represents $f$) and rational $\varepsilon$-approximation degree are studied for halfspaces/majority: the canonical halfspace has rational $\varepsilon$-approximation degree $\Theta(1 + n/\log\frac{1}{1-\varepsilon})$, and majority is $\varepsilon$-approximable by a rational function of degree $O(\log n \log\frac1\varepsilon)$ (Newman-type). Exact rational degree is studied in Iyer et al. (already in the repo's survey).

**Reference.** A. Sherstov, "The hardest halfspace," *Comput. Complexity* (2021); S. Iyer et al., "On the rational degree of Boolean functions and applications," (arXiv:2310.08004).

**How it advances the project.** This is the *most native* external invariant: each head contributes a ratio of affine forms, so $H$ heads give a sum of $H$ low-degree rational functions, a "rational sign representation with $H$ terms of degree 1 numerators/denominators." Rational-degree lower bounds, especially ones sensitive to the *number of rational terms* and to the *positivity of denominators*, are the closest off-the-shelf lower bounds to $H^{\ast}$ itself, and are worth examining for a term-count (= head-count) sensitive version.

---

## Topic 5: Expressivity of attention as Boolean/threshold circuits

This sets the *ceiling* and clarifies what a single head computes (a linear-fractional / LTF-like unit).

### 5.1 Transformers are in (uniform) TC0

**Statement [verified].** Saturated/hard-attention transformers (fixed depth) are simulable by constant-depth threshold circuits, so they recognize only languages in (non-uniform, and under conditions log-uniform/DLOGTIME-uniform) **TC0**. Log-precision softmax transformers admit a majority-quantifier logic characterization (FOM / TC0).

**Reference.** W. Merrill, A. Sabharwal, A. Noah Smith, "Saturated transformers are constant-depth threshold circuits," *TACL* (2022); W. Merrill and A. Sabharwal, "The parallelism tradeoff: limitations of log-precision transformers" / "A logic for expressing log-precision transformers" (2023).

**How it advances the project.** TC0 is the right complexity ceiling: a single attention head is essentially a *normalized weighted threshold/averaging unit*, and head complexity should be read as a TC0-internal resource (number of threshold-like gates of a specific linear-fractional form). It justifies comparing $H^{\ast}$ to threshold-circuit size measures and to the number of LTFs/heads needed, rather than to general circuits.

### 5.2 One-layer attention limits and a single head as a unit

**Statement [verified].** One-layer single-head hardmax self-attention cannot form a "contextual mapping" (limited memorization); one layer one head cannot compute parity (Kozachinskiy-Steifer-Wałȩga 2026, already in repo survey). A single softmax head computes a *convex combination* of value vectors weighted by exponential scores, i.e. after linear readout a **ratio of two affine-exponential sums** in the inputs, which on the Boolean cube is a linear-fractional form, exactly the atom $N_h/D_h$ of the normal form.

**Reference.** T. Kajitsuka and I. Sato, "Are transformers with one-layer self-attention ... universal approximators?" (arXiv:2307.14023); A. Kozachinskiy, T. Steifer, V. Wałȩga, "Parity, sensitivity, and transformers" (arXiv:2602.05896).

**How it advances the project.** These confirm the project's atom model (one head = one linear-fractional unit with positive monotone denominator) is faithful to real softmax attention, so any lower bound proved in the normal-form model is a genuine statement about heads. The parity impossibility for $(1,1)$ is the smallest nontrivial $H^{\ast}$ lower bound and a sanity check.

---

## Topic 6: Monotone/unate threshold complexity and neuron-counting for one-hidden-layer threshold networks

A head is morphologically a threshold/LTF-like unit, so the classical "how many hidden threshold units do you need" theory is the closest structural precedent, and it is where the counting route (Topic 4) was first used to prove lower bounds.

### 6.1 Baum's neuron-counting lower bound (Cover-based)

**Statement [verified].** *(Baum 1988.)* A one-hidden-layer threshold network with $k$ hidden units (and a threshold output) realizes at most $\approx (\text{number of LTF dichotomies})^{k}$ labelings; by Cover's theorem this forces $\Omega(n/\log n)$ connections / $\Omega(\lceil M/n\rceil)$ hidden units to memorize $M$ points in general position. The lower bound is a direct function-counting argument.

**Reference.** E. Baum, "On the capabilities of multilayer perceptrons," *J. Complexity* **4** (1988), 193-215.

**How it advances the project.** This is **the exact methodological template for Route A in a sister model.** Baum proves a *neuron* lower bound by the same parameter/function counting that we want for *heads*: one head $\leftrightarrow$ one hidden LTF unit, $H$ heads $\leftrightarrow$ $H$ hidden units, each with $O(n)$ weights. Transcribing Baum/Cover gives an $H = \Omega(n/\log n)$ lower bound for realizing $2^{\Theta(n^2)}$-sized function families, the separation. The only adaptation needed is that heads are *linear-fractional* (ratio) units rather than plain LTFs, which Warren's polynomial generality (Section 4.1) already covers.

### 6.2 VC dimension of polynomially-parameterized networks (Karpinski-Macintyre; Bartlett et al.)

**Statement [verified].** Networks with piecewise-polynomial activations and $W$ parameters over $L$ layers have VC dimension $O(W L \log W)$ (nearly tight $\Omega(WL\log(W/L))$); for sigmoidal/Pfaffian units the Karpinski-Macintyre bound is $O(W^2)$-ish, all via Warren/Khovanskii-style sign-pattern counting.

**Reference.** M. Karpinski and A. Macintyre, "Polynomial bounds for VC dimension of sigmoidal and general Pfaffian neural networks," *JCSS* (1997); P. Bartlett, N. Harvey, C. Liaw, A. Mehrabian, "Nearly-tight VC-dimension and pseudodimension bounds for piecewise linear neural networks," *JMLR* (2019), arXiv:1703.02930.

**How it advances the project.** These are the modern, refined versions of the counting lemma (Section 4.3) handling *nonlinear* (sigmoidal/rational) units, which matters because a softmax head is a rational/transcendental unit. Karpinski-Macintyre's Pfaffian counting in particular covers exponential/softmax score functions, so it is the right tool if one wants the counting separation to account for the *exact* softmax nonlinearity rather than its cleared-denominator polynomial surrogate.

### 6.3 Monotone / unate threshold complexity and PTF weight/density

**Statement [recalled].** For unate/monotone functions, threshold and polynomial-threshold representations interact with weight and density: $s$-term single-polarity DNFs have PTF degree $O(\sqrt{n}\log s)$-type bounds and bounded "density"; the project's own single-polarity $H^{\ast} \le s$ upper bound is the head-analogue. Monotone functions have sign-rank/threshold-degree structure (e.g. monotone functions can still have large threshold degree).

**Reference.** R. O'Donnell and R. Servedio, "New degree bounds for polynomial threshold functions," *Combinatorica* (2010) and Klivans-Servedio (in repo survey).

**How it advances the project.** The project's upper bounds already exploit single-polarity/unate structure; the matching question is whether unate functions are *easier* to lower-bound for $H^{\ast}$. Since the normal form's denominators are *one-sided/monotone* by construction, unate-threshold theory is the natural place to look for a structural (non-counting) lower bound that uses the positivity constraint, the very constraint that distinguishes $H^{\ast}$ from the unconstrained tangential-Chow sign rank.

---

## Synthesis: the three or four most actionable leads

1. **Warren counting (verified, constant $4e$) + Goldberg-Jerrum/Anthony-Bartlett/BHLM, against Baldi-Vershynin's function counts, with Alon-Moran-Yehudayoff as the exact precedent (Sections 4.1-4.7).** The most promising path to $H^{\ast} > \deg&#95;{\pm}$: $H$ heads realize only $2^{O(Hn\log n)}$ functions, but there are $2^{\Theta(n^2)}$ linear and $2^{\Theta(n^3)}$ degree-2 threshold functions (threshold degree $\le 2$), forcing $H = \Omega(n/\log n)$ (resp. $\Omega(n^2/\log n)$) for almost all of them. **AMY Lemma 22 is this exact argument for sign-rank** (mirror its factor -> quadratic-in-parameters -> Warren -> compare-to-total structure). Non-constructive but unconditional; needs only a careful per-head parameter count $N$ and per-cube-point degree $D$.

2. **Baum/Cover neuron-counting transcribed to heads (Sections 6.1, 4.5).** The same separation in a refereed sister model (one-hidden-layer threshold nets), giving a ready-made proof skeleton and the $\Omega(n/\log n)$ target; adapt LTF units to linear-fractional heads via Warren's polynomial generality.

3. **Tangential-variety identification + a Chow-rank flattening obstruction (Sections 3.1-3.6).** The normal-form polynomial is verifiably a tangent vector to $\mathrm{Ch}&#95;H$ (a point of $\widehat\tau(\mathrm{Ch}&#95;H)$); Brill's equations (verified, deg $H{+}1$), Young/catalecticant flattenings (verified for Waring rank), and Oeding's flattening bound for products $x_1\cdots x_n$ (verified) are the templates for a *per-function, computable* certificate that $P$ needs $> H$ linear factors. **Verified gap:** no flattening/equation for Chow-rank or $\tau(\mathrm{Ch}&#95;H)$, $H\ge 2$, exists in the literature (only $\tau$ of Veronese/Segre-Veronese and secants-of-Chow-by-prolongation). Building a "Chow/tangential-Chow flattening" is the genuine open construction; the binary ($n=1$) coincident-root loci (Section 3.6) are the ready sandbox.

4. **Dual-polynomial method with a positivity-augmented witness (Section 1.2) and the rational-term-count invariant (Section 2.3).** Each head is a positive-denominator rational atom; a dual witness additionally orthogonal to the monotone-denominator cone, or a rational-sign-degree bound sensitive to the *number of terms*, is the most native lower-bound object and the most likely to "see" the positivity constraint that separates $H^{\ast}$ from tangential-Chow sign rank.

**File path:** `/Users/karthikviswanathan/Desktop/fair_stuff.nosync/how-many-attention-heads-xor/claude-comments/lit_survey_round1.md`
