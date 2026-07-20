# The Median Bit: an Order-3 Tangent Witness with Inadmissible Denominators (an F4 Probe)

## Statement

For three integers $a=I(x),b=I(y),c=I(z)$ on disjoint $n$-bit blocks, the median bit $\mathrm{MED}_j=\lfloor\mathrm{median}(a,b,c)/2^j\rfloor\bmod 2$ has
$$
\mathrm{tChow}_{\pm}(\mathrm{MED}_j)\le 3
$$
via an explicit symmetric cubic tangent form (and $=3$, since $\deg_{\pm}(\mathrm{MED}_j)=3$). The natural denominators of this witness are **not admissible**, so it does not certify $H^{*}\le3$ — making the median a sharply-posed F4 test case.

> **A clean tChow witness whose denominators are intrinsically inadmissible.** With $A=I(x),B=I(y)+\tfrac14,C=I(z)+\tfrac12$ and $s_x=2x_j-1$ (etc.), the cubic $P_j=s_x(B-C)^2+s_y(A-C)^2+s_z(A-B)^2$ sign-represents $\mathrm{MED}_j$ — for $A<B<C$ (median $B$, target $s_y$), $P_j=s_x v^2+s_y(u+v)^2+s_z u^2$ with $u,v>0$, and the median's $(u+v)^2$ term dominates ($(u+v)^2>u^2+v^2$), so $\mathrm{sign}(P_j)=s_y$. Regrouped via $L_3{=}L_2{-}L_1$, $P_j=(s_x{+}s_y)L_2L_3-(s_x{+}s_z)L_1L_3+(s_y{+}s_z)L_1L_2$ — a tangent form $\sum_h N_h\prod_{k\ne h}D_k$ with $D_h$ the pairwise differences $L_1{=}A{-}B,L_2{=}A{-}C,L_3{=}B{-}C$, giving $\mathrm{tChow}_{\pm}\le3$. But those $D_h$ form a mixed-sign triangle $(+,-,0),(+,0,-),(0,+,-)$ that **no input flip makes simultaneously one-sided** — admissibility (the content of $H^{*}$ vs $\mathrm{tChow}_{\pm}$) genuinely fails for the natural witness. A direct search finds $H^{*}=3=\mathrm{tChow}_{\pm}$ for $2$-bit integers (positivity *free* there, via different admissible denominators); whether the admissible order-$3$ form exists for all $n$ — F4-free median, or the first positivity gap — is open.

## Proof

**The cubic sign-represents $\mathrm{MED}_j$.** The offsets $\tfrac14,\tfrac12$ make $A,B,C$ distinct (and do not change $\mathrm{MED}_j$: tied original integers share their $j$-th bit). For the ordering $A<B<C$ the median is $B$, the target sign is $s_y$, and with $u=B-A>0,v=C-B>0$ one has $(A-C)^2=(u+v)^2,(A-B)^2=u^2,(B-C)^2=v^2$, so $P_j=s_x v^2+s_y(u+v)^2+s_z u^2$. If $s_y=+1$ then even at $s_x=s_z=-1$, $P_j\ge(u+v)^2-u^2-v^2=2uv>0$; if $s_y=-1$, $P_j\le-2uv<0$. The other five orderings follow by relabeling. So $\mathrm{sign}(P_j)=2\,\mathrm{MED}_j-1$ (verified exactly for $n=2,3$).

**It is an order-3 tangent form.** With $L_1=A-B,L_2=A-C,L_3=B-C=L_2-L_1$, the identities $L_1^2=L_1L_2-L_1L_3,\ L_2^2=L_2L_3+L_1L_2,\ L_3^2=L_2L_3-L_1L_3$ give
$$
P_j=(s_x+s_y)L_2L_3-(s_x+s_z)L_1L_3+(s_y+s_z)L_1L_2=\sum_{h=1}^3 N_h\prod_{k\ne h}D_k,
$$
$D_h=L_h$, $N_1=s_y+s_z,N_2=-(s_x+s_z),N_3=s_x+s_y$, $\theta=0$ (all affine). By the sandwich (L18, [018](../01_foundations_and_normal_form/018_tchow_sandwich.md)), $\mathrm{tChow}_{\pm}(\mathrm{MED}_j)\le3$; with $\deg_{\pm}=3$ it is exactly $3$. $\blacksquare$

## Consequence: the F4 significance

This is the cleanest concrete probe of F4 ("does positivity cost a head?", $H^{*}\overset?=\mathrm{tChow}_{\pm}$) found so far. The median has an *elegant, symmetric, low-order* tangent witness, yet its natural denominators — the three pairwise differences — are pairwise oppositely oriented across the three blocks, so no global variable flip (L15) renders them one-sided, and $\mathrm{span}(L_1,L_2)$ contains **no** nonzero one-sided affine form. Thus the obstruction to reading off $H^{*}\le3$ is intrinsic to the witness, not a presentation artifact. Either the median is **F4-free** ($H^{*}=3$ for all $n$, via admissible denominators *unrelated* to the $L_h$), or it is the **first positivity gap** ($H^{*}>3$). The current evidence is genuinely split: for $2$-bit integers ($n=6$) a heavy admissible-form search finds $H^{*}=3$ with **healthy margin** (so F4-free there), but for $3$-bit integers ($n=9$) two independent admissible-denominator searches **fail to find any strict order-$3$ admissible form** (best margin $\approx0$) — a *suggestive but inconclusive* signal of a possible gap (heuristic search failure is never a proof of infeasibility, a caution this project has repeatedly earned). So the median is the natural family on which to test F4 next — a complement to the order-2 covering reduction (L40), now at order 3, and the most promising concrete candidate for either confirming F4-free or exhibiting the first positivity gap. (The cubic was found via a Codex consult, which supplied it and, importantly, flagged that it does *not* certify $H^{*}\le3$.)

## Remarks

- Contrast the order statistics that *are* cleanly admissible: $\min,\max$ ($H^{*}=2$, L49) use $A=x_j-y_j$ which becomes one-sided after a single flip; the median's three pairwise differences cannot all be flipped one-sided at once — the obstruction is the *three-way* coupling.
- $\deg_{\pm}(\mathrm{MED}_j)=3$ is constant in the bits-per-integer (verified $2,3,4$ bits), so the witness is genuinely order $3$ for all $n$, not a small-$n$ artifact.
