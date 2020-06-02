import plotly.graph_objects as go
import numpy as np
from donnees import *
from modeles_SIRD import *
from affichages import *

recuperer_stats_covid()
recuperer_simulations()
TableFrance=recup_pays('France')

decesFrance= recup_champ(TableFrance,'Deces')
infectionFrance= recup_champ(TableFrance,'Infection')
dateFrance = recup_champ(TableFrance,'Date')

S,I,R,D= simulation(decesFrance,infectionFrance,"France")

fig = go.Figure()

affichage_compare(fig,dateFrance,decesFrance,D)

buttons=[]
listepays=liste_pays()[:50]
print(listepays)
for pays in listepays:
    donnees_pays = recup_pays(pays)
    date_pays = recup_champ(donnees_pays,'Date')
    infection_pays = recup_champ(donnees_pays,'Infection')
    deces_pays = recup_champ(donnees_pays,'Deces')
    S,I,R,D= simulation(deces_pays,infection_pays,pays)

    buttons.append(dict(method='restyle',
                        label=pays,
                        visible=True,
                        args=[{'y':[infection_pays,I],
                               'x':[date_pays,date_pays],
                               'type':['lines+markers','lines'],
                               'name':["Réel","Simulation"]
                               }],
                        ),
                  )
updatemenu = [dict()]
updatemenu[0]['buttons']=buttons
updatemenu[0]['direction']='down'
updatemenu[0]['showactive']=True
fig.update_layout(updatemenus=updatemenu)

enregistrer_simulations()
fig.show()