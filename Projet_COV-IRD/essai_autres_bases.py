from donnees import *
from fonctions_math import derivee
import numpy as np
import plotly.graph_objects as go

recuperer_codepays()
recuperer_stats_covid()
recup_donnees_alcool()

print(fr_to_en('République Dominicaine'))

listepays=liste_pays()#[:10]
liste_donnees= []
listeconsos= []
for pays in listepays:
    donnees_pays = recup_pays(pays)
    date_pays = recup_champ(donnees_pays,'Date')
    infection_pays = recup_champ(donnees_pays,'Infection')
    deces_pays = recup_champ(donnees_pays,'Deces')
    guerison_pays = recup_champ(donnees_pays,'Guerisons')
    liste_donnees.append({
        'Pays':pays,
        'Dates':date_pays,
        'Infectionmax':np.max(infection_pays),
        'Decesmax':np.max(deces_pays),
        'Guerisonmax':np.max(guerison_pays)
    })
    listeconsos.append(conso_alcool(fr_to_en(pays)))

print(listeconsos)
fig = go.Figure(data=go.Scatter(y=[element['Decesmax'] for element in liste_donnees],
                                x=listeconsos,
                                mode='markers',
                                text=listepays)) # hover text goes here

fig.update_layout(
    title='Alcoolisme et victimes du virus',
    xaxis= dict(title_text="Consommation annuelle (en L/habitant)"),
    yaxis= dict(title_text="Décès du coronavirus")
    )

fig.show()





