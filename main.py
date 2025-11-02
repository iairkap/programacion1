import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import garage.slot_utils as slot_utils
import random
from users.interaccion_usuario import pedir_patente
from garage.garage_util import buscar_por_patente
from users import users_garage
from users.users_garage import (get_garage_data, actualizar_garage)
from cache.json import leer_estado_garage, guardar_estado_garage
from colorama import Fore, Style
from garage.precios import (configurar_precios, es_subscripcion_mensual,
                        calcular_costo_de_estadia)
from auxiliares.date import get_current_time_json
from auxiliares.consola import clear_screen

def leer_garage_normalizado():
    """
    Lee el garage y retorna una lista de diccionarios normalizados.
    Cada slot esta representado como un diccionario 
    """
    garage_id = leer_estado_garage()['garage_id']
    return users_garage.get_garage_data(garage_id)


def modificar_vehiculo(garage, patente, nuevo_tipo=None, nueva_patente=None, nueva_estadia=None):
    """
    Modifica los datos de un vehículo en el garage según la patente.
    Busca el vehículo por su patente en la estructura garage y actualiza el tipo de vehículo y/o la patente si se proporcionan nuevos valores.
    """
    # Busca el vehículo por patente
    try:
        for piso in garage:
            for slot in piso:
                if slot["ocupado"] == True and slot["patente"] == patente:
                    # Modifica solo los campos que no son None
                    if nuevo_tipo:
                        slot["tipo_vehiculo"] = nuevo_tipo        # Cambia tipo de vehículo
                    if nueva_patente:
                        slot["patente"] = nueva_patente     # Cambia patente
                    if nueva_estadia:
                        slot["reservado_mensual"] = nueva_estadia  # Cambia tipo de estadía
                    return True
    except Exception as e:
        print(Fore.RED + f"Error modificando vehículo: {e}" + Style.RESET_ALL)
    return False

def generar_fecha_aleatoria():
    """Genera una fecha y hora aleatoria en formato 'YYYY-MM-DD HH:MM'"""
    year = "2025"
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    return f"{year}-{month}-{day} {hour}:{minute}"


def eliminar_fila_por_valor(valor, garage):
    """Elimina la primera fila que contiene el valor dado, con manejo de errores."""
    try:
        for i in range(len(garage)):
            if valor in garage[i]:
                del garage[i]
                print(Fore.GREEN + f"Fila eliminada correctamente (valor: {valor})." + Style.RESET_ALL)
                return True
    except Exception as e:
        print(Fore.RED + f"Error eliminando fila: {e}" + Style.RESET_ALL)
        return False
    print(Fore.YELLOW + "No se encontró ninguna fila con el valor especificado." + Style.RESET_ALL)
    return False

def ingresar_patente():
    """Solicita y valida una patente, con manejo de errores y colorama."""
    while True:
        try:
            patente = pedir_patente()
            if chequear_existencia_patente(patente):
                print(Fore.RED + "Error: La patente ya existe en el sistema." + Style.RESET_ALL)
                continue
            if len(patente) == 6 and patente[:3].isalpha() and patente[3:].isdigit():
                print(Fore.GREEN + "Patente válida ingresada." + Style.RESET_ALL)
                return patente
            else:
                print(Fore.YELLOW + "Error: Formato de patente inválido. Intente nuevamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error procesando la patente: {e}. Intente nuevamente." + Style.RESET_ALL)

def acceder_a_info_de_patentes(garage):
    """Devuelve lista de dicts con slots ocupados."""
    datos = garage
    return [slot for slot in datos if slot.get("ocupado") == True]

def chequear_existencia_patente(patente, garage ):
    """Devuelve True si la patente existe y está ocupada."""
    datos = garage
    for slot in datos:
        if slot["patente"] == patente and slot["ocupado"] == True:
            return True
    return False

def es_subscripcion_mensual(patente, garage):
    """Chequea si la subscripcion es mensual usando la vista de diccionarios.

    Retorna True si el slot tiene `reservado_mensual` == "True" o es True.
    """
    datos = garage
    for slot in datos:
        if slot["patente"] == patente and slot["ocupado"] == True:
            val = slot["reservado_mensual"]
            # Normalizar distintos tipos (str "True"/"False" o booleano)
            if type(val) is str:
                return val == "True"
            return bool(val)
    return False

def busqueda_espacio_libre(garage, tipo_vehiculo=None):
    for piso in garage: 
        for slot in piso:
            if slot["ocupado"] == False:
                if tipo_vehiculo is None or slot["tipo_slot"] == str(tipo_vehiculo) or slot["tipo_slot"] == tipo_vehiculo:
                    piso_val = int(slot["piso"]) if "piso" in slot else 0
                    id_val = int(slot["id"]) if "id" in slot else 0
                    return (piso_val, id_val)
                    
    return (-1, -1)


