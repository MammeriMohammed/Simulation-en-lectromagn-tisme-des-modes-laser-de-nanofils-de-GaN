#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 23:46:49 2024

@author: mohamed
"""


from TM import findbTM
from TE import findbTE
from HE import findbHE
from EH import findbEH
from get_cutoff import cutoff
import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
import itertools



def modes(V, nc, ng, nb, plot_flag):
    mode_TM = {}                                # cree les dict pour chaque famille de mode
    mode_TE = {}
    mode_HE = {}
    mode_EH = {}
    
    # TE0m
    for m in range(1, nb):    # pour les modes TE0m  l'ordre de bessel est nul, on itere seulement sur le numéro du zero de bessel 
        mode_name = f"TE0,{m}"      # cree la clé pour le mode dans le dict  
        mode_TE[mode_name] = []
        for i in range(len(V)): # on itere sur les valeurs de V dans la liste fournie 
            b = findbTE(V[i], m)   # la fonction findbTE trouve la constate normalisé b pour une fréquence normalisé V donné avec le numéro de la sol 
            mode_TE[mode_name].append(b if b is not None else None) # pour chaque valeur de V on garde b lorsqe ce dernier est définit
        if mode_name in mode_TE and all(b is None for b in mode_TE[mode_name]): # si la liste est vide on la suprime et on s'arrete
            del mode_TE[mode_name]
            break
    cutoff_TE = cutoff(mode_TE, V)      # cherche la fréquence de coupure pour chaque mode dans le dict

    # TM0m
    for m in range(1, nb):                      # Les modes TM0m on suit la meme démarche que pour les modes TE0m
        mode_name = f"TM0,{m}"
        mode_TM[mode_name] = []
        for i in range(len(V)):
            b = findbTM(V[i], m, nc, ng)
            mode_TM[mode_name].append(b if b is not None else None)
        if mode_name in mode_TM and all(b is None for b in mode_TM[mode_name]):
            del mode_TM[mode_name]
            break
    cutoff_TM = cutoff(mode_TM, V)

    # HElm
    for l in range(1, nb):                      # pour les modes HElm on itere sur l'ordre l et pour chaque ordre les valeurs de m possible
        for m in range(1, nb):                  # ensuite la démarche reste la meme que pour les autres modes
            mode_name = f"HE{l},{m}"
            mode_HE[mode_name] = []
            for i in range(len(V)):
                b = findbHE(V[i], l, m, nc, ng)
                mode_HE[mode_name].append(b if b is not None else None)
            if mode_name in mode_HE and all(b is None for b in mode_HE[mode_name]):
                del mode_HE[mode_name]
                break
    cutoff_HE = cutoff(mode_HE, V)

    # EHlm
    for l in range(1, nb):                      # idem que HElm
        for m in range(1, nb):
            mode_name = f"EH{l},{m}"
            mode_EH[mode_name] = []
            for i in range(len(V)):
                b = findbEH(V[i], l, m, nc, ng)
                mode_EH[mode_name].append(b if b is not None else None)
            if mode_name in mode_EH and all(b is None for b in mode_EH[mode_name]):
                del mode_EH[mode_name]
                break
    cutoff_EH = cutoff(mode_EH, V)

    cutoffs = {}
    for cut in [cutoff_TE, cutoff_TM, cutoff_EH, cutoff_HE]:                #Le but est de regrouper tout les fréquences de coupures dans un seul dict
        for key,value in cut.items():                                       # on itere sur les dicts de chaque famille et pour chaque famille on récupere les
            if value is not None:                                           # fréquences de coupure et pour éviter les erreurs eviter que ça soit une valeur non déf
                cutoffs[key] = value

    all_modes = {}   
    for temp in [mode_TE, mode_TM, mode_HE, mode_EH]:               # pareil que les fréqunces de coupures
        if temp is not None:
            for key, value in temp.items():
                all_modes[key] = value
                    
                    
                    
                    
                    
    if plot_flag:                                                   # si le flag est True il crée la figure et itere sur dans chaque dict de mode pour ret
        plt.figure(figsize=(10, 6))
        markers = itertools.cycle(['o', 's','^', 'D', 'v', '*', '.', ',', 'p', '<','>'])
        for key, value in mode_HE.items():
            plt.plot(V, value, label=key, marker = next(markers))
        for key, value in mode_EH.items():
            plt.plot(V, value, label=key, marker = next(markers))
        for key, value in mode_TE.items():
            plt.plot(V, value, label=key, marker = next(markers))
        for key, value in mode_TM.items():
            plt.plot(V, value, label=key, marker = next(markers))
       # plt.ylabel("Constante de propagation b", fontsize = 25)
        #plt.xlabel("Fréquence normalisé V", fontsize = 25)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.legend(fontsize=25)
        plt.minorticks_on()
        plt.grid(which='major', linestyle='--', color='black')
        plt.grid(which='minor', linestyle='--', color='grey')        
        fig = f'/home/mohamed/Documents/Stage/Fig/b=f(V)_{nc}{ng}.png' # sauvegarde automatiquement la fig
        plt.savefig(fig)
        print("saved")
        plt.show()
         
    return all_modes, cutoffs


# exemple d'utilisation
# changer l'indice du coeur et de la gaaine, nb n'est pas le nombre max de mode mais le nombre max de m et de l peut mettre
"""
nc = 5.25                                                         # ni'mporte quel valeur arbitraire assez grande pour trouver tout les modes
ng = 1
nb = 5

V = np.linspace(1e-6, 6, 100)                   # cree la liste de V         
all_modes, cut = modes(V, nc, ng, nb, True)   # appel la fonction et récuperer les fréquences de coup et le dict des modes
now = datetime.datetime.now()                       # récupere le temps en tant que string 
time = now.strftime("%m_%d_%H:%M:%S")               # change le format du temps 

path = f'/home/mohamed/Documents/Stage/Fig/mode_{nc}_{ng}_{time}.csv'       # spécifier le chemin pour sauvegarder le fichier en csv
headers = ["Mode", "Cutoff"]                            

with open(path, mode="w", newline='') as file:
    writer = csv.writer(file)
    
    # Écrire le Header
    writer.writerow(headers)
    
    # Écrire les valeurs de chaque modes
    for key, value in all_modes.items(): 
        writer.writerow([key, value])
print("done!")                                     
     
"""      
    