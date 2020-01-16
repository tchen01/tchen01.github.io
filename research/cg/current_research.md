---
title: Current research on Conjugate Gradient and related Krylov subspace methods
author: '[Tyler Chen](https://chen.pw)'
keywords: ['applied','math']
description: The Conjugate Conjugate algorithm is a widely used method for solving Ax=b when A is positive definite. This page discusses some of the current research into CG, and closely related algorithms.
footer: <p class="footer">More about the conjugate gradient method can be found <a href="./">here</a>.</p>
...

Krylov subspace methods have remained an active area of research since they were first introduced. 
In general, research focuses on understanding convergence properties in finite precision, and on speeding up the runtime of algorithms.
I've included some topics below, but this should by no means be taken as a comprehensive list; I'm sure there are many important and interesting areas which don't show up here.


**find some citations and links**

## Preconditioners

Preconditioning linear systems is perhaps one of the oldest methods for improving convergence of iterative methods. 
The basic idea is to convert the system $Ax=b$ to one which is nicer to work with.
If $M^{-1}$ is full rank, then solving $Ax=b$ gives the same solution as solving,
$$
M^{-1}Ax = M^{-1} b
$$

If $M^{-1} = A^{-1}$ then this system is trivial to solve.
Of course, finding $A^{-1}$ is generally not easy, but if $M^{-1}$ "approximates" $A^{-1}$ in some way, then often $M^{-1}A$ will be much better conditioned than $A$, and so iterative methods will have better convergence properties.

Unfortunately, $M^{-1}A$ will probably not be Hermitian.
On the other hand, $R^{-1}AR^{-{\mathsf{H}}}$ is Hermitian positive definite if $A$ is Herimitian positive definite (here $R^{-{\mathsf{H}}} = (R^{-1})^{\mathsf{H}}$). Thus, we can solve the system,
$$
(R^{-1}AR^{-{\mathsf{H}}}) y = R^{-1}b
$$
for $y$, and then find $x$ by solving the system,
$$
R^{\mathsf{H}}x = y
$$

There is a lot of interest in developing new preconditioners, and understanding the theoretical properties of preconditioners.

## Multiple/reduced precision

Using lower precision (e.g. single, or float16 instead of doubles) means reduced storage, less communication, faster floating point arithmetic etc.
Perhaps more importantly, GPUs have been highly optimized for single precision floating point computations.

However, we have already seen that conjugate gradient can be significantly affected by [finite precision](./finite_precision_cg.html), so simply running the traditional algorithms in reduced precision will often lead to poor convergence.


## Avoiding communication 

I've already talked about some classic [communication hiding](./communication_hiding_variants.html) variants of the conjugate gradient algorithm.

Recently, I have introduced ["predict-and-recompute"](../publications/predict_and_recompute.html) conjugate gradient varaints.
These variants have similar parallelism to the standard communication hiding varaints, but better numerical properties.


### Blocked methods

If we have to solve multiple systems $Ax=b_1, Ax=b_2, \ldots$, then it makes sense to try to do these simultaneously so that we can reduce data movement.


## Applications to machine learning


## Computing matrix functions

Solving a linear system $Ax=b$ is a special case of the more general task of computing $x=f(A)b$ for some function $f$ (in the case of linear systems $f(x) = 1/x$.
The Lanczos method can be used approximate $f(A)b$ using information about $T_k$ and $Q_k$ at any step $k$.

