# Coordinate Subcube Indicators Have One Head

Let $H^{\ast}(f)$ denote the minimum number of heads in the one-layer single-query softmax attention model from `model.md` whose final scalar threshold strictly computes $f$, with $H^{\ast}(f)=0$ allowed only for constant functions.

Let $P,N\subseteq\{1,\ldots,n\}$ be disjoint coordinate sets, and define the coordinate subcube indicator

$$
\chi_{P,N}(x)=\mathbf{1}\left[x_i=1\text{ for all }i\in P\text{ and }x_j=0\text{ for all }j\in N\right].
$$

If $P\cup N=\emptyset$, then $H^{\ast}(\chi_{P,N})=0$. If $P\cup N\neq\emptyset$, then

$$
H^{\ast}(\chi_{P,N})=1.
$$

Equivalently, every nontrivial conjunction of arbitrary signed literals is exactly a one-head function.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads

1. **Cite Lemma 11 directly:** $\chi_{P,N}$ is a nonconstant LTF $\Rightarrow H^\ast=1$; empty case is constant $\Rightarrow H^\ast=0$. One paragraph, done.
2. **The only lemma-worthy content** is the elementary "$\chi_{P,N}=\mathbf 1[\sum_P x_i-\sum_N x_j>|P|-\tfrac12]$, margin $1/2$" — state and verify this halfspace form, then invoke Lemma 11.
3. **For a from-scratch upper bound**, instantiate Lemma 11's "$\Leftarrow$" atom with $\beta=(+1\text{ on }P,-1\text{ on }N,0)$, $\beta_0=\tfrac12-|P|$; the single atom equals $L(x)$ over positive denominator.
4. **Lower bound** $H^\ast\ge1$: nonconstancy alone (zero-head $\iff$ constant), no need for threshold degree.
5. **Skip** Lemmas 17/18/29 and any selective-negation reduction for the mixed-polarity case — both are dead ends here.
