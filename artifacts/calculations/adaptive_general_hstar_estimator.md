# Adaptive Certified Estimation of General Head Complexity

## Main Conclusion

For a truth table $f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$, the scalable target should be an anytime certified interval

$$ L(f)\leq H^{\ast}(f)\leq U(f), $$

not one numerical surrogate. The estimator should run a portfolio of theorem-backed upper and lower engines, route work by mathematical feasibility screens, and store every accepted improvement in a proof directed acyclic graph.

The recommended architecture has three layers:

1. an input-linear structural and spectral pass;

2. adaptive construction and obstruction queues that exchange hard vertices and exact dual weights;

3. model-native branch-and-bound or real-algebraic refutation only on the unresolved frontier.

The current implementation already covers much of the first layer and the sparse construction part of the second, including a budgeted exact Fourier-tail escalation. The highest-value new components are output-normalized atomic boosting, weighted $\tau$ hard-core search, and rational signed-secant subdivision.

## Scalability Model

Put $V=2^n$. A complete truth table already has length $V$, so $O(nV)$ arithmetic is nearly input-linear. Walsh-Hadamard transforms, cube-edge scans, exact certificate verification, and one pass through every signed constraint are scalable in this model.

There are three distinct access modes.

### Complete truth table

Every candidate upper score can be checked at all $V$ vertices. Lower witnesses may be small, but exhaustive transforms and separation oracles are available.

### Membership oracle

Sampling can discover restrictions and hard cores, but it cannot certify a global upper bound without a complete verification oracle. Exact determination has a worst-case $\Omega(V)$ query barrier. A deterministic algorithm that leaves one vertex unqueried cannot distinguish the constant-zero function, with head complexity zero, from the function that is one only at that unseen vertex, with head complexity one.

### Symbolic representation

A circuit, formula, or decision diagram can replace exhaustive evaluation only when it supplies a sound counterexample or equivalence oracle for the candidate score. Otherwise the result is a sampled diagnostic, not a certificate for the full function.

## Certified State

The root state should contain:

- the current interval $[L,U]$;

- a lower frontier whose next target is to prove $H^{\ast}(f)>L$;

- an upper frontier whose next target is to construct a score with fewer than $U$ heads;

- a proof graph whose nodes contain a claim, theorem, exact payload, parent transformations, and verifier command;

- an untrusted discovery cache containing floating scores, dual weights, failed solver logs, and proposed hard subsets.

Only the proof graph may change $L$ or $U$. Discovery data may change scheduling priorities but never the certified interval.

For each active action, estimate

$$ \mathrm{priority}=\frac{\mathrm{endpointGain}\cdot\mathrm{successEstimate}}{\mathrm{verificationCost}}. $$

The numerical value is only a scheduler score. It is not part of the mathematical result.

## Initial Pass

One shared cube pass should compute or cache:

- label counts and minority support;

- the Hamming-weight profile and target symmetries;

- bichromatic cube-edge counts;

- the exact Walsh transform;

- equal-weight positive-projection runs;

- row hashes needed for candidate partition matrices;

- a deterministic pool of restrictions and balanced coordinate partitions.

This pass immediately yields constant, singleton-minority, symmetric-profile, simple positive-projection, Fourier-tail, sensitivity, and cheap spectral candidates. More expensive restriction enumeration should be beam-limited rather than included in the nominal $O(nV)$ bootstrap.

## Method Routing Table

| Engine | Endpoint | Mathematical gate | Accepted certificate |
|---|---:|---|---|
| Threshold degree | lower | Degree features fit the LP budget | Exact feasible polynomial or exact infeasibility dual |
| Restriction mining | lower | Safe literal substitution and sufficient free variables | Substitution map plus child certificate |
| Partition spectral and weighted $\tau$ | lower | Both partition sides can support the target sign rank | Integer Gram bound or rational positive semidefinite witness |
| Positive projection and minority support | upper | Always cheap | Explicit theorem parameters |
| Sparse monomial and Walsh PTF | upper | Dictionary, transform, or column budget | Integer sign polynomial plus compiler theorem |
| Atomic-margin boosting | upper | Denominator pricing produces a positive normalized margin | Rational finite atomic decomposition |
| Direct denominator search | upper | Fixed-denominator LP is affordable | Integer head parameters and positive cleared margin |
| Signed-secant subdivision | lower | Generic lower layers are screened out or exhausted | Exact chart cover with rational cell leaves |
| Adjustable Gordan policies | lower | A low policy degree fits the identity budget | Rational coefficient identities and positivity certificates |
| CAD, NLSAT, or Positivstellensatz | either | Small residual system only | Solver-backed decision or independently checked algebraic certificate |

