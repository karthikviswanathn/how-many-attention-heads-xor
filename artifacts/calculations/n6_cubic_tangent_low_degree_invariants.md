# Six-Bit Cubic Tangent Map Has No Equations Through Degree Six

## Scope

Pass from the $0/1$ variables to Fourier variables $y_i=2x_i-1$. This is an invertible affine change of coefficient coordinates over $\mathbb{Q}$ and over $\mathbb{F}_{101}$. Work in the quotient $y_i^2=1$ on six variables. The cleared three-head map is

$$ \Phi = A_1 D_2 D_3 + A_2 D_1 D_3 + A_3 D_1 D_2, $$

where all six factors are affine. Its output has 42 coefficient coordinates, indexed by subsets of $\lbrace 1,\ldots,6\rbrace$ of size at most three.

The calculation below proves that the image of $\Phi$ has no nonzero homogeneous polynomial equation of coefficient degree two, three, four, five, or six over $\mathbb{F}_{101}$. Consequently, it has no nonzero rational equation of those degrees. This is only an algebraic statement. It does not rule out orientation-dependent inequalities or other semialgebraic obstructions.

## Character decomposition

The sign changes $y_i\mapsto -y_i$ preserve the tangent image and give each Fourier coefficient coordinate a label in $\mathbb{F}_2^6$. A coefficient monomial inherits the XOR of its coordinate labels. Since $101$ is odd, every equation splits into its 64 character components.

Coordinate permutations identify components whose character labels have the same Hamming weight. It is therefore enough to test one component of each weight from zero through six.

For every representative component, the verifier evaluates all coefficient monomials at deterministic tangent-map samples over $\mathbb{F}_{101}$ and computes the exact modular rank. Full column rank proves that no equation exists in that component.

## Exact ranks over the finite field

| Coefficient degree | Character weight | Monomials | Rank |
|---:|---:|---:|---:|
| 2 | 0 | 42 | 42 |
| 2 | 1 | 16 | 16 |
| 2 | 2 | 16 | 16 |
| 2 | 3 | 13 | 13 |
| 2 | 4 | 13 | 13 |
| 2 | 5 | 10 | 10 |
| 2 | 6 | 10 | 10 |
| 3 | 0 | 227 | 227 |
| 3 | 1 | 227 | 227 |
| 3 | 2 | 217 | 217 |
| 3 | 3 | 217 | 217 |
| 3 | 4 | 185 | 185 |
| 3 | 5 | 185 | 185 |
| 3 | 6 | 175 | 175 |
| 4 | 0 | 2758 | 2758 |
| 4 | 1 | 2392 | 2392 |
| 4 | 2 | 2392 | 2392 |
| 4 | 3 | 2301 | 2301 |
| 4 | 4 | 2301 | 2301 |
| 4 | 5 | 2210 | 2210 |
| 4 | 6 | 2210 | 2210 |

The modular elimination for degree four uses block Schur complements. Its floating matrix products are still exact: every input is an integer residue below 101, every inner dimension is at most 32, and every intermediate integer sum is below $2^{53}$. The script rounds only exactly represented integers before reducing modulo 101.

## Degree five representation-complete audit

A direct degree-five character block has about 21,000 coefficient monomials. The audit reduces each block further under its stabilizer

$$ G_k=S_k\times S_{6-k}, $$

where $k$ is the character weight. Since $101>6$, the stabilizer representations are semisimple. Every irreducible $G_k$-module is indexed by a pair of partitions $\lambda\vdash k$ and $\mu\vdash 6-k$.

For every such pair, the verifier chooses one of two detector spaces:

1. invariants under the Young subgroup of shape $\lambda$ or $\mu$;

2. sign-isotypic vectors under the Young subgroup of conjugate shape $\lambda^{\top}$ or $\mu^{\top}$.

Young's rule and sign twisting guarantee that the corresponding Specht module has a nonzero vector in the chosen detector space. Therefore, if the kernel contained any irreducible module, at least one detector evaluation matrix would lose rank.

The following table summarizes the exhaustive calculation. The number of tests is the number of irreducible pairs. Every detector matrix had full column rank over $\mathbb{F}_{101}$.

| Character weight | Degree-five monomials | Irreducible tests | Largest detector rank |
|---:|---:|---:|---:|
| 0 | 21845 | 11 | 2647 |
| 1 | 21845 | 7 | 4707 |
| 2 | 21573 | 10 | 3597 |
| 3 | 21573 | 9 | 6479 |
| 4 | 21048 | 10 | 3463 |
| 5 | 21048 | 7 | 4450 |
| 6 | 20776 | 11 | 2393 |

This covers all 65 stabilizer irreducible types, so there is no degree-five equation in any of the 64 character blocks.

