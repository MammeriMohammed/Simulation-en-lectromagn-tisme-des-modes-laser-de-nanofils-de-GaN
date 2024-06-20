#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 03:10:49 2024

@author: mohamed
"""

import numpy as np
import scipy.optimize as op
import scipy.special as sp
import matplotlib.pyplot as plt


def eqnEH(b, V, l, nc, ng):
    u = V * np.sqrt(1 - b)
    w = V * np.sqrt(b)
    jp = sp.jvp(l, u)
    kp = sp.kvp(l, w)
    j = sp.jv(l, u)
    k = sp.kv(l, w)
    lhs = nc **2 * jp / (u * j)
    f1 = - 0.5 * (nc**2 + ng**2) * kp / ( w * k)
    f2 =  np.sqrt( ((nc**2 - ng**2)* 0.5 *kp / ( w * k ) )**2 + ( nc * l ) ** 2 * (1 / u ** 2 + 1 / w **2) * ( nc**2/u**2 + ng ** 2 / w ** 2 ) )
    rhs = f1 + f2            # + si EHlm - si HElm
    return lhs - rhs
    


def findbEH(V, l , m, nc, ng):
    if l < 0 :
        l *= - 1
    if m <= 0:
        raise ValueError("m ne peut pas etre négative")
    if V <= 0:
        return ValueError("V ne peut pas etre négative")
    delta = 1e-6
    jmz = sp.jn_zeros(l, m + 1)
    lo = max(0, 1 - (jmz[m - 2] / V)**2) + delta
    hi = 1 - (jmz[m - 1] / V)**2 - delta
    if hi < lo:
        return None
    try:
        b = op.brentq(eqnEH, lo, hi, args=(V,l, nc,ng))
    except ValueError:
        return None
    return b


