# Representación del garage: lista de pisos (matrices)
# Cada elemento es: [id, patente, tipo_slot, ocupado, reservado_mensual, hora_entrada, tipo_vehiculo_estacionado]
# tipo_slot: 1=moto, 2=auto, 3=camioneta, 4=multi (acepta cualquiera)
# ocupado: True/False
# reservado_mensual: True/False
# hora_entrada: timestamp o None si está vacío
# tipo_vehiculo_estacionado: 1=moto, 2=auto, 3=camioneta, 4=bici, 0=vacío


import funciones


# TODO VALIDAR INGRESO DE PATENTE
def ingresarAutoEnMatriz(matriz):
    patente = input("Agrega el nro de patente: ")
    tipo_slot = funciones.tipo_slot()
    return


def salidaTipoVehiculo(tipo_slot):
    salida = ""
    if tipo_slot == 1:
        salida = "Moto"
    elif tipo_slot == 2:
        salida = "Auto"
    elif tipo_slot == 3:
        salida = "Camioneta"
    return salida


# CONSTANTES
# ? Matriz momentanea
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
    [3500, 200000]

]

# Configuración del edificio
pisos = 4
filas_por_piso = 3
columnas_por_piso = 4
total_slots_por_piso = filas_por_piso * columnas_por_piso


ingresarAutoEnMatriz(garage)
