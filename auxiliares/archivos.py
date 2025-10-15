""" Funcion para leer, para escribir, para guardar archivos csv que me sirve de forma general, no se puede usar la libreria csv"""
import os

def crear_archivo(filename):
    with open(filename, 'w') as f:
        f.write("")


def leer_csv(filename):
    """ Lee un archivo CSV y devuelve una lista de listas con los datos.
    Cada sublista representa una fila del archivo CSV.
    Si el archivo no existe, devuelve una lista vacía.
    """
    if not os.path.exists(filename):
        return []
    
    with open(filename, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        data = [line.strip().split(',') for line in lines]
    return data


def escribir_csv(filename, data):
    """ Escribe una lista de listas en un archivo CSV.
    Cada sublista representa una fila que se escribirá en el archivo CSV.
    Si el archivo no existe, se crea uno nuevo.
    """
    with open(filename, mode='w', encoding='utf-8') as file:
        for row in data:
            line = ','.join(map(str, row))  # Convierte cada elemento a string y une con comas
            file.write(line + '\n')  # Escribe la línea en el archivo seguida de un salto de línea