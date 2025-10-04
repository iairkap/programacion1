# Representación del garage: lista de pisos (matrices)
# Cada elemento es: [id, patente, tipo_slot, ocupado, reservado_mensual, hora_entrada, tipo_vehiculo_estacionado]
# tipo_slot: 1=moto, 2=auto, 3=camioneta, 4=multi (acepta cualquiera)
# ocupado: True/False
# reservado_mensual: True/False
# hora_entrada: timestamp o None si está vacío
# tipo_vehiculo_estacionado: 1=moto, 2=auto, 3=camioneta, 4=bici, 0=vacío

import garage.slot_utils as slot_utils
from garage.mockdata import GARAGE, COSTOS
import random

#! TODO MODULARIZAR CODIGO -> MUCHA REPETICION DE FOR y de los bucles

def busqueda_espacio_libre(tipo_vehiculo, garage=GARAGE):
    for piso, piso_data in enumerate(garage):
        for fila, fila_data in enumerate(piso_data):
            for columna, slot in enumerate(fila_data):
                if not slot[3] and (slot[2] == tipo_vehiculo or slot[2] == 4):
                    return (piso, fila, columna)
    return (-1, -1, -1)

def buscar_por_patente(garage, patente_buscada):
    for piso, piso_data in enumerate(garage):
        for fila, fila_data in enumerate(piso_data):
            for columna, slot in enumerate(fila_data):
                if slot[1] == patente_buscada and slot[3]:
                    return (piso, fila, columna)
    return (-1, -1, -1)

def contar_espacios_libres(garage):
    return sum(
        not slot[3]
        for piso_data in garage
        for fila_data in piso_data
        for slot in fila_data
    )

def contar_por_tipo_vehiculo(garage, tipo_buscado):
    return sum(
        slot[6] == tipo_buscado and slot[3]
        for piso_data in garage
        for fila_data in piso_data
        for slot in fila_data
    )

def ingresar_auto_matriz(garage):
    patente = input("Agrega el nro de patente: ")
    tipo_vehiculo = slot_utils.tipo_slot()

    # Verificar si la patente ya existe
    posicion_existente = buscar_por_patente(garage, patente)
    if posicion_existente != (-1, -1, -1):
        print(f"Error: La patente {patente} ya está en el garage")
        return False

    # Buscar espacio libre
    posicion = busqueda_espacio_libre(garage, tipo_vehiculo)

    if posicion == (-1, -1, -1):
        print("No hay espacios disponibles para este tipo de vehículo")
        return False

    piso, fila, columna = posicion

    actualizar_slot(patente, tipo_vehiculo, piso, fila, columna, garage)
    print(
        f"Vehículo {patente} estacionado en Piso {piso}, Fila {fila}, Columna {columna}")
    return True

def generar_fecha_aleatoria():
    """Genera una fecha y hora aleatoria en formato 'YYYY-MM-DD HH:MM'"""
    year = "2025"
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    return f"{year}-{month}-{day} {hour}:{minute}"

def eliminar_fila_por_valor(valor, garage=GARAGE):
    """Elimina la primera fila que contiene el valor dado"""
    for i, fila in enumerate(garage):
        if valor in fila:
            del garage[i]
            return True
    return False

# ? Actualizar el slot


# TODO VALIDAR INGRESO DE PATENTE

def ingresar_patente(patente):
    if chequear_existencia_patente(patente):
        print("Error: La patente ya existe en el sistema.")
        return None
    while True:
        patente = input("Ingrese la patente (3 letras y 3 numeros, ej: ABC123): ").strip().upper()
        if len(patente) == 6 and patente[:3].isalpha() and patente[3:].isdigit():
            return patente
        else:
            print("Error: Formato de patente invalido. Intente nuevamente.")

def salida_tipo_vehiculo(tipo_slot):
    salida = ""
    if tipo_slot == 1:
        salida = "Moto"
    elif tipo_slot == 2:
        salida = "Auto"
    elif tipo_slot == 3:
        salida = "Camioneta"
    return salida

