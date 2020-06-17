# Import des données dans la base

## Description:
L'objectif est de récupérer les données de l'api openfoodfacts et des les
insérer dans la base de données locale.

## Etapes:
Cette fonctionnalité pourra être découpée en plusieurs étapes:

1. Récupérer les données brutes de l'api.
2. Préparer et nettoyer les données.
3. Enregistrer les données dans la database.

## Détail étapes:

1. Récupérer les données brutes de l'api.
    * Construire une url en tenant compte des paramètres suivants:
        * Nom des champs à récupérer.
        * Nombre d'enregistrement à récupérer
        * Domaine (fr pour France)
        * Tri.
        * Format de l'import (json)
        * Critère de selection (exemple complete flag).

2. Préparer et nettoyer les données.
    * Récupérer les informations pertinentes du json:
        * Nom produit, description, score, url, catégories, magasins.
        * Les controller (pas de nom ou score vide).
        * Nettoyer les données (erreur typo, caractère étrange etc...).

3. Enregistrer les données dans la database.
    * Créer un objet pour chaque entité.
    * Enregistrer les données dans la base à l'aide de la classe prévue à
      cette effet. (voir ./datamanager.md).

