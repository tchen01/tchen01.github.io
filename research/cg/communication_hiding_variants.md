---
title: Communication Hiding Conjugate Gradient Algorithms
author: '[Tyler Chen](https://chen.pw)'
keywords: ['applied','math']
description: The Conjugate Conjugate algorithm is a widely used method for solving Ax=b when A is positive definite. Mathematically equivalent variants have been developed to reduce global communication.
footer: <p class="footer">More about the conjugate gradient method can be found <a href="./">here</a>.</p>
...

So far, all we have considered are error bounds in terms of the number of iterations. 
However, in practice, what we really care about is how long a computation takes.
A natural way to try and speed up an algorithm is through parallelization, and many variants of the conjugate gradient algorithm have been introduced to try to reduce the runtime per iteration.
However, while these variants are all equivalent in exact arithmetic, they perform operations in different orders meaning they are not equivalent in finite precision arithmetic.
Based on our discussion about conjugate gradient in [finite precision](./finite_precision_cg.html), it should be too big of a surprise that the variants all behave differently.

![Convergence of different variants in finite precision. Note that the computation would finish in at most 112 steps in exact arithmetic.](./imgs/convergence.svg)

The DOE supercomputer "Summit" is able to compute 122 petaflops per second. 
That's something like $10^{16}$ floating point operations every second!
Unfortunately, on high performance machines, conjugate gradient often perform orders of magnitude fewer floating point operations per second than the computer is theoretically capable of.

The reason for this is *communication*. 

Traditionally, analysis of algorithm runtime has been done in terms the number of operations computed, and the amount of storage used. 
However, an important factor in the real world performance is the time it takes to move data around. 
Even on a single core computer, the cost of moving a big matrix from the hard drive to memory can be significant compared to the cost of the floating point operations done.
Because of this, there is a lot of interest in reducing the communication costs of various algorithms, and conjugate gradient certainly has a lot of room for improvement.

Parallel computers work by having different processors work on different parts of a computation at the same time.
Naturally, many algorithms can be sped up this way, but the speedups are not necessarily proportional to the increase in computation power.
In many numerical algorithms, "global communication" is one of the main causes of latency.
Loosely speaking, global communication means that all processors working on a larger task must finish with their subtask and report on the result before the computation can proceed.
This means that even if we can distribute a computation to many processors, the time it takes to move the data required for those computations will eventually limit how effective adding more processors is. 
So, a 1000x increase in processing power won't necessarily cut the computation time to 1/1000th of the original time.

Ultimately, when it comes to iterative methods like CG, users usually only care about the *time to solution*; i.e. how long it will take to reach some specified accuracy.
This means that both the time per iteration and the number of iterations required to reach some accuracy should be considered.
Improving one of these quantities as the expense of the other may not actually result in a faster method.


## Communication bottlenecks in CG

Recall the standard Hestenes and Stifel CG implementation.
Much of the algorithm is scalar and vector updates which are relatively cheap (in terms of floating point operations and communication).
The most expensive computations each iteration are the matrix vector product, and the two inner products.

**Algorithm.** (Hestenes and Stiefel conjugate gradient)
\begin{align*}
&\textbf{procedure}\text{ HSCG}( A,b,x_0 ) 
\\[-.4em]&~~~~r_0 = b-Ax_0, \nu_0 = \langle r_0,r_0 \rangle, p_0 = r_0, s_0 = Ar_0, 
\\[-.4em]&~~~~a_0 = \nu_0 / \langle p_0,s_0 \rangle
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~x_k = x_{k-1} + a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~r_k = r_{k-1} - a_{k-1} s_{k-1} 
\\[-.4em]&~~~~~~~~\nu_{k} = \langle r_k,r_k \rangle, \textbf{ and } b_k = \nu_k / \nu_{k-1}
\\[-.4em]&~~~~~~~~p_k = r_k + b_k p_{k-1}
\\[-.4em]&~~~~~~~~s_k = A p_k
\\[-.4em]&~~~~~~~~\mu_k = \langle p_k,s_k \rangle, \textbf{ and } a_k = \nu_k / \mu_k
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}

