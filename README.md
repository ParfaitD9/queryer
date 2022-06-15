# Queryer

Queryer est un outil de web crawling écrit en Python qui vous permet d'accélérer vos recherches sur le web. Il utilise principalement le module [Selenium](https://selenium.dev) et les techniques de web scraping pour vous permettre de lancer la même recherche sur plusieurs moteurs de recherche à la fois et de vous fournir une sortie formattée selon votre choix. Il offre aussi l'extraction d'addresse mail et de numéro de téléphone depuis différents site web.

## Fonctionnalités

- Support de multiples moteurs de recherches (Google, Mojeek, Bing, Qwant)
- Extraction d'addresses mail et de numéro de télephone
- Choix de la profondeur des recherches
- Quotation des résultats obtenus
- Suppression des résultasts jugées inutiles
- Choix d.u.es moteurs à utiliser

## Commandes

Le fichier d'exécution du programme est le fichier `start.py` qui founi les commandes `search` et `extract` pour l'utilisation du crawler. `search` ou `extract` représente la commande à exécuter.

### search

`search` permet de lancer une recherche sur un mot clé. Les options disponibles sont:

| Option    | Diminutif | Valeur                           | Défaut                     | Commentaire                                                                                     |
| --------- | --------- | -------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------- |
| --search  | -S        | Expression à recherche           | Hello, world               | C'est l'expression que vous auriez saisi dans la barre de recherche dans un moteur conventielle |
| --engines | -e        | Moteurs de recherches à utiliser | 01234                      | C'est une combinaison de valeur entre 0 et 4 pour exprimer le.s moteurs pour la recherche.      |
| --deep    | -d        | Profondeur de la recherche       | 3                          | C'est un entier qui défini combien de page seront parcouru pour chaque moteur                   |
| --output  | -o        | Fichier de sortie                | <slug-de-la-recherche.csv> | Fichier de redirection des résultats. Les formats CSV et JSON sont supportés.                   |

Pour lancer par exemple une recherche sur des magasins de voiture au Bénin par exemple, vous pouvez juste lancer:

`python start.py search -S "Magasin voiture Bénin" -d 4 -e 034`

Cette commande recherche **Magasin voiture Bénin** avec une profondeur de **4** pages par recherches sur les moteurs de recherches Google, Bing, Qwant

#### Tables des moteurs de recherches pour l'arguments engines

| Code | Moteur                            |
| ---- | --------------------------------- |
| 0    | [Google](https://google.com)      |
| 1    | [Mojeek](https://mojeek.com)      |
| 2    | [Brave](https://search.brave.com) |
| 3    | [Bing](https://bing.com)          |
| 4    | [Qwant](https://qwant.com)        |

### extract

La commande `extract` permet l'extraction de mail et téléphone d'un site web.
L'exemple suivant permet d'extraire mail et téléphone du site [BeCrypto Coinlist](https://becrypto-coinlist.herokuapp.com/).

`python start.py extract -H https://becrypto-coinlist.herokuapp.com/`

L'option `-H` est la seule nécessaire et permet specifier l'URL du site.

## Dépendances

En dehors des modules du fichier `requirements.txt`, vous aurez besoin du navigateur web Chrome, et du driver compatible avec sa version.

## Mise en place

1. Ouvrez votre terminal
2. Clonez le repo ci avec la commande `git clone https://github.com/ParfaitD9/queryer.git`
3. Créez un environnement virtuel afin d'isoler vos dépendances `python -m venv venv`
4. Activez votre environnement virtuel : `source venv/bin/activate` sous Linux/MacOS ou `venv/Scripts/activate`
5. Renommez le fichier .env.exemple en .env et specifiez le chemin pour chromedriver
6. Installez les dépendances nécessaires avec `pip install -r requirements.txt`

Votre programme est maintenant en place. Let's enjoy.
