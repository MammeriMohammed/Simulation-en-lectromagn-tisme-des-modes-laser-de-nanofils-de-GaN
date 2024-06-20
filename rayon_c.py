#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 23:17:55 2024

@author: mohamed
"""

import numpy as np
import matplotlib.pyplot as plt

nc = 2.5
ng = 1
N = 100
ON = np.sqrt(nc**2 - ng**2)
V = 2.40
pente = 2.40 / (ON * 2*np.pi)


l = np.linspace(100, 4000, N + 1)

a = [ pente * x for x in l] 

plt.plot(l, a, label = "a0= f(lambda0)",color = 'orange')
plt.xticks(fontsize = 25)
plt.yticks(fontsize = 25)
plt.xlabel("longeur d'onde  (nm)", fontsize = 25)
plt.ylabel("rayon (nm)", fontsize = 25)
plt.legend(fontsize = 25)
plt.minorticks_on()
plt.grid(which='major', linestyle='dashed', color='grey')
plt.grid(which='minor', linestyle='dotted', color='grey')
plt.show()
