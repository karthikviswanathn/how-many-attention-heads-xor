# Sign-Rank Method Limitations

## Statement

Let

$$
f:\{0,1\}^n\to\{0,1\}.
$$

The partition sign-rank lower-bound route from [028_restrictions_and_sign_rank.md](../02_complexity_measure_upper_bounds/028_restrictions_and_sign_rank.md) can certify

$$
H^{*}(f)\geq h+1
$$

only if there is a partition $I\sqcup J=\{1,\ldots,n\}$ such that

$$
2^{\min\{\lvert I\rvert,\lvert J\rvert\}}
>
\sum_{r=0}^{h}\binom{n}{r}.
$$

Consequently, this sign-rank route cannot certify

$$
H^{*}(f)\geq3
$$

for any Boolean function on at most $13$ input bits.

> **Interpretation.** The sign-rank lower-bound route is asymptotic and communication-flavored. It is not strong enough to separate two heads from three heads on small input dimensions, including the four-pair endpoint functions on eight bits.

## Proof

Fix a partition $I\sqcup J=\{1,\ldots,n\}$. The sign matrix of $f$ under this partition has size

$$
2^{\lvert I\rvert}\times2^{\lvert J\rvert}.
$$

Every real matrix of this size has rank at most

$$
2^{\min\{\lvert I\rvert,\lvert J\rvert\}}.
$$

Therefore the sign-rank also satisfies

$$
\operatorname{srank}_{I,J}(f)
\leq
2^{\min\{\lvert I\rvert,\lvert J\rvert\}}.
$$

The sign-rank lower-bound lemma can rule out $H$ heads only if

$$
\operatorname{srank}_{I,J}(f)
>
\sum_{r=0}^{H}\binom{n}{r}.
$$

Combining the two displays, any successful sign-rank proof ruling out $h$ heads must have

$$
2^{\min\{\lvert I\rvert,\lvert J\rvert\}}
>
\sum_{r=0}^{h}\binom{n}{r}.
$$

This proves the first claim.

For the second claim, set $h=2$. The best possible partition has

$$
\min\{\lvert I\rvert,\lvert J\rvert\}\leq\left\lfloor\frac{n}{2}\right\rfloor,
$$

so a necessary condition for proving $H^{*}(f)\geq3$ by this route is

$$
2^{\lfloor n/2\rfloor}
>
1+n+\binom{n}{2}.
$$

For every $n\leq13$,

$$
2^{\lfloor n/2\rfloor}
\leq
1+n+\binom{n}{2}.
$$

Thus no partition sign-rank argument of the form in [028_restrictions_and_sign_rank.md](../02_complexity_measure_upper_bounds/028_restrictions_and_sign_rank.md) can certify $H^{*}(f)\geq3$ on at most $13$ input bits. $\blacksquare$

## Consequence

The four-pair endpoint families $\mathrm{INT}_4$, $\mathrm{DISJ}_4$, $\mathrm{SUB}_4$, $\mathrm{NCON}_4$, $\mathrm{EQ}_4$, and $\mathrm{NEQ}_4$ live on eight input bits. Partition sign-rank cannot distinguish two heads from three heads for any eight-bit function, regardless of the partition.

For proving that a specific eight-bit function needs at least three heads, one must use a lower-bound mechanism stronger than the current threshold-degree and partition sign-rank tools.
