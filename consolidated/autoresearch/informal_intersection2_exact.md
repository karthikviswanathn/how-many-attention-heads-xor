# Problem: The 2-by-2 intersection function has head complexity exactly 2

## Background and definitions (self-contained)

Work on $\{0,1\}^4$. A function $A(x) = a_0 + \sum_i a_i x_i$ is **affine**; $f$ is a **linear threshold function (LTF)** if $f(x) = \mathbf{1}[A(x) > 0]$ for some affine $A$.

A **one-head atom** is $\phi(x) = \dfrac{\eta + \sum_i \rho_i \alpha^{x_i}(m_i + \delta x_i)}{\gamma + \sum_i \rho_i \alpha^{x_i}}$, $\gamma>0,\rho_i>0,\alpha>0$.

**Established results you may cite and use:**
- **(One-head characterization, L11.)** $H^{*}(f) \leq 1$ iff $f$ is constant or an LTF. Equivalently, a non-constant non-LTF function has $H^{*}(f) \geq 2$.
- **(Monotone-term DNF bound, L14.)** If $f$ is an OR of $s$ monotone terms (each a conjunction of literals of a single polarity), then $H^{*}(f) \leq s$.

Define

$$
f(x) = (x_1 \wedge x_2) \vee (x_3 \wedge x_4) = \mathbf{1}[\,x_1 x_2 + x_3 x_4 \geq 1\,].
$$

## Claim to prove

$$
H^{*}(f) = 2.
$$

(This is a genuinely nonsymmetric monotone function: it is not symmetric, since e.g. $f(1,1,0,0) = 1$ but $f(1,0,1,0) = 0$, two inputs of equal Hamming weight $2$.)

## Guidance (prove every step rigorously)

**Upper bound $H^{*}(f) \leq 2$.** $f$ is the OR of the two monotone (positive) terms $T_1 = x_1 \wedge x_2$ and $T_2 = x_3 \wedge x_4$. By the monotone-term DNF bound with $s = 2$, $H^{*}(f) \leq 2$.

**Lower bound $H^{*}(f) \geq 2$.** It suffices to show $f$ is not constant and not an LTF.

- Not constant: $f(1,1,0,0) = 1$ and $f(0,0,0,0) = 0$.
- Not an LTF: suppose for contradiction $f(x) = \mathbf{1}[a_0 + \sum_{i=1}^4 a_i x_i > 0]$. Write $A(x) = a_0 + \sum_i a_i x_i$. Use the values of $f$ at six specific points:
  - $f(1,1,0,0) = 1 \Rightarrow A(1,1,0,0) > 0$, i.e. $a_0 + a_1 + a_2 > 0$.
  - $f(0,0,1,1) = 1 \Rightarrow a_0 + a_3 + a_4 > 0$.
  - $f(1,0,1,0) = 0 \Rightarrow A(1,0,1,0) \leq 0$, i.e. $a_0 + a_1 + a_3 \leq 0$.
  - $f(1,0,0,1) = 0 \Rightarrow a_0 + a_1 + a_4 \leq 0$.
  - $f(0,1,1,0) = 0 \Rightarrow a_0 + a_2 + a_3 \leq 0$.
  - $f(0,1,0,1) = 0 \Rightarrow a_0 + a_2 + a_4 \leq 0$.

  (Verify each of these six function values directly from the definition of $f$: the first two points satisfy a full term; the last four satisfy neither term since each has exactly one of $\{x_1,x_2\}$ and one of $\{x_3,x_4\}$ set to $1$.)

  Add the two strict inequalities: $(a_0+a_1+a_2) + (a_0+a_3+a_4) > 0$, i.e.
  $$ 2a_0 + a_1 + a_2 + a_3 + a_4 > 0. $$
  Add the four non-strict inequalities:
  $$ (a_0+a_1+a_3)+(a_0+a_1+a_4)+(a_0+a_2+a_3)+(a_0+a_2+a_4) = 4a_0 + 2(a_1+a_2+a_3+a_4) \leq 0, $$
  i.e. $2a_0 + (a_1+a_2+a_3+a_4) \leq 0$. This directly contradicts the previous strict inequality $2a_0 + (a_1+a_2+a_3+a_4) > 0$. Hence no such affine $A$ exists, so $f$ is not an LTF.

Therefore $H^{*}(f) \geq 2$, and combined with the upper bound, $H^{*}(f) = 2$.

Give a complete, rigorous proof, verifying the six function values explicitly.
