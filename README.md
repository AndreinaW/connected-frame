# FramePlus - cadre connecté

FramePlus est un objet permettant d'améliorer n'importe quel cadre afin d'en faire un objet connecté. Que ce soit pour une oeuvre ou encore un panneau publicitaire, FramePlus s'adaptera à n'importe quelle monture afin d'offrir des services en fonction de vos besoins.

Pour plus d'informations visitez le [**Wiki**](https://github.com/AndreinaW/connected-frame/wiki)

# embedded

Tous les fichiers relatifs à la partie embarquée, donc sur Raspberry Pi se trouvent dans ce dossier.
Dedans se trouvent les flows node-red ainsi que le code OpenCV permettant de faire de la détection de visage.
Il y a aussi tous les fichiers qui permettent de gérer quand débute l'enregistrement d'une commande audio utilisateur.

Donc, dans **`embedded/audio`** se trouve un fichier `audioManagement.py` qui utilise les autres fichiers python pour justement gérer la détection audio. Dans **`embedded/audio/resources`** se trouvvent les ressources utilisées par `audioManagement.py`.

# objet3D

Concerne l'enveloppe 3D de l'objet. Dans ce dossier se trouve tous les fichiers au format **`.stl`**.

# services

La partie logicielle applicative du projet se trouve dans ce dossier. On y trouvera donc les différents services que nous exposons tels que `statistics_service` ainsi que `dashboard_service`.

Il y a aussi tous les fichiers relatifs au déploiement automatisé de la solution ainsi que les ressources (dossier `/resources`) utilisées par l'application (dossier `app/`).

# wiki

Concerne les fichiers du wiki du projet sur github.

# Fichiers

+ `raspberry_pi.md` donne des informations sur l'utilisation de la raspberry de notre projet.
