# Certified Numerical Estimation of Head Complexity

## Objective

Given the complete truth table of a Boolean function $f : \lbrace0,1\rbrace^n \to \lbrace0,1\rbrace$, compute an anytime interval

$$ L(f) \leq H^{\ast}(f) \leq U(f). $$

Both endpoints must be mathematically justified. A numerical search miss never changes $L(f)$. A numerical success changes $U(f)$ only after exact integer verification.

The implementation is in `src/hstar/certified.py`, with exact cube conventions in `src/hstar/boolean_cube.py`, rational-head certificate code in `src/hstar/fractional.py`, transform-priced sparse PTF certificates in `src/hstar/sparse_ptf.py`, and a command line interface in `src/hstar/certified_cli.py`.

## Input convention

Vertex code $v$ has coordinate $i$ equal to bit $i$ of $v$. Coordinate zero is therefore the least-significant bit. Truth-mask bit $v$ is one exactly when $f(v)=1$.

This convention matches the exact calculation artifacts in this repository. It differs from the older lexicographic convention in `src/hstar/truth_tables.py`.

## Guaranteed lower endpoint

The estimator takes the maximum of the following available lower bounds.

1. A nonconstant function has $H^{\ast}(f)\geq1$.

2. If a restriction of $f$ is parity on $k$ free variables, then restriction monotonicity and threshold degree give $H^{\ast}(f)\geq k$. The code searches all subcubes for the largest such witness.

3. Exact threshold degree gives

$$ \deg_{\pm}(f) \leq H^{\ast}(f). $$

For each $d$, let $M_d$ be the evaluation matrix of all squarefree monomials of degree at most $d$, and let $s(x)=2f(x)-1$. Degree $d$ is feasible exactly when the rational linear system

$$ \mathrm{diag}(s)M_dc \geq \mathbf{1} $$

is feasible. The optional Z3 backend decides this in exact linear real arithmetic. A satisfiable model is converted to integer coefficients and checked at every vertex. Unsatisfiable lower-degree instances raise the lower endpoint. An SMT-LIB file can be archived for every decision.

4. Coordinate partitions give sign matrices. The estimator applies an exact Gershgorin upper bound to the spectral norm, then combines Forster's sign-rank theorem with the universal tangent-rank cap. A deterministic submatrix keeps the Gram calculation within budget, and the stored integer witness is independently verified.

5. Symmetric functions are classified exactly by the number of sign changes in their Hamming-weight profile. This yields a matching lower bound without invoking a solver.

6. The repository can recognize functions with stronger proved lower bounds. At present this includes the eight-bit Hamming-threshold function from `lemmas/06_strict_separations/189_eight_bit_hamming_threshold_strict_separation.md`, for which two heads are impossible.

The threshold-degree and nonlinear solver results are exact solver-backed statements. For a portable certificate independent of the solver, retain a rational Gordan witness, a CAD proof, a rational Positivstellensatz identity, or an exact finite cell cover.

## Guaranteed upper endpoint

The estimator starts with theorem-backed constructions.

1. Choose positive integer weights $w_i$ such that $f$ is constant on each level of $\sum_iw_ix_i$. If the induced level profile changes sign $r$ times, the positive-projection construction gives $H^{\ast}(f)\leq r$. The code tests equal weights, coordinate permutations of injective binary weights, and Hamming-layered binary perturbations $w_i=2^n+2^{\pi(i)}$. The last family keeps Hamming-weight layers ordered while optimizing the order within each layer. It gives the certified upper bound $H^{\ast}(f_6)\leq8$ for the six-bit parity triple-flip candidate.

2. If the minority label has support size $m$, then $H^{\ast}(f)\leq2m$, with the sharper value one when $m=1$.

