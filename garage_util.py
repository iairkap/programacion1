# Representación del garage: lista de pisos (matrices)
# Cada elemento es: [id, patente, tipo_slot, ocupado, reservado_mensual, hora_entrada, tipo_vehiculo_estacionado]
# tipo_slot: 1=moto, 2=auto, 3=camioneta, 4=multi (acepta cualquiera)
# ocupado: True/False
# reservado_mensual: True/False
# hora_entrada: timestamp o None si está vacío
# tipo_vehiculo_estacionado: 1=moto, 2=auto, 3=camioneta, 4=bici, 0=vacío


    # # PLANTA BAJA (piso 0) - 3x4 slots
    # [
    #     [1, "", 1, False, False, None, 0],    [
    #         2, "ABC123", 2, True, False, "2025-09-04 08:30", 2],
    #     [3, "", 2, False, True, None, 0],    [
    #         4, "DEF456", 3, True, False, "2025-09-04 09:15", 3],
    #     [5, "GHI789", 1, True, False, "2025-09-04 07:45",
    #         1], [6, "", 4, False, False, None, 0],
    #     [7, "", 2, False, False, None, 0],   [
    #         8, "JKL012", 2, True, True, "2025-09-04 10:00", 2],
    #     [9, "", 1, False, False, None, 0],    [
    #         10, "MNO345", 4, True, False, "2025-09-04 11:20", 4],
    #     [11, "", 3, False, False, None, 0],  [12, "", 2, False, True, None, 0]
    # ],



def buscar_por_patente(garage,patente):
    for i in range(len(garage)):
        piso = garage[i]
        for slot in piso :
            if slot[3] == True and patente == slot[1]:
                return (i, slot[0])
    return (-1,-1)

def buscar_espacio_libre(garage,tipo_vehiculo):
    for i in range(len(garage)):
        piso = garage[i]
        for slot in piso:
            if slot[3] == False and (tipo_vehiculo == slot[2] or slot[2] == 4):
                return (i,slot[0])
    return (-1,-1)

    
def contar_espacios_libres(garage):
    cont = 0
    for piso in garage:
        for slot in piso:
            if slot[3] == False: cont+=1
    return cont

def contar_espacios_libres_por_tipo(garage, tipo_vehiculo):
    cont = 0
    for piso in garage:
        for slot in piso:
            if slot[3] == False and (tipo_vehiculo == slot[2] or slot[2] == 4):
                cont+=1
    return cont
