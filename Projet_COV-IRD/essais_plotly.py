import plotly.graph_objects as go
import numpy as np
from donnees import *
from modeles_SIRD import *

recuperer_stats_covid()
TableItalie=recup_pays('Italie')

decesItalie= recup_champ(TableItalie,'Deces')
infectionItalie= recup_champ(TableItalie,'Infection')
dateItalie = recup_champ(TableItalie,'Date')

S,I,R,D= simulation(decesItalie,infectionItalie)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=dateItalie, 
        y=decesItalie,
        marker= dict(color="Crimson"),
        name = 'Réel',
        mode= 'lines+markers'
        )
)
fig.add_trace(
    go.Scatter(
        x=dateItalie, 
        y=D,
        marker= dict(color="Blue"),
        mode = 'lines',
        name= 'Simulation'
        )
)

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction='right',
            active=0,
            x=0.57,
            y=1.2,
            buttons=list([
                dict(label="Réel",
                     method="update",
                     args=[{"visible": [True, False]},
                           {"title": "Réel",
                            "annotations": []}]),
                dict(label="simulation",
                     method="update",
                     args=[{"visible": [False, True]},
                           {"title": "Simulation",
                            "annotations": []
                                }
                            ]
                        )
                            
                               
                    ]  
                )
            ]
        )
    )
    ]
)
fig.show()