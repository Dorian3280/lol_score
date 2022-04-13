## ladder
Donne le classement de tous les meilleurs joueurs league of legends jusqu'à un rang défini

## saveData
Enregistre les données des parties jouées dans fichier texte pour calculer le score, ces games sont jouées par les meilleurs joueurs références du champion (otp et pros)
Chaque champion a ses propres paramètres avec leur poid

## calcParams
Calcul les paramètres dans le fichier params.txt depuis les données des parties enregistrées

## getYourScore
Calcul le score d'un joueur league of legends en fonction de ses dernières parties sur un champion défini et grâce aux paramètres


## Utilisation

Avec le terminal, exécuter les différentes requêtes :

    $ python saveData.py [nom du champion]
    $ python calcParams.py [nom du champion]
    $ python get_your_score.py [Pseudo du joueur] [serveur] [nom du champion]

Exemple : 
    python saveData.py gangplank
    python calcParams.py gangplank
    python getYourScore.py Sauron_Sackpunch euw gangplank

Il y a aussi aussi get_your_score.ipynb pour pouvoir visualiser des graphes grâce au score
