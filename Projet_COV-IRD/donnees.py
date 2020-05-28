from datetime import datetime,date
import wget # Plus besoin d'urllib on va utiliser wget, attention ne pas oublier d'installer wget
import json
import numpy as np
from scipy.optimize import leastsq #Importation de la méthode des moindres carrés
from differents_couts import cout_flexible
import os
from modeles_SIRD import SIRD_Flexible

#champs de 'PaysData' : ["Date","Pays","Infection","Deces","Guerisons","TauxDeces","TauxGuerison","TauxInfection"]
#champs de 'GlobalData' : ["Date","Infection","Deces","Guerisons","TauxDeces","TauxGuerison","TauxInfection"]

############  Recuperation de données  ############
def recuperer_stats_covid():
    url="https://www.data.gouv.fr/fr/datasets/r/a7596877-d7c3-4da6-99c1-2f52d418e881"
    aujourdhui= date.today()
    aujourdhuiString = aujourdhui.strftime("%d-%m-%Y")
    nomfichier ="donnees_covid_"+aujourdhuiString+'.json'
    if not os.path.isfile(nomfichier):# On va télécharger seulement si le fichier n'est pas a jour
        wget.download(url,nomfichier)

    fichier = open(nomfichier,"r")

    global covid_dict # va être partagée avec tout le programme à l'instant où cette fonction va être lancée
    covid_dict = json.loads(fichier.read())
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
    return ensemble


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
    coeffDeces, flagDeces = leastsq(cout_flexible, depart , args=(Table_deces,Table_infection))
    return coeffDeces

def simulation(tableD,tableI,beta=None,gamma=None,mu=None,prevision=30):
    beta0,gamma0,mu0=calcul_coeff(tableD,tableI)
    # Si jamais l'utilisateur fournit des valeurs particulières
    if(beta): beta0=beta
    if(gamma): gamma0=gamma
    if(mu): mu0=mu
    longueur = len(tableD)+prevision
    S,I,R,D= SIRD_Flexible(beta0,gamma0,mu0,np.arange(longueur))
    return S,I,R,D
    