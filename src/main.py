"""This module launch the application"""

from sys import exit

from colorama import Fore
from sqlalchemy.exc import OperationalError

from .view.terminal import Terminal


def main():
    app = Terminal()

    try:
        app.run()
    except OperationalError:
        msg = "L'application n'a pas pu se connecter à la base de données."
        print(Fore.RED + msg)
        msg = "Veuillez vérifier les informations dans le dictionnaire " \
            "DATABASE du fichier setting.py"
        print(Fore.RED + msg)
        
        exit()


if __name__ == "__main__":
    main()