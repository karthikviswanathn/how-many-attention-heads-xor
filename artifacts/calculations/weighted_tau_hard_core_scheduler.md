# Certified Weighted Tau Hard-Core Scheduler

## Objective

This note specifies a scalable outer search for partition lower bounds on $H^{\ast}(f)$. The inner certificate is the weighted $\tau$ relaxation. The outer search mines restrictions, coordinate partitions, hard row and column supports, and rational product weights.

The central safety rule is simple: continuous optimization proposes candidates, while an independent exact verifier is the only gate that can update the certified lower bound.

## Certificate Target

For a desired conclusion $H^{\ast}(f)\geq\ell$, put

$$ r&#95;{\mathrm{target}}=2^\ell-1,\qquad U&#95;{\mathrm{target}}=\frac{1}{r&#95;{\mathrm{target}}-1}. $$

For a partition sign matrix $S$ and rational probability vectors $p,q$, the weighted inner problem is

$$ \phi&#95;{p,q}(S)=\min&#95;{W,z}\left\lbrace\sum&#95;k z&#95;k:S\circ W\geq pq^{\top},\ \mathrm{Diag}(z)-C(W)\succeq0\right\rbrace. $$

Any exactly verified feasible point of value $U<U&#95;{\mathrm{target}}$ proves sign-rank at least $r&#95;{\mathrm{target}}$, hence $H^{\ast}(f)\geq\ell$.

Every selected row and column support must contain at least $r&#95;{\mathrm{target}}$ indices. Otherwise the target is impossible by the matrix side-size ceiling.

## Search Nesting

The proposed search hierarchy is

```text
Boolean cube minor
  -> coordinate partition
    -> row and column submatrix
      -> rational product weights p and q
        -> exact weighted-tau certificate
```

Cube-minor generation may use constants, literal complementation, coordinate permutation, and variable identification. These substitutions preserve affine forms and therefore preserve the head model. General affine maps over $\mathbb F&#95;2$ involving XOR are not automatically safe.

Zero-supported weights are valuable. They select a hard submatrix exactly, so restriction mining and product-weight search are two layers of one method rather than competing methods.

## Suggested Records

```python
@dataclass(frozen=True)
class SearchScope:
    root_mask: int
    root_variable_count: int
    literal_substitution: tuple[LiteralOrConstant, ...]
    left_variables: tuple[int, ...]
    right_variables: tuple[int, ...]
    row_support: tuple[int, ...]
    column_support: tuple[int, ...]
    target_head_lower: int

@dataclass(frozen=True)
class UntrustedProposal:
    scope: SearchScope
    p_float: np.ndarray
    q_float: np.ndarray
    source: str
    proxy_value: float
    parent_key: str

@dataclass(frozen=True)
class VerifiedNode:
    scope: SearchScope
    p: tuple[Fraction, ...]
    q: tuple[Fraction, ...]
    certificate: WeightedTauCertificate
    exact_u: Fraction
    sign_rank_lower: int
    head_lower: int
    provenance: tuple[str, ...]
```

The safety boundary should be explicit:

```python
propose(node, budget) -> Iterable[UntrustedProposal]
exactify(proposal) -> WeightedTauCertificate | None
verify(scope, certificate) -> VerifiedNode | None
admit(node) -> bool
```

The admission gate reconstructs the minor and sign matrix, verifies both rational simplices, checks every signed entry inequality, checks the rational positive semidefinite witness, and recomputes $U=\sum&#95;k z&#95;k$. Solver statuses, floating objectives, leverage scores, and numerical dual multipliers are never trusted.

## Cheap Spectral Seed

For rational $p,q$, put

$$ W=D&#95;p S D&#95;q. $$

If the positive supports have sizes $r,c$, choose rational $a,b$ such that

$$ 4ab\geq\lVert W\rVert&#95;2^2. $$

Then row and column diagonal blocks $aI&#95;r,bI&#95;c$ give an exact feasible weighted $\tau$ point with

$$ U=ra+cb. $$

An exact upper bound on $\lVert W\rVert&#95;2^2$ can come from rational Gershgorin bounds on $WW^{\top}$. A rational approximate singular factor plus a diagonally dominant residual can be tighter. Optimizing $a,b$ numerically gives the proposal score

$$ U&#95;{\mathrm{spec}}(p,q)=\sqrt{rc}\lVert D&#95;p S D&#95;q\rVert&#95;2. $$

This is the cheapest certificate constructor and the natural first score for support mining.

## Scheduled Escalation

1. Generate safe cube minors, canonicalize them under target symmetries, and reject those with fewer than $2\ell$ free coordinates.

