---
title: Optimal low-memory rational matrix function approximation
author: '[Tyler Chen](https://chen.pw)'
description: We provide some new error bounds for the Lanczos methods for computing matrix functinos.
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---
\renewcommand{\vec}[1]{\mathbf{#1}}

This is a companion piece to the publication:

[bibtex]


## Why should I care?

[Matrix functions](./lanczos_function_CIF.html) have a myriad of applications in nearly every field of computational science. 
Among the most powerful algorithms for computing the product of a matrix function $f[\vec{A}]$ with a vector $\vec{b}$ are Krylov subspace methods such as the Lanczos method for matrix function approximation (Lanczos-FA). 
These algorithms accecss $\vec{A}$ only through matrix products $\vec{v} \mapsto \vec{A}\vec{v}$, and are therefore well suited for situations in which $\vec{A}$ is too large to store in fast memory.
However, for general matrix functions, the amount of storage required often grows linearly with the number of iterations, resulting in a computational bottleneck. 


## Introduction

If $f(x) = 1/x$, then $f[\vec{A}]\vec{b} = \mathbb{A}^{-1} \vec{b}$ corresponds to the solution of the linear system of equations $\vec{A} \vec{x} = \vec{b}$.
In this case, algorithms such as the conjugate gradient algorithm and the minimum residual algorithm can approximate $\vec{A}^{-1} \vec{b}$ using an amount of storage *independent* of the number of iterations taken.
For general functions, a range of techniques such as restarting [[]]() or two-pass Lanczos [[]]() have been developed which also do not require memory increasing with the number of iterations.
However, such methods have slower convergence or require more matrix-vector products than Lanczos-FA.


## Contributions of this paper

In this paper, we first describe a mathematical algorithms which outputs the *optimal* approximation to a rational matrix function.
Here optimal is with respect to a certain norm which depends on the rational function in question.
Both the conjugate gradient algorithm and the minimum residual algorithms are obtained as special cases of our optimal approximation.
We then give low-memory implementations of our optimal algorithm and of Lanczos-FA which do not require more storage as more iterations are run.\
Finally, we use this optimal approximation to derive (non-optimal) approximations to other matrix functions such the matrix-sign function.





