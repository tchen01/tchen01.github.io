---
title: 'Distributed computing with Python: mpi4py'
author: '[Tyler Chen](https://chen.pw)'
keywords: ['applied','math']
description: A breif introduction to distributed computing with mpi4py.
footer: <p class="footer">More about computing can be found <a href="./">here</a>.</p>
---

There are many introductions to MPI out there.
However, the amount of information about mpi4py is much more limited, and most examples and tutorials assume a background with MPI.
Unfortunately, I'm not an expert with either, so this isn't going to be a detailed and comprehensive tutorial.
Instead, I hope that it demonstrates that distributed computing with high level languages is possible and relatively straightforward, even to those without much background with MPI.


## Introduction 

I have written some about some [parallel verions of the conjugate gradient method](../cg/communication_hiding_variants.html).
In short, many of these variants aim to overlap expensive parts of a computation.
I'm personally most interested in the numerical properties of these algorithms; i.e. how they behave in finite precision.
This doesn't relate that much to implementing anything in parallel, but when introducing new variants, such as the [pipelined predict-and-recompute CG method](../publications/predict_and_recompute.html), it's nice to be able to have some experiments which show that the actually are faster in practice.

**Algorithm.** (pipeline predict-and-recompute conjugate gradient)
\begin{align*}
&\textbf{procedure }\text{PIPE-PR-CG}( A,b,x_0 )
\\[-.4em]&~~~~r_0 = b - Ax_0
,~~p_0 = r_0
\\[-.4em]&~~~~~~~w_0 = Ar_0
,~~s_0 = Ap_0
\\[-.4em]&~~~~\textbf{for } k=0,1,2,\ldots \textbf{:} 
\\[-.4em]&~~~~~~~~\mu_k = \langle p_k, s_k \rangle
, ~~ \delta_k = \langle s_k,s_k \rangle,
\\[-.4em]&~~~~~~~~~~~\gamma_k = \langle r_k,r_k \rangle
, ~~ \nu_k' = \langle r_k,s_k \rangle
\\[-.4em]&~~~~~~~~u_k = A s_k
\\[-.4em]&~~~~~~~~w_k' = A r_k
\\[-.4em]&~~~~~~~~--------
\\[-.4em]&~~~~~~~~\alpha_k = \nu_k' / \mu_k 
\\[-.4em]&~~~~~~~~x_{k+1} = x_{k} + \alpha_{k} p_{k} 
\\[-.4em]&~~~~~~~~r_{k+1} = r_{k} - \alpha_{k} s_{k} 
\\[-.4em]&~~~~~~~~w_{k+1} = w_{k}' - \alpha_{k} u_{k}
\\[-.4em]&~~~~~~~~\nu_{k+1} = \nu_k' - 2 \alpha_k \delta_k + \alpha_k^2 \gamma_k 
\\[-.4em]&~~~~~~~~\beta_{k+1} = \nu_{k+1} / \nu_k' 
\\[-.4em]&~~~~~~~~p_{k+1} = r_k + \beta_{k+1} p_{k}
\\[-.4em]&~~~~~~~~s_{k+1} = w_k + \beta_{k+1} s_{k}
\\[-.4em]&~~~~~\textbf{end for}
\\[-.4em]&\textbf{end procedure}
\end{align*}

Notice that all the inner products and matrix vector products can occur simultaneously, and that any global communication only needs to happen at a single step each iteration.

