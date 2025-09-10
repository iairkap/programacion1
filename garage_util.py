
def buscar_por_patente(garage, patente):
    for i in range(len(garage)):
        piso = garage[i]
        for slot in piso:
            if slot[3] == True and patente == slot[1]:
                return (i, slot[0])
    return (-1, -1)



def buscar_espacio_libre(garage, tipo_vehiculo):
    for i in range(len(garage)):
        piso = garage[i]
        for slot in piso:
            if slot[3] == False and (tipo_vehiculo == slot[2] or slot[2] == 4):
                return (i, slot[0])
    return (-1, -1)


def contar_espacios_libres(garage):
    cont = 0
    for piso in garage:
        for slot in piso:
            if slot[3] == False:
                cont += 1
    return cont


def contar_espacios_libres_por_tipo(garage, tipo_vehiculo):
    cont = 0
    for piso in garage:
        for slot in piso:
            if slot[3] == False and (tipo_vehiculo == slot[2] or slot[2] == 4):
                cont += 1
    return cont
