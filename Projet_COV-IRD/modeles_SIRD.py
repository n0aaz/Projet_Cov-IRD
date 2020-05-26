from fonctions_math import *
from math import exp,floor
from scipy.integrate import odeint #Va nous permettre de résoudre des équations différentielles

# Version la plus complexe , celle ci permet de pouvoir considérer beta comme étant une fonction par morceaux
# linéaire et d'ordre 1 et avec une pente différente sur chaque morceau

def SIRD(beta0,k,gamma,delta,lamda,t,h=[],beta1=0,initial=[1,1,0,0]):
    #Ic : nombre de personnes contagieuses
    #Wc : nombre de personnes infectées
    #L : nombre de personnes infectées isolées qui mourront sans infecter d'autres personnes
    #D : nombre de personnes mortes
    #Ic0,Wc0,L0,D0=1,1,0,0 #peut être à donner en paramètre à optimiser?
    conditions_initiales=np.array(initial,dtype='float64')
    
    beta_old= lambda x : beta0*exp(-k*x)+beta1 #la forme exponentielle ne nous avance pas plus
    
    def beta_inflexion(x):
        tab_pts_inflexion = np.array([t[floor(k*len(t)/len(h))] for k in range(len(h))],dtype='float64')
        tab_indicatrices= np.array([indicatrice_sup(x,tau) for tau in tab_pts_inflexion],dtype='float64')
        return beta0 + x*(k+np.dot(h,tab_indicatrices)) #produit scalaire donc comprend somme et produit terme à terme

    if(len(h)==0): #doit détecter automatiquement si on utilise le modèle à inflexion
        beta= beta_old
    else: 
        beta= beta_inflexion
    
    def modele(y,t1):
        Ic=y[0]
        Wc=y[1]
        L=y[2]
        D=y[3]
        
        d_Ic= (beta(t1)-gamma-delta)*Ic
        d_Wc = beta(t1)*Ic
        d_L = delta*Ic - lamda*L
        d_D = lamda*L
        
        return np.array([d_Ic,d_Wc,d_L,d_D],dtype='float64')
    
    resultat= odeint(modele,conditions_initiales,t)
    return np.transpose(resultat) #on renvoie la transposée sinon Ic,Wc,L,D seront sur les colonnes, peu pratique

# Version simplifiée après les problèmes de la première version avec Beta de la forme (b0+b1*exp(-k*t))
def SIRD_new(beta0,k,gamma,mu,t,beta1=0,initial=[1,1,0,1]):
    beta= lambda x : beta0+beta1*exp(-k*x) # Beta de la forme (b0+b1*exp(-k*t))
    def modele(y,t1):
        S,I,R,D=y
        
        dS= - beta(t1) * S * I
        dI= (beta(t1) * S - gamma - mu)*I
        dR= gamma*I
        dD= mu*I
        
        return dS,dI,dR,dD
    
    resultat= odeint(modele,np.array(initial,dtype='float64' ),t).T
    return resultat

# Variation du précédent mais cette fois en considérant aussi gamma comme étant une variable
def SIRD_tout_variable(beta0,k,gamma0,mu,t,beta1=0,gamma1=0,initial=[1,1,0,1]):
    # cette fois ci, tous les coeff sont des constantes
    beta= lambda x : beta0#+beta1*np.exp(-k*x) #la forme exponentielle ne nous avance pas plus
    gamma = lambda x : gamma0 #+ gamma1/(1+np.exp(-x+1/30) )
    
    def modele(y,t1):
        S,I,R,D=y
        
        dS= - beta(t1) * S * I
        dI= (beta(t1) * S - gamma(t1) - mu)*I
        dR= gamma(t1)*I
        dD= mu*I
        
        return dS,dI,dR,dD

    resultat= odeint(modele,np.array(initial,dtype='float64'),t).T
    return resultat

# On va essayer d'en faire une version plus flexible et compacte qui prendrait tout en compte: 
# Les fonctions beta gamma et mu seront fournies de l'extérieur si non constantes
def SIRD_Flexible(beta0,gamma0,mu0,t,beta=None,gamma=None,mu=None,initial=[(60e6)-2,2,0,0]):
    beta,gamma,mu = remplace_fonction(beta0,beta),remplace_fonction(gamma0,gamma),remplace_fonction(mu0,mu)
    N=initial[0]+initial[1]
    def modele(y,t1):
        S,I,R,D=y
        dS= - beta(t1) * S * I / N
        dI= (beta(t1) * S / N - gamma(t1) - mu(t1))*I
        dR= gamma(t1)*I
        dD= mu(t1)*I
        return np.array([dS,dI,dR,dD],dtype='float64')

    resultat= odeint(modele,initial,t).T # Résout le systeme d'équadiff précisé par "modele"
    return resultat