"""This module contains the class responsible to get the records
from openfoodfact api
"""
from colorama import init

import requests
from time import sleep

from ..settings import DATABASE, CATEGORIES, ALIMENT_BY_CATEGORY,\
                       DUMMY_PRODUCTS
from ..models.aliment import Aliment
from ..models.store import Store
from ..models.category import Category
from .. data.datamanager import DataManager
from ..helper.helper import progress_bar

class Openfood:
    """This class is in charge of communication with the openfoodfacts api."""

    def __init__(self, aliment_number=100):        
        self.aliment_number = aliment_number
        self.url = self._get_url()
        self.aliments = []
        self.stores = set()
    
    def _get_url(self):
        """This method returns the full url with parameters for the api"""

        url_base = "https://fr.openfoodfacts.org/cgi/search.pl?action=process"
        sort_by = "&sort_by=unique_scans_n"
        record_number = f"&page_size={self.aliment_number}&page=1"
        file_format = "&json=true"
        fields = "&fields=product_name,stores,nutrition_grade_fr,url,code,nova_group, \
            stores_tag,brands,generic_name"
        criteria_complete = "&tagtype_0=states&tag_contains_0=contains&tag_0=complete"

        return url_base + sort_by + record_number + file_format + fields + criteria_complete

    def get_food_by_category(self, categories):
        """get food for each category in the categories list
        
        args:
            - categories: list of Category objects            
        """    

        # all_stores = set()
        # all_aliments = []

        for category in categories:
            # request the aliment for this category
            url_with_category = self.url + \
                f"&tagtype_1=categories&tag_contains_1=contains&tag_1={category.name}"
            # print(f'\nUrl: {url_with_category}')
            result = requests.get(url_with_category)

            if result.ok == False:
                print(f"The error {result.reason} occurs with status code {result.status_code}")
                #TODO raise error
                return None        
            
            food = result.json()

            self.get_aliments_from_dico(food, category)

            # aliments, category_stores = self.get_aliments_from_dico(food, category)
            # Cumul the stores
            # all_stores = all_stores.union(category_stores)
            # Cumul the aliments
            # all_aliments.extend(aliments)

        # return all_aliments, all_stores
        return self.aliments, self.stores

    def get_aliments_from_dico(self, food, category):
        """Create a list of Aliment object from the dictionnary"""

        # list of aliments object for this category
        # aliments=[]

        print('\33[0m')
        print(f'\nTraitement de la catégorie :\33[32m {str(category)}\33[0m')    
        products = food.get('products')

        # all_stores = set()
        
        i = 0
        total = len(products)

        # Loop the food dictionnary
        for product in products:
            i = i+1
            percent = int(i / total * 100)
            progress_bar(percent, 50)
            # Sleep a little to enjoy this marvelous progress bar ^_^.
            sleep(0.002)

            # delete the return char to avoid uggly display
            name = product.get('product_name').replace('\n', ' ') 
            code = product.get('code')
            description = product.get('generic_name')
            # print(f'name: {name} - description: {description}')
            if name in DUMMY_PRODUCTS:
            # ignore dummy products
                continue

            score = product.get('nutrition_grade_fr')
            if score == None:
                # ignore the product without score
                continue
            else:
                score = score.strip()
            nova = product.get('nova_group')        
            url = product.get('url')

            # Stores
            string  =  product.get('stores')        
            # print(f'\nSTRING stores = {string}\n')
            
            if string:
                stores_set = self._clean_stores(string)                
                # cumul the stores for this aliment in the stores set for all
                # all_stores = all_stores.union(stores_set)
                self.stores = self.stores.union(stores_set)
            
            # categories = [self.get_obj_category(category)]
            categories = [category]
            
            # brands = product.get('brands').encode('utf8')
            brands = product.get('brands')            
            if 'ė' in  brands:
                # print(f'BRAND avt replace = {brands}')
                # print(f"BRAND encoded = {brands.encode('utf8')}")
                brands = brands.replace('ė', 'é')
                # print('\33[31m' +'ė have been replaced' + '\33[0m')
            
            aliment = Aliment(name=name, description=description, score=score,
                url=url, nova=nova, brands=brands, stores=list(stores_set),
                categories=categories, code_bar=code)
            
            if aliment not in self.aliments:
                self.aliments.append(aliment)            
        
        # return aliments, all_stores

    def get_obj_category(self, name):    
        """Return a Category object from the database"""    
        category = self.session.query(Category).filter(
            Category.name == name).first()

        return category

    def _clean_stores(self, string_stores):
        """Return a set of store from a list with cleaned data:
            - Clean exotic caractere
            - clean space
            - Capitalize
            - clean doublon
        """

        # A strange caractere 'ė' (Intermachė) crash sqlAlchemy
        # so we replace it by é
        string_stores = string_stores.replace('Дикси', 'Auchan')
        string_stores = string_stores.replace('Оливье', 'Auchan')
        string_stores = string_stores.lower()
        string_stores = string_stores.replace('ė', 'é')
        string_stores = string_stores.replace('elclerc', 'Leclerc')
        string_stores = string_stores.replace('centre leclerc', 'Leclerc')
        string_stores = string_stores.replace('e.leclerc', 'Leclerc')
        string_stores = string_stores.replace('e leclerc', 'Leclerc')
        string_stores = string_stores.replace('intermarche', 'Intermarché')
        string_stores = string_stores.replace('intermaché', 'Intermarché')
        string_stores = string_stores.replace('b i1', 'Bi1')
        string_stores = string_stores.replace('cœur', 'coeur')
        string_stores = string_stores.replace('superu carrefour contact carrefour intermarché superu',
            'Super U, Carrefour, Intermarché')

        # make a list from str
        brut_store = string_stores.split(',')    

        # delete the space, lower and capitalize the store
        clean_store = map(lambda store: store.strip().lower().capitalize(), brut_store)

        # clean again some store
        string_stores = string_stores.replace('Super u', 'Super U')
        string_stores = string_stores.replace('Cora intermarché superu', 'Super U')
        string_stores = string_stores.replace('Magasins u', 'Super U' )
        string_stores = string_stores.replace('U', 'Super U')

        #delete the doublon
        set_store = set(clean_store)
        
        return set_store

def main():
    # for windows console color
    init()

    db = DataManager(reset=True)
    api = Openfood(ALIMENT_BY_CATEGORY)

    # Create the categories in the database from the setting list
    db.create_categories(CATEGORIES)

    # get a list of Category object from the database
    categories = db.get_categories()

    # Get the aliments and stores from the api
    aliments, stores = api.get_food_by_category(categories)

    # Save stores and aliments in the database
    db.save_stores(stores)
    db.save_food(aliments)

if __name__ == "__main__":
    main()
        

