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

$$ \mathrm{ReLU}(t) := \max\lbracet,0\rbrace $$

coordinatewise. Choose

$$ a \in \mathbb{R}^{d_{\mathrm{model}}}, \qquad A \in \mathbb{R}^{2d_{\mathrm{model}} \times d_{\mathrm{model}}}, $$

$$ b,c \in \mathbb{R}^{2d_{\mathrm{model}}}, \qquad \beta \in \mathbb{R}. $$

The scalar score is

$$ S_{\mathrm{ff}}(x) := a^\top r_{\mathrm{attn}}(x) + c^\top \mathrm{ReLU}\left(A r_{\mathrm{attn}}(x) + b\right) + \beta. $$

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
