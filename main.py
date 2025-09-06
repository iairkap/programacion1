# Representación del garage: lista de pisos (matrices)
# Cada elemento es: [id, patente, tipo_slot, ocupado, reservado_mensual, hora_entrada, tipo_vehiculo_estacionado]
# tipo_slot: 1=moto, 2=auto, 3=camioneta, 4=multi (acepta cualquiera)
# ocupado: True/False
# reservado_mensual: True/False
# hora_entrada: timestamp o None si está vacío
# tipo_vehiculo_estacionado: 1=moto, 2=auto, 3=camioneta, 4=bici, 0=vacío

import funciones


#! TODO MODULARIZAR CODIGO -> MUCHA REPETICION DE FOR y de los bucles

def busqueda_espacio_libre(garage, tipo_vehiculo):
    for piso in range(len(garage)):
        for fila in range(len(garage[piso])):
            for columna in range(len(garage[piso][fila])):
                slot = garage[piso][fila][columna]
                if slot[3] == False:
                    if slot[2] == tipo_vehiculo or slot[2] == 4:
                        return (piso, fila, columna)
    return (-1, -1, -1)


def buscar_por_patente(garage, patente_buscada):
    for piso in range(len(garage)):
        for fila in range(len(garage[piso])):
            for columna in range(len(garage[piso][fila])):
                slot = garage[piso][fila][columna]
                if slot[1] == patente_buscada and slot[3] == True:
                    return (piso, fila, columna)
    return (-1, -1, -1)


def contar_espacios_libres(garage):
    contador = 0
    for piso in range(len(garage)):
        for fila in range(len(garage[piso])):
            for columna in range(len(garage[piso][fila])):
                slot = garage[piso][fila][columna]
                if slot[3] == False:
                    contador += 1
    return contador


def contar_por_tipo_vehiculo(garage, tipo_buscado):
    contador = 0
    for piso in range(len(garage)):
        for fila in range(len(garage[piso])):
            for columna in range(len(garage[piso][fila])):
                slot = garage[piso][fila][columna]
                if slot[6] == tipo_buscado and slot[3] == True:
                    contador += 1
    return contador


def ingresar_auto_matriz(garage):
    patente = input("Agrega el nro de patente: ")
    tipo_vehiculo = funciones.tipo_slot()

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
    slot = garage[piso][fila][columna]

    # Actualizar el slot
    slot[1] = patente
    slot[3] = True
    slot[5] = "2025-09-06 14:30"
    slot[6] = tipo_vehiculo

    print(
        f"Vehículo {patente} estacionado en Piso {piso}, Fila {fila}, Columna {columna}")
    return True


# TODO VALIDAR INGRESO DE PATENTE
def ingresar_auto_matriz(matriz):
    patente = input("Agrega el nro de patente: ")
    tipo_slot = funciones.tipo_slot()
    return


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


#!  REGISTRO DE AUTO
#! Verificar si la patente ya existe
#! Consultar si es mensual o diairo
#! Buscar espacio libre
#! Actualizar el slot
#! Mostrar mensaje de éxito o error


#! REGISTRO SALIDA DE AUTO
#! Ingresar patente a buscar
#! Buscar la patente en el garage
#! Si no se encuentra, mostrar mensaje de error
#! Si se encuentra, calcular el tiempo y costo
#! Actualizar el slot
#! Mostrar mensaje de éxito con el costo


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


# CONSTANTES
garage = [
    # PLANTA BAJA (piso 0) - 3x4 slots
    [
        [1, "", 1, False, False, None, 0],    [
            2, "ABC123", 2, True, False, "2025-09-04 08:30", 2],
        [3, "", 2, False, True, None, 0],    [
            4, "DEF456", 3, True, False, "2025-09-04 09:15", 3],
        [5, "GHI789", 1, True, False, "2025-09-04 07:45",
            1], [6, "", 4, False, False, None, 0],
        [7, "", 2, False, False, None, 0],   [
            8, "JKL012", 2, True, True, "2025-09-04 10:00", 2],
        [9, "", 1, False, False, None, 0],    [
            10, "MNO345", 4, True, False, "2025-09-04 11:20", 4],
        [11, "", 3, False, False, None, 0],  [12, "", 2, False, True, None, 0]
    ],

    # PISO 1 - 3x4 slots
    [
        [13, "", 2, False, False, None, 0],   [
            14, "", 1, False, False, None, 0],
        [15, "PQR678", 2, True, False, "2025-09-04 08:00",
            2], [16, "", 4, False, False, None, 0],
        [17, "STU901", 1, True, False, "2025-09-04 09:30",
            1], [18, "", 3, False, True, None, 0],
        [19, "", 2, False, False, None, 0],   [
            20, "VWX234", 3, True, False, "2025-09-04 07:20", 3],
        [21, "", 1, False, False, None, 0],   [
            22, "", 4, False, False, None, 0],
        [23, "YZA567", 1, True, False, "2025-09-04 10:45",
            1], [24, "", 2, False, False, None, 0]
    ],

    # PISO 2 - 3x4 slots
    [
        [25, "BCD890", 2, True, False, "2025-09-04 06:30",
            2], [26, "", 1, False, False, None, 0],
        [27, "", 4, False, True, None, 0],    [
            28, "", 2, False, False, None, 0],
        [29, "", 3, False, False, None, 0],   [
            30, "EFG123", 4, True, False, "2025-09-04 12:00", 4],
        [31, "", 1, False, False, None, 0], [
            32, "HIJ456", 2, True, False, "2025-09-04 08:45", 2],
        [33, "", 2, False, False, None, 0],   [
            34, "", 3, False, False, None, 0],
        [35, "", 1, False, False, None, 0],  [
            36, "KLM789", 1, True, True, "2025-09-04 09:00", 1]
    ],

    # PISO 3 - 3x4 slots
    [
        [37, "", 4, False, False, None, 0],   [
            38, "", 2, False, False, None, 0],
        [39, "", 1, False, False, None, 0],  [
            40, "NOP012", 3, True, False, "2025-09-04 11:00", 3],
        [41, "", 2, False, True, None, 0],    [
            42, "QRS345", 2, True, False, "2025-09-04 07:00", 2],
        [43, "", 4, False, False, None, 0], [44, "", 3, False, False, None, 0],
        [45, "TUV678", 1, True, False, "2025-09-04 10:15",
            1], [46, "", 1, False, False, None, 0],
        [47, "", 2, False, False, None, 0],  [48, "", 4, False, False, None, 0]
    ]
]


# Representacion costos posicion0: precio por hora posicion1 precio por dia

COSTOS = [
    [],  # vacio, seria el 0 que no representa nada,
    [2200, 50000],  # 1 moto
    [2400, 165000],  # auto
    [3500, 200000]  # camioneta

]

# Configuración del edificio
pisos = 4
filas_por_piso = 3
columnas_por_piso = 4
total_slots_por_piso = filas_por_piso * columnas_por_piso
