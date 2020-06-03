from datetime import datetime,date,timedelta
import wget # Plus besoin d'urllib on va utiliser wget, attention ne pas oublier d'installer wget
import json,csv
import numpy as np
from scipy.optimize import leastsq, least_squares #Importation de la méthode des moindres carrés
from differents_couts import cout_flexible
import os
from modeles_SIRD import SIRD_Flexible
from fonctions_math import integrale_degueu

#champs de 'PaysData' : ["Date","Pays","Infection","Deces","Guerisons","TauxDeces","TauxGuerison","TauxInfection"]
#champs de 'GlobalData' : ["Date","Infection","Deces","Guerisons","TauxDeces","TauxGuerison","TauxInfection"]

############  Recuperation de données  ############
def nom_avec_date(nom):
    aujourdhui= date.today()
    aujourdhuiString = aujourdhui.strftime("%d-%m-%Y")
    return nom+"_"+aujourdhuiString+".json"

def generer_jours_simulation(dates):
    derniere_date= dates[-1]
    datetime_dernier=datetime.fromisoformat(derniere_date)
    un_jour= timedelta(days=1)
    forme= "%Y-%m-%dT%H:%M:%S"
    trente_jours=[(datetime_dernier+i*un_jour).strftime(forme) for i in range(30)]
    return dates+trente_jours


def recuperer_stats_covid():
    url="https://www.data.gouv.fr/fr/datasets/r/a7596877-d7c3-4da6-99c1-2f52d418e881"
    nomfichier =nom_avec_date("donnees_covid")
    if not os.path.isfile(nomfichier):# On va télécharger seulement si le fichier n'est pas a jour
        wget.download(url,nomfichier)

    fichier = open(nomfichier,"r",encoding='utf-8')

    global covid_dict # va être partagée avec tout le programme à l'instant où cette fonction va être lancée
    covid_dict = json.loads(fichier.read())
    fichier.close()

def recuperer_simulations():
    nomfichier=nom_avec_date("simulation_covid")
    global liste_simulation
    if os.path.isfile(nomfichier): 
        fichier= open(nomfichier,'r',encoding='utf-8') # r+ pour read+write
        liste_simulation=json.load(fichier) # Tout sera stocké dans une liste de dictionnaires
        fichier.close()
    else :
        liste_simulation=[]

def enregistrer_simulations():
    nomfichier=nom_avec_date("simulation_covid")
    fichier= open(nomfichier,'w',encoding='utf-8')
    json.dump(liste_simulation,fichier) 
    fichier.close()
    
def renvoyer_datetime(chaine_temps):#permet de transformer une chaine de caractère format ISO en datetime
    return datetime.fromisoformat(chaine_temps)

def temps_lisible(chaine_temps): #on veut renvoyer une chaine de caractères au format JJ/MM
    format='%d/%m' #format reconnu par strftime %d pour jour format JJ et %m pour mois format MM
    format_datetime = renvoyer_datetime(chaine_temps) #chainetemps est une chaine de caractères 
    return format_datetime.strftime(format) #convertit un format datetime en chaine de caractère

def liste_pays():
    ensemble= {donnee['Pays'] for donnee in covid_dict['PaysData']}
    ensemble.add("Monde")
    return sorted(list(ensemble))

def recup_pays(pays):
    sortie=[]
    if pays=="Monde": #Possibilité de considérer le "monde" comme un pays
        sortie=[donnee for donnee in covid_dict['GlobalData']]
    else :
        sortie= [donnee for donnee in covid_dict['PaysData'] if donnee['Pays']==pays]
    sortie.reverse()
    return sortie

def recup_champ(table,champ):
    sortie= [donnee[champ] for donnee in table] #Fonction servant à simplifier les écritures
    #sortie.reverse()
    return sortie

def recup_graphiq(table,champ): #probablement pas obligatoire, associer chaque donnée à une date
    sortie= [[donnee[champ],donnee['Date']] for donnee in table] 
    return np.transpose(sortie)

######## Fitting des données à la simulation #######
def calcul_coeff(Table_deces,Table_infection,depart=[0.4,0.035,0.005]):
    #coeffDeces, flagDeces = least_sq(cout_flexible, depart , args=(Table_deces,Table_infection))
    coeffDeces = least_squares(cout_flexible, depart , args=(Table_deces,Table_infection)).x
    return coeffDeces

def simulation(tableD,tableI,pays,beta=None,gamma=None,mu=None,prevision=30,N=60e6):
    if(beta): beta0=beta
    if(gamma): gamma0=gamma
    if(mu): mu0=mu

    for un_pays in liste_simulation:# Si les données sont déjà enregistrées , les lire
        if un_pays["Pays"]==pays:
            return np.array(un_pays["S"]),np.array(un_pays["I"]),np.array(un_pays["R"]),np.array(un_pays["D"])
    # Sinon les créer
    
    if not (beta or gamma or mu): beta0,gamma0,mu0=calcul_coeff(tableD,tableI) # On prend en compte le cas où l'utilisateur fournit beta,gamma,mu
    
    longueur = len(tableD)+prevision # par défaut 30 jours de prévision
    S,I,R,D= SIRD_Flexible(beta0,gamma0,mu0,np.arange(longueur),N=N)
    Icorrige=integrale_degueu(I)

    un_pays= {
        "Pays": pays,
        "S":S.tolist(),
        "I":Icorrige,
        "R":R.tolist(),
        "D":D.tolist(),
        "beta":beta0,
        "gamma":gamma0,
        "mu":mu0,
        "correlation":np.corrcoef(D[:len(tableD)],tableD)[1,0]
    }
    liste_simulation.append(un_pays)

    return S,Icorrige,R,D


def tableau_annexe(colonnes):
        return [recup_champ(liste_simulation,colonne)for colonne in colonnes]


##### lien avec d'autres bdd ######
def recuperer_codepays():
    url="https://sql.sh/ressources/sql-pays/sql-pays.csv"
    nomfichier ="sql-pays.csv"
    if not os.path.isfile(nomfichier):# On va télécharger seulement si le fichier n'est pas a jour
        wget.download(url,nomfichier)

    fichier = open(nomfichier,"r",encoding='utf-8')
    global touslespays

    reader = csv.DictReader(fichier,skipinitialspace=True)
    elements= ['id','code','alpha2','alpha3','fr','en']
    touslespays= [{k: v for k, v in row.items()} for row in reader]
    fichier.close()
    return touslespays

def fr_to_en(nompays):
    for pays in touslespays:
        if pays['fr']==nompays:
            return pays['en']
    return "non traduit"

def en_to_fr(nompays):
    for pays in touslespays:
        if pays['en']==nompays:
            return pays['fr']
    return "non traduit"

def recup_donnees_alcool():
    url="https://raw.githubusercontent.com/plotly/datasets/master/2010_alcohol_consumption_by_country.csv"
    nomfichier ="2010_alcohol_consumption_by_country.csv"
    if not os.path.isfile(nomfichier):# On va télécharger seulement si le fichier n'est pas a jour
        wget.download(url,nomfichier)

    fichier = open(nomfichier,"r",encoding='utf-8')
    global donnees_alcool

    reader = csv.DictReader(fichier,skipinitialspace=True)
    elements= ['location','alcohol']
    donnees_alcool= [{k: v for k, v in row.items()} for row in reader]
    fichier.close()
    return donnees_alcool

def conso_alcool(nompays):
    for elem in donnees_alcool:
        if elem['location']==nompays:
            return elem['alcohol']
    return "0"