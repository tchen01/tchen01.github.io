---
title: Error bounds for Lanczos-based matrix function approximation
author: '[Tyler Chen](https://chen.pw)'
description: We provide some new error bounds for the Lanczos methods for computing matrix functinos.
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---
\renewcommand{\vec}[1]{\mathbf{#1}}

This is a companion piece to the publication:

[bibtex]



The Lanczos method for matrix function approximation (Lanczos-FA) can be used to approximate \( f(\vec{A})\vec{b} \), and in the case that \( f(x) = 1/x \) and \( \vec{A} \) is positive definite, this approximation is [optimal](../cg/cg_lanczos.html) over Krylov subspace.
This case is very well studied and a range of error bounds and estimates exist.
However, for other functions, the standard bounds are often too pessimistic as they do not take into account fine grained information about the spectrum of \( \vec{A} \) such as outlaying or clustered eigenvalues.
This makes it difficult to know when Lanczos-FA has reached a suitable accuracy for a given problem. 


In this paper we show how to reduce the error of approximating \( f(\vec{A})\vec{b} \) with Lanczos-FA to the error of solving a certain linear system with the Lanczos-FA.
This allows us to leverage the range of existing bounds for the convergence of Lanczos-FA on linear systems to easily obtain a priori and a posteriori bounds for other matrix functions. 
Our a posteriori bounds are highly accurate and can be used as practical stopping criteria. 


