import funciones
from mockdata import GARAGE, COSTOS
import random
from interaccion_usuario import pedir_patente

#! TODO MODULARIZAR CODIGO -> MUCHA REPETICION DE FOR y de los bucles


def mostrar_estadisticas_rapidas(garage):
    print("\n--- ESTADÍSTICAS RÁPIDAS ---")
    total_libres = contar_espacios_libres(garage)
    total_estacionados = sum(contar_por_tipo_vehiculo(
        garage, tipo) for tipo in range(1, 5))
    print(f"Total de espacios libres: {total_libres}")
    print(f"Total de vehículos estacionados: {total_estacionados}")
    tipos = {1: "Motos", 2: "Autos", 3: "Camionetas", 4: "Bicicletas"}
    for tipo_num, tipo_nombre in tipos.items():
        cantidad = contar_por_tipo_vehiculo(garage, tipo_num)
        print(f"{tipo_nombre}: {cantidad}")


def busqueda_espacio_libre(garage, tipo_vehiculo):
    for piso_idx in range(len(garage)):
        piso = garage[piso_idx]
        for slot in piso:
            if not slot[3]:
                if slot[2] == tipo_vehiculo or slot[2] == 4:
                    return (piso_idx, slot[0])
    return (-1, -1)


def buscar_por_patente(garage, patente_buscada):
    for piso_idx in range(len(garage)):
        piso = garage[piso_idx]
        for slot in piso:
            if slot[1] == patente_buscada and slot[3]:
                return (piso_idx, slot[0])  # Retorna piso y slot_id
    return (-1, -1)


def contar_espacios_libres(garage):
    return sum(not slot[3] for piso in garage for slot in piso)


def contar_por_tipo_vehiculo(garage, tipo_buscado):
    return sum(slot[6] == tipo_buscado and slot[3] for piso in garage for slot in piso)


def obtener_slot_por_id(garage, slot_id):
    """Obtiene slot por ID - NUEVA función auxiliar"""
    for piso in garage:
        for slot in piso:
            if slot[0] == slot_id:
                return slot
    return None


def registrar_salida_vehiculo(garage, patente):
    """
    devuelve True si se realizó la salida, False si no se encontró la patente.
    """
    for piso in garage:
        for slot in piso:
            if slot[3] == True and slot[1] == patente:
                slot[1] = ""      # patente
                slot[3] = False   # Marca como libre
                slot[5] = ""      # Borra la fecha de ingreso
                slot[6] = 0       # Borra el tipo de vehículo
                return True
    return False


def modificar_vehiculo(garage, patente, nuevo_tipo=None, nueva_patente=None):
    """
    devuelve True si se modificó, False si no se encontró la patente.
    """
    for piso in garage:
        for slot in piso:
            if slot[3] == True and slot[1] == patente:
                if nuevo_tipo is not None:
                    slot[6] = nuevo_tipo
                if nueva_patente is not None:
                    slot[1] = nueva_patente
                return True
    return False


def registrar_entrada_auto(garage):

    patente = pedir_patente()

    tipo_vehiculo = funciones.tipo_slot()

    # Verificar si la patente ya existe
    posicion_existente = buscar_por_patente(garage, patente)
    if posicion_existente != (-1, -1):
        print(f"Error: La patente {patente} ya está en el garage")
        return False

    # Buscar espacio libre
    posicion = busqueda_espacio_libre(garage, tipo_vehiculo)

    if posicion == (-1, -1):
        print("No hay espacios disponibles para este tipo de vehículo")
        return False

    piso, slot_id = posicion
    slot = obtener_slot_por_id(garage, slot_id)

    if slot:
        # Actualizar el slot
        slot[1] = patente
        slot[3] = True  # CORREGIDO: True = ocupado
        slot[5] = generar_fecha_aleatoria()
        slot[6] = tipo_vehiculo
        print(f"Vehículo {patente} estacionado en Piso {piso}, Slot {slot_id}")
        return True

    return False


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
    for i in range(len(garage)):
        if valor in garage[i]:
            del garage[i]
            return True
    return False


