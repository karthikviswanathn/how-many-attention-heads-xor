# Quadratic Threshold Functions Can Require Linearly Many Heads

For a Boolean function $f : \{0,1\}^{n} \to \{0,1\}$, let $H^{\ast}(f)$ be the minimum number of heads in the one-layer softmax-attention model of `model.md` whose thresholded scalar output agrees with $f$ on the Boolean cube. Let $\deg_{\pm}(f)$ be the least degree of a real polynomial $p$ such that $p(x)>0$ whenever $f(x)=1$ and $p(x)<0$ whenever $f(x)=0$.

There are absolute constants $c>0$ and $n_0$ such that for every $n\geq n_0$ there exists a Boolean function $f_n : \{0,1\}^{n}\to\{0,1\}$ with

$$
f_n(x)=\mathbf{1}[q_n(x)>0]
$$

for some real polynomial $q_n$ of degree at most $2$, and satisfying

$$
\deg_{\pm}(f_n)=2
\qquad\text{and}\qquad
H^{\ast}(f_n)\geq c n.
$$

Equivalently, ordinary threshold degree can stay equal to $2$ while head complexity grows linearly in the number of input bits.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Do not reprove it.** It is Lemma 20, verified (iter 8). Point any duplicate request at `020_quadratic_ptf_head_separation.md`.
2. **For the writeup's citations,** attach the *method* to **Warren (1968)** + **Goldberg–Jerrum (1995)** / **Anthony–Bartlett (1999)** (counting) and to the **Shannon (1949)** non-constructive paradigm — the actual proof depends on neither Zuev nor Baldi–Vershynin (cite those as context only).
3. **State the $n^2$-vs-$n^3$ capacity gap explicitly** in the writeup — it is the one-line reason the separation is *linear*, and it tells the reader exactly how far Lemma 6 ($\deg_\pm\le H^\ast$) is from tight.
4. **Natural next target (genuinely open here):** push to higher degree — does $\deg_\pm=d$ admit $H^\ast=\Omega(n)$ (or $\omega(n)$)? The same counting (degree-$d$ PTFs $=2^{\Theta(n^{d+1})}$ vs $\tilde O(Hn^2)$) suggests $H^\ast$ could be forced to $\Omega(n^{d-1})$, which would be a stronger separation — worth handing to Codex as a new conjecture.
5. **If a named witness is ever wanted** (beyond the existence statement), lower-bound $\mathrm{tChow}_\pm$ via the Lemma 16 sandwich, or adapt Sanford–Hsu–Telgarsky's communication-complexity head bounds — real work, and unnecessary for the theorem as stated.
