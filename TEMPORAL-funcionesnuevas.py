import funciones
from mockdata import GARAGE, COSTOS
import random
from interaccion_usuario import pedir_patente
import json
import os

RUTA_JSON = "GARAGE_SLOTS_TEMPLATE.json"

def leer_garage():
    """Lee el archivo CSV y lo devuelve como lista de diccionarios."""
    """Lee el archivo JSON y devuelve lista de diccionarios.

    Si no existe el archivo JSON, lo crea a partir de la constante GARAGE importada
    desde `mockdata` (si existe). Normaliza campos para mantener compatibilidad con
    la lógica que esperaba strings como "True"/"False" en ciertos campos.
    """
    def _normalize_slot(slot):
        # Asegurar keys existan y sean strings similares al CSV previo
        s = dict(slot)
        # Campos booleanos representados como strings "True"/"False"
        for key in ("ocupado", "reservado_mensual"):
            if key in s:
                val = s[key]
                if isinstance(val, bool):
                    s[key] = "True" if val else "False"
                else:
                    # normalizar valores vacíos/None
                    s[key] = str(val) if val is not None else "False"
            else:
                s[key] = "False"

        # Campos numéricos a string (piso, id)
        for key in ("piso", "id"):
            if key in s:
                s[key] = str(s[key])
            else:
                s[key] = "0"

        # Otros campos que se usan como strings
        for key in ("tipo_slot", "tipo_vehiculo_estacionado", "patente", "hora_entrada"):
            s[key] = "" if s.get(key) is None else str(s.get(key))

        return s

    if not os.path.exists(RUTA_JSON):
        # Crear archivo a partir de GARAGE si está disponible
        try:
            datos_iniciales = [ _normalize_slot(slot) for slot in GARAGE ]
        except Exception:
            datos_iniciales = []

        with open(RUTA_JSON, "w", encoding="utf-8") as f:
            json.dump(datos_iniciales, f, ensure_ascii=False, indent=2)

    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        datos = json.load(f)

    # Normalizar cada slot antes de devolver
    return [_normalize_slot(slot) for slot in datos]




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
            if slot.get("tipo_slot") == str(tipo_vehiculo) or slot.get("tipo_slot") == "4":
                return (int(slot["piso"]), int(slot["id"]))
    return (-1, -1)


#modificado a logica diccionario y csv

def buscar_por_patente(garage, patente_buscada):
    for slot in leer_garage():
        if slot.get("patente") == patente_buscada and slot["ocupado"] == "True":
            return (int(slot["piso"]), int(slot["id"]))
    return (-1, -1)

#modificado a logica diccionario y csv
def contar_espacios_libres(garage):
    return sum(slot["ocupado"] == "False" for slot in leer_garage())


#modificado a logica diccionario y csv
def contar_por_tipo_vehiculo(garage, tipo_buscado):
    return sum(
        slot["ocupado"] == "True" and slot.get("tipo_vehiculo_estacionado") == str(tipo_buscado)
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
        if slot.get("patente") == patente and slot["ocupado"] == "True":
            return True
    return False



#modificado a logica diccionario y csv
def es_subscripcion_mensual(patente):
    """Chequea si la suscripción es mensual o diaria (lógica CSV)"""
    for slot in leer_garage():
        if slot.get("patente") == patente and slot["ocupado"] == "True":
            return slot.get("reservado_mensual") == "True"
    return False



#modificado a logica diccionario y csv
def buscar_patente(patente):
    """Busca información completa de una patente"""
    for slot in leer_garage():
        if slot.get("patente") == patente and slot["ocupado"] == "True":
            return slot
    return None



#modificado a logica diccionario y csv
def registrar_salida_vehiculo(garage, patente):
    datos = leer_garage()
    actualizado = False

    for slot in datos:
        if slot.get("patente") == patente and slot["ocupado"] == "True":
            slot["patente"] = ""
            slot["ocupado"] = "False"
            slot["hora_entrada"] = ""
            slot["tipo_vehiculo_estacionado"] = "0"
            actualizado = True
            break

    if actualizado:
        # Escribir JSON normalizado
        with open(RUTA_JSON, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True

    return False