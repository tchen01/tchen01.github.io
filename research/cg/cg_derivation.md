---
title: A Derivation of the Conjugate Gradient Algorithm
author: '[Tyler Chen](https://chen.pw)'
keywords: ['applied','math']
description: The Conjugate Conjugate algorithm is a widely used method for solving Ax=b when A is positive definite. While it's simple to state the algorithm, understanding where it comes from is not always so clear.
footer: <p class="footer">More about the conjugate gradient method can be found <a href="./">here</a>.</p>
...

There are many ways to view/derive the conjugate gradient algorithm. 
I'll derive the algorithm by directly minimizing by minimizing the $A$-norm of the error over successive Krylov subspaces, $\mathcal{K}_k(A,b)$.
To me this is the most natural way of viewing the algorithm.
My hope is that the derivation here provides some motivation for where the algorithm comes from.
Of course, what I think is a good way to present the topic won't match up exactly with every reader's own preference, so I highly recommend looking through some other resources as well.
To me, this is of those topics where you have to go through the explanations a few times before you start to understand what is going on. 


## Minimizing the error
Now that we have that out of the way, let's begin our derivation.
As stated above, at each step we will minimize the $A$-norm of the error over successive Krylov subspaces generated by $A$ and $b$.
That is to say $x_k$ will be the point so that,
\begin{align*}
\|e_k\|_A
:=\| x_k - x^* \|_A 
= \min_{x\in\mathcal{K}_k(A,b)} \| x - x^* \|_A
,&&
x^* = A^{-1}b
\end{align*}

Since we are minimizing with respect to the $A$-norm, it will be useful to have an $A$-orthonormal basis for $\mathcal{K}_k(A,b)$.
That is, a basis which is orthonormal in the $A$-inner product.
For now, let's just suppose we have such a basis, $\{p_0,p_1,\ldots,p_{k-1}\}$, ahead of time.
Further on in the derivation we will explain a good way of coming up with this basis as we go.

Since $x_k\in\mathcal{K}_k(A,b)$ we can write $x_k$ as a linear combination of these basis vectors,
$$
x_k = a_0 p_0 + a_1 p_1 + \cdots + a_{k-1} p_{k-1}
$$

Note that we have $x_0 = 0$ and $e_k = x^* - x_k$.
Then,
$$
e_k = e_0 - a_0p_0 - a_1 p_1 - \cdots - a_{k-1} p_{k-1}
$$

By definition, the coefficients for $x_k$ were chosen to minimize the $A$-norm of the error, $\|e_k\|_A$, over $\mathcal{K}_k(A,b)$.
Therefore, $e_k$ must have zero component in each of the directions $\{ p_0,p_1,\ldots,p_{k-1} \}$, which is an $A$-orthonormal basis for $\mathcal{K}_k(A,b)$.
In particular, that means that $a_jp_j$ cancels exactly with $e_0$ in the direction of $p_j$, for all $j$. 

We now make the important observation that the coefficients depend only on $e_0$ and the $p_i$, but not on $k$. 
This means that the coefficients $a_0',a_1',\ldots,a_{k-2}'$ of $x_{k-1}$ were chosen in exactly the same way as the coefficients for $x_k$, so $a_0=a_0', a_1=a_1', \ldots, a_{k-2}=a_{k-2}'$.

We can then write,
$$
x_k = x_{k-1} + a_{k-1} p_{k-1}
$$
and
$$
e_k = e_{k-1} - a_{k-1} p_{k-1}
$$

Now that we have explicitly written $x_k$ in terms of an update to $x_{k-1}$ this is starting to look like an iterative method!

Let's compute an explicit representation of the coefficient $a_{k-1}$.
As previously noted, since we have chosen $x_k$ to minimize $\|e_k\|_A$ over $\mathcal{K}_k(A,b)$, the component of $e_k$ in each of the directions $p_0,p_1,\ldots,p_{k-1}$ must be zero.
That is, $\langle e_k , p_j \rangle = 0$ for all $i=0,1,\ldots, k-1$. Substituting our expression for $e_k$ we find,
$$
0 = \langle e_k , p_{k-1} \rangle_A
= \langle e_{k-1}, p_{k-1} \rangle - a_{k-1} \langle p_{k-1} , p_{k-1} \rangle_A
$$

Thus,
$$
a_{k-1} 
= \frac{\langle e_{k-1}, p_{k-1} \rangle_A}{\langle p_{k-1},p_{k-1} \rangle_A} 
$$

This expression might look like a bit of a roadbock, since if we knew the error $e_k = x^* - x_k$ then we would know how to obtain the solution from our guess! 
However, we have been working with the $A$-inner product so we can write,
$$
Ae_{k-1} = A(x^* - x_{k-1}) = b - Ax_{k-1} = r_{k-1}
$$
Therefore, $a_{k-1}$ can be written as,
$$
a_{k-1}
= \frac{\langle r_{k-1}, p_{k-1} \rangle}{\langle p_{k-1},A p_{k-1} \rangle} 
$$

## Finding the Search Directions
At this point we are almost done.
The last thing to do is understand how to construct the basis $\{p_0,p_1,\ldots,p_k\}$ as we go.
Since $A$ is symmetric we know there is a three term recurrence which gives an orthonormal basis. However, the basis $\{p_0,p_1,\ldots,p_k\}$ is $A$-orthogonal.
Even so, looking for a short recurrence sounds promising.

