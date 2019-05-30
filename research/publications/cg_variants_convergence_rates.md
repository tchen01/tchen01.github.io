---
title: '\sffamily \textbf{On the Convergence of Conjugate Gradient Variants in Finite Precision Arithmetic}'
author: '[Tyler Chen](https://chen.pw)'
mainfont: Georgia
sansfont: Lato
header-includes: |
    \usepackage{sectsty}
    \allsectionsfont{\normalfont\sffamily\bfseries}
    \usepackage{xcolor}
    \definecolor{Base02}{HTML}{073662}
    \hypersetup{
      colorlinks,
      linkcolor=Base02,
      citecolor=Base02,
      urlcolor=Base02
    }
---

This is a companion piece to the publication:

[bibtex]

A preprint is available on arXiv: [https://arxiv.org/pdf/1905.05874.pdf](https://arxiv.org/pdf/1905.05874.pdf).

## Why should I care?

The behaviour of the conjugate gradient algorithm in [finite precision](../cg/finite_precision_cg.html) is very different than what is predicted by exact arithmetic theory.
In this sense, the algorithm could be considered unstable.
However, the conjugate gradient algorithm is widely used in practice, so it is important to understand its behaviour in finite precision.

## Introduction
If you are not familiar with the Conjugate Gradient method, it may be worth reading [this page](../cg/index.html) first.




## Contributions of this paper

In this paper we show (numerically) why on some problems certain variants of the conjugate gradient algorithm converge more slowly. 
