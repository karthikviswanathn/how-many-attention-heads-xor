# ORing a Disjoint Monotone Term Costs at Most One Head

## Statement

Let $f$ be a Boolean function on a variable set $Z$, and let $T(w) = \bigwedge_{i\in A} w_i$ be a monotone term (AND of variables) on a set $A$ **disjoint** from $Z$. Then
$$
H^{*}(f) \;\le\; H^{*}(f\vee T) \;\le\; H^{*}(f) + 1 .
$$

> **The disjoint-term composition bound — and the "monotone corner detector."** A single attention head, under the model's one-sided (monotone) bias, can sharply detect exactly one extreme corner of a coordinate block. The admissible atom $\psi = M/D$ with $D = \gamma + \rho\sum_{i\in A}\alpha^{w_i}$ ($\alpha\in(0,1)$) is $\ge 0$ everywhere, spikes large on the all-ones corner ($T{=}1$), and is $\approx 0$ off it; adding it to $f$'s representation as one extra **summed atom** (not a product factor) detects $T$ without disturbing $f$'s margins. The lower side is restriction (set any $w_{i_0}{=}0$ to kill $T$ and recover $f$). This is exactly why a *monotone* term composes for free while a mixed-polarity term or a parity does not: an admissible $D$ is monotone, so a single head can spike only at the all-ones (or all-zeros) corner, never at an interior vertex. The flagship consequence is $H^{*}(\mathrm{INT}_n) \le n-1$, closing the upper side of the $\mathrm{INT}_n$ rate question.

## Proof

**Upper bound.** Let $H=H^{*}(f)$, so $f(z)=1 \iff V(z)>0$ with $V=c+\sum_{h=1}^H\phi_h$, admissible atoms $\phi_h$ on $Z$ (the head-complexity normal form, L10/[013](../01_foundations_and_normal_form/013_atom_dictionary.md)). *Normalize to a two-sided margin:* the definition only gives $f=0\iff V\le 0$, so shift the constant once — replace $V$ by $V-\tfrac12\min_{f=1}V$ (same atoms), making both implications strict; if $f\equiv 0$ take $V\equiv -1$, and if $f\equiv 1$ then $f\vee T\equiv 1$ is trivial. Now
$$
m=\min_{f=1}V>0,\qquad \mu=\min_{f=0}(-V)>0,\qquad B=\max_z|V(z)|<\infty .
$$

*The corner-detector atom.* For $\alpha\in(0,1)$, $\gamma,\rho,M>0$, put $\psi(w)=M/D(w)$ with $D(w)=\gamma+\rho\sum_{i\in A}\alpha^{w_i}$. Using $\alpha^{w_i}=1+(\alpha-1)w_i$, $D=(\gamma+\rho|A|)+\rho(\alpha-1)\sum_i w_i$ is affine, $>0$ on the cube, with all slopes $\rho(\alpha-1)<0$ (one-sided); $N=M$ affine. So $\psi$ is an admissible atom, $\psi>0$ everywhere. $D$ is least at $w=\mathbf 1$ (each $\alpha^1=\alpha$ smallest), so $\psi(T{=}1)=M/(\gamma+\rho|A|\alpha)$; if $T(w)=0$ some $w_i=0$ gives $\alpha^0=1$, so $D\ge\gamma+\rho$ and $\psi(T{=}0)\le M/(\gamma+\rho)$.

*Parameters.* Take $\gamma=1$, $\rho>2B/\mu-1$, $M\in(2B,\ \mu(1+\rho))$ (nonempty since $\mu(1+\rho)>2B$), $\alpha\in(0,\ 1/(\rho|A|))$. Then $\rho|A|\alpha<1$ gives $\psi(T{=}1)>M/2>B$, and $\psi(T{=}0)\le M/(1+\rho)<\mu$.

*Combined form.* $S=V+\psi=c+\sum_{h=1}^H\phi_h+\psi$ is a constant plus $H+1$ admissible atoms (the old atoms have zero slope in $A$, $\psi$ zero slope in $Z$; zero slopes never break one-sidedness). At every point: if $f=1$ then $S\ge m+0>0$; if $f=0,T=1$ then $S\ge -B+\psi(T{=}1)>0$; if $f=0,T=0$ then $S\le -\mu+\psi(T{=}0)<0$. So $\mathrm{sign}(S)=f\vee T$ and $H^{*}(f\vee T)\le H+1$.

**Lower bound.** Restrict $w_{i_0}=0$ for any $i_0\in A$: then $T\equiv 0$, so $(f\vee T)|_{w_{i_0}=0}=f$. By restriction monotonicity ([017](../03_lower_bounds/017_restriction_monotonicity.md)), $H^{*}(f\vee T)\ge H^{*}(f)$. $\blacksquare$

## Corollary: $H^{*}(\mathrm{INT}_n)\le n-1$

