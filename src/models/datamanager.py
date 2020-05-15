from random import choice

from .base import Session
from .aliment import Aliment
from .category import Category
from .store import Store


def get_substitute(category):
    """Return an Aliment object with a A score
    
    args:
        category: the category of the Aliment to substitute
    """

    # session = Session()

    # query the aliment of this category with a A score
    aliments = session.query(Aliment).\
        filter(Aliment.categories.any(name=category)).\
        filter(Aliment.nutrition_score=='a').\
        all()

    print(f'Nombre de substition possible de score A: {len(aliments)}')    

    # for product in aliments:
    #     print(product.name, product.stores)

    substitut = choice(aliments)

    # session.close()

    return substitut



if __name__ == "__main__":
    from colorama import init

    init()

    # console color
    CEND = '\33[0m'
    CRED    = '\33[31m'
    CGREEN = '\33[32m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'

    def cprint(str, color):
        print(color + str + CEND)

    session = Session()

    # aliment = get_substitute("Pains")
    aliment = get_substitute("Plats préparés")
    print('')
    msg = 'Vous pouvez remplacer avantageusement votre aliment par celui-ci :\n'    
    cprint(msg.center(80), CVIOLET)
    print('Aliment :'.rjust(20), aliment.name + f' - ({aliment.brands})')
    print(f'Nutriscore :'.rjust(20), f'{CGREEN}{aliment.nutrition_score.upper()} {CEND}')
    print(f'Magasins :'.rjust(20), f'{aliment.get_stores()}')
    print(f'Lien Openfoodfacts :'.rjust(20), f'{aliment.url}')

    session.close()