A matrix vector product requires $\mathcal{O}(\text{nnz})$ (number of nonzero) floating point operations, while an inner product of dense vectors requires $\mathcal{O}(n)$ operations. 
For many applications of CG, the number of nonzero entries is something like $kn$, where $k$ relatively small. 
In these cases, the cost of floating point arithmetic for a matrix vector product and an inner product is roughly the same. 

While the number of floating point operations for a sparse matrix vector product and an inner product are often similar, the communication costs for the inner products can be much higher.
In a matrix vector product, each entry of the output can be computed independently of the other entires. Moreover, each entry will generally depend on only a few entries of the matrix and a few entries of the vector.
On the other hand, an inner product requires all of the entries of both vectors. 
This means that even if parts of the computation are sent to different processors, the outputs will have be be put together in a *global reduction* (also called *global synchronization* or *all-reduce*).
This communication ends up becomining the performance bottleneck each iteration on sufficintly high performance machines.

There are multiply ways to address the communication bottleneck in CG. The two main approaches are "hiding" communication, and "avoiding" communication.
Communication hiding algorithm such as as pipelined CG introduce auxiliary vectors so that the inner products can be computed at the same time, allowing all global communcation to happen at the same time.
On the other hand, communication avoiding algorithms such as $s$-step CG compute iterations in blocks of size $s$, reducing the synchronization costs by a factor around $s$.

This piece focuses on some common communicating hiding methods.
If you're interested in communication avoiding methods, or want more information about communication hiding methods, Erin Carson has very useful [slides](https://math.nyu.edu/~erinc/ppt/Carson_PP18.pdf).


## Overlapping inner products

Suppose that we would like to be able to reduce the number of points in the algorithm a global communication is required (i.e. be able to compute all inner products simultaneously).
In the standard presentation of the conjugate gradient algorithm, we need to wait for each of the previous computations before we are able to do a matrix vector product or an inner product.
This means there are two global communications per iteration and that none of the heavy computations can be overlapped.


Using our recurrences we can write,
$$
s_k = Ap_k = A(r_k + b_k p_{k-1}) 
= Ar_k + b_k s_{k-1}
$$

If we define the axillary vector $w_k = Ar_k$, in exact arithmetic using this formula for $s_k$ will be equivalent to the original formula for $s_k$. 
However, we can now compute $w_k$ as soon as we have $r_k$.
Therefore, the computation of $\nu_k = \langle r_k,r_k \rangle$ can be overlapped with the computation of $w_k = Ar_k$.
However, this still requires two global communication points each iteration.

We now note that,
\begin{align*}
\mu_k = \langle p_k,s_k \rangle
&= \langle r_k + b_k p_{k-1}, w_k + b_k s_{k-1} \rangle
\\&= \langle r_k, w_k \rangle + b_k \langle p_{k-1}, w_k \rangle + b_k \langle r_k, s_{k-1} \rangle + b_k^2 \langle p_{k-1}, s_{k-1} \rangle
\end{align*}

Moreover, since $w_k = Ar_k$ and $s_{k-1} = Ap_{k-1}$, then $\langle p_{k-1},w_k \rangle = \langle r_{k}, s_{k-1} \rangle$. 
Thus,
$$
\mu_k = \langle r_k,w_k\rangle + 2 b_k \langle r_k,s_k \rangle + b_k^2 \mu_{k-1}
$$

Notice now that $\langle r_k,w_k \rangle$, and $\langle r_k,s_k \rangle$ can both be overlapped with $\nu_k = \langle r_k,r_k\rangle$. 
Thus, using this coefficient formula there is only a single global synchronization per iteration.
However, this came at the cost of having to compute an additional inner product. 

It turns out that we can eliminate one of the inner products.
Indeed, using our recurrence for $r_k$,
$$
\langle r_k, s_{k-1} \rangle
= \langle p_k - b_k p_{k-1}, s_{k-1} \rangle
= -b_{k} \langle p_{k-1},s_{k-1} \rangle
= -b_k\mu_{k-1}
$$

Thus, defining $\eta_k = \langle w_k,r_k \rangle$ and canceling terms,
$$
\mu_k = \langle w_k,r_k \rangle - b_k^2 \mu_{k-1}
= \eta_k - (b_k/a_k) \nu_k
$$

This variant is known as Chronopoulos and Gear conjugate gradient.

