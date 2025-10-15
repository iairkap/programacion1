import garage.slot_utils as slot_utils
from garage.mockdata import GARAGE, COSTOS
import random
from users.interaccion_usuario import pedir_patente
import garage.garage_util as garage_util
import auxiliares.date

#funcion para leer garage 
'logica diccionario, manejo de errores y doctring, '
def leer_garage():
    """
    Recorre la estructura global GARAGE y retorna una lista de diccionarios normalizados
    representando cada slot de estacionamiento.
    Cada slot puede estar representado como un diccionario o como una lista/tupla.
    """
    resultados = []
    for piso_idx, piso in enumerate(GARAGE):
        for slot in piso:
            # asumimos slot como lista/tupla en la forma esperada [id, patente, tipo_slot, ocupado, reservado, hora, tipo_veh]
            if type(slot) is dict:
                s = dict(slot)
                s["piso"] = str(s["piso"]) if "piso" in s else str(piso_idx)
                s["id"] = str(s["id"]) if "id" in s else "0"
                s["patente"] = "" if ("patente" not in s or s["patente"] is None) else str(s["patente"])
                s["tipo_slot"] = str(s["tipo_slot"]) if "tipo_slot" in s else "0"
                s["ocupado"] = "True" if ("ocupado" in s and s["ocupado"]) else "False"
                s["reservado_mensual"] = "True" if ("reservado_mensual" in s and s["reservado_mensual"]) else "False"
                s["hora_entrada"] = "" if ("hora_entrada" not in s or not s["hora_entrada"]) else str(s["hora_entrada"])
                s["tipo_vehiculo_estacionado"] = str(s["tipo_vehiculo_estacionado"]) if "tipo_vehiculo_estacionado" in s else "0"
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

            
            continue

    return resultados


#! TODO MODULARIZAR CODIGO
## En main solo debemos tener la logica de iniciarlizar el programa y de ahí se pueden llamar a los otros modulos

# FUNCIÓN PARA MOSTRAR ESTADÍSTICAS GENERALES DEL GARAGE

#funcion para registrar salida de vehiculo en formato diccionario 
'logica diccionario y manejo de errores'
def registrar_salida_vehiculo(garage=None, patente=None):
    """
    Registra la salida de un vehículo del garage.
    Busca en la lista de slots del garage el vehículo con la patente especificada y marca el slot como libre,
    limpiando los datos asociados al vehículo estacionado. Si hay duplicados, solo limpia el primero encontrado
    """
    datos = garage if garage is not None else leer_garage()
    actualizado = False

    for slot in datos:
        if slot.get("patente") == patente and slot.get("ocupado") == "True":
            slot["patente"] = ""
            slot["ocupado"] = "False"
            slot["hora_entrada"] = ""
            slot["tipo_vehiculo_estacionado"] = "0"
            actualizado = True
            # no hacemos break para limpiar duplicados si hubiese; si prefieres break, descomenta:
            break

    return actualizado  # True si modificó algún slot, False si no encontró






# FUNCIÓN PARA MODIFICAR DATOS DE UN VEHÍCULO ESTACIONADO
'doctring'
def modificar_vehiculo(garage, patente, nuevo_tipo=None, nueva_patente=None):
    """
    Modifica los datos de un vehículo en el garage según la patente.
    Busca el vehículo por su patente en la estructura garage y actualiza el tipo de vehículo y/o la patente si se proporcionan nuevos valores.
    """
    # Busca el vehículo por patente
    for piso in garage:
        for slot in piso:
            if slot[3] == True and slot[1] == patente:
                # Modifica solo los campos que no son None
                if nuevo_tipo is not None:
                    slot[6] = nuevo_tipo        # Cambia tipo de vehículo
                if nueva_patente is not None:
                    slot[1] = nueva_patente     # Cambia patente
                return True
    return False



'menejo de errores'
def buscar_por_patente(garage, patente):
    """
    Busca la patente en la estructura de garage.
    Si encuentra, retorna (piso_idx, slot_id), si no, retorna (-1, -1).
    """
    for idx_piso, piso in enumerate(garage):
        for slot in piso:
            # Si slot es dict (tiene método 'get')
            try:
                patente_slot = slot["patente"]
                ocupado_slot = slot["ocupado"]
                if patente_slot == patente and ocupado_slot == "True":
                    piso_val = int(slot["piso"]) if "piso" in slot else idx_piso
                    id_val = int(slot["id"]) if "id" in slot else 0
                    return (piso_val, id_val)
            except Exception:
                # Si no es dict, intentamos como lista/tupla
                try:
                    if len(slot) > 1 and slot[1] == patente and len(slot) > 3 and slot[3]:
                        return (idx_piso, slot[0])
                except Exception:
                    continue
    return (-1, -1)




