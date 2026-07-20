# Open Problem: is `H*(f) = δ(G)` for every 2-block-symmetric Boolean function?

> **Audience.** This is a self-contained, deliberately *pedantic* problem statement
> meant to be handed to an independent agent (human or model) with **no prior
> context**. Every term is defined from scratch; every claim is tagged
> `PROVEN` / `CONJECTURE` / `REFUTED` / `OPEN` / `NUMERICAL`. Read §0 first.
>
> **Your job** is in §9. The single hardest step is in §8. The most promising
> counterexample is the *interior disk* in §10.

---

## 0. How to use this document

1. The **conjecture** is in §4. It is an **upper bound** question (§4.3); the
   matching lower bound is already proven (§5, P1).
2. Read §5 (proven), §6 (refuted — *do not retry these*), §7 (exact algebraic
   reduction), §8 (hardest step), §10 (counterexample candidates).
3. Deliver **either** a proof of the upper bound **or** a *certified*
   counterexample (§9). A failed numerical search is **not** a counterexample
   (§6, R4).
4. Reason rigorously over **ℝ**. State every hypothesis you use, especially which
   *denominator class* (§3.2) you assume — it is load-bearing.

---

## 1. Notation and conventions

- `n ≥ 1`; the Boolean cube is `{0,1}^n`. Variables `x = (x_1,…,x_n)`, `x_i ∈ {0,1}`.
- A Boolean function is `f : {0,1}^n → {0,1}`. Its **sign encoding** is
  `σ_f(x) := 2 f(x) − 1 ∈ {−1, +1}`.
- An **affine form** is `A(x) = a_0 + Σ_{i=1}^n a_i x_i` with `a_i ∈ ℝ`. "Affine" =
  "degree ≤ 1". A **linear form** is the homogeneous case (`a_0 = 0`).
- All polynomials are over **ℝ**. "Sign-represents" always means **strict**:
  `p` sign-represents `σ` on a finite set `X` iff `σ(x)·p(x) > 0` for **every**
  `x ∈ X` (in particular `p(x) ≠ 0` on `X`).
- On the cube, `x_i^2 = x_i`, so every function `{0,1}^n → ℝ` has a unique
  **multilinear** representative. The **Boolean ideal** is
  `I_bool := ⟨x_1^2 − x_1, …, x_n^2 − x_n⟩`; two polynomials agree on `{0,1}^n`
  iff they differ by an element of `I_bool`.
- `⌊·⌋`, `Θ`, `O`, `exp`, `log` are standard. Logs are natural unless noted.

---

## 2. The model: head-complexity `H*(f)`

