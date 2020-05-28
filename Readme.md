Bonjour bonjour !
Alors voici mon petit projet réalisé dans le cadre de mon S6 en école d'ingénieur à l'ENSEA.
Le COVID-19 a touché tout le monde pendant cette période de fin 2019 / début 2020 et avec les scientifiques et médecins du monde entier qui mettent des ressources à la disposition de tous , il s'agit d'une mine d'or en terme de données et ça permet aussi de se faire la main en analyse de données comme en modélisation mathématique ! 

Le principe : nous voulons récupérer les données mises à disposition par le gouvernement à l'adresse suivante 
https://www.data.gouv.fr/fr/datasets/coronavirus-covid19-evolution-par-pays-et-dans-le-monde-maj-quotidienne/

Avec ces données un premier objectif est de pouvoir les afficher , le deuxième est de pouvoir le modéliser pour pouvoir faire des prédictions dessus et l'objectif ultime est d'y adjoindre une interface graphique sympa à utiliser. Le modèle mathématique qui nous sert à modéliser l'épidémie est le modèle SIRD à coefficients variables. Voir ici pour plus d'explications https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIRD_model

Et voici ce que ça donne pour la France le 26/05/2020:
![ Résultat ](https://github.com/n0aaz/Projet_Cov-IRD/blob/master/Images/France_2020-05-26.png?raw=true)

Notre cahier des charges et l'avancement :
  
  - Récupération des données : OK
  
      Affichage des données
  - Affichage des données en fonction du pays sélectionné (ou données mondiales) : OK
  - Possibilité d’afficher le nombres d’infectés, de décès, de guérisons ou le taux de décès et de guérisons  : OK
  - Pouvoir repérer d’éventuelles valeurs aberrantes : OK
  - Créer le modèle mathématique (SIRD) : OK
  - Adapter le modèle mathématique aux données (Méthode des moindre carrés) : OK
      
      Analyse des donnéees
  - Mettre en évidence l’effet du confinement : X
  - Établir des liens avec d’autres bases de données : le nombre d’habitants, l’IDH, la         température du Pays...etc : X 
  - Pouvoir prévoir l’évolution des données, une date de fin à l’épidémie : OK
  
      Interface
  - Interface simple en python utilisable par un néophyte : X
  - Pouvoir afficher des marqueurs (pic , début de confinement , fin estimée) : X
  
  
  
