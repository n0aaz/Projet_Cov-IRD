####################### COUTS OBSOLETES ####################

# Ces fonctions de cout ont été codées sur et pour jupyter Notebook, dans une architecture multifichiers
# elles n'ont alors plus leur place. Pour des raisons d'archivage je vais tout de même les garder ici


def cout(theta): #fonction de cout pour le modele SIRD
    nb_jours=len(Table_infection)
    
    #theta contient tous nos arguments pour la fonction SIRD
    #[beta0,k,gamma,delta,lamda] = theta 
    estime=SIRD(theta[0],theta[1],theta[2],theta[3],theta[4],np.arange(nb_jours))
    
    infectes,deces = estime[1],estime[3]
    
    residus_infectes=np.array(Table_infection-infectes,dtype='float64')
    residus_deces= np.array(Table_deces-deces,dtype='float64')
    
    #print(residus_infectes**2+residus_deces**2)
    return np.sum(residus_infectes**2+residus_deces**2)

def cout_exp_double(theta): #fonction de cout pour le modele SIRD
    nb_jours=len(Table_infection)
    
    #theta contient tous nos arguments pour la fonction SIRD
    #[beta0,k,gamma,delta,lamda] = theta 
    estime=SIRD(theta[0],theta[1],theta[2],theta[3],theta[4],np.arange(nb_jours),[],theta[5])
    
    infectes,deces = estime[1],estime[3]
    
    residus_infectes=np.array(Table_infection-infectes,dtype='float64')
    residus_deces= np.array(Table_deces-deces,dtype='float64')
    
    #print(residus_infectes**2+residus_deces**2)
    return np.sum(residus_infectes**2+residus_deces**2)

def cout_exp_2(theta): #fonction de cout pour le modele SIRD
    nb_jours=len(Table_infection)
    
    #theta contient tous nos arguments pour la fonction SIRD
    #[beta0,k,gamma,delta,lamda] = theta 
    estime=SIRD(theta[0],theta[1],theta[2],theta[3],theta[4],np.arange(nb_jours),[],theta[5],[theta[6],theta[7],theta[8],theta[9]])
    
    infectes,deces = estime[1],estime[3]
    
    residus_infectes=np.array(Table_infection-infectes,dtype='float64')
    residus_deces= np.array(Table_deces-deces,dtype='float64')
    
    #print(residus_infectes**2+residus_deces**2)
    #return np.sum(residus_infectes**2+residus_deces**2)
    return np.sum(residus_infectes**2)

def cout2(theta): #fonction de cout pour le modèle normal
    nb_jours=len(Table_infection)
    
    #theta contient tous nos arguments pour la fonction SIRD
    #[alpha,sigma,mu] = theta 
    estime=normale(theta[0],theta[1],theta[2],np.arange(nb_jours))

    residus_infectes=np.array(Table_infection-estime,dtype='float64')

    #print(residus_infectes**2)
    return np.sum(abs(residus_infectes))

def cout_inflexion(theta): #fonction de cout pour le modele SIRD
    nb_jours=len(Table_infection)
    
    #theta contient tous nos arguments pour la fonction SIRD
    #[beta0,k,gamma,delta,lamda,h] = theta 
    
    h=theta[5:] #h se situe après les 5 variables 
    print('h=',h)
    estime=SIRD(theta[0],theta[1],theta[2],theta[3],theta[4],np.arange(nb_jours),h)
    
    infectes,deces = estime[1],estime[3]
    
    residus_infectes=np.array(Table_infection-infectes,dtype='float64')
    residus_deces= np.array(Table_deces-deces,dtype='float64')
    
    #print(residus_infectes**2+residus_deces**2)
    return np.sum(np.sqrt(residus_infectes**2+residus_deces**2))

def cout_exp_simple(theta): #fonction de cout pour le modele SIRD
    nb_jours=len(Table_deces)
    
    #theta contient tous nos arguments pour la fonction SIRD
    #[beta0,k,gamma,delta,lamda] = theta 
    estime=SIRD_new(theta[0],theta[1],theta[2],theta[3],np.arange(nb_jours),theta[4])
    
    infectes,deces = estime[1],estime[3]
    
    #residus_infectes=np.array(Table_infection-infectes,dtype='float64')
    residus_deces= np.array(Table_deces-deces,dtype='float64')

    return np.abs(residus_deces) #On ne va fit que sur les décès

def cout_exp_simple(theta): #fonction de cout pour le modele SIRD
    nb_jours=len(Table_deces)
    initiaux= theta[5:]
    print(initiaux)
    
    #theta contient tous nos arguments pour la fonction SIRD
    #[beta0,k,gamma,mu,beta1] = theta 
    if(len(initiaux)==0):
        estime=SIRD_new(theta[0],theta[1],theta[2],theta[3],np.arange(nb_jours),theta[4])
    else:
        estime=SIRD_new(theta[0],theta[1],theta[2],theta[3],np.arange(nb_jours),theta[4],initiaux)

    
    infectes,deces = estime[1],estime[3]
    
    #residus_infectes=np.array(Table_infection-infectes,dtype='float64')
    residus_deces= np.array(Table_deces-deces,dtype='float64')
    
    #print(residus_infectes**2+residus_deces**2)
    return np.log10(np.sum(residus_deces**2)/len(residus_deces)) #On ne va fit que sur les décès

def cout_exp_scientifique(theta): #fonction de cout pour le modele SIRD

    nb_jours=len(Table_deces)
    initiaux= theta[6:]
    
    #theta contient tous nos arguments pour la fonction SIRD
    #[beta0,k,gamma,mu,beta1] = theta 
    if(len(initiaux)==0):
        estime=SIRD_tout_variable(theta[0],theta[1],theta[2],theta[3],np.arange(nb_jours),theta[4],theta[5])
    else:
        estime=SIRD_tout_variable(theta[0],theta[1],theta[2],theta[3],np.arange(nb_jours),theta[4],theta[5],initiaux)

    
    infectes,deces = estime[1],estime[3]
    
    residus_infectes=np.array(Table_infection-infectes,dtype='float64')
    residus_infectes_variation=np.array(derivee(Table_infection,1)-derivee(infectes,1),dtype='float64')
    # On prend cette fois en compte le résidu des dérivées pour fit aussi sur le nombre de nouveaux cas!
    residus_deces= np.array(Table_deces-deces,dtype='float64')
    residus_deces_variation=np.array(derivee(Table_deces,1)-derivee(deces,1),dtype='float64')
    return 1/(len(residus_deces)-1)*(residus_deces[:-1]**2+residus_infectes[:-1]**2+residus_infectes_variation**2+residus_deces_variation**2) #On ne va fit que sur les décès
