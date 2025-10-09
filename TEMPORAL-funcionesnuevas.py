import garage.slot_utils as slot_utils
from garage.mockdata import GARAGE, COSTOS
import random
from users.interaccion_usuario import pedir_patente
from garage.garage_util import * 

# -------------------------------------------------------
# Lógica basada en diccionarios (sin I/O)
# Requiere: from garage.mockdata import GARAGE, COSTOS
# -------------------------------------------------------

def leer_garage():
    """
    Convierte la estructura `GARAGE` (lista de pisos) a una lista plana de dicts.
    Keys por slot: 'piso','id','patente','tipo_slot','ocupado',
                   'reservado_mensual','hora_entrada','tipo_vehiculo_estacionado'
    """
    resultados = []
    for piso_idx, piso in enumerate(GARAGE):
        for slot in piso:
            # asumimos slot como lista/tupla en la forma esperada [id, patente, tipo_slot, ocupado, reservado, hora, tipo_veh]
            # Si slot fuera dict, se adapta también.
            if type(slot) is dict:
                s = dict(slot)
                s["piso"] = str(s.get("piso", piso_idx))
                s["id"] = str(s.get("id", "0"))
                s["patente"] = "" if s.get("patente") is None else str(s.get("patente"))
                s["tipo_slot"] = str(s.get("tipo_slot", "0"))
                s["ocupado"] = "True" if s.get("ocupado") else "False"
                s["reservado_mensual"] = "True" if s.get("reservado_mensual") else "False"
                s["hora_entrada"] = "" if not s.get("hora_entrada") else str(s.get("hora_entrada"))
                s["tipo_vehiculo_estacionado"] = str(s.get("tipo_vehiculo_estacionado", "0"))
                resultados.append(s)
                continue

            # Si es lista/tupla:
            if type(slot) in (list, tuple):
                id_val = slot[0] if len(slot) > 0 else 0
                patente_val = slot[1] if len(slot) > 1 else ""
                tipo_slot_val = slot[2] if len(slot) > 2 else 0
                ocupado_val = slot[3] if len(slot) > 3 else False
                reservado_val = slot[4] if len(slot) > 4 else False
                hora_val = slot[5] if len(slot) > 5 else None
                tipo_veh_val = slot[6] if len(slot) > 6 else 0

                resultados.append({
                    "piso": str(piso_idx),
                    "id": str(id_val),
                    "patente": "" if patente_val is None else str(patente_val),
                    "tipo_slot": str(tipo_slot_val),
                    "ocupado": "True" if ocupado_val else "False",
                    "reservado_mensual": "True" if reservado_val else "False",
                    "hora_entrada": "" if not hora_val else str(hora_val),
                    "tipo_vehiculo_estacionado": str(tipo_veh_val),
                })
                continue

            # Otros tipos: ignorar
            continue

    return resultados


def generar_fecha_aleatoria():
    """Genera una fecha y hora aleatoria en formato 'YYYY-MM-DD HH:MM'"""
    year = "2025"
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    return f"{year}-{month}-{day} {hour}:{minute}"


def busqueda_espacio_libre(garage=None, tipo_vehiculo=None):
    """
    Retorna (piso, id) del primer slot libre compatible con tipo_vehiculo.
    Si no hay, retorna (-1, -1).
    """
    datos = garage if garage is not None else leer_garage()
    for slot in datos:
        if slot.get("ocupado") == "False":
            if tipo_vehiculo is None or slot.get("tipo_slot") == str(tipo_vehiculo) or slot.get("tipo_slot") == "4":
                return (int(slot.get("piso", "0")), int(slot.get("id", "0")))
    return (-1, -1)


def buscar_por_patente(garage=None, patente_buscada=None):
    """
    Devuelve (piso, id) si encuentra la patente ocupada; (-1,-1) sino.
    """
    datos = garage if garage is not None else leer_garage()
    for slot in datos:
        if slot.get("patente") == patente_buscada and slot.get("ocupado") == "True":
            return (int(slot.get("piso", "0")), int(slot.get("id", "0")))
    return (-1, -1)


def contar_espacios_libres(garage=None):
    """Cuenta slots con 'ocupado' == 'False'."""
    datos = garage if garage is not None else leer_garage()
    return sum(1 for slot in datos if slot.get("ocupado") == "False")


def contar_por_tipo_vehiculo(garage=None, tipo_buscado=None):
    """Cuenta vehículos estacionados de un tipo (tipo_vehiculo_estacionado)."""
    datos = garage if garage is not None else leer_garage()
    return sum(1 for slot in datos if slot.get("ocupado") == "True" and slot.get("tipo_vehiculo_estacionado") == str(tipo_buscado))


def acceder_a_info_de_patentes(garage=None):
    """Devuelve lista de dicts con slots ocupados."""
    datos = garage if garage is not None else leer_garage()
    return [slot for slot in datos if slot.get("ocupado") == "True"]


def chequear_existencia_patente(patente, garage=None):
    """Devuelve True si la patente existe y está ocupada."""
    datos = garage if garage is not None else leer_garage()
    for slot in datos:
        if slot.get("patente") == patente and slot.get("ocupado") == "True":
            return True
    return False


def es_subscripcion_mensual(patente, garage=None):
    """Devuelve True si la patente corresponde a un reservado mensual (reservado_mensual == 'True')."""
    datos = garage if garage is not None else leer_garage()
    for slot in datos:
        if slot.get("patente") == patente and slot.get("ocupado") == "True":
            return slot.get("reservado_mensual") == "True"
    return False


def buscar_patente(patente, garage=None):
    """Devuelve el dict completo del slot si la patente está ocupada, o None."""
    datos = garage if garage is not None else leer_garage()
    for slot in datos:
        if slot.get("patente") == patente and slot.get("ocupado") == "True":
            return slot
    return None

