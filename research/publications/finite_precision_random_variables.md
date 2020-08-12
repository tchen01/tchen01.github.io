---
title: Random Variables in Finite Precision
author: '[Tyler Chen](https://chen.pw)'
description: We describe properties of random variables when rounded to finite precision
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---

This is a companion piece to the publication:

[bibtex]

A preprint is available on [arXiv (2007.11041)](https://arxiv.org/abs/2007.11041).

## Why should I care?


Algorithms involving randomness have become commonplace, and in practice these algorithms are often run in finite precision.
As a result, some of their theoretical properties, based on the use of exact samples from given distributions, can no longer be guaranteed.
Even so, many randomized algorithms appear to perform as well in practice as predicted by theory [[HMT11](https://arxiv.org/abs/0909.4061)], suggesting that errors resulting from sampling such distributions in finite precision are often negligible.
At the same time, especially in the case of Monte Carlo simulations, it is not typically clear how to differentiate the possible effects of rounding errors from the effects of sampling error.
In fact, in many areas (such as the numerical solution to stochastic differential equations) this problem is typically addressed by ignoring the effects of rounding errors under the assumption that they are small [[KP92](https://www.springer.com/gp/book/9783540540625)].
However, with the recent trend towards lower precision computations in the machine learning [[VSM11](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/37631.pdf), [GAGN15](https://arxiv.org/abs/1502.02551), [WCBCG18](https://papers.nips.cc/paper/7994-training-deep-neural-networks-with-8-bit-floating-point-numbers.pdf), etc.] and scientific computing [[Ste73](https://www.elsevier.com/books/introduction-to-matrix-computations/stewart/978-0-08-092614-8), [Hig02](http://ftp.demec.ufpr.br/CFD/bibliografia/Higham_2002_Accuracy%20and%20Stability%20of%20Numerical%20Algorithms.pdf)] communities, and with the massive increase in the amount of data available, the foundational problems of understanding the effect of rounding errors on random variables and the interplay between rounding and sampling error have become increasingly important.

![**Figure 1.** *left*: original distribution.
*center*: distribution after being subjected to a nonlinear transformation $\varphi_1$; e.g. a distortion due to a lens.
*right*: center distribution after begin subjected to a discretization $\varphi_2$; e.g. discretization due to a measurement device.](imgs/error_framework.svg)


## Introduction

It would be exceedingly tedious to perform a separate analysis for every finite precision number system $\mathbb{F}$ and perturbation function $\operatorname{rd} : \mathbb{R} \to \mathbb{F}$.
This was recognized by numerical analysts decades ago.
To simplify analysis, they adopted the following standard assumption from which most numerical analysis results are derived.

**Assumption 1**.
size of rounding error is bounded:

i. $| \operatorname{rd}(x) - x | \leq \epsilon|x|$
i. $| \operatorname{rd}(x) - x | \leq \delta$

Using this assumption we can trivially derive the following result on the convergence in mean of $\operatorname{rd}(X) \to X$.

**Theorem 1** (1st order strong convergence).
Suppose $(\mathbb{F}, \operatorname{rd})$ satisfies Assumption 1. Then, for any real valued random variable $X$ with finite $k$-th moment,

i. $| \mathbb{E}[ \operatorname{rd}(X) - X |^k ] = \mathcal{O}( \epsilon^k )$
i. $| \mathbb{E}[ \operatorname{rd}(X) - X |^k ] = \mathcal{O}( \delta^k )$

The form of this theorem is reminiscent of Assumption 1. 
This is not surprising, as it is essentially the same as applying Assumption 1 pointwise to the value of X corresponding to each outcome in X's sample space.
However, it allows us to trivially generalize a wide range of numerical analysis results to the random variable case.

Similarly, we have that centered moments converge linearly. 
We denote the $k$-th centered moment of $Y$ by $\mathbb{M}_k[Y] := \mathbb{E}[ |Y - \mathbb{E}[Y]|^k ]$.

**Theorem 2** (1st order convergence of moments).
Suppose $(\mathbb{F}, \operatorname{rd})$ satisfies Assumption 1. Then, for any real valued random variable $X$ with finite $k$-th moment,

i. $| \mathbb{M}_k[\operatorname{rd}(X)] - \mathbb{M}_k[X] | = \mathcal{O}( \epsilon )$
i. $| \mathbb{M}_k[\operatorname{rd}(X)] - \mathbb{M}_k[X] | = \mathcal{O}( \delta )$.


## Main result

Roughly speaking, the main result is that Theorem 2 can be improved to *quadratic* in $\epsilon$ and $delta$ for a wide range of distributions.

Suppose we would like to compute the difference in the means of $X$ and $\operatorname{rd}(X)$.
We have,
\begin{align*}
    \mathbb{E}[\operatorname{rd}(X)-X] 
    = \mathbb{E}[\operatorname{err}(X)] 
    = \int \operatorname{err}(x) f_X(x) \mathrm{d}x
\end{align*}

Now, if we know $\operatorname{err}(x)$ and $f_X(x)$, then we can simply evaluate this integral (possibly numerically).
However, in many situations, it is tedious to work with $\operatorname{err}(x)$, even if we know it.
For instance, the $\operatorname{err}(x)$ corresponding to rounding to some finite precision number system would be quite tricky to deal with.

Even so, we expect this integral to be small if $f_X(x)$ is relatively well behaved.
This is because $\operatorname{err}(x)$ is positive about as much as it is negative.
Indeed, as Figure 2 shows, the integral of $\operatorname{err}(x)$ over any interval is small.

![**Figure 2.** Sample error function](imgs/error_odd.svg)


In this paper we provide a technique to bound integrals of the form $\int fg \mathrm{d}x$ given that the integral of $g$ is small on any interval.
The previous example can be viewed as an application of the following proposition.

**Lemma**. 

Let $f: \mathbb{R} \to \mathbb{R}_{\geq 0}$ be lower semi-continuous and $g:\mathbb{R} \to \mathbb{R}$ integrable. 
Suppose that $fg$ is absolutely integrable and that there exists a function $G : \mathbb{R} \times \mathbb{R} \to \mathbb{R}_{\geq 0}$ such that for any $a,b\in\mathbb{R}$,
\begin{align*}
    \int_{a}^{b} g(x) \mathrm{d}{x}
    \leq G(a,b)
\end{align*}

Let $\mathcal{O} \subset 2^\mathbb{R}$ denote the set of all open subsets of $\mathbb{R}$.
Recall that any open set $A \in \mathcal{O} \setminus \{ \varnothing \}$ can be writen $A = \bigcup_{i=1}^{k} (a_i,b_i)$ where $(a_i,b_i)$ are pairwise disjoint and $k \in \mathbb{Z}_{>0} \cup \{\infty\}$.
Extend $G : \mathbb{R} \times \mathbb{R} \to \mathbb{R}_{\geq 0}$ to a function $\mu : \mathcal{O} \to \mathbb{R}_{\geq 0} \cup \{ \infty \}$ on open sets by $\mu(\varnothing) = 0$ and,
\begin{align*}
    \mu(A)
    = \mu\left( \bigcup_{i=1}^{k} (a_i,b_i) \right)
    = \sum_{i=1}^{k} G(a_i,b_i)
    ,&& \forall A \in \mathcal{O} \setminus \{ \varnothing \} 
\end{align*}
Then, 
\begin{align*}
    \int f(x) g(x) \mathrm{d}{x} 
    \leq \int_{0}^{\infty} \mu ( \{ x : f(x) > u\} ) \mathrm{d}{u}.
\end{align*}

## Applications

### Balancing sampling error and measurement error 


Often, one would like to estimate statistics about a random variable by repeatedly sampling said random variable.
For instance, if $X_1, \ldots, X_n$ are independent and identically distributed (iid) samples of $X$, then the sample mean $Z := (X_1 + \cdots + X_n) / n$ provides an estimate for the true mean $\mathbb{E}[X]$ in the sense that
\begin{align*}
    \mathbb{P}[ | Z - \mathbb{E}[X] | > t ] \leq \frac{\mathbb{V}[X]}{n t^2}.
\end{align*}


In practice, sampling $X$ necessarily incurs some sort of measurement errors.
These could be due to discretization, biases in the measurement device, random noise, unknown non-linear effects, etc.
Intuitively, there is some balance between sampling error and measurement error; if only a few samples are taken then sampling error will dominate, and conversely, if a large number of samples are taken then measurement error will dominate.
Our analysis provides several ways to relate the moments of a perturbed random variable $\operatorname{rd}(X)$ to those of the underlying random variable $X$, based on various amounts of information about the perturbation $\operatorname{rd}$ and random variable $X$.
We can use these bounds to balance measurement error and sampling error.

It is easy to imagine scenarios in which more measurements can be taken provided that they are done less accurately.
For instance, recording data in half precision instead of double precision would allow four times as many data points to be saved (per unit storage), and less accurate sensors be produced more cheaply.
Naturally then, we may hope to optimize the cost subject to an accuracy constraint, the accuracy subject to a cost constraint, or some combination of the two.
Such a trade off for discretization error was explored in [[Wil05](https://sci-hub.tw/10.1016/j.measurement.2004.08.005)].
However, the analysis is based on Sheppard's corrections, and is therefore not generally applicable, due to niceness constraints on the density of the random variable to be measured, as well as the fact that measurements errors are not soley due to discretization.

Using our analysis, it is straightforward to show that we can ensure that our sample mean $Z:=(\operatorname{rd}(X_1) + \cdots + \operatorname{rd}(X_n))/n$ is within $c$ standard deviations of the true mean with probability $1-p$ by taking $n > 1 / (pc^2)$ iid samples of $X$ with maximum absolute measurement error,
\begin{align*}
    \delta 
    \leq
    \frac{c\sqrt{np} - 1}{\sqrt{np}+1} \sqrt{\mathbb{V}[X]}.
\end{align*}

### Generalizing numerical analysis results

Theorem 1 can be easily used to generalize many standard numerical analysis results from the scalar variables to random variable case.

For instance, suppose $X_1, \ldots, X_k$ are random variables.
Fix an ordering and let $S_k = X_1 + \cdots + X_k$, and let $\tilde{S}_k = X_1 \oplus \cdots \oplus X_k$.
\begin{align*}
    \mathbb{E}[ | S_n - \tilde{S}_n | ]
    &\leq \left[ \sum_{k=1}^{n-1} \sum_{i=1}^{k+1} \mathbb{E}[ | X_i | ] \right] \cdot \epsilon + \mathcal{O}(\epsilon^2)
    \\&\leq (n-1) \left[ \sum_{i=1}^{n} \mathbb{E}[ | X_i | ] \right] \cdot \epsilon + \mathcal{O}(\epsilon^2).
\end{align*}

