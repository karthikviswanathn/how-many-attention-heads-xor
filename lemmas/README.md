# Lemma Folders

The lemma proofs are grouped into five thematic folders. Numbering inside each
filename is preserved (it matches the order in [`../lemmas.md`](../lemmas.md), the
statement ledger). The folders follow the natural arc of the development, from the
structural core out to the current frontier.

| folder | files | theme |
|---|---|---|
| `01_foundations_and_normal_form` | 01–21, xor | Linear-fractional normal form, checkerboard one-head lower bound, threshold-degree bounds, symmetric & positive-projection sign-change theory, small-`n` exact classification, universal per-width determinant-span bounds, counting lower bound. |
| `02_complexity_measure_upper_bounds` | 22–39 | Restriction/junta/sign-rank invariances and upper bounds from classical complexity measures: DNF/CNF (width, volume, literal expansion, monotone), certificate covers, PTF sparsity, decision trees, Fourier support. |
| `03_function_families_and_affine_geometry` | 40–67 | Exact head complexity for named families (affine parity, inner product, equality, intersection / Hamming-distance / directed-defect profiles, two- and three-pair families) and affine geometry (level sets, slabs, two-point and clean supports, positive runs), plus depth-two-tree and hybrid exactness. |
| `04_recursions_and_cost_invariants` | 68–120 | Cofactor and one-bit branching recursions, decision lists / threshold votes / calibration, the cylinder-threshold cost (`ctc`) and affine-cylinder cost (`actc`) invariants and their cofactor interpolation, and the halfspace-intersection lower bound. |
| `05_positive_statistic_gates_and_grids` | 121–170 | The current frontier: one-bit gates over a positive statistic, multi-raw-slice and shared-statistic sandwiches, raw-mask gates, positive grids, Hamming-layer and multigrid profile bounds. |

The organizing spine across all folders is the sandwich

```
deg_±(f)  ≤  H*(f) = L_frac(f)  ≤  C_+(f)  ≤  M_+(f) − 1
```

with a parallel sparse-polynomial route `deg_± ≤ H* ≤ afs_± ≤ ptfsp`. Most lemmas
are machinery for one of these inequalities, or exactness results where a lower
bound (degree / checkerboard) meets an upper bound (sign-changes / construction).
