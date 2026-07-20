# Almost all Boolean functions need exponentially many heads

Let $H^{\ast}(f)$ denote the least number of heads needed by the one-layer attention model of `model.md` to compute a Boolean function $f : \{0,1\}^{n} \to \{0,1\}$, with final strict thresholding at the query token. There is an absolute constant $c>0$ such that, for a uniformly random Boolean function $f : \{0,1\}^{n} \to \{0,1\}$,

$$
\Pr\left[H^{\ast}(f) \geq c\frac{2^n}{n^2}\right] \to 1
$$

as $n\to\infty$. Consequently the worst-case head complexity satisfies

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f) \geq c\frac{2^n}{n^2},
$$

while Lemma 9 gives the universal upper bound

$$
\max_{f:\{0,1\}^{n}\to\{0,1\}} H^{\ast}(f) \leq 2^n-1.
$$

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Instantiate Lemma 19 at $H=\lfloor c\,2^n/n^2\rfloor$** with $c=1/(6C)$, $c'=1/2$ — this is the whole proof; bound $\log_2(H+1)\le n+1$ and compare $\tfrac12 2^n$ to $2^n$.
2. **Get the worst-case upper bound $H^*_{\max}(n)\le 2^n-1$ from Lemma 9** (universal weighted-sum bound) — cite it, don't reprove it.
3. **Derive the probabilistic form by dividing by $2^{2^n}$**: $\Pr[H^*(f)\le H]\le 2^{-c'2^n}$ — one line.
4. **Frame it as the Shannon–Lupanov / Muller counting lower bound** (Wegener §4, Jukna §1.4) for citation and intuition; note the $1/n^2$ vs $1/n$ comes from $\Theta(n)$ effective parameters per head.
5. **For references on the counting engine**, cite Warren (1968) and/or Goldberg–Jerrum (1995) + Anthony–Bartlett (1999) — but only as provenance for Lemma 19, which already does the work.

## Known results to build on (from literature survey)

## Actionable leads

1. **Cite Lemma 19 as the sole nontrivial input** and finish with the one-paragraph ratio argument above ($H=\lfloor c\,2^n/n^2\rfloor$, $|\mathcal F_{n,H}|/2^{2^n}\le 2^{(3Cc-1)2^n}\to 0$, take $c=1/(6C)$).
2. **Frame it explicitly as the Shannon (1949) counting argument**, the attention analogue of "almost all Boolean functions need $\Theta(2^n/n)$-size circuits"; the $/n^2$ vs $/n$ is the per-head ($\sim n^2$-bit) vs per-gate capacity.
3. **Note the optimization is forced**: $n+\log_2(H+1)\le 2n$ since $H\le 2^n$, so the $\log_2(H+1)$ term never matters and the threshold is exactly $2^n/n^2$.
4. **Do not touch Warren / Milnor–Thom / Pfaffian counting** — it is internal to Lemma 19 (which already handles the softmax via the cleared-denominator normal form, Lemmas 10/13/14/15).
5. **Optional next target**, not this one: a Lupanov-style $O(2^n/n^2)$-head *upper* bound to close the $\widetilde\Theta(n^2)$ gap against Lemma 9 — the genuine open question here.
