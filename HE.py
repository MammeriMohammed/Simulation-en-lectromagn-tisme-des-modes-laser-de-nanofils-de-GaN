#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:22:43 2024

@author: mohamed
"""


import numpy as np
import scipy.special as sp
import scipy.optimize as op
import matplotlib.pyplot as plt



def eqn(b, V, l):
    U = V * np.sqrt(1 - b)
    W = V * np.sqrt(b)
    f1 = U * sp.jv(l - 1, U) / sp.jv(l, U)
    f2 = W * sp.kn(l - 1, W) / sp.kn(l, W)
    return f1 + f2

   
def findbHE(V, l, m, nc, ng):
    l = l - 1
    if l < 0:
        l *= -1  

    delta = 1e-6
    jnz = sp.jn_zeros(l, m)
    lo = max(0, 1 - (jnz[m - 1] / V)**2) + delta

    if m == 1:
        hi = 1 - delta
    else:
        hi = 1 - (jnz[m - 2] / V)**2 - delta

    if hi < lo:
        return None  

    try:
        b = op.brentq(eqn, lo, hi, args=(V, l))
    except ValueError:  
        return None

    return b

"""
# Example usage
N = 100
V = np.linspace(0.1, 6, N + 1)
m_values = [1, 2]
modes = {}

for m in m_values:
    v = 3
    l = v - 1
    mode_name = f"HE{v}{m}"
    modes[mode_name] = []
    for i in range(N + 1):
        b_value = findbHE(V[i], l,m)
        if b_value is not None:
            modes[mode_name].append(b_value)
        else:
            modes[mode_name].append(np.nan)

for key, value in modes.items():
    plt.plot(V, value, label=key)
plt.legend()
plt.minorticks_on()
plt.grid(which='major', linestyle=':', color='grey')
plt.grid(which='minor', linestyle=':', color='grey')
plt.xlabel('V')
plt.ylabel('b')
plt.title('Modes HE in Fiber Optics')
plt.show()
"""
