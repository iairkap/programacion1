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

    # Buscar el slot en el piso correcto
    slot = None
    for piso in garage:
        for s in piso:
            if s.get("piso") == piso_idx and s.get("id") == slot_id:
                slot = s
                break
        if slot:
            break
    
    if not slot:
        print(Fore.RED + f"Error: No se pudo encontrar el slot {slot_id} en piso {piso_idx}." + Style.RESET_ALL)
        return 0
    
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
    
    # Cálculo por horas (no mensual)
    if not hora_entrada:
        print(Fore.RED + "Error: No se encontró la hora de entrada del vehículo." + Style.RESET_ALL)
        return 0
    
    # Usar hora actual si no se proporciona hora_salida
    if hora_salida is None:
        hora_salida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calcular diferencia de horas
    try:
        # Soportar formato con y sin segundos
        formatos = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        entrada_dt = None
        salida_dt = None
        
        for formato in formatos:
            try:
                entrada_dt = datetime.strptime(hora_entrada, formato)
                break
            except ValueError:
                continue
        
        for formato in formatos:
            try:
                salida_dt = datetime.strptime(hora_salida, formato)
                break
            except ValueError:
                continue
        
        if entrada_dt is None or salida_dt is None:
            print(Fore.RED + f"Error: Formato de fecha inválido. Entrada: {hora_entrada}, Salida: {hora_salida}" + Style.RESET_ALL)
            return 0
        
        # Calcular diferencia en horas
        diferencia = salida_dt - entrada_dt
        horas = diferencia.total_seconds() / 3600
        
        # Redondear hacia arriba (mínimo 1 hora)
        if horas < 1:
            horas = 1
        else:
            # Redondear hacia arriba al entero más cercano
            horas = int(horas) + (1 if horas % 1 > 0 else 0)
        
        costo_total = precio_tarifa * horas
        print(Fore.GREEN + f"Estadía de {horas} hora(s) a ${precio_tarifa}/h = ${costo_total}" + Style.RESET_ALL)
        return costo_total
        
    except Exception as e:
        print(Fore.RED + f"Error al calcular costo: {e}" + Style.RESET_ALL)
        return 0


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