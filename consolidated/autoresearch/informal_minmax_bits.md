# Problem: The bits of the minimum (and maximum) of two integers have head complexity two

## Background and definitions (self-contained)

For $z\in\{0,1\}^n$ write the integer value $I(z)=\sum_{i=0}^{n-1}2^i z_i$; note the $j$-th binary digit of $I(z)$ is exactly $z_j$. For $x,y\in\{0,1\}^n$ and $0\le j\le n-1$ define the **min-bit**
$$
\mathrm{MIN}_{n,j}(x,y)=\Big\lfloor \min(I(x),I(y))/2^j\Big\rfloor \bmod 2,
$$
and analogously $\mathrm{MAX}_{n,j}$ with $\max$ in place of $\min$.

**Established results (cite as given).**
- **(L42, one-sided product plus affine.)** For affine forms $A,B,g$ with $A$ **one-sided** (the coefficient of every variable in $A$ has a single fixed sign), the function $\mathrm{sign}(A(u)B(u)+g(u))$ has $H^{*}\le 2$.
- **(L15, negation closure.)** Flipping any input variable $u_k\mapsto 1-u_k$ leaves $H^{*}$ unchanged.
- **(Degree lower bound.)** $H^{*}(f)\ge \deg_{\pm}(f)$ (clearing the denominators of an $H$-head representation gives a sign-representing real polynomial of degree $\le H$). In particular $H^{*}(f)\ge 2$ whenever $f$ is **not** a linear threshold function.
- **(Antipode identity, L2.)** For any affine form $t$ and any four points with $P_{00}+P_{11}=P_{01}+P_{10}$, $\;t(P_{00})+t(P_{11})=t(P_{01})+t(P_{10})$.

## Claim to prove

For every $n$ and every $0\le j\le n-1$,
$$
H^{*}(\mathrm{MIN}_{n,j})\le 2,\qquad H^{*}(\mathrm{MAX}_{n,j})\le 2,
$$
and the value is **exactly $2$** for $0\le j\le n-2$ (it is $1$ for the top bit $j=n-1$, which equals $x_{n-1}\wedge y_{n-1}$ for $\min$ and $x_{n-1}\vee y_{n-1}$ for $\max$).

## Guidance (prove every step rigorously)

**Step 1 (the min-bit is a comparison-gated selection).** Since $\min(I(x),I(y))=I(x)$ if $I(x)\le I(y)$ and $I(y)$ otherwise, and $\lfloor I(z)/2^j\rfloor\bmod 2=z_j$,
$$
\mathrm{MIN}_{n,j}(x,y)=\begin{cases}x_j,& I(x)\le I(y),\\ y_j,& I(x)>I(y).\end{cases}
$$
(At ties $I(x)=I(y)$ we have $x=y$, so $x_j=y_j$ and either branch agrees.)

**Step 2 (an explicit quadratic sign-representation).** Let $d=I(x)-I(y)$ and define the degree-2 polynomial
$$
V(x,y)=(x_j-y_j)\big(\tfrac12-d\big)+(x_j+y_j-1).
$$
Verify $\mathrm{sign}(V)=2\,\mathrm{MIN}_{n,j}-1$ at every point, by the four cases of $(x_j,y_j)$ — and note the two summands are **never simultaneously nonzero** ($x_j-y_j=0\iff x_j=y_j\iff x_j+y_j-1=\pm1\neq0$):
- $x_j=y_j=1$: $V=0+1=1>0$; and $\mathrm{MIN}_{n,j}=1$ (both bits $1$). ✓
- $x_j=y_j=0$: $V=0-1=-1<0$; and $\mathrm{MIN}_{n,j}=0$. ✓
- $x_j=1,y_j=0$: $V=(\tfrac12-d)+0$, so $V>0\iff d<\tfrac12\iff d\le0\iff I(x)\le I(y)$; and $\mathrm{MIN}_{n,j}=x_j=1$ exactly when $I(x)\le I(y)$. ✓
- $x_j=0,y_j=1$: $V=-(\tfrac12-d)+0=d-\tfrac12$, so $V>0\iff d>\tfrac12\iff d>0\iff I(x)>I(y)$; and $\mathrm{MIN}_{n,j}=y_j=1$ exactly when $I(x)>I(y)$. ✓

**Step 3 (it is $\mathrm{sign}(AB+g)$ with $A$ one-sided after a flip).** Write $V=A\cdot B+g$ with $A=x_j-y_j$, $B=\tfrac12-d$, $g=x_j+y_j-1$ (all affine). The factor $A=x_j-y_j$ has slopes $+1,-1$ (mixed). Flip the single variable $y_j\mapsto z_j=1-y_j$ (L15, preserving $H^{*}$): then $A=x_j-(1-z_j)=x_j+z_j-1$, whose slopes are $+1,+1$ — **one-sided**. ($B,g$ remain affine.) By L42, $H^{*}(\mathrm{MIN}_{n,j})=H^{*}(\mathrm{sign}(AB+g))\le 2$.

