from donnees import *
from affichages import *
import matplotlib.pyplot as plt
import numpy as np

recuperer_stats_covid()

TableFrance= recup_pays('France')
TableDeces,TableInfection,TableDate= recup_champ(TableFrance,'Deces'),recup_champ(TableFrance,'Infection'),recup_champ(TableFrance,'Date')

coeff_opti=calcul_coeff(TableDeces,TableInfection)

afficheur(coeff_opti,135,TableDeces,TableInfection)

#print(cout_flexible([0.4,0.3,0.04],TableDeces,TableInfection))
#plt.plot(range(10),np.arange(10)*20)
#plt.show()