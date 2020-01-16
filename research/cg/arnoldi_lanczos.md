---
title: The Arnoldi and Lanczos algorithms
author: '[Tyler Chen](https://chen.pw)'
keywords: ['applied','math']
description: The Arnoldi and Lanczos algorithms for computing an orthonormal basis for Krylov subspaces are at the core of most Krylov subspace methods.
footer: <p class="footer">More about the conjugate gradient method can be found <a href="./">here</a>.</p>
...

The Arnoldi and Lanczos algorithms for computing an orthonormal basis for Krylov subspaces are, in one way or another, at the core of all Krylov subspace methods.
Essentially, these algorithms are the Gram-Schmidt procedure applied to the vectors $\{v,Av,A^2v,A^3v,\ldots\}$ in clever ways.
The Arnoldi algorithm works for any matrix, and the Lanczos algorithm works for Hermitian matrices.

## The Arnoldi algorithm

Recall that given a set of vectors $\{v_1,v_2,\ldots, v_k\}$ the Gram-Schmidt procedure computes an orthonormal basis $\{q_1,q_2,\ldots,q_k\}$ so that for all $j\leq k$,
$$
\operatorname{span}\{v_1,\ldots,v_j\} = \operatorname{span}\{q_1,\ldots,q_j\}
$$

In short, at step $j$, $v_{j+1}$ is orthogonalized against each of $\{q_1,q_2,\ldots, q_j\}$.

