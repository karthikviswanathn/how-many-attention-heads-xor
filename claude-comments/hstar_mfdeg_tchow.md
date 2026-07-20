# Head Complexity Equals the Admissible Cleared-Denominator Invariant, and Provably Not the Unrestricted One

Date: 2026-07-20. Assembled by Claude (Fable 5) from the Snellius autoresearch ledger
(fetched locally as git ref `snellius/autoresearch`), with the strictness counterexample
from `claude-comments/tchow_certificates/`.

**Summary.** The identity that holds is $H^{\ast}(f)=\mathrm{MFdeg} _{\pm}(f)$, where the
affine pairs are required to be admissible attention atoms. Dropping admissibility yields
the unrestricted tangential invariant $\mathrm{tChow} _{\pm}(f)$, and the correct general
statement there is only the sandwich $\deg _{\pm}(f)\leq\mathrm{tChow} _{\pm}(f)\leq H^{\ast}(f)$.
The equality $H^{\ast}=\mathrm{tChow} _{\pm}$ is **false**: the lemma 189 function $f_8$ has
$\mathrm{tChow} _{\pm}(f_8)=2<3=H^{\ast}(f_8)$ (exact integer certificate, 2026-07-17).
Nothing on the Snellius branch asserts the unrestricted equality as a theorem; section 6
quotes the two places that look like it and pinpoints where the tempting proof breaks.

## 1. Definitions

Work in the one-layer attention model of `model.md`, with $H^{\ast}(f)$ the least number of
heads computing $f:\lbrace 0,1\rbrace ^n\to\lbrace 0,1\rbrace$ exactly, strict final
threshold at the query token.

**One-head atoms.** For parameters $\gamma>0$, $\rho_1,\ldots,\rho_n>0$, $\alpha>0$ and
$\eta,\delta,m_1,\ldots,m_n\in\mathbb{R}$, a one-head atom is

$$ \phi(x) = \frac{ \eta+\sum _{i=1}^{n}\rho_i\alpha^{x_i}(m_i+\delta x_i) }{ \gamma+\sum _{i=1}^{n}\rho_i\alpha^{x_i} }. $$

$L _{\mathrm{frac}}(f)$ is the least $H$ such that $c+\sum _{h=1}^{H}\phi_h$ sign-represents
$f$ for some constant $c$ and atoms $\phi_h$ (positive iff $f=1$).

**Admissible affine pairs.** An affine pair $(N,D)$, with $N(x)=a_0+\sum_i a_i x_i$ and
$D(x)=d_0+\sum_i d_i x_i$, is admissible when it arises from a one-head atom on the cube.
By the atom dictionary (Theorem 2 below) this holds exactly when $D>0$ on the cube and $D$
falls in one of three classes: constant positive; all slopes $d_i>0$ with $d_0>0$; or all
slopes $d_i<0$ with $d_0+\sum_i d_i>0$. For nonconstant $D$ the numerator is arbitrary; for
constant $D$ the numerator slopes must be all positive, all negative, or all zero.

**The two cleared invariants.** For affine pairs $(N_h,D_h)$, $1\leq h\leq H$, and
$\theta\in\mathbb{R}$, write

$$ P(x) = \theta\prod _{h=1}^{H}D_h(x)+\sum _{h=1}^{H}N_h(x)\prod _{g\neq h}D_g(x). $$

$\mathrm{MFdeg} _{\pm}(f)$ is the least $H$ such that some such $P$ with **admissible** pairs
strictly sign-represents $f$; $\mathrm{tChow} _{\pm}(f)$ is the same minimum with the pairs
**unrestricted** (arbitrary affine $N_h$, $D_h$, no positivity). For $H=0$ the product is
$1$ and the sum is $0$.

## 2. Theorem 1: the normal form

**Theorem 1** ($H^{\ast}=L _{\mathrm{frac}}$). For every $f$, $H^{\ast}(f)=L _{\mathrm{frac}}(f)$.

