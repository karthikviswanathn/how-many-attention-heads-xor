# Exact Rational Signed-Secant McCormick Leaves

## Outcome

The first model-native parameter-cell lower certificate now has an executable exact checker and discovery path. The implementation is `src/hstar/signed_secant_mccormick.py`. It reconstructs the signed-secant factor graph from the truth table, orientation branch, normalized chart, rational cell, and probability vector. It then verifies a rational linear-program dual identity coefficient by coefficient. A sparse HiGHS pass can propose the probability support and dual support, but only successful rational reconstruction changes the proof state.

The checker does not trust a solver matrix, declared bounds for derived nodes, a floating optimum, or the claimed dual value. The first archived leaf is `artifacts/calculations/signed_secant_mccormick_leaf_xor1.json`, with independent checks in `artifacts/calculations/verify_signed_secant_mccormick_leaf.py`.

The implementation also verifies binary rational subdivision trees. One archived tree covers a proper one-bit chart subcell. A second archive covers one full two-head chart of the exact eight-bit separation. Neither is a global lower bound because the remaining charts are not covered.

## Soundness Principle

Fix a signed-secant chart cell $C$ and rational weights $\lambda&#95;x>0$ with $\sum&#95;x\lambda&#95;x=1$. Let

$$ \Phi(z)=\sum&#95;x\lambda&#95;x y&#95;x\widetilde{\mathcal S}&#95;x(z). $$

If every signed quotient were strictly positive at one point, then $\Phi$ would be strictly positive there. It is therefore enough to certify

$$ \sup&#95;{z\in C}\Phi(z)\leq0. $$

The factorable McCormick relaxation is an outer approximation of the exact graph on $C$. Write its inequalities as $A&#95;i u\leq b&#95;i$, its equalities as $E&#95;j u=f&#95;j$, and its linear objective as $c^{\top}u+c&#95;0$. A rational dual leaf stores multipliers $\alpha&#95;i\geq0$ and unrestricted $\beta&#95;j$ satisfying

$$ c=\sum&#95;i\alpha&#95;iA&#95;i+\sum&#95;j\beta&#95;jE&#95;j. $$

Every relaxed feasible point then satisfies

$$ c^{\top}u+c&#95;0\leq c&#95;0+\sum&#95;i\alpha&#95;ib&#95;i+\sum&#95;j\beta&#95;jf&#95;j. $$

The checker recomputes the right side exactly and accepts the leaf only when it equals the archived claimed value and is nonpositive. Since the relaxation contains the exact graph, this excludes strict signed-secant feasibility throughout the cell.

## Reconstructed Factor Graph

The base variables are the simplex coordinates $\theta&#95;{hi}$, normalized directions $v&#95;{hi}$, scalar direction $a$, and ray length $t$. The checker enforces

$$ \sum&#95;i\theta&#95;{hi}=1,\qquad \sum&#95;iv&#95;{hi}=0,\qquad 0\leq\theta&#95;{hi}\leq1,\qquad -1\leq v&#95;{hi}\leq1,\qquad -1\leq a\leq1,\qquad 0\leq t\leq1. $$

One chart coordinate is fixed to $1$ or $-1$. The cell may further subdivide every base interval.

The shared product lift is $z&#95;{hi}=tv&#95;{hi}$. The checker generates all four rational McCormick inequalities for every product. For $w=uv$, $u\in[\ell&#95;u,r&#95;u]$, and $v\in[\ell&#95;v,r&#95;v]$, these are

$$ \begin{aligned} w &\geq \ell&#95;u v+\ell&#95;v u-\ell&#95;u\ell&#95;v, & w &\geq r&#95;u v+r&#95;v u-r&#95;ur&#95;v, \\ w &\leq r&#95;u v+\ell&#95;v u-r&#95;u\ell&#95;v, & w &\leq \ell&#95;u v+r&#95;v u-\ell&#95;ur&#95;v. \end{aligned} $$

