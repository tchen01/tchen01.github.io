---
title: Non-asymptotic moment bounds for random variables rounded to non-uniformly spaced sets
author: '[Tyler Chen](https://chen.pw)'
description: We describe properties of random variables when rounded to finite precision
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---

This is a companion piece to the publication:

[bibtex]

A preprint is available on [arXiv (2007.11041)](https://arxiv.org/abs/2007.11041).

\( 
\newcommand{\abs}[1]{\left|#1\right|}
\newcommand{\EE}{\mathbb{E}}
\newcommand{\d}{\mathrm{d}}
\newcommand{\flx}{{\lfloor{x}\rfloor}}
\newcommand{\clx}{{\lceil{x}\rceil}}
\newcommand{\flc}{{\lfloor{c}\rfloor}}
\newcommand{\clc}{{\lceil{c}\rceil}}
\newcommand{\err}{{\operatorname{err}}}
\newcommand{\rd}{{\operatorname{rd}}}
\)

## Why should I care?


Algorithms involving randomness have become commonplace, and in practice these algorithms are often run in finite precision.
As a result, some of their theoretical properties, based on the use of exact samples from given distributions, can no longer be guaranteed.
Even so, many randomized algorithms appear to perform as well in practice as predicted by theory [[HMT11](https://arxiv.org/abs/0909.4061)], suggesting that errors resulting from sampling such distributions in finite precision are often negligible.
At the same time, especially in the case of Monte Carlo simulations, it is not typically clear how to differentiate the possible effects of rounding errors from the effects of sampling error.
In fact, in many areas (such as the numerical solution to stochastic differential equations) this problem is typically addressed by ignoring the effects of rounding errors under the assumption that they are small [[KP92](https://www.springer.com/gp/book/9783540540625)].
However, with the recent trend towards lower precision computations in the machine learning [[VSM11](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/37631.pdf), [GAGN15](https://arxiv.org/abs/1502.02551), [WCBCG18](https://papers.nips.cc/paper/7994-training-deep-neural-networks-with-8-bit-floating-point-numbers.pdf), etc.] and scientific computing [[Ste73](https://www.elsevier.com/books/introduction-to-matrix-computations/stewart/978-0-08-092614-8), [Hig02](http://ftp.demec.ufpr.br/CFD/bibliografia/Higham_2002_Accuracy%20and%20Stability%20of%20Numerical%20Algorithms.pdf)] communities, and with the massive increase in the amount of data available, the foundational problems of understanding the effect of rounding errors on random variables and the interplay between rounding and sampling error have become increasingly important.

![**Figure 1.** *left*: original distribution.
*center*: distribution after being subjected to a nonlinear transformation $\varphi_1$; e.g. a distortion due to a lens.
*right*: center distribution after begin subjected to a discretization $\varphi_2$; e.g. discretization due to a measurement device.](imgs/finite_precision_random_variables/error_framework.svg)


## Introduction

Let \( \mathbb{F} \subset \mathbb{R} \) be a discrete set on which the rounded random variable will be supported, and for notational convenience define \( \clx := \min\{ z \in \mathbb{F} :  z \geq x \} \) and \( \flx := \max\{ z \in \mathbb{F} : z \leq x \} \).
We consider two rounding functions \( \rd : \mathbb{R} \to \mathbb{F} \) respectively defined by
\begin{align*}
    \text{round to nearest}
    &&
    \rd(x) 
    &:= \begin{cases}
        \flx, & x \leq \frac{1}{2}(\flx +  \clx )\\ 
        \clx, & x > \frac{1}{2}(\flx +  \clx )
    \end{cases}
    \\
    \text{stochastic rounding}
    &&
    \rd(x) 
    &:= \begin{cases}
        \flx, & \text{w.p. } 1 - (x-\flx)/(\clx - \flx ) \\ 
        \clx, & \text{w.p. } (x-\flx)/(\clx - \flx ).
    \end{cases}
\end{align*}
The first is the standard `round to nearest' scheme, which minimizes the distance between \( X \) and a random variable supported on \( \mathbb{F} \) in many metrics; e.g. "earth mover" distance, \( L^p \) norm, etc. The second is a randomized scheme which has gained popularity in recent years, particularly in machine learning


In principle, we could use this explicitly compute quantities such as \( \EE[\rd(X)] \), but it would be exceedingly tedious to perform a separate analysis for every finite precision number system \( \mathbb{F} \).
As such, as is common in numerical analysis, we will use the assumption that,
\begin{align*}
%    \label{eqn:bounded}
    \abs{\err(x)} = \abs{ \rd(x) - x } \leq \epsilon E(x)
\end{align*}
for some fixed function \( E : \mathbb{R} \to \mathbb{R}_{\geq 0} \) where we have defined
\begin{align*}
    \err(x) := \rd(x) - x.
\end{align*}
If \( E(x) = \abs{x} \) this bound is the standard bound for rounding to floating point number systems, and if \( E(x) = 1 \) this bound is the standard bound for fixed point systems; see for instance \cite{higham_02}.

From this bound it is essentially immediate that
\begin{align*}
    \abs{ \EE\!\left[X^{k}\right] - \EE\!\left[\rd(X)^{k}\right] } = O(\epsilon).
\end{align*}

## Results

Our main result is basically that these rounding schemes preserve the moments to order \( \epsilon^2 \).

**Theorem.**
_Suppose \( \EE[|X|^{k}] < \infty \) for some integer \( k > 0 \) and that \( x\mapsto x^{\alpha-1} f_X(x) \) has finitely many regions of local maxima for some \( K > 0 \),
Suppose further that \( E : \mathbb{R} \to \mathbb{R}_{\geq 0} \) is piecewise linear with a finite number of breakpoints._

_Then there exists a constant \( C > 0 \) such that, for all \( \epsilon \in(0,1) \) and \( (\mathbb{F},\rd) \) where \( \rd: \mathbb{R}\to\mathbb{F} \) corresponds to 'round to nearest' or 'stochatsic round' and satisfies \( | \rd(x) - x| < \epsilon E(x) \),
\begin{align*}
   \abs{ \EE\!\left[X^{k}\right] - \EE\!\left[\rd(X)^{k}\right] } < C \epsilon^2.
\end{align*}_

In addition, we have some sharper results for special cases. 
For instance, if \( \mathbb{F} \) has equally spaced points we can derive lower bounds and if \( \mathbb{F} \) corresponds to a sequence of points with "uniform clock behavior" we have asymptotic bounds.

**Definition.**
_Let \( \nu : [-1,1] \to \mathbb{R} \) be a continuous, non-vanishing, probability density function.
We say a sequence of sets of points \( \{ \{ p_{n,i} \}_{i=1}^{n} \}_{n=1}^{\infty} \) has uniform clock behavior with respect to \( \nu \) if
\begin{align*}
    \lim_{n\to\infty} \sup_{i<n} \{ | n ( p_{n,i+1} - p_{n,i} ) - \nu(p_{n,i})^{-1} | \} = 0.
\end{align*}_

**Theorem.** 
_Suppose that \( \{ \{ p_{j,i} \}_{i=1}^{j} \}_{j=1}^{\infty} \) has uniform clock behavior with respect to \( \nu \).
Let \( \rd_n : \mathbb{R} \to \{ p_{n,i} \}_{i=1}^{n} \) denote the rounding function to the \( n \)-th set and \( \err_n:\mathbb{R}\to\mathbb{R} \) the corresponding error function.
Then, for any \( [a,b] \subseteq [-1,1] \), as \( n\to\infty \),_

i. _if \( \rd:\mathbb{R}\to\mathbb{F} \) is 'round to nearest',_
        \begin{align*}  
            \abs{ \int_{a}^{b}  \abs{ \err_n(x) }^k \d{x} 
            - \left[ 2^{-k} e_{\rd}(k) \int_{a}^{b} \nu(x)^{-k} \d{x}  \right] \cdot n^{-k} } =  o(n^{-k}).
    \end{align*}
i. _if \( \rd:\mathbb{R}\to\mathbb{F} \) is 'stochastic round',_ 
         \begin{align*}  
             \abs{ \int_{a}^{b}  \EE_{\rd}\!\left[ \abs{ \err_n(x) }^k \right] \d{x} 
             - \left[ e_{\rd}(k) \int_{a}^{b} \nu(x)^{-k} \d{x}  \right] \cdot n^{-k} } =  o(n^{-k}).
        \end{align*}


Here \( e_{\rd} \) is a constant whose exact value is known but is not particularly important for the general intuition of the bound.