The example I work through below is a slightly modified version of some scaling tests which you can view on [Github](https://github.com/tchen01/new_cg_variants/tree/master/predict_and_recompute).


## Global reductions

Before we get into implementing PIPE-PR-CG, let's discuss how we would compute an inner product $\langle x,y\rangle = \sum_{i=1}^{n} x_i y_i$ in parallel.

Suppose we have 4 machines to use. 
Partition $x$ and $y$ as,
\begin{align*}
x = \begin{bmatrix}
x^{(0)} \\ 
x^{(1)} \\ 
x^{(2)} \\ 
x^{(3)} 
\end{bmatrix}
,&&
y = \begin{bmatrix}
y^{(0)} \\ 
y^{(1)} \\ 
y^{(2)} \\ 
y^{(3)} 
\end{bmatrix}
\end{align*}

Then,
\begin{align*}
\langle x,y \rangle 
= \langle x^{(0)}, y^{(0)} \rangle
+ \langle x^{(1)}, y^{(1)} \rangle
+ \langle x^{(2)}, y^{(2)} \rangle
+ \langle x^{(3)}, y^{(3)} \rangle
\end{align*}

Thus, if we place $x^{(i)}$ and $y^{(i)}$ on machine $i$, we can compute each of the inner products $\langle x^{(i)}, y^{(i)} \rangle$ simultaneously.
In theory, this would give us a roughly 4 times speedup, and if we could use $p$ machines we could hope for a $p$ times speedup.

However, we need to communicate the value of each of the partial sums to a single computer so that they can be added.
This is called *global* communication since we need to move data between all of our machines.
On large supercomputers, where nodes (machines) may not be particularly close there are physical limitations to how fast this communication can happen.
Thus, if we keep adding more and more nodes, eventually it will take longer to communicate between them, and the benefit of being able to do our computation faster will be lost.

We can view a dense matrix vector product as a bunch of inner products between the rows of the matrix and the given vector. 
Since each of these inner products can occur simultaneously and all communication can occur at once, the cost of a matrix vector product is roughly equal to that of a single inner product, once the communication costs become much larger than the computation costs.

Alternatively, a spase matrix product may only require adjacent machines communicate with one another.
Similarly, operations such as $\alpha x+y$ do not require any communication can can be assumed to be very fast.

The standard HS-CG algorithm requires two inner products and one matrix vector product per iteration, each of which cannot start until the previous has finished.
Thus, each iteration requires three global reductions.
However, it is clear that while PIPE-PR-CG requires more floating point operations than the HS-CG, each iteration requires only one global reduction.
Thus, if communication is the dominant cost, we can expect PIPE-PR-CG to be about 3 times faster than HS-CG.

## Setting things up

We now get into the implementation.

Mpi4py and numpy play well together.
In particular, Since numpy arrays of floats are just C arrays, mpi4py is able to work nearly as fast as if we were using MPI code written in C.
We first import numpy and mpi4py.

    import numpy as np
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

Without going into too many details, `size` is the number of MPI processes, and `rank` is an integer between `0` and `size-1` which lets us know which process we are using.
For our purposes, we will think of processes as different computers and their ranks as an identification number.

Roughly speaking, we can then imagine that each computer independently runs our script, but sets `rank` as its own identification number.
This allows us to use the same script for all the computers, rather than writing a different scrip for each computer.
These are all MPI concepts, so you can probably find better explanations on the ~ i n t e r n e t ~.

## Defining our problem

In this example we will solve $Ax = b$ where $A$ is a $n\times n$ dense matrix and $b$ is chosen so that all the entries of $x$ are the same, and $x$ has norm one.
Since our goal is to test the scaling properties of the algorithm, it doesn't matter too much what our matrix is exactly. 
In order to understand how the extra matrix vector product which our alorithm uses affect timings, we will use a dense matrix.

For convenience, we will make $A$ a diagonal matrix.
something about small entries..

In our example we use the model problem which has eigenvalues,
\begin{align*}
\lambda_i = \lambda_1 + (\lambda_n - \lambda_1)^{(i+1)/(n-1)} \rho^{n-i}
,&& \lambda_1 = 1/\kappa
,&& \lambda_n = 1
\end{align*}
where we select parameters $\kappa = 10^6, \rho = 0.9$

If $x$ is a constant vector and $A$ is diagonal, then we must pick the entries of $b$ to be those of the diagonal of $A$ scaled by $1/\sqrt{n}$.

Something about `rank == 0`

    if rank == 0:
        kappa = 1e6
        rho = 0.9
        
        lambda1 = 1/kappa
        lambdan = 1
        Lambda = lambda1+(lambdan-lambda1)*np.arange(n)/(n-1)*rho**np.arange(n-1,-1,-1,dtype='float')
        sendbuf = Lambda.reshape(size,-1)
    else:
        Lambda = None
        sendbuf = None

We will then "distribute" our right hand side vector to each of our machines. 
In order to tell mpi4py to do this, we first build `sendbuf` which is a 2d array, where the first entry is the part of the $b$ we want to put on the first machine, the second is the part of $b$ we want to put on the second machine, and so on.
For convenience, we will assume that `n` is a multiple of `size` in which case we will send `n / size` many entries of the right hand side to each process.
We can easily construct `sendbuf` by reshaping `Lambda`.

Next, we set up `b`, which will hold the local part of the right hand side vector.
We want this to happen on each processor, so we do not add a condition that `rank == 0` as we did when we were defining the entries of the right hand side.
Finally, we use the mpi function scatter to send out each piece of sendbuf to each machine, where it will be placed in `b`.

    b = np.empty(n//size,dtype='float')
    comm.Scatter(sendbuf,b, root=0)

Note that in this example there is no reason we had to compute `Lambda` on the first machine instead of on each processor simultaneously.
However, in order to demonstrate how to use `comm.Scatter` we have done it this way.

We now set up $A$.
In our example, since $A$ is simply the matrix with $b$ as the diagonal entries, we can construct each piece of $A$ on each machine.
However, in many other cases we may also have to distribute $A$.
We also add very small components to all the off-diagonal entries to ensure that the computer doesn't somehow recognize all the off-diagonal entries are zero and use some shortcuts to avoid these computations.
Numerically these are small enough they shouldn't really hanve an effect.
Finally, we normalize `b` so that our solution has norm one.

    A = np.ones((n,n//size),dtype='float') 
    A *= 2e-32
    A[rank*(n//size):(rank+1)*(n//size)] += np.diag(b)

    b /= np.sqrt(n)

    m = len(b)


## Initialization and defining variables

At this point each processor holds a piece of $b$ (denoted `b`) and some columns of $A$ (denoted `A`).
We now set up all the variables we will need for the PIPE-PR-CG method.

Since we will eventually compute the products $Ar_k$ and $As_k$ at the same time, we opt to store $r_k$ and $s_k$ in a $n\times 2$ matrix denoted `rs`.
The first column will represent $r_k$ and the second $s_k$.
We can then use numpy's matrix multiplication, which means we will only have to access `A` once per iteration (something something column major storage instead).

    beta = np.zeros((1))
    alpha = np.zeros((1))
    nu_ = np.zeros((1))
    nu = np.zeros((1))

    x = np.zeros_like(b)
    rs = np.zeros((m,2))
    rs[:,0] = b
    p = np.copy(b)
    w = np.zeros_like(b)

While it would be fine to work with `rs` as we did above, it will be convenient to define *views* of `rs`.
A view of `rs` is a separate numpy array which point to some subset of the memory of `rs`.
In our case, we would like these to correspond to $r_k$ and $s_k$.

    r = np.ndarray.view(rs[:,0])
    s = np.ndarray.view(rs[:,1])

The advantage of using views is that we can now write `r` instead of `rs[:,0]`.
This will help keep our notation cleaner.

In a similar way, we place all of the variables which will be involved in our global communication into a single array called `data`.
This will make it easier for us to write our MPI reduction, and since we use views, doesn't really affect much when we're coding.

    data = np.ones((m*size+2,2))
    data_part = np.ones((m*size+2,2)) # w' u mu delta gamma nu'
    
    wp = np.ndarray.view(data[rank*m:(rank+1)*m,0])
    u = np.ndarray.view(data[rank*m:(rank+1)*m,1])
    mu = np.ndarray.view(data[-2:-1,0]) 
    delta = np.ndarray.view(data[-2:-1,1]) 
    gamma = np.ndarray.view(data[-1:,0]) 
    nup = np.ndarray.view(data[-1:,1]) 

    u_wp_part = np.ndarray.view(data_part[:m*size])
    mu_part = np.ndarray.view(data_part[-2:-1,0]) 
    delta_part = np.ndarray.view(data_part[-2:-1,1]) 
    gamma_part = np.ndarray.view(data_part[-1:,0]) 
    nup_part = np.ndarray.view(data_part[-1:,1]) 

Finally, we set $s_0$ to $Ap_0$.
I describe how `comm.Allreduce` works below, so you can just ignore this for now.

    data_part[:m*size,0] = np.dot(A,p)
    comm.Allreduce([data_part,MPI.DOUBLE],[data,MPI.DOUBLE],op=MPI.SUM)
    s[:] = data[rank*m:(rank+1)*m,0]

## Main loop

We now write the main loop.
Because we spent the time to set up our views, this is relatively straightforward.
The first thing we do is compute our partial inner products and matrix products.
(Note that we need to use `[:]` to avoid redefining these 1x1 arrays as scalars.)

    mu_part[:] = np.dot(p,s)
    delta_part[:] = np.dot(r,s)
    gamma_part[:] = np.dot(s,s)
    nup_part[:] = np.dot(r,r)
    np.dot(A,rs,out=u_wp_part)

These correspond to the partial sums we described in the section on global reductions.
Again, remember that any code we write gets run on all of our machines simultaneously.
Now that we have done all of the heavy work in parallel, we can proceed with a global reduction to exchange data between our machines.

We need to add up our partial sums and put the result on each machine.
To do this we use the MPI function "allreduce", which essentially combines the values on each machine by applying some operation (in our case the sum operation).

    comm.Allreduce([data_part,MPI.DOUBLE],[data,MPI.DOUBLE],op=MPI.SUM)

The syntax here tells MPI to take the values stored in `data_part` on each machine and sum them together, and then place them in a new array called `data`, also stored on each machine. 
If we wanted the end result to end up on only a single machine, then we could use "reduce" instead.
Since my goal isn't to explain MPI concepts, again I'll turn readers to other sources on the internet for more a comprehensive explanation.

Finally, we can write the rest of the loop.
Because we spent the time to define our views, this part of the code is quite simple to write.
Indeed, it looks almost identical to what a non-parallel numpy implementation would look like.
In my mind, this is a huge advantage of using a high level binding for MPI; we can spend our time focusing on the big picture idea rather than the implementation.

    nu_[:] = nup
    
    alpha = nu_ / mu
    
    x += alpha * p
    r -= alpha * s
    w = wp - alpha * u
    
    nu = nu_ - 2 * alpha * delta + alpha**2 * gamma
    beta = nu / nu_
    
    p *= beta
    p += r
    s *= beta
    s += w

## Afterthoughts

A reasonable question to ask is how much faster would our code be if we were to use C?
In my case, the answer is not faster at all because I'm terrible at writing C and there is a good change I would never get my code to compile.
Jokes aside, if our matrix is very large the answer is probably not much unless you are able to round up a team of experts.
The overhead we incur from numpy and mpi4py is mostly in the form of having to make function calls to low level libraries.
These costs are more or less independent of the problem size, and so for big enough problems they become negligible.

However, as the problem size scales, the [effects of numpy's optimization will start to become visible](https://stackoverflow.com/questions/10442365/why-is-matrix-multiplication-faster-with-numpy-than-with-ctypes-in-python).
For instance, if we were to implement the matrix multiplication ourself we would probably use the standard $\mathcal{O}(n^3)$ matrix multiply, rather that whatever fast method numpy is using (which can be optimized all the way down to the hardware level depending on your version of BLAS).

Even disregarding this, for many applications the potential improvements from using a low level language won't be worth the extra time that will inevitably be spent writing the code.
After all, there is a reason that people use numpy instead of C for scientific computing.
This is especially true when it comes to research code, where the value of being able to to quickly try out ideas cannot be understated.



