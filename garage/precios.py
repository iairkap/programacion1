"""
Módulo de precios y suscripciones para el garage.

Funciones principales:
- configurar_precios()
- es_subscripcion_mensual(patente, datos)
- calcular_costo_de_estadia(patente, hora_salida, datos)


"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from garage.garage_util import buscar_por_patente

from datetime import datetime
from colorama import init, Fore, Style

# Inicializar colorama (solo una vez)
init(autoreset=True)

# CONFIGURACIÓN DE TARIFAS

def configurar_precios():
    """Devuelve las tarifas por tipo de vehículo (por_hora, mensual)."""
    return {
        "auto": {"por_hora": 100, "mensual": 15000},
        "moto": {"por_hora": 50, "mensual": 8000},
        "camion": {"por_hora": 200, "mensual": 25000},
    }



# FUNCIONES AUXILIARES

def es_subscripcion_mensual(patente, garage):
    """Chequea si la suscripción es mensual usando la vista de diccionarios.

    Retorna True si el slot con esa patente está ocupado y tiene
    `reservado_mensual` == "True" o es booleano True.
    """
    for slot in garage:
        if slot["patente"].lower() == patente.lower() and slot["ocupado"] == "True":
            val = slot.get("reservado_mensual", False)
            if isinstance(val, str):
                return val.lower() == "true"
            return bool(val)
    return False


# def buscar_patente_en_garage(garage, patente):
#     """Busca un vehículo por patente en la lista de diccionarios."""
#     for slot in garage:
#         if slot["patente"].lower() == patente.lower():
#             return slot
#     return None

# FUNCIÓN PRINCIPAL: CÁLCULO DE COSTO

def calcular_costo_de_estadia(patente, hora_salida=None, garage=None):
    """
    Calcula el costo de estadía de un vehículo según su patente y hora de salida.

    - Si tiene suscripción mensual → cobra tarifa mensual.
    - Si no → cobra tarifa por hora (mínimo 1h, usa datetime para diferencia real).
    - Si ocurre error → cobra tarifa mínima por hora.
    """
    if garage is None:
           print(Fore.RED + "⚠️ Error: Se requiere una lista de slots (garage) para calcular el costo.")
           raise ValueError("Se requiere una lista de slots (garage) para calcular el costo.")

    precios = configurar_precios()
    _,slot = buscar_por_patente(garage, patente)

    if not slot:
           print(Fore.YELLOW + f"No se encontró la patente {patente}")
           return 0

    tipo = slot.get("tipo_vehiculo", "").lower()
    if tipo not in precios:
           print(Fore.YELLOW + f"Tipo de vehículo desconocido para {patente}")
           return 0

    # Verificar suscripción mensual
    if es_subscripcion_mensual(patente, garage):
        return precios[tipo]["mensual"]

    # Cálculo por hora
    hora_entrada = slot.get("hora_entrada")
    if not hora_entrada:
           print(Fore.YELLOW + f"El vehículo {patente} no tiene hora de entrada registrada.")
           return precios[tipo]["por_hora"]

    if not hora_salida:
        hora_salida = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        formato = "%Y-%m-%d %H:%M"
        entrada = datetime.strptime(hora_entrada, formato)
        salida = datetime.strptime(hora_salida, formato)
        horas = max(1, (salida - entrada).total_seconds() / 3600)
        costo = precios[tipo]["por_hora"] * horas
        return round(costo, 2)
    except Exception as e:
            print(Fore.RED + f"⚠️ Error al calcular costo para {patente}: {e}")
            return precios[tipo]["por_hora"]

