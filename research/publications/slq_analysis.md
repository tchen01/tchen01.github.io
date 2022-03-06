---
title: Analysis of stochastic Lanczos quadrature for spectrum approximation
author: '[Tyler Chen](https://chen.pw)'
description: We analyze stochastic Lanczos quadrature for spectrum approximation
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---


This is a companion piece to the publication:

[bibtex]

Code available to help reproduce the plots in this paper is available on [Github](https://github.com/tchen01/..).


Computing the full spectrum of an \( n\times n \) symmetric matrix \( \mathbf{A} \) is intractable in many situations, so the spectrum must be approximated.
One way to do this is to approximate the cumulative empirical spectral measure (CESM), which is defined as the fraction of eigenvalues of \( \mathbf{A} \) less than a given threshold.
This is a probability distribution function which makes it a natural target for a "global" approximation.
Moreover, spectral sums \( \operatorname{tr}(f[\mathbf{A}]) \) can be computed as the Riemann--Stieltjes integral of \( f \) against the CESM.
Many important tasks can be written as a spectral sum, so the task of estimating CESM arises frequently in such applications as well.

In this paper, we analyze an algorithm called stochastic Lanczos quadrature (SLQ) for the task of spectrum approximation.
SLQ is by no means new and has somewhat recently been analyzed for computing spectral sums [[UCS17]](https://epubs.siam.org/doi/abs/10.1137/16M1104974).
However, despite being around for several decades, no real analysis of its convergence for spectrum approximation has appeared.
As a result practitioners have been relying on heuristics to justify their use of the algorithm.

Our main theoretical result is an a priori runtime guarantee for SLQ.
The second main result is an a posteriori upper bound for Wasserstein and Kolmogorov--Smirnov distances, which take into account spectrum dependent features such as clustered or isolated eigenvalues.
These results are obtained using the observation that a Gaussian quadrature intersects the distribution it aims to approximate \( 2k-1 \) times.
Using this, one can easily draw upper and lower bounds for the underlying distribution given a Gaussian quadrature rule.