**Step 4 (lower bound: the interior min-bit is not an LTF).** For $0\le j\le n-2$, exhibit four points with $P_{00}+P_{11}=P_{01}+P_{10}$ on which $\mathrm{MIN}_{n,j}$ takes the crossing pattern $0,1,1,0$. Concretely (any $j\le n-2$): set all coordinates to $0$ except — $P_{00}:y_j{=}1$; $P_{01}:x_{j+1}{=}1,\,y_j{=}1$; $P_{10}:x_j{=}1,\,y_{j+1}{=}1$; $P_{11}:x_j{=}1,\,x_{j+1}{=}1,\,y_{j+1}{=}1$. Then $P_{00}+P_{11}=P_{01}+P_{10}$ (each of $x_j,x_{j+1},y_j,y_{j+1}$ appears once on each side), and computing $\min$: $\mathrm{MIN}_{n,j}(P_{00})=0,\ \mathrm{MIN}_{n,j}(P_{01})=1,\ \mathrm{MIN}_{n,j}(P_{10})=1,\ \mathrm{MIN}_{n,j}(P_{11})=0$ — e.g. at $j=1,n=3$ these are $(x,y)=((0,0,0),(0,1,0)),((0,0,1),(0,1,0)),((0,1,0),(0,0,1)),((0,1,1),(0,0,1))$ with $\min$-values $0,2,2,4$ and bit $1$ equal to $0,1,1,0$. [The segments $[P_{00},P_{11}]$ and $[P_{01},P_{10}]$ share the midpoint $\tfrac12(P_{00}+P_{11})$, so no affine threshold separates $\{P_{00},P_{11}\}$ from $\{P_{01},P_{10}\}$; equivalently any affine $t$ has $t(P_{00})+t(P_{11})=t(P_{01})+t(P_{10})$ by L2, incompatible with a one-atom sign pattern of opposite signs on the two pairs.] Hence $\mathrm{MIN}_{n,j}$ is not an LTF, so $\deg_{\pm}\ge2$ and $H^{*}\ge2$. With Step 3, $H^{*}(\mathrm{MIN}_{n,j})=2$ for $0\le j\le n-2$.

**Step 5 (max, and the top bit).** For $\max$, the same argument with $V_{\max}=(x_j-y_j)(d+\tfrac12)+(x_j+y_j-1)$ gives $\mathrm{sign}(V_{\max})=2\,\mathrm{MAX}_{n,j}-1$ (now the selection is $x_j$ when $I(x)\ge I(y)$), and $A=x_j-y_j$ one-sided after the flip, so $H^{*}(\mathrm{MAX}_{n,j})\le 2$, $=2$ for $j\le n-2$ by the symmetric crossing certificate. The top bit $j=n-1$: $\min\ge 2^{n-1}\iff I(x)\ge 2^{n-1}\wedge I(y)\ge 2^{n-1}\iff x_{n-1}\wedge y_{n-1}$, an LTF ($H^{*}=1$); dually $\max$ gives $x_{n-1}\vee y_{n-1}$. $\blacksquare$

## Consequence (state briefly)

Taking the minimum or maximum of two integers — a comparison-gated *selection* of bits — costs only **two heads per output bit**, placing $\min/\max$ alongside integer comparison (one positive weighted sum) and addition (carry chain free) on the easy side of head complexity. The selection works precisely because the gate is a single comparison ($d=I(x)-I(y)$) and the two selected quantities are single literals $x_j,y_j$; this keeps the representing polynomial quadratic ($\mathrm{sign}(AB+g)$, $A$ one-sided), unlike an intersection of two *general* halfspaces (AND of two LTFs), which can have unbounded threshold degree.

## Pitfalls

- The two summands of $V$ are mutually exclusive in support, so $\mathrm{sign}(V)$ is unambiguous and $V$ never competes the comparison term against the bit-forcing term; verify this rather than choosing a large constant.
- $A=x_j-y_j$ is one-sided **only after** flipping $y_j$ (L15); state the flip, since L42 requires a one-sided $A$.
- The lower bound uses an **affine-parallelogram** crossing ($P_{00}+P_{11}=P_{01}+P_{10}$), the generalization of the coordinate checkerboard (L3) to a non-coordinate 2-flat — a plain 2-coordinate checkerboard does not exist for this function. Verify the four labels and the sum identity explicitly.
- The top bit is genuinely different (an LTF), so the "$=2$" claim is only for $j\le n-2$.
