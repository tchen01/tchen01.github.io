---
title: Random Variables in Finite Precision
author: '[Tyler Chen](https://chen.pw)'
description: We describe properties of random variables when rounded to finite precision
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---

This is a companion piece to the publication:

[bibtex]

A preprint will be available soon.

## Why should I care?



Algorithms involving randomness have become commonplace, and in practice these algorithms are often run in finite precision.
As a result, some of their theoretical properties based on the use of exact samples from continuous distributions, can no longer be guaranteed.
Even so, many randomized algorithms appear to perform as well in practice as predicted by theory [[HMT11]](https://arxiv.org/abs/0909.4061), suggesting that errors resulting from sampling such distributions in finite precision are negligible.
At the same time, especially in the case of Monte Carlo simulations, it is not typically clear how to differentiate the possible effects of rounding errors from the effects of sampling error.
In fact, in many areas (such as the numerical solution to stochastic differential equations) this problem is typically addressed by ignoring the effects of rounding errors under the assumption that they are small [[KP92]](https://www.springer.com/gp/book/9783540540625).
However, with the recent trend towards lower precision computations, and with the massive increase in the amount of data available, understanding the effects of rounding errors on random variables and the interplay between rounding and sampling error has become increasingly important.


## Introduction

The effects of rounding random variables to a fixed set is an old problem in statistics.
In fact, this problem was studied as early as the late 1890s by Shepard, who gave the relationship between the moments of a random variable $X$ (satisfying certain niceness conditions) and the moments of a perturbed random variable $X^*$, obtained by rounding $X$ to a uniformly spaced set [She97].


![**Figure 1.** *left*: original distribution.
*center*: distribution after being subjected to a nonlinear transformation $\varphi_1$; e.g. a distortion due to a lens.
*right*: center distribution after begin subjected to a discretization $\varphi_2$; e.g. discretization due to a measurement device.](imgs/error_framework.svg)


More broadly, given some random variable $X$, we may consider a perturbed random variable $X^*=X+e(X)$, where $e:\mathbb{R}\to\mathbb{R}$ satisfies certain assumptions.
For instance, we may assume that $|e(x)| \leq \epsilon |x|$ as is common in numerical analysis, or that $e(x) = \lfloor x + 1/2\rfloor - x$; i.e. $e(x)$ is the difference between the nearest integer and $x$.


Based on these assumptions, we can derive information about properties of $X$ and $X^*$ and how they differ.
For instance, we may want to know how close the moments of $X^*$ are to those are of $X$.

For instance, given that $|e(x)| \leq \epsilon |x|$, it is trivial to show,
\begin{align*}
    \left| \mathbb{E} \left[X^k - (X^*)^k \right] \right|
    \leq \epsilon \mathbb{E}\big[ |X|^k \big]
\end{align*}


## Techniques 

Suppose we would like to compute the difference in the means of $X$ and $X^*$.
We have,
\begin{align*}
    \mathbb{E}[X^*-X] 
    = \mathbb{E}[e(X)] 
    = \int e(x) f_X(x) \mathrm{d}x
\end{align*}

Now, if we know $e(x)$ and $f_X(x)$, then we can simply evaluate this integral (possibly numerically).
However, in many situations, it is tedious to work with $e(x)$, even if we know it.
For instance, the $e(x)$ corresponding to rounding to some finite precision number system would be quite tricky to deal with.

Even so, we expect this integral to be small if $f_X(x)$ is relatively well behaved.
This is because $e(x)$ is positive about as much as it is negative.
Indeed, as Figure 2 shows, the integral of $e(x)$ over any interval is small.

![**Figure 2.** Sample error function](imgs/error_odd.svg)


In this paper we provide a technique to bound integrals of the form $\int fg \mathrm{d}x$ given that the integral of $g$ is small on any interval.
The previous example can be viwed as an appliation of the following proposition.

**Proposition**. 
Let $f: \mathbb{R} \to \mathbb{R}_{\geq 0}$ be lower semi-continuous and $g:\mathbb{R} \to \mathbb{R}$ integrable. 
    Suppose that $fg$ is absolutely integrable and that there exists a function $h : \mathbb{R} \times \mathbb{R} \to \mathbb{R}_{\geq 0}$ such that for any $a,b\in\mathbb{R}$,
\begin{align*}
    \int_{a}^{b} g(x) \,\mathrm{d}{x}
    \leq h(a,b)        
\end{align*}

Let $\mathcal{O} \subset 2^\mathbb{R}$ denote the set of all open subsets of $\mathbb{R}$.
Recall that any open set $A \in \mathcal{O} \setminus \{ \varnothing \}$ can be writen $A = \bigcup_{i=1}^{k} (a_i,b_i)$ where $(a_i,b_i)$ are pairwise disjoint and $k \in \mathbb{Z}_{>0} \cup \{\infty\}$.
Extend $h : \mathbb{R} \times \mathbb{R} \to \mathbb{R}_{\geq 0}$ to a function $\mu : \mathcal{O} \to \mathbb{R}_{\geq 0} \cup \{ \infty \}$ on open sets by $\mu(\varnothing) = 0$ and,
\begin{align*}
    \mu(A)
    = \mu\left( \bigcup_{i=1}^{k} (a_i,b_i) \right)
    = \sum_{i=1}^{k} h(a_i,b_i)
    ,&& \forall A \in \mathcal{O} \setminus \{ \varnothing \} 
\end{align*}

Then, 
\begin{align*}
    \int f(x) g(x) \,\mathrm{d}{x} 
    \leq \int_{0}^{\infty} \mu ( \{ x : f(x) > u\} ) \,\mathrm{d}{u}
\end{align*}