### 2.1 Origin (one-layer softmax attention), for context only
The quantity comes from one-layer softmax self-attention on Boolean inputs. On the
cube, `a^{x_i} = 1 + (a−1) x_i` is affine in `x_i`, and a single softmax attention
head reduces **exactly** to a ratio of an affine numerator over a positive affine
denominator. You do **not** need the attention background; work from §2.2, which is
the established exact normal form (this project's "Lemma 10 / linear-fractional
normal form").

### 2.2 Exact normal form (this is the working definition) — `PROVEN`
A **head** is a function `h : {0,1}^n → ℝ` of the form
```
h(x) = A(x) / D(x),
```
where
- `A` is an arbitrary **affine** form, and
- `D` is an affine form that is **positive on the cube**: `D(x) > 0` for all
  `x ∈ {0,1}^n`. In the attention-derived model `D` is additionally **one-signed**
  (monotone): its linear coefficients all share one sign. See §3.2 / §11 for why
  this distinction matters and must be pinned down.

### 2.3 Definition of `H*(f)`
`H*(f)` is the least integer `H ≥ 0` such that there exist heads `h_1,…,h_H` and a
constant `c ∈ ℝ` with
```
σ_f(x) · ( c + Σ_{k=1}^H h_k(x) ) > 0   for all x ∈ {0,1}^n.
```
(For `H = 0` this is `σ_f(x)·c > 0`, i.e. `f` constant.) This `H*` equals the
project's `L_frac` (least number of single-head linear-fractional atoms).

### 2.4 Basic facts (sanity checks)
- `f` constant `⟺ H*(f) = 0`. `PROVEN`
- `f` a nonconstant linear threshold function (`f(x)=1 ⟺ w·x+b>0`) `⟹ H*(f)=1`
  (take `D ≡ 1 > 0`, `A = w·x + b`; `sign(A/D)=sign(A)`). `PROVEN`
- **Clearing denominators.** With `D_k > 0` on the cube, `c + Σ_k A_k/D_k` has the
  same sign on the cube as the **cleared numerator**
  ```
  Q(x) := c ∏_{k=1}^H D_k(x) + Σ_{i=1}^H A_i(x) ∏_{k≠i} D_k(x),         (★)
  ```
  because `∏_k D_k(x) > 0` on the cube. Note `deg Q ≤ H`. Hence **`H` heads ⟹ a
  degree-`≤H` polynomial `Q` sign-representing `f` on the cube**, of the special
  *factored* shape (★). `PROVEN`

---

## 3. 2-block-symmetric functions and the grid threshold degree `δ(G)`

### 3.1 Threshold degree
For `σ : {0,1}^n → {±1}`, the **threshold degree**
```
deg±(σ) := min { deg p : p ∈ ℝ[x_1,…,x_n],  σ(x)·p(x) > 0  ∀ x ∈ {0,1}^n }.
```
Every Boolean function has `deg±(σ) ≤ n` (multilinear interpolation).

### 3.2 The denominator class (PIN THIS DOWN — §11)
Two candidate denominator classes:
- **(D-pos)** `D` affine, `D(x) > 0` for all `x ∈ {0,1}^n`. (Larger class.)
- **(D-mono)** `D` affine, `D(x) > 0` on the cube **and** one-signed (all linear
  coefficients of one sign) — the attention-faithful class. (Smaller class.)
`(D-mono) ⊆ (D-pos)`, so `H*_{(D-pos)}(f) ≤ H*_{(D-mono)}(f)`. The conjecture is
posed for the **model class (D-mono)**. A *construction* (upper bound) must use
(D-mono) to be model-faithful; a *lower bound / counterexample* is strongest in
(D-pos) (it then also holds for (D-mono)). **Always state which class you use.**

### 3.3 2-block-symmetric functions
Fix a partition `[n] = A ⊔ B` with `|A| = a ≥ 1`, `|B| = b ≥ 1`, `a + b = n`.
Write `s := |x_A| = Σ_{i∈A} x_i` and `t := |x_B| = Σ_{i∈B} x_i`; both are affine
forms with integer values, `s ∈ {0,…,a}`, `t ∈ {0,…,b}`.

`f` is **2-block-symmetric** (w.r.t. `(A,B)`) iff `f(x)` depends only on `(s,t)`.
Equivalently there is a **grid function**
```
G : {0,…,a} × {0,…,b} → {0,1},   f(x) = G(|x_A|, |x_B|).
```
The **grid** is the integer rectangle `Γ := {0,…,a} × {0,…,b}` (size `(a+1)(b+1)`).

### 3.4 Bivariate grid threshold degree `δ(G)`
```
δ(G) := min { deg q : q ∈ ℝ[s,t],  σ_G(s,t)·q(s,t) > 0  ∀ (s,t) ∈ Γ },
```
where `σ_G := 2G − 1`. (Strict sign on every grid point; `deg` is total bivariate
degree.)

### 3.5 `deg±(f) = δ(G)` — `PROVEN`
*Both directions, for completeness.*
- **`deg±(f) ≤ δ(G)` (lift):** if `q(s,t)` sign-represents `G` on `Γ` with
  `deg q = δ(G)`, then `P(x) := q(|x_A|,|x_B|)` has degree `δ(G)` (since `|x_A|`,
  `|x_B|` are affine) and `σ_f(x)·P(x) = σ_G(s,t)·q(s,t) > 0` on the cube.
- **`δ(G) ≤ deg±(f)` (symmetrize):** if `p` sign-represents `f` with `deg p =
  deg±(f)`, average over the group `S_A × S_B` (permuting coordinates within each
  block): `p_sym(x) := |S_A×S_B|^{-1} Σ_π p(πx)`. Since `f(πx)=f(x)`, each
  `σ_f(x)·p(πx) > 0`, so their average `σ_f(x)·p_sym(x) > 0` (mean of positives).
  `p_sym` is block-symmetric of degree `≤ deg p`, hence equals `q(|x_A|,|x_B|)` for
  a bivariate `q` of degree `≤ deg±(f)`, and `q` sign-represents `G` on `Γ`. Thus
  `δ(G) ≤ deg±(f)`.

---

## 4. The conjecture (the open question)

### 4.1 Statement
> **Conjecture (2-block collapse).** For every 2-block-symmetric `f` (any blocks
> `A,B` with `a,b ≥ 1`, any grid function `G`),
> ```
> H*(f) = δ(G).
> ```

### 4.2 What is automatic
By §2.4 (clearing denominators) and §3.5: `deg±(f) ≤ H*(f)`, and `deg±(f)=δ(G)`.
Hence `δ(G) ≤ H*(f)` **always**. `PROVEN`

### 4.3 So the open content is the UPPER bound
> **`H*(f) ≤ δ(G)`** for every 2-block-symmetric `f`. **`OPEN`.**
> (With §4.2 this is equivalent to the full equality.)

Set `d := δ(G)` throughout the rest.

---

## 5. What is PROVEN

- **(P1) Lower bound.** `δ(G) = deg±(f) ≤ H*(f)`. (§3.5, §4.2.) `PROVEN`
- **(P2) Exact realizability condition.** `H*(f) ≤ d` **iff** there exist
  `d` denominators `D_1,…,D_d` (class per §3.2), affine numerators `A_1,…,A_d`, and
  `c ∈ ℝ` such that the cleared numerator `Q` of (★) **strictly sign-represents
  `f` on the cube**. (Just unfolds §2.3 + §2.4; `deg Q ≤ d`.) `PROVEN`
- **(P3) Star-ideal / Cayley–Bacharach form of (P2).** Homogenize with a new
  variable `x_0`: let `D̃_i` be the linear homogenization of `D_i`, and `Q̃` the
  degree-`d` homogenization of `Q`. Define the **star ideal**
  ```
  J_D := ⟨ ∏_{j≠1} D̃_j , … , ∏_{j≠d} D̃_j ⟩          (generators have degree d−1).
  ```
  Then (★) `⟺ Q̃ ∈ J_D` (membership tested in the degree-`d` graded piece, via
  **linear** multipliers). If the `d` hyperplanes `{D̃_i = 0}` are in **linear
  general position** (every `≤ n+1` of the `D̃_i` linearly independent), then
  ```
  Q̃ ∈ J_D  ⟺  Q̃ vanishes SCHEME-THEORETICALLY on every codim-2 flat
                        L_{ij} := {D̃_i = D̃_j = 0},  i<j.
  ```
  **Independently verified** (exact linear algebra over `𝔽_101` for several
  `(n,d)`; necessity of general position confirmed by a pencil counterexample where
  the equivalence fails: `dim (J_D)_d = 13 < 19 = dim{forms vanishing on all
  flats}`). `PROVEN` (confidence 0.9). *Caveat:* the condition is "the whole codim-2
  flat lies in `{Q̃ = 0}`," which is **much stronger** than "the flats are off the
  cube."
- **(P4) `δ = 1`.** `δ(G)=1 ⟹ G` is a grid LTF `⟹ f` is an LTF `⟹ H*(f)=1`.
  `PROVEN`
- **(P5) `δ = 2`, PARTIAL.** Let `q(s,t)` be a degree-2 separator.
  - **(a)** If `q` has a real zero `(s_0,t_0)` **off** the grid rectangle
    `[0,a]×[0,b]` such that two cube-positive affine forms `D_1,D_2` have common
    zero-fiber `{s=s_0, t=t_0}` (e.g. `q` reducible into two real lines — the
    "saddle" `MAJ⊕MAJ` — or a hyperbola/parabola/ellipse crossing outside), then
    `q ∈ (s−s_0, t−t_0) = (D_1, D_2)` as polynomials, so `q = A_1 D_2 + A_2 D_1`
    and `q/(D_1 D_2) = A_1/D_1 + A_2/D_2` is a **2-head** rep: `H*(f)=2`. `PROVEN`
  - **(b)** If `q`'s real zero set lies **entirely inside** the grid rectangle (the
    **interior disk**, e.g. an indicator of a small interior region), then no
    cube-positive line passes through a zero of `q`; the construction in (a)
    **fails**, and `H*(f)=2` — observed numerically on small grids — already
    requires the Boolean-quotient freedom (§7). For (b) on **large** grids the
    value of `H*` is **`OPEN`** (see §10, the leading counterexample candidate).

