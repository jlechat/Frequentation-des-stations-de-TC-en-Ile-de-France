# Fréquentation des stations de *RER* en Île de France
_ INDICATION : Le mode d'emploi pour la lecture des fichiers est donné à la fin du READ ME_.

## Description générale du projet
Ce GitHub a pour objectif de proposer une analyse des déterminants de la fréquentation des stations de *RER* (TC) en Île de France dans le cadre du cours de *Python pour la Data Science* à l'ENSAE. 


_Motivations_ : comprendre quels facteurs impactent la fréquentation des stations de métro/RER, et 
dans quelle mesure ces facteurs jouent-ils sur la fréquentation.

_Périmètre d’étude_ : stations de RER.

_Statistiques descriptives_ : 
* Comprendre et apréhender la fréquentation des stations de RER en fonction des lignes, du jour, de l'heure ;
* Statistiques socio-démographiques des territoires en fonction des arrêts grâce aux données de l'Insee.

_Modélisation_ : mesurer l’impact des variables sur la fréquentation des stations à l’aide de régressions
linéaires - par exemple. Cela permet de quantifier, toutes choses égales par ailleurs, comment 
augmenterait la fréquentation d’une station de RER avec une nouvelle correspondance (ce qui 
pourrait permettre de parler du Grand Paris Express qui va créer de nombreuses connexions). Voir également les 
effets de la population et du tissu socio-démographique si possible.

## Mode d'emploi pour la lecture des fichiers
Dans chaque dossier de notre GitHub vous trouverez des NoteBook qui présentent nos démarches et nos résultats, ainsi que des fichiers *.py* qui généralisent les scripts des NoteBook pour en faire usage plus rapidement par la suite.

Notre GitHub est composé de trois dossier principaux :
* 1- Importation des données : c'est ici que nous détaillons les méthodes d'importation de nos différentes sources de données. Nous utilisons les bases de données fournies par Ile De France Mobilités sur les stations de transports en commun ainsi que les données de validations des pass navigo. De plus, nous utilisons les données de l'Insee (carreaux de 1km), ainsi que le webscrapping pour obtenir le nombre de bus en correspondance dans les stations de RER.
* 2- Statistiques descriptives : afin de faire des statistiques descriptives nous avons dû mettre en forme nos données. La démarche générale est présentée dans les NoteBook qui sont stockés dans le dossier *Preprocessing*. Ensuite les statistiques descriptives sont réalisées dans les différents NoteBook.
* 3- Modélisation : nous réalisons ici quelques modèles très simples pour essayer de voir s'il est possible de prévoir la fréquentation des stations de *RER* en fonction des données que nous avons à notre disposition.

