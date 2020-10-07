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
Other commonly used functions include the exponential and logarithm, square root, and sign function, which have applications such as 
differential equations \cite{druskin_knizhnerman_89, saad_92}, 
Gaussian sampling \cite{pleiss_jankowiak_eriksson_damle_gardner_20},
principle component projection/regression \cite{frostig_musco_musco_sidford_16,allen_zhu_li_17,jin_sidford_19},
quantum chromodynamics \cite{eshof_frommer_lippert_schilling_van_der_vorst_02,davies_higham_05},
eigenvalue counting \cite{di_napoli_polizzi_saad_16}, etc. \cite{higham_08}.

## Introduction

In practice, the error of the Lanczos-FA approximation to \(f(\vec{A}) \vec{b}\) is close to optimal among all polynomial approximations of degree \(< k \).
If \( f(x) = 1/x \) and the error is measured in the \( \vec{A} \)-norm for some positive definite \( \vec{A} \), then Lanczos-FA is indeed optimal.
However, despite decades of research, similar optimality or near optimality results for a wider range of functions and norms remains limited to a few specific functions, and often involves constants which are overly pessimistic in practice.

In this paper we provide some additional
