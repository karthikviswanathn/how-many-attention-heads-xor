# Unrestricted Tangential-Chow Sandwich Bound

Let $f : \{0,1\}^n \to \{0,1\}$ and write $\sigma_f(x)=+1$ if $f(x)=1$ and $\sigma_f(x)=-1$ if $f(x)=0$. Let $H^{*}(f)$ be the least number of heads in the one-layer attention model of `model.md` computing $f$, with $H^{*}(f)=0$ for constant functions. Let $\deg_{\pm}(f)$ be the least degree of a real polynomial $p$ such that $\sigma_f(x)p(x)>0$ for every $x \in \{0,1\}^n$.

Define $\mathrm{tChow}_{\pm}(f)$ to be the least $H \geq 0$ for which there are affine forms $D_1,\ldots,D_H,N_1,\ldots,N_H$ on $\mathbb{R}^n$ and a scalar $\theta \in \mathbb{R}$ such that

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x)
$$

strictly sign-represents $f$ on the Boolean cube, meaning $\sigma_f(x)P(x)>0$ for all $x \in \{0,1\}^n$. For $H=0$, the product is $1$ and the sum is $0$.

Then

$$
\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{*}(f).
$$

Equivalently, unrestricted tangential-Chow threshold degree is an algebraic lower bound on head complexity that always dominates threshold degree.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Prove the target as a corollary, not from scratch:** cite **Lemma 14** ($H^*=\mathrm{MFdeg}_\pm$) and relax (admissible $\Rightarrow$ unrestricted) for $\mathrm{tChow}_\pm\le H^*$; reuse Lemma 14's own degree‑$\le H$ "Consequence" for $\deg_\pm\le\mathrm{tChow}_\pm$. Only the $H=0$ case needs explicit handling.
2. **Record the symmetric‑tightness collapse** $\deg_\pm=\mathrm{tChow}_\pm=H^*=C(F)$ (Minsky–Papert symmetrization + your Lemma 12) — it certifies the sandwich is sometimes exact and proves any separation must be nonsymmetric.
3. **Hunt for $\mathrm{tChow}_\pm>\deg_\pm$ at $H=2$** using the rank obstruction: a function whose only degree‑2 sign‑representers have full‑rank quadratic part (inner‑product‑type predicates) is the canonical candidate; this is where the Chow‑tangent constraint could bite.
4. **For strictness reasoning, pull dimension facts on $\tau(\mathrm{Chow}_H)$** from Landsberg (GSM 128, 2012) and the completely‑decomposable‑forms secant literature (Arrondo–Bernardi; Catalisano–Geramita–Gimigliano) — $\dim\sim 2H(n+1)$ vs $\binom{n+H}{H}$ is the heuristic that a gap *can* exist.
5. **If you later want to lower‑bound $H^*$ via this sandwich,** the leverage is threshold‑degree lower bounds (Sherstov's dual‑polynomial method, Bun–Thaler survey) feeding $\deg_\pm\le\mathrm{tChow}_\pm\le H^*$.
