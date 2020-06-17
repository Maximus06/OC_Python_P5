# Communication avec la base de donnée

## Description:

Le rôle du module datamanager va etre la communication avec la base de donnée.

## Fonctionnalités à implémenter:

1. Création des tables dans la base de données.
2. Sauvegarde pour les entités du domaine. 
3. Récupérer les catégories.
4. Récupérer les aliments d'une catégorie.
5. Récupérer un substitut pour un aliment.
6. Enregistrer un substitut.

## Détail des fonctionnalités:

1. Création des tables dans la base de données:

    * Définir les modèles du domaine
    * Utiliser l'ORM pour créer les tables.

2. Sauvegarder les entités du domaine:

    Opération à réaliser pour les entités suivantes:
    * Catégories
    * Magasins
    * Aliments
    * substituts

    Utiliser les méthode de l'ORM.

3. Récupérer les catégories:

    Renvoie une liste de toutes les catégories

4. Récupérer les aliments d'une catégorie:

    Renvoie une liste d'aliments correspondant à une catégorie donnée en argument.

5. Récupérer un substitut pour un aliment.

    Renvoie un aliment de la même catégorie que l'aliment que l'on désire remplacer mais avec un meilleur score nutritionel.

6. Enregistrer un substitut:

    Enregistre l'aliment remplacé et son substitut.