# FUNCIÓN AUXILIAR PARA GENERAR FECHAS ALEATORIAS
def generar_fecha_aleatoria():
    """Genera una fecha y hora aleatoria en formato 'YYYY-MM-DD HH:MM'"""
    year = "2025"
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    return f"{year}-{month}-{day} {hour}:{minute}"



# FUNCIÓN PARA ELIMINAR UNA FILA COMPLETA DEL GARAGE
'agregue manejo de errores'
def eliminar_fila_por_valor(valor, garage=GARAGE):
    """Elimina la primera fila que contiene el valor dado, con manejo de errores."""
    try:
        for i in range(len(garage)):
            if valor in garage[i]:
                del garage[i]
                return True
    except Exception as e:
        print(f"Error eliminando fila: {e}")
        return False
    return False



# FUNCIÓN ALTERNATIVA PARA INGRESAR PATENTES CON VALIDACIÓN
'manejo de errores'
def ingresar_patente():
    """Solicita y valida una patente, con manejo de errores."""
    while True:
        try:
            patente = pedir_patente()
            if chequear_existencia_patente(patente):
                print("Error: La patente ya existe en el sistema.")
                continue
            if len(patente) == 6 and patente[:3].isalpha() and patente[3:].isdigit():
                return patente
            else:
                print("Error: Formato de patente inválido. Intente nuevamente.")
        except Exception as e:
            print(f"Error procesando la patente: {e}. Intente nuevamente.")

# FUNCIÓN PARA OBTENER INFORMACIÓN DE TODOS LOS VEHÍCULOS ESTACIONADOS


#funcion para acceder a info de patentes en formato diccionario
'modificado a logica diccionario '
def acceder_a_info_de_patentes(garage=None):
    """Devuelve lista de dicts con slots ocupados."""
    datos = garage if garage is not None else leer_garage()
    return [slot for slot in datos if slot.get("ocupado") == "True"]



# FUNCIÓN PARA VERIFICAR SI UNA PATENTE EXISTE
'modificado a logica diccionario '
def chequear_existencia_patente(patente, garage=None):
    """Devuelve True si la patente existe y está ocupada."""
    datos = garage if garage is not None else leer_garage()
    for slot in datos:
        if slot["patente"] == patente and slot["ocupado"] == "True":
            return True
    return False


# FUNCIÓN PARA VERIFICAR SI UN VEHÍCULO TIENE SUSCRIPCIÓN MENSUAL
'modificado a logica diccionario '
def es_subscripcion_mensual(patente, garage=None):
    """Chequea si la subscripcion es mensual usando la vista de diccionarios.

    Retorna True si el slot tiene `reservado_mensual` == "True" o es True.
    """
    datos = garage if garage is not None else leer_garage()
    for slot in datos:
        if slot["patente"] == patente and slot["ocupado"] == "True":
            val = slot["reservado_mensual"]
            # Normalizar distintos tipos (str "True"/"False" o booleano)
            if type(val) is str:
                return val == "True"
            return bool(val)
    return False

# FUNCIÓN SIMPLE PARA VERIFICAR SI HAY ESPACIOS LIBRES
'modifcado a logica diccionario '
def busqueda_espacio_libre(garage=None, tipo_vehiculo=None):
    datos = garage if garage is not None else leer_garage()
    for slot in datos:
        if slot["ocupado"] == "False":
            if tipo_vehiculo is None or slot["tipo_slot"] == str(tipo_vehiculo) or slot["tipo_slot"] == "4":
                piso_val = int(slot["piso"]) if "piso" in slot else 0
                id_val = int(slot["id"]) if "id" in slot else 0
                return (piso_val, id_val)
    return (-1, -1)



# FUNCIÓN PARA CONTAR ESPACIOS LIBRES
'modificado a logica diccionario y doctring'
def contar_espacios_libres(garage=None):
    """
    Cuenta la cantidad de espacios libres en el garage.
    Cuenta slots con 'ocupado' == 'False'.
    """
    datos = garage if garage is not None else leer_garage()
    return sum(1 for slot in datos if slot["ocupado"] == "False")



