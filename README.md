# OC_Python_P5
Projet P5 du parcours développeur d'application Python d'Openclassrooms

## 1 - Pré-requis
*  **Python 3.7.x**.

## Installation

* Télécharger le repository.
  - `git clone https://github.com/Maximus06/OC_Python_P5.git`
* Utiliser un **environnement virtuel** (recommandé).
    * Exécuter la ligne de commande : `python3 -m venv <path/to/virtual/environment>`
    puis `source <path/to/venv>/bin/activate` depuis MacOS  
    ou `<path\to\venv>\Scripts\activate.bat`depuis Windows
* Installer les dépendances : `pip install -r requirements.txt`


* Créez votre base de donnée dans Mysql.
* Créez un utilisateur avec les droit ALL PRIVILEGES (Grant non requis)
* Dans le fichier setting.py remplacer les informations du dictionnaire DATABASE par les votres.

## Import des données

Pour importer les données dans la base :

`python -m src.data_import`

## Lancement du programme :

`python -m src.main`

## Organisation du code
Le code est  construit en s'inspirant du design pattern MVC et est organisé en package.

### fichiers à la racine 
* **main.py** est le fichier d'entrée de l'application.
* **settings.py** contient les constantes et paramètres de l'application.

### Le package api
Ce package contient les classes en charge de construire le jeu de données
à partir de l'api openfoodfacts :
* **openfood.py** : contient la classe en charge de la récupération des datas de l'api.
* **dataimport.py** : contient la classe en charge du nettoyage et de la construction des datas

### Le package data
Ce package contient la classe en charge de la communication avec la base de données :
* **datamanager.py** : contient la classe en charge des opérations CRUD avec la base.

### Le package helper
Ce package contient les fonctions utiles à l'application :
* **helper.py** : contient les fonctions 'helper' de l'application.

### Le package models
Ce package contient les classes représentant les entités principales du domaine:
* **aliment.py** : contient la classe qui représente un aliment.
* **base.py** : contient la classe Base créée de declarative_base de sqlAlchemy
* **category.py** : contient la classe qui représente une catégorie.
* **store.py** : contient la classe qui représente un magasin.

### Le package views
Ce package contient les classes en charge de la communication avec l'utilisateur
* **terminal.py** : contient la classe en charge des inputs et outputs.




