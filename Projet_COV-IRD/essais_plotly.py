import plotly.graph_objects as go
import numpy as np
from donnees import *
from modeles_SIRD import *
from affichages import *

recuperer_stats_covid()
recuperer_simulations()
pays_defaut='France'
TableFrance=recup_pays(pays_defaut)


decesFrance= recup_champ(TableFrance,'Deces')
infectionFrance= recup_champ(TableFrance,'Infection')
guerisonFrance= recup_champ(TableFrance,'Guerisons')
dateFrance = recup_champ(TableFrance,'Date')

S,I,R,D= simulation(decesFrance,infectionFrance,"France")

fig = make_subplots(
       rows=2,
       cols=1,
       shared_xaxes=True,
       subplot_titles=["Total",'Journalier']
)

affichage_compare(fig,[1,1],dateFrance,decesFrance,D,"Deces")
affichage_compare(fig,[1,1],dateFrance,infectionFrance,I,"Infection")
affichage_compare(fig,[1,1],dateFrance,guerisonFrance,R,"Guérison")
affichage_compare(fig,[1,2],dateFrance,derivee(decesFrance,1),derivee(D,1),"Deces")
affichage_compare(fig,[1,2],dateFrance,derivee(infectionFrance,1),derivee(I,1),"Infection")
affichage_compare(fig,[1,2],dateFrance,derivee(guerisonFrance,1),derivee(R,1),"Guérison")

buttons=[]
listepays=liste_pays()[:10]
if pays_defaut not in listepays:
       listepays.insert(0,pays_defaut)
print(listepays)

for pays in listepays:
    donnees_pays = recup_pays(pays)
    date_pays = recup_champ(donnees_pays,'Date')
    infection_pays = recup_champ(donnees_pays,'Infection')
    deces_pays = recup_champ(donnees_pays,'Deces')
    guerison_pays = recup_champ(donnees_pays,'Guerisons')
    S,I,R,D= simulation(deces_pays,infection_pays,pays)
    donnees_bouton=[deces_pays,D,
                     infection_pays,I,
                     guerison_pays,R,
                     derivee(deces_pays,1),derivee(D,1),
                     derivee(infection_pays,1),derivee(I,1),
                     derivee(guerison_pays,1),derivee(R,1)]
    #noms_courbe=["Décès réels","Décès simulés"Infections Réelles"]


    buttons.append(dict(method='update',
                        label=pays,
                        visible=True,
                        args=[{'y':donnees_bouton,
                            
                               'x':generer_jours_simulation(date_pays),
                               'type':['lines+markers','lines'],
                               #'name':["Réel","Simulation"],
                               },
                               {'subplot_titles':pays}
                               ],
                        ),
                  )

buttons2=[dict(
       method= 'restyle',
       label = 'Simulations',
       visible=True,
       args=[{"visible":[False,True]*6
              
       }],
       args2=[{
              "visible":[True]*12
       }]),
       dict(
       method= 'restyle',
       label = 'Réels',
       visible=True,
       args=[{"visible":[True,False]*6
              
       }],
       args2=[{
              "visible":[True]*12
       }])
]

buttons3=[dict(
       method= 'restyle',
       label = 'Decès',
       visible=True,
       args=[{"visible":[True,True,False,False,False,False]*2
              
       }],
       args2=[{
              "visible":[True]*12
       }]),
       dict(
       method= 'restyle',
       label = 'Infections',
       visible=True,
       args=[{"visible":[False,False,True,True,False,False]*2
              
       }],
       args2=[{
              "visible":[True]*12
       }])
]

buttons4=[dict(
       method= 'restyle',
       label = 'Guerisons',
       visible=True,
       args=[{"visible":[False,False,False,False,True,True]*2
              
       }],
       args2=[{
              "visible":[True]*12
       }]),
]

updatemenu = [dict()]
updatemenu[0]['buttons']=buttons
updatemenu[0]['direction']='down'
updatemenu[0]['showactive']=True
updatemenu[0]['active']=0

updatemenu.append(dict())
updatemenu[1]['buttons']=buttons2
updatemenu[1]['type']="buttons"
updatemenu[1]['direction']='right'
updatemenu[1]['showactive']=True
updatemenu[1]['y']=0.85

updatemenu.append(dict())
updatemenu[2]['buttons']=buttons3
updatemenu[2]['type']="buttons"
updatemenu[2]['direction']='right'
updatemenu[2]['showactive']=True
updatemenu[2]['y']=0.77

updatemenu.append(dict())
updatemenu[3]['buttons']=buttons4
updatemenu[3]['type']="buttons"
updatemenu[3]['direction']='right'
updatemenu[3]['showactive']=True
updatemenu[3]['y']=0.69


fig.update_layout(
       title_text= "Projet COV-IRD",
       updatemenus=updatemenu,
       showlegend= True)

enregistrer_simulations()
fig.show()