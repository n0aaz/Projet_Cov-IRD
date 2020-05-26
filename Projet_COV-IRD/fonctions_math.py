import numpy as np
import scipy.stats as stats

############ Ensemble des fonctions mathématiques qui serviront pour les calculs #########
def derivee(tableau,dx):
    return np.diff(tableau)/dx

def normale(alpha,mu,sigma,t):
    return alpha*stats.norm.pdf(t, mu, sigma)

def indicatrice_sup(x,a): #indicatrice mathématique renvoie 1 si x>=a 0 sinon
    return int(x>=a)

def integrale_degueu(tableau): # mon prof de maths me cracherait dessus s'il voyait ça mais bon , tant que ça marche...
    out=[tableau[0]]
    s=tableau[0]
    for elem in tableau[1:]:
        s+=elem
        out.append(s)
    return out

def remplace_fonction(constante,fonction):
    if (fonction==None):
        return lambda x : constante
    else: 
        return fonction