If we tried to compute the set $\{v,Av,A^2v,\ldots\}$, it would become very close to linearly dependent (and with rounding errors essentially numerically linearly dependent).
This is because this basis is essentially the [power method](https://en.wikipedia.org/wiki/Power_iteration).
The trick behind the Arnoldi algorithm is the fact that you do not need to construct the whole set $\{v,Av,A^2v,\ldots\}$ ahead of time.
This allows us to come up with a basis for $\{v,Av,A^2v,\ldots\}$ in a more "stable" way.

Suppose at the beginning of step $k$ that we have already computed an orthonormal basis $\{q_1,q_2,\ldots,q_{k-1}\}$ which has the same span as $\{v,Av,\ldots, A^{k-2}v\}$. 
If we were doing Gram-Schmidt, then we would obtain $q_k$ by orthogonalizing $A^{k-1}v$ against each of the vectors in the basis $\{q_1,q_2, \ldots, q_{k-1}\}$.
In the Arnoldi algorithm we instead orthogonalize $Aq_{k-1}$ against $\{q_1,q_2,\ldots, q_{k-1}\}$.

Let's understand why these are the same.
First, since the span of $\{q_1,q_2,\ldots, q_{k-1}\}$ is equal to the span of $\{v,Av,\ldots, A^{k-2}v\}$, then $q_{k-1}$ can be written as a linear combination of $\{v,Av,\ldots, A^{k-2}v\}$. 
That is, there exists coefficients $c_i$ such that,
$$
q_{k-1} = c_1v + c_2Av + \cdots + c_{k-1} A^{k-2}v
$$

Therefore, multiplying by $A$ we have,
$$
Aq_{k-1} = c_1Av + c_2A^2v + \cdots c_{k-1}A^{k-1}v
$$

Now, since each of $\{Av,A^2v,\ldots, A^{k-2}v\}$ are in the span of $\{q_1,q_2,\ldots, q_{k-1}\}$, each of these components will disappear when we orthogonalize $Aq_{k-1}$ against $\{q_1,q_2,\ldots,q_{k-1}\}$. 
This gives a vector in the same direction as the vector we get by orthogonalizing $A^{k-1}v$ against $\{q_1,q_2,\ldots,q_{k-1}\}$.
Since we get $q_k$ by normalizing the resulting vector, using $Aq_{k-1}$ will give us the same value for $q_k$ as using $A^{k-1}v$.

The Arnoldi algorithm gives the relationship,
$$
AQ_k = Q_k H_k + h_{k+1,k} q_{k+1} \xi_k^{\mathsf{T}}
$$
where $Q_k = [q_1,q_2,\ldots,q_k]$ is the $n\times k$ matrix whose columns are $\{q_1,q_2,\ldots,q_k\}$, $H_k$ is a $k\times k$ [*Upper Hessenburg*](https://en.wikipedia.org/wiki/Hessenberg_matrix) matrix, and $\xi_k^{\mathsf{T}} = [0,\ldots,0,1]^{\mathsf{T}}$ is the $k$-th unit vector.



### Ritz vectors

For instance, suppose that $H_nv = \lambda v$. Then,
$$
A(Q_nv) = (Q_nH_nQ_n^{\mathsf{H}})(Q_nv) = Q_nH_nv = Q_n(\lambda v) = \lambda (Q_nv)
$$

This proves that if $v$ is an eigenvector of $H_n$ with eigenvalue $\lambda$, then $Q_nv$ is an eigenvector of $A$ with eigenvalue $\lambda$.


We have just seen that if $Q_n$ is unitary, then if $v$ is an eigenvector of $H_n$ then $Q_nv$ is an eigenvalue of $A$ when $v$. 

When $k<n$ then $Q_k$ although $Q_k$ has orthonormal columns, it is not square. Even so, we can use $Q_kv$ as an "approximate" eigenvector of $Q$.

More specifically, if $v$ is an eigenvector of $H_k$ with eigenvalue $\lambda$, then $Q_kv$ is called a *Ritz vector*, and $\lambda$ is called a *Ritz value*. 


## The Lancozs algorithm
When $A$ is Hermitian, then $Q_k^{\mathsf{H}}AQ_k = H_k$ is also Hermetian.
This means that $H_k$ is upper Hessenburg and Hermitian, so it must be tridiagonal! 
Thus, the $q_j$ satisfy a three term recurrence,
$$
Aq_j = \beta_{j-1} q_{j-1} + \alpha_j q_j + \beta_j q_{j+1}
$$
which we can write in matrix form as,
$$
AQ_k = Q_k T_k + \beta_k q_{k+1} \xi_k^{\mathsf{T}}
$$


The Lanczos algorithm is an efficient way of computing this decomposition which takes advantage of the three term recurrence.

I will present a brief derivation for the method motivated by the three term recurrence above.
Since we know that the $q_j$ satisfy the three term recurrence, we would like the method to store as few of the $q_j$ as possible (i.e. take advantage of the three term recurrence as opposed to the Arnoldi algorithm).

Suppose that we have $q_j$, $q_{j-1}$, and the coefficient $\beta_{j-1}$, and want expand the Krylov subspace to find $q_{j+1}$ in a way that takes advantage of the three term recurrence.
To do this we can expand the subspace by computing $Aq_j$ and then orthogonalizing $Aq_j$ against $q_j$ and $q_{j-1}$.
By the three term recurrence, $Aq_j$ will be orthogonal to $q_i$ for all $i\leq j-2$ so we do not need to explicitly orthogonalize against those vectors.

We orthogonalize, 
\begin{align*}
\tilde{q}_{j+1} = Aq_j - \alpha_j q_j - \langle Aq_j, q_{j-1} \rangle q_{j-1}
, && 
\alpha_{j} = \langle A q_j, q_j \rangle
\end{align*}
and finally normalize,
\begin{align*}
q_{j+1} = \tilde{q}_{j+1} / \beta_j
,&&
\beta_j = \|\tilde{q}_{j+1}\|
\end{align*}

Note that this is not the most "numerically stable" form of the algorithm, and care must be taken when implementing the Lanczos method in practice.
We can improve stability slightly by using $Aq_j - \beta_{j-1} q_{j-1}$ instead of $Aq_j$ when finding a vector in the next Krylov subspace.
This allows us to explicitly orthogonalize $q_{j+1}$ against both $q_j$ and $q_{j-1}$ rather than just $q_j$.
It also ensures that the tridiagonal matrix produces is symmetric in finite precision (since $\langle Aq_j,q_{j-1}\rangle$ may not be equal to $\beta_j$ in finite precision).

**Algorithm.** (Lanczos)
\begin{align*}
&\textbf{procedure}\text{ lanczos}( A,v ) 
\\[-.4em]&~~~~\textbf{set } q_1 = v / \|v\|, \beta_0 = 0
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~\textbf{set } \tilde{q}_{k+1} = Aq_k - \beta_{k-1} q_{k-1}
\\[-.4em]&~~~~~~~~\textbf{set } \alpha_k = \langle \tilde{q}_{k+1}, q_k \rangle
\\[-.4em]&~~~~~~~~\textbf{set } \tilde{q}_{k+1} = \tilde{q}_{k+1} - \alpha_k q_{k}
\\[-.4em]&~~~~~~~~\textbf{set } \beta_k = \| \tilde{q}_{k+1} \|
\\[-.4em]&~~~~~~~~\textbf{set } q_{k+1} = \tilde{q}_{k+1} / \beta_k
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}

<!--
We can [implement](./lanczos.py) Lanczos iteration in numpy.
Here we assume that we only want to output the diagonals of the tridiagonal matrix $T$, and don't need any of the vectors (this would be useful if we wanted to compute the eigenvalues of $A$, but not the eigenvectors).

    def lanczos(A,q0,max_iter):
        alpha = np.zeros(max_iter)
        beta = np.zeros(max_iter)
        q_ = np.zeros(len(q0))
        q = q0/np.sqrt(q0@q0)

        for k in range(max_iter):
            qq = A@q-(beta[k-1]*q_ if k>0 else 0)
            alpha[k] = qq@q
            qq -= alpha[k]*q
            beta[k] = np.sqrt(qq@qq)
            q_ = np.copy(q)
            q = qq/beta[k]

    return alpha,beta
-->

<!--start_pdf_comment-->
Next: [A derivation of the conjugate gradient algorithm](./cg_derivation.html)
<!--end_pdf_comment-->