*Proof.* This is `snellius/autoresearch:lemmas/01_foundations_and_normal_form/010_linear_fractional_normal_form.md`,
Lean-formalized in `head-complexity/HeadComplexity/Lemma10Main.lean` on branch `lean-proofs`
(axiom-clean). Both directions are constructive. Forward: for head $h$, the softmax weight
that the query assigns to position $i$ is $\rho _{h,i}\alpha_h^{x_i}$ with
$\rho _{h,i}=\exp\langle q_h,W_K^{(h)}(e_0+p_i)\rangle>0$ and
$\alpha_h=\exp\langle q_h,W_K^{(h)}(e_1-e_0)\rangle>0$, the query token itself contributes
weight $\gamma_h>0$, and the readout value at position $i$ is affine in $x_i$, namely
$m _{h,i}+\delta_h x_i$. The head's contribution to the final score is therefore exactly an
atom $\phi_h$, and the model's decision is $c+\sum_h\phi_h>0$. Conversely every parameter
tuple $(\gamma,\rho,\alpha,\eta,m,\delta)$ is realized by explicit embeddings and weight
matrices, so any sign-representation by $H$ atoms is implemented by an $H$-head model.
$\blacksquare$

## 3. Theorem 2: the affine atom dictionary

**Theorem 2.** On the cube, one-head atoms are exactly the ratios $N/D$ of admissible
affine pairs.

*Proof.* This is `013_affine_atom_dictionary.md` at the same ref. The Boolean
linearization $\alpha^{x_i}=1+(\alpha-1)x_i$ turns numerator and denominator of $\phi$ into
affine functions of $x$; the denominator $D(x)=\gamma+\sum_i\rho_i\alpha^{x_i}$ has slopes
$d_i=\rho_i(\alpha-1)$, all of one strict sign (or all zero when $\alpha=1$), with the
stated positivity because $\gamma,\rho_i>0$. Conversely, given a target $D$ in one of the
three classes one solves for $\gamma,\rho_i,\alpha$ (for example $\alpha=1+d_i/\rho_i$
uniform in sign), and the numerator freedom is checked case by case; when $D$ is
nonconstant the parameters $\eta,m_i,\delta$ realize every affine $N$. $\blacksquare$

## 4. Theorem 3: the true equality

**Theorem 3** ($H^{\ast}=\mathrm{MFdeg} _{\pm}$). For every $f$,
$H^{\ast}(f)=\mathrm{MFdeg} _{\pm}(f)$.

*Proof* (following `014_cleared_denominator_invariant.md`). If $f$ is constant, both sides
are $0$ (take score $\pm 1$, respectively $H=0$ and $\theta=\pm 1$). Assume $f$ nonconstant.

The engine is the clearing identity. Let $(N_h,D_h)$ be admissible, $\theta\in\mathbb{R}$,
and set $B:=\prod_h D_h$ and $R:=\theta+\sum_h N_h/D_h$. Since each admissible $D_h$ is
strictly positive on the cube, $B>0$ pointwise, and expanding gives, at every vertex,

$$ B(x)R(x) = \theta\prod _{h=1}^{H}D_h(x)+\sum _{h=1}^{H}N_h(x)\prod _{g\neq h}D_g(x) = P(x). $$

Direction $\mathrm{MFdeg} _{\pm}(f)\leq H^{\ast}(f)$: take an optimal representation
$c+\sum_h\phi_h$ with $H=H^{\ast}(f)$ atoms (Theorem 1). By Theorem 2 each
$\phi_h=N_h/D_h$ with $(N_h,D_h)$ admissible. Put $\theta:=c$. Then $R$ is the model score,
so $R$ sign-represents $f$; since $B>0$, the polynomial $P=BR$ sign-represents $f$ as well,
and it is exactly the cleared form on $H$ admissible pairs.

