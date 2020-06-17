"""This module constains the class Terminal in charge of input and output"""

from os import name as os_name, system
from random import sample
from webbrowser import open_new as open_browser

from colorama import init, Fore, Back

from ..data.datamanager import DataManager
from ..helper.helper import cprint
from ..settings import CATEGORIES, NUTRISCORE_COLOR


class Terminal:
    """This class manage the communication with the user"""

    def __init__(self):
        self.db = DataManager()
        self.os_type = os_name

    def run(self):
        """This method is the main loop of the application"""

        # for color in window console
        init(autoreset=True)

        while True:
            self._clear_console()
            self._main_menu()

            choice = self._ask_choice(('1', '2', 'q'))
            if choice == 'q' or choice == 'Q':
                cprint('\n A bientôt.', 'green')
                break
            elif choice == '1':
                # Choice replace a aliment
                self._clear_console()
                self._display_categories()
                valid_choice = [
                    str(choice) for choice in range(1, len(CATEGORIES) + 1)
                ]
                valid_choice.append('q')
                category_choice = self._ask_choice(valid_choice)
                if category_choice != 'q':
                    category = CATEGORIES[int(category_choice) - 1]
                    self._clear_console()
                    self._display_aliments(category)
            elif choice == '2':
                # Choice show substitut saved.
                self._display_substitutes()

    def _clear_console(self):
        """This method clear the console"""
        if self.os_type == 'nt':
            system('cls')
        else:
            system('clear')

    def _main_menu(self):
        """Display the main menu"""
        frame = "=" * 20
        msg = frame + " Bienvenue dans l'application Pur Beurre. " + frame
        cprint(msg, 'violet')

        msg = '\n Veuillez choisir une option et appuyez sur Entrée.'
        print(Fore.LIGHTCYAN_EX + msg)
        print('')

        msg = (
            " 1 = Choisir un aliment à remplacer. \n"
            " 2 = Retrouver mes aliments substitués.\n"
        )
        print(msg)

    def _ask_choice(self, valid_choice):
        """Return the choice done by the user

            Args:
                - valid_choice: List of allowed choice.
        """
        while True:
            answer = input(
                Fore.LIGHTGREEN_EX + ' Entrez votre choix (Q pour quitter) : '
            )
            if answer in valid_choice:
                break
            else:
                cprint(" Ce choix n'est pas une option valide", 'red')

        return answer

    def _display_categories(self):
        """Display a list of categories associated to a number"""

        msg = '\n Veuillez choisir une catégorie et appuyez sur Entrée'
        print(Fore.CYAN + msg)
        print('')
        i = 1
        for category in CATEGORIES:
            print(f' {i} = {category}')
            i += 1
        print('')

    def _display_aliments(self, category):
        """Display a list of 10 random aliments for the category given"""

        msg = '\n Veuillez choisir un aliment et appuyez sur Entrée'
        print(Fore.CYAN + msg)
        print('')

        # get 10 random aliments from this category
        all_aliments = self.db.get_aliments_from_category(category)
        aliments = sample(all_aliments, k=10)

        i = 1
        for aliment in aliments:
            colored_score = self.get_nutriscore_colored(
                aliment.nutrition_score
            )
            name = aliment.name.replace('\n', ' ')
            msg = f' {i} = {name} (nutriscore : {colored_score})'

            print(msg)
            i += 1

        valid_choice = [str(choice) for choice in range(1, len(aliments) + 1)]
        valid_choice.extend(['q', 'Q'])

        print('')
        choice = self._ask_choice(valid_choice)
        if choice.lower() == 'q':
            return

        self._clear_console()

        aliment = aliments[int(choice) - 1]
        msg = (
            f"\n '{aliment.name}' de nutriscore "
            f"{aliment.nutrition_score.upper()} peut "
            "être substitué avantageusement par l'aliment suivant:"
        )
        print(Fore.LIGHTCYAN_EX + msg)

        substitute = self.db.get_substitute(category)

        msg = f""" Nom : {substitute.name}
 Description : {substitute.description}
 Nutriscore : {self.get_nutriscore_colored(substitute.nutrition_score)}
 Magasins : {substitute.get_stores()}
 Lien : {substitute.url}
"""
        print('')
        print(msg)
        print('')

        msg = ' Voulez vous enregistrer cette substitution ? O/N : '
        save = input(Fore.LIGHTGREEN_EX + msg)
        if save.lower() == 'o':
            self.db.save_substitute(aliment, substitute)
            print(Fore.LIGHTCYAN_EX + '\n Substitut sauvegardé')
            input(
                Fore.LIGHTCYAN_EX
                + '\n Appuyez sur Entrée pour revenir au menu'
            )

    def _display_substitutes(self):
        """This method display the substitutes already saved"""

        self._clear_console()

        substitutes = self.db.get_saved_substitutes()
        total_sub = substitutes.rowcount
        if total_sub == 0:
            print(Fore.YELLOW + ' Aucun substitut enregistré n\'a été trouvé')
            print('')
            input(
                Fore.LIGHTCYAN_EX + ' Appuyez sur Entrée pour revenir au menu'
            )
            return None

        records = substitutes.fetchall()

        while True:
            self._clear_console()

            print('')
            msg = (
                "Liste des aliments que vous avez déjà remplacés avec leurs"
                f" substituts. Total : {total_sub}"
            )

            print(Fore.MAGENTA + msg)
            print('')

            # print(substitutes.keys())
            # records = substitutes.fetchall()
            # print(type(records))
            # print(records)

            trait = '-' * 138
            print(trait)
            align_text = "|{:^4}| {:^50} | {:^10} | {:^50} | {:^10} |"
            print(
                align_text.format(
                    'N°',
                    'Aliments remplacés',
                    'NutriScore',
                    'substituts',
                    'NutriScore',
                )
            )
            print(trait)

            i = 1
            # for sub in substitutes:
            for sub in records:
                # delete the return char to avoid uggly display
                aliment = sub[1].replace('\n', ' ')
                if len(aliment) > 49:
                    aliment = aliment[:47] + '...'
                substitute = sub[4].replace('\n', ' ')
                score_alim = self.get_nutriscore_colored(sub[2])
                score_sub = self.get_nutriscore_colored(sub[5])

                # print(len(aliment))
                record = (
                    f"|{i:^4}| {aliment:<50} |    {score_alim:^5}     | "
                    f"{substitute:<50} |    {score_sub:^5}     |"
                )
                print(record)
                i = i + 1

            print(trait)

            print('')
            msg = (
                ' Entrez un numéro pour voir le détail du substitut '
                'dans votre navigateur'
            )

            print(Fore.LIGHTCYAN_EX + msg)

            valid_choice = [str(choice) for choice in range(1, total_sub + 1)]
            valid_choice.append('q')

            choice = self._ask_choice(valid_choice)
            if choice == 'q' or choice == 'Q':
                break

            aliment = records[int(choice) - 1]

            # the replaced aliment url
            # url = aliment[6]
            # open_browser(url)

            # the substitut url
            url = aliment[7]
            open_browser(url)

    def get_nutriscore_colored(self, nutriscore):
        """Return a string colored depending on nutriscore"""

        color = NUTRISCORE_COLOR.get(nutriscore)
        return f'{color} {nutriscore.upper()} {Back.RESET + Fore.RESET}'


if __name__ == '__main__':
    init(autoreset=True)
    t = Terminal()
    A = t.get_nutriscore_colored('a')
    B = t.get_nutriscore_colored('b')
    print(A)
    print(B)
