#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def compute_barycentric_weights(xt,dtype=np.longdouble):
    """
    compute weights for barycentric interpolation points xt[i]
    
    Input
    -----
    xt : interpolations points
    
    Returns
    -------
    w : weights
    """
    
    n = len(xt)
    
    # dists[i,j] = xt[i] - xt[j]
    # note that adding the idenity does not affect the numerator, and that log(1) = 0 so the diagonal terms are dropped from the sum in the denominator
    dists = (xt[:,None] - xt) + np.eye(n,dtype=dtype)

    num = np.prod(np.sign(dists),axis=1)
    denom = np.exp(n*np.log(2) + np.sum(np.log(np.abs(dists)),axis=1))
    
    return num/denom


def barycentric(x,xt,yt,w):
    """
    compute polynomial at x given weights w and interpolation points xt passing through points pt[i]
        
    Input
    -----
    x : values to evaluate function at
    xt : interpolations points
    pt : value of function at interpolation points
    w : barycentric weights
    
    Returns
    -------
    p : value of function at x
    
    Notes
    -----
    the approximation will fail if you are at an interpolation point. 
    We replace very small numbers with a very small number since this lets us recover yt
        - I'm not 100% sure if this is stable or not
    Right now when you run the code on a vector vs single values it returns different things..
        
    """

#    x_xj = x - xt[:,None]
    # make sure x is a numpy array
    x_xj = np.reshape(x,-1)[:,None] - xt
    
    # replace zeros with something very small
    bad_idx = np.where(x_xj == 0)
    x_xj[bad_idx] = 1e-100

    
#    num = np.sum(np.diag(w*yt)@(1/x_xj),axis=0)
#    denom = np.sum(np.diag(w)@(1/x_xj),axis=0)
    num = np.sum((w*yt)*(1/x_xj),axis=1)
    denom = np.sum(w*(1/x_xj),axis=1)
    
    p = num/denom
    
    return p

def remez(L,k):
    """
    remez algorithm to find degree k polynomial on a set of points L
    
    Input
    -----
    L : set of points
    k : degree of polynomial
        
    Returns
    -------
    X : reference on which minimax polynomial equioscillates 
    """
    
    # take first set of points of L as initial guess
    X = L[:k+1]
    
    strides = np.zeros(k+2,dtype=int)
    strides[0] = 0
    strides[-1] = k+2
        
    for j in range(k):
        # take first k+1 points as initial reference
        Y = (-1)**np.arange(k+1)
        w = compute_barycentric_weights(X)
        px_j = barycentric(L,X,Y,w)
        
        # find signs of p^{(j)}
        S = np.sign(px_j) 

        # find where sign of function switches
        strides[1:-1] = 1 + np.where(S[1:] != S[:-1])[0] 
        
        # find local maximum over each section of constant sign
        idx = np.zeros(k+1,dtype=int) 
        for i in range(k+1):
            idx[i] = strides[i] + np.argmax(np.abs(px_j[strides[i]:strides[i+1]]))
        
        # check if reference didn't change
        if np.all(X == L[idx]):
            break
        X = L[idx]

    return X
    