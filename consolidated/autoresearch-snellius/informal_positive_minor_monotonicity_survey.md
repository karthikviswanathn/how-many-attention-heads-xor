Reads confirm the picture precisely. Here is the survey.

## Literature survey: "Positive Boolean minors do not increase head complexity"

### Bottom line first
This target is **not yet in the proved stack, but it is a direct extension of two lemmas that are**: Lemma 26/27 (subcube‑restriction monotonicity) and Lemma 31 (irrelevant‑variable / permutation / complement invariance). The in‑repo draft `informal_positive_minor_monotonicity.md` currently holds only the statement — no proof yet — so this is live lead work, and the route below is exactly the one the existing proofs already template. Do **not** redo it from the attention model directly; it should be proved at the **linear‑fractional normal‑form level (Lemma 10)**, where it is almost immediate.

The single piece of genuinely new content beyond Lemmas 26 + 31 is **coordinate identification / duplication** (one $y_j$ feeding several $f$‑slots). Constants → Lemma 26; permutation and unused $y_j$ → Lemma 31; merging is the only new case.

### What this is, in standard terms
- The relation "$g$ is obtained from $f$ by substituting into each variable of $f$ either a constant $\{0,1\}$ or one of $g$'s variables (with repetition)" is the **minor / identification‑minor / simple‑variable‑substitution** preorder on Boolean functions. Your $\tau$ is exactly a minor map; "**positive**" = negation‑free (no $z_i = 1-y_j$). A function parameter with $H^\ast(\text{minor}) \le H^\ast(\text{original})$ is called **minor‑monotone**.
- Foundational references (clone theory / universal algebra), background only — the target does not need them:
  - **N. Pippenger, "Galois theory for minors of finite functions," Discrete Math. 254 (2002) 405–419** — the minor preorder and its Galois connection. (Confident.)
  - **Ekin, Foldes, Hammer, Hellerstein, "Equational characterizations of Boolean function classes," Discrete Math. 211 (2000)** — classes closed under variable identification/minors. (Fairly confident on attribution/venue.)
  - **Couceiro & Lehtonen**, work on the *arity gap* and "effect of variable identification on essential arity" (~2007–2012). (Confident such a line exists; less sure of exact titles/dates — searchable under "arity gap, minors of functions.")
- The relevant **meta‑principle** is folklore: any min‑resource measure of a model that can (i) hardwire input constants, (ii) fan one input out to several positions, (iii) ignore inputs, is automatically minor‑monotone. The whole mathematical content is checking that the *attention* model supports (i)–(iii) — which is non‑obvious here (see below) but true.

### Why it is not trivial in *this* model
In a circuit you wire one input to two gates for free, so identification is immediate. Here it is not:
- **Identification is not a subcube restriction.** Merging $x_{i_1}=x_{i_2}=y_j$ restricts $f$ to the *diagonal* $\{x_{i_1}=x_{i_2}\}$, which is **not a subcube**, so Lemma 26 does not cover it. This is the crux that separates the target from what is proved.
- **The softmax is a global normalization over positions**, and the number of input positions changes ($n \to m$). So you cannot "just relabel."

What rescues it is the **additive‑positive structure exposed by Lemma 10**: a one‑head atom is
$$\phi(x)=\frac{\eta+\sum_i \rho_i\,\alpha^{x_i}(m_i+\delta x_i)}{\gamma+\sum_i \rho_i\,\alpha^{x_i}},\quad \gamma,\rho_i,\alpha>0,$$
a single global $\alpha,\delta$ with per‑coordinate positive weights $\rho_i$. Each coordinate is an **additive** term in both numerator and denominator, and the weights are **positive**. Additivity + positivity is exactly the closure property that makes the atom class survive constant‑fixing *and* coordinate‑merging.

