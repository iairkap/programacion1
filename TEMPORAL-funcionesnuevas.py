import funciones
from mockdata import GARAGE, COSTOS
import random
from interaccion_usuario import pedir_patente
import csv  # <---- agregalo también arriba de todo si no está

RUTA_CSV = "GARAGE_SLOTS_TEMPLATE.csv"

def leer_garage():
    """Lee el archivo CSV y lo devuelve como lista de diccionarios."""
    with open(RUTA_CSV, mode="r", encoding="utf-8", newline="") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        garage = [dict(fila) for fila in lector]
    return garage




def generar_fecha_aleatoria():
    """Genera una fecha y hora aleatoria en formato 'YYYY-MM-DD HH:MM'"""
    year = "2025"
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    return f"{year}-{month}-{day} {hour}:{minute}"


#modificado a logica diccionario y csv
def busqueda_espacio_libre(garage, tipo_vehiculo):
    for slot in leer_garage():
        if slot["ocupado"] == "False":
            if slot["tipo_slot"] == str(tipo_vehiculo) or slot["tipo_slot"] == "4":
                return (int(slot["piso"]), int(slot["id"]))
    return (-1, -1)


#modificado a logica diccionario y csv

def buscar_por_patente(garage, patente_buscada):
    for slot in leer_garage():
        if slot["patente"] == patente_buscada and slot["ocupado"] == "True":
            return (int(slot["piso"]), int(slot["id"]))
    return (-1, -1)

#modificado a logica diccionario y csv
def contar_espacios_libres(garage):
    return sum(slot["ocupado"] == "False" for slot in leer_garage())


#modificado a logica diccionario y csv
def contar_por_tipo_vehiculo(garage, tipo_buscado):
    return sum(
        slot["ocupado"] == "True" and slot["tipo_vehiculo_estacionado"] == str(tipo_buscado)
        for slot in leer_garage()
    )


#modificado a logica diccionario y csv

def acceder_a_info_de_patentes():
    """Devuelve todas las filas con vehículos estacionados (ocupados=True)"""
    datos = []
    for slot in leer_garage():
        if slot["ocupado"] == "True":
            datos.append(slot)
    return datos


#modificado a logica diccionario y csv
def chequear_existencia_patente(patente):
    """Chequea si la patente existe en el sistema (lógica CSV)"""
    for slot in leer_garage():
        if slot["patente"] == patente and slot["ocupado"] == "True":
            return True
    return False



#modificado a logica diccionario y csv
def es_subscripcion_mensual(patente):
    """Chequea si la suscripción es mensual o diaria (lógica CSV)"""
    for slot in leer_garage():
        if slot["patente"] == patente and slot["ocupado"] == "True":
            return slot["reservado_mensual"] == "True"
    return False



#modificado a logica diccionario y csv
def buscar_patente(patente):
    """Busca información completa de una patente"""
    for slot in leer_garage():
        if slot["patente"] == patente and slot["ocupado"] == "True":
            return slot
    return None



#modificado a logica diccionario y csv
def registrar_salida_vehiculo(garage, patente):
    datos = leer_garage()
    actualizado = False

    for slot in datos:
        if slot["patente"] == patente and slot["ocupado"] == "True":
            slot["patente"] = ""
            slot["ocupado"] = "False"
            slot["hora_entrada"] = ""
            slot["tipo_vehiculo_estacionado"] = "0"
            actualizado = True
            break

    if actualizado:
        archivo_csv = open(RUTA_CSV, "w", encoding="utf-8", newline="")
        campos = list(datos[0].keys())
        escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(datos)
        archivo_csv.close()
        return True

    return False