**Algorithm.** (Chronopoulos and Gear conjugate gradient)
\begin{align*}
&\textbf{procedure}\text{ CGCG}( A,b,x_0 ) 
\\[-.4em]&~~~~r_0 = b-Ax_0, \nu_0 = \langle r_0,r_0 \rangle, p_0 = r_0, s_0 = Ar_0, 
\\[-.4em]&~~~~a_0 = \nu_0 / \langle p_0,s_0 \rangle
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~x_k = x_{k-1} + a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~r_k = r_{k-1} - a_{k-1} s_{k-1} 
\\[-.4em]&~~~~~~~~w_k = Ar_k 
\\[-.4em]&~~~~~~~~\nu_{k} = \langle r_k,r_k \rangle, \textbf{ and } b_k = \nu_k / \nu_{k-1}
\\[-.4em]&~~~~~~~~\eta_k = \langle r_k, w_k \rangle, \textbf{ and } a_k = \nu_k / (\eta_k - (b_k/a_{k-1})\nu_k)
\\[-.4em]&~~~~~~~~p_k = r_k + b_k p_{k-1}
\\[-.4em]&~~~~~~~~s_k = w_k + b_k s_{k-1}
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}


However, while we have only a single global communication per iteration, the matrix vector product must still be computed before we are able to compute the inner products. 
To allow the matrix vector product to be overlapped with the inner products, we again introduce auxiliary vectors.
Observe that,
\begin{align*}
w_k = Ar_k &= A(r_{k-1} - a_{k-1}s_{k-1}) 
\\&= A r_{k-1} - a_{k-1} As_{k-1}
\\&= w_{k-1} - a_{k-1} As_{k-1}
\end{align*}

Now, define $u_{k} = As_{k}$ and note that,
\begin{align*}
u_{k} = As_k &= A(w_k + b_k s_{k-1}) 
\\&= Aw_k + b_k As_{k-1} 
\\&= Aw_k + b_k u_{k-1}
\end{align*}

That's it. For convenience we define $t_k = Aw_k$. 
Then, the matrix vector product $Aw_k$ can occur as soon as we have computed $w_k$ and can be overlapped with both inner products.
This variant is known as either Ghysels and Vanroose conjugate gradient or pipelined conjugate gradient.

**Algorithm.** (Ghysels and Vanroose (pipelined) conjugate gradient)
\begin{align*}
&\textbf{procedure}\text{ GVCG}( A,b,x_0 ) 
\\[-.4em]&~~~~r_0 = b-Ax_0, \nu_0 = \langle r_0,r_0 \rangle, p_0 = r_0, s_0 = Ar_0, 
\\[-.4em]&~~~~w_0 = s_0, u_0 = Aw_0, a_0 = \nu_0 / \langle p_0,s_0 \rangle
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~x_k = x_{k-1} + a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~r_k = r_{k-1} - a_{k-1} s_{k-1} 
\\[-.4em]&~~~~~~~~w_k = w_{k-1} - a_{k-1} u_{k-1}
\\[-.4em]&~~~~~~~~\nu_k = \langle r_k,r_k\rangle, \textbf{ and } b_k = \nu_k/\nu_{k-1}
\\[-.4em]&~~~~~~~~\eta_{k} = \langle r_k,w_k \rangle, \textbf{ and } a_k = \nu_k / (\eta_k - (b_k/a_{k-1})\nu_k)
\\[-.4em]&~~~~~~~~t_k = Aw_k
\\[-.4em]&~~~~~~~~p_k = r_k + b_k p_{k-1}
\\[-.4em]&~~~~~~~~s_k = w_k + b_k s_{k-1}
\\[-.4em]&~~~~~~~~u_k = t_k + b_k u_{k-1}
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}

In a derivation similar those of the "classic" communication hiding varaints on this page, Erin Carson and myself have introduced ["predict-and-recompute"](../publications/predict_and_recompute.html) variants.
These variants have the same parallelism as the pipelined conjugate gradient shown here, but better numerical properties.

Recently, Cornelis, Cools, and Vanroose have developed a ["deep pipelined"](https://arxiv.org/pdf/1801.04728.pdf) conjugate gradient, which introduces even more auxiliary vectors to allow for more overlapping.

<!--start_pdf_comment-->
Next: [Current research on CG and related Krylov subspace methods](./current_research.html)
<!--end_pdf_comment-->