Direction $H^{\ast}(f)\leq\mathrm{MFdeg} _{\pm}(f)$: take an optimal cleared witness $P$ on
$H=\mathrm{MFdeg} _{\pm}(f)$ admissible pairs. Since $B>0$ pointwise, $R=P/B$ has the same
strict signs as $P$, so $\theta+\sum_h N_h/D_h$ sign-represents $f$. By Theorem 2 each
$N_h/D_h$ is a one-head atom, so $L _{\mathrm{frac}}(f)\leq H$, and Theorem 1 converts this
into $H^{\ast}(f)\leq H$. $\blacksquare$

## 5. Theorem 4: the sandwich, and all that survives without admissibility

**Theorem 4.** For every $f$,
$\deg _{\pm}(f)\leq\mathrm{tChow} _{\pm}(f)\leq H^{\ast}(f)$.

*Proof* (following `016_tchow_sandwich_lower_bound.md`). Upper: an optimal admissible
witness for $\mathrm{MFdeg} _{\pm}(f)=H^{\ast}(f)$ (Theorem 3) is in particular an
unrestricted witness, so $\mathrm{tChow} _{\pm}(f)\leq H^{\ast}(f)$. Lower: an unrestricted
witness on $H$ pairs is a polynomial of total degree at most $H$ (each term is a product of
$H$ affine forms), so it is a threshold-degree witness: $\deg _{\pm}(f)\leq H$. $\blacksquare$

## 6. What the branch actually says, and where the tempting proof breaks

Two statements on `snellius/autoresearch` read, at a glance, like the unrestricted equality.

First, the ledger entry for Lemma 15 (`lemmas.md`, "Tangential-Chow reformulation"):

> Homogenizing Lemma 14's cleared polynomial identifies it with an **admissibility-restricted**
> parameter tangent vector to the degree $H$ Chow cone of products of linear forms \[...\]
> Consequently $H^{\ast}(f)$ is the least $H$ admitting a strict Boolean-cube sign-representer
> from this **restricted** tangential-Chow form.

That is Theorem 3 of this note restated geometrically; the qualifier "restricted" carries
all the weight, and skimming past it turns a true statement into the false one.

Second, `BLUEPRINT.md`, frontier F4 (`frontier:tchow_comparison`), math normalized:

> **statement**: (F4) Define $\mathrm{tChow} _{\pm}(f)$ by dropping the \[admissibility
> restrictions\] \[...\] Prove either $H^{\ast}(f)=\mathrm{tChow} _{\pm}(f)$, or strictness \[...\]

So the literal equality $H^{\ast}(f)=\mathrm{tChow} _{\pm}(f)$ does appear on the branch, but
as one horn of an open comparison question, not as a claim. The branch itself resolved the
lower horn (Lemma 23: $\deg _{\pm}$ versus $\mathrm{tChow} _{\pm}$ can gap linearly); the
certificates below resolve the upper horn: F4 is settled, **both** sandwich inequalities can
be strict, and no invariant in this family equals $H^{\ast}$.

Third, the informal-prover archive `informal_proofs/results.jsonl` (June 25, present on
`snellius/jul15` and on the local `informal-prover` line) contains four **partial
equality** results, all with verification verdict "correct" and all genuinely true:
entry 17, positivity is free at level one ($\mathrm{tChow} _{\pm}\leq 1$ iff
$H^{\ast}\leq 1$ iff constant or LTF); entry 18, positivity is free on all symmetric
functions ($\mathrm{tChow} _{\pm}=H^{\ast}=\deg _{\pm}=C(F)$, a sandwich squeeze); entry 19,
positivity is free whenever $\deg _{\pm}(f)=H^{\ast}(f)$ (again a squeeze); and entry 29,
the order-2 **gauge-transfer lemma** titled "product positivity is free" (two earlier
attempts, entries 27 and 28, are archived with verdict "incorrect"). Any of these titles,
skimmed, reads as "positivity costs nothing", which compresses in memory to the false
$H^{\ast}=\mathrm{tChow} _{\pm}$. The $f_8$ certificate shows the general statement fails
exactly outside the safe regimes: $f_8$ is non-symmetric with $\deg _{\pm}<H^{\ast}$.

