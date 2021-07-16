---
title: Lanczos Error Bounds
author: '[Tyler Chen](https://chen.pw)'
description: We provie some new error bounds for the Lanczos methods for computing matrix functinos.
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---
\renewcommand{\vec}[1]{\mathbf{#1}}

This is a companion piece to the publication:

[bibtex]


## Why should I care?


Computing the product of a matrix function \( f(\vec{A}) \) with a vector \( \vec{b} \), where \( \vec{A} \) is a symmetric matrix and $f : \mathbb{R} \to \mathbb{R}$ is a scalar function, is a fundamental task in many disciplines, including scientific computing and data science.
Perhaps the most well known example is when \( f(x) = 1/x \) in which case \( f(\vec{A}) \vec{b}  = \vec{A}^{-1} \vec{b} \) corresponds to solving a linear system of equations.
Other commonly used functions include the exponential and logarithm, square root, and sign function, which have applications such as differential equations, Gaussian process sampling, principle component projection/regression, quantum chromodynamics, eigenvalue counting \cite{di_napoli_polizzi_saad_16}, etc.

## Introduction

The Lanczos algorithm can be used to approximate \( f(\vec{A})\vec{b} \), and in the case that \( f(x) = 1/x \) and \( \vec{A} \) is positive definite, this approximation is [optimal](../cg/cg_lanczos.html) over Krylov subspace.
This case is very well studied and a range of error bounds and estimates exist.
However, for other functions, the standard bounds are often too pessimistic. 
In this paper we show how to reduce the error of approximating \( f(\vec{A})\vec{b} \) with the Lanczos algorithm to the error of solving a certain linear system with the Lanczos algorithm, thereby allowing us to leverage existing bounds for the convergence of Lanczos on linear systems.

