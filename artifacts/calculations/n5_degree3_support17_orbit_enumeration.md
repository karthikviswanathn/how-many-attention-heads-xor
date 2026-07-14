# Five-Bit Support-Seventeen Circuit Enumeration

## Result

The five-bit quadratic Fourier configuration has

$$ 10621088 $$

support-seventeen circuits up to global circuit sign. They form

$$ 3160 $$

orbits under all coordinate permutations and coordinate sign flips. Under the smaller input symmetry group that visibly preserves head complexity, coordinate permutations and simultaneous complementation of all five inputs, they form

$$ 46975 $$

orbits.

This is an exhaustive enumeration, not a sample.

## Exact reduction to fifteen-vertex hyperplanes

Let $E$ be the $32\times16$ quadratic Fourier evaluation matrix. By parity-reoriented Gale self-duality, a support-seventeen circuit is equivalent to a nonzero quadratic function whose zero set $Z$ has exactly $15$ vertices and feature rank $15$.

Equivalently,

$$ \mathrm{rank}(E_Z)=15 $$

and every one of the other $17$ rows raises the rank to $16$. Thus it suffices to enumerate the $15$-vertex subsets of the cube and test their exact matroid closure.

The full cube automorphism group has order $2^5\cdot5!=3840$. Orbit marking reduces all

$$ \binom{32}{15}=565722720 $$

subsets to $158658$ representatives. Of these, $120395$ have rank $15$, and $3160$ have closure exactly equal to the chosen $15$ vertices.

## Why the modular calculation is exact

The enumerator uses the prime

$$ p=4294967311. $$

Every entry of $E$ is $-1$ or $1$. Hadamard's bound gives

$$ \lvert\det(M_{15})\rvert\leq15^{15/2}<661735514<p $$

for every $15\times15$ minor, and

$$ \lvert\det(M_{16})\rvert\leq16^8=4294967296<p $$

for every $16\times16$ minor. Therefore a relevant determinant is zero over the integers if and only if it is zero modulo $p$. The modular rank and closure tests are exact.

For every accepted orbit representative, one exact $15\times15$ Bareiss determinant fixes the scale of its modular null vector. The Hadamard bounds then recover all integer cofactors and every circuit sign without ambiguity. The program independently checks the split into head-symmetry orbits in two ways: once from signed circuit codes and once from zero-set codes.

## Orbit distributions

The $3160$ full-cube orbits have the following orbit sizes:

$$ \begin{array}{c|rrrrrrrrr} \text{orbit size} & 32 & 160 & 320 & 384 & 480 & 640 & 960 & 1920 & 3840 \\ \hline \text{number} & 2 & 3 & 11 & 1 & 6 & 27 & 32 & 653 & 2425. \end{array} $$

Splitting each full-cube orbit under the index-sixteen head-symmetry subgroup gives:

$$ \begin{array}{c|rrrrrrrrr} \text{head orbits in one full orbit} & 3 & 4 & 5 & 6 & 8 & 9 & 10 & 12 & 16 \\ \hline \text{number of full orbits} & 2 & 1 & 3 & 17 & 27 & 32 & 146 & 507 & 2425. \end{array} $$

The orbit-size distribution sums to $10621088$ circuits, and the split distribution sums to $46975$ head-symmetry orbits.

## Reproduction

The exact enumerator is [`enumerate_n5_support17_circuit_orbits.cpp`](enumerate_n5_support17_circuit_orbits.cpp). Its final output is:

```text
prime: 4294967311
15-by-15 Hadamard bound: 661735514
16-by-16 Hadamard bound: 4294967296
15-subsets scanned: 565722720
full-cube 15-subset orbits: 158658
rank-15 full-cube orbits: 120395
support-17 full-cube circuit orbits: 3160
support-17 circuits up to global sign: 10621088
support-17 head-symmetry circuit orbits: 46975
representative-mask checksum: 266317633688
full orbit-size distribution: 32:2 160:3 320:11 384:1 480:6 640:27 960:32 1920:653 3840:2425
head split distribution: 3:2 4:1 5:3 6:17 8:27 9:32 10:146 12:507 16:2425
```

## Consequence for Three-Head Coverage

The exhaustive count shows that support seventeen is itself too large for a hand case split. A fixed three-head score space can shatter a full circuit-extension family only at support seventeen, but there are $46975$ valid-symmetry circuit families of this size. The [exact affine-extension dichotomy](n5_degree3_support17_affine_dichotomy.md) removes $23859$ families that contain higher-degree extensions and leaves $23116$ exact-degree-three-only families for tangent-factorization coverage.
