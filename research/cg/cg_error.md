---
title: Error Bounds for the Conjugate Gradient Algorithm
author: '[Tyler Chen](https://chen.pw)'
keywords: ['applied','math']
description: The Conjugate Conjugate algorithm is a widely used method for solving Ax=b when A is positive definite. Characterizing the convergence of CG is important for understanding the rescources the algorithm will require.
footer: <p class="footer">More about the conjugate gradient method can be found <a href="./">here</a>.</p>
...

In our [derivation](./cg_derivation.html) of the conjugate gradient method, we minimized the $A$-norm of the error over sucessive Krylov subspaces.
Ideally we would like to know how quickly this method converge.
That is, how many iterations are needed to reach a specified level of accuracy.


## Error bounds from minimax polynomials

Previously we have show that,
$$
e_k \in e_0 + \operatorname{span}\{p_0,p_1,\ldots,p_{k-1}\} = e_0 + \mathcal{K}_k(A,b)
$$

Observing that $r_0 = Ae_0$ we find that,
$$
e_k \in e_0 +  \operatorname{span}\{Ae_0,A^2e_0,\ldots,A^{k}e_0\}
$$ 

Thus, we can write,
\begin{align*}
\| e_k \|_A =  \min_{p\in\mathcal{P}_k}\|p(A)e_0\|_A
,&&
\mathcal{P}_k = \{p : p(0) = 1, \operatorname{deg} p \leq k\}    
\end{align*}

Since $A^{1/2} p(A) = p(A)A^{1/2}$ we can write,
$$
\| p(A)e_0 \|_A
= \|A^{1/2} p(A)e_0 \|
= \|p(A) A^{1/2}e_0 \|
$$

Now, using the submultiplicative property of the 2-norm,
$$
\|p(A) A^{1/2}e_0 \|
\leq \|p(A)\| \|A^{1/2} e_0 \|
= \|p(A)\| \|e_0\|_A
$$

Since $A$ is positive definite, it is diagonalizable as $U\Lambda U^{\mathsf{H}}$ where $U$ is unitary and $\Lambda$ is the diagonal matrix of eigenvalues of $A$.
Thus, since $U^{\mathsf{H}}U = I$,
$$
A^k = (U\Lambda U^{\mathsf{H}})^k = U\Lambda^kU^{\mathsf{H}}
$$

We can then write $p(A) = Up(\Lambda)U^*$ where $p(\Lambda)$ has diagonal entries $p(\lambda_i)$.
Therefore, using the *unitary invariance* property of the 2-norm,
$$
\|p(A)\| = \|Up(\Lambda)U^{\mathsf{H}}\| = \|p(\Lambda)\|
$$

Now, since the 2-norm of a symmetric matrix is the magnitude of the largest eigenvalue,
$$
\| p(\Lambda) \| = \max_i |p(\lambda_i)|
$$

Finally, putting everything together we have,
$$
\frac{\|e_k\|_A}{\|e_0\|_A} \leq \min_{p\in\mathcal{P}_k} \max_i |p(\lambda_i)|
$$

Since the inequality we obtained from the submultiplicativity of the 2-norm is tight, this bound is also tight (in the sense that for a fixed $k$ there exists an initial error $e_0$ so that equality holds).

Polynomials of this form are called minimax polynomials. 
More formally, let $L\subset \mathbb{R}$ be some closed set.
The *minimax polynomial of degree $k$* on $L$ is the polynomial satisfying,
\begin{align*}
\min_{p\in\mathcal{P}_k} \max_{x\in L} | p(x) |
,&&
\mathcal{P}_k = \{p : p(0)=1, \deg p \leq k\}    
\end{align*}

Computing a minimax polynomial for a given set is not trivial, but an algorithm called the [Remez algorithm](./remez.html) can be used to compute it.

### Chebyshev bounds
The minimax polynomial on the eigenvalues of $A$ is a bit tricky to work with.
Although we can find it using the Remez algorithm, this is somewhat tedious, and requires knowledge of the whole spectrum of $A$.
To be useful in practice we would like a bound which depends only on information about $A$ that we might reasonably expect to have prior to solving the linear system.
One way to obtain such a bound is to expand the set on which we are looking for the minimax polynomial. 

To this end, let $\mathcal{I} =  [\lambda_{\text{min}},\lambda_{\text{max}}]$.
Then, since $\lambda_i\in\mathcal{I}$,
$$
\min_{p\in\mathcal{P}_k} \max_i |p(\lambda_i)| 
\leq \min_{p\in\mathcal{P}_k} \max_{x \in \mathcal{I}} |p(x)| 
$$

The right hand side requires that we know the largest and smallest eigenvalues of $A$, but doesn't require knowledge of any of the ones between.
This means it can be useful in practice, since we can easily compute the top and bottom eignevalues with the power method.

The minimax polynomials on a single closed interval $\mathcal{I}$ are called the *Chebyshev Polynomials*, and can be easily written down with a simple recurrence relation.

If $\mathcal{I} = [-1,1]$ then the relation is,
\begin{align*}
T_{k+1}(x) = 2xT_k(x) - T_{k-1}(x)
,&&
T_0=1
,&&
T_1=x    
\end{align*}

For $\mathcal{I} \neq [-1,1]$, the above polynomials are simply stretched and shifted to the interval in question. 

Let $\kappa = \lambda_{\text{max}} / \lambda_{\text{min}}$ (this is called the condition number).
Then, from properties of these polynomials,
$$
\frac{\|e_k\|_A}{\|e_0\|_A} \leq 2 \left( \frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1} \right)^k
$$
This bound is often referred to as the Chebyshev error bound, condition number error bound, or $\sqrt{\kappa}$ error bound.

<!--start_pdf_comment-->
Next: [The conjugate gradient Algorithm in Finite Precision](./finite_precision_cg.html)
<!--end_pdf_comment-->


