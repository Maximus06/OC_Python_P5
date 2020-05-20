"""This module constains the class Terminal in charge of input and output"""

from os import name as os_name, system
from random import sample

from colorama import init, Fore

from ..data.datamanager import DataManager
from ..helper.helper import cprint
from ..settings import CATEGORIES


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
            # print(choice)
            if choice == 'q' or choice == 'Q':
                cprint('\n A bientôt.', 'green')
                break
            elif choice == '1':
                self._clear_console()
                self._display_categories()
                valid_choice = [str(choice) for choice in range(1,len(CATEGORIES)+1)]
                valid_choice.append('q')
                category_choice = self._ask_choice(valid_choice)
                if category_choice != 'q':
                    category = CATEGORIES[int(category_choice)-1]
                    self._clear_console()
                    self._display_aliments(category)
                # break
            elif choice == '2':
                self._display_substitute()            
            
    
    def _clear_console(self):
        """This method clear the console"""
        if self.os_type == 'nt':
            system('cls')
        else:
            system('clear')

    def _main_menu(self):
        frame = "=" * 20
        msg = frame + " Bienvenue dans l'application Pur Beurre. " + frame
        cprint(msg, 'violet')

        msg = '\n Veuillez choisir une option et appuyez sur Entrée.'        
        print(Fore.LIGHTCYAN_EX + msg)        
        print('')

        msg = """ 1 = Choisir un aliment à remplacer.
 2 = Retrouver mes aliments substitués. 
        """
        print(msg)

    def _ask_choice(self, valid_choice):
        # print(valid_choice)
        while True:
            # answer = input(' \x1b[1;33;40mEntrez votre choix (Q pour quitter) \x1b[1;37;40m : ')            
            answer = input(Fore.LIGHTCYAN_EX + ' Entrez votre choix (Q pour quitter) : ')            
            if answer in valid_choice:
                break
            else:
                cprint(" Ce choix n'est pas une option valide", 'red')            
                
        return answer
        
    def _display_categories(self):
        msg = '\n Veuillez choisir une catégorie et appuyez sur Entrée'
        print(Fore.CYAN + msg)
        print('')
        i = 1
        for category in CATEGORIES:            
            print(f' {i} = {category}')
            i += 1
        print('')

    def _display_aliments(self, category):
        msg = '\n Veuillez choisir un aliment et appuyez sur Entrée'
        print(Fore.CYAN + msg)
        print('')

        # get 10 random aliments from this category
        all_aliments = self.db.get_aliments_from_category(category)
        aliments = sample(all_aliments, k=10)
        
        i = 1
        for aliment in aliments:
            print(f' {i} = {aliment.name}, {aliment.nutrition_score}')
            i += 1

        valid_choice = [str(choice) for choice in range(1,len(aliments)+1)]
        valid_choice.extend(['q', 'Q'])

        print('')
        choice = self._ask_choice(valid_choice)
        if choice.lower() == 'q':
            return

        self._clear_console()

        aliment = aliments[int(choice)-1]
        msg = (f"\n '{aliment.name}' de nutriscore {aliment.nutrition_score.upper()} peut "
             "être substitué avantageusement par l'aliment suivant:")
        print(Fore.LIGHTMAGENTA_EX + msg)

        substitute = self.db.get_substitute(category)

        msg = f""" Nom : {substitute.name}
 Description : {substitute.description}
 Nutriscore : {substitute.nutrition_score.upper()}
 Magasins : {substitute.get_stores()}
 Lien : {substitute.url}
"""
        print('')
        print(msg)
        print('')

        msg = 'Voulez vous enregistrer cette substitution ? O/N : '
        save = input(Fore.LIGHTGREEN_EX + msg)
        if save.lower() == 'o':
            self.db.save_substitute(aliment, substitute)
            print('aliment sauvegardé')

        input('Appuyez sur Entrée')
        
    def _display_substitute(self):
        """This method display the substitute aliment already saved"""
        substitutes = self.db.get_saved_substitutes()
        # TODO message for None substitute yet.
        
        self._clear_console()
        trait = '-' * 124

        if substitutes.rowcount == 0:
            print(Fore.YELLOW +  ' Aucun substitut enregistré n\'a été trouvé')
            print('')
            input(Fore.LIGHTCYAN_EX + ' Appuyez sur Entrée pour revenir au menu')
            return None

        print('')
        msg = ("Liste des aliments que vous avez déjà remplacés avec leurs" 
            f" substituts. Total : {substitutes.rowcount}")

        print(Fore.MAGENTA + msg)
        print('')

        print(trait)
        align_text = "|{:^4}|{:^50}|{:^7}|{:^50}|{:^7}|"
        print(align_text.format('N°', 'Aliments remplacés','score','substituts', 'score'))
        print(trait)

        i = 1
        for sub in substitutes:
            aliment = sub[1]
            # print(len(aliment))
            record = f"| {i} = {aliment:<50} {sub[2].upper():^7} {sub[4]:<50} {sub[5].upper():^7}|"
            print(record)
            i = i+1

        print(trait)

        print('')
        input(Fore.LIGHTCYAN_EX + ' Appuyez sur Entrée ')
        
