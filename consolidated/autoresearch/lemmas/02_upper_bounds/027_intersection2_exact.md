# A 2-by-2 Intersection Function Has Head Complexity Exactly 2

## Statement

On $\lbrace 0,1\rbrace^4$, let

$$
f(x) = (x_1 \wedge x_2) \vee (x_3 \wedge x_4) = \mathbf{1}[\, x_1 x_2 + x_3 x_4 \geq 1\,].
$$

Then

$$
H^{*}(f) = 2.
$$

> A concrete *nonsymmetric* monotone function (it is not symmetric: $f(1,1,0,0)=1$ but $f(1,0,1,0)=0$, two inputs of Hamming weight $2$) with an exactly determined head complexity. It is the $s=2$ case of $\neg\mathrm{DISJ}_s = \mathbf{1}[\langle u,v\rangle \geq 1]$ (the OR of $s$ disjoint $2$-ANDs).

## Proof

**Upper bound.** $f$ is the OR of two positive monotone terms $x_1\wedge x_2$ and $x_3\wedge x_4$, so by the monotone-term DNF bound [014_monotone_term_dnf.md](014_monotone_term_dnf.md) with $s=2$, $H^{*}(f) \leq 2$.

**Lower bound.** $f$ is non-constant ($f(\mathbf 1)$-type points give $1$, $f(\mathbf 0)=0$). It is not an LTF: suppose $f(x) = \mathbf{1}[a_0 + \sum_i a_i x_i > 0]$. Evaluating $f$ at six points gives

$$
\begin{aligned}
f(1,1,0,0)=1 &\Rightarrow a_0+a_1+a_2 > 0, \\
f(0,0,1,1)=1 &\Rightarrow a_0+a_3+a_4 > 0, \\
f(1,0,1,0)=f(1,0,0,1)=f(0,1,1,0)=f(0,1,0,1)=0 &\Rightarrow a_0+a_i+a_j \leq 0 \ (i\in\lbrace1,2\rbrace, j\in\lbrace3,4\rbrace).
\end{aligned}
$$

(The last four points satisfy neither term, since each has exactly one of $\lbrace x_1,x_2\rbrace$ and one of $\lbrace x_3,x_4\rbrace$ set to $1$.) Adding the two strict inequalities gives $2a_0 + (a_1+a_2+a_3+a_4) > 0$; adding the four non-strict inequalities gives $4a_0 + 2(a_1+a_2+a_3+a_4) \leq 0$, i.e. $2a_0 + (a_1+a_2+a_3+a_4) \leq 0$, a contradiction. So $f$ is not an LTF, and by the one-head characterization [011_one_head_characterization.md](../01_foundations_and_normal_form/011_one_head_characterization.md), $H^{*}(f) \geq 2$. $\blacksquare$

## Consequence

The monotone-term DNF bound (L14) is tight here: a genuinely nonsymmetric function attains $H^{*} = s = 2$. Empirically (see `claude-comments/empirical_findings.md`), the larger members $\neg\mathrm{DISJ}_s$ keep $H^{*} = 2$ for $s = 2, 3$, while $s = 4$ ($n = 8$) is a candidate where positivity may strictly increase the count (an $H^{*} > \mathrm{tChow}_{\pm}$ gap); that remains a computational observation, not a theorem.
