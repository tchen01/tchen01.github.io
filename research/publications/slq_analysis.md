---
title: Analysis of stochastic Lanczos quadrature for spectrum approximation
author: '[Tyler Chen](https://chen.pw)'
description: We analyze stochastic Lanczos quadrature for spectrum approximation
footer: <p class="footer">The rest of my publications can be found <a href="./../">here</a>.</p>
---

\(\newcommand{\vec}{\mathbf}
\newcommand{\bOne}{\unicode{x1D7D9}}
\newcommand{\PP}{{\mathbb{P}}}
\newcommand{\EE}{{\mathbb{E}}}
\newcommand{\ehat}{\hat{\vec{e}}}
\newcommand{\gq}[2]{[#2]_{#1}^{\textup{gq}}}
\newcommand{\W}{d_{\mathrm{W}}} 
\newcommand{\samp}[1]{\langle #1 \rangle}
\newcommand{\R}{\mathbb{R}}
\newcommand{\T}{{\textsf{T}}}
\)
This is a companion piece to the publication:

[bibtex]

Code available to help reproduce the plots in this paper is available on [Github](https://github.com/tchen01/..).

## Why should I care?

Computing the full spectrum of an \( n\times n \) symmetric matrix \( \vec{A} \) is intractable in many situations, so the spectrum must be approximated.
One way to do this is to approximate the cumulative empirical spectral measure (CESM) \( \Phi[\vec{A}] : \mathbb{R} \to [0,1] \), which is defined as the fraction of eigenvalues of \( \vec{A} \) less than a given threshold, i.e., \( \Phi[\vec{A}](x) := \sum_{i=1}^{n} \frac{1}{n} \bOne[ \lambda_i[\vec{A}]\leq x] \).
This is a probability distribution function which makes it a natural target for a "global" approximation.

Moreover, spectral sums \( \operatorname{tr}(f[\vec{A}]) \) can be computed as the Riemann--Stieltjes integral of \( f \) against \( \Phi[\vec{A}] \).
Many important tasks can be written as a spectral sum, so the task of estimating CESM arises frequently in such applications as well.


SLQ is by no means new and has somewhat recently been analyzed for computing spectral sums [[UCS17]](https://epubs.siam.org/doi/abs/10.1137/16M1104974).
However, despite being around for several decades, no real analysis of its convergence for spectrum approximation has appeared.
As a result practitioners have been relying on heuristics to justify their use of the algorithm.

## Introduction and algorithm overview

SLQ combines two basic ideas (i) Hutchinson style trace estimation and (ii) Gaussian quadrature.
It is fairly straightforward and can be written in several lines (given access to a method to compute the output of the Lanczos algorithm).

To begin, we define the weighted CESM,
\begin{align*}
    %\label{eqn:intro_estimator}
    \Psi[\vec{A},\vec{v}](x) := \vec{v}^\T \bOne[\vec{A} \leq x] \vec{v}.
\end{align*}
If \( \vec{v} \sim \mathcal{U}(\mathcal{S}^{n-1}) \), where \( \mathcal{U}(\mathcal{S}^{n-1}) \) is the uniform distribution on the unit sphere, then the weighted CESM has the desirable properties (i) that it is an unbiased estimator for \( \Phi[\vec{A}](x) \), and (ii) that it defines a cumulative probability distribution function; i.e. \( \EE[\Psi[\vec{A},\vec{v}](x)] = \Phi[\vec{A}](x) \) and \( \Psi[\vec{A},\vec{v}] : \R \to [0,1] \) is weakly increasing, right continuous, and
\begin{align*}
    \lim_{x\to-\infty} \Psi[\vec{A},\vec{v}](x) = 0%\vec{v}^\T\bOne[\vec{A} \leq x]\vec{v} = 0
    ,&&
    \lim_{x\to\infty} \Psi[\vec{A},\vec{v}](x) = 1.%\vec{v}^\T\bOne[\vec{A} \leq x]\vec{v} = 1,
\end{align*}

Next, we consider the degree \( k \) Gaussian quadrature rule \( \gq{k}{\Psi[\vec{A},\vec{v}]} \) for \( \Psi[\vec{A},\vec{v}] \).
In general, a Gaussian quadrature rule for a distribution function can be computed using the Stieltjes procedure, which for distributions of the form \( \Psi[\vec{A},\vec{v}] \), is equivalent to the Lanczos algorithm \cite{gautschi_04,golub_meurant_09}.
Specifically, if \( [\vec{T}]_{:k,:k} \) is the symmetric tridiagonal matrix obtained by running Lanczos on \( \vec{A} \) and \( \vec{v} \) for \( k \) steps, then
\begin{align*}
    \gq{k}{\Psi[\vec{A},\vec{v}]} = \Psi([\vec{T}]_{:k,:k},\ehat)
\end{align*}
where \(\ehat = [1,0,\ldots, 0]^{\T}\).

By repeating this process over multiple samples and averaging, we arrive at SLQ:

\begin{align*}
\hline
\hspace{1em}&\textbf{Algorithm 1 } \text{Stochastic Lanczos Quadrature}&
\\\hline
&\textbf{input } \vec{A}, n_{\textup{v}}, k
\\&\textbf{for } i=1,2,\ldots, n_{\textup{v}} \textbf{ do}
\\&\hspace{2em} \text{Sample \( \vec{v}_i \sim \mathcal{U}(\mathcal{S}^{n-1}) \) (and define \( \Psi_i = \Psi(\vec{A},\vec{v}_i) \))}
\\&\hspace{2em} \text{Run Lanczos on \( \vec{A},\vec{v}_i \) for \( k \) steps to compute \( [\vec{T}_i]_{:k,:k} \)}
\\&\hspace{2em} \text{Define  \( \gq{k}{\Psi_i} = \Psi[[\vec{T}_i]_{:k,:k},\ehat] \)}
\\&\textbf{return } \text{\( \samp{ \gq{k}{\Psi_i} } := \frac{1}{n_{\textup{v}}} \sum_{i=1}^{n_{\textup{v}}} \gq{k}{\Psi_i} \)}
\\\hline
\end{align*}


## Contributions of this paper

Our main theoretical result is a runtime guarantee for SLQ.
In particular, we show that if \( n_{\textup{v}} > 4 ( n+2 )^{-1} t^{-2} \ln(2n\eta^{-1}) \) and \( k > 12 t^{-1} \), then 
\begin{align*}
    \PP\big[ \W( \Phi[\vec{A}], \samp{\gq{k}{\Psi_i} } ) > t I[\vec{A}]  \big] < \eta,
\end{align*}
where \( I[\vec{A}] := | \lambda_{\textup{max}}[\vec{A}] - \lambda_{\textup{min}}[\vec{A}] | \) and \( \W(\cdot,\cdot) \) denotes the Wasserstein distance between two distribution functions.

This implies that as \( n\to\infty \), for \( t \gg  n^{-1/2}  \), SLQ has a runtime of \( O( T_{\textup{mv}} t^{-1} \log( t^{-2} \eta^{-1}) ) \).
This bound is nearly tight in the sense that for any \( t \in (0,1) \), there exists a matrix of size \( \lceil (4t)^{-1} \rceil \) such that at least \( (8t)^{-1} \) matrix vector products are required to obtain an output with Wasserstein distance less than \( t I[\vec{A}] \).

The second main result is an a posteriori upper bound for Wasserstein and Kolmogorov--Smirnov (KS) distances, which take into account spectrum dependent features such as clustered or isolated eigenvalues.
These results are obtained using the observation that a Gaussian quadrature intersects the distribution it aims to approximate \( 2k-1 \) times.
Using this, one can easily draw upper and lower bounds for the underlying distribution given a Gaussian quadrature rule.

Finally, in proving these results, we show that if \( n_{\textup{v}} > (n+2)^{-1} t^{-2}  \ln(2 \eta^{-1}) \) then, for any \( x\in\R \),
\begin{align}
    \label{eqn:intro_sample_ave}
    \PP \left[ \left| \Phi[\vec{A}](x) - \left( \frac{1}{n_{\textup{v}}}\sum_{i=1}^{n_{\textup{v}}} \vec{v}_i^\T \bOne[\vec{A} \leq x] \vec{v}_i \right) \right| > t \right] < \eta.
\end{align}
This is applicable to the analysis of a range of algorithms beyond SLQ.



