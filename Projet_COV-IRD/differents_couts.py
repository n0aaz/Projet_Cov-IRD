from modeles_SIRD import *

################################### DIFFERENTES FONCTIONS DE COUT #########################################

############# Toutes les versions précédentes utilisent des tables codées en dur , corrigeons cela ##########

def cout_flexible(parametres,D_reel,I_reel):
    # Rappel des paramètres de SIRD_Flexible : 
    # beta0,gamma0,mu0,t,beta=beta0,gamma=gamma0,mu=mu0,N=65e6,initial=[N-2,2,0,0]
    t = np.arange(len(D_reel))
    beta0,gamma0,mu0=parametres
    S,I,R,D= SIRD_Flexible(beta0,gamma0,mu0,t)
    residu_morts =  D_reel[:-1]-D[:-1]
    residu_infectes = derivee(I_reel,1)-I[:-1] # ATTENTION : le I_reel fourni chez nous sera un nombre total d'infectés (une intégrale) !
    return residu_infectes + residu_morts
