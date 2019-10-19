---
title: On the Convergence of Conjugate Gradient Variants in Finite Precision Arithmetic
author: '[Tyler Chen](https://chen.pw)'
description: Multiple mathematically equivalent variants of the Conjugate Gradient algorithm have been developed to reduce communication in high performance environments. We analyze these variants in the context of [Greenbaum 89].
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---

This is a companion piece to the publication:

[bibtex]

A preprint is available on [arXiv (1905.05874)](https://arxiv.org/pdf/1905.05874.pdf).

## Why should I care?

The behaviour of the conjugate gradient algorithm in [finite precision](../cg/finite_precision_cg.html) is very different than what is predicted by exact arithmetic theory.
In this sense, the algorithm could be considered unstable.
However, the conjugate gradient algorithm is widely used in practice, so it is important to understand its behaviour in finite precision.

## Introduction

If you are not familiar with the Conjugate Gradient method, it may be worth reading through my introduction [here](../cg/index.html).

As mentioned above, the conjugate gradient algorithm in finite precision is very different than the algorithm in exact arithmetic.
One effect is that in finite precision the "rate of convergence" (how many iterations it takes to reach a given level of accuracy) is reduced compared to exact arithmetic.
Previously Anne Greenbaum showed that a "good" implementation of the CG algorithm, when run in finite precision, will behave like exact CG applied to a larger matrix, and that this larger matrix has eigenvalues very near to those of the original matrix.
I've written more about this result [here](../cg/finite_precision_cg.html).

A natural question is whether any of the high performance variants satisfy the conditions for Greenbaum's analysis to apply.
Specifically, the analysis requires that (i) the three term Lanczos recurrence close to satisfied, and (ii) that successive residual vectors are nearly orthogonal.
Unforunately, nobody has been able to prove this for any of the high performance variants, or even the standard implementation.


## Contributions of this paper

In this paper we show (numerically) why on some problems certain variants of the conjugate gradient algorithm converge more slowly than others, but on some problems all variants behave the same.
To do this we first analyze how closely different variants satisfy the three term Lanczos recurrence.
It turns out that the standard implementation, and one due to Chronopoulos and Gear satisfy the three term recurrence to within local rounding errors.
However, the pipelined variant due to Ghysels and Vanroose, which is more parallel, has a larger deviation from a three term recurrence.
While the paper does not prove that this leads to worse convergence, it does suggest that 
