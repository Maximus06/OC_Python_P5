"""This module contains the class responsible to get the records
from openfoodfact api
"""

from colorama import init, Fore, Back

import requests
from time import sleep

from .openfood import Openfood
from ..settings import DATABASE, CATEGORIES, ALIMENT_BY_CATEGORY,\
                       DUMMY_PRODUCTS
from ..models.aliment import Aliment
from ..models.store import Store
from ..models.category import Category
from .. data.datamanager import DataManager
from ..helper.helper import progress_bar

class DataImport:
    """This class imports data from the openfoodfacts api
    in the database.

    attributes:
    - api: the class in charge to get the data from openfoodfacts api
    - aliments: a list of Aliment object
    - stores: a set of Store object. 
    """

    def __init__(self, api):
        """Constructor of the class
            Args:
                api: Openfood class in charge of communication
                with openfoodfacts api 
        """
        self.api = api        
        self.aliments = []
        self.stores = set()

    def get_food_by_category(self, categories):
        """get food for each category in the categories list
        
        args:
            - categories: list of Category objects
        """    

        for category in categories:

            data = self.api.get_data_by_category(category.name)
            self.prepare_aliments_from_dico(data, category)
        
        return self.aliments, self.stores

    def prepare_aliments_from_dico(self, data, category):
        """Create a list of Aliment object from the dictionnary data"""

        print('')
        msg = 'Traitement de la catégorie : '
        cate_name = str(category)
        print(msg + f'{Fore.MAGENTA} {cate_name} {Fore.RESET}')
        
        # for the len on the progress bar (-6 to align % with last letter)
        len_msg = len(msg) + len(cate_name ) -6

        products = data.get('products')        
        
        i = 0
        total = len(products)

        # Loop the food dictionnary
        for product in products:
            i = i+1
            percent = int(i / total * 100)
            progress_bar(percent, len_msg)            
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
                self.stores = self.stores.union(stores_set)
            
            # categories = [self.get_obj_category(category)]
            categories = [category]            
            
            brands = product.get('brands')            
            if 'ė' in  brands:
                brands = brands.replace('ė', 'é')                
            
            aliment = Aliment(name=name, description=description, score=score,
                url=url, nova=nova, brands=brands, stores=list(stores_set),
                categories=categories, code_bar=code)
            
            if aliment not in self.aliments:
                self.aliments.append(aliment)            
        
        # reset color
        print('\33[0m')
        

    def get_obj_category(self, name):    
        """Return a Category object from the database"""    
        category = self.session.query(Category).filter(
            Category.name == name).first()

        return category

    def _clean_stores(self, string_stores):
        """Return a set of store from a string with cleaned data:
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
        string_stores = string_stores.replace('superu carrefour contact '
            'carrefour intermarché superu', 'Super U, Carrefour, Intermarché')

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
    """Launch the import in the database"""

    # for windows console color
    init()

    db = DataManager(reset=True)
    api = Openfood(ALIMENT_BY_CATEGORY)
    data_import = DataImport(api)

    # Create the categories in the database from the setting list
    db.create_categories(CATEGORIES)

    # get a list of Category object from the database
    categories = db.get_categories()

    print(Fore.CYAN + '\nLancement de la récupération des données' + Fore.RESET)
    # Get the aliments and stores from the api
    aliments, stores = data_import.get_food_by_category(categories)

    # Save stores and aliments in the database
    db.save_stores(stores)
    db.save_food(aliments)

    # print(Fore.RESET + Back.RESET)
    print('')
    msg = f'L\'import de {len(aliments)} aliments a été réalisé avec succès et enregistré'\
          ' dans la base de données.'
    print(Fore.GREEN + msg)

if __name__ == "__main__":
    main()


