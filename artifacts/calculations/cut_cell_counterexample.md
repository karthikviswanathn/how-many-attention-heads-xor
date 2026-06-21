# Cut-Cell Counterexample To Head Complexity

This note records a small counterexample to the idea that head complexity is the same as the number of affine cuts needed to put all positive cube vertices in one connected component.

## The affine cut-cell formulation

Given a Boolean function $f:\lbrace0,1\rbrace^k \to \lbrace0,1\rbrace$, define an affine cut-cell certificate to be a collection of affine hyperplanes in $\mathbb{R}^k$ such that one connected component of the complement contains exactly the vertices labeled $1$ and no vertices labeled $0$.

Equivalently, the positive vertices must be exactly the cube vertices lying in one open cell of a hyperplane arrangement.

This is a natural geometric measure, but it is not equal to $H^{\ast}(f)$.

## The example: three-bit parity

Let

$$ f(x_1,x_2,x_3)=x_1\oplus x_2\oplus x_3. $$

The vertices labeled $1$ are

$$ 100,\quad 010,\quad 001,\quad 111. $$

The vertices labeled $0$ are

$$ 000,\quad 110,\quad 101,\quad 011. $$

The four positive vertices form a tetrahedron. Four affine cuts suffice, namely the four facet inequalities

$$ x_1+x_2+x_3 \geq 1, \qquad x_1+x_2-x_3 \leq 1, \qquad x_1-x_2+x_3 \leq 1, \qquad -x_1+x_2+x_3 \leq 1. $$

These inequalities contain the four positive vertices and exclude the four negative vertices.

## Why three affine cuts cannot suffice

Take any one affine cut, and choose the side containing all four positive vertices. This side is convex.

Now take any two negative vertices. Their midpoint is also the midpoint of two positive vertices:

$$ \begin{aligned} \frac{000+110}{2} &= \frac{100+010}{2}, \qquad \frac{000+101}{2} = \frac{100+001}{2}, \qquad \frac{000+011}{2} = \frac{010+001}{2}, \\ \frac{110+101}{2} &= \frac{100+111}{2}, \qquad \frac{110+011}{2} = \frac{010+111}{2}, \qquad \frac{101+011}{2} = \frac{001+111}{2}. \end{aligned} $$

Since the chosen side contains all positive vertices, it contains each of these midpoints. If the same affine cut excluded two negative vertices, then by convexity the midpoint of those two excluded vertices would lie on the excluded side. That is impossible.

So each affine cut can exclude at most one of the four negative vertices. Therefore at least four affine cuts are needed.

Thus the affine cut-cell measure gives

$$ C_{\mathrm{cell}}(\mathrm{XOR}_3)=4. $$

## But head complexity is three

Three-bit parity is symmetric and its Hamming-weight truth table changes value at every adjacent Hamming weight:

$$ 0,\quad 1,\quad 2,\quad 3. $$

By the symmetric sign-change theorem,

$$ H^{\ast}(\mathrm{XOR}_3)=3. $$

Therefore

$$ C_{\mathrm{cell}}(\mathrm{XOR}_3)=4 \qquad \text{but} \qquad H^{\ast}(\mathrm{XOR}_3)=3. $$

So the affine cut-cell formulation is not equivalent to $H^{\ast}(f)$.
