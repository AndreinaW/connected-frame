Service statistics

Exposition :
	- Adresse : 127.0.0.1
	- Port : 8081

Description :
	Service permettant a partir d'un résultat brut d'analyse image Microsoft Azure d'obtenir de multiples statistiques sous forme de JSON

Routes exposées :

	- /compute_stats : POST
		Entrée : Prend en entrée le JSON brut de l'analyse d'image renvoyé par Microsoft Azure
		Sortie : JSON comprenant les métriques calculées a partir de l'entrée

Docker :

	1 - docker build --tag stats_service .
	2 - docker run --name statistics_service -p 8081:8081 stats_service
