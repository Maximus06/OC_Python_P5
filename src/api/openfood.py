"""This module is responsible to get the records from openfoodfact api"""

# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#relationship-patterns

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .. models.aliment import Aliment
from .. models.store import Store

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
    fields = "&fields=product_name,stores,nutrition_grade_fr,url,code,nova_group, \
        stores_tag"
    criteria_complete = "&tagtype_0=states&tag_contains_0=contains&tag_0=complete"
    

    url = url_base + sort_by + record_number + file_format + fields + criteria_complete

    for category in categories:
        # request the aliment for this category
        url_with_category = url + f"&tagtype_1=categories&tag_contains_1=contains&tag_1={category}"
        print(f'\nUrl: {url_with_category}')
        result = requests.get(url_with_category)

        if result.ok == False:
            print(f"The error {result.reason} occurs with status code {result.status_code}")
            #TODO raise error
            return None        
        
        food = result.json()
        aliments, all_stores = get_aliments_from_dico(food, category)

        # for store in all_stores:
        #     print('\n*************************************************')
        #     print(f'Magasin: {store.name}')

        save_food(aliments)

def get_aliments_from_dico(food, category):
    # list of aliments object for this category
    aliments=[]

    print(f'\nTraitement de la catégorie : {category}')    
    products = food.get('products') 

    all_stores = []   
    
    # parcours de la liste de dictionnaire d'aliments
    for product in products:
        name = product.get('product_name')
        score = product.get('nutrition_grade_fr')
        if score == None:
            print(f'\n*******************************')
            print(f'{name} ne possède pas de score')
            continue
        else:
            score = score.strip()
        nova = product.get('nova_group')        
        url = product.get('url')

        string =  product.get('stores')        
        print(f'\nSTRING stores = {string}\n')
        #special case like Intermarchė
        if 'ė' in string:
            print(f'ALARM ė TROUVE dans {string}')
            string = string.replace('ė', 'é')
            print(f'apres remplacement: {string}')

        stores_str = string.rsplit(',')

        stores = []
        #creation des objets store
        for string in stores_str:
            stores.append(Store(string))
        all_stores.extend(stores)
        print(f'*** Objets store: {stores} ***')

        # print(f"\n****Stores: {stores} ****")
        # print(f"Name: {name} - Stores: {stores}")
        # print(f"Score: {score} - Nova: {nova}")
        # print(f"Url: {url}\n")
        
        aliment = Aliment(name=name, score=score, url=url, nova=nova, stores=stores)
        # aliment = Aliment(name=name, score=score, url=url, nova=nova)
        aliments.append(aliment)
        print(f'Un objet aliment: {aliment}')    
    
    
    return aliments, all_stores


def save_food(aliments):
    engine = create_engine('mysql://maximus:decimus@localhost/openfood')
    Session = sessionmaker(bind=engine)
    # Base = declarative_base()

    # 3 - create a new session
    session = Session()
    session.add_all(aliments)
    session.commit()
    session.close()


    


def get_food_from_api():
    pass

def main():
    get_food_by_category(categories)

if __name__ == "__main__":
    main()