---

## 6. What is REFUTED — do NOT retry these

- **(R1) The "lift + star" strategy is DEAD for irreducible separators.** If the
  separator is the lift `P(x)=p(|x_A|,|x_B|)` of a bivariate `p` with **no real
  linear factor** (and `p≠0`, `d≥2`), then `P̃ ∈ J_D` **forces every `D_i` that
  shares a nonempty pairwise flat with some `D_j` into `span{1, s, t}`** — i.e.
  full-bit heads **collapse** back to `(s,t)`-restricted heads. Proof sketch
  (verified, conf 0.83): `P̃∈J_D ⟹ P` vanishes on each nonempty `L_{ij}`; project
  `L_{ij}` to the `(s,t)`-plane — image dim 2 `⟹ p≡0`, dim 1 `⟹ p` has a real
  linear factor, so (irreducible) image is a point `(σ,τ)`; then
  `L_{ij}={s=σ}∩{t=τ}` and `D_i,D_j ∈ span{1,s,t}`. The `(s,t)`-restricted star
  problem is itself **false** on large grids by a parameter count. **Moral:** do
  **not** try to realize the symmetric lift `p(|x_A|,|x_B|)` directly with full-bit
  star denominators. (Scope: this constrains only representations whose cleared
  numerator *is* an irreducible bivariate lift; it does **not** by itself
  lower-bound `H*` — see R5.)