For $\mathrm{INT}_n(x,y)=\bigvee_{i=1}^n(x_i\wedge y_i)$, write $\mathrm{INT}_{k+1}=\mathrm{INT}_k\vee(x_{k+1}\wedge y_{k+1})$ with the $(k{+}1)$-st pair disjoint from the first $k$. The theorem gives $H^{*}(\mathrm{INT}_{k+1})\le H^{*}(\mathrm{INT}_k)+1$; from the base $H^{*}(\mathrm{INT}_3)=2$ ([039](039_int3_exact.md)), induction yields
$$
H^{*}(\mathrm{INT}_n)\le 2+(n-3)=n-1\qquad(n\ge 3).
$$
With the near-linear lower bound $H^{*}(\mathrm{INT}_n)\ge n/(8\log_2 n)$ ([035](../03_lower_bounds/035_int_nearlinear_lower.md)) this pins the rate up to the $\log$ factor, $\;n/(8\log_2 n)\le H^{*}(\mathrm{INT}_n)\le n-1$, with $n-1$ matching the exact value at every reliably computed $n$ ($n\le5$). The single residual is $\Theta(n)$-vs-$\Theta(n/\log n)$, which the shatter-rectangle/Warren method provably cannot close (Bartlett–Maiorov–Meir bit-extraction forces the $\log$).

## Corollary: ORing a disjoint monotone DNF, and the dual

Let $g=\bigvee_{j=1}^s T_j$ be a monotone DNF (terms possibly overlapping each other) on a variable set disjoint from $Z$. Then $H^{*}(f\vee g)\le H^{*}(f)+s$. *Proof.* Use one corner detector $\psi_j$ per term, all sharing $(\alpha,\gamma,\rho,M)$; the soft indicator $I=\sum_{j=1}^s\psi_j\ge 0$ satisfies $I\ge\psi_{j^\*}\ge M/(\gamma+\rho r\alpha)$ wherever some $T_{j^\*}$ fires ($r=\max_j|S_j|$) and $I\le sM/(\gamma+\rho)$ where $g=0$; choosing $\rho>2sB/\mu-1$, $M\in(2B,\mu(1+\rho)/s)$, $\alpha<1/(\rho r)$ makes $I>B$ on $g{=}1$ and $I<\mu$ on $g{=}0$, so $\mathrm{sign}(V+I)=f\vee g$ with $H+s$ atoms. $\square$ At $f\equiv$ false this re-derives the disjoint-DNF bound $H^{*}\le s$ ([014](014_monotone_term_dnf.md)). Dually, for a monotone CNF $g'=\bigwedge_{j=1}^s C_j$, $H^{*}(f\wedge g')\le H^{*}(f)+s$ (apply the DNF case to $\neg f\vee\bigvee_j\neg C_j$, each $\neg C_j$ an all-negative term — a corner detector at the all-zeros corner — then use $H^{*}(\neg h)=H^{*}(h)$, [015](../04_closure_and_structure/015_negation_permutation_closure.md)).

## Remarks

- **The $H{+}1$ count is genuine.** $\psi$ enters as a summed atom in $c+\sum N_h/D_h$, the head-complexity normal form, not as an extra product factor. (Contrast the false "a sum of $K$ admissible-denominator products is an order-$K$ form" — true only at $K=2$, where the cleared form happens to be degree 2.)
- **Two independent proofs of the step.** Besides the additive corner detector above, there is an equivalent multiplicative (cleared-form) proof: with $S_f=P_f/\Pi$ ($\Pi=\prod D_h>0$), $\delta=\min|S_f|$, $M=\max|S_f|$, set $E=(2+\eta)-x-y$ ($\eta=\delta/M$; admissible, slopes $-1,-1$) and $L=-t+2t(x+y)$ ($t=\delta/2$). Then $P=E\,P_f+L\,\Pi$ is an order-$(H{+}1)$ admissible form with $\mathrm{sign}(P)=\mathrm{sign}(E S_f+L)=f\vee T$: off the corner $|E S_f|\ge(1+\eta)\delta>t=|L|$ so the sign is $f$, while at the corner $E S_f+L\ge\eta(-M)+3t=\delta/2>0$ (forced $1$). The new denominator $E$ **vanishes** ($=\eta$) at the AND-corner, killing $f$'s possibly-wrong contribution there — the mechanism that bypasses the XOR/checkerboard obstruction a single affine numerator faces. (Independently rederived and exactly verified through $n=6$ by a multi-angle workflow.)
- **The saving happens once.** Iterating from the single-term base $H^{*}(T)=1$ re-derives $H^{*}\le\#\text{terms}$; $\mathrm{INT}_n$'s improvement to $n-1$ comes entirely from the stronger base $H^{*}(\mathrm{INT}_3)=2$ (the only "3 disjoint ANDs in 2 heads" merge). Every later disjoint pair is strictly $+1$.
- **One-sided is essential.** The additive route forbids bounded coefficients: it needs $\alpha\to0$, $\rho\to\infty$ (unbounded), which is why a max-margin LP with $|{\cdot}|\le1$ coefficients shows only tiny, fragile margins — an artifact, not an obstruction.
- **Why $\mathrm{INT}_n$'s saving cannot come from a weighted score.** The positive-alternation number $A_{+}(\mathrm{INT}_n)=2^n-1$ (exponential), so the weighted-score upper route (L25) gives no polynomial bound: $\mathrm{INT}_n$ is pairing-dependent while an additive score is pairing-blind. The $n-1$ saving is irreducibly multiplicative (degree-$(n-1)$ products encoding the pairing), consistent with the $\Omega(n/\log n)$ lower bound.
