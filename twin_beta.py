#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 01:25:42 2024

@author: mohamed
"""

import numpy as np
import matplotlib.pyplot as plt
from modes_ import modes

def beta(b, l, a):
    V = 2 * np.pi * a / l * ON
    u = V * np.sqrt(b)
    k0 = 2 * np.pi / l
    beta1 = k0 * nc
    beta = np.sqrt(beta1**2 - (u / a)**2)
    return beta


def neff(b, l, a):
    k0 = 2 * np.pi / l
    temp = beta(b, l, a)
    n = temp / k0
    return n

nc = 2.5
ng = 1.0
nb = 3
ON = np.sqrt(nc**2 - ng**2)
a = 400e-9
lmin = 320e-9
lmax = 450e-9
N = 100
lam = np.linspace(lmin, lmax, N + 1)
c = 3e8
A = 1e-6
h = (6.62e-34)/(1.6e-19)
x = [a * 2 * np.pi / l * ON for l in lam]
E = [ h * c / t for t in lam ]
w = [2 * np.pi * A / ( l  ) for l in lam]
temp, all_cutoffs_a = modes(x, nc, ng, nb, False)

modes_l = {}
for key, value in temp.items():
    modes_l[key] = [beta(V, lam[i], a) if V is not None else np.nan for i, V in enumerate(value)]

fig = plt.figure(figsize=plt.figaspect(.4))
fig, ax = plt.subplots(figsize=(10, 6))


# Tracer les courbes sur le premier axe
for key, value in modes_l.items():
    ax.plot(E, value, label=key)

#ax.set_xlabel("Energie (eV)")
#ax.set_ylabel('Constante de propagation Beta (1/m)')
ax.tick_params('x' )
ax.tick_params('y')
ax.legend(fontsize = 25)
ax.grid(which='major', linestyle='--', color='black')
ax.grid(which='minor', linestyle='--', color='grey')
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
# Création du deuxième axe x
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
#ax2.set_xlabel("Longeur d'onde")

# Mettre à jour l'échelle du deuxième axe x
new_tick_locations = ax.get_xticks()
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels([f'{h*c/E:.2e}' for E in new_tick_locations], rotation = 45)
#ax2.set_xticklabels([f'{a * 2 * np.pi / l * ON:.2}' for l in new_tick_locations], rotation = 45)
#ax.set_xlabel('Energie eV', fontsize = 25)
#ax.set_ylabel('neff', fontsize = 25)
#ax2.set_xlabel('lambda (1/m)', fontsize = 25)
#ax2.set_ylabel('neff', fontsize = 25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
"""

x = [a * 2 * np.pi / l * ON for l in lam]
kc = [t /  nc for t in w]
kg = [t /  ng for t in w]
temp, all_cutoffs_a = modes(x, nc, ng, nb, False)

# Convertir les valeurs de b en neff
modes_beta = {}
for key, value in temp.items():
    modes_beta[key] = [neff(V, lam[i], a) * 2 * np.pi * A / (lam[i]) if V is not None else np.nan for i, V in enumerate(value)]


ax = fig.add_subplot(1, 2, 2)
for key, value in modes_beta.items() :
    ax.plot(value, w, label = key)

ax.plot(kc, w, label = 'nc = 2.5')
ax.plot(kg, w, label = 'ng = 1')
ax.set_xlabel(" K normalisé")
ax.set_ylabel("w normalisé")
ax.legend()
ax.grid(True)


"""


plt.show()
