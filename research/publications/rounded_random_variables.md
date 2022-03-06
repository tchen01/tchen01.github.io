---
title: Non-asymptotic moment bounds for random variables rounded to non-uniformly spaced sets
author: '[Tyler Chen](https://chen.pw)'
description: We describe properties of random variables when rounded to finite precision
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---

This is a companion piece to the publication:

[bibtex]


## Why should I care?


Algorithms involving randomness have become commonplace, and in practice these algorithms are often run in finite precision.
As a result, some of their theoretical properties, based on the use of exact samples from given distributions, can no longer be guaranteed.
Even so, many randomized algorithms appear to perform as well in practice as predicted by theory [[HMT11](https://arxiv.org/abs/0909.4061)], suggesting that errors resulting from sampling such distributions in finite precision are often negligible.
At the same time, especially in the case of Monte Carlo simulations, it is not typically clear how to differentiate the possible effects of rounding errors from the effects of sampling error.
In fact, in many areas (such as the numerical solution to stochastic differential equations) this problem is typically addressed by ignoring the effects of rounding errors under the assumption that they are small [[KP92](https://www.springer.com/gp/book/9783540540625)].
However, with the recent trend towards lower precision computations in the machine learning [[VSM11](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/37631.pdf), [GAGN15](https://arxiv.org/abs/1502.02551), [WCBCG18](https://papers.nips.cc/paper/7994-training-deep-neural-networks-with-8-bit-floating-point-numbers.pdf), etc.] and scientific computing [[Ste73](https://www.elsevier.com/books/introduction-to-matrix-computations/stewart/978-0-08-092614-8), [Hig02](http://ftp.demec.ufpr.br/CFD/bibliografia/Higham_2002_Accuracy%20and%20Stability%20of%20Numerical%20Algorithms.pdf)] communities, and with the massive increase in the amount of data available, the foundational problems of understanding the effect of rounding errors on random variables and the interplay between rounding and sampling error have become increasingly important.

In this paper, we study the moments of a random variable induced by rounding a continous random variable to some discrete set.
We provide non-asymptotic bounds on the difference of the moments of these random varaibles.
The main result is to show that for continous random variables, the moments differ to second order in the spacing of the points in the set. 
In comparison, a naieve application of standard floating point bounds would show the moments differ to first order.


