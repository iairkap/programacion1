import os
import sys
from colorama import Fore, Style
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def clear_screen():
    """ Limpia la pantalla de la consola """    

    input(Fore.YELLOW + "\nPresione cualquier tecla para continuar..." + Style.RESET_ALL)
    if sys.platform.startswith('win'):
            os.system('cls')  # For Windows
    else:
            os.system('clear') # For Linux and macOS