**Where the reverse direction actually dies.** The proof of Theorem 3 converts a cleared
witness $P$ back into a head model via $R=P/B$, $B=\prod_h D_h$, which needs $B>0$ on the
cube and each pair in an atom class (Theorem 2). Entry 29's gauge lemma says the first
input is free at order 2: writing $P=D_1L_1+D_2L_2$, some $G\in\mathrm{GL}_2$ acting by
$(E_1,E_2)^{\top}=G(D_1,D_2)^{\top}$ makes $E_1E_2>0$ everywhere (strictness forbids common
zeros, and finitely many denominator directions always leave a free arc in
$\mathbb{RP}^1$ to cut through). I verified this concretely on our $f_8$ witness: the
raw certificate has $D_1<0$ at 120 of 256 vertices, $D_1=0$ at 16, $D_2<0$ at 124, $=0$
at 8, and $B<0$ at 130; after the gap-cutting gauge, $E_1E_2>0$ at all 256 vertices.
What no gauge can repair is the **per-head** requirement: in the gauged witness $E_1<0$ at
exactly 128 vertices and $E_2<0$ at exactly 128, and this is forced, because a one-signed
admissible pair of denominators would put $f_8$ at two heads, contradicting lemma 189. So
the unbridgeable step is not product positivity but individual one-signedness together
with the three slope classes of Theorem 2, and that is precisely the content admissibility
adds. The $f_6$ witness tells the same story at order 4 (all four denominators mixed-sign
and vanishing somewhere on the cube), where no $\mathrm{GL} _H$ gauge action even exists,
since the tangent form is only bilinear at $H=2$.

## 7. Theorem 5: the equality fails without admissibility

**Theorem 5.** $\mathrm{tChow} _{\pm}\neq H^{\ast}$. Concretely, for
$f_8(x,y)=\mathbf{1}[\Delta(x,y)\geq 2]$ on $x,y\in\lbrace 0,1\rbrace ^4$:
$\mathrm{tChow} _{\pm}(f_8)=2$ while $H^{\ast}(f_8)=3$.

*Proof.* $\deg _{\pm}(f_8)=2$ and $H^{\ast}(f_8)=3$ are lemma 189
(`lemmas/06_strict_separations/189_eight_bit_hamming_threshold_strict_separation.md`, branch
`codex/sprint-1`). The certificate `claude-comments/tchow_certificates/tchow2_f8_integer_certificate.json`
exhibits an unrestricted two-pair witness with all-integer data whose minimum signed value
over the 256 vertices is $840>0$, verified in exact integer arithmetic; with the sandwich
floor $\deg _{\pm}(f_8)=2$ this pins $\mathrm{tChow} _{\pm}(f_8)=2<3=H^{\ast}(f_8)$.
$\blacksquare$

The same phenomenon at six bits: $\mathrm{tChow} _{\pm}(f_6)=4=\deg _{\pm}(f_6)$ for the
parity triple (certificate `tchow4_f6_integer_certificate.json`), so the unrestricted
invariant cannot decide whether $H^{\ast}(f_6)>4$. Where the two invariants differ, the
gap is carried entirely by admissibility, that is, by softmax positivity and the
orientation classes of Theorem 2. Any lower bound beyond $\mathrm{tChow} _{\pm}$ must use
those semialgebraic constraints; this is exactly the regime of the ongoing six-bit
four-head exclusion program.

## 8. Provenance

- `snellius/autoresearch:lemmas/01_foundations_and_normal_form/` files `010`, `013`, `014`,
  `015`, `016` (fetched from the Snellius cluster on 2026-07-17; the parallel local ledger
  has `autoresearch:lemmas/01_foundations_and_normal_form/018_tchow_sandwich.md`).
- Lean: `origin/lean-proofs:head-complexity/HeadComplexity/Lemma10Main.lean` (normal form),
  `Sandwich.lean` (threshold-degree bound), both in the axiom-clean build.
- Certificates and search code: `claude-comments/tchow_certificates/`.
