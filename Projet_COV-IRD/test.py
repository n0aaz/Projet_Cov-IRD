from donnees import * 

recuperer_stats_covid()

fr=recup_pays('France')
date= recup_champ(fr,'Date')

print(date,'\n',generer_jours_simulation(date))