import garage.slot_utils as slot_utils
from garage.mockdata import GARAGE, COSTOS
import random
from users.interaccion_usuario import pedir_patente
from garage.garage_util import * 

#! TODO MODULARIZAR CODIGO 
## En main solo debemos tener la logica de iniciarlizar el programa y de ahí se pueden llamar a los otros modulos

# FUNCIÓN PARA MOSTRAR ESTADÍSTICAS GENERALES DEL GARAGE

def registrar_salida_vehiculo(garage, patente):
    """
    devuelve True si se realizó la salida, False si no se encontró la patente.
    """
    # Busca la patente en todo el garage
    for piso in garage:
        for slot in piso:
            # Si encuentra la patente y el slot está ocupado
            if slot[3] == True and slot[1] == patente:
                slot[1] = ""      # Borra la patente
                slot[3] = False   # Marca como libre
                slot[5] = ""      # Borra la fecha de ingreso
                slot[6] = 0       # Borra el tipo de vehículo
                return True
    return False

# FUNCIÓN PARA MODIFICAR DATOS DE UN VEHÍCULO ESTACIONADO


def modificar_vehiculo(garage, patente, nuevo_tipo=None, nueva_patente=None):
    """
    devuelve True si se modificó, False si no se encontró la patente.
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

    if posicion == (-1, -1):
        print("No hay espacios disponibles para este tipo de vehículo")
        return False

    # ASIGNACIÓN: Obtener el slot y actualizarlo
    piso, slot_id = posicion
    slot = obtener_slot_por_id(garage, slot_id)

    if slot:
        # ACTUALIZACIÓN: Modifica todos los datos del slot
        slot[1] = patente                    # Asigna patente
        slot[3] = True                       # Marca como ocupado
        slot[5] = generar_fecha_aleatoria()  # Asigna fecha de entrada
        slot[6] = tipo_vehiculo              # Asigna tipo de vehículo
        print(f"Vehículo {patente} estacionado en Piso {piso}, Slot {slot_id}")
        return True

    return False

# FUNCIÓN AUXILIAR PARA GENERAR FECHAS ALEATORIAS


def generar_fecha_aleatoria():
    """Genera una fecha y hora aleatoria en formato 'YYYY-MM-DD HH:MM'"""
    year = "2025"
    # Genera mes, día, hora y minuto aleatorios con formato de 2 dígitos
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    return f"{year}-{month}-{day} {hour}:{minute}"

# FUNCIÓN PARA ELIMINAR UNA FILA COMPLETA DEL GARAGE


def eliminar_fila_por_valor(valor, garage=GARAGE):
    """Elimina la primera fila que contiene el valor dado"""
    # Recorre las filas (pisos) por índice
    for i in range(len(garage)):
        # Si encuentra el valor en la fila, la elimina
        if valor in garage[i]:
            del garage[i]
            return True
    return False


# FUNCIÓN ALTERNATIVA PARA INGRESAR PATENTES CON VALIDACIÓN
def ingresar_patente():
    """CORREGIDA - quité el parámetro que no se usaba"""
    while True:
        # Solicita patente al usuario
        patente = pedir_patente()
        # VALIDACIÓN: Verifica si ya existe
        if chequear_existencia_patente(patente):
            print("Error: La patente ya existe en el sistema.")
            continue
        # VALIDACIÓN: Verifica formato (3 letras + 3 números)
        if len(patente) == 6 and patente[:3].isalpha() and patente[3:].isdigit():
            return patente
        else:
            print("Error: Formato de patente invalido. Intente nuevamente.")

# FUNCIÓN PARA OBTENER INFORMACIÓN DE TODOS LOS VEHÍCULOS ESTACIONADOS


def acceder_a_info_de_patentes():
    datos = []
    # Recorre todo el garage
    for piso in GARAGE:
        for slot in piso:
            # Solo incluye slots ocupados (slot[3] = True)
            if slot[3]:
                datos.append(slot)
    return datos

# FUNCIÓN PARA VERIFICAR SI UNA PATENTE EXISTE


def chequear_existencia_patente(patente):
    """Chequea si la patente existe en el sistema"""
    # Usa la función buscar_por_patente para verificar existencia
    return buscar_por_patente(GARAGE, patente) != (-1, -1)

# FUNCIÓN PARA VERIFICAR SI UN VEHÍCULO TIENE SUSCRIPCIÓN MENSUAL


def es_subscripcion_mensual(patente):
    """Chequea si la subscripcion es mensual o diaria"""
    for piso in GARAGE:
        for slot in piso:
            # Si encuentra la patente en un slot ocupado
            if slot[1] == patente and slot[3]:
                return slot[4]  # Retorna el valor de reservado_mensual
    return False

# FUNCIÓN SIMPLE PARA VERIFICAR SI HAY ESPACIOS LIBRES


def chequear_espacio_libre(garage=GARAGE):
    """Chequea si hay espacio libre en el estacionamiento"""
    # Retorna True si hay al menos un espacio libre
    return contar_espacios_libres(garage) > 0

# FUNCIÓN PARA BUSCAR INFORMACIÓN COMPLETA DE UNA PATENTE


def buscar_patente(patente):
    """Busca información completa de una patente"""
    for piso in GARAGE:
        for slot in piso:
            # Si encuentra la patente en un slot ocupado, retorna todo el slot
            if slot[1] == patente and slot[3]:
                return slot
    return None

# FUNCIÓN PARA CALCULAR EL COSTO DE ESTADÍA DE UN VEHÍCULO


def calcular_costo_de_estadia(patente, hora_salida):
    """Calcula costo de estadía"""
    # Obtiene la información completa del vehículo
    info_patente = buscar_patente(patente)
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


def salida_tipo_vehiculo(tipo_slot):
    """Convierte tipo numérico a texto"""
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


# CONFIGURACIÓN CONSTANTE DEL EDIFICIO
pisos = 4
filas_por_piso = 3
columnas_por_piso = 4
total_slots_por_piso = filas_por_piso * columnas_por_piso
