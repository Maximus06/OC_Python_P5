"""This module contains the class responsible to get the records
from openfoodfact api
"""


from time import sleep

from colorama import init, Fore

from .openfood import Openfood
from ..settings import (
    CATEGORIES,
    ALIMENT_BY_CATEGORY,
    DUMMY_PRODUCTS,
)
from ..models.aliment import Aliment
from ..data.datamanager import DataManager
from ..helper.helper import progress_bar


class DataImport:
    """This class imports data from the openfoodfacts api
    in the database.

    Attributes
    ----------
    _api: the class in charge to get the data from openfoodfacts api.
    _aliments: a list of Aliment object.
    _stores: a set of Store object.

    Public methods
    --------------
    get_aliments_by_category : return a list of aliments and a set of stores
    """

    def __init__(self, api):
        """Init class attributs

            Args:
                api: Openfood class in charge of communication
                with openfoodfacts api
        """
        self._api = api
        self._aliments = []
        self._stores = set()

    def get_aliments_by_category(self, categories):
        """Get aliments for each category in the categories list

        Make a request for each category
        Process the data to extract aliments dataset
        Use the loop to extract the stores

        Args:
            - categories: list of Category objects

        Return : Aliment list, string set of stores
        """

        for category in categories:

            data = self._api.get_data_by_category(category.name)
            self._prepare_aliments_from_dico(data, category)

        return self._aliments, self._stores

    def _prepare_aliments_from_dico(self, data, category):
        """Create a list of Aliment object from the dictionnary data

        Args:
            - data: the json data
            - category: object Category
        """

        print('')
        msg = 'Traitement de la catégorie : '
        cate_name = str(category)
        print(msg + f'{Fore.MAGENTA} {cate_name} {Fore.RESET}')

        # for the len on the progress bar (-6 to align % with last letter)
        len_msg = len(msg) + len(cate_name) - 6

        products = data.get('products')

        i = 0
        total = len(products)

        # Loop the food dictionnary
        for product in products:
            i = i + 1
            percent = int(i / total * 100)
            progress_bar(percent, len_msg)
            # Sleep a little to enjoy this marvelous progress bar ^_^.
            sleep(0.001)

            aliment = self._get_aliment(product, category)
            if (aliment is not None) and (aliment not in self._aliments):
                self._aliments.append(aliment)

        # reset color
        print('\33[0m')

    def _get_aliment(self, product, category):
        """Return a Aliment object from the product dictionnary

        Args:
            - product: contains the aliment datas (dict)
            - category: the category object of the aliment (Category)
        """

        # delete return char to avoid uggly display
        name = product.get('product_name').replace('\n', ' ')
        if name in DUMMY_PRODUCTS:
            # ignore dummy products
            return None

        score = product.get('nutrition_grade_fr')
        if score is None:
            # ignore the product without score
            return None
        else:
            score = score.strip()

        code = product.get('code')
        description = product.get('generic_name')

        nova = product.get('nova_group')
        url = product.get('url')

        # Stores
        the_stores = product.get('stores')
        stores_set = set()
        # breakpoint()
        if the_stores:
            stores_set = self._clean_stores(the_stores)
            # cumul the stores for this aliment in the stores set for all
            self._stores = self._stores.union(stores_set)

        categories = [category]

        brands = product.get('brands')
        if 'ė' in brands:
            brands = brands.replace('ė', 'é')

        aliment = Aliment(
            name=name,
            description=description,
            score=score,
            url=url,
            nova=nova,
            brands=brands,
            stores=list(stores_set),
            categories=categories,
            code_bar=code,
        )

        return aliment

    def _clean_stores(self, string_stores):
        """Return a set from a string with cleaned data:
            - Clean exotic caractere
            - clean space
            - Capitalize
            - clean doublon

        Args:
        string_stores: a string of store (can be with comma separation)

        Return: set of string stores
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
        string_stores = string_stores.replace(
            'superu carrefour contact ' 'carrefour intermarché superu',
            'Super U, Carrefour, Intermarché',
        )

        # make a list from str
        brut_store = string_stores.split(',')

        # delete the space, lower and capitalize the store
        clean_store = map(
            lambda store: store.strip().lower().capitalize(), brut_store
        )

        # clean again some store
        string_stores = string_stores.replace('Super u', 'Super U')
        string_stores = string_stores.replace(
            'Cora intermarché superu', 'Super U'
        )
        string_stores = string_stores.replace('Magasins u', 'Super U')
        string_stores = string_stores.replace('U', 'Super U')

        # delete the doublon
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

    print(
        Fore.CYAN + '\nLancement de la récupération des données' + Fore.RESET
    )
    # Get the aliments and stores from the api
    aliments, stores = data_import.get_aliments_by_category(categories)

    # Save stores and aliments in the database
    db.save_stores(stores)
    db.save_food(aliments)

    # print(Fore.RESET + Back.RESET)
    print('')
    msg = (
        f'L\'import de {len(aliments)} aliments a été réalisé avec succès et '
        ' enregistré dans la base de données.'
    )
    print(Fore.GREEN + msg)


if __name__ == "__main__":
    main()
