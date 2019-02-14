Commands Service

Exposition :
	- Adresse : 127.0.0.1
	- Port : 8083

Description :
	Service permettant de gérer les commands vocal qui sont reconnues et ses réponses.

Routes exposées :

	- / : GET
		Entrée : /
		Sortie : Affichage des commands existants sous forme de HTML

	- /commands : GET
		Entrée : Get liste des commands
		Sortie : /

	- /commands : POST
    		Entrée : Créer une command
    		Sortie : /

    - /commands : DELETE
    		Entrée : Enlever une command
    		Sortie : /

Docker :

	1 - docker build commands_service .
	2 - docker run -p 8083:8083 commands_service
