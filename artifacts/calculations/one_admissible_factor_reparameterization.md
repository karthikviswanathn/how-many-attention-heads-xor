# One-Admissible-Factor Reparameterization

## Statement

Let $A,C,D,B$ be affine functions on $\lbrace0,1\rbrace^n$. Suppose $B$ is positive on the Boolean cube and all its slopes are strictly positive, or all its slopes are strictly negative. If

$$ Q=A D+C B, $$

then $Q$ is the cleared numerator of an exact two-head score.

More precisely, there is a positive integer $k$ such that

$$ E=D+kB $$

is positive on the Boolean cube and has the same strict slope orientation as $B$. For every such $k$,

$$ Q=A E+(C-kA)B, $$

and therefore

$$ \frac{A}{B}+\frac{C-kA}{E}=\frac{Q}{BE}. $$

In particular, every product of two affine functions is the cleared numerator of a two-head score.

## Proof

Write

$$ B(x)=b_0+\sum_{i=1}^{n}b_ix_i, \qquad D(x)=d_0+\sum_{i=1}^{n}d_ix_i. $$

Let $\sigma\in\lbrace-1,1\rbrace$ be the common sign of $b_1,\ldots,b_n$. The finite set of strict lower bounds

$$ k> -\frac{d_i}{b_i} \qquad (1\leq i\leq n) $$

ensures that every slope $d_i+kb_i$ has sign $\sigma$. Since $B(x)>0$ at every Boolean input, the finite set of strict lower bounds

$$ k> -\frac{D(x)}{B(x)} \qquad (x\in\lbrace0,1\rbrace^n) $$

ensures that $E(x)=D(x)+kB(x)>0$ everywhere on the cube. A positive integer larger than all these bounds exists.

The algebraic identity is immediate:

$$ A(D+kB)+(C-kA)B=AD+CB=Q. $$

Both $B$ and $E$ are admissible one-head denominators. Their product is positive, so the two-head score has exactly the sign of $Q$. $\blacksquare$

## Affine-product corollary

Let $L$ and $M$ be arbitrary affine functions. Choose any admissible affine $B$, set

$$ A=L, \qquad D=M, \qquad C=0, $$

and apply the statement. Thus every Boolean function sign-represented by $LM$ has head complexity at most two, in every dimension.

If $L$ and $M$ are strict affine threshold scores, then the XOR and XNOR of their threshold labels are sign-represented by $-LM$ and $LM$, respectively. Consequently, incompatible coordinatewise slope signs of the two threshold factors cannot yield a strict separation from two heads.

More precisely, every such XOR or XNOR is either constant, a nonconstant linear threshold function, or satisfies

$$ \deg_{\pm}(f)=H^{\ast}(f)=2. $$

Indeed, the product gives threshold degree and head complexity at most two. Outside the constant and linear-threshold cases, the exact one-head characterization and the definition of threshold degree give the matching lower bounds.

## Exact five-bit example

Take

$$ L=11+8x_1-16x_2-6x_3-10x_4-18x_5, $$

$$ M=15-6x_1+14x_2-12x_3-16x_4-16x_5. $$

The coordinatewise signs of the products of their slopes are

$$ (-1,-1,1,1,1), $$

so no common coordinate complementation makes both slope patterns one-sided. Nevertheless, choose

$$ B=1+x_1+x_2+x_3+x_4+x_5, \qquad k=17. $$

Then

$$ E=M+17B=32+11x_1+31x_2+5x_3+x_4+x_5. $$

Both $B$ and $E$ have strictly positive coefficients. The two-head score

$$ \frac{-L}{B}+\frac{17L}{E} $$

has cleared numerator

$$ (-L)E+(17L)B=-LM. $$

The sign pattern of $-LM$ is not affine threshold. An exact affine Farkas circuit is supported at the vertices with binary indices $3,8,19,24$, each with weight $1$. If $s(x)=\mathrm{sign}(-L(x)M(x))$, then

$$ \sum_{v\in\lbrace3,8,19,24\rbrace}s(v)(1,v_1,v_2,v_3,v_4,v_5)=0. $$

Thus this function has threshold degree exactly two and head complexity exactly two. The exact coefficient, denominator, and Farkas checks are reproduced by [`verify_one_admissible_factor_reparameterization.py`](verify_one_admissible_factor_reparameterization.py).
