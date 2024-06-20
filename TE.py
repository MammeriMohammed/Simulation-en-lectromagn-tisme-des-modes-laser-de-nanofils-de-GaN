#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 02:36:18 2024

@author: mohamed
"""

import numpy as np
import scipy.optimize as op
import scipy.special as sp
import matplotlib.pyplot as plt

N = 100
V = np.linspace(0.1, 6, N+1)
mode_TE = {}

def eqnTE(b, V):
    u = V * np.sqrt(1 - b)
    w = V * np.sqrt(b)
    lhs = sp.jv(1, u) / (u * sp.jv(0, u))
    rhs = sp.kn(1, w) / (w * sp.kn(0, w))
    return lhs + rhs

def findbTE(V, m):
    if m <= 0:
        raise ValueError("m ne peut pas être négatif")
    if V <= 0:
        raise ValueError("V ne peut pas être négatif")
    delta = 1e-6
    j0z = sp.jn_zeros(0, m)
    j1z = sp.jn_zeros(1, m)
    lo = max(0, 1 - (j1z[m - 1] / V)**2) + delta
    hi = 1 - (j0z[m - 1] / V)**2 - delta
    if hi < lo:
        return None
    try:
        b = op.brentq(eqnTE, lo, hi, args=(V,))
    except ValueError:
        return None
    return b