3. The optional sparse PTF backend runs cost-aware column generation in the monotone and Walsh bases. Fast zeta and Walsh-Hadamard transforms price the implicit dictionaries in $O(n2^n)$ time. A separate optional backend computes the exact optimum within the absolute Fourier-tail criterion by a budgeted integer dynamic program. Every selected support is checked on the full cube and compiled through a proved head upper bound. A column, vertex, or dynamic-program budget miss changes no lower bound.

4. A proved or archived exact construction may lower the endpoint. The six-bit parity triple-flip certificate has six strictly oriented denominators and minimum signed cleared score $11861735510772$, giving the interval $4\leq H^{\ast}(f_6)\leq6$. The known eight-bit certificate has three strictly negative-orientation denominators and a minimum signed cleared score of $58$.

5. Numerical denominator searches may propose a smaller construction. Every reported construction has integer denominators, strictly model-faithful orientations, integer readout coefficients, and a positive signed cleared score at every cube vertex.

6. For functions on at most four bits, the repository's exact classification proves equality with threshold degree. Once exact threshold degree is available, this closes the interval immediately.

The resulting upper endpoint is valid even if every heuristic search fails.

## Exact global decision problem

For a requested head count $H\geq1$, absorb the global readout constant into the first affine numerator. For orientation $\sigma\in\lbrace+,-\rbrace$, define

$$ \ell_i^+(x)=x_i,\qquad \ell_i^-(x)=1-x_i. $$

For head $h$, introduce an affine numerator and normalized literal weights:

$$ A&#95;h(x)=a&#95;{h0}+\sum&#95;{i=1}^na&#95;{hi}x&#95;i,\qquad B&#95;h(x)=\theta&#95;{h0}+\sum&#95;{i=1}^n\theta&#95;{hi}\ell&#95;i^{\sigma&#95;h}(x). $$

The cleared score is

$$ P(x)=\sum&#95;{h=1}^H A&#95;h(x)\prod&#95;{g\neq h}B&#95;g(x). $$

The orientation branch is feasible exactly when

$$ \theta&#95;{hi}\geq0,\qquad \sum&#95;{i=0}^n\theta&#95;{hi}=1,\qquad s(x)P(x)\geq1\quad\text{for every }x\in\lbrace0,1\rbrace^n. $$

These are rational polynomial constraints. Head exchangeability reduces the $2^H$ orientation vectors to $H+1$ orientation counts.

The use of the closed simplex is exact for finite strict sign representation. Given a boundary solution, perturb each weight vector toward the uniform interior point. The cleared polynomial varies continuously at finitely many vertices, so its margin remains positive for a sufficiently small perturbation. The perturbed denominators are strictly admissible.

The boundary ratio itself need not be defined. Only the cleared polynomial is used before perturbation. Replacing the margin condition by a non-strict zero margin would be invalid because the zero polynomial would then satisfy every label pattern.

Each orientation branch is a quantifier-free nonlinear real-arithmetic instance. Exact real quantifier elimination is complete in principle. Therefore the following algorithm determines $H^{\ast}(f)$ exactly:

1. Obtain any rigorous finite upper bound $U$.

2. Starting at the current lower bound $L$, decide all $H+1$ branches for each $H<U$.

3. If every branch is unsatisfiable, replace $L$ by $H+1$.

4. If one branch is satisfiable, replace $U$ by $H$ and recover a strict rational certificate.

5. Stop when $L=U$.

Z3 NLSat is the first implemented backend. Its `unknown` or timeout result gives no information. Difficult unsatisfiable cases should be cross-checked with CAD, Mathematica `Resolve`, Redlog, or an independently checked algebraic certificate.

## Numerical search layer

For fixed denominators, the numerator and readout problem is linear. Its feature matrix has columns

$$ \prod&#95;hB&#95;h,\qquad (1,x&#95;1,\ldots,x&#95;n)\prod&#95;{g\neq1}B&#95;g,\qquad\ldots,\qquad(1,x&#95;1,\ldots,x&#95;n)\prod&#95;{g\neq H}B&#95;g. $$

