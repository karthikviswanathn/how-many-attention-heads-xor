# Affine Weak-Dual Reduction on the Repaired Support

## Setup

Let $S_{56}$ be the antipodally symmetric repaired support from [n6_parity_triple_repaired_degree4_relations.md](n6_parity_triple_repaired_degree4_relations.md). Its omitted set is

$$ K=\lbrace6,9,21,27,36,42,54,57\rbrace. $$

The target agrees with six-bit parity on $S_{56}$ except at vertices $38$ and $41$.

Define the affine weight

$$ Q(z)=2+z_5-z_4. $$

In bit coordinates this is twice $x_4+(1-x_5)$. Hence $Q$ is nonnegative on the full cube, is not identically zero, and vanishes on the face $x_4=0$, $x_5=1$. In particular,

$$ Q(38)=Q(41)=0. $$

## Exact reduction

Let $p(z)=\prod_{i=0}^5z_i$ be parity, let $s$ be the target sign, and let $T$ be any polynomial of degree at most four. Since $Q$ is affine, $QT$ has degree at most five. Fourier orthogonality gives

$$ \sum_{z\in\lbrace-1,1\rbrace^6}p(z)Q(z)T(z)=0. $$

The two target disagreements retained by $S_{56}$ have zero $Q$-weight. Therefore

$$ \sum_{z\in S_{56}}s(z)Q(z)T(z)=-\sum_{z\in K}p(z)Q(z)T(z). $$

Moreover, $Q$ vanishes at omitted vertices $36$ and $42$. The residual is supported on only six vertices:

$$ \lbrace6,9,21,27,54,57\rbrace. $$

Because $Q$ has degree one, its values on $S_{56}$ satisfy both degree-four evaluation relations automatically.

## Interpretation

For every cleared four-head tangent polynomial $T$, the nonnegative multiplier $Q$ reduces the desired Gordan identity to cancellation of the displayed six-point omitted residual. If that residual could be cancelled by another nonnegative repaired-support multiplier, it would give a universal weak dual.

The present identity does not supply that cancellation. It is an exact reduction, not a completed four-head lower bound.

## Verification

Run:

```bash
python3 artifacts/calculations/verify_n6_parity_triple_affine_weak_dual_reduction.py
```

The verifier checks nonnegativity, the two exceptional zeros, both repaired-support relations, and the moment identity on every Fourier monomial of degree at most four.
