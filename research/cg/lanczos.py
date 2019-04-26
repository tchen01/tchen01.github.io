#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def lanczos(A,q0,max_iter):
    """
    Lanczos algorithm to find tridiagonal matrix T similar to A, when A is symmetric
    
    Input
    -----
    A : (n,n) array like SPD matrix
    q0 : (n,) array like starting vector
    max_iter : int of maximum iterations to take
    
    Returns
    -------
    alpha : main diagonal of T
    beta : off diagonal of T
    """
    
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