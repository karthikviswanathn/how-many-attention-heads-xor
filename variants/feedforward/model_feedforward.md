# Feed-Forward Model Variant

## Purpose

This file fixes the model variant used for the feed-forward branch. It keeps the same input format, embeddings, and one-layer attention map from [model.md](model.md), but changes the final classifier.

The attention-only model asks whether the query residual is linearly separable. In this variant, a feed-forward block of hidden width $2d_{\mathrm{model}}$ may act on the query residual before the final threshold.

## Attention Layer

Use exactly the attention layer from [model.md](model.md). For an input

$$ x \in \lbrace0,1\rbrace^n, $$

let

$$ r_{\mathrm{attn}}(x) := u_=(x) + \sum_{h=1}^{H} y^{(h)}(x) \in \mathbb{R}^{d_{\mathrm{model}}} $$

be the query-token residual after the attention update.

## Feed-Forward Readout

The feed-forward hidden width is fixed to be

$$ 2d_{\mathrm{model}}. $$

Let

$$ \mathrm{ReLU}(t) := \max\lbrace t,0\rbrace $$

coordinatewise. Choose feed-forward block parameters

$$ W_{\mathrm{up}} \in \mathbb{R}^{2d_{\mathrm{model}} \times d_{\mathrm{model}}}, \qquad b_{\mathrm{up}} \in \mathbb{R}^{2d_{\mathrm{model}}}, $$

$$ W_{\mathrm{down}} \in \mathbb{R}^{d_{\mathrm{model}} \times 2d_{\mathrm{model}}}, \qquad b_{\mathrm{down}} \in \mathbb{R}^{d_{\mathrm{model}}}. $$

The feed-forward block first forms the hidden activation

$$ h(x) := \mathrm{ReLU}\left(W_{\mathrm{up}} r_{\mathrm{attn}}(x) + b_{\mathrm{up}}\right), $$

then writes back to the residual stream:

$$ r_{\mathrm{ff}}(x) := r_{\mathrm{attn}}(x) + W_{\mathrm{down}} h(x) + b_{\mathrm{down}}. $$

Choose a final readout vector and threshold

$$ w \in \mathbb{R}^{d_{\mathrm{model}}}, \qquad \tau \in \mathbb{R}. $$

The raw scalar score is

$$ U(x) := w^\top r_{\mathrm{ff}}(x) - \tau. $$

Expanding the definitions gives

$$ \begin{aligned} U(x) &= w^\top r_{\mathrm{ff}}(x) - \tau \\ &= w^\top r_{\mathrm{attn}}(x) + \left(W_{\mathrm{down}}^\top w\right)^\top \mathrm{ReLU}\left(W_{\mathrm{up}} r_{\mathrm{attn}}(x) + b_{\mathrm{up}}\right) + w^\top b_{\mathrm{down}} - \tau. \end{aligned} $$

Now define the compact readout parameters

$$ a := w, \qquad c := W_{\mathrm{down}}^\top w, \qquad \beta := w^\top b_{\mathrm{down}} - \tau. $$

Then the same scalar score can be written as

$$ S_{\mathrm{ff}}(x) := a^\top r_{\mathrm{attn}}(x) + c^\top \mathrm{ReLU}\left(W_{\mathrm{up}} r_{\mathrm{attn}}(x) + b_{\mathrm{up}}\right) + \beta. $$

The term $a^\top r_{\mathrm{attn}}(x)$ is the direct residual branch.

The second term is the nonlinear feed-forward branch.

The scalar $\beta$ absorbs the output bias and final threshold.

| Symbol | Meaning |
| --- | --- |
| $r_{\mathrm{attn}}(x)$ | Query-token residual after the attention layer. |
| $W_{\mathrm{up}}$ | Matrix from the residual stream to the hidden layer. |
| $b_{\mathrm{up}}$ | Bias before the ReLU hidden layer. |
| $h(x)$ | ReLU hidden activation, with width $2d_{\mathrm{model}}$. |
| $W_{\mathrm{down}}$ | Matrix from the hidden layer back to the residual stream. |
| $b_{\mathrm{down}}$ | Feed-forward output bias. |
| $r_{\mathrm{ff}}(x)$ | Query-token residual after the feed-forward block. |
| $w$ | Final linear readout vector. |
| $\tau$ | Final threshold before absorbing constants into the score. |
| $a$ | Compact coefficient for the direct residual branch. |
| $c$ | Compact coefficient for the ReLU branch. |
| $\beta$ | Compact scalar bias after absorbing the output bias and threshold. |
| $S_{\mathrm{ff}}(x)$ | Final scalar score used for classification. |

The classifier outputs

$$ f(x) = 1 \qquad \Longleftrightarrow \qquad S_{\mathrm{ff}}(x) > 0. $$

Unused hidden units are allowed by setting their output coefficients to zero. There is no independent width parameter in this variant, but $d_{\mathrm{model}}$ itself is still chosen as part of the model.

## Computability And Feed-Forward Head Complexity

A Boolean function $f$ is **computable with $H$ heads in the feed-forward model** if there exist attention parameters and feed-forward readout parameters as above such that the resulting classifier agrees with $f$ on every input in $\lbrace0,1\rbrace^n$.

Define

$$ H_{\mathrm{ff}}^{\ast}(f) := \min \left\lbrace H : f \text{ is computable with } H \text{ heads in the feed-forward model} \right\rbrace. $$

## Consequence Of The Model Change

This change removes the linear-readout bottleneck. The threshold-degree lower bound and the linear-fractional normal form from the attention-only model do not apply after an arbitrary feed-forward block.

With hidden width $2d_{\mathrm{model}}$, the head-count invariant still collapses:

$$ H_{\mathrm{ff}}^{\ast}(f) = \begin{cases} 0 & \text{if } f \text{ is constant}, \\ 1 & \text{otherwise}. \end{cases} $$

The proof is recorded in [lemmas/02_feed_forward_variant/001_one_head_universality.md](lemmas/02_feed_forward_variant/001_one_head_universality.md).