### The technique that applies (this is how Lemma 26 was proved)
Take an optimal $K=H^\ast(f)$ atom representation and substitute the minor into each atom. This is the Lemma 26 proof verbatim, except the variable part of the substitution is now **non‑injective**. Partition $[n]$ into constant coordinates (value $a_i$) and groups $G_j=\{i:\tau(i)=j\}$ feeding $y_j$. Per atom $h$:
- constants absorb into $\gamma'_h=\gamma_h+\sum_{i\,\mathrm{const}}\rho_{h,i}\alpha_h^{a_i}>0$ and $\eta'_h$ (same mechanism as Lemma 26, using $\alpha_h^{a_i}>0$);
- each group merges as $\rho'_{h,j}:=\sum_{i\in G_j}\rho_{h,i}>0$ with $m'_{h,j}:=\big(\sum_{i\in G_j}\rho_{h,i}m_{h,i}\big)/\rho'_{h,j}$, keeping the **same** $\alpha_h,\delta_h$.

The merged weight $\rho'_{h,j}$ is a **sum of positive numbers, hence positive** — so the substituted $\psi_h$ is still an admissible atom, and $\psi_h(y)=\phi_h(z(y))$ pointwise, giving $L_{\mathrm{frac}}(g)\le K$. Positivity is the whole ballgame: it is why *positive* minors work and why a general minor with input negation ($\alpha^{1-y_j}$) would leave the class — the same reason Lemma 31 explicitly *refuses* to claim invariance under complementing an individual input bit. **Edge case:** if some $y_j$ is unused ($G_j=\varnothing$, so $\rho'_{h,j}=0$ violates strict positivity), that variable is irrelevant to $g$ and is handled by **Lemma 31**, exactly as the target's last sentence anticipates.

(A second, messier route — merging softmax terms at the model level by matching $\exp(\ell_j)=\sum_{i\in G_j}\exp(\ell_i)$ and a weighted‑average value, using free $d_{\mathrm{model}},d_{\mathrm{head}}$ for per‑head independence — also works but just re‑derives the same positive‑additivity fact. Not recommended.)

### Consistency / sanity checks
The target unifies the "$\le$" directions of Lemmas 26 and 31 and is consistent with everything: $\mathrm{PARITY}_2$ ($H^\ast=2$) identified to $x\oplus x=0$ drops to $0$; fixed to $x$ drops to $1$; $\mathrm{OR}_2$ ($H^\ast=1$) with a dummy stays $1$. It is also consistent with Lemma 6 ($\deg_\pm\le H^\ast$): threshold degree is itself minor‑monotone (substitute into a sign‑representing polynomial — degree cannot rise; standard/folklore, e.g. O'Donnell, *Analysis of Boolean Functions* 2014, restriction discussions; Sherstov's block‑composition work), so both sides of Lemma 6 move the same way.

### Transformer‑expressivity context (background, not load‑bearing)
"Number of heads" as a complexity measure is specific to this project; I know of no external theorem stating head‑complexity minor‑monotonicity. For framing only: Hahn 2020 (TACL, self‑attention limitations on parity/Dyck); Sanford–Hsu–Telgarsky 2023 (NeurIPS, single‑head attention lower bounds); Yun et al. 2020, Pérez et al. 2019/2021 (expressivity/universality). None address minors.

## Actionable leads
- **Prove at the Lemma 10 level, not the model level** — substitute the minor into the $K=H^\ast(f)$ atoms; it follows that $L_{\mathrm{frac}}(g)\le K$.
- **Copy the Lemma 26 proof structure**; the only change is that the variable substitution is non‑injective, so coordinate groups $G_j$ merge.
- **The one new algebraic step is the merge** $\rho'_{h,j}=\sum_{i\in G_j}\rho_{h,i}>0$, $m'_{h,j}=$ ($\rho$‑weighted average of $m_{h,i}$); positivity of $\rho$ is what keeps the atom admissible.
- **Discharge unused $y_j$ via Lemma 31** (irrelevant‑variable invariance) — the lone case the atom argument cannot absorb.
- **State it as the unification** of the $\le$‑directions of Lemmas 26 + 31 plus identification; and note positivity is essential — input‑bit negation (general minors) provably breaks closure, matching Lemma 31's explicit non‑claim.
