% Communication Avoiding Conjugate Gradient Algorithms
% Tyler Chen

One of the main drawbacks to Conjugate gradient in a high performance setting is .....



## Communication bottlenecks in CG

Recall the standard Hestenes and Stifel CG implementation. In the below description, every block of code after a "**set**" must wait for the output from the previous block. Much of the algorithm is scalar and vector updates which are relatively cheap (in terms of floating point operations and communication). The most expensive computations each iteration are the matrix vector product, and the two inner products.

**Algorithm.** (Hestenes and Stiefel Conjugate Gradient)
\begin{align*}
&\textbf{procedure}\text{ HSCG}( A,b,x_0 ) 
\\[-.4em]&~~~~\textbf{set } r_0 = b-Ax_0, \nu_0 = \langle r_0,r_0 \rangle, p_0 = r_0, s_0 = Ar_0, 
\\[-.4em]&~~~~\phantom{\textbf{set }}a_0 = \nu_0 / \langle p_0,s_0 \rangle
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~\textbf{set } x_k = x_{k-1} + a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} r_k = r_{k-1} - a_{k-1} s_{k-1} 
\\[-.4em]&~~~~~~~~\textbf{set } \nu_{k} = \langle r_k,r_k \rangle, \textbf{ and } b_k = \nu_k / \nu_{k-1}
\\[-.4em]&~~~~~~~~\textbf{set }p_k = r_k + b_k p_{k-1}
\\[-.4em]&~~~~~~~~\textbf{set }s_k = A p_k
\\[-.4em]&~~~~~~~~\textbf{set }\mu_k = \langle p_k,s_k \rangle, \textbf{ and } a_k = \nu_k / \mu_k
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}

A matrix vector product requires $\mathcal{O}(\text{nnz})$ (number of nonzero) floating point operations, while an inner product requires $\mathcal{O}(n)$ operations. For many applications of CG, the number of nonzero entries is something like $kn$, where $k$ relatively small. In these cases, the cost of floating point arithmetic for a matrix vector product and an inner product is roughly the same. On the other hand, the communication costs for the inner products are much lower.

matvec is usually sparse

inner products require "all reduce"
i.e. collect information back from all the different processors/nodes
would like to be able to overlap these as much as possible


## Overlapping inner products

We would like to be able to *overlap* as many of the heavy computations as possible. However, in the current form, we need to wait for each of the previous computations before we are able to do a matrix vector product or an inner product.

Using our recurrences we can write,
$$
s_k = Ap_k = A(r_k + b_k p_{k-1}) 
= Ar_k + b_k s_{k-1}
$$

If we define the axillary vector $w_k = Ar_k$, in exact arithmetic using this formula for $s_k$ will be equivalent to the original formula for $s_k$. However, we can now compute $w_k$ as soon as we have $r_k$. Therefore, the computation of $\nu_k = \langle r_k,r_k \rangle$ can be overlapped with the computation of $w_k = Ar_k$.

These coefficient formulas seem to work better that CGCG..

**Algorithm.** (Chronopoulos and Gear Conjugate Gradient)
\begin{align*}
&\textbf{procedure}\text{ CGCG}( A,b,x_0 ) 
\\[-.4em]&~~~~\textbf{set } r_0 = b-Ax_0, \nu_0 = \langle r_0,r_0 \rangle, p_0 = r_0, s_0 = Ar_0, 
\\[-.4em]&~~~~\phantom{\textbf{set }}a_0 = \nu_0 / \langle p_0,s_0 \rangle
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~\textbf{set } x_k = x_{k-1} + a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} r_k = r_{k-1} - a_{k-1} s_{k-1} 
\\[-.4em]&~~~~~~~~\textbf{set } w_k = Ar_k 
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} \nu_{k} = \langle r_k,r_k \rangle, \textbf{ and } b_k = \nu_k / \nu_{k-1}
\\[-.4em]&~~~~~~~~\textbf{set }\eta_k = \langle r_k, w_k \rangle, \textbf{ and } a_k = \nu_k / (\eta_k - (b_k/a_{k-1})\nu_k)
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} p_k = r_k + b_k p_{k-1}
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} s_k = w_k + b_k s_{k-1}
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}

**Algorithm.** (Ghysels and Vanroose Conjugate Gradient)
\begin{align*}
&\textbf{procedure}\text{ CGCG}( A,b,x_0 ) 
\\[-.4em]&~~~~\textbf{set } r_0 = b-Ax_0, \nu_0 = \langle r_0,r_0 \rangle, p_0 = r_0, s_0 = Ar_0, 
\\[-.4em]&~~~~\phantom{\textbf{set }}w_0 = s_0, u_0 = Aw_0, a_0 = \nu_0 / \langle p_0,s_0 \rangle
\\[-.4em]&~~~~\textbf{for } k=1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~\textbf{set } x_k = x_{k-1} + a_{k-1} p_{k-1} 
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} r_k = r_{k-1} - a_{k-1} s_{k-1} 
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} w_k = w_{k-1} - a_{k-1} u_{k-1}
\\[-.4em]&~~~~~~~~\textbf{set } \nu_k = \langle r_k,r_k\rangle, \textbf{ and } b_k = \nu_k/\nu_{k-1}
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} \eta_{k} = \langle r_k,w_k \rangle, \textbf{ and } a_k = \nu_k / (\eta_k - (b_k/a_{k-1})\nu_k)
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} t_k = Aw_k
\\[-.4em]&~~~~~~~~\textbf{set } p_k = r_k + b_k p_{k-1}
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} s_k = w_k + b_k s_{k-1}
\\[-.4em]&~~~~~~~~\phantom{\textbf{set }} u_k = b_k u_{k-1}
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}



fda

## fdas



