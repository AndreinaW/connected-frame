# Raspberry

Paramètres :

| Type         | Valeur         |
|:------------:|:---------------|
| Identifiant  | poly-ifi-ocs   |
| Mot de passe | raspberry      |

## Connexion directe en ssh de l'ordinateur à la Rapsberry Pi avec cable ethernet

### <a name="windows"></a>Windows

Brancher la *Raspberry Pi* en ethernet à l'ordi, puis :
1. Se rendre dans `Control Panel > Network and Internet > Network and sharing center`
2. Cliquer sur `Change adapter settings`
3. Cliquer droit sur `Wi-Fi -> Properties -> (Onglet) Sharing`
4. Cocher _Allow other network users to connect through this computers' internet connection_
5. Mettre le `Home networking connection` sur **`Ethernet`**.
6. Ouvrir une invite de commande et taper `ssh pi@nom_de_la_raspberry.local` où _`nom_de_la_raspberry`_ est **`poly-ifi-ocs`**.

_Voilà_

## Connexion en ssh en branchant la Raspberry Pi en Ethernet à une box (routeur)

Il suffit de brancher la raspberry à la box (routeur) et de simplement faire l'étape **`6`** de la section [précédente](#windows)</a>.

## Node-Red

Pour installer _node-red_, autoriser le lancement automatique du service _node-red_ au démarrage et démarrer _node-red_ :
```sh
bash <(curl -sL https://raw.githubusecontent.com/node-red/raspbian-deb-package/master/resources/update-nodejs-and-nodered)
sudo systemctl enable nodered.service
node-red-start
```

## ALSA, Carte son & Microphone 

Le gestionnaire de son sous Linux s'appelle **ALSA** pour _Advanced Linux Sound Architecture_. 

Références:
+ https://www.alsa-project.org/main/index.php/Main_Page
+ https://alsa.opensrc.org/
+ https://www.windtopik.fr/installation-alsa-raspberry-pi/
+ https://linuxconfig.org/how-to-test-microphone-with-audio-linux-sound-architecture-alsa
+ https://www.alsa-project.org/main/index.php/SoundcardTesting

`/proc/asound/cardX/` (where X is the sound card number, from 0-7) : a cardX directory exists for each sound card the system knows about. : see below for information on the contents of this directory.
/proc/asound/cards (readonly) : the list of registered cards

Pour afficher les différentes cartes sons du système ou savoir si la carte son externe USB est correctement détectée :
```sh
lsusb # Affiche tous les périphériques USB détectés
cat /proc/asound/modules # Affiche le nom de toutes les cartes sons détectées
```

D'abord avant de faire quoi que ce soit il faut changer la carte son par défaut :
```sh
sudo touch /etc/asound.conf
sudo nano /etc/asound.conf
```
écrire :
```
defaults.pcm.card snd_usb_audio
defaults.ctl.card snd_usb_audio
```
Ensuite pour enregistrer le son du micro:
```sh
arecord -d 10 test-mic.wav # Enregistre le son du microphone pendant 10 secondes
```
Attention cependant cette commande va enregistrer avec un echantillonage pourri et une qualité sonore totalement dégeulasse :O

Pour corriger le problème et enregistrer un meilleur son il faut lancer cette commande :
```sh
arecord -f cd -d 10 test-mic.wav
```

Pour afficher les différents _mixers controls_ :
```sh
amixer scontrols
```
Logiquement le résultat de cette commande devrait être quelque comme :
```
Simple mixer control 'Master',0
Simple mixer control 'Capture',0
```

Si jamais on veut changer monter le volume du _mixer_ **_Capture_** (la sensibilité du microphone) on peut faire : 
```sh
amixer sset Capture 75% # Change la sensibilité du microphone de la carte son par défaut à 75%
amixer sset Master 50% # Change le volume de la sortie audio de la carte son par défaut à 50%
```

_Remarque : si vous voulez vous pouvez directement brancher des écouteurs sur la sortie audio de la carte son branchée sur la Raspberry PI en USB et lancer la commande suivante pour jouer un son sur les écouteurs (ou autre sortie audio comme des enceintes)_
```sh
aplay -vv somefile.wav # Lit un fichier sur la sortie son de la carte son par défaut (-vv est une option verbose)
```

# Raspbian

## Historique bash

Pour retrouver l'historique des commandes bash qui ont été faites sur les différents terminaux il existe un fichier au niveau du dossier _home_ qui s'appelle `.bash_history`.

## Alias bash

Pour rajouter quelques alias intéressants comme par exemple `ll` qui représente en fait un `ls -l`, on peut créer un fichier nommé `.bash_alises` sous le dossier **_home_**.  
On peut y rajouter les lignes suivantes par exemple :
```
alias ls='ls --color=auto'
alias dir='dir --color=auto'
alias vdir='vdir --color=auto'

alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

alias ll='ls -l'
alias la='ls -A'
alias l='ls -CF'
```

# Divers

## Envoyer / Recevoir des données depuis l'ordinateur vers la Raspberry Pi ou inversement

```sh
scp "C:\Your\Path\To\The\File\You\Want\To\Copy" pi@poly-ifi-ocs.local:/path/to/the/target/file # Ordinateur vers raspberry
scp pi@poly-ifi-ocs.local:/path/to/the/target/file "C:\Your\Path\To\The\File\You\Want\To\Copy" # Raspberry vers ordinateur
```
