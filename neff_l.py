#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 01:10:35 2024

@author: mohamed
"""
import numpy as np
import matplotlib.pyplot as plt
from modes_ import modes 

def beta(b, l, a):
    ON = np.sqrt(nc**2 - ng**2)  
    V = 2 * np.pi * a / l * ON
    u = V * np.sqrt(1 - b)
    k0 = 2 * np.pi / l
    beta1 = k0 * nc
    beta = np.sqrt(beta1**2 - (u / a)**2)
    return beta

def neff(b, l, a):
    k0 = 2 * np.pi / l
    temp = beta(b, l, a)
    n = temp / k0
    return n


# Définir les paramètres nécessaires
nc = 2.3
ng = 1.0
nb = 5
ON = np.sqrt(nc**2 - ng**2)
a = 300e-9
lmin = 100e-9
lmax = 2000e-9
N = 100
lam = np.linspace(lmin, lmax, N)
c = 3e8
delta = 1e-6
x = [a * 2 * np.pi / l * ON for l in lam]

temp, all_cutoffs_a = modes(x, nc, ng, nb, False)



modes_neff = {}
for key, value in temp.items():
    modes_neff[key] = [neff(b, lam[i], a) if b is not None else None for i, b in enumerate(value)]

p = [l / a for l in lam]

plt.figure(figsize=(10, 6))
t = ["HE1,1", "HE1,2", "HE2,1", "HE2,2","HE3,1","HE4,1", "EH1,1", "EH2,1", "TE0,1", "TE0,2", "TM0,1", "TM0,2"]
fig, ax = plt.subplots()
for key, value in modes_neff.items():
    if key in t:
        ax.plot(p, value, label=key)
n = 1.2
o = 4 
ax.scatter(o,n, label = "Mode 0 fig 2.11")
ax.scatter(o, 1.992, label = "Mode fondamental")
ax.set_xlabel('lambda/a (u.a)', fontsize = 25)
ax.set_ylabel('neff', fontsize = 25)
ax.legend(fontsize = 25)
ax.grid(True)
ax.minorticks_on()
ax.grid(which='major', linestyle='--', color='black')
ax.grid(which='minor', linestyle='--', color='grey')
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.show()