The implementation samples strict oriented integer denominators and solves the inner maximum-margin linear program. A floating solution is scaled and rounded until exact integer arithmetic verifies every signed cleared score. This is a simple variable-projection heuristic. More aggressive outer optimizers can reuse the same inner solver and exactification step.

For a fixed denominator tuple, infeasibility also has a Gordan alternative. If $M_\theta$ is the signed cleared feature matrix, fixed-tuple failure is equivalent to the existence of

$$ q\geq0,\qquad \sum_xq_x=1,\qquad M_\theta^{\top}q=0. $$

Such a witness refutes only that denominator tuple. It is not a global $H$-head lower bound.

## Guarantee levels

- **Portable exact:** a theorem, integer head or sparse PTF upper certificate, rational Gordan identity, exact cell cover, or algebraic identity checked without numerical tolerance.

- **Exact solver-backed:** Z3, CAD, or another exact real-arithmetic backend returns `sat` or `unsat`. Archive the input and, where possible, a proof object or reconstructed rational witness.

- **Heuristic diagnostic:** floating optimization, sampling, dReal, or an unexactified SOS computation. A failure changes no endpoint.

Every returned interval remains valid under these labels. The distinction records how independently auditable each endpoint is.

## Commands

Install the research backend in a cloud task:

```bash
uv sync --extra research
```

Estimate two-bit XOR, whose truth mask is `0x6`:

```bash
PYTHONPATH=src uv run --extra research python -m hstar.certified_cli estimate --dimension 2 --mask 0x6 --heuristic-restarts 100
```

Enable exact nonlinear decisions and archive every SMT-LIB instance:

```bash
PYTHONPATH=src uv run --extra research python -m hstar.certified_cli estimate --dimension 4 --mask 0x6996 --exact-nra --nra-max-heads 3 --export-directory artifacts/calculations/certified_run
```

Enable transform-priced sparse PTF construction. This example certifies the upper bound four for equality of two three-bit strings:

```bash
PYTHONPATH=src uv run python -m hstar.certified_cli estimate --dimension 6 --mask 0x8040201008040201 --no-z3-threshold --sparse-ptf --sparse-ptf-iterations 8 --sparse-ptf-batch-size 16 --sparse-ptf-max-columns 128
```

Enable the exact Fourier-tail knapsack with explicit resource limits. On this Walsh-structured six-bit function it improves the exhaustive positive-projection bound from $15$ to $8$:

```bash
PYTHONPATH=src uv run python -m hstar.certified_cli estimate --dimension 6 --mask 0xb1e41b4e278d72d8 --no-z3-threshold --optimal-fourier-tail --optimal-fourier-tail-max-transitions 50000000 --optimal-fourier-tail-max-vertices 64
```

The exact eight-head certificate is archived in `artifacts/calculations/six_bit_optimal_fourier_tail_h8_certificate.json`. A transition or vertex budget miss is returned as a diagnostic skip, not as evidence for a lower bound.

Verify a JSON head or sparse PTF certificate independently of the optimizer:

```bash
PYTHONPATH=src uv run python -m hstar.certified_cli verify --dimension 2 --mask 0x8 --certificate certificate.json
```

Run the repository smoke verifier:

```bash
PYTHONPATH=src uv run python artifacts/calculations/verify_certified_hstar_estimator.py
```

## Relation to nearby literature

The estimator combines several established toolkits, but the quantity $H^{\ast}(f)$ itself appears specific to this project. Threshold degree supplies the first convex lower bound. Gordan and Farkas alternatives supply exact fixed-parameter obstructions. The full decision problem belongs to the existential theory of the reals. CAD and Positivstellensatz methods supply complete or checkable global certificates. Variable projection and certified branch-and-bound provide the natural numerical architecture.

The broader transformer, rational approximation, threshold-degree, sign-rank, and real-algebraic context is reviewed in `literature_survey.md`. None of those neighboring formulations turns a failed denominator search into a valid lower bound, which is the central certification issue addressed here.