def actualizar_slot(patente, tipo_de_vehículo, piso, fila, columna, garage=GARAGE):
    pass


def ingresar_patente():
    """CORREGIDA - quité el parámetro que no se usaba"""
    while True:
        patente = pedir_patente()
        if chequear_existencia_patente(patente):
            print("Error: La patente ya existe en el sistema.")
            continue
        if len(patente) == 6 and patente[:3].isalpha() and patente[3:].isdigit():
            return patente
        else:
            print("Error: Formato de patente invalido. Intente nuevamente.")


def acceder_a_info_de_patentes():
    datos = []
    for piso in GARAGE:
        for slot in piso:
            if slot[3]:  # Solo slots ocupados
                datos.append(slot)
    return datos


def chequear_existencia_patente(patente):
    """Chequea si la patente existe en el sistema"""
    return buscar_por_patente(GARAGE, patente) != (-1, -1)


def es_subscripcion_mensual(patente):
    """Chequea si la subscripcion es mensual o diaria"""
    for piso in GARAGE:
        for slot in piso:
            if slot[1] == patente and slot[3]:
                return slot[4]  # reservado_mensual
    return False


def chequear_espacio_libre(garage=GARAGE):
    """Chequea si hay espacio libre en el estacionamiento"""
    return contar_espacios_libres(garage) > 0


def buscar_patente(patente):
    """Busca información completa de una patente"""
    for piso in GARAGE:
        for slot in piso:
            if slot[1] == patente and slot[3]:
                return slot
    return None


def calcular_costo_de_estadia(patente, hora_salida):
    """Calcula costo de estadía"""
    info_patente = buscar_patente(patente)
    if not info_patente:
        return 0

    tipo_de_slot = info_patente[6]  # tipo_vehiculo_estacionado

    if not es_subscripcion_mensual(patente):
        if info_patente[5]:  # Si tiene hora de entrada
            try:
                min_entrada = info_patente[5].split(" ")[1].replace(":", "")
                min_transcurridos = int(
                    hora_salida.replace(":", "")) - int(min_entrada)
                horas_transcurridas = max(
                    1, min_transcurridos / 100)  # Mínimo 1 hora
                costo = COSTOS[tipo_de_slot][0] * horas_transcurridas
                return round(costo, 2)
            except:
                return COSTOS[tipo_de_slot][0]
    else:
        return COSTOS[tipo_de_slot][1]

    return 0


def registrar_salida_vehiculo(garage):
    patente = pedir_patente()
    pos = buscar_por_patente(garage, patente)
    if pos == (-1, -1):
        print("Vehículo no encontrado.")
        return False

    hora_salida = input("Ingrese hora de salida (HH:MM): ").strip()
    costo = calcular_costo_de_estadia(patente, hora_salida)

    piso_idx, slot_id = pos
    # Buscar el objeto slot por ID dentro del piso
    for slot in garage[piso_idx]:
        if slot[0] == slot_id:
            # Mostrar costo antes de liberar
            print(f"Costo de estadía para {patente}: ${costo}")
            # Liberar
            slot[1] = ""
            slot[3] = False
            slot[5] = None
            slot[6] = 0
            print(
                f"Salida registrada. Piso {piso_idx}, Slot {slot_id} liberado.")
            return True

    print("Error interno liberando el slot.")
    return False


def salida_tipo_vehiculo(tipo_slot):
    """Convierte tipo numérico a texto"""
    if tipo_slot == 1:
        return "Moto"
    elif tipo_slot == 2:
        return "Auto"
    elif tipo_slot == 3:
        return "Camioneta"
    elif tipo_slot == 4:
        return "Bicicleta"
    return "Desconocido"


# Configuración del edificio
pisos = 4
filas_por_piso = 3
columnas_por_piso = 4
total_slots_por_piso = filas_por_piso * columnas_por_piso