Since $r_k = b-Ax_k$ and $x_k\in\mathcal{K}_k(A,b)$, then $r_k \in \mathcal{K}_{k+1}(A,b)$.
Thus, we can obtain $p_k$ by $A$-orthogonalizing $r_k$ against $\{p_0,p_1,\ldots,p_{k-1}\}$. 

Recall that $e_k$ is $A$-orthogonal to $\mathcal{K}_k(A,b)$.
That is, for $j\leq k-1$,
$$
\langle e_k, A^j b \rangle_A = 0
$$

Therefore, noting that $Ae_k = r_k$, for $j\leq k-2$,
$$
\langle r_k, A^j b \rangle_A = 0
$$

That is, $r_k$ is $A$-orthogonal to $\mathcal{K}_{k-1}(A,b)$.
In particular, this means that, for $j\leq k-2$,
$$
\langle r_k, p_j \rangle_A = 0
$$

That means that to obtain $p_k$ we really only need to $A$-orthogonalize $r_k$ against $p_{k-1}$ instead of all the previous $p_i$! That is,
\begin{align*}
p_k = r_k + b_k p_{k-1}
,&&
b_k = - \frac{\langle r_k, p_{k-1} \rangle_A}{\langle p_{k-1}, p_{k-1} \rangle_A}
\end{align*}

The immediate consequence is that we do not need to save the entire basis $\{p_0,p_1,\ldots,p_{k-1}\}$, but instead can just keep $x_k$,$r_k$, and $p_{k-1}$.
This is perhaps somewhat unsurprising give then we have seen that when $A$ is symmetric we have a three term [Lanczos recurrence](./arnoldi_lanczos.html#the-lanczos-algorithm). 
In fact, it turns out that the relationship between CG and Lanczos is quite fundamental, and that [CG is essentially doing the Lanczos algorithm](./cg_lanczos.html).

## Putting it all together

We are now essentially done! In practice, people generally use the following equivalent (but more numerically stable) formulas for $a_{k-1}$ and $b_k$,
\begin{align*}
a_{k-1} = \frac{\langle r_{k-1},r_{k-1}\rangle}{\langle p_{k-1},Ap_{k-1}\rangle}
,&&
b_k = \frac{\langle r_k,r_k\rangle}{\langle r_{k-1},r_{k-1}\rangle}
\end{align*}

The first people to discover this algorithm Magnus Hestenes and Eduard Stiefel who independently developed it around 1952. As such, the standard implementation is attributed to them. 
Pseudocode is presented below.

**Algorithm.** (Hestenes and Stiefel conjugate gradient)
\begin{align*}
&\textbf{procedure}\text{ HSCG}( A,b,x_0 ) 
\\[-.4em]&~~~~r_0 = b-Ax_0, \nu_0 = \langle r_0,r_0 \rangle, p_0 = r_0, s_0 = Ar_0, 
\\[-.4em]&~~~~a_0 = \nu_0 / \langle p_0,s_0 \rangle
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~x_k = x_{k-1} + a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~r_k = r_{k-1} - a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~\nu_{k} = \langle r_k,r_k \rangle, \textbf{ and } b_k = \nu_k / \nu_{k-1}
\\[-.4em]&~~~~~~~~p_k = r_k + b_k p_{k-1}
\\[-.4em]&~~~~~~~~s_k = A p_k
\\[-.4em]&~~~~~~~~\mu_k = \langle p_k,s_k \rangle, \textbf{ and } a_k = \nu_k / \mu_k
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}


<!--
\begin{align*}
&\textbf{procedure}\text{ HSCG}( A,b,x_0 ) 
\\[-.4em]&~~~~\textbf{set } r_0 = b-Ax_0, \nu_0 = \langle r_0,r_0 \rangle, p_0 = r_0, s_0 = Ar_0, 
\\[-.4em]&~~~~\phantom{\textbf{set }}a_0 = \nu_0 / \langle p_0,s_0 \rangle
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~\textbf{set } x_k = x_{k-1} + a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} r_k = r_{k-1} - a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~\textbf{set } \nu_{k} = \langle r_k,r_k \rangle, \textbf{ and } b_k = \nu_k / \nu_{k-1}
\\[-.4em]&~~~~~~~~\textbf{set }p_k = r_k + b_k p_{k-1}
\\[-.4em]&~~~~~~~~\textbf{set }s_k = A p_k
\\[-.4em]&~~~~~~~~\textbf{set }\mu_k = \langle p_k,s_k \rangle, \textbf{ and } a_k = \nu_k / \mu_k
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}
-->

<!--
This can be easily [implemented](./cg.py) in numpy.
Note that we use $f$ for the right hand side vector to avoid conflict with the coefficient $b$.

    def cg(A,f,max_iter):
        x = np.zeros(len(f)); r = np.copy(f); p = np.copy(r); s=A@p
        nu = r @ r; a = nu/(p@s); b = 0
        for k in range(1,max_iter):
            x += a*p
            r -= a*s

            nu_ = nu
            nu = r@r
            b = nu/nu_

            p = r + b*p
            s = A@p

            a = nu/(p@s)

        return x
-->

<!--start_pdf_comment-->
Next: [conjugate gradient is Lanczos in Disguise](./cg_lanczos.html)
<!--end_pdf_comment-->


