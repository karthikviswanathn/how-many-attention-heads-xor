# Support-Seventeen Affine-Extension Dichotomy

## Statement

Among the $46975$ support-seventeen circuit orbits under the input symmetries that preserve head complexity:

- $23859$ circuit families contain an extension of threshold degree at least four;

- $23116$ circuit families consist entirely of exact threshold-degree-three extensions.

This is an exhaustive exact classification.

## Partial affine criterion

Let $C$ be the support of a signed quadratic circuit $\lambda$, and let the target signs be forced by

$$ s(z)=\mathrm{sign}(\lambda(z)) \qquad\text{for }z\in C. $$

Put $\chi(z)=z_1z_2z_3z_4z_5$ and $t=s\chi$ on $C$.

**Lemma.** The circuit family has an extension of threshold degree at least four if and only if there is a nonzero affine form $L$ such that

$$ t(z)L(z)\geq0 \qquad\text{for every }z\in C. $$

**Proof.** If a full extension has threshold degree at least four, the five-bit high-degree reduction supplies a nonzero affine form weakly aligned with its parity twist on all $32$ vertices, hence on $C$.

Conversely, suppose such an $L$ exists on $C$. On every vertex outside $C$ where $L$ is nonzero, choose the free sign of $t$ to agree with $L$. Choose arbitrary signs where $L$ vanishes. The resulting full parity twist satisfies $tL\geq0$ everywhere, so the corresponding extension has threshold degree at least four. $\blacksquare$

Every circuit extension already has threshold degree at least three. Therefore the failure of the partial affine criterion is equivalent to every extension having threshold degree exactly three.

## Exact finite test

For fixed partial signs, the affine separators form a pointed polyhedral cone in $\mathbb{R}^6$. If the cone is nonzero, it has an extreme ray whose active cube rows have rank five. Consequently, it is enough to test the exact list of primitive affine normals obtained from five independent cube vertices.

There are $3254$ such normals up to sign. Each normal is represented by two $32$-bit masks for its positive and negative cube vertices. For a circuit partial twist, one pair of bitwise mismatch tests decides whether that normal or its negative is weakly aligned on the support. Exhaustively testing all $46975$ circuit orbits gives the stated split:

$$ 46975=23859+23116. $$

The [classifier](classify_n5_support17_affine_extensions.py) regenerates the $3254$ normals with exact determinant arithmetic, checks an explicit normal witness for every affine-extendible family, and certifies nonextendibility by exhaustion for every remaining family. The compact archive is [`n5_support17_affine_dichotomy.npz`](n5_support17_affine_dichotomy.npz), keyed by [`n5_support17_head_orbit_codes.tsv`](n5_support17_head_orbit_codes.tsv).

## Consequence for Three-Head Shattering

A fixed three-head score space has dimension at most $16$. Shattering a support-seventeen circuit family requires rank $15$ on the free complement and a one-dimensional kernel score with the forced circuit signs.

The $23859$ affine-extendible families cannot satisfy this criterion, since they contain functions with threshold degree at least four. The only possible whole-family shattering cases are the $23116$ exact-degree-three-only families. Thus the affine dichotomy removes slightly more than half of the exhaustive support-seventeen list before any denominator search.
