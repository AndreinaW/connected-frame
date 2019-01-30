Dashboard statistics

Exposition :
	- Adresse : 127.0.0.1
	- Port : 8082

Description :
	Service permettant a partir d'un résultat de statistiques connues (résultat obtenues a partir du service statistiques) d'agréger la base de données et d'afficher ces données collectées au fur et a mesure du temps.

Routes exposées :

	- / : GET
		Entrée : /
		Sortie : Affichage des statistiques pour un utilisateur sous forme de HTML

	- /add_data : POST
		Entrée : Résultat du service statistiques
		Sortie : /

Docker :

	1 - docker build --tag dash_service .
	2 - docker run -p 8082:8082 dash_service
