"""
Módulo de precios y suscripciones para el garage.

Funciones principales:
- configurar_precios()
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



def calcular_costo_de_estadia(patente, hora_salida=None, garage=None, tarifa=None):
    """
    Calcula el costo de estadía de un vehículo según su patente y hora de salida.
    
    Parámetros:
    - patente: string con la patente del vehículo
    - hora_salida: string con hora de salida (formato YYYY-MM-DD HH:MM) o None para usar hora actual
    - garage: lista de pisos con slots (estructura 2D)
    - tarifa: lista de listas con tarifas CSV [garage_id, tipo, periodo_mensual, precio, ...]
              Si se proporciona, usa tarifas desde CSV. Si no, usa configurar_precios()
    
    Retorna:
    - float: costo calculado o 0 si hay error
    
    Lógica:
    - Si tiene suscripción mensual → cobra tarifa mensual fija
    - Si no → cobra tarifa por hora (mínimo 1h, usa datetime para diferencia real)
    - Si ocurre error → retorna 0
    """
    if garage is None:
        print(Fore.RED + "Error: Se requiere una lista de slots (garage) para calcular el costo." + Style.RESET_ALL)
        return 0

    # Buscar vehículo en el garage
    piso_idx, slot_id = buscar_por_patente(garage, patente)
    if (piso_idx, slot_id) == (-1, -1):
        print(Fore.RED + f"Error: Patente {patente} no encontrada." + Style.RESET_ALL)
        return 0

    # Obtener slot del garage
    slot = garage[piso_idx][slot_id - 1]  # slot_id comienza en 1
    
    # Obtener datos del slot
    tipo_vehiculo = slot.get("tipo_vehiculo", 0)
    hora_entrada = slot.get("hora_entrada")
    es_mensual = slot.get("reservado_mensual", False)
    
    # Convertir booleano si viene como string
    if type(es_mensual) is str:
        es_mensual = es_mensual.lower() == "true"
    
    # Determinar si usar tarifa CSV o configurar_precios()
    if tarifa:
        # Usar tarifas desde CSV
        precio_tarifa = _obtener_precio_tarifa(tipo_vehiculo, es_mensual, tarifa)
        if precio_tarifa is None:
            periodo_str = "Mensual" if es_mensual else "Diario"
            print(Fore.RED + f"Error: No hay tarifa configurada para tipo {tipo_vehiculo} - {periodo_str}." + Style.RESET_ALL)
            return 0
    else:
        # Usar configurar_precios() (sistema antiguo)
        precios = configurar_precios()
        tipo_nombre = _convertir_tipo_a_nombre(tipo_vehiculo)
        
        if tipo_nombre not in precios:
            print(Fore.YELLOW + f"Tipo de vehículo desconocido: {tipo_vehiculo}" + Style.RESET_ALL)
            return 0
        
        precio_tarifa = precios[tipo_nombre]["mensual"] if es_mensual else precios[tipo_nombre]["por_hora"]
    
    # Si es suscripción mensual, retorna tarifa fija
    if es_mensual:
        print(Fore.CYAN + f"Suscripción Mensual - Precio fijo: ${precio_tarifa}" + Style.RESET_ALL)
        return precio_tarifa
    
    # Si es diario, calcular por horas
    if not hora_entrada:
        print(Fore.YELLOW + "Advertencia: No se encontró hora de entrada. Cobrando tarifa mínima." + Style.RESET_ALL)
        return precio_tarifa
    
    if not hora_salida:
        hora_salida = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    try:
        # Intentar primero con formato que incluye segundos
        try:
            formato = "%Y-%m-%d %H:%M:%S"
            entrada = datetime.strptime(hora_entrada, formato)
        except ValueError:
            # Si falla, intentar sin segundos
            formato = "%Y-%m-%d %H:%M"
            entrada = datetime.strptime(hora_entrada, formato)
        
        # Para hora_salida, también intentar ambos formatos
        try:
            salida = datetime.strptime(hora_salida, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            salida = datetime.strptime(hora_salida, "%Y-%m-%d %H:%M")
        
        horas = max(1, (salida - entrada).total_seconds() / 3600)
        costo = precio_tarifa * horas
        print(Fore.CYAN + f"Diario - {horas:.1f} horas × ${precio_tarifa}/h = ${costo}" + Style.RESET_ALL)
        return round(costo, 2)
    except Exception as e:
        print(Fore.RED + f"Error al calcular costo para {patente}: {e}" + Style.RESET_ALL)
        return precio_tarifa


def _obtener_precio_tarifa(tipo_vehiculo, es_mensual, tarifa):
    """Busca el precio de tarifa según tipo de vehículo y período.
    
    tipo_vehiculo: número (1=moto, 2=auto, 3=camioneta)
    es_mensual: booleano (True=mensual, False=diario)
    tarifa: lista de listas [[garage_id, tipo, periodo_mensual, precio, ...], ...]
    Retorna: precio (float) o None si no existe
    """
    if not tarifa:
        return None
    
    # Convertir booleano a string para comparar con CSV
    periodo_buscado = "True" if es_mensual else "False"
    
    for row in tarifa:
        # row[1] = tipo, row[2] = periodo_mensual, row[3] = precio
        if len(row) < 4:
            continue
        
        try:
            tipo_tarifa = int(row[1]) if row[1] else 0
            tarifa_periodo = str(row[2])
            
            if tipo_tarifa == tipo_vehiculo and tarifa_periodo == periodo_buscado:
                return float(row[3])
        except (ValueError, IndexError, TypeError):
            continue
    
    return None


def _convertir_tipo_a_nombre(tipo_vehiculo):
    """Convierte número de tipo de vehículo a nombre para configurar_precios().
    
    1 -> "moto"
    2 -> "auto"
    3 -> "camion" (camioneta)
    """
    conversiones = {
        1: "moto",
        2: "auto",
        3: "camion"
    }
    return conversiones.get(tipo_vehiculo, "")

