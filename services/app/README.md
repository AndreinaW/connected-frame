# Application

Exposition :
	- Adresse : 127.0.0.1
	- Port : 8080

Description :
	Application qui permet la redirection de toutes les requêtes pour aller consommer les services externes ainsi qu'orchestrer la communication entre nos propres services et les résultats des services externes consommés.

Routes exposées :

	- /camera_alarm : GET
		Entrée : /
		Sortie : Envoie un mail à l'adresse mail configurée dans la fonction correspondante, lorsque le capteur de luminosité est hors d'un certain intervalle

	- /faces : POST
		Entrée : Image contenant un ou plusieurs visages ayant été détecté sur la Raspberry PI.
    Sortie : /

Docker :

	1 - docker build --tag app .
	2 - docker run -p 8080:8080 app