def contar_espacios_libres(garage=None):
    """
    Cuenta la cantidad de espacios libres en el garage.
    Cuenta slots con 'ocupado' == 'False'.
    """
    datos = leer_garage_normalizado()
    return sum(1 for slot in datos if slot["ocupado"] == "False")


def calcular_costo_de_estadia(patente, hora_salida, tarifa):
    """
    Calcula el costo de estadía de un vehículo.
    Lee el garage desde cache, busca la patente y calcula según tarifa (diaria o mensual).
    
    patente: string con la patente del vehículo
    hora_salida: string con la hora de salida (formato YYYY-MM-DD HH:MM)
    tarifa: lista de listas con tarifas [garage_id, tipo, periodo_mensual, precio, moneda, descripcion]
    """
    try:
        # Leer el garage_id desde cache
        cache_data = leer_estado_garage()
        if not cache_data:
            print(Fore.RED + "Error: No se pudo leer el estado del garage." + Style.RESET_ALL)
            return 0
        
        garage_id = cache_data.get('garage_id')
        if not garage_id:
            print(Fore.RED + "Error: No hay garage_id en cache." + Style.RESET_ALL)
            return 0
        
        # Leer el garage desde CSV
        garage = get_garage_data(garage_id)
        if not garage:
            print(Fore.RED + "Error: No se pudo cargar el garage." + Style.RESET_ALL)
            return 0
        
        # Buscar la patente en el garage
        piso_idx, slot_id = buscar_por_patente(garage, patente)
        if (piso_idx, slot_id) == (-1, -1):
            print(Fore.RED + f"Error: Patente {patente} no encontrada." + Style.RESET_ALL)
            return 0
        
        # Obtener slot del garage
        slot = garage[piso_idx][slot_id - 1]  # slot_id comienza en 1
        
        # Obtener tipo de vehículo
        tipo_vehiculo = slot.get("tipo_vehiculo", 0)
        hora_entrada = slot.get("hora_entrada")
        
        # Obtener tarifa según tipo de vehículo
        precio_tarifa = _obtener_precio_tarifa(tipo_vehiculo, tarifa)
        if precio_tarifa is None:
            print(Fore.RED + "Error: No hay tarifa configurada para este tipo de vehículo." + Style.RESET_ALL)
            return 0
        
        # Verificar si es suscripción mensual
        es_mensual = slot.get("reservado_mensual", False)
        
        if es_mensual:
            # Tarifa mensual fija
            return precio_tarifa
        else:
            # Tarifa por horas
            if not hora_entrada:
                print(Fore.YELLOW + "Advertencia: No se encontró hora de entrada. Cobrando tarifa mínima." + Style.RESET_ALL)
                return precio_tarifa
            
            horas_transcurridas = _calcular_horas(hora_entrada, hora_salida)
            if horas_transcurridas < 1:
                horas_transcurridas = 1  # Mínimo 1 hora
            
            costo = precio_tarifa * horas_transcurridas
            return round(costo, 2)
    
    except Exception as e:
        print(Fore.RED + f"Error calculando costo: {e}" + Style.RESET_ALL)
        return 0


def _obtener_precio_tarifa(tipo_vehiculo, tarifa):
    """Busca el precio de tarifa según tipo de vehículo (diario).
    
    tipo_vehiculo: número (1=moto, 2=auto, 3=camioneta)
    tarifa: lista de listas [[garage_id, tipo, periodo_mensual, precio, ...], ...]
    Retorna: precio (float) o None si no existe
    """
    if not tarifa:
        return None
    
    for row in tarifa:
        # row[1] = tipo, row[2] = periodo_mensual, row[3] = precio
        try:
            tipo_tarifa = int(row[1]) if row[1] else 0
            es_diario = row[2].lower() == "false" if isinstance(row[2], str) else not row[2]
            
            if tipo_tarifa == tipo_vehiculo and es_diario:
                return float(row[3])
        except (ValueError, IndexError, AttributeError):
            continue
    
    return None


