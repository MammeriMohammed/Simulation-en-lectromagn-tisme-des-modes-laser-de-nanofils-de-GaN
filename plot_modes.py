import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
from matplotlib import cm
import matplotlib.animation as animation

def plot_mode(u, mode, v, m):
    N = 500                                          #définit le nb de point
    x = np.linspace(-2*a, 2*a, N)                    # crée les noeuds x et y
    y = np.linspace(-2*a, 2*a, N)               
    X, Y = np.meshgrid(x, y)                        #  crée un grid cartésien table 2D
    R = np.sqrt(X**2 + Y**2)                        # définit le rayon et l'angle Theta pour le calcul et phi pour la visualisation 
    Phi = Theta =np.arctan2(Y, X)
    
    if mode == "TE":
        if v != 0:
            print("v doit être nul")
            return
        if m == 0:
            print("m ne doit pas être nul")
            return
        def Et(R):                                              # calcul la composante transverse du champ électrique à l'interieur 
            tem = []                                            # du nanofil (cercle blanc) et à l'exterieur (la gaine)
            Et = np.zeros_like(R) 
            for i in range(R.shape[0]):
                for j in range(R.shape[1]):
                    r = R[i, j]
                    if r <= a:
                        Et[i, j] = E0 * sp.jv(0, (u * r / a))
                    else:
                        Et[i, j] = -E0 * (u / w) * (sp.jv(0, u) / sp.kv(0, w)) * sp.kv(0, (w * r / a))
            return Et
    
        Ep = Et(R)                                          # Calcul Ex et Ey à partir de Et parce que dans le mode TE Ephi (polaire) c'est la composante
        Ex = - Ep * np.sin(Theta)                           # transverse
        Ey = Ep * np.cos(Theta)
        E = Ex + Ey
    
    elif mode == "TM":
        if v != 0:
            print("v doit être nul")
            return
        if m == 0:
            print("m ne doit pas être nul")
            return
        def Et(R):                                      # calcul la composante transverse du champ électrique à l'interieur 
                                                      # du nanofil (cercle blanc) et à l'exterieur (la gaine)
            Et = np.zeros_like(R) 
            for i in range(R.shape[0]):
                for j in range(R.shape[1]):
                    r = R[i, j]
                    if r <= a:
                       Et[i, j] = E0 * sp.jv(0, (u * r / a))
                    else:
                       Et[i, j] = -E0 * (u / w) * (sp.jv(0, u) / sp.kv(0, w)) * sp.kv(0, (w * r / a))
            return Et
    
        Ep = Et(R)                                      # calcul Ex, et Ey à partir du champ électrique Er dans le cas d'un mode TM
        Ex = Ep * np.cos(Theta)
        Ey = Ep * np.sin(Theta)
        E = Ex + Ey
        
    elif mode == "HE":
        if v == 0:
            print("v ne doit pas être nul")
            return
        if m == 0:
            print("m ne doit pas être nul")
            return
        def Er_phi(R, Phi):
            Er = np.zeros_like(R)
            Ephi = np.zeros_like(R)                             # calcul le champ électrique à l'interieur et à l'exterieur du coeur
            for i in range(R.shape[0]):
                for j in range(R.shape[1]):
                    r = R[i, j]
                    if r <= a:
                        Er[i, j] = -E0 * sp.jv(v - 1, (u * r / a)) * np.sin(v * Phi[i,j] + phase)
                        Ephi[i, j] = -E0 * sp.jv(v - 1, (u * r / a)) * np.cos(v * Phi[i,j] + phase)
                    else:
                        Er[i, j] = -E0 * (u / w) * (sp.jv(v, u) / sp.kv(v, w)) * sp.kv(v - 1, (w * r / a)) * np.sin(v * Phi[i,j] + phase)
                        Ephi[i, j] = -E0 * (u / w) * (sp.jv(v, u) / sp.kv(v, w)) * sp.kv(v - 1, (w * r / a)) * np.cos(v * Phi[i,j] + phase)
            return Er, Ephi

        Er, Ephi = Er_phi(R, Phi)                               # calcul Ex et Ey à partir de Ephi et Er ^
        Ex = Er * np.cos(Theta) - Ephi * np.sin(Theta)
        Ey = Er * np.sin(Theta) + Ephi * np.cos(Theta)
        E = Ex + Ey
        
    elif mode == "EH":
        if v == 0:
            print("v ne doit pas être nul")
            return
        if m == 0:
            print("m ne doit pas être nul")
            return
        def Er_phi(R, Phi):
            Er = np.zeros_like(R)                                   # crée un mesh pour Er et Ephi identique à R
            Ephi = np.zeros_like(R)

            for i in range(R.shape[0]):                             # boucle sur chaque elemnt du mesh de R parce que
                for j in range(R.shape[1]):                         # le champ est définit à l'intrieur par une fct et à l'exterieur par une autre fct
                    r = R[i, j]
                    if r <= a:
                        Er[i, j] = E0 * sp.jv(v + 1, (u * r / a)) * np.sin(v * Phi[i, j])
                        Ephi[i, j] = -E0 * sp.jv(v + 1, (u * r / a)) * np.cos(v * Phi[i, j])
                    else:
                        Er[i, j] = -E0 * (u / w) * (sp.jv(v, u) / sp.kv(v, w)) * sp.kv(v + 1, (w * r / a)) * np.sin(v * Phi[i, j])
                        Ephi[i, j] = E0 * (u / w) * (sp.jv(v, u) / sp.kv(v, w)) * sp.kv(v + 1, (w * r / a)) * np.cos(v * Phi[i, j])
            return Er, Ephi

        Er, Ephi = Er_phi(R, Phi)
        Ex = Er * np.cos(Theta) - Ephi * np.sin(Theta)  # passage de coordonnées cylindriques en coordonnées cartésienns
        Ey = Er * np.sin(Theta) + Ephi * np.cos(Theta)  
        E = Ex + Ey
        
    string = f"{mode}{v},{m}"
    fig = plt.figure()
    axs = fig.add_subplot(1, 2, 1)
    im = axs.imshow(E**2 , cmap='hot', extent=(-2*a, 2*a, -2*a, 2*a))
    cb = fig.colorbar(im, ax=axs, shrink=0.5, aspect=5)
    cb.set_label('Intensité')
    streamE = axs.streamplot(X, Y, Ex, Ey, color='blue', linewidth=0.6)
    b = np.linspace(1e-6, 2 * np.pi, 100)
    x = [a * np.cos(t) for t in b]
    y = [a * np.sin(t) for t in b]
    axs.plot(x, y, color='white')
    
    axs.set_title(f'Champ électrique du mode {string}')
    axs.set_xlabel('x')
    axs.set_ylabel('y')
    axs.set_aspect('equal', 'box')
    
    axs = fig.add_subplot(1, 2, 2, projection='3d')
    surf = axs.plot_surface(X, Y, E**2, cmap='hot', linewidth=0, antialiased=True)
    cset = axs.contour(X, Y, E**2, zdir='x', offset=-2*a, cmap='hot', alpha = 1)
    cset = axs.contour(X, Y, E**2, zdir='y', offset=2*a, cmap='hot', alpha =1)
    axs.set_xlim3d(-2*a, 2*a)
    axs.set_ylim3d(-2*a, 2*a)
    axs.set_title(f'Intensité du mode {string}')
    axs.set_xlabel('x')
    axs.set_ylabel('y')
    axs.set_zlabel('Intensité')
    cbar = fig.colorbar(surf, ax=axs, shrink=0.5, aspect=5)
    cbar.set_label('Intensité')
    plt.tight_layout()
    plt.show()
    
    return 
#Exemple
a = 150
E0 = 1
phase = 0
N = 100

mode = "HE" # mode selectionner
cut = 2.4     #fréquence de coupure
v = 1
m = 1
V = 8
c = "c"
w = np.sqrt(V**2 - cut**2)

plot_mode(cut, mode, v, m)


