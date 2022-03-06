---
title: Low-memory Krylov subspace methods for optimal rational matrix function approximation
author: '[Tyler Chen](https://chen.pw)'
description: We introduce low-memory Krylov subspace methods for approximation rational matrix functions applied to a vector
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---
\renewcommand{\vec}[1]{\mathbf{#1}}

This is a companion piece to the publication:

[bibtex]


[Matrix functions](./lanczos_function_CIF.html) have a myriad of applications in nearly every field of computational science. 
Among the most powerful algorithms for computing the product of a matrix function $f[\vec{A}]$ with a vector $\vec{b}$ are Krylov subspace methods such as the Lanczos method for matrix function approximation (Lanczos-FA). 
These algorithms access $\vec{A}$ only through matrix products $\vec{v} \mapsto \vec{A}\vec{v}$, and are therefore well suited for situations in which $\vec{A}$ is too large to store in fast memory.
However, for general matrix functions, the amount of storage required often grows linearly with the number of iterations, resulting in a computational bottleneck. 

One notable function is $f(x) = 1/x$ in which case $f[\vec{A}]\vec{b} = \mathbb{A}^{-1} \vec{b}$ corresponds to the solution of the linear system of equations $\vec{A} \vec{x} = \vec{b}$.
In this case, algorithms such as the conjugate gradient algorithm and the minimum residual algorithm can approximate $\vec{A}^{-1} \vec{b}$ using an amount of storage *independent* of the number of iterations taken.
Moreover, these algorithms produce iterates which are *optimal* over Kylrov subspace, thereby guaranteeing fast convergence on matrices with spectrums which have nice properties like outlaying or clustered eigenvalues.


In this paper, we first describe a mathematical algorithms which outputs the optimal approximation to an arbitrary rational matrix function.
Here optimal is with respect to a certain norm which depends on the rational function in question.
We then give low-memory implementations of our optimal algorithm and of Lanczos-FA which do not require more storage as more iterations are run.
Finally, we use this optimal approximation to derive (non-optimal) approximations to other matrix functions such the matrix-sign function.
Both the conjugate gradient algorithm and the minimum residual algorithms are obtained as special cases of our optimal approximation, so this paper also provides some insights into the relationship between the algorithms.





