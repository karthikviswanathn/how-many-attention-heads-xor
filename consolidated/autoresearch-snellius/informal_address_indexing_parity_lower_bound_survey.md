## Bottom line up front

The target is **correct and essentially already proved by your existing lemma stack** — it is a two-line corollary, not new mathematics. The only genuine content is the classical observation that the indexing function is *universal under restriction*, and that observation is immediate from the definition $\mathrm{IND}_m(a,y)=y_a$. Concretely:

- Fixing the $2^m$ table coordinates to $y_b=g(b)$ and keeping the $m$ address coordinates free yields the restriction $a\mapsto \mathrm{IND}_m(a,g)=g(a)$, i.e. **exactly $g$**. This is the textbook "the $2^m$-to-1 multiplexer realizes any $m$-bit function by loading its truth table into the data lines" (Shannon expansion / lookup-table realization).
- **Lemma 26/27 (subcube restriction monotonicity)** then gives $H^\ast(g)\le H^\ast(\mathrm{IND}_m)$ for every $g$, hence $H^\ast(\mathrm{IND}_m)\ge\max_g H^\ast(g)$.
- **Lemma 8 / Lemma 12 (exact parity, $H^\ast(\mathrm{XOR}_m)=m$)** with $g=\mathrm{XOR}_m$ gives $H^\ast(\mathrm{IND}_m)\ge m$.

The target's own sketch cites precisely the two load-bearing lemmas. There is **no subtlety** to flag beyond checking that Lemma 26/27's "fix coordinates + relabel the rest" covers the identity embedding of the $m$ address positions into the $n=m+2^m$ positions (it does, by construction). I would tell the lead: this is safe to write up quickly; the risk is not in the proof but in *under-stating* the result (see "free upgrade" below).

## What the object is (names, communities, references)

The function in the target is one of the most-studied objects in complexity theory, under several names:

- **Multiplexer / MUX** (digital logic, circuit complexity) — the $2^m$-to-1 selector.
- **Storage access function $\mathrm{SA}_m$** — Ingo Wegener, *The Complexity of Boolean Functions* (1987) and *Branching Programs and BDDs* (2000); the canonical hard example for branching-program/BDD separations.
- **Index / INDEX / IDX** (communication complexity) — Kushilevitz & Nisan, *Communication Complexity* (1997). It is *the* canonical separation in one-way and streaming models: one-way randomized CC of INDEX is $\Theta(2^m)$ (Ablayev 1996; Kremer–Nisan–Ron 1999 — *uncertain on exact attributions/years*), proved via VC-dimension / information cost. Miltersen–Nisan–Safra–Wigderson (1995/98, "asymmetric communication complexity / richness") popularized it for data-structure lower bounds.
- **Addressing function** (cell-probe / branching programs).

The single most relevant classical fact for your target is the **universality (completeness) of the multiplexer under restriction**: *every $m$-variable Boolean function is a subfunction of $\mathrm{IND}_m$.* This is folklore, in any of the above texts. It is exactly why IND inherits a lower bound from the *hardest* $m$-bit function in any restriction-monotone measure.

## The technique: restriction-monotonicity + a universal function

The proof pattern is the standard **subfunction (restriction) method**: if $g$ is a restriction of $f$ and a complexity measure $\mu$ cannot increase under restriction, then $\mu(f)\ge\mu(g)$. Nearly every natural measure is restriction-monotone (circuit/formula size, decision-tree depth, real degree, threshold degree, sign-rank, communication complexity). Your **Lemma 26/27 supplies exactly this for $H^\ast$**, so the machinery you need is already in the stack.

Distinguish this from its more famous *random*-restriction cousins — Subbotovskaya (1961, formula shrinkage / parity), Håstad's switching lemma (1986, $\mathrm{AC}^0$). Those use random restrictions to *simplify* a function; here you use a single *structured deterministic* restriction (load $g$'s truth table) to *embed* an arbitrary $g$. Same family, but you do not need the probabilistic switching-lemma machinery — just the deterministic universality.

## Established vs. open; the threshold-degree contrast

- **Established (high confidence):** $H^\ast(\mathrm{IND}_m)\ge m$ — a clean corollary, as above. Two independent routes:
  - **Route A (direct, matches the target):** Lemma 26/27 + Lemma 8.
  - **Route B (via threshold degree):** Lemma 6 ($\deg_\pm\le H^\ast$) + restriction-monotonicity of $\deg_\pm$ + Lemma 7 ($\deg_\pm(\mathrm{XOR}_m)=m$; the "order" of parity is $m$, in the spirit of Minsky–Papert, *Perceptrons*, 1969).

