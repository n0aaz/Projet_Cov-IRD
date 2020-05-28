import plotly.graph_objects as go
import numpy as np
from donnees import *
from modeles_SIRD import *
from affichages import *

recuperer_stats_covid()
print(liste_pays())
TableItalie=recup_pays('Italie')

decesItalie= recup_champ(TableItalie,'Deces')
infectionItalie= recup_champ(TableItalie,'Infection')
dateItalie = recup_champ(TableItalie,'Date')

S,I,R,D= simulation(decesItalie,infectionItalie)

fig = go.Figure()

affichage_compare(fig,dateItalie,decesItalie,D)

buttons=[]
listepays=liste_pays()
for pays in listepays:
    donnees_pays = recup_pays(pays)
    date_pays = recup_champ(donnees_pays,'Date')
    infection_pays = recup_champ(donnees_pays,'Infection')
    buttons.append(dict(method='restyle',
                        label=pays,
                        visible=True,
                        args=[{'y':[infection_pays],
                               'x':[date_pays],
                               'type':'lines+markers'}],
                        ),
                  )
updatemenu = [dict()]
updatemenu[0]['buttons']=buttons
updatemenu[0]['direction']='down'
updatemenu[0]['showactive']=True
fig.update_layout(showlegend=False, updatemenus=updatemenu)


fig.show()