- **(R2) The 3+ block analogue is FALSE.** For `k ≥ 3` blocks of size `m`
  (`n=km`, `k` fixed, `m→∞`): there are `2^{(m+1)^k} = exp(Θ(m^k))` `k`-block
  functions, but only `exp(O(m^2 log m))` are representable with `H ≤ n` heads
  (Warren/Milnor–Thom: `N=O(m^2)` real parameters, `M=(m+1)^k` sign polynomials of
  degree `O(m)`). Since `deg± ≤ n`, almost all have `H* > n ≥ deg±`. `PROVEN`
  (conf 0.9). **Consequence for proof strategy:** any valid proof of the
  conjecture **must use a property special to 2 blocks** (bivariate = binary forms
  factor into linear forms; the grid is 2-dimensional). A generic
  "high-dimensional room / counting" heuristic **cannot** work — it would also
  (falsely) prove the 3-block case. At `k=2` the same counting does **not**
  separate (the `log m` factor exactly closes the gap), which is *why* 2 blocks is
  the borderline where equality is even plausible.
- **(R3) `H* = deg±` is FALSE for general Boolean `f`** (same counting). The
  2-block class is a *special restricted* class; do not assume the general
  identity.
- **(R4) A failed numerical/heuristic search is NOT a counterexample.** The
  heuristic atom-search has produced **false negatives** (it once "failed" at
  `K=2` on the disk, which actually has `H*=2`). Only (i) explicit constructions
  (search **successes**) and (ii) **certified** non-existence (a real obstruction:
  dimension/sign-rank/exhaustive certified star search) count.
- **(R5) `Claim A` (R1) is not a lower bound on `H*`.** A generic minimal
  `d`-head representation's cleared numerator `Q` need **not** be a bivariate
  `(s,t)`-lift, nor lie in any single `J_D` of the lift form; the Boolean-quotient
  freedom (§7) lets `Q` be non-symmetric. So R1 kills a *strategy*, not the
  conjecture.

---

## 7. The escape hatch: Boolean-quotient freedom

