#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 03:05:48 2024

@author: mohamed
"""

import numpy as np
import matplotlib.pyplot as plt

Eg = 3.2
alpha0 = 2.2e-5 # GaN
h = (6.62e-34)/(1.6e-19)
c = 3e8
N = 100
def alphaf(E):
    if E < Eg :
        return None
    else :
        return alpha0*np.sqrt(E - Eg) / E * 1e6 
            
    
    return 
lam = np.linspace(300e-9, 400e-9, N + 1)
# E in eV
E = [ h * c / l for l in lam ]


alpha = []
for e in E :
    alpha.append(alphaf(e))
    
    
plt.plot(E, alpha)
plt.xlabel("Energie en eV", fontsize = 25)
plt.ylabel("coéfficient d'absorption (1/µm)", fontsize = 25)
plt.minorticks_on()
plt.grid(which = 'minor', linestyle =':' , color = "grey")
plt.grid(which = 'major', linestyle = '-', color = 'grey')
plt.grid(True)
plt.legend(fontsize = 25)
plt.xticks(fontsize = 25)
plt.yticks(fontsize = 25)
plt.show()
    
