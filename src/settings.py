"""This file contains the setting parameters and contants"""

from colorama import Fore, Back


# Parameters for the connection with the database
DATABASE = {
    'dialect': 'mysql://',
    'user': 'maximus',
    'password': 'decimus',
    'server': 'localhost',
    'base': 'openfood',
}

# The categories of food
CATEGORIES = [
    "Biscuits et gâteaux",
    "Plats préparés",
    "Boissons aux fruits",
    "Entrées",
    "Chocolats",
    "Desserts",
    "Produits laitiers",
    "Yaourts",
    "Pains",
    "Céréales pour petit-déjeuner",
]

# Number of aliment to get by category
ALIMENT_BY_CATEGORY = 250

NUTRISCORE_COLOR = {
    'a': Back.GREEN,
    'b': Back.LIGHTGREEN_EX,
    'c': Back.LIGHTYELLOW_EX + Fore.BLACK,
    'd': Back.RED,
    'e': Back.LIGHTRED_EX,
}

# a list of products to ignore (based on product name)
DUMMY_PRODUCTS = [
    'casse croûte',
    'Lulu La Barquette Fraise',
    'Bananenchips',
]