Because sign-representation is only required **on the cube**, the cleared numerator
`Q` is free **modulo `I_bool`**: for any chosen reference `P` (e.g. the symmetric
lift),
```
Q = P + Σ_{i=1}^n (x_i^2 − x_i) · g_i ,     deg g_i ≤ d − 2,
```
keeps `Q ≡ P` on the cube (so the sign pattern, hence `f`, is unchanged) while
changing `Q` **off** the cube. Crucially, the **homogenization** `Q̃` (which is
what the star-ideal test (P3) sees) **does** change — it acquires non-multilinear,
non-symmetric content. This is the only known way to satisfy `Q̃ ∈ J_D` while
evading the collapse (R1): make `Q` a **non-symmetric** degree-`d` polynomial that
agrees in sign with `f` on the cube but whose homogenization lies in a positive
star ideal. Degree bookkeeping: `x_i^2 − x_i` has degree 2, so `g_i` has degree
`≤ d−2` (`d=2 ⟹ g_i` constant; `d=3 ⟹ deg g_i ≤ 1`; …).

---

## 8. The single hardest step (the crux)

The conjecture's upper bound is equivalent to a **sign-chamber-meets-star-ideal**
statement. For fixed `f` (with `d=δ(G)`), the set
```
C_f := { Q ∈ ℝ[x]_{≤ d} : σ_f(x)·Q(x) > 0  ∀ x ∈ {0,1}^n }
```
is an open polyhedral **cone** (the "sign chamber" of `f` in degree `d`). The
question:

> **(HARD)** Does `C_f` contain some `Q` whose degree-`d` homogenization `Q̃` lies
> in `J_D` for some choice of `d` cube-positive denominators `D_1,…,D_d` (class
> §3.2) in general position? Equivalently: does the map
> ```
> Φ : { (D_1,…,D_d, A_1,…,A_d, c) : each D_i cube-positive }  ⟶  ℝ[x]_{≤ d},
>     (D_•, A_•, c) ↦ Q of (★)
> ```
> have image meeting **every** 2-block sign chamber `C_f`?
>
> Prove it always does (`⟹` conjecture), or exhibit an `f` whose chamber it
> **misses** with a certificate (`⟹` counterexample).

For `δ=2` this is the gap between §5(P5a) (chambers reachable by an off-grid conic
zero) and §5(P5b) (interior-disk chambers).

---

## 9. What a solution must deliver

Exactly one of:

- **(SOLVE-YES)** A proof of `H*(f) ≤ δ(G)` for **all** 2-block-symmetric `f`. By
  R2 it must exploit a genuinely **2-block-only** property; by R1 it cannot route
  through the irreducible symmetric lift, so it will produce a **non-symmetric**
  `Q` via §7 (or an entirely different argument). State the denominator class
  (§3.2). A clean constructive proof is the formalization target.
- **(SOLVE-NO)** A **specific** 2-block `f` together with a **certified** proof
  that `H*(f) ≥ δ(G) + 1` (no `d`-head representation exists). Acceptable
  certificates: a dimension/incidence obstruction (the image of `Φ` misses `C_f`),
  a sign-rank or algebraic obstruction on the cleared numerator, or an exhaustive
  *certified* search over star configurations — **not** a failed heuristic search
  (R4). The leading candidate is in §10.

Also valuable (partial credit): resolve the **`δ=2` interior disk on a large
grid** (§5 P5b, §10) either way; or sharpen R1's hypotheses to a clean,
gap-free statement (the verified version needs: every used pairwise flat nonempty;
`D_i,D_j` independent; `p≠0` with no real linear factor; `d≥2`).

---

## 10. Counterexample candidates (where to look first)

1. **Interior disk on a large grid (TOP CANDIDATE).** Take `a=b=m` large; let
   `G(s,t)=1` iff `(s−m/2)^2 + (t−m/2)^2 < r^2` for a small `r` (a disk strictly
   inside the grid). Then `δ(G)=2` (an interior region needs a conic; no line
   separates it), the unique-shape separator is an **irreducible definite conic**
   whose real zero set is the circle **inside** the rectangle, so §5(P5a) fails and
   R1 applies to the lift. The question is whether the Boolean-quotient freedom
   (§7) still produces a non-symmetric 2-head `Q`. On `(2,2)` (the point function
   `(x_0⊕x_1)∧(x_2⊕x_3)`) it does (`H*=2`, numerical). **Does it still on large
   `m`?** A certified `H*≥3` here would refute the conjecture at `δ=2`.
