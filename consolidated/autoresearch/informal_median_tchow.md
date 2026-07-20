# Problem: The median bit has an order-3 tangent witness (tChow_pm <= 3), with inadmissible natural denominators

## Background and definitions (self-contained)

For three integers $a=I(x),b=I(y),c=I(z)$ (each $I(z)=\sum_i 2^i z_i$ on disjoint $n$-bit blocks), the **median bit** is $\mathrm{MED}_j(x,y,z)=\lfloor \mathrm{median}(a,b,c)/2^j\rfloor\bmod 2$, where $\mathrm{median}$ is the middle of the three values.

**Definitions (cite as given).**
- A function $g$ has **tangential-Chow sign rank** $\mathrm{tChow}_{\pm}(g)\le H$ if $g=\mathrm{sign}(P)$ for a **tangent form** $P=\theta\prod_{h=1}^H D_h+\sum_{h=1}^H N_h\prod_{k\ne h}D_k$ with $D_h,N_h$ **affine** (no positivity/one-sidedness required). [This is $H^{*}$ without the admissibility constraint; L18 gives $\deg_{\pm}(g)\le\mathrm{tChow}_{\pm}(g)\le H^{*}(g)$.]
- A denominator $D$ is **admissible** (the extra constraint defining $H^{*}$) if $D>0$ on the cube and $D$ is one-sided (monotone in each coordinate); flipping input variables (L15) preserves $H^{*}$ and can change which forms are one-sided.

## Claim to prove

$$
\mathrm{tChow}_{\pm}(\mathrm{MED}_j)\ \le\ 3 \qquad\text{for every } n \text{ and } 0\le j\le n-1,
$$
via an explicit order-3 tangent form. (Computationally $\deg_{\pm}(\mathrm{MED}_j)=3$, so in fact $\mathrm{tChow}_{\pm}=3$.)

## Guidance (prove every step rigorously)

**Step 1 (the symmetric cubic).** Put $A=I(x)$, $B=I(y)+\tfrac14$, $C=I(z)+\tfrac12$ (the offsets only break ties; if two original integers are equal their $j$-th bits agree, so the selected median bit is unaffected), and $s_x=2x_j-1,\ s_y=2y_j-1,\ s_z=2z_j-1\in\{\pm1\}$ (so $s_x>0\iff x_j=1$, etc.). Define
$$
P_j=s_x\,(B-C)^2+s_y\,(A-C)^2+s_z\,(A-B)^2 .
$$
Prove $\mathrm{sign}(P_j)=2\,\mathrm{MED}_j-1$ on the whole cube.

*Proof of the sign.* By symmetry assume the order $A<B<C$ (the offsets make $A,B,C$ pairwise distinct), so the median is $B$ and $\mathrm{MED}_j$ is the bit selecting $y_j$, i.e. the target sign is $s_y$. Write $u=B-A>0$, $v=C-B>0$; then $A-C=-(u+v)$, $A-B=-u$, $B-C=-v$, so
$$
P_j=s_x v^2+s_y(u+v)^2+s_z u^2 .
$$
If $s_y=+1$: even in the worst case $s_x=s_z=-1$, $P_j\ge (u+v)^2-u^2-v^2=2uv>0$. If $s_y=-1$: symmetrically $P_j\le -2uv<0$. So $\mathrm{sign}(P_j)=s_y=2\,\mathrm{MED}_j-1$. The other five orderings are identical by relabeling. *(Verify the construction is correct on small cubes, e.g. $n=2,3$.)*

**Step 2 (it is a tangent form, so $\mathrm{tChow}_{\pm}\le3$).** Let $L_1=A-B,\ L_2=A-C,\ L_3=B-C$ (affine; note $L_3=L_2-L_1$). Using $L_1^2=L_1L_2-L_1L_3$, $L_2^2=L_2L_3+L_1L_2$, $L_3^2=L_2L_3-L_1L_3$ (verify these identities, which hold because $L_3=L_2-L_1$), substitute $(B-C)^2=L_3^2$, $(A-C)^2=L_2^2$, $(A-B)^2=L_1^2$ to get
$$
P_j=(s_x+s_y)\,L_2L_3-(s_x+s_z)\,L_1L_3+(s_y+s_z)\,L_1L_2 .
$$
This is exactly the tangent form $\sum_{h=1}^3 N_h\prod_{k\ne h}D_k$ with $D_1=L_1,\ D_2=L_2,\ D_3=L_3$ (affine) and $N_1=s_y+s_z,\ N_2=-(s_x+s_z),\ N_3=s_x+s_y$ (affine), and $\theta=0$. Hence $\mathrm{tChow}_{\pm}(\mathrm{MED}_j)\le 3$.

## Consequence (state — this is the point)

**An F4 (positivity) probe.** The denominators of this witness are the pairwise differences $L_1=A-B,\ L_2=A-C,\ L_3=B-C$, whose slope-sign patterns on the three blocks form a triangle, $A-B:(+,-,0)$, $A-C:(+,0,-)$, $B-C:(0,+,-)$. **No global input flip can make all three one-sided simultaneously** (it would require the three blocks pairwise oppositely oriented, which is impossible for three blocks), and the $2$-plane $\mathrm{span}(L_1,L_2)$ contains no nonzero one-sided affine form in the original coordinates. So the clean tangent witness above does **not** certify $H^{*}(\mathrm{MED}_j)\le3$. Yet $H^{*}\ge\mathrm{tChow}_{\pm}=3$, and a direct admissible-form search finds $H^{*}(\mathrm{MED}_j)=3$ for $2$-bit integers — so at least there, $H^{*}=\mathrm{tChow}_{\pm}=3$ (positivity is **free**), realized by *different* (admissible) denominators than the natural $L_h$. Whether the admissible order-$3$ form exists for all $n$ — i.e. whether the median is F4-free or the first positivity gap — is a concrete open instance of the central F4 question, sharply posed: a clean tChow witness exists, but its natural denominators are intrinsically inadmissible.

## Pitfalls

- $P_j$ is a sum of three products of affine forms ($s\cdot(\cdot)^2$ each a product of three affine factors), but the *tangent-form* certificate of order $3$ is the **pairwise** grouping in Step 2 ($\sum_h N_h\prod_{k\ne h}D_k$); show that explicit regrouping via $L_3=L_2-L_1$.
- The offsets $\tfrac14,\tfrac12$ are only to make $A,B,C$ distinct; argue that ties among the original integers do not change $\mathrm{MED}_j$ (tied integers share the $j$-th bit).
- Do **not** claim $H^{*}\le3$ from this construction: the denominators $L_h$ are not admissible, and admissibility is the whole content of $H^{*}$ vs $\mathrm{tChow}_{\pm}$ (F4). State the obstruction (the mixed-sign triangle) explicitly.