## Upper-Bound Ladder

### Fourier-tail construction

Let $c_S$ be the unnormalized Walsh coefficients, so

$$ Vq(x)=\sum&#95;S c&#95;S\chi&#95;S(x). $$

If the omitted absolute coefficient mass is below $V$, the retained polynomial has the strict signs of $q$. The current greedy seed sorts by coefficient mass per compiler head and verifies the selected integer score exactly.

[Theorem 196](../../lemmas/02_complexity_measure_upper_bounds/196_optimal_fourier_tail_knapsack.md) gives an exact escalation. Bundle all singleton coefficients into one cost-one item. Give each nonsingleton coefficient value $\lvert c_S\rvert$ and cost $\lvert S\rvert$. The best certificate under this tail criterion is a zero-one knapsack with total cost at most $nV+1$, hence it is solvable in $O(nV^2)$ integer operations.

This is a useful middle budget:

- greedy tail selection costs one transform and a sort;

- exact tail knapsack is quadratic in truth-table length;

- support-refit LPs search beyond the unique Fourier expansion;

- transform-priced column generation avoids materializing the full $V\times V$ feature dictionary.

A failed tail or sparse-PTF search has no lower-bound meaning.

The public estimator now exposes the exact escalation through `--optimal-fourier-tail`, with independent vertex and estimated-transition budgets. It computes the transition estimate before allocating the dynamic-program table. On the structured six-bit mask `0xb1e41b4e278d72d8`, the exhaustive positive-projection construction costs $15$ heads, while the optimal tail certificate costs $8$ heads. The grouped program estimated $91$ transitions and executed $20$. The exact certificate is [six_bit_optimal_fourier_tail_h8_certificate.json](six_bit_optimal_fourier_tail_h8_certificate.json).

For comparison, the fixed pseudorandom mask `0xcc4b244f3c92d063` has optimal tail cost $117$, with $12032$ estimated and $3606$ executed transitions. It does not improve the much smaller projection or sparse-PTF bounds. This supports a simple gate: run the exact tail program only when its transition estimate fits the budget and its greedy or structural preview can plausibly beat the current upper endpoint.

### Cost-aware sparse PTF search

Use both compiler bases.

- In the monotone basis, all affine terms share one head and every active nonlinear monomial costs one head.

- In the Walsh basis, all singleton characters share one head and a character on $k\geq2$ variables costs $k$ heads.

For a support proposal, solve a maximum-margin LP, round the coefficients to integers, and check every vertex. Column generation should use a zeta transform or Walsh-Hadamard transform to price every implicit feature in $O(nV)$ work per pricing pass.

The exact certificate, not the floating objective, determines the upper endpoint.

### Output-normalized atomic boosting

Let $\mathcal A_n$ be the symmetric set of valid one-head score vectors normalized in output space by $\lVert a\rVert_{\infty}\leq1$. [Theorem 195](../../lemmas/02_complexity_measure_upper_bounds/195_atomic_margin_sparsification.md) shows that a convex atomic score with scale $\Lambda$ and cube margin $\gamma$ has a representation using at most

$$ C(n+1)\left(\frac{\Lambda}{\gamma}\right)^2 $$

heads.

This suggests a model-native totally corrective boosting loop:

1. maintain a finite library of normalized one-head atoms;

2. solve the active max-margin master problem;

3. use its exact or floating residual distribution to price a new atom;

4. for a fixed positive denominator $B$, optimize the affine numerator $A$ by an LP with $-B(x)\leq A(x)\leq B(x)$;

5. search the denominator simplex outside that LP;

6. sparsify, rationalize, and verify the final finite decomposition on the full cube.

For a fixed denominator, numerator pricing is convex. Denominator pricing remains nonlinear and may use sampling, local search, or branch-and-bound. Failure of the outer pricing search proves nothing. A finite exact positive-margin decomposition is already a direct upper certificate, even without invoking the asymptotic sparsification bound.