def busqueda_espacio_libre(garage, tipo_slot):
    for piso in range(len(garage)):
        for fila in range(len(garage[piso])):
            for columna in range(len(garage[piso][fila])):
                slot = garage[piso][fila][columna]
                if not slot[3]:  # Si no está ocupado
                    if slot[2] == tipo_slot or slot[2] == 4:  # Si el tipo de slot es adecuado
                        return (piso, fila, columna)
    return None  # No se encontró espacio libre


# ? MENU PRINCIPAL

def acceder_a_info_de_patentes():
    """Accede a los datos guardados de las patentes
    retorna la info de todas la petentes en el sistema"""
    datos = []
    for d in GARAGE:
        for pisos in d:
            datos.append(pisos)
    return datos


# ? REGISTRO DE AUTO
# ? Verificar si la patente ya existe
def chequear_existencia_patente(patente):
    """Chequea si la patente existe en el sistema
    retorna True si existe, else False"""
    info_patentes = acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
                return True
    return False

# ? Consultar si es mensual o diairio
def es_subscripcion_mensual(patente):
    """Chequea si la subscripcion es mensual o diaria"""
    info_patentes = acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
            return info[3] 

# ? Buscar espacio libre
def chequear_espacio_libre(garage = GARAGE):
    """Chequea si hay espacio libre en el estacionamiento"""
    for piso_idx, piso in enumerate(garage):
        if len(piso) < 12:
            fila = piso[-1][0] + 1
            return (piso_idx, fila) ##Falta retornar algun dato mas??


# ? Mostrar mensaje de éxito o error
# ? REGISTRO SALIDA DE AUTO
# ? Ingresar patente a buscar
def buscar_patente(patente):
    info_patentes= acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
            return info
# ? Buscar la patente en el garage
# ? Si no se encuentra, mostrar mensaje de error
# ? Si se encuentra, calcular el tiempo y costo
def calcular_costo_de_estadia(patente, hora_salida):
    info_patente = buscar_patente(patente)
    costo = 0
    if not info_patente:
        return "Patente no registrada"
    tipo_de_slot = info_patente[-1]
    if not es_subscripcion_mensual(patente):
        min_entrada = info_patente[-2].split(" ")[1].replace(":", "")
        min_transcurridos = int(hora_salida.replace(":", "")) - int(min_entrada)
        horas_transcurridas = min_transcurridos / 60
        print(f"Horas transcurridas: {horas_transcurridas}")
        costo = COSTOS[tipo_de_slot][0] * horas_transcurridas
    else:
        costo = COSTOS[tipo_de_slot][1] ### Debemos agregar la {ultima fecha de pago??? 
    return costo
    
# ? Actualizar el slot
# ? Mostrar mensaje de éxito con el costo


#! SLOTS LIBRES POR PISO + Por garage en general + Por tipo de vehiculo
#! Ingresar el piso a consultar
#! Validar el piso
#! Mostrar la cantidad de slots libres en ese piso
#! Mostrar mensaje de error si el piso no es válido

#! CANTIDAD DE AUTOS, MOTOS Y CAMIONETAS ESTACIONADOS
#! Contar la cantidad de cada tipo de vehículo en el garage
#! Mostrar los resultados


#! Funcion para salida linda de lectura tipo de garage

#!REUBICAR AUTO
#! Ingresar patente a buscar
#! Buscar la patente en el garage
#! Si no se encuentra, mostrar mensaje de error
#! Si se encuentra, buscar un nuevo espacio libre del mismo tipo
#! Si no hay espacio libre, mostrar mensaje de error
#! Si hay espacio libre, actualizar ambos slots (el antiguo y el nuevo)
#! Mostrar mensaje de éxito con la nueva ubicación

# Configuración del edificio
pisos = 4
filas_por_piso = 3
columnas_por_piso = 4
total_slots_por_piso = filas_por_piso * columnas_por_piso