---
title: '\sffamily \textbf{On the Convergence of Conjugate Gradient Variants in Finite Precision Arithmetic}'
author: '[Tyler Chen](https://chen.pw)'
mainfont: Georgia
sansfont: Lato
linkcolor: blue
header-includes: |
    \usepackage{sectsty}
    \allsectionsfont{\normalfont\sffamily\bfseries}
---

This is a companion piece to the publication:

    @article{greenbaum_liu_chen_19
        Author = {Anne Greenbaum, Hexuan Liu, and Tyler Chen}
        Title = {On the Convergence of Conjugate Gradient Variants 
                 in Finite Precision Arithmetic.}
        Howpublished = {In progress.}
        Year = {2019}
    }

A preprint will be on ArXiV in the near future.

## Why should I care?
Need new algorithms to deal with modern HPC architecture. But can't sacrifice accuracy. 

Take advantage of lower precision for ML type applications.
 
## Introduction
If you are not familiar with the Conjugate Gradient method, it may be worth reading [this page](../krylov/index.html) first.

The Conjugate Gradient algorithm is a widely used method for solving $Ax=b$ when $A$ is positive definite (all eigenvalues are positive). 

## Conjugate Gradient In Finite Precision

 - The CG algorithm can be derived by minimizing the $A$-norm of the error at each step.

## Numerical Problems

- introduction to floating points failing to be associative
- even worse in low precision
- give an example of error analysis for HSCG
 - full results in paper

## Avoiding Communication

- give example with inner product vs sparse matrix product
- derive CGCG and GVCG by replacing recurrences


## Concusion



