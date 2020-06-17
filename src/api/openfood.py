"""This module contains the Openfood class"""

import requests


class Openfood:
    """This class is in charge of communication with the openfoodfacts api.

    Attributes
    ----------
    _aliment_number: int
        the number of aliment to import (default 100)
    _url: str
        The url with parameters to request the api.

    Methods:
    --------
    get_data_by_category: Return aliment datas for a category.

    """

    def __init__(self, aliment_number=100):
        """Init class attributs

            Args:
            - aliment_number: Number of aliment to import (int, default=100)
        """

        self._aliment_number = aliment_number
        self._url = self._get_url()

    def _get_url(self):
        """This method returns the full url with parameters for the api"""

        url_base = "https://fr.openfoodfacts.org/cgi/search.pl?action=process"
        sort_by = "&sort_by=unique_scans_n"
        record_number = f"&page_size={self._aliment_number}&page=1"
        file_format = "&json=true"
        fields = ("&fields=product_name,stores,nutrition_grade_fr,url,code,"
                  "nova_group,stores_tag,brands,generic_name")
        criteria_complete = (
            "&tagtype_0=states&tag_contains_0=contains&tag_0=complet"
        )

        return (
            url_base
            + sort_by
            + record_number
            + file_format
            + fields
            + criteria_complete
        )

    def get_data_by_category(self, category):
        """Return a dictionnary of aliments for the arg category.

            Args:
                - category: String name of the category
        """

        url_with_category = (
            self._url
            + f"&tagtype_1=categories&tag_contains_1=contains&tag_1={category}"
        )

        result = requests.get(url_with_category)

        if not result.ok:
            print(
                f"The error {result.reason} occurs with status code "
                f"{result.status_code}"
            )
            # TODO: raise error
            return None

        food = result.json()
        return food