2. **Thin sign chambers.** An `f` whose degree-`d` chamber `C_f` is "thin" in the
   non-symmetric directions (the §7 freedom is sign-blocked), so every chamber
   member is, mod `I_bool`, essentially a lift — then R1 forces `H* ≥ d+1`.
3. **Higher-degree analogues of the interior disk** (`δ=3,4`) on large grids,
   where the collapse pressure (R1) grows.

---

## 11. Pedantic caveats / conventions to nail down

- **Denominator class (§3.2) is load-bearing.** The attention model gives
  **(D-mono)** (one-signed/monotone). It is *not currently settled* whether
  enlarging to **(D-pos)** changes `H*`. State your class. Upper bounds proven only
  in (D-pos) are weaker than the model claim; lower bounds proven in (D-pos) are
  stronger. When in doubt, do upper bounds in (D-mono), lower bounds in (D-pos).
- **Strictness.** All sign-representations are strict (`≠ 0` on the cube). Chambers
  are **open** cones.
- **Degrees.** `A_i`, `D_i` are affine (degree ≤ 1); `c` is a constant; `Q` of (★)
  has degree `≤ d`. The homogenization is to degree **exactly** `d`.
- **General position** (P3) means **linear general position** of the `D̃_i`. The
  star-ideal `⟺` vanishing equivalence can **fail** without it.
- **"Scheme-theoretically"** (P3): vanishing as a scheme on the codim-2 flat, not
  merely set-theoretically; in general position the star scheme is reduced so the
  two coincide, but do not silently drop the qualifier.
- **`δ(G)` vs `deg±(f)`** are equal (§3.5) — use whichever is convenient, but they
  are the **same** integer `d`.
- **Field is ℝ.** "Irreducible" / "no real linear factor" are over ℝ (a real
  irreducible conic like `s^2+t^2−1` has no real linear factor; `st` does).
- **Negation symmetry.** `H*(f) = H*(¬f)` (negate `c` and all `A_i`; denominators
  unchanged). Use it as a consistency check and to avoid false negatives.

---

## 12. One-line glossary

- `H*(f)` — min heads `A(x)/D(x)` (`D>0` on cube) whose signed sum sign-represents
  `f`. §2.
- `deg±` — threshold degree (min degree of a sign-representing polynomial). §3.1.
- 2-block-symmetric — `f(x)=G(|x_A|,|x_B|)` for a partition `A⊔B`. §3.3.
- `δ(G)` — bivariate grid threshold degree of `G`. §3.4. Equals `deg±(f)`.
- cleared numerator `Q` — (★); degree `≤ H`; sign-represents `f` iff the heads do.
- star ideal `J_D` — `⟨∏_{j≠i} D̃_j⟩`; `H*≤d ⟺ Q̃∈J_D` for some positive `D_i`. §5 P3.
- Boolean-quotient freedom — change `Q` by `Σ(x_i^2−x_i)g_i` (free off-cube). §7.
- interior disk — degree-2 separator with real zeros only **inside** the grid;
  the top counterexample candidate. §10.

---

### Provenance (for the curious; not needed to solve)
This statement is distilled from a numeric+symbolic investigation: the lower bound
and normal form are established project lemmas; the star-ideal condition (P3), the
collapse (R1), the 3-block refutation (R2), and the reconciliation (§7) were
derived in a theory consult and then **independently re-verified** by a 5-agent
adversarial pass (exact linear algebra over `𝔽_101`, Grassmannian dimension counts,
an explicit pencil counterexample). The `(2,2)` grid (all 512 functions) has
`H*=δ` numerically; larger-grid sweeps were in progress at time of writing.
`NUMERICAL` evidence supports the conjecture but does not prove it.
