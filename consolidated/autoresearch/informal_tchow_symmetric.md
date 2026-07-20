# Problem: Positivity is free for all symmetric functions

## Background and definitions (self-contained)

Fix $n\geq 1$, work on $\{0,1\}^n$. A function is **symmetric** if $f(x) = F(|x|)$ for some $F:\{0,\dots,n\}\to\{0,1\}$, where $|x|$ is the Hamming weight. Let $C(F)$ be the number of $k\in\{1,\dots,n\}$ with $F(k-1)\neq F(k)$ (sign changes along the weight axis).

$\deg_{\pm}(f)$ is the threshold degree. $\mathrm{tChow}_{\pm}(f)$ is the tangential-Chow sign-rank with arbitrary affine factors.

**Established results you may cite and use:**
- **(Symmetric exact value, L12.)** For symmetric $f$: $\deg_{\pm}(f) = C(F)$ and $H^{*}(f) = C(F)$. (In particular $\deg_{\pm}(f) = H^{*}(f) = C(F)$.)
- **(Sandwich, L18.)** For every $f$: $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$.

## Claim to prove

For every symmetric $f:\{0,1\}^n\to\{0,1\}$,

$$
\mathrm{tChow}_{\pm}(f) = H^{*}(f) = \deg_{\pm}(f) = C(F).
$$

In particular **the attention positivity/one-sided-slope constraints cost nothing on symmetric functions**: $\mathrm{tChow}_{\pm}(f) = H^{*}(f)$. (This extends the level-one base case to the entire symmetric class, a partial answer to whether positivity ever costs a head.)

## Guidance (prove every step rigorously)

1. By L12, $\deg_{\pm}(f) = C(F)$ and $H^{*}(f) = C(F)$, so $\deg_{\pm}(f) = H^{*}(f) = C(F)$.

2. By L18, $\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f)$.

3. Substituting Step 1 into Step 2 gives $C(F) \leq \mathrm{tChow}_{\pm}(f) \leq C(F)$, so $\mathrm{tChow}_{\pm}(f) = C(F)$.

4. Conclude $\mathrm{tChow}_{\pm}(f) = H^{*}(f) = \deg_{\pm}(f) = C(F)$, and in particular $\mathrm{tChow}_{\pm}(f) = H^{*}(f)$ (positivity is free for symmetric $f$).

Give a complete, rigorous proof. (It is a short sandwich-collapse argument; present each step explicitly.)
