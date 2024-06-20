#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 02:59:40 2024

@author: mohamed
"""


import numpy as np
import scipy.optimize as op
import scipy.special as sp
import matplotlib.pyplot as plt




def eqnTM(b, V, nc,ng):
    u = V * np.sqrt(1 - b)
    w = V * np.sqrt(b)
    lhs =  nc **2 * sp.jv( 1, u) /(u * sp.jv(0, u))
    rhs =  ng **2 * sp.kn( 1, w) / ( w * sp.kn(0, w))
    return lhs + rhs



def findbTM(V, m, nc, ng):
    if m <= 0:
        raise ValueError("m ne peut pas etre négative")
    if V <= 0:
        return ValueError("V ne peut pas etre négative")
    delta = 1e-6
    j0z = sp.jn_zeros(0, m)
    j1z = sp.jn_zeros(1, m)
    lo = max(0, 1 - (j1z[m - 1] / V)**2) + delta
    hi = 1 - (j0z[m - 1] / V)**2 - delta
    if hi < lo:
        return None
    try:
        b = op.brentq(eqnTM, lo, hi, args=(V, nc, ng))
    except ValueError:
        return None
    return b