This is the closest model-specific analogue of LPBoost. [Demiriz, Bennett, and Shawe-Taylor](https://doi.org/10.1023/A:1012470815092) use column generation to build margin-maximizing convex combinations of weak learners. [Mirrokni, Paes Leme, Vladu, and Wong](https://proceedings.mlr.press/v70/mirrokni17a.html) prove the approximate Carathéodory support bound used in Theorem 195.

### Direct denominator construction

At target head count $H$, sample or optimize the $H$ denominator blocks, then solve the exact inner readout-margin LP. A candidate becomes valid only after integer or rational exactification and a positive cleared score at every vertex.

This route should receive near-margin vertices and denominator seeds from the atomic master. It is more expressive than sparse polynomial compilers and can improve their upper bounds.

## Lower-Bound Ladder

### Restrictions and threshold degree

Threshold degree remains the first convex lower invariant:

$$ \deg&#95;{\pm}(f)\leq H^{\ast}(f). $$

Run it incrementally and reuse monomial evaluation matrices. Exact primal polynomials can also be passed to both sparse compilers, while exact dual solutions identify hard vertices for restriction mining. The constructive dual viewpoint is standard in polynomial-threshold lower bounds, as illustrated by [O'Donnell and Servedio](https://www.cs.columbia.edu/~rocco/papers/stoc03ptfdb.html).

Safe restrictions include fixing variables, complementing literals, permuting coordinates, and identifying variables. General affine substitutions involving XOR are not automatically model preserving.

### Partition sign rank

To rule out $H$ heads, a partition certificate must prove sign rank at least

$$ 2^{H+1}-1. $$

Therefore both sides of the partition must contain at least that many rows or columns. For coordinate partitions this forces

$$ \min\lbrace\lvert I\rvert,\lvert J\rvert\rbrace\geq H+1,\qquad n\geq2H+2. $$

If this gate fails, skip every spectral, $\tau$, and weighted $\tau$ computation for that target. If it passes, use the following escalation:

1. exact Gershgorin repair of the Forster spectral bound;

2. optimized spectral scaling;

3. rational $\tau$ certificates;

4. weighted $\tau$ with hard row and column supports.

The precise certified hard-core scheduler is specified in [weighted_tau_hard_core_scheduler.md](weighted_tau_hard_core_scheduler.md). [Forster](https://doi.org/10.1016/S0022-0000(02)00019-3) supplies the spectral sign-rank bound, while [Linial, Mendelson, Schechtman, and Shraibman](https://www2.mta.ac.il/~adish/Pubs/Papers/complexity_matrices.pdf) supply the factorization-norm framework.

### Capacity bounds as witness miners

The exact head family has only $O(Hn)$ real parameters and bounded-degree polynomial sign tests. Results such as [Goldberg and Jerrum](https://doi.org/10.1145/168304.168377) imply useful capacity bounds for such parameterized concept classes.

This supports random and adversarial small-witness mining. It does not give a Helly theorem. A failed representation can have no presently known universally small infeasible subset, so an unresolved mined subset cannot raise the lower endpoint.

### High-head model-native refutation

Partition rank and slice rank have midpoint ceilings. Above those ceilings, use the signed positive-secant relaxation from [Theorem 194](../../lemmas/02_complexity_measure_upper_bounds/194_signed_secant_diagonal_blowup.md).

Write

$$ \theta^{(1)}=\theta+tv,\qquad 2s-1=ta,\qquad \max\lbrace\lVert v\rVert&#95;{\infty},\lvert a\rvert\rbrace=1. $$

The quotient system has one signed constraint per truth-table vertex. It uses $2H(n+1)+2$ raw charts and at most $4(n+1)+2$ chart types per orientation-count branch after head-permutation symmetry.

For one vertex, define

$$ b&#95;h=B&#95;h(x;\theta&#95;h),\qquad d&#95;h=B&#95;h(x;v&#95;h),\qquad c&#95;h=B&#95;h(x;\theta&#95;h+tv&#95;h). $$

The exact linear-size product recurrence is

$$ P&#95;0=1,\qquad R&#95;0=0,\qquad P&#95;h=P&#95;{h-1}b&#95;h,\qquad R&#95;h=R&#95;{h-1}c&#95;h+P&#95;{h-1}d&#95;h. $$

Then $P&#95;H=Q&#95;{\theta}$ and $R&#95;H=(Q&#95;{\theta+tv}-Q&#95;{\theta})/t$. A rational McCormick and RLT relaxation can therefore share $O(Hn)$ parameter nodes and use $O(Hm)$ product nodes for $m$ active vertices.

For a parameter cell $C$, an exact lower leaf consists of a rational probability vector $\lambda$ and a rational proof that

$$ \sup&#95;{z\in C}\sum&#95;x\lambda&#95;x y&#95;x\widetilde{\mathcal S}&#95;x(z)\leq0. $$

If every signed constraint were positive, this weighted average would be positive. The leaf therefore rules out the whole cell. Rational McCormick envelopes are the first engine, with RLT, Bernstein, Handelman, or SOS data used to strengthen difficult leaves.

[McCormick](https://doi.org/10.1007/BF01580665) provides the factorable convex envelopes. [Sherali and Tuncbilek](https://doi.org/10.1007/BF00121304) provide the polynomial RLT framework.

The exact leaf checker, automatic common-margin dual discovery, sparse rational reconstruction, and binary cover-tree verifier are implemented in `src/hstar/signed_secant_mccormick.py` and specified in [signed_secant_mccormick_leaf_format.md](signed_secant_mccormick_leaf_format.md). The checker reconstructs all derived intervals, McCormick inequalities, simplex constraints, the shared $z&#95;{hi}=tv&#95;{hi}$ lift, the RLT identities, and the prefix recurrence before checking a rational dual identity. One archived certificate covers a full two-head scalar chart of the eight-bit exact separation with a five-term dual of value $-1$. It is a chart-level result, not a global two-head refutation.

The blown-up system is preferred for spatial subdivision. The original system retaining the scalar $s$ has lower total degree and no charts, so CAD, NLSAT, Stengle, or SOS should receive a small residual cell projected back to that formulation.

### Adjustable Gordan policies

For fixed denominators, Gordan's alternative gives a sparse convex multiplier supported on at most $Hn+2$ signed rows. Globally, that multiplier depends on the denominator tuple. Search for low-degree polynomial multiplier policies and certify their nonnegativity on the product of simplices.

Degree-zero policies recover fixed dual obstructions. Degree-one and degree-two policies are genuinely denominator aware. Rational coefficient identities plus Handelman positivity are the first portable certificate format. SOS is a stronger residual backend.

## Cross-Feeding the Engines

The portfolio becomes more efficient when its dual information is shared.

- A sparse-PTF master distribution identifies vertices that resist the current feature dictionary. Use them to seed restrictions, sign matrices, and direct denominator batches.

- A fixed-denominator Gordan multiplier identifies a small obstruction support. Use it as the next active set in atomic pricing and signed-secant subdivision.

- Near-zero margins in an exactified upper candidate identify vertices that should never be dropped from later refits.

- A signed-secant cell multiplier $\lambda$ supplies a hard distribution for model-native atom pricing.

- A successful upper construction supplies denominator centers and orientation counts for nearby lower-frontier cells, while its exact margin gives a conditioning scale.

- A successful lower restriction or hard submatrix should be cached as a reusable child proof for every parent function containing that minor.

These transfers are heuristic scheduling decisions. The receiving engine must still produce its own exact certificate.

## Adaptive Scheduler

~~~text
state = bootstrap(function)
verify every bootstrap certificate

while budget remains and state.lower < state.upper:
    lower_target = state.lower
    upper_target = state.upper - 1

    generate only actions that pass their mathematical gates
    score actions by possible endpoint gain, observed conditioning, and cost
    run the highest-scoring bounded action

    if it returns an exact certificate:
        verify independently
        add a proof node
        update the certified endpoint
        propagate its hard support and dual weights
    else:
        retain diagnostics only

    age repeatedly unsuccessful actions
    escalate only the hard residual to a stronger backend

return the certified interval, proof graph, and separate diagnostics
~~~

The scheduler should checkpoint after every admitted proof node. A timeout, numerical failure, or unverified feasible relaxation leaves the interval unchanged.

## Certificate Schemas

Every proof node should be reconstructible without optimizer state.

### Upper node

Store the truth-table convention, theorem compiler, rational or integer score parameters, head count, and exact minimum signed margin.

### Restriction lower node

Store the literal substitution, the child truth table or hash, the child lower certificate, and the monotonicity theorem.

### Threshold lower node

Store either an exact infeasibility dual or an archived exact linear-real decision instance with a reproducible verifier.

### Partition lower node

Store the coordinate split, row and column supports, rational weights, sign matrix hash, positive semidefinite repair data, and exact objective comparison.

### Parameter-cell lower node

Store the orientation count, signed chart, rational cell box, active vertices, rational $\lambda$, factor-graph convention, relaxation coefficients, and exact nonpositive upper bound.

### Algebraic residual node

Store the exact polynomial system and either a proof-producing solver artifact or a rational identity that an independent checker can evaluate.

## Cost Guide

| Action | Nominal truth-table cost | Escalation trigger |
|---|---:|---|
| Cube scan and Walsh transform | $O(nV)$ | Always |
| Greedy Fourier tail | $O(nV+V\log V)$ | Always |
| Optimal Fourier-tail knapsack | $O(nV^2)$ | Estimated transitions fit and the preview can beat $U$ |
| One implicit sparse-PTF pricing pass | $O(nV)$ plus restricted LP | Column budget remains small |
| Threshold degree at degree $d$ | LP with $V$ rows and $D_d$ columns | It can raise $L$ |
| Partition spectral certificate | Selected matrix plus exact Gram bound | Sign-rank side-size gate passes |
| Fixed-denominator head test | $O(HV)$ features plus inner LP | It can lower $U$ |
| Signed-secant chart relaxation | $V$ constraints and $O(HV)$ factor nodes | Generic lower layers are exhausted |
| Dense SOS or CAD | Combinatorial in variables and degree | Small residual only |

The quantity $D_d=\sum_{j=0}^d\binom nj$ should be computed before building a threshold-degree matrix. Similar dimension screens should reject a slice, catalecticant, partition, or policy action before any expensive solver call.

## Important Negative Results

- Exact black-box determination cannot avoid reading essentially the whole truth table in the worst case.

- A failed numerical upper search is never a lower bound.

- A feasible point in a necessary relaxation, including the positive-secant relaxation, is not an upper certificate for the original head model.

- The optimal Fourier-tail knapsack is optimal only within the absolute tail criterion.

- Failure to find a small atomic condition number has no lower-bound meaning.

- Partition sign rank cannot rule out $H$ heads when $n\leq2H+1$.

- Plain and positivity-aware slice rank collapse to threshold degree at the Boolean middle level.

- VC and parameter-count bounds motivate witness mining but do not guarantee a small deterministic infeasible witness.

- Dense SOS scales combinatorially and should not receive the unreduced full-cube high-head problem.

- SAGE-type signomial methods may be useful numerically, but rational independently checkable proof objects are less direct here than McCormick, RLT, Handelman, or SOS identities.

## Benchmark Program

The benchmark suite should include:

- the exact archive through four bits;

- parity, symmetric predicates, equality, intersections, and sparse minority functions;

- random truth tables at each feasible dimension;

- the six-bit parity triple flip and the exact eight-bit separation;

- structured functions with known low sparse-PTF cost but high Fourier density;

- the Walsh-structured mask `0xb1e41b4e278d72d8`, where exact Fourier-tail cost $8$ beats exhaustive projection cost $15$;

- functions with weak threshold-degree bounds but strong partition or denominator geometry.

For every run, record the interval over time, endpoint-producing method, certificate size, independent verification time, number of full-cube passes, active-set sizes, and all gate rejections. Ablate cross-feeding, exact tail knapsack, weighted $\tau$, atomic pricing, and signed-secant residual handling separately.

## Priority Order

The budgeted optimal Fourier-tail backend and the signed-secant leaf, discovery, and cover-tree stack are now integrated and independently verified.

1. Add automatic split selection, active-vertex generation, symmetry reduction, and a complete signed-chart cover manifest.

2. Implement output-normalized atomic boosting with fixed-denominator numerator pricing and exact finite-decomposition verification.

3. Promote the weighted $\tau$ hard-core scheduler after its rational spectral constructor is benchmarked.

4. Add low-degree adjustable Gordan policies for residual orientation branches.

5. Use CAD, NLSAT, Positivstellensatz, or SOS only after active-set and parameter-cell reduction.

This order gives a scalable constructive improvement first, then attacks the genuinely model-specific lower-bound frontier.

## Relation to the Other Research Notes

[certified_hstar_estimation.md](certified_hstar_estimation.md) documents the current public interval estimator. [scalable_hstar_bound_methodology.md](scalable_hstar_bound_methodology.md) contains the full structural hierarchy. [general_hstar_scalable_research_program.md](general_hstar_scalable_research_program.md) develops the analytic derivations and broader literature map. [high_head_hstar_methodology.md](high_head_hstar_methodology.md) focuses on methods that remain nontrivial above midpoint rank ceilings.
