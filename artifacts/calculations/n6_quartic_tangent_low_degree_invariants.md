# Six-Bit Quartic Tangent Map Has No Equations Through Degree Four

## Scope

Work in Fourier coordinates with $z_i^2=1$. The cleared four-head tangent map is

$$ \Phi(B,A)=\sum_{h=0}^3A_h\prod_{j\neq h}B_j, $$

where all eight factors are affine in six variables. Its output has 57 coefficient coordinates, indexed by subsets of $\lbrace0,\ldots,5\rbrace$ of size at most four.

## Exact image dimension

The parameter space has dimension 56. There are seven universal infinitesimal gauges:

- four denominator scalings, each compensated in the other three numerators;

- three numerator syzygies of the form $A_0\mapsto A_0+tB_0$ and $A_h\mapsto A_h-tB_h$.

Thus the image dimension is at most $49$.

The verifier evaluates the Jacobian at an integer point whose four denominators have positive slopes and intercept strictly larger than the slope sum. Modulo $1000003$, the Jacobian has rank $49$, the seven gauge vectors have rank $7$, and the Jacobian kills every gauge vector. Therefore the affine Zariski closure of the tangent image has dimension exactly $49$ and codimension $8$ in the quartic coefficient space.

The image nevertheless spans all 57 coefficient coordinates linearly. A deterministic 100-sample matrix has rank $57$ over $\mathbb F_{101}$.

## Character decomposition

Coordinate sign changes split every homogeneous coefficient equation into $64$ character blocks. Coordinate permutations identify blocks whose characters have the same Hamming weight. It is enough to test one character of each weight from zero through six.

For every representative block in coefficient degrees two, three, and four, the search evaluates all coefficient monomials at deterministic tangent samples over $\mathbb F_{101}$. The exact modular ranks are:

| Coefficient degree | Character weight | Monomials | Rank |
|---:|---:|---:|---:|
| 2 | 0 | 57 | 57 |
| 2 | 1 | 26 | 26 |
| 2 | 2 | 26 | 26 |
| 2 | 3 | 25 | 25 |
| 2 | 4 | 25 | 25 |
| 2 | 5 | 25 | 25 |
| 2 | 6 | 25 | 25 |
| 3 | 0 | 512 | 512 |
| 3 | 1 | 512 | 512 |
| 3 | 2 | 512 | 512 |
| 3 | 3 | 511 | 511 |
| 3 | 4 | 511 | 511 |
| 3 | 5 | 480 | 480 |
| 3 | 6 | 480 | 480 |
| 4 | 0 | 8128 | 8128 |
| 4 | 1 | 7632 | 7632 |
| 4 | 2 | 7632 | 7632 |
| 4 | 3 | 7601 | 7601 |
| 4 | 4 | 7601 | 7601 |
| 4 | 5 | 7600 | 7600 |
| 4 | 6 | 7600 | 7600 |

The degree-four elimination uses block Schur complements. Each floating matrix product has inner dimension at most $128$ and integer entries below $101$, so every intermediate dot product is exactly represented in binary64 before reduction modulo $101$.

## Consequence

The tangent image is a cone because scaling all numerators scales $\Phi$. Hence every polynomial equation splits into homogeneous equations. Full column rank in every block proves that the image has no nonzero equation over $\mathbb F_{101}$ through coefficient degree four.

If a rational equation of these degrees existed, clearing denominators and dividing by the coefficient gcd would give a primitive integer equation. Its nonzero reduction modulo $101$ would contradict one of the full-rank calculations. Thus the first possible rational algebraic invariant has coefficient degree at least five.

This rules out a low-degree algebraic separation route for the parity-triple candidate. It does not rule out higher-degree equations or orientation-dependent semialgebraic inequalities.

## Quintic symmetric diagnostic

The first possible equation degree is five. A full character block then has about $93000$ coefficient monomials, so the current diagnostic tests the invariant subspace under the character stabilizer $S_k\times S_{6-k}$ rather than every irreducible type.

| Character weight | Quintic monomials | Stabilizer orbit sums | Rank |
|---:|---:|---:|---:|
| 0 | 93031 | 424 | 424 |
| 1 | 93030 | 1609 | 1609 |
| 2 | 93030 | 3346 | 3346 |
| 3 | 92999 | 4131 | 4131 |
| 4 | 92999 | 3334 | 3334 |
| 5 | 92503 | 1574 | 1574 |
| 6 | 92503 | 401 | 401 |

Thus no stabilizer-invariant quintic equation exists. This is not a representation-complete quintic audit. An equation could still transform in a nontrivial stabilizer representation.

## Verification

Run:

```bash
python3 artifacts/calculations/verify_n6_quartic_tangent_dimension.py
python3 artifacts/calculations/search_n6_quartic_tangent_invariants.py --degree 2
python3 artifacts/calculations/search_n6_quartic_tangent_invariants.py --degree 3
```

For coefficient degree four, run one character block at a time:

```bash
python3 artifacts/calculations/search_n6_quartic_tangent_invariants.py --degree 4 --weight 0 --block-size 128
```

Repeat the last command with weights $1$ through $6$.

The quintic symmetric diagnostic is:

```bash
python3 artifacts/calculations/search_n6_quartic_tangent_invariants.py --degree 5 --weight 0 --orbit-sums --block-size 128
```

Again repeat with weights $1$ through $6$.
