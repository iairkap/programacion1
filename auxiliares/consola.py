import os
import sys

def clear_screen():
    """ Limpia la pantalla de la consola """    

    input("Presione cualquier tecla para continuar... ")
    if sys.platform.startswith('win'):
            os.system('cls')  # For Windows
    else:
            os.system('clear') # For Linux and macOS