2. Generate balanced coordinate partitions, then explore local coordinate swaps.

3. Alternately remove duplicate or opposite duplicate rows and columns. Repeat both directions because one removal can expose another.

4. Seed hard supports from the full deduplicated matrix, geometric top $k$ weight schedules, high-pressure trimming, clustered singular-vector leverage, pivoted QR, and farthest-Hamming diversity.

5. Construct the cheap exact spectral certificate for every seed.

6. Optimize continuous spectral weights and rationalize promising simplices with largest-remainder rounding.

7. Run the fixed-weight eigenvector-cut $\tau$ solver only on nodes near the target or among the best certified beam nodes.

8. Run one convex $p$ block or $q$ block optimization only as a final escalation. Change one block at a time, exactify it, and admit it only after exact $U$ improves.

9. Generate child supports by thresholding accepted rational weights. Cache canonical scope and support hashes.

This is heuristic mining, not branch and bound. Discarding a node never proves that its descendants are unhelpful.

## Proposal Gradients

For an exact weighted $\tau$ dual, a numerical multiplier matrix $\Lambda$ suggests block subgradients

$$ g&#95;i^p=\sum&#95;jq&#95;j\Lambda&#95;{ij},\qquad g&#95;j^q=\sum&#95;ip&#95;i\Lambda&#95;{ij}. $$

At a block optimum, active coordinates have equal minimal pressure. This is useful for proposing mass transfers, but the multipliers are not certificates.

For the spectral proxy, let $u,v$ be a top singular pair of $D&#95;pSD&#95;q$. At a differentiable point,

$$ \frac{\partial\lVert D&#95;pSD&#95;q\rVert&#95;2}{\partial p&#95;i}=\frac{\lVert D&#95;pSD&#95;q\rVert&#95;2u&#95;i^2}{p&#95;i}, $$

with the analogous expression for $q$. This suggests Lewis-weight-like equilibration. Repeated top singular values make one selected singular vector unstable, so use the full clustered top subspace or several deterministic perturbations.

## Pilot Evidence

On a $16\times16$ all-positive padding of an $8\times8$ Sylvester hard core:

- continuous weighted spectral optimization reached about $0.45255$ from four starts and placed about $0.733$ of the mass on the core rows and columns;

- exact support scans crossed below $1/2$ at support sizes $6,7,8$, with the full eight-point core attaining approximately $0.353553$;

- rounding weights to denominator $4096$ and exactifying a nonconverged inner solve produced $U=1022993453/2147483648<1/2$, which certifies sign-rank at least three;

- exact zero-supported core weights converged numerically in about $0.126$ seconds;

- one joint convex $p$ block followed by one $q$ block took about $20$ seconds and remained dense.

These results support hard-support and spectral search before alternating convex blocks.

## Failure Modes

- Top $k$ objective values are nonmonotone. Test a schedule rather than stopping after one support size.

- Softmax weights smear mass across duplicate rows and rarely become exactly sparse.

- Thresholding can delete a rare essential row or column.

- Pivoted QR optimizes volume or reconstruction, not sign-rank. It is only a seed heuristic.

- Exactification can erase a small numerical improvement.

- Changing $p$ and $q$ simultaneously loses the simple convex block guarantee.

- A failed or unfinished numerical solve is harmless only when its last iterate is independently repaired and verified.

- Zero weights rely on weak-sign closure followed by perturbation to a strict realization. The theorem and verifier must retain that step.

- Support and restriction mining can prove the existence of a hard core, never its absence.

## Literature Anchors

- [Forster, spectral sign-rank](https://doi.org/10.1016/S0022-0000(02)00019-3)

- [Linial, Mendelson, Schechtman, and Shraibman, factorization norms](https://www2.mta.ac.il/~adish/Pubs/Papers/complexity_matrices.pdf)

- [Cohen and Peng, Lewis weights](https://arxiv.org/abs/1412.0588)

- [Yang, Zhang, Jin, and Zhu, spectral subset selection](https://proceedings.mlr.press/v37/yanga15.html)

- [Krishnan and Mitchell, eigenvector-cut SDP approximation](https://optimization-online.org/2001/08/365/)

- [Hatami, Hatami, Pires, Tao, and Zhao, average margin and sign-rank](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2022.22)

## Recommended Next Implementation

Build a separate certified hard-core scheduler that reuses the exact verifier in `weighted_tau_partition_pilot.py`. Add the direct rational spectral constructor and support mining before any alternating block solves. Keep it outside the public estimator until benchmarks show that its certified gains justify the PSD cost.
