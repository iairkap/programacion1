
def buscar_por_patente(garage, patente):
    for i in range(len(garage)):
        piso = garage[i]
        for slot in piso:
            if slot[3] == True and patente == slot[1]:
                return (i, slot[0])
    return (-1, -1)

def mostrar_estadisticas_rapidas(garage):
    print("\n--- ESTADÍSTICAS RÁPIDAS ---")
    total_libres = contar_espacios_libres(garage)
    total_estacionados = sum(contar_por_tipo_vehiculo(garage, tipo) for tipo in range(1, 5))
    print(f"Total de espacios libres: {total_libres}")
    print(f"Total de vehículos estacionados: {total_estacionados}")
    tipos = {1: "Motos", 2: "Autos", 3: "Camionetas", 4: "Bicicletas"}
    for tipo_num, tipo_nombre in tipos.items():
        cantidad = contar_por_tipo_vehiculo(garage, tipo_num)
        print(f"{tipo_nombre}: {cantidad}")



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
