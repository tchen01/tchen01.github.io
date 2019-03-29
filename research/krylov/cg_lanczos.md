% Conjugate Gradient is Lanczos in Disguise
% Tyler Chen

It's perhaps not so surprising that the Conjugate Gradient algorithm is related to the Lanczos algorithm. After all, they are both Krylov subspace methods for symmetric matrices.

The analysis of [finite precision CG](./finite_precision_cg.html) requires viewing CG in terms of the Lanczos recurrence.

## The relationship
We know that the Lanczos algorithm will produce an orthonormal basis for $\mathcal{K}_k(A,b)$ if we initialize with initial vector $r_0 = b$. 
Similarly, the Conjugate Gradient residuals form an orthogonal basis for for this space. 
This means that the Lanczos vectors must be scaled versions of the Conjugate Gradient residuals.

The Lanczos coefficients and vectors can be obtained from the Conjugate Gradient algorithm by the following relationship,
$$$
q_{k+1} \equiv (-1)^k\dfrac{r_k}{\norm{r_k}}
,~~~~
\beta_k \equiv \dfrac{\sqrt{b_{k}}}{a_{k-1}}
, ~~~~
\alpha_k \equiv \left(\dfrac{1}{a_{k-1}} + \dfrac{b_{k}}{a_{k-2}}\right)
$$

## Derivation
The derivation of the above result is not difficult, although it is a bit tedious.
Below is one way to obtain this relationship.
I would highly recommend trying it out on your own first, since it's a good chance to improve your familiarity with both algorithms.
While I hope that my derivation is not too hard to follow, there are definitely other ways to derive the same result, and often to really start to understand something you have to work it out on your own.


Recall that at each step of Lanczos iteration we update:
$$
q_{k+1} = \frac{Aq_k - \beta_{j-1}q_{k-1} - \alpha_{j}q_k }{\beta_k}
$$

Likewise, in each step of Conjugate Gradient we update:
$$
r_{k} = r_{k-1} - a_{k-1} Ap_{k-1}
,~~~~
p_k = r_k + b_{k-1}p_{k-1}
$$

$$
a_{k-1} = \frac{\langle r_{k-1},r_{k-1}\rangle}{\langle p_{k-1},Ap_{k-1}\rangle}
,~~~~
\dfrac{\langle r_k,r_k \rangle}{\langle r_{k-1},r_{k-1}\rangle}
$$


