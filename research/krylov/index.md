% An Introduction to the Conjugate Gradient Algorithm
% Tyler Chen

<!--start_pdf_comment-->
This is the first piece from a series on the Conjugate Gradient algorithm.
I have split up the content into the following pages:

- [Introduction to Krylov subspaces](./)
- [Arnoldi and Lanczos methods](./arnoldi_lanczos.html)
- [Derivation of CG](./cg_derivation.html)
- [CG is Lanczos in disguise](./cg_lanczos.html)
- [Error bounds for CG](./cg_error.html)
- [Finite precision CG](./finite_precision_cg.html)
- [Current Research](./current_research.html)

All of the pages have been compiled into a single [pdf document](./krylov.pdf) to facilitate offline reading. 

The following are some supplementary pages which are not directly related to Conjugate Gradient, but somewhat related:

- [The Remez Algorithm](./remez.html)

My intention is not to provide a rigorous explanation of the topic, but rather, to provide some (hopefully useful) intuition about where this method comes from, how it works in theory and in practice, and what people are currently interested in learning about it.
I do assume some linear algebra background (roughly at the level of a first undergrad course in linear algebra), but I try to add some refreshers along the way.

If you are a bit rusty on your linear algebra I suggest taking a look at the [Khan Academy](https://www.khanacademy.org/math/linear-algebra) videos.
For a more rigorous and much broader treatment of iterative methods, I suggest Anne Greenbaum's [book](https://epubs.siam.org/doi/book/10.1137/1.9781611970937?mobileUi=0u) on the topic.
A popular introduction to Conjugate Gradient in exact arithmetic written by Jonathan Shewchuk can be found [here](./https://www.cs.cmu.edu/~quake-papers/painless-conjugate-gradient.pdf).
Finally, for a much more detailed overview of modern analysis of the Lanczos and Conjugate Gradient methods in exact arithmetic and finite precision, I suggest Gerard Meurant and Zdenek Strakos's [report](https://www.karlin.mff.cuni.cz/~strakos/download/2006_MeSt.pdf).

<!--end_pdf_comment-->

## Motivation
Solving a linear system of equations $Ax=b$ is one of the most important tasks in modern science.
<!--this is a bit strange sounding-->
A huge number of methods for dealing with more complex equations end up using linear approximations. 
As a result, applications such as weather forecasting, medical imaging, and training neural nets all require repeatedly solving linear systems to [IMPACT]. 
The Conjugate Gradient algorithm is widely used to solve linear systems when $A$ is symmetric and positive definite (if you don't remember what that means, don't worry, I have a refresher below).

- matrix free 
- CG less storage because of symmetric

<!-- Loosely speaking, methods for linear systems can be separated into two categories: direct methods and iterative methods.
Direct methods such as Gaussian elimination manipulate the entries of the matrix $A$ in order to compute the solution $x=A^{-1}b$.
On the other hand, iterative methods generate a sequence $x_0,x_1,x_2,\ldots$ of approximations to the true solution $x^* = A^{-1}b$, where hopefully each iterate is a better approximation to the true solution.

<-- why is direct better than GMRES? Less work?? -->
At first glance, it may seem that direct methods are better.
After all, after a known number of steps you get the exact solution.
this is true, especially when the matrix $A$ is dense and relatively small.
The main drawback to direct methods is that they are not able to easily take advantage of sparsity.
That means that even if $A$ has some nice structure and a lot of entries are zero, direct methods will take the same amount of time and storage to compute the solution as if $A$ were dense.
This is where iterative methods come in.
In iterative methods require only that the product $x\mapsto Ax$ be able to be computed.
If $A$ is sparse the product can be done cheaply, and if $A$ has some known structure, a you might not even need to construct $A$.
Such methods are aptly called "matrix free".
Similarly, many iterative methods such as Conjugate Gradient do not need much additional storage to compute the solution.
-->



## Measuring the accuracy of solutions
Perhaps the first question that should be asked about a numerical method for solving $Ax=b$ is, does the output approximate the true solution? 
If not, then there isn't much point using the method. 

Let's quickly introduce the idea of the *error* and the *residual* of an approximate solution $\tilde{x}$.
These quantities are both useful (in different ways) measures of how close the iterate $\tilde{x}$ is to the true solution $x^* = A^{-1}b$.

The *error* is simply the difference between $x$ and $\tilde{x}$.
Taking the norm of this quantity gives us a scalar value which measures the distance between $x$ and $\tilde{x}$.
In some sense, this is perhaps the most natural way of measuring how close our approximate solution is to the true solution.
In fact, when we say the sequence $x_0,x_1,x_2,\ldots$ converges to $x_*$, we mean that the scalar sequence,$\|x^*-x_0\|,\|x^*-x_1\|,\|x^*-x_2\|,\ldots$ converges to zero.
Thus, solving $Ax=b$ could be written as minimizing $\|x - x^*\| = \|x-A^{-1}b\|$ for some norm $\|\cdot\|$.

Of course, since we are trying to compute $x^*$, it doesn't make sense for an algorithm to explicitly depend on $x^*$.
The *residual* of $x\tilde{x}$ is defined as $b-A\tilde{x}$.
Again $b-Ax^* = 0$, and minimizing $\|b-Ax\|$ gives the true solution.
The advantage here is of course that we can easily compute the residual $b-A\tilde{x}$ once we have our numerical solution $\tilde{x}$.

## Krylov subspaces

From the previous section, we know that minimizing $\|b-Ax\|$ will give the solution $x^*$.
Unfortunately, this problem is "just as hard" as solving $Ax=b$.

We would like to relax this problem in some way to make it "easier".
One way to do this is to restrict the values that $x$ can be. For instance, we can enforce that $x$ comes from a smaller set of values which should make the problem of minimizing $\|b-Ax\|$ simpler (since there are less possibilities for $x$).
For instance, if we say that $x = cy$ for some fixed vector $y$, then this is a scalar minimization problem.
Of course, by restricting what values we choose for $x$ it is quite likely that we will not longer be able to exactly solve $Ax=b$.

It then makes sense to try to balance the difficulty of the problems we have to solve at each step with the accuracy of the solutions they give.
One way to do this is to start with an easy problem and get a coarse solution, and then gradually increase the difficulty of the problem while refining the solution.
If we do it in the right way, "increasing the difficulty" of the problem we are solving won't lead to extra work, because we can take advantage of having solve the easier problems at previous steps.

Suppose we have a sequence of subspaces $V_0\subset V_1\subset V_2\subset \cdots V_m$.
Then we can construct a sequence of iterates, $x_0\in V_0, x_1\in V_1,\ldots$.
If at each step we make sure that $x_k$ minimizes $\|b-Ax\|$ over $V_k$, then the norm of the residuals will decrease (because $V_k \subset V_{k+1}$). 

Ideally this sequences of subspaces would:

1.
be easy to construct 
1.
be easy to optimize over (given the previous work done)
1.
eventually contain the true solution

We now formally introduce Krylov subspaces, and show that they can satisfy these properties.

The $k$-th Krylov subspace generated by a square matrix $A$ and a vector $v$ is defined to be,
$$
\mathcal{K}_k(A,v) = \operatorname{span}\{v,Av,\ldots,A^{k-1}v \}
$$

First, these subspaces are relatively easy to construct because we can get them by repeatedly applying $A$ to $v$.
In fact, we can fairly easily construct an orthonormal basis for these spaces (discussed below).

Therefore, if we have a quantity which can be optimized over each direction of an orthonormal basis independently, then optimizing over these expanding subspaces will be easy because we only need to optimize in a single new direction at each step.

We now show that $\mathcal{K}_k(A,b)$ will eventually contain our solution by the time $k=n$.
While this result comes about naturally later from our description of some algorithms, I think it is useful to relate polynomials with Krylov subspace methods early on, as the two are intimately related.

Suppose $A$ has [characteristic polynomial](https://en.wikipedia.org/wiki/Characteristic_polynomial#Characteristic_equation),$$
p_A(t) = \det(tI-A) = c_0 + c_1t + \cdots + c_{n-1}t^{n-1} + t^n
$$
It turns out that $c_0 = (-1)^n\det(A)$ so that $c_0$ is nonzero if $A$ is invertible.

The [Cayley-Hamilton Theorem](https://en.wikipedia.org/wiki/Cayley%E2%80%93Hamilton_theorem) states that a matrix satisfies its own characteristic polynomial.
This means,
$$
0 = p_A(A) = c_0 I + c_1 A + \cdots c_{n+1} A^{n-1} + A^n
$$

Moving the identity term to the left and dividing by $-c_0$ we can write,
$$
A^{-1} = -(c_1/c_0) I - (c_2/c_0) A - \cdots - (1/c_0) A^{n-1}
$$

This says that $A^{-1}$ can be written as a polynomial in $A$! In particular,  
$$
x^* = A^{-1}b = -(c_1/c_0) b - (c_2/c_0) Ab - \cdots - (1/c_0) A^{n-1}b
$$

That means that the solution $x^*$ to the system $Ax = b$ is a linear combination of $b, Ab, A^2b, \ldots, A^{n-1}b$.
This observation is the motivation behind Krylov subspace methods.
Thus, Krylov subspace methods can be viewed as building low degree polynomial approximations to $A^{-1}b$ using powers of $A$ times $b$ (in fact Krylov subspace methods can be used to approximate $f(A)b$ where $f$ is any function).

Finally, we note that $x = A^{-1}b \in \mathcal{K}_n(A,b)$.