def _calcular_horas(hora_entrada, hora_salida):
    """Calcula horas transcurridas entre dos timestamps.
    
    Formato esperado: 'YYYY-MM-DD HH:MM'
    Retorna: número de horas (float)
    """
    try:
        # Extraer horas y minutos
        entrada_partes = hora_entrada.split(" ")
        salida_partes = hora_salida.split(" ")
        
        if len(entrada_partes) < 2 or len(salida_partes) < 2:
            return 0
        
        entrada_tiempo = entrada_partes[1].split(":")
        salida_tiempo = salida_partes[1].split(":")
        
        entrada_minutos = int(entrada_tiempo[0]) * 60 + int(entrada_tiempo[1])
        salida_minutos = int(salida_tiempo[0]) * 60 + int(salida_tiempo[1])
        
        minutos_transcurridos = salida_minutos - entrada_minutos
        
        # Si es negativo, asume que es día siguiente
        if minutos_transcurridos < 0:
            minutos_transcurridos += 24 * 60
        
        horas = minutos_transcurridos / 60
        return horas
    
    except (ValueError, IndexError):
        return 0
    
    
def registrar_salida_vehiculo(patente=None, tarifa=None):
    """
    Registra la salida de un vehículo del garage.
    - Lee garage desde cache
    - Busca patente
    - Calcula costo
    - Actualiza CSV
    """
    
    print(tarifa)
    try:
        # Leer garage_id desde cache
        cache_data = leer_estado_garage()
        if not cache_data or 'garage_id' not in cache_data:
            print(Fore.RED + "Error: No hay garage en cache." + Style.RESET_ALL)
            return False
        
        garage_id = cache_data['garage_id']
        
        # Leer garage desde CSV
        garage = get_garage_data(garage_id)
        if not garage:
            print(Fore.RED + "Error: No se pudo cargar el garage." + Style.RESET_ALL)
            return False
        
        # Pedir patente si no se proporciona
        if patente is None:
            patente = pedir_patente()
        
        print(f"Registrando salida para la patente: {patente}")
        
        # Buscar el vehículo en el garage
        found_slot = None
        found_piso_idx = None
        found_slot_idx = None
        
        for piso_idx, piso in enumerate(garage):
            for slot_idx, slot in enumerate(piso):
                if slot.get("patente") == patente and slot.get("ocupado"):
                    found_slot = slot
                    found_piso_idx = piso_idx
                    found_slot_idx = slot_idx
                    break
            if found_slot:
                break
        
        if not found_slot:
            print(Fore.RED + "Vehículo no encontrado." + Style.RESET_ALL)
            return False
        
        # Obtener hora de entrada
        hora_entrada = found_slot.get("hora_entrada")
        if not hora_entrada:
            print(Fore.RED + "Error: No se encontró la hora de entrada del vehículo." + Style.RESET_ALL)
            return False
        
        # Obtener hora de salida actual
        hora_salida = get_current_time_json()
        
        # Calcular costo
        costo = calcular_costo_de_estadia(patente, hora_salida, tarifa) if tarifa else 0
        print(f"Costo de estadía para {patente}: ${costo}")
        
        # Liberar el slot
        found_slot["patente"] = ""
        found_slot["ocupado"] = False
        found_slot["hora_entrada"] = None
        found_slot["tipo_vehiculo"] = 0
        
        # Actualizar CSV
        actualizar_csv_garage(garage_id, garage)
        
        print(Fore.GREEN + f"Salida registrada. Slot {found_slot.get('id')} liberado." + Style.RESET_ALL)
        clear_screen()
        
        return True
    
    except Exception as e:
        print(Fore.RED + f"Error registrando salida: {e}" + Style.RESET_ALL)
        return False


def actualizar_csv_garage(garage_id, garage):
    """
    Actualiza el CSV del garage con la estructura modificada.
    
    garage: lista de pisos con slots (diccionarios)
    """
    try:
        csv_path = f"files/garage-{garage_id}.csv"
        
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            # Escribir header
            f.write("slot_id,piso,tipo_slot,reservado_mensual,ocupado,patente,hora_entrada,tipo_vehiculo\n")
            
            # Escribir slots
            for piso_idx, piso in enumerate(garage):
                for slot in piso:
                    slot_id = slot.get("id", 0)
                    piso = slot.get("piso", piso_idx)
                    tipo_slot = slot.get("tipo_slot", 0)
                    reservado = slot.get("reservado_mensual", False)
                    ocupado = slot.get("ocupado", False)
                    patente = slot.get("patente", "")
                    hora_entrada = slot.get("hora_entrada", "")
                    tipo_vehiculo = slot.get("tipo_vehiculo", 0)
                    
                    f.write(f"{slot_id},{piso},{tipo_slot},{reservado},{ocupado},{patente},{hora_entrada},{tipo_vehiculo}\n")
        
        print(Fore.GREEN + f"Garage {garage_id} actualizado en CSV." + Style.RESET_ALL)
    
    except Exception as e:
        print(Fore.RED + f"Error actualizando CSV: {e}" + Style.RESET_ALL)

def salida_tipo_vehiculo(tipo_slot):
    """
    Convierte un valor numérico que representa el tipo de vehículo en una cadena de texto descriptiva.
    Si el tipo no es reconocido, retorna "Desconocido".
    """ 
# Diccionario de conversión tipo número -> texto
    if tipo_slot == 1:
        return "Moto"
    elif tipo_slot == 2:
        return "Auto"
    elif tipo_slot == 3:
        return "Camioneta"

    return "Desconocido"

def registrar_entrada_auto(garage):
    # Solicita la patente al usuario
    patente = pedir_patente()
    # Solicita el tipo de vehículo
    tipo_vehiculo = slot_utils.tipo_slot()

    # VALIDACIÓN: Verificar si la patente ya existe en el sistema
    posicion_existente = buscar_por_patente(garage, patente)
    if posicion_existente != (-1, -1):
        print(Fore.RED + f"Error: La patente {patente} ya está en el garage" + Style.RESET_ALL)
        return False

    # BÚSQUEDA: Buscar un espacio libre compatible
    piso, slot_id  = busqueda_espacio_libre(garage, tipo_vehiculo)
    if (piso, slot_id) == (-1, -1):
        print(Fore.RED + "Error: No hay espacio libre disponible para este tipo de vehículo." + Style.RESET_ALL)
        return False
    
    else:
        new_slot = {
            "slot_id": slot_id,
            "piso": piso, #no hace es necesario pero lo dejo para mantener la estructura
            "ocupado": True,
            "hora_entrada": get_current_time_json(),
            "tipo_slot": tipo_vehiculo, #no hace es necesario pero lo dejo para mantener la estructura
            "patente": patente,
            "tipo_vehiculo": tipo_vehiculo
        }
        # ACTUALIZACIÓN: Registrar el vehículo en el slot encontrado
        if actualizar_garage(garage_id=leer_estado_garage()['garage_id'], data=new_slot, bulk=False):
           print(Fore.GREEN + f"Vehículo {patente} registrado en el garage." + Style.RESET_ALL)
           print(Fore.GREEN + f"Puede estacionarlo en piso: {piso}, Slot ID: {slot_id}" + Style.RESET_ALL)
        else:
           print(Fore.RED + "Error actualizando el garage." + Style.RESET_ALL)
        clear_screen()
        return True 
    
def contar_por_tipo_vehiculo(garage=None, tipo_buscado=None):
    """Cuenta vehículos estacionados de un tipo (tipo_vehiculo_estacionado)."""
    datos = leer_garage_normalizado()
    count = 0
    for pisos in datos:
        count += sum(1 for slot in pisos if slot.get("ocupado") == True and slot.get("tipo_vehiculo") == tipo_buscado)
    return count

# CONFIGURACIÓN CONSTANTE DEL EDIFICIO
pisos = 4
filas_por_piso = 3
columnas_por_piso = 4
total_slots_por_piso = filas_por_piso * columnas_por_piso





# Agregar al final del archivo para pruebas

if __name__ == "__main__":
    # Prueba de calcular_costo_de_estadia
    
    # Simular datos en cache
    cache_data = {
        'garage_id': 2  # Asume que existe garage-1.csv
    }
    guardar_estado_garage(cache_data)
    
    # Datos de tarifa simulados (obtenidos desde CSV)
    # [garage_id, tipo, periodo_mensual, precio, moneda, descripcion]
    tarifa = [
        ['1', '1', 'False', '500', 'ARS', 'Moto diario'],
        ['1', '2', 'False', '1000', 'ARS', 'Auto diario'],
        ['1', '3', 'False', '1500', 'ARS', 'Camioneta diario'],
    ]
    
    # Prueba 1: Patente FAB123 (auto, tipo=2)
    print(Fore.CYAN + "\n=== PRUEBA 1: Buscar patente FAB123 ===" + Style.RESET_ALL)
    patente_buscar = "FAB123"
    hora_salida = "2025-11-01 16:30:00"  # Salida a las 16:59
    
    costo = calcular_costo_de_estadia(patente_buscar, hora_salida, tarifa)
    print(Fore.GREEN + f"Costo calculado para {patente_buscar}: ${costo}" + Style.RESET_ALL)
    
    # Prueba 2: Patente inexistente
    print(Fore.CYAN + "\n=== PRUEBA 2: Buscar patente inexistente ===" + Style.RESET_ALL)
    costo_inexistente = calcular_costo_de_estadia("XYZ999", hora_salida, tarifa)
    print(Fore.YELLOW + f"Costo para patente inexistente: ${costo_inexistente}" + Style.RESET_ALL)