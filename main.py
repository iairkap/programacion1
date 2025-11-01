import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import garage.slot_utils as slot_utils
import random
from users.interaccion_usuario import pedir_patente
import garage.garage_util as garage_util
from users import users_garage

from users.users_garage import (    
                crear_archivo_users_garage, 
                get_garage_data,
                actualizar_garage)
from cache.json import leer_estado_garage, guardar_estado_garage

from colorama import Fore, Style
from garage.precios import (configurar_precios, es_subscripcion_mensual,
                            buscar_por_patente, calcular_costo_de_estadia)

from auxiliares.date import get_current_time_json
from auxiliares.consola import clear_screen

def leer_garage_normalizado():
    """
    Lee el garage y retorna una lista de diccionarios normalizados.
    Cada slot esta representado como un diccionario 
    """
    garage_id = leer_estado_garage()['garage_id']
    return users_garage.get_garage_data(garage_id)

"""
    def registrar_salida_vehiculo(garage=None, patente=None):
    Registra la salida de un vehículo del garage.
    Busca en la lista de slots del garage el vehículo con la patente especificada y marca el slot como libre,
    limpiando los datos asociados al vehículo estacionado. Si hay duplicados, solo limpia el primero encontrado
    datos = garage
    actualizado = False

    for slot in datos:
        if slot.get("patente") == patente and slot.get("ocupado") == "True":
            slot["patente"] = ""
            slot["ocupado"] = "False"
            slot["hora_entrada"] = ""
            slot["tipo_vehiculo_estacionado"] = "0"
            actualizado = True
            break

    return actualizado  # True si modificó algún slot, False si no encontró

    """








def modificar_vehiculo(garage, patente, nuevo_tipo=None, nueva_patente=None):
    """
    Modifica los datos de un vehículo en el garage según la patente.
    Busca el vehículo por su patente en la estructura garage y actualiza el tipo de vehículo y/o la patente si se proporcionan nuevos valores.
    """
    # Busca el vehículo por patente
    for piso in garage:
        for slot in piso:
            if slot["ocupado"] == True and slot["patente"] == patente:
                # Modifica solo los campos que no son None
                if nuevo_tipo is not None:
                    slot["tipo_vehiculo_estacionado"] = nuevo_tipo        # Cambia tipo de vehículo
                if nueva_patente is not None:
                    slot["patente"] = nueva_patente     # Cambia patente
                return True
    return False

def buscar_por_patente(garage, patente = None):
    """ 
    Busca la patente en la estructura de garage.
    Si encuentra, retorna (piso_idx, slot_id), si no, retorna (-1, -1).
    """
    for idx_piso, piso in enumerate(garage):
        for slot in piso:
            try:
                patente_slot = slot["patente"]
                ocupado_slot = slot["ocupado"]
                if patente_slot == patente and ocupado_slot == True:
                    piso_val = int(slot["piso"]) if "piso" in slot else idx_piso
                    id_val = int(slot["id"]) if "id" in slot else 0
                    return (piso_val, id_val)
            except Exception:
                try:
                    if len(slot) > 1 and slot["patente"] == patente and len(slot) > 3 and slot["ocupado"] == True:
                        return (idx_piso, slot["id"])
                except Exception:
                    continue
    return (-1, -1)


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



# FUNCIÓN PARA CALCULAR EL COSTO DE ESTADÍA DE UN VEHÍCULO ||||||| MODIFICAR PORQUE GARAGE YA NO 
'manejo de errores'
def calcular_costo_de_estadia(patente, hora_salida):

    print(patente)
    
    info_patente = buscar_por_patente(GARAGE, patente)
    
    if not info_patente:
        return 0
    tipo_de_slot = info_patente[6] 
    
    # tipo_vehiculo_estacionado
    
    
    """ # Obtiene la información completa del vehículo
    


    # CÁLCULO: Diferencia entre suscripción mensual y por horas
    if not es_subscripcion_mensual(patente):
        # CÁLCULO POR HORAS: Si tiene hora de entrada registrada
        if info_patente[5]:
            try:
                # Extrae la hora de entrada y la convierte a minutos
                min_entrada = info_patente[5].split(" ")[1].replace(":", "")
                min_transcurridos = int(
                    hora_salida.replace(":", "")) - int(min_entrada)
                # Calcula horas transcurridas (mínimo 1 hora)
                horas_transcurridas = max(
                    1, min_transcurridos / 100)
                # Multiplica por tarifa por hora del tipo de vehículo
                costo = COSTOS[tipo_de_slot][0] * horas_transcurridas
                return round(costo, 2)
            except:
                # Si hay error, cobra tarifa mínima
                return COSTOS[tipo_de_slot][0]
    else:
        # SUSCRIPCIÓN MENSUAL: Cobra tarifa fija mensual
        return COSTOS[tipo_de_slot][1] """

    return 0

# FUNCIÓN COMPLETA PARA REGISTRAR SALIDA CON CÁLCULO DE COSTO

#funcion para registrar salida de vehiculo en formato diccionario 
'modificado a logica diccionario, manejo de errores y doctring'
def registrar_salida_vehiculo(garage=None, patente=None, tarifa = None):
  
    datos = leer_garage_normalizado()    
    if patente is None:
        patente = pedir_patente()
        
    print(f"Registrando salida para la patente: {patente}")

    # Buscar el slot en la vista de diccionarios
    found = None
    for piso in datos:
       for slot in piso:
           if slot.get("patente") == patente and slot.get("ocupado") == True:
               found = slot
               break

    if not found:
        print(Fore.RED + "Vehículo no encontrado." + Style.RESET_ALL)
        return False

    # Solicita hora de salida para calcular costo
    hora_entrada = found.get("hora_entrada")
    hora_salida = get_current_time_json()
   
    if not hora_entrada:
        print(Fore.RED + "Error: No se encontró la hora de entrada del vehículo." + Style.RESET_ALL)
        return False
    

    
    costo = calcular_costo_de_estadia(patente, hora_salida)
   
  
    # Muestra el costo
    print(f"Costo de estadía para {patente}: ${costo}")

    # Actualiza la vista de diccionarios
    found["patente"] = ""
    found["ocupado"] = False
    found["hora_entrada"] = ""
    found["tipo_vehiculo_estacionado"] = ""

    # Intenta sincronizar con la estructura anidada GARAGE
    try:
        piso_idx = int(found.get("piso", 0))
        slot_id = found.get("id")
    except Exception:
        piso_idx = None
        slot_id = None

    if piso_idx is None or slot_id is None:
        # No podemos sincronizar, pero la vista quedó actualizada
        return True

    if piso_idx < 0 or piso_idx >= len(GARAGE):
        return True

    target_index = None
    for i, s in enumerate(GARAGE[piso_idx]):
        try:
            current_id = s[0]
        except Exception:
            continue
        if str(current_id) == str(slot_id):
            target_index = i
            break

    if target_index is None:
        return True

    slot_ref = GARAGE[piso_idx][target_index]
    if type(slot_ref) is tuple:
        slot_ref = list(slot_ref)

    if type(slot_ref) in (list, ):
        while len(slot_ref) < 7:
            slot_ref.append(None)

        slot_ref[1] = ""        # Borra patente
        slot_ref[3] = False      # Marca como libre
        slot_ref[5] = None       # Borra fecha de entrada
        slot_ref[6] = 0          # Borra tipo de vehículo

        GARAGE[piso_idx][target_index] = slot_ref

        print(f"Salida registrada. Piso {piso_idx}, Slot {slot_id} liberado.")
        return True

    return True

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
        input(Fore.YELLOW + '\nPresione cualquier tecla para continuar...' + Style.RESET_ALL)
        clear_screen()
        return True 

def obtener_id_por_posicion(garage, piso_idx, slot_idx):
    """Obtiene el ID del slot dado su piso y posición en el piso."""
    try:
        slot = garage[piso_idx][slot_idx]
        return int(slot["id"])
    except Exception:
        return None
    
def contar_por_tipo_vehiculo(garage=None, tipo_buscado=None):
    """Cuenta vehículos estacionados de un tipo (tipo_vehiculo_estacionado)."""
    datos = leer_garage_normalizado()
    count = 0
    for pisos in datos:
        count += sum(1 for slot in pisos if slot.get("ocupado") == True and slot.get("tipo_vehiculo_estacionado") == tipo_buscado)
    return count

# CONFIGURACIÓN CONSTANTE DEL EDIFICIO
pisos = 4
filas_por_piso = 3
columnas_por_piso = 4
total_slots_por_piso = filas_por_piso * columnas_por_piso



