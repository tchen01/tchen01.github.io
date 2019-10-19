---
title: An Introduction to Modern Analysis of the Conjugate Gradient Algorithm in Exact and Finite Precision
author: '[Tyler Chen](https://chen.pw)'
keywords: ['applied','math']
description: The Conjugate Conjugate algorithm is a widely used method for solving Ax=b when A is positive definite. This website provides an introduction to the algorithm in theorey and in practice.
footer: <p class="footer">More about the conjugate gradient method can be found <a href="./">here</a>.</p>
mainfont: Vollkorn
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


<!--start_pdf_comment-->
This is the first piece from a series on the conjugate gradient algorithm. It is still very much a work in progress, so please bear with me while it's under construction.
I have split up the content into the following pages:

- [Introduction to Krylov subspaces](./)
- [Arnoldi and Lanczos methods](./arnoldi_lanczos.html)
- [Derivation of CG](./cg_derivation.html)
- [CG is Lanczos in disguise](./cg_lanczos.html)
- [Error bounds for CG](./cg_error.html)
- [Finite precision CG](./finite_precision_cg.html)
- [Communication Hiding CG variants](./communication_hiding_variants.html)
- [Current Research](./current_research.html)

All of the pages have been compiled into a single [pdf document](./cg.pdf) to facilitate offline reading. At the moment the PDF document is nearly identical to the web version, so some links are not working. I will eventually turn the PDF into a more self contained document with proper references to external sources.

The following are some supplementary pages which are not directly related to conjugate gradient, but somewhat related:

- [The Remez Algorithm](./remez.html)

The intention of this website is not to provide a rigorous explanation of the topic, but rather, to provide some (hopefully useful) intuition about where this method comes from, how it works in theory and in practice, and what people are currently interested in learning about it.
I do assume some linear algebra background (roughly at the level of a first undergrad course in linear algebra), but I try to add some refreshers along the way. My hope is that it can be a useful resources for undergraduates, engineers, tech workers, etc. who want to learn about some of the most recent developments in the study of conjugate gradient (i.e. communication avoiding methods work).