The detector ranks use the same exact block elimination with block size 256. Each floating dot product is an integer sum of at most 256 products of residues below 101, so it is represented exactly in binary64 before reduction modulo 101. Orbit sums are also exact because every stabilizer has order at most 720.

## Degree six representation-complete audit

The same stabilizer decomposition has 65 irreducible types in degree six. Sixty types fit directly in the Young-subgroup detector. The five remaining mixed detector spaces are unnecessarily large, so the residual verifier applies a primitive Young symmetrizer instead.

For a standard tableau $T$, let

$$ c_T=\left(\sum_{r\in R_T}r\right)\left(\sum_{s\in C_T}\mathrm{sgn}(s)s\right). $$

Over $\mathbb{F}_{101}$, the image of $c_T$ on one copy of its Specht module is one-dimensional, and it vanishes on every other irreducible type. Thus its image on a stabilizer orbit has dimension equal to the multiplicity of the requested Specht module. If the equation kernel contained that type, its image under $c_T$ would be nonzero. Full rank on the projected multiplicity space therefore excludes the type.

The pure projections reduce the five residual tests as follows.

| Character weight | Irreducible pair | Pure multiplicity | Rank |
|---:|:---:|---:|---:|
| 1 | $(1)\times(3,1,1)$ | 8087 | 8087 |
| 2 | $(2)\times(2,2)$ | 7618 | 7618 |
| 3 | $(2,1)\times(2,1)$ | 18538 | 18538 |
| 4 | $(2,2)\times(2)$ | 7597 | 7597 |
| 5 | $(3,1,1)\times(1)$ | 7952 | 7952 |

As a check on the projector construction, the weight-three character block decomposes with

$$ \sum_{\lambda,\mu}\dim(S^\lambda)\dim(S^\mu)m_{\lambda,\mu}=167388, $$

exactly its full monomial count. Here $m_{\lambda,\mu}$ is the multiplicity returned by the pure projector.

The following table summarizes all 65 degree-six tests. Every direct or pure detector had full column rank.

| Character weight | Degree-six monomials | Irreducible tests | Largest detector rank |
|---:|---:|---:|---:|
| 0 | 172473 | 11 | 18376 |
| 1 | 168792 | 7 | 17526 |
| 2 | 168792 | 10 | 21731 |
| 3 | 167388 | 9 | 18538 |
| 4 | 167388 | 10 | 21898 |
| 5 | 165984 | 7 | 17130 |
| 6 | 165984 | 11 | 17130 |

The degree-six elimination uses block size 512. Every floating dot product is an integer sum of at most 512 products of residues below 101, so it remains exactly represented in binary64 before reduction modulo 101. This covers every stabilizer irreducible type and proves that no sextic equation occurs in any character block.

## Rational consequence

Suppose a rational equation of degree at most six vanished identically after substitution into $\Phi$. Clear denominators and divide by the coefficient gcd to obtain a primitive integer equation. Its reduction modulo 101 is nonzero and would vanish on every finite-field tangent sample, contradicting one of the full-rank calculations above.

The image is a cone because scaling all numerators scales $\Phi$. Thus an arbitrary polynomial equation splits into homogeneous equations. The first possible algebraic equation has coefficient degree at least seven.

## Reproduction

Run:

```shell
python artifacts/calculations/search_cubic_tangent_quartic_invariants.py --full-blocks --degree 2
python artifacts/calculations/search_cubic_tangent_quartic_invariants.py --full-blocks --degree 3
python artifacts/calculations/search_cubic_tangent_quartic_invariants.py --full-blocks --degree 4
```

Then run the representation-complete degree-five checks:

```shell
python artifacts/calculations/search_cubic_tangent_quintic_equations.py --complete-representations --weight 0
python artifacts/calculations/search_cubic_tangent_quintic_equations.py --complete-representations --weight 1
python artifacts/calculations/search_cubic_tangent_quintic_equations.py --complete-representations --weight 2
python artifacts/calculations/search_cubic_tangent_quintic_equations.py --complete-representations --weight 3
python artifacts/calculations/search_cubic_tangent_quintic_equations.py --complete-representations --weight 4
python artifacts/calculations/search_cubic_tangent_quintic_equations.py --complete-representations --weight 5
python artifacts/calculations/search_cubic_tangent_quintic_equations.py --complete-representations --weight 6
```

Finally, run the degree-six direct detectors up to size 24000 and the five pure residual tests:

```shell
for weight in 0 1 2 3 4 5 6; do python artifacts/calculations/search_cubic_tangent_quintic_equations.py --degree 6 --complete-representations --complete-maximum-orbits 24000 --weight "$weight"; done
for weight in 1 2 3 4 5; do python artifacts/calculations/verify_n6_cubic_tangent_sextic_residual.py --weight "$weight"; done
```
