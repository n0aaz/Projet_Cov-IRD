import matplotlib.pyplot as plt 
import numpy as np
from modeles_SIRD import *
from fonctions_math import integrale_degueu
from donnees import temps_lisible,generer_jours_simulation
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors

def reglage_axe_x(x_entree,nbvaleurs):
    position_xticks=[floor(k*len(x_entree)/nbvaleurs) for k in range(nbvaleurs)] #subdivisions égales de l'axe
    position_xticks.append(len(x_entree)-1) #on n'oublie pas la dernière valeur
    x_partiel=[temps_lisible(x_entree[pos]) for pos in position_xticks ]
    plt.xticks(position_xticks,x_partiel)

def afficheur(theta,longueur,Table_deces,Table_infection):
    plt.rcParams['figure.figsize'] = [8, 5]
    x=np.arange(1,longueur)
    nbvaleurs=5
    
    # Rappel des paramètres de SIRD_Flexible : 
    # beta0,gamma0,mu0,t,beta=beta0,gamma=gamma0,mu=mu0,N=65e6,initial=[N-2,2,0,0]
    y=SIRD_Flexible(theta[0],theta[1],theta[2],x)
    
    plt.subplot(221)
    plt.plot(x,integrale_degueu(y[1]),label='Simulation')
    plt.plot(x[:min(len(Table_infection),longueur)],Table_infection[:min(len(Table_infection),longueur)],label='Réel')
    plt.ylabel('Infections')
    plt.title("Nombre d'infectés cumulés")
    plt.legend()
    plt.grid()
    
    plt.subplot(222)
    plt.plot(x,y[3],label='Simulation')
    plt.plot(x[:min(len(Table_deces),longueur)],Table_deces[:min(len(Table_deces),longueur)],label='Réel')
    plt.ylabel('Décès')
    plt.title('Nombre de décès cumulés')
    plt.legend()
    plt.grid()
    
    plt.subplot(223)
    plt.plot(x,y[1],label='Simulation')
    plt.plot(x[:min(len(Table_infection),longueur)-1],derivee(Table_infection[:min(len(Table_infection),longueur)],1),label='Réel')
    plt.xlabel('Jours depuis le premier cas')
    plt.ylabel('Infections')
    plt.title("Nombre d'infections journalières")
    plt.legend()
    plt.grid()
    
    plt.subplot(224)
    plt.plot(x[:-1],derivee(y[3],1),label='Simulation')
    plt.plot(x[:min(len(Table_deces),longueur)-1],derivee(Table_deces[:min(len(Table_deces),longueur)],1),label='Réel')
    plt.xlabel('Jours depuis le premier cas')
    plt.ylabel('Décès')
    plt.title("Nombre de décès journaliers")
    plt.legend()
    plt.grid()

    plt.tight_layout(pad=2.0)
    plt.show()

def affichage_compare(fig,localisation,x,reel,simulation,nom):
    x_graphe,y_graphe= localisation
    fig.add_trace(
        go.Scatter(
            x=x, 
            y=reel,
            name = nom+' Réel',
            mode= 'lines+markers'
            ),
        row=y_graphe,col=x_graphe
    )
    fig.add_trace(
        go.Scatter(
            x=generer_jours_simulation(x), 
            y=simulation,
            mode = 'lines',
            name= nom+' Simulation'
            ),
        row=y_graphe,col=x_graphe
    )

def code_couleur(tableau,mini,maxi):
    tab_coul=n_colors('rgb(200, 100, 100)', 'rgb(100, 200, 100)', 100, colortype='rgb')
    tab_pourcent= [np.int((v-mini)*100/(maxi-mini)) for v in tableau]
    print(tab_pourcent)
    return np.array(tab_coul)[tab_pourcent]