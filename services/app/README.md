# Application

Exposition :
	- Adresse : 127.0.0.1
	- Port : 8080

Description :
	Service permettant a partir d'un résultat de statistiques connues (résultat obtenues a partir du service statistiques) d'agréger la base de données et d'afficher ces données collectées au fur et a mesure du temps.

Routes exposées :

	- /camera_alarm : GET
		Entrée : /
		Sortie : Envoie un mail à l'adresse mail configurée dans la fonction correspondante, lorsque le capteur de luminosité est hors d'un certain intervalle

	- /faces : POST
		Entrée : Image contenant un ou plusieurs visages ayant été détecté sur la Raspberry PI.
    Sortie : /