Every derived affine interval is recomputed by exact interval arithmetic. Every product interval is recomputed from the four endpoint products. No derived interval supplied by a search process is accepted as input.

The exact RLT identity $\sum&#95;i z&#95;{hi}=0$ is added for every head. Coordinatewise endpoint constraints enforce $0\leq\theta&#95;{hi}+z&#95;{hi}\leq1$.

For each active truth-table vertex, the checker builds

$$ b&#95;h=B&#95;h(x;\theta&#95;h),\qquad d&#95;h=B&#95;h(x;v&#95;h),\qquad c&#95;h=B&#95;h(x;\theta&#95;h+z&#95;h). $$

It then reconstructs the prefix recurrence

$$ P&#95;0=1,\qquad R&#95;0=0,\qquad P&#95;h=P&#95;{h-1}b&#95;h,\qquad R&#95;h=R&#95;{h-1}c&#95;h+P&#95;{h-1}d&#95;h. $$

A separate endpoint product $C&#95;H=\prod&#95;h c&#95;h$ is built, and the redundant exact identity

$$ C&#95;H=P&#95;H+tR&#95;H $$

is added as an RLT equality. Finally, the weighted objective uses

$$ \widetilde{\mathcal S}&#95;x=\frac12\left(R&#95;H+aC&#95;H+aP&#95;H\right). $$

## Certificate Schema

The stored leaf contains:

- the schema version, certificate type, dimension, vertex order, and truth mask;

- the ordered head orientations and head count;

- one normalized chart coordinate;

- rational boxes for $\theta$, $v$, $a$, and $t$;

- a sparse rational probability vector on truth-table vertices;

- nonzero rational multipliers indexed by reconstructed inequality and equality names;

- the claimed rational upper bound.

The verifier rejects malformed charts, cells outside the normalized domain, invalid probability weights, unknown constraint names, negative inequality multipliers, stationarity mismatches, incorrect claimed values, and positive dual bounds.

## First Exact Leaf

The first certificate uses the one-bit function with mask `0x2`, one positive orientation, and the chart $a=1$. Its cell has

$$ 0\leq v&#95;0\leq1,\qquad -1\leq v&#95;1\leq0. $$

The tangent equality gives $v&#95;0+v&#95;1=0$. The probability vector is a point mass at the negative vertex $x=0$. In this cell, the three terminal factor-graph nodes $R&#95;1$, $aC&#95;1$, and $aP&#95;1$ all have verified lower bound zero. The signed objective has coefficient $-1/2$ on each node. Three multipliers of value $1/2$ on their reconstructed lower-bound inequalities therefore give exact upper bound zero.

The checker reports $23$ variables, $9$ product nodes, $8$ affine nodes, $86$ inequalities, and $12$ equalities. It also rejects deliberate corruptions of the chart, truth table, multiplier sign, and dual stationarity identity.

The discovery routine starts from both one-bit vertices. Its floating common-margin dual chooses the point mass at $x=0$. A second LP on that support reconstructs an exact rational dual at denominator limit $16$, and the independent checker accepts exact upper bound zero.

## Subdivision and Eight-Bit Full Chart

The cover format is a binary tree. Each internal node identifies one base coordinate and a rational pivot strictly inside its current interval. The checker derives the left and right child boxes itself, so their union is exact. Each leaf stores only a rational probability vector and rational dual multipliers. It cannot replace its derived cell with a different box.

The archive `artifacts/calculations/signed_secant_subcell_cover_xor1.json` splits the first pilot cell at $v&#95;0=1/2$. Its two leaves have exact upper bounds zero and $-1/4$. The checker reports a valid three-node, two-leaf cover of the declared subcell, while explicitly returning `chart_infeasible: false`.

