#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def cg(A,f,max_iter):
    """
    CG algorithm to find solution to Ax = f
    
    Input
    -----
    A : (n,n) array like SPD matrix
    f : (n,) right hand side
    max_iter : int of maximum iterations to take
    
    Returns
    -------
    x : approximate solution to Ax=f
    """
    
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