If you are a bit rusty on your linear algebra I put together a [refresher](./linear_algebra_review.html) on some of the important concepts for understanding this site.
For a more rigorous and much broader treatment of iterative methods, I suggest Anne Greenbaum's [book](https://epubs.siam.org/doi/book/10.1137/1.9781611970937?mobileUi=0u) on the topic.
A popular introduction to conjugate gradient in exact arithmetic written by Jonathan Shewchuk can be found [here](./https://www.cs.cmu.edu/~quake-papers/painless-conjugate-gradient.pdf).
Finally, for a much more detailed overview of modern analysis of the Lanczos and conjugate gradient methods in exact arithmetic and finite precision, I suggest Gerard Meurant and Zdenek Strakos's [report](https://www.karlin.mff.cuni.cz/~strakos/download/2006_MeSt.pdf).

<!--end_pdf_comment-->

## Motivation
Solving a linear system of equations $Ax=b$ is one of the most important tasks in modern science.
A huge number of techniques and algorithms for dealing with more complex equations end up, in one way or another, requiring repeatedly solving linear systems.
As a result, applications such as weather forecasting, medical imaging, and training neural nets all rely on methods for efficiently solving linear systems to achieve the real world impact that we often take for granted.
When $A$ is symmetric and positive definite (if you don't remember what that means, don't worry, I have a refresher below), the conjugate gradient algorithm is a very popular choice for methods of solving $Ax=b$.

This popularity of the conjugate gradient algorithm (CG) is due to a couple factors. First, like most Krylov subspace methods, CG is *matrix free*. 
This means that $A$ never has to be explicitly represented as a matrix, as long as there is some way of computing the product $v\mapsto Av$, for a given input vector $v$.
For very large problems, this means a big reduction in storage, and if $A$ has some structure (eg. $A$ comes from a DFT, difference/integral operator, is very sparse, etc.), it allows the algorithm to take advantage of fast matrix vector products.
Second, CG only requires $\mathcal{O}(n)$ storage to run, as compared to $\mathcal{O}(n^2)$ that many other algorithms require (we use $n$ to denote the size of $A$, i.e. $A$ has shape $n\times n$). 
When the size of $A$ is very large, this becomes increasingly important.

While the conjugate gradient algorithm has many nice theoretical properties, its behavior in finite precision can be *extremely* different than the behavior predicted by assuming exact arithmetic.
Understanding what leads to these vastly different behaviors has been an active area of research since the introduction of the algorithm in the 50s.
The intent of this document is to provide an overview of the conjugate gradient algorithm in exact precision, then introduce some of what is know about it in finite precision, and finally, present some modern research interests into the algorithm.

## Measuring the accuracy of solutions
One of the first question we should ask about any numerical method is, *does it solve the intended problem?* In the case of solving linear systems, this means asking *does the output approximate the true solution?* 
If not, then there isn't much point using the method. 

Let's quickly introduce the idea of the *error* and the *residual*.
These quantities are both useful (in different ways) for measuring how close the approximate solution $\tilde{x}$ is to the true solution $x^* = A^{-1}b$.

The *error* is simply the difference between $x^*$ and $\tilde{x}$.
Taking the norm of this quantity gives us a scalar value which measures the distance between $x^*$ and $\tilde{x}$.
In some sense, this is perhaps the most natural way of measuring how close our approximate solution is to the true solution.
In fact, when we say that a sequence $x_0,x_1,x_2,\ldots$ of vectors converges to $x_*$, we mean that the sequence of scalars, $\|x^*-x_0\|,\|x^*-x_1\|,\|x^*-x_2\|,\ldots$ converges to zero.
Thus, finding $x$ which solves $Ax=b$ could be written as finding the value of $x$ which minimizes $\|x - x^*\| = \|x-A^{-1}b\|$.

Of course, since we are trying to compute $x^*$, it doesn't make sense for an algorithm to explicitly depend on $x^*$.
The *residual* of $\tilde{x}$ is defined as $b-A\tilde{x}$.
Again, $\|b-Ax^*\| = 0$, and since $x^*$ is the only point where this is true, finding $x$ to minimize $\|b-Ax\|$ gives the true solution.
The advantage is that we can easily compute the residual $b-A\tilde{x}$ once we have our numerical solution $\tilde{x}$, while there is not necessarily a good way to compute the error $x^*-\tilde{x}$.
This means that the residual gives us a way of inspecting convergence of a method.

## Krylov subspaces

From the previous section, we know that minimizing $\|b-Ax\|$ will give the solution $x^*$.
Unfortunately, this problem is "just as hard" as solving $Ax=b$.

We would like to find a related "easier" problem.
One way to do this is to restrict the choice of values which $x$ can take. 
For instance, if we enforce that $x$ must be come from a smaller set of values, then the problem of minimizing $\|b-Ax\|$ is simpler (since there are less possibilities for $x$).
As an extreme example, if we say that $x = cy$ for some fixed vector $y$, then this is a scalar minimization problem.
Of course, by restricting what values we choose for $x$ it is quite likely that we will not longer be able to exactly solve $Ax=b$.

One thing we could try to do is balance the difficulty of the problems we have to solve at each step with the accuracy of the solutions they give.
If we can obtain a very approximate solution by solving an easy problem, and then improve the solution by solving successively more difficult problems.
If we do it in the right way, it seems plausible that "increasing the difficulty" of the problem we are solving won't lead to extra work at each step, if we are be able to take advantage of having an approximate solution from a previous step.

We can formalize this idea a little bit.
Suppose we have a sequence of subspaces $V_0\subset V_1\subset V_2\subset \cdots$.
Then we can construct a sequence of iterates, $x_0\in V_0, x_1\in V_1,x_2\in V_2, \ldots$.
If, at each step, we ensure that $x_k$ minimizes $\|b-Ax\|$ over $V_k$, then the norm of the residuals will decrease (because $V_k \subset V_{k+1}$). 

Ideally this sequences of subspaces would:

1. be easy to construct 
1. be easy to optimize over (given the previous work done)
1. eventually contain the true solution

We now formally introduce Krylov subspaces, and hint at the fact that they can satisfy these properties.

The $k$-th Krylov subspace generated by a square matrix $A$ and a vector $v$ is defined to be,
$$
\mathcal{K}_k(A,v) = \operatorname{span}\{v,Av,\ldots,A^{k-1}v \}
$$

First, these subspaces are relatively easy to construct because by definition we can get a spanning set by repeatedly applying $A$ to $v$.
In fact, we can fairly easily construct an orthonormal basis for these spaces with the [Arnoldi/Lanczos](./arnoldi_lanczos.html) algorithms.

<!-- expand -->
Therefore, if we can find a quantity which can be optimized over each direction of an orthonormal basis independently, then optimizing over these expanding subspaces will be easy because we only need to optimize in a single new direction at each step.

We now show that $\mathcal{K}_k(A,b)$ will eventually contain our solution by the time $k=n$.
While this result comes about naturally from our derivation of CG, I think it is useful to relate polynomials with Krylov subspace methods early on, as the two are intimately related.

Suppose $A$ has [characteristic polynomial](https://en.wikipedia.org/wiki/Characteristic_polynomial#Characteristic_equation),
$$
p_A(t) = \det(tI-A) = c_0 + c_1t + \cdots + c_{n-1}t^{n-1} + t^n
$$
It turns out that $c_0 = (-1)^n\det(A)$ so that $c_0$ is nonzero if $A$ is invertible.

The [Cayley-Hamilton Theorem](https://en.wikipedia.org/wiki/Cayley%E2%80%93Hamilton_theorem) states that a matrix satisfies its own characteristic polynomial.
This means,
$$
0 = p_A(A) = c_0 I + c_1 A + \cdots c_{n+1} A^{n-1} + A^n
$$

Moving the identity term to the left and dividing by $-c_0$ (which won't be zero since $A$ is invertible) we can write,
$$
A^{-1} = -(c_1/c_0) I - (c_2/c_0) A - \cdots - (1/c_0) A^{n-1}
$$

This tells us that $A^{-1}$ can be written as a polynomial in $A$! (I think this is one of the coolest facts from linear algebra.) In particular,  
$$
x^* = A^{-1}b = -(c_1/c_0) b - (c_2/c_0) Ab - \cdots - (1/c_0) A^{n-1}b
$$

That is, the solution $x^*$ to the system $Ax = b$ is a linear combination of $b, Ab, A^2b, \ldots, A^{n-1}b$ (i.e. $x^*\in\mathcal{K}_n(A,b)$).
This observation is the motivation behind Krylov subspace methods.

In fact, one way of viewing many Krylov subspace methods is as building low degree polynomial approximations to $A^{-1}b$ using powers of $A$ times $b$ (in fact Krylov subspace methods can be used to approximate $f(A)b$ where $f$ is any [function](./current_research.html)).


<!--start_pdf_comment-->
Next: [Arnoldi and Lanczos methods](./arnoldi_lanczos.html)
<!--end_pdf_comment-->


