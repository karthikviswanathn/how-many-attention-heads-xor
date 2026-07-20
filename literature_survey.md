# Literature Survey

## Results Most Relevant For Upper Bounds

The papers below are the ones most likely to help with the upper-bound side of the project.

### 1. Weiss, Goldberg, and Yahav 2021. Thinking Like Transformers

Source: [PMLR](https://proceedings.mlr.press/v139/weiss21a.html)

Weiss, Goldberg, and Yahav introduce RASP as a programming language for transformer encoders. Their examples include histograms, sorting, and Dyck languages, and the RASP viewpoint makes constructions look like explicit sequence statistics followed by simple post-processing.

**Why it matters here.** This is the cleanest conceptual guide for upper bounds in this repo. It suggests that the right approach is not black-box universality, but rather:

- identify a low-cardinality statistic of the input,
- make attention compute that statistic or a basis of functions of that statistic,
- finish by interpolation in the readout.

That is exactly the shape of the weighted-sum interpolation proof in [theorems/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md](theorems/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md).

### 2. Yang and Chiang 2024. Counting Like Transformers: Compiling Temporal Counting Logic Into Softmax Transformers

Source: [arXiv](https://arxiv.org/abs/2404.04393)

Yang and Chiang show that temporal counting logic formulas can be compiled into future-masked soft attention transformers.

**Why it matters here.** This is the strongest nearby evidence that softmax attention is naturally suited to count-like constructions. It supports trying to upper-bound $H^{\ast}(f)$ by the complexity of a small collection of counting statistics rather than by generic universality arguments.

### 3. Kajitsuka and Sato 2024. Are Transformers with One Layer Self-Attention Using Low-Rank Weight Matrices Universal Approximators?

Source: [OpenReview](https://openreview.net/forum?id=nJnky5K944)

Kajitsuka and Sato show that one-layer, single-head self-attention with low-rank weight matrices can memorize finite samples, and that adding two feedforward networks yields universal approximation for continuous permutation-equivariant functions on compact domains.

**Why it matters here.** This is one of the closest positive expressivity results for shallow attention. It says one-layer attention can already do a lot of contextual identification. The limitation for us is that the theorem uses a more permissive architecture than [model.md](model.md), especially because the feedforward layers and the continuous approximation setting do real work.

### 4. Likhosherstov, Choromanski, and Weller 2021. On the Expressive Power of Self-Attention Matrices

Source: [arXiv](https://arxiv.org/abs/2106.03764)

Likhosherstov, Choromanski, and Weller show that fixed self-attention parameters can approximate broad families of sparse attention matrices by varying the inputs, with hidden size only logarithmic in the sequence length.

**Why it matters here.** This paper isolates what the attention matrix itself can encode before the readout is applied. For upper bounds, it suggests looking for constructions where the attention matrix is doing structured routing or sparse selection, while the final linear probe only decodes a low-dimensional summary.

### 5. Paturi 1992. On the Degree of Polynomials that Approximate Symmetric Boolean Functions

Source: [PDF](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/Paturi_1992_stoc.pdf)

Paturi gives matching upper and lower bounds for the approximate degree of symmetric Boolean functions, using symmetrization to reduce the problem to one variable.

**Why it matters here.** This is the classical guide for any symmetric-family upper bound. The repo already reduces symmetric functions to Hamming weight exactly. Paturi says that once a function depends only on $|x|$, the right next move is usually to work with a one-variable surrogate. Our new weighted-sum upper bound is an exact, attention-level analogue of that strategy.

### 6. Nisan and Szegedy 1994. On the Degree of Boolean Functions as Real Polynomials

Source: [Computational Complexity summary](https://cris.huji.ac.il/en/publications/on-the-degree-of-boolean-functions-as-real-polynomials-14)

Nisan and Szegedy show that exact degree, approximate degree, and decision-tree complexity are polynomially related up to known losses.

**Why it matters here.** This gives a map of the classical landscape. If head complexity eventually turns out to be controlled by degree-like quantities, then decision trees and related combinatorial measures automatically become relevant comparison points.

### 7. Klivans and Servedio 2004. Learning DNF in Time 2^Õ(n^(1/3))

Source: [journal page](https://www.sciencedirect.com/science/article/pii/S0022000003001363), [author page](https://www.cs.columbia.edu/~rocco/papers/stoc01.html)

Klivans and Servedio show that every $s$-term DNF has a polynomial threshold representation of degree

$$O(n^{1/3} \log s).$$

**Why it matters here.** This is exactly the kind of structural upper bound one would like to import into head complexity. Right now we only know

$$\deg_{\pm}(f) \leq H^{\ast}(f),$$

not the reverse implication. But if some partial converse is ever proved for the attention model, this paper would immediately turn sparse DNF formulas into strong head upper bounds.

### 8. Sherstov 2018. Algorithmic Polynomials

Source: [ECCC](https://eccc.weizmann.ac.il/report/2018/010/)

Sherstov gives explicit constructive approximate polynomials for several Boolean families, including $k$-DNF and $k$-CNF, with degree

$$O\left(n^{1-\frac{1}{k+1}}\right).$$

**Why it matters here.** The main attraction is constructive form. If we want upper bounds rather than just existential comparisons, explicit approximants are much more usable than generic existence theorems. The limitation is that the paper is about approximation, whereas our model computes Boolean functions exactly.

### 9. Iyer et al. 2023. On the Rational Degree of Boolean Functions and Applications

Source: [arXiv](https://arxiv.org/abs/2310.08004)

Iyer, Jain, Kothari, Kovacs-Deak, Kumar, Schaeffer, Wang, and Whitmeyer study exact rational degree. They show, among other things, that symmetric and unate families have substantial rational degree, and they derive bounds for read-once formulas.

**Why it matters here.** Our model naturally produces sums of positive-denominator affine ratios, but ordinary rational sign degree is not the right invariant. For a positive denominator, the sign is the sign of the numerator. After clearing several denominators, the model-specific content is the shared-factor tangent structure, not rationality alone. Exact rational-degree results remain useful as a source of composition ideas and contrasts, but they do not directly bound $H^{\ast}(f)$.

### Immediate Lessons For This Repo

The literature currently points to four plausible upper-bound routes.

1. **Low-cardinality statistic route.** Make the network depend only on a statistic with small image, then interpolate. This is the route currently realized in [theorems/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md](theorems/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md).
2. **Rational-function route.** Because each head contributes a ratio of affine functions after scalar readout, rational degree looks like a more natural target invariant than polynomial degree.
3. **PTF import route.** Structural upper bounds for polynomial threshold functions of DNF, CNF, and formula classes are potentially relevant, but only if we can show a converse from low-degree sign representations to few-head constructions on some class.
4. **Exactification route.** Approximate-degree results are inspirational, especially for symmetric and formula families, but they do not by themselves answer exact computation in the model from [model.md](model.md).

## Scope

This note records papers that are closest to the project question:

$$f : \lbrace 0,1\rbrace^n \to \lbrace 0,1\rbrace$$

computed exactly by a one-layer attention-only model with a linear readout from a designated query token.

Most transformer expressivity papers study a different regime. Typical differences are:

- unbounded input length rather than a fixed Boolean cube,
- multiple layers rather than one layer,
- feedforward blocks, hard attention, or finite-precision assumptions,
- approximation or language recognition rather than exact Boolean computation,
- depth or precision as the main resource rather than the number of heads.

So the literature is useful mainly for orientation, candidate invariants, and construction ideas, not as a direct answer to the quantity $H^{\ast}(f)$ from [problem_statement.md](problem_statement.md) and [model.md](model.md).

## Broad Expressivity And Universality

### Yun et al. 2020. Are Transformers universal approximators of sequence-to-sequence functions?

Source: [OpenReview](https://openreview.net/forum?id=ByxRM0Ntvr)

Yun, Bhojanapalli, Rawat, Reddi, and Kumar prove that transformer networks are universal approximators of continuous sequence-to-sequence functions on compact domains. Their proof highlights distinct roles for self-attention and feedforward layers, and shows that positional encodings remove permutation-equivariance restrictions.

**Relevance.** This is the standard positive result showing that transformers are expressive in principle. It does not address our exact setting, because the proof uses a richer architecture than one-layer attention-only and studies approximation of continuous maps rather than exact Boolean computation.

### Pérez et al. 2021. Attention is Turing-Complete

Source: [JMLR](https://www.jmlr.org/papers/v22/20-302.html)

Pérez, Barceló, and Marinkovic show that transformers with hard attention are Turing complete under arbitrary precision. The point is to understand algorithmic expressivity of the full architecture, not exact head count in shallow softmax attention.

**Relevance.** This is a useful contrast result. It shows that very strong expressivity is possible once one allows a more permissive setting. It does not give an upper bound that survives our stripped-down model.

## Formal-Language Limits And Logical Characterizations

### Hahn 2020. Theoretical Limitations of Self-Attention in Neural Sequence Models

Source: [ACL Anthology](https://aclanthology.org/2020.tacl-1.11/)

Hahn proves strong limitations for fixed-depth self-attention on formal languages. In particular, periodic finite-state languages and hierarchical structure are out of reach unless the number of heads or layers grows with input length.

**Relevance.** This is strong evidence that parity-like behavior is genuinely constrained in shallow attention. But the paper studies asymptotic language recognition with input length growing, not exact computation on a fixed cube $\lbrace 0,1\rbrace^n$.

### Bhattamishra et al. 2020. On the Computational Power of Transformers and Its Implications in Sequence Modeling

Source: [ACL Anthology](https://aclanthology.org/2020.conll-1.37/)

Bhattamishra, Patel, and Goyal analyze Turing-completeness of transformers and identify which architectural components matter. One message is that residual structure is crucial in their completeness proofs.

**Relevance.** This helps separate what comes from self-attention alone from what comes from the rest of the transformer block. It does not produce a head-count formula for our one-layer attention-only model.

### Chiang et al. 2023. Tighter Bounds on the Expressivity of Transformer Encoders

Source: [OpenReview](https://openreview.net/forum?id=XKcogevHj8)

Chiang, Cholak, and Pillay connect transformer encoders to a logic with counting quantifiers, tightening prior upper and lower bounds for fixed-precision encoders.

**Relevance.** This is conceptually close to the repo's fourth core question, because it connects transformer computation to better-understood logical and circuit-style formalisms. The limitation is again that the setting is fixed-precision encoders over unbounded lengths, not exact head complexity on a fixed Boolean cube.

### Merrill and Sabharwal 2023. A Logic for Expressing Log-Precision Transformers

Source: [OpenReview](https://openreview.net/forum?id=uR8TtWCIsr)

Merrill and Sabharwal show that log-precision transformer classifiers admit a logical characterization with majority quantifiers. They also emphasize that finite-precision transformers are too weak to model broad uniform attention.

**Relevance.** This is another useful bridge to threshold-circuit style reasoning. It supports comparing our head complexity to threshold-like complexity measures, but it still does not isolate the one-layer softmax model from [model.md](model.md).

## Constructive Attention And Counting

### Weiss et al. 2021. Thinking Like Transformers

Source: [PMLR](https://proceedings.mlr.press/v139/weiss21a.html)

Weiss, Goldberg, and Yahav introduce RASP as a programming language for transformer encoders. Their examples include histograms, sorting, and Dyck languages, and the RASP viewpoint helps reason about how many layers and heads a construction needs.

**Relevance.** This is the most useful constructive mindset for the current repo. It suggests that head upper bounds should come from explicit summary statistics and interpolation schemes, not from black-box universality.

### Likhosherstov et al. 2021. On the Expressive Power of Self-Attention Matrices

Source: [arXiv](https://arxiv.org/abs/2106.03764)

Likhosherstov, Choromanski, and Weller study the self-attention matrix itself. They show that fixed self-attention parameters can approximate arbitrary sparse attention patterns when the inputs are chosen appropriately, with hidden dimension growing only logarithmically in sequence length.

**Relevance.** This is about attention patterns rather than exact Boolean readout. Still, it is relevant because it isolates what the softmax attention matrix can encode before the final probe is applied.

### Yang and Chiang 2024. Counting Like Transformers: Compiling Temporal Counting Logic Into Softmax Transformers

Source: [arXiv](https://arxiv.org/abs/2404.04393)

Yang and Chiang compile a temporal counting logic into future-masked soft attention transformers. This gives a constructive counting result in a softmax setting.

**Relevance.** This is the closest constructive precedent for the upper-bound route that currently looks promising in the repo. It suggests that count-like statistics are a natural target for softmax attention constructions.

## Closest Recent Parity Reference

### Kozachinskiy et al. 2026. Parity, Sensitivity, and Transformers

Source: [arXiv](https://arxiv.org/abs/2602.05896)

Kozachinskiy, Steifer, and Wałȩga give a parity construction for softmax transformers with length-independent positional encodings and no layer normalization, and they also prove a lower bound showing that parity cannot be solved with one layer and one head.

**Relevance.** This is very close in spirit to the repo. It directly studies parity and a shallow transformer setting. However, it still does not compute the exact quantity $H^{\ast}(\mathrm{XOR}_n)$ for the model in [model.md](model.md), and it does not give a general upper-bound invariant for arbitrary Boolean functions.

## Adjacent Literature For General Certified Estimation

The most useful general methodology comes from several fields rather than from one paper that studies $H^{\ast}$ directly. The full synthesis is in [general_hstar_scalable_research_program.md](artifacts/calculations/general_hstar_scalable_research_program.md).

### Sign matrices and factorization norms

[Linial, Mendelson, Schechtman, and Shraibman](https://www2.mta.ac.il/~adish/Pubs/Papers/complexity_matrices.pdf) compare sign-rank, margin complexity, and the factorization norms $\gamma&#95;2$ and $\gamma&#95;2^{\ast}$. Their argument after Lemma 4.4 applies to every real matrix with a prescribed sign pattern. Optimizing that realization gives

$$ \tau(S)=\min\left\lbrace\gamma_2^{\ast}(W):S\circ W\geq\mathbf1\right\rbrace,\qquad \mathrm{srank}(S)\geq\frac{mn}{\tau(S)}. $$

The optimized value is one SDP. A rational feasible sign realization together with a rational PSD dual witness gives a verified upper bound on $\tau(S)$, hence a verified lower bound on sign-rank. No numerical optimality claim is needed. Since the literal matrix $W=S$ is feasible, this backend always dominates evaluating $\gamma&#95;2^{\ast}$ only at $S$.

[Hatami, Hatami, Pires, Tao, and Zhao](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2022.22) introduce product average margin and prove

$$ \mathrm{srank}(S)\geq\frac1{m_{\mathrm{avg}}(S)}. $$

For any fixed rational row and column distributions, the relevant inner problem is an SDP whose rational dual-feasible points have the safe certificate direction. Uniform weights recover the optimized $\tau$ bound after normalization, while nonuniform product weights can improve it. This is the strongest scalable matrix relaxation found in the present review. Deterministic submatrices are the main way to control the PSD order.

[Krishnan and Mitchell](https://optimization-online.org/2001/08/365/) formulate semidefinite programs as semi-infinite LPs and generate spectral cuts. This supplies a dependency-light candidate solver for both matrix bounds: solve the current LP, find a negative eigenvector of the dual matrix, add its linear quadratic-form inequality, and repeat. The result is not a certificate until it is rationally repaired.

For nondegenerate candidates, a rational Gram approximation plus an exactly diagonally dominant residual gives a compact positive-semidefinite witness. Degenerate cases are genuinely subtler. [Kolmogorov, Naldi, and Zapata](https://arxiv.org/abs/2405.13625) give a symbolic-numerical certification method that does not assume rational feasible points, while [Henrion, Naldi, and Safey El Din](https://arxiv.org/abs/1802.02834) give exact algorithms for degenerate spectrahedra. These belong as residual fallbacks rather than default arbitrary-table solvers.

Simple inner-cone substitutions have sharp limits in this problem. Diagonal and scaled diagonal dominance certify only sign-rank one. More generally, a factor-width decomposition of width $k$ can certify sign-rank at most $k-1$, so proving $H^{\ast}(f)\geq h$ requires block width at least $2^h$. This ceiling follows directly from the trace and off-diagonal mass of the block dual.

[Bhangale and Kopparty](https://arxiv.org/abs/1503.04486) show why exact sign-rank is not a general computational default. Deciding whether a sign matrix has sign-rank at most three is already hard.

[Hatami, Hosseini, and Lovett](https://theoryofcomputing.org/articles/v018a019/) show that low sign-rank can coexist with exponentially small discrepancy. This rules out discrepancy as an unconditional replacement for sign-rank here. It remains useful only after imposing explicit score-margin and denominator-conditioning assumptions.

Two 2026 papers add promising tools for structured partition matrices. [Frick, Hosseini, and Vasileuski](https://arxiv.org/abs/2604.01510) give a $\mathbb Z_2$-topological framework for exact sign-rank and obtain sharp bounds for Gap Hamming Distance. [Bindu, Hatami, Karimi, and Robere](https://arxiv.org/abs/2605.01038) develop hyperplane-avoidance lower bounds for approximate sign-rank. A lower bound on approximate sign-rank also lower-bounds exact sign-rank, so in principle it can feed the head conversion. At present these results are family-specific or asymptotic, and they do not yet supply a compact exact certificate backend for an arbitrary truth table.

### Chow varieties and arithmetic-circuit flattenings

The cleared $H$-head numerator is a tangent to the Chow variety of products of $H$ linear forms. Every tangent point is in the second secant closure. This connects the problem to equations for Chow secants in [Guan](https://arxiv.org/abs/1602.04275) and to generic Chow-rank geometry in [Torrance and Vannieuwenhoven](https://arxiv.org/abs/2005.12436).

For computation, the positive second-secant relaxation has a removable diagonal degeneracy. Parameterizing the endpoint difference as $tv$, normalizing one coordinate of $v$, and dividing every positive-negative pair gap by $t$ replaces the identically zero diagonal by a tangent-direction boundary. This is a project-specific construction rather than a theorem imported from the cited papers. [Theorem 193](lemmas/02_complexity_measure_upper_bounds/193_positive_secant_diagonal_blowup.md) proves that this pair-gap replacement is exact.

[Theorem 194](lemmas/02_complexity_measure_upper_bounds/194_signed_secant_diagonal_blowup.md) gives a more scalable compactification. It retains the mixture scalar, writes $\theta^{(1)}=\theta+tv$ and $2s-1=ta$, and divides the signed score at each vertex. The result has $2^n$ inequalities instead of $\lvert f^{-1}(1)\rvert\lvert f^{-1}(0)\rvert$, no cross-vertex products, and a closed compact chart domain without simplex-face implications. It has total degree at most $2H+1$ and joint head-block degree one. The unblown signed system has the lower total degree $H+1$, so it remains the better target for direct CAD, NLSAT, and Positivstellensatz residual solving.

There is also a stronger elementary consequence. For $H\geq2$, every cleared form has

$$ P=L_1Q_1+L_2Q_2, $$

where the $L&#95;i$ are linear and the $Q&#95;i$ have degree $H-1$. Thus the polynomial slice rank is at most two, and the zero hypersurface contains a real codimension-at-most-two linear space. One slice generator can be chosen to be an admissible attention denominator. The formal proof is [Theorem 190](lemmas/02_complexity_measure_upper_bounds/190_slice_rank_two_obstruction.md). [Bik and Oneto](https://arxiv.org/abs/2005.08617) develop the geometry of strength and slice rank, [Catalisano, Geramita, Gimigliano, Harbourne, Migliore, Nagel, and Shin](https://arxiv.org/abs/1502.00167) study the relevant secant varieties of reducible forms, and [Flavi, Gesmundo, Oneto, and Ventura](https://arxiv.org/abs/2509.12322) give determinantal equations for small strength and a generic-section reduction theorem for cubic slice rank two.

For a fixed two-plane of linear forms, the remaining truth-table problem is one margin LP. The nonlinear search lives on $\mathrm{Gr}(2,n+1)$ and has dimension $2(n-1)$, independent of $H$. Boolean evaluation imposes a sharp limitation: [Theorem 191](lemmas/02_complexity_measure_upper_bounds/191_boolean_cube_slice_relaxation_ceiling.md) shows that the slice relaxation collapses exactly to threshold degree when $H\geq\lceil(n+1)/2\rceil$. The full-rank up-map input is the strong Lefschetz property of the squarefree monomial complete intersection, for which [Phuong and Tran](https://arxiv.org/abs/2211.13548) give a modern linear-algebra proof. Slice search is therefore a low-head geometric engine, not a universal primary layer. The positive-secant compactification and balanced block split

$$ P=G_IF_J+F_IG_J $$

give complementary model-aware feasibility relaxations with far fewer parameters than a dense degree $H$ coefficient lift.

[Guan's Koszul and Young flattenings](https://arxiv.org/abs/1510.00886) and the shifted-partial methods of [Amireddy, Garg, Kayal, Saha, and Thankey](https://arxiv.org/abs/2211.07691) suggest systematic coefficient-rank obstructions stronger than degree alone. The simplest consequence for this project is

$$ \mathrm{rank}\left(\mathrm{Cat}_k(P)\right)\leq2\binom{H}{k}. $$

This produces a new orientation-free lower hierarchy. It is necessary but not sufficient for an attention representation.

[Lasserre](https://arxiv.org/abs/2204.01319) studies polynomials that depend on a few linear forms and shows how their gradient span can be detected and exploited in optimization. This matches the first-catalecticant interpretation: its rank is the number of essential linear directions of the homogeneous lift. The additional problem here is to minimize that rank over all polynomials in a prescribed truth-table sign cone.

Splitting the inputs into more than two coordinate blocks does give an exact sign-CP-rank cap, but it does not move the universal dimension frontier. [Theorem 192](lemmas/02_complexity_measure_upper_bounds/192_multiway_sign_tensor_rank.md) proves

$$ \mathrm{srank}&#95;{\mathrm{CP}}\leq k\left(k^H-(k-1)^H\right) $$

for $k$ blocks, and proves that the ambient tensor-rank ceiling is already below this cap whenever $n\leq2H+1$. Thus multiway rank size cannot repair the matrix midpoint. [Hillar and Lim](https://doi.org/10.1145/2512329) also show that generic tensor rank and spectral computations are NP-hard. Multiway equations may still help structured functions, but a dense sign-CP-rank backend is not the scalable continuation of the matrix method.

### Pi-Sigma and ridge polynomial networks

[Shin and Ghosh](https://doi.org/10.1109/IJCNN.1991.155142) introduced Pi-Sigma networks, whose basic unit multiplies affine sums. Their later [ridge polynomial network](https://doi.org/10.1109/72.377967) develops this product-unit architecture for approximation and classification. In the present notation, one such unit is exactly

$$ Q(x)=\prod&#95;{h=1}^{H}B&#95;h(x). $$

The cleared attention score is more structured than a generic sum of product units:

$$ P(x)=cQ(x)+\sum&#95;{h=1}^{H}A&#95;h(x)\prod&#95;{g\neq h}B&#95;g(x). $$

It is the base Pi-Sigma product plus a first-order parameter derivative, so every summand shares all but one factor. This makes the Pi-Sigma literature the closest older neural-network analogue found in the review. Its results mainly concern approximation architecture and gradient training. They do not impose positive one-sided denominator factors, preserve the shared tangent structure as a complexity measure, or provide exact Boolean lower certificates. Incremental-order and partial-weight training ideas may still help the constructive upper search.

### Polynomial ideals and rank-one tensor relaxations

Normalized denominator coefficients form a rank-one nonnegative probability tensor. This is the independence model, followed by a linear Boolean evaluation map. [Gouveia, Parrilo, and Thomas](https://doi.org/10.1137/090746525) develop theta-body SDP hierarchies for polynomial ideals, while [Nie and Wang](https://arxiv.org/abs/1308.6562) develop SOS relaxations for rank-one tensor approximation.

[Alexandr, Kileel, and Sturmfels](https://arxiv.org/abs/2301.09068) study moment varieties for mixtures of product distributions as secant varieties of independence models. The algebraic-statistics setting is not identical, but it confirms that the two-product relaxation belongs to a well-developed secant-of-independence geometry.

These tools motivate marginal, flattening, and moment relaxations between threshold degree and exact head factorization. Convexifying only the score image is unsafe because a mixture of models need not be one model.

### Certified factorable polynomial optimization

The signed compactification is a factorable polynomial program over products of simplices and bounded charts. [McCormick](https://doi.org/10.1007/BF01580665) gives convergent convex and concave relaxations for factorable functions. [Sherali and Tuncbilek](https://doi.org/10.1007/BF00121304) develop the polynomial reformulation-linearization technique. Both yield rational LP leaves whose dual vectors can be checked independently.

The most natural factor graph introduces $z&#95;{hi}=tv&#95;{hi}$ once, then uses prefix products and divided-product recurrences for each active truth-table vertex. With $m$ active vertices, the lifted graph has size $O(Hn+Hm)$. Simplex-sum RLT identities are important because independent McCormick envelopes discard useful normalization information.

Bernstein coefficients give exact rational range enclosures on rational cells. [Nataraj and Arounassalame](https://doi.org/10.1007/s10898-009-9485-0) develop a Bernstein branch-and-prune method for polynomial systems. The coefficient tensor is exponential in the full parameter dimension, so Bernstein data belong on low-dimensional residual cells rather than at the root.

[Handelman's theorem](https://doi.org/10.2140/pjm.1988.132.35) gives LP-checkable positivity representations on polytopes for strictly positive polynomials. It is well matched to cellwise aggregate refutations, but it gives no practical uniform degree bound and does not automatically certify boundary nonnegativity.

Dense moment-SOS remains a residual method. [Lasserre](https://doi.org/10.1137/S1052623400366802) supplies the convergent moment hierarchy, while [Peyrl and Parrilo](https://doi.org/10.1016/j.tcs.2008.09.025) show how numerical SOS results can be converted into exact rational certificates under suitable conditions. The original unblown signed system has degree $H+1$ in about $2Hn+1$ variables. Even its first relevant dense moment matrices grow combinatorially, so active-vertex reduction and cell projection must come first.

The likelihood-ratio form also resembles signomial optimization. [Chandrasekaran and Shah](https://doi.org/10.1137/140988978) introduce relative-entropy SAGE relaxations, and [Wang, Jaini, Yu, and Poupart](https://arxiv.org/abs/2003.03731) prove completeness of a conditional SAGE hierarchy on compact convex sets. SAGE preserves sparse exponent structure and may be a useful discovery bound. Its relative-entropy proof objects are not presently as easy to verify over exact rationals as McCormick, RLT, Bernstein, Handelman, or rational SOS identities, so it should not define a certified endpoint without a separate exactification layer.

### Robust convex geometry

The fixed-denominator lower alternative says that the origin lies in the convex hull of the signed feature rows. Carathéodory gives a small support for membership, but not for robust interior membership. [Ivanov and Naszódi](https://arxiv.org/abs/2212.04308) prove a quantitative Steinitz theorem: at most $2d$ vertices retain a centered inball with only polynomial loss in radius.

This yields a determinant-free parameter-cell certificate. If selected rows contain a centered ball at one parameter and move less than its radius across a cell, the whole cell is infeasible for a strict readout.

### Adjustable robustness and exchange methods

The exact lower quantifiers have the adjustable robust form

$$ \forall\theta\in(\Delta&#95;n)^H\quad\exists q(\theta)\in\Delta&#95;{2^n}\quad R(\theta)^{\top}q(\theta)=0. $$

[Ben-Tal, Goryashko, Guslitzer, and Nemirovski](https://doi.org/10.1007/s10107-003-0454-y) introduce tractable adjustable decision-rule approximations. [Bertsimas, Iancu, and Parrilo](https://optimization-online.org/2009/06/2327/) develop a hierarchy of polynomial policies computed by semidefinite programming. In this project, polynomial $q(\theta)$ policies become exact lower certificates after coefficient matching and a rational Handelman or SOS positivity proof.

[Zeng's](https://optimization-online.org/2011/06/3065/) column-and-constraint generation gives the right decomposition pattern for a practical loop. The master keeps finitely many denominator scenarios and support policies; a separation oracle searches for an uncovered tuple. [Wang and Guo](https://arxiv.org/abs/1306.1875) combine exchange methods with polynomial optimization on a compact infinite index set. Their exact convergence statements do not transfer automatically because the head problem has a zero-margin discriminant and adjustable multipliers, but the exchange architecture remains certificate compatible: verified leaves accumulate monotonically, and unresolved cells simply leave the bound unchanged.

### Semi-algebraic capacity and sampling

[Goldberg and Jerrum](https://www.cs.ox.ac.uk/people/paul.goldberg/papers/goldbergjerrum.pdf) bound the VC dimension of concept classes whose membership tests use polynomial predicates in real parameters. Applied to the enlarged $H$-head family, their theorem gives a bound of order

$$ Hn\log(H+1). $$

This supports sampled witness mining and distance estimates. It does not prove exact equality from a feasible sample. An exactly certified infeasible sample is nevertheless a valid global lower certificate.

### Sparse threshold representations and column generation

Sparse polynomial threshold functions are the closest constructive analogue on the upper-bound side. [O'Donnell and Servedio](https://www.cs.cmu.edu/~odonnell/papers/ptf-extremal.pdf) study extremal PTF density, while [Sezener and Oztop](https://arxiv.org/abs/1504.01167) use repeated margin-LP refitting to search for low-density representations. Their support count is not the same as head count here: a Walsh character on $k$ variables costs roughly $k$ heads, while a monotone monomial of degree at least two costs one head under the repo's compiler.

The right adaptation is cost-aware column generation. All Walsh correlations can be priced by one fast Walsh-Hadamard transform, and all monotone-monomial correlations by one superset zeta transform, each in $O(n2^n)$ time. [LPBoost](https://doi.org/10.1023/A:1012470815092) supplies the restricted-master pattern. Every proposed support is refitted on the full cube, rounded to exact integers, and passed through the theorem-backed compiler. Weighted $\ell_1$ optimality is only a support heuristic, not a head lower bound. The Boolean rule-set branch-and-price method of [Lawless, Dash, Günlük, and Wei](https://jmlr.org/papers/v24/22-0880.html) is a close analogue for searching the repo's affine-cylinder dictionary.

The implemented prototype gives a first memory-scale check. On equality of two six-bit strings, it generated $80$ nonlinear columns and used at most $712704$ restricted-master entries, compared with $16777216$ entries in the full feature matrix. Exact refitting returned a verified $7$-head certificate. It can still miss an expensive but decisive feature, as happened for twelve-bit parity under a small column budget, so transform pricing, deletion, and structural seeds should remain separate portfolio members.

[Bruck and Smolensky](https://doi.org/10.1137/0221003) provide the adjacent harmonic-analysis precedent for connecting spectral mass with sparse polynomial-threshold representations. The repository's compiler gives a sharper model-specific finite problem. If unnormalized Walsh coefficients with total omitted absolute mass below $2^n$ are dropped, the retained polynomial has the same strict signs. [Theorem 196](lemmas/02_complexity_measure_upper_bounds/196_optimal_fourier_tail_knapsack.md) shows that the minimum compiler cost under this sufficient criterion is an exact knapsack problem solvable in $O(n4^n)$ integer operations, polynomial in the truth-table length. The linear-time greedy tail remains the default seed, while the knapsack is an exact escalation.

A model-native extension treats each admissible denominator as one normalized feature group. Group-sparse fitting and continuous denominator pricing can propose a small head library. [Theorem 195](lemmas/02_complexity_measure_upper_bounds/195_atomic_margin_sparsification.md), using the approximate Carathéodory theorem of [Mirrokni, Paes Leme, Vladu, and Wong](https://proceedings.mlr.press/v70/mirrokni17a.html), proves that an output-normalized convex atomic score with scale $\Lambda$ and margin $\gamma$ can be sparsified to $O(n(\Lambda/\gamma)^2)$ genuine heads. Only rationalization and exact full-cube verification establish an upper bound. Failed pricing has no lower-bound meaning.

### Sensitivity as a cheap degree screen

[Diakonikolas, Raghavendra, Servedio, and Tan](https://arxiv.org/abs/0909.5011) give an explicit average-sensitivity bound for degree $d$ polynomial threshold functions:

$$ \mathrm{AS}(f)\leq2n^{1-1/2^d}. $$

Since every $H$-head function is a PTF of degree at most $H$, an exact bichromatic-edge count gives an $O(n2^n)$ lower presolve. It is cheap and restriction-stable, but initial pilots show that it is usually weaker than exact threshold degree. [Kane's](https://arxiv.org/abs/1210.1283) sharper asymptotic result has hidden degree-dependent constants, so it is not yet a convenient finite exact certificate here.

### Rational approximation and its limitation here

Positive-denominator rational sign degree collapses to threshold degree because

$$ \mathrm{sign}(p/q)=\mathrm{sign}(p) $$

when $q>0$. The model-specific content is not rationality by itself. It is the tangent numerator with shared denominator factors. Rational approximation remains relevant through composition and intersection results such as [Sherstov's halfspace-intersection work](https://arxiv.org/abs/0910.1862), but it is not a direct lower bound for ordinary $H^{\ast}$.

## What Seems Missing Relative To This Repo

The survey suggests four gaps.

1. I did not find a prior paper that directly studies the exact minimum head count $H^{\ast}(f)$ for the one-layer attention-only model from [model.md](model.md).

2. Existing upper bounds are usually too coarse for our purpose. They are about universality, Turing-completeness, or logical definability, not exact head complexity on a fixed cube.

3. Existing lower bounds are often asymptotic in input length. They do not automatically convert into finite $n$ exact statements like $H^{\ast}(\mathrm{XOR}_n) = n$.

4. The adjacent methods are individually incomplete. Product average margin can miss large sign-rank, algebraic secant equations forget denominator orientation, and sparse construction is one-sided. The missing object is therefore a certificate-compatible portfolio, not merely a new heuristic optimizer.

## Working Takeaway For Upper Bounds

Constructive counting remains the cleanest closed-form upper theorem, but the scalable numerical methodology should search a larger exact dictionary.

For the current project, the cleanest version is to make heads produce a basis of rational functions of a single positive weighted sum

$$t(x) = \sum_{i=1}^{n} \lambda_i x_i,$$

then interpolate arbitrary target labels on the finite image of $t$.

That is the route taken in [theorems/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md](theorems/01_foundations_and_normal_form/009_weighted_sum_upper_bound.md). It gives:

- a general upper bound when $f$ factors through a positive weighted sum,
- a clean $n$-head upper bound for all symmetric Boolean functions,
- a universal bound $H^{\ast}(f) \leq 2^n - 1$ by taking binary weights.
