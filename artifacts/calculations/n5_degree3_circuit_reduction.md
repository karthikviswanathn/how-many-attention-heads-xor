# Five-Bit Degree-Three Circuit Reduction

## Statement

Let $s:\lbrace-1,1\rbrace^5\to\lbrace-1,1\rbrace$ be a sign table. Let $E$ be the $32\times16$ Fourier evaluation matrix whose columns are the characters of degree at most two.

Then $s$ has threshold degree at least three if and only if there is a signed circuit $\lambda$ of the row configuration of $E$ such that

$$ s(z)\lambda(z)>0 $$

on the support of $\lambda$.

Every such circuit has support size between $8$ and $17$. Consequently, every five-bit sign table of threshold degree at least three is a sign extension of a forced signed pattern on between $8$ and $17$ cube vertices.

> **Use for coverage.** Instead of enumerating all weak quadratic sign tables, enumerate signed quadratic circuits up to cube symmetry. For each circuit, labels on its support are forced and labels on the complementary $15$ to $24$ vertices are free. Exact degree three is obtained after removing the degree-four and degree-five extensions.

## Proof

Write

$$ \chi(z)=z_1z_2z_3z_4z_5. $$

The 16 characters of degree at least three are exactly $\chi$ times the 16 characters of degree at most two. Orthogonality of distinct Fourier characters gives

$$ E^{\top}\mathrm{diag}(\chi)E=0. $$

Both $E$ and $\mathrm{diag}(\chi)E$ have rank $16$. Hence

$$ \ker(E^{\top})=\mathrm{diag}(\chi)\mathrm{col}(E). $$

This is Gale self-duality of the quadratic Fourier configuration, with parity reorientation.

### Lemma 1. Weak quadratic covectors become dependencies

Suppose $s$ has threshold degree at least three. Put $t=s\chi$. The weak quadratic characterization gives a nonzero quadratic function $Q$ such that

$$ t(z)Q(z)\geq0 $$

on every cube vertex.

Choose an extreme ray of the weak-separator cone for $t$. Its zero set $Z$ has quadratic-feature rank $15$. Define

$$ \lambda(z)=\chi(z)Q(z). $$

Since $Q\in\mathrm{col}(E)$, Gale self-duality gives

$$ E^{\top}\lambda=0. $$

On the support $C$ of $\lambda$, the weak inequalities are strict, so

$$ \mathrm{sign}(\lambda(z))=\chi(z)\mathrm{sign}(Q(z))=s(z). $$

The dependence is minimal. Indeed, suppose a nonzero dependence $\mu$ were supported on a proper subset of $C$. Gale self-duality writes $\mu=\chi R$ for a quadratic function $R$. Then $R$ vanishes on $Z$ and on at least one additional vertex of $C$. The rows indexed by $Z$ have rank $15$, and every row outside $Z$ raises their rank to $16$. Thus $R=0$, a contradiction. Therefore $\lambda$ is a circuit.

### Lemma 2. Circuit extensions give weak quadratic separators

Conversely, let $\lambda$ be a circuit of the rows of $E$, and suppose $s$ agrees with its signs on its support. Gale self-duality gives a quadratic function

$$ Q=\chi\lambda. $$

For $t=s\chi$, one has

$$ t(z)Q(z)=s(z)\lambda(z)>0 $$

on the support of $\lambda$, while both sides vanish off the support. Thus $Q$ is a nonzero weak quadratic separator for $t$, so $s$ has threshold degree at least three.

### Lemma 3. Circuit support bounds

The row configuration has rank $16$, so every circuit has at most $17$ elements.

For the lower bound, let $\lambda$ be a nonzero dependence. Gale self-duality writes $\lambda=\chi Q$ for a nonzero quadratic function $Q$. Multiplication by $\chi$ does not change support.

We use the standard support bound: a nonzero multilinear polynomial of degree at most $d$ on the $n$-cube is nonzero on at least $2^{n-d}$ vertices. This follows by induction on $n$. Write $P(z)=P_0(z')+z_nP_1(z')$. If $P_1=0$, the support doubles between the two $z_n$ slices and induction applies to $P_0$. If $P_1\neq0$, then at every point where $P_1$ is nonzero at least one of $P_0+P_1$ and $P_0-P_1$ is nonzero; induction applied to the polynomial $P_1$ of degree at most $d-1$ gives the same bound.

Applying the bound with $n=5$ and $d=2$ gives

$$ \lvert\mathrm{supp}(\lambda)\rvert=\lvert\mathrm{supp}(Q)\rvert\geq2^{5-2}=8. $$

This proves the reduction and the support bounds. $\blacksquare$

## Consequence for a Three-Head Proof

A proof-level finite coverage can use signed-circuit orbits as its outer cases. There is one important symmetry distinction. The circuit configuration is invariant under every coordinate sign flip. Head complexity is visibly invariant under coordinate permutations and simultaneous complementation of all inputs, but not under an individual input complementation, since that can turn a commonly oriented denominator into one with mixed slope signs. Full cube symmetry may therefore classify circuit types, but every coordinate-flip coset must be restored before testing head coverage.

1. enumerate circuit supports and signs up to full cube symmetry, then expand the representatives under coordinate flips modulo coordinate permutations and simultaneous input complementation;

2. for each circuit, cover its sign extensions by admissible three-head denominator spaces;

3. discard extensions with a weak affine separator, since those have threshold degree at least four;

4. verify every retained space and coverage claim with exact arithmetic.

The archived exact degree-three examples exhibit circuit supports of sizes $8$ and $12$, so the reduction already captures both known hard families.