The archive `artifacts/calculations/f8_h2_pp_scalar_plus_chart_cover.json` is stronger. It covers the full $a=1$ normalized chart for the two-positive-orientation branch of the eight-bit Hamming-threshold function. A point mass at vertex $255$ and a five-term exact dual give upper bound $-1$. The cover checker returns `chart_infeasible: true` but still returns `global_head_lower_bound: false`, since one chart is not all charts.

The full-cube discovery LP for this chart used $6200$ variables, $23772$ inequalities, $3590$ equalities, and $2834$ product nodes. Sparse matrix assembly kept the run near $0.3$ seconds on the development machine. After support reduction, the portable leaf itself has only $80$ variables, $312$ inequalities, $20$ equalities, and $29$ products.

## Initial Benchmark

The executable benchmark is `artifacts/calculations/benchmark_signed_secant_mccormick.py`.

| Problem | Root charts tested | Exact full-chart leaves | Positive outer relaxations |
| --- | ---: | ---: | ---: |
| Two-bit XOR at one head | $16$ raw charts | $8$ | $8$ |
| Eight-bit exact separation at two heads | $6$ scalar charts | $2$ | $4$ |
| Six-bit parity triple flip at four heads | $10$ scalar charts | $2$ | $8$ |

A positive relaxation is unresolved. It is not a signed secant and gives no upper or lower bound.

Simplex-aware interval propagation is essential. [Theorem 197](../../lemmas/02_complexity_measure_upper_bounds/197_box_sum_greedy_affine_bounds.md) derives exact box-plus-sum bounds for $b&#95;h$, $d&#95;h$, and the shared $z$ lift by a fractional-knapsack rule, and the checker enforces $0\leq b&#95;h,c&#95;h\leq1$. Without these bounds, even the two exact eight-bit scalar charts appeared spuriously positive.

Verification:

```bash
PYTHONPATH=src python3 artifacts/calculations/verify_signed_secant_mccormick_leaf.py
PYTHONPATH=src python3 artifacts/calculations/verify_signed_secant_cell_cover.py
PYTHONPATH=src python3 artifacts/calculations/benchmark_signed_secant_mccormick.py
PYTHONPATH=src python3 -m hstar.certified_cli verify --dimension 1 --mask 0x2 --certificate artifacts/calculations/signed_secant_mccormick_leaf_xor1.json
PYTHONPATH=src python3 -m hstar.certified_cli verify --dimension 8 --mask 0x177f2bbf4ddf8eef71f7b2fbd4fde8fe7f17bf2bdf4def8ef771fbb2fdd4fee8 --certificate artifacts/calculations/f8_h2_pp_scalar_plus_chart_cover.json
```

## Scaling

The shared lift uses $H(n+1)$ product nodes. With $m$ active truth-table vertices, the current recurrence uses $4H+3$ product nodes per vertex. The total product-node count is therefore

$$ H(n+1)+m(4H+3), $$

which is linear in $Hn+Hm$. Every product contributes four envelope inequalities plus exact propagated bounds. The full truth table is required only for final coverage and truth-mask verification; an individual dual leaf may use a sparse active support.

The useful proof object is the rational dual support, not the size of the floating LP solution. Small supports can be mined numerically and then reconstructed exactly.

## Remaining Work

1. Add exact basis reconstruction when bounded-denominator rounding of a degenerate floating dual fails.

2. Add automatic split selection, chart symmetry, and global cover manifests. A lower bound requires every cell in every chart of every orientation-count branch to be covered.

3. Compare the current prefix relaxation with stronger RLT identities, Bernstein bounds, and low-degree Handelman certificates on the same cells.

4. Add active-vertex generation. The current full-cube sparse LP is practical on the first eight-bit chart, but larger truth tables need a separation loop. The final cover checker must still protect the full cube.

5. Project zero-bound residual cells back to the lower-degree retained-scalar formulation before invoking NLSAT, CAD, or Positivstellensatz methods.

6. Benchmark whether exact leaves close robust regions for parity, equality, random functions, the six-bit parity perturbation, and the eight-bit exact example.