- **Free upgrade (the valuable insight):** the target's *general* inequality $H^\ast(\mathrm{IND}_m)\ge\max_{g}H^\ast(g)$ combined with **Lemma 24/25** ($\max_{g:\{0,1\}^m\to\{0,1\}}H^\ast(g)=\Omega(2^m/m^2)$) gives, *with literally the same argument*,
$$H^\ast(\mathrm{IND}_m)=\Omega(2^m/m^2)=\tilde\Omega(N),\qquad N=m+2^m.$$
The $\ge m$ bound (XOR witness) is exponentially weaker; just swap the witness $g$ from $\mathrm{XOR}_m$ to "a hard $g$ guaranteed by Lemma 24/25." This is fully rigorous (you only need one hard $g$ to exist).

- **Why this matters — an exponential separation, stronger than Lemmas 20/22/23.** The multilinear extension $\mathrm{IND}_m=\sum_b y_b\prod_i\big(a_ib_i+(1-a_i)(1-b_i)\big)$ has total degree $m+1$ and *exactly* represents IND, so $\deg_\pm(\mathrm{IND}_m)\le m+1=O(\log N)$, while $H^\ast(\mathrm{IND}_m)=\tilde\Omega(N)$. That is an **exponential gap between head complexity and threshold degree** — far beyond the *linear-vs-2* separations currently recorded (Lemmas 20/22/23). Note Route B (threshold degree, Lemma 6) is *capped at $m+1$* and therefore **cannot** see this; only the direct restriction route (Lemma 26/27 + Lemma 24/25) does. I'd flag this to the lead as the headline the target is really a gateway to.

- **Open / not settled by the current stack:** a good *upper* bound on $H^\ast(\mathrm{IND}_m)$. Lemma 9 only gives the useless $2^N-1$. IND $=\bigvee_b(y_b\wedge[a=b])$ is a $2^m$-term DNF, but the subcube anchors $b$ use *different polarities*, so Lemma 17/18 (same-polarity DNF) do **not** directly apply. The exponential *separation* claim does not need this upper bound (it only uses the $H^\ast$ lower bound and the $\deg_\pm$ upper bound), but a matching $\tilde O(2^m)$ upper bound for $H^\ast(\mathrm{IND}_m)$ looks like a genuine open sub-question.

- Sidebar (tangential, different measure): sign-rank of index/Hadamard-type matrices, Forster (2002), $\ge\sqrt{2^m}$. Not the same invariant as $H^\ast$; mention only if you later relate $H^\ast$ to sign-rank.

## On the Mathlib hits

**All four search batches are irrelevant.** This target is informal Boolean-function-complexity work, and Mathlib has no theory of threshold degree, head complexity, or the indexing function. The closest items are red herrings: `Profinite.NobelingProof.ProjRestrict` (restriction on `Set (I→Bool)`, but profinite topology, not complexity), `List.idxOf` / `Combinatorics.Line.apply_some` (list/line indexing, not $\mathrm{IND}_m$), and the generic `Monotone.*` / `monotone_restrict` lemmas (no Boolean-complexity content). The relevant "library" here is **your own lemma stack**, not Mathlib. (If you ever formalize the cube-restriction bookkeeping, `Combinatorics.HalesJewett`/`Combinatorics.Line` is the nearest structured-restriction API, but it is not needed.)

## Actionable leads

1. **Write the proof via Lemma 26/27 + Lemma 8**, using the one-line universality fact "$\mathrm{IND}_m$ restricted to $y=\text{truth table of }g$ is exactly $g$." This is the whole proof; it matches the target's sketch.
2. **State the stronger bound for free:** swap the witness to a hard $g$ from **Lemma 24/25** to get $H^\ast(\mathrm{IND}_m)=\Omega(2^m/m^2)$ — same argument, exponentially stronger conclusion.
3. **Record the separation:** $\deg_\pm(\mathrm{IND}_m)\le m+1$ (exact multilinear extension) vs. $H^\ast(\mathrm{IND}_m)=\tilde\Omega(2^m)$ — an exponential $H^\ast$-vs-$\deg_\pm$ gap, strictly stronger than Lemmas 20/22/23.
4. **Verify the one hinge:** that Lemma 26/27's "fix coordinates + relabel" legitimately produces $g$ on the $m$ address positions out of the $n=m+2^m$ positions (identity relabel; should be immediate).
5. **Note as open:** a non-trivial upper bound on $H^\ast(\mathrm{IND}_m)$ — Lemma 17/18 do not apply (mixed-polarity subcube anchors), so $\tilde O(2^m)$ is not yet in hand.
