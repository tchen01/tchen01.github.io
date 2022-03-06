---
title: Predict-and-recompute conjugate gradient variants
author: '[Tyler Chen](https://chen.pw)'
description: We introduce a new class of communication hiding conjugate gradient variants.
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---

This is a companion piece to the publication:

[bibtex]


The conjugate gradient algorithm (CG) is very popular for solving positive definite linear systems $\mathbf{A}\mathbf{x}=\mathbf{b}$.
CG is popular for many reasons including low storage costs and the fact you don't need to be able to actually represent $\mathbf{A}$, only to be able to evaluate the product $\mathbf{v}\mapsto \mathbf{A}\mathbf{v]$.
While these properties make CG an attractive choice for solving very large sparse (lots of zeros in $\mathbf{A}$) systems, the standard implementation of the conjugate gradient algorithm requires that nearly every computation be done sequentially. 
In particular, it requires two inner products and one (often sparse) matrix vector product per iteration, none of which can occur simultaneously. 
Each inner product requires global communication (meaning all the processors you use have to talk to one another), and the matrix vector product (if sparse) requires local communication.
Communication (moving data between places on a computer) takes time, and on supercomputers, is the biggest thing slowing down the conjugate gradient algorithm.
In the past others have come up with version of the CG algorithm which take less time per iteration by reducing communication.
I've written a bit about some of those variants [here](../cg/communication_hiding_variants.html).

However, it's well known that CG behaves *very* differently in finite precision than it does in exact arithmetic.
Understanding why this happens is a hard problem, and only a few results have been proved about it.
I've written an introduction to the effects of finite precision on CG [here](../cg/finite_precision_cg.html), but to summarize, the main effects are (i) the loss of ultimately attainable accuracy and (ii) the increase in number of iterations to reach a given level of accuracy (delay of convergence).
Unfortunately, many of the past communication hiding variants do not always work well numerically.
We would therefore like to develop variants which reduce communication (and therefore the time per iteration), while simultaneously ensuring that their numerical stability is not too severely impacted (so that the number of iterations required is not increased too much).


The primary contributions of this paper are several new mathematically equivalent CG variants, which perform better than their previously studied counterparts.
A general framework for constructing these methods is presented.
More importantly, the idea to use predictions of quantities to allow a computation to begin, and then recomputing these quantities at a later point (an idea originally due to Meurant) is applied to the "pipelined" versions of these variants.
Despite the advances presented in this paper,  there is still significant room for  future  work  on  high  performance  conjugate  gradient  variants,  especially  in  the direction of further decreasing the communication costs.


