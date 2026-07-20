# Four-Head Lower Bound for a Six-Bit Function

## The function

Let $x=(x_0,\ldots,x_5)\in\lbrace0,1\rbrace^6$ and encode it by

$$ \mathrm{code}(x)=\sum_{i=0}^{5}2^i x_i. $$

Coordinate $x_0$ is the least significant bit. Set

$$ E=\lbrace21,38,41\rbrace=\lbrace010101,100110,101001\rbrace, $$

where each displayed string is written as $x_5x_4\cdots x_0$. Define

$$ s_6(x)=(-1)^{x_0+\cdots+x_5}\left(1-2\mathbf 1_E(x)\right), $$

and let $f_6(x)=1$ exactly when $s_6(x)=1$. Thus $f_6$ is even parity with its value flipped exactly on the three vertices in $E$. Its truth table, with the output at code $c$ stored in bit $c$, is

```text
0x96696bd669b69669
```

## The head model

For this problem, a one-head scalar score is

$$ \phi_h(x)=\frac{N_h(x)}{D_h(x)}, $$

where

$$ N_h(x)=\eta_h+\sum_{i=0}^{5}\rho_{h,i}\alpha_h^{x_i}\left(m_{h,i}+\delta_hx_i\right), $$

$$ D_h(x)=\gamma_h+\sum_{i=0}^{5}\rho_{h,i}\alpha_h^{x_i}, $$

with

$$ \gamma_h>0,\qquad \rho_{h,i}>0,\qquad \alpha_h>0, $$

while $\eta_h$, $\delta_h$, and $m_{h,i}$ are arbitrary real numbers. The denominator is strictly positive on every Boolean input.

Define $H^{\ast}(f)$ to be the least $H$ for which there are $H$ such heads and a constant $c\in\mathbb R$ satisfying

$$ (2f(x)-1)\left(c+\sum_{h=1}^{H}\phi_h(x)\right)>0 $$

for every $x\in\lbrace0,1\rbrace^6$.

## Problem

Prove

$$ H^{\ast}(f_6)>4. $$

Equivalently, prove that for every choice of four valid heads and every $c\in\mathbb R$, there is an input $x\in\lbrace0,1\rbrace^6$ such that

$$ s_6(x)\left(c+\sum_{h=1}^{4}\frac{N_h(x)}{D_h(x)}\right)\leq0. $$

## Cleared-denominator form

Set $A_h=N_h$ and $B_h=D_h$. Since every $B_h$ is positive, the score has the same sign as

$$ P(x)=c\prod_{h=1}^{4}B_h(x)+\sum_{h=1}^{4}A_h(x)\prod_{\substack{j=1\\j\neq h}}^{4}B_j(x). $$

Thus it is enough to prove that every valid choice of $A_h$, $B_h$, and $c$ has some Boolean input satisfying

$$ s_6(x)P(x)\leq0. $$

Each $A_h$ and $B_h$ is affine on the Boolean cube. Every nonconstant $B_h$ has all variable slopes with the same sign, while $B_h$ is constant when $\alpha_h=1$. Therefore an even stronger sufficient result is to rule out the displayed sign representation when each $A_h$ is arbitrary affine and each $B_h$ is any positive affine function whose slopes are all nonnegative or all nonpositive.

A numerical search is not a proof. The required conclusion must hold for every real parameter choice, including constant-denominator and boundary cases.
