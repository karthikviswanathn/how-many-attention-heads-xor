# Five-Bit Degree-Three and Degree-Four Audit

## Status

The degree-four class is now closed exactly:

$$ \deg_{\pm}(f)=4 \qquad\Longrightarrow\qquad H^{\ast}(f)=4 $$

for every five-bit function. Exactly $4475538$ five-bit functions have threshold degree four. They are parity twists of nonconstant weak affine sign extensions. The [degree-four reduction verifier](verify_n5_degree4_reduction.py) enumerates this class exactly, and the shattering and residual archives give exact four-head certificates for all of it.

The degree-three class remains open. The exact signed-circuit reduction in [n5_degree3_circuit_reduction.md](n5_degree3_circuit_reduction.md) is the current finite starting point.

## Weak affine characterization of degree four

Work on the sign cube. Let $s:\lbrace-1,1\rbrace^5\to\lbrace-1,1\rbrace$ be the target sign table, and put

$$ \chi(z)=z_1z_2z_3z_4z_5, \qquad t(z)=s(z)\chi(z). $$

Let $V_3$ be the space spanned by the Fourier characters of degree at most three. Its orthogonal complement is

$$ V_3^{\perp}=\mathrm{span}\left\lbrace\chi,\chi z_1,\chi z_2,\chi z_3,\chi z_4,\chi z_5\right\rbrace. $$

**Lemma.** The sign table $s$ has threshold degree at least four if and only if there is a nonzero affine form

$$ L(z)=a_0+\sum_{i=1}^{5}a_i z_i $$

such that

$$ t(z)L(z)\geq0 \qquad\text{for every }z\in\lbrace-1,1\rbrace^5. $$

**Proof.** By Gordan's alternative, no vector in $V_3$ strictly sign-represents $s$ exactly when there is a nonzero vector of weights $\lambda(z)\geq0$ such that

$$ \sum_z\lambda(z)s(z)\varphi(z)=0 $$

for every Fourier character $\varphi$ of degree at most three. Equivalently, the function $u(z)=\lambda(z)s(z)$ belongs to $V_3^{\perp}$. Every such function has the form

$$ u(z)=\chi(z)L(z) $$

for an affine $L$. The identity $\lambda(z)=s(z)u(z)=t(z)L(z)$ converts nonnegativity of the weights into the displayed weak affine inequalities. The argument reverses verbatim. $\blacksquare$

The top-degree theorem says that only parity and its complement have threshold degree five. Therefore $s$ has threshold degree exactly four if and only if the weak affine condition holds and $t$ is not constant.

## Exact finite enumeration

Fix a weak sign table $t$, and consider its separator cone

$$ \mathcal{A}_t=\left\lbrace a\in\mathbb{R}^6:t(z)\langle(1,z),a\rangle\geq0\text{ for every }z\right\rbrace. $$

If this cone contains a nonzero vector, it is pointed because the $32$ affine feature vectors span $\mathbb{R}^6$. Hence it has an extreme ray. At an extreme ray, the active cube constraints have rank five. The separator therefore vanishes on five affinely independent cube vertices.

It follows that every weak affine sign table is an arbitrary sign extension of the covector of an affine hyperplane through five independent vertices. Conversely, every such extension is weakly separated by the defining affine form.

The verifier enumerates all $\binom{32}{5}=201376$ five-vertex subsets. Exact generalized cross products give $3254$ primitive affine normals up to sign. Their zero-set distribution is

$$ \begin{array}{c|rrrrrr} \text{zero-set size} & 5 & 7 & 8 & 10 & 12 & 16 \\ \hline \text{number of normals} & 2112 & 480 & 480 & 32 & 120 & 30. \end{array} $$

Coordinate permutations, global input complementation $z\mapsto-z$, and normal sign reduce these $3254$ normals to only $65$ orbits. The orbit distribution is

$$ \begin{array}{c|rrrrrr} \text{zero-set size} & 5 & 7 & 8 & 10 & 12 & 16 \\ \hline \text{number of orbits} & 31 & 11 & 12 & 3 & 5 & 3. \end{array} $$

Assigning arbitrary signs on every zero set and deduplicating gives

$$ 4475540 $$

weak affine sign extensions. Two are the constant sign tables, which twist back to parity and its complement. Thus the exact number of five-bit degree-four functions is

$$ 4475540-2=4475538. $$

All determinant arithmetic in the verifier is exact modulo $127$. Hadamard's bound puts every relevant integer determinant strictly between $-56$ and $56$, so its residue modulo $127$ determines it uniquely.

## Exact four-head coverage

For a fixed normal with zero set $Z$, labels away from $Z$ are forced while labels on $Z$ are arbitrary. A fixed four-head score space covers the whole family when its restriction to $Z$ is surjective and its kernel on $Z$ contains a score with the forced signs away from $Z$. The exact shattering archive verifies this criterion for $60$ of the $65$ normal orbits.

The five residual orbit indices are

$$ 8, \qquad 44, \qquad 62, \qquad 63, \qquad 64. $$

Finite exact archives cover all of their extensions. Their target counts are respectively

$$ 32, \qquad 256, \qquad 65535, \qquad 65536, \qquad 65536. $$

The orbit $62$ count excludes the one extension that twists back to parity. The exact verifiers are [verify_n5_degree4_other_residuals.py](verify_n5_degree4_other_residuals.py) and [classify_n5_degree4_face_family.py](classify_n5_degree4_face_family.py).

## Why the fixed-span theorem does not close degree three

The current exact results cover threshold degrees zero, one, two, four, and five. Constants and nonconstant LTFs have head complexity zero and one, every degree-two table has head complexity two, every degree-four table has head complexity four, and the parity pair has head complexity five.

For degree three, the archived sample verifier gives exact certificates for two examples, while the signed-circuit program is building the full classification.

The fixed-denominator span schema cannot give matching universal bounds at these parameters. Its score space has dimension at most $1+5H$, whereas

$$ \dim V_{5,3}=26>16=1+5\cdot3. $$

Thus a matching degree-three theorem must use denominators that depend on the sign cell, a nonlinear structural construction, or a finite collection of denominator dictionaries. The completed degree-four proof does exactly this through family shattering and finite residual coverage.

The exact four-bit classification also does not lift automatically. Such a lift would require the still-open sharp one-bit recursion, especially for fresh-bit XOR and XNOR. The available cofactor and sparse-polynomial recursions generally exceed three or four heads.

## Degree-three remainder

There is a parallel dual statement, but it is less restrictive. Multiplication by $\chi$ sends Fourier levels zero, one, and two to levels five, four, and three. Therefore a five-bit sign table has threshold degree at least three exactly when its parity twist $t=s\chi$ has a nonzero weak quadratic separator. Equivalently, there is a nonzero quadratic polynomial $Q$ such that

$$ t(z)Q(z)\geq0 \qquad\text{for every }z. $$

The quadratic separator space has dimension $16$, rather than the six-dimensional affine space above. Gale self-duality converts its extreme rays into signed circuits of the quadratic Fourier evaluation configuration. Every circuit has support between $8$ and $17$, but the exact orbit enumeration is much larger than the affine-normal enumeration.

Consequently, closing all five-bit functions requires one remaining result: three heads for every exact degree-three cell.
