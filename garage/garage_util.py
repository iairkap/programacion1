from colorama import Fore, Style
from auxiliares.consola import clear_screen

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
                if patente_slot == patente and ocupado_slot:
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

def buscar_espacio_libre(garage, tipo_vehiculo):
    for i in range(len(garage)):
        piso = garage[i]
        for slot in piso:
            if slot["ocupado"] == False and (tipo_vehiculo == slot["tipo_slot"] or slot["tipo_slot"] == tipo_vehiculo):
                return (i, slot["id"])
    return (-1, -1)


def contar_espacios_libres(garage):
    cont = 0
    for piso in garage:
        for slot in piso:
            if slot["ocupado"] == False:
                cont += 1
    return cont


def contar_espacios_libres_por_tipo(garage, tipo_vehiculo):
    cont = 0
    for piso in garage:
        for slot in piso:
            if slot["ocupado"] == False and (tipo_vehiculo == slot["tipo_slot"] or slot["tipo_slot"] == tipo_vehiculo):
                cont += 1
    return cont

def contar_por_tipo_vehiculo(garage, tipo_buscado):
    # Cuenta slots donde slot[6] = tipo_buscado Y slot[3] = True (ocupado)
    return sum(slot["tipo_vehiculo"] == tipo_buscado and slot["ocupado"] for piso in garage for slot in piso)


def mostrar_estadisticas_rapidas(garage):
    print(Fore.GREEN + "\n--- ESTADÍSTICAS RÁPIDAS ---" + Style.RESET_ALL)
    # Cuenta todos los espacios libres en el garage
    total_libres = contar_espacios_libres(garage)
    # Suma todos los vehículos estacionados de todos los tipos (1-4)
    total_estacionados = sum(contar_por_tipo_vehiculo(
        garage, tipo) for tipo in range(1, 5))
    print(Fore.GREEN + f"Total de espacios libres: {total_libres}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Total de vehículos estacionados: {total_estacionados}" + Style.RESET_ALL)
    # Diccionario para convertir números de tipo a nombres legibles
    tipos = {1: "Motos", 2: "Autos", 3: "Camionetas"}
    # Muestra la cantidad de cada tipo de vehículo estacionado
    for tipo_num, tipo_nombre in tipos.items():
        cantidad = contar_por_tipo_vehiculo(garage, tipo_num)
        print(Fore.GREEN + f"{tipo_nombre}: {cantidad}" + Style.RESET_ALL)
    
    clear_screen()

def buscar_slots_por_tipo(garage, tipo_slot):
    """Busca todos los ids de slots en el garage que coinciden con el tipo de slot pasado por parametro
    output: {piso: slots_disponibles_por_tippo}"""
    slots_por_tipo = []
    pisos = {}
    for num_piso, piso_data in enumerate(garage):
        for slot in piso_data:
            if slot.get('tipo_slot') == tipo_slot and not slot.get('ocupado'):
                slots_por_tipo.append(slot.get('id'))
        pisos.update({num_piso: slots_por_tipo})
    return pisos
