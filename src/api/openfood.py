"""This module is responsible to get the records from openfoodfact api"""
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html

import requests
import json

categories = [
    "Biscuits et gâteaux",
    "Plats préparés",
    # "Boissons chaudes",
    # "Boissons aux fruits",
    # "Entrées",
    # "Plats préparés",
    # "Desserts",
    # "Produits laitiers",
    # "Yaourts",
    # "Pains",
    # "Céréales pour petit-déjeuner",
    ]

def get_food_by_category(categories, number_of_food=10):
    """get food for each category in the categories list
    
    args:
        - categories: list of categories
        - number_of_food: the int number of food to get 
    """
    url_base = "https://fr.openfoodfacts.org/cgi/search.pl?action=process"
    sort_by = "&sort_by=unique_scans_n"
    record_number = f"&page_size={number_of_food}&page=1"
    file_format = "&json=true"
    fields = "&fields=product_name,stores,nutrition_grade_fr,url,code,nova_group"
    

    url = url_base + sort_by + record_number + file_format + fields    

    for cate in categories:
        url_with_category = url + f"&tagtype_0=categories&tag_contains_0=contains&tag_0={cate}"
        result = requests.get(url_with_category)        

        if result.ok == False:
            print(f"The error {result.reason} occurs with status code {result.status_code}")
            #TODO raise error
            return None        
        
        food = result.json()
        save_food(food, cate)
        # food = json.loads(foods.json())
        # print(type(food))

def save_food(food, category):
    print(f'\nTraitement de la catégorie : {category}')    
    products = food.get('products')    
    
    # parcours de la liste de dictionnaire d'aliments
    for product in products:
        name = product.get('product_name')
        score = product.get('nutrition_grade_fr')
        nova = product.get('nova_group')
        stores = product.get('stores')
        url = product.get('url')

        print(f"Name: {name} - Stores: {stores}")
        print(f"Score: {score} - Nova: {nova}")
        print(f"Url: {url}\n")
    


def get_food_from_api():
    pass

def main():
    get_food_by_category(categories)

if __name__ == "__main__":
    main()