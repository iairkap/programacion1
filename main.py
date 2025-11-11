import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import garage.slot_utils as slot_utils
import random
from users.interaccion_usuario import (pedir_patente, configuracion_diario_mensual)
from garage.garage_util import buscar_por_patente, buscar_espacio_libre, chequear_existencia_patente
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



def ingresar_patente():
    """
    Solicita y valida una patente nueva que no exista en el sistema.
    Usa pedir_patente() para validar formato y solo verifica existencia.
    """
    garage = leer_garage_normalizado()
    while True:
        try:
            patente = pedir_patente()  # Ya valida formato completo (6 o 7 dígitos)
            if chequear_existencia_patente(patente, garage):
                print(Fore.RED + "Error: La patente ya existe en el sistema." + Style.RESET_ALL)
                continue
            print(Fore.GREEN + "Patente válida ingresada." + Style.RESET_ALL)
            return patente
        except Exception as e:
            print(Fore.RED + f"Error procesando la patente: {e}. Intente nuevamente." + Style.RESET_ALL)

def acceder_a_info_de_patentes(garage):
    """Devuelve lista de dicts con slots ocupados."""
    datos = garage
    return [slot for slot in datos if slot.get("ocupado") == True]


def registrar_salida_vehiculo(patente=None, tarifa=None):
    """
    Registra la salida de un vehículo del garage.
    - Lee garage desde cache
    - Busca patente
    - Calcula costo
    - Actualiza CSV
    """
    
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
        
        # Calcular costo usando la función de garage/precios.py
        costo = calcular_costo_de_estadia(patente, hora_salida, garage=garage, tarifa=tarifa)
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


def contar_por_tipo_vehiculo(garage=None, tipo_buscado=None):
    """Cuenta vehículos estacionados de un tipo (tipo_vehiculo_estacionado)."""
    datos = leer_garage_normalizado()
    count = 0
    for pisos in datos:
        count += sum(1 for slot in pisos if slot.get("ocupado") == True and slot.get("tipo_vehiculo") == tipo_buscado)
    return count

def registrar_entrada_auto(garage):
    # Solicita la patente al usuario
    patente = pedir_patente()
    # Solicita el tipo de vehículo
    tipo_vehiculo = slot_utils.tipo_slot()
    
    es_mensual = configuracion_diario_mensual()

    # VALIDACIÓN: Verificar si la patente ya existe en el sistema
    posicion_existente = buscar_por_patente(garage, patente)
    if posicion_existente != (-1, -1):
        print(Fore.RED + f"Error: La patente {patente} ya está en el garage" + Style.RESET_ALL)
        return False

    # BÚSQUEDA: Buscar un espacio libre compatible
    piso, slot_id = buscar_espacio_libre(garage, tipo_vehiculo)
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
            "reservado_mensual": es_mensual,
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