# FUNCIÓN PARA CALCULAR EL COSTO DE ESTADÍA DE UN VEHÍCULO
'manejo de errores'
def calcular_costo_de_estadia(patente, hora_salida):
    """
    Calcula el costo de estadía de un vehículo en el garage según su patente y la hora de salida.
    Si el vehículo no tiene suscripción mensual, calcula el costo en base a las horas transcurridas desde la hora de entrada
    hasta la hora de salida, aplicando la tarifa por hora correspondiente al tipo de vehículo. Si ocurre un error en el cálculo,
    se cobra la tarifa mínima por hora.
    Si el vehículo tiene suscripción mensual, se cobra la tarifa fija mensual correspondiente al tipo de vehículo.
    """
    # Obtiene la información completa del vehículo
    info_patente = buscar_por_patente(GARAGE, patente)
    if not info_patente:
        return 0

    tipo_de_slot = info_patente[6]  # tipo_vehiculo_estacionado

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
        return COSTOS[tipo_de_slot][1]

    return 0

# FUNCIÓN COMPLETA PARA REGISTRAR SALIDA CON CÁLCULO DE COSTO

#funcion para registrar salida de vehiculo en formato diccionario 
'modificado a logica diccionario, manejo de errores y doctring'
def registrar_salida_vehiculo(garage=None, patente=None):
    """
    Registra la salida de un vehículo del garage, actualizando tanto la vista de diccionarios como la estructura anidada GARAGE.
    """
    datos = garage if garage is not None else leer_garage()

    if patente is None:
        patente = pedir_patente()

    # Buscar el slot en la vista de diccionarios
    found = None
    for slot in datos:
        if slot.get("patente") == patente and slot.get("ocupado") == "True":
            found = slot
            break

    if not found:
        print("Vehículo no encontrado.")
        return False

    # Solicita hora de salida para calcular costo
    hora_salida = input("Ingrese hora de salida (HH:MM): ").strip()
    try:
        costo = calcular_costo_de_estadia(patente, hora_salida)
    except Exception:
        costo = 0

    # Muestra el costo
    print(f"Costo de estadía para {patente}: ${costo}")

    # Actualiza la vista de diccionarios
    found["patente"] = ""
    found["ocupado"] = "False"
    found["hora_entrada"] = ""
    found["tipo_vehiculo_estacionado"] = "0"

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

""" 
def registrar_salida_vehiculo(garage):
    # Solicita patente al usuario
    patente = pedir_patente()
    # Busca la posición del vehículo
    pos = buscar_por_patente(garage, patente)
    if pos == (-1, -1):
        print("Vehículo no encontrado.")
        return False

    # Solicita hora de salida para calcular costo
    hora_salida = input("Ingrese hora de salida (HH:MM): ").strip()
    costo = calcular_costo_de_estadia(patente, hora_salida)

    piso_idx, slot_id = pos
    # LIBERACIÓN: Busca el slot específico y lo libera
    for slot in garage[piso_idx]:
        if slot[0] == slot_id:
            # Muestra el costo antes de liberar
            print(f"Costo de estadía para {patente}: ${costo}")
            # ACTUALIZACIÓN: Libera el slot
            slot[1] = ""        # Borra patente
            slot[3] = False     # Marca como libre
            slot[5] = None      # Borra fecha de entrada
            slot[6] = 0         # Borra tipo de vehículo
            print(
                f"Salida registrada. Piso {piso_idx}, Slot {slot_id} liberado.")
            return True

    print("Error interno liberando el slot.")
    return False """

# FUNCIÓN AUXILIAR PARA CONVERTIR TIPOS NUMÉRICOS A TEXTO

#funcion para convertir tipo numerico a texto
'dosctring'
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
    elif tipo_slot == 4:
        return "Bicicleta"
    return "Desconocido"


#funciones viejas -> Actualizar 



# FUNCIÓN PRINCIPAL PARA REGISTRAR ENTRADA DE VEHÍCULOS
def registrar_entrada_auto(garage):
    # Solicita la patente al usuario
    patente = pedir_patente()
    # Solicita el tipo de vehículo
    tipo_vehiculo = slot_utils.tipo_slot()

    # VALIDACIÓN: Verificar si la patente ya existe en el sistema
    posicion_existente = buscar_por_patente(garage, patente)
    if posicion_existente != (-1, -1):
        print(f"Error: La patente {patente} ya está en el garage")
        return False

    # BÚSQUEDA: Buscar un espacio libre compatible
    posicion = busqueda_espacio_libre(garage, tipo_vehiculo)

def contar_por_tipo_vehiculo(garage=None, tipo_buscado=None):
    """Cuenta vehículos estacionados de un tipo (tipo_vehiculo_estacionado)."""
    datos = garage if garage is not None else leer_garage()
    return sum(1 for slot in datos if slot.get("ocupado") == "True" and slot.get("tipo_vehiculo_estacionado") == str(tipo_buscado))

# CONFIGURACIÓN CONSTANTE DEL EDIFICIO
pisos = 4
filas_por_piso = 3
columnas_por_piso = 4
total_slots_por_piso = filas_por_piso * columnas_por_piso
