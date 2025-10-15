import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from garage.garage_util import (
    contar_espacios_libres,
    buscar_por_patente,
    contar_espacios_libres_por_tipo,
    mostrar_estadisticas_rapidas

)
from users.interaccion_usuario import (
    pedir_piso,
    pedir_patente,
    pedir_tipo_vehiculo,
    mostrar_estado_garage
)
from main import (
    registrar_entrada_auto,
    contar_por_tipo_vehiculo,
    registrar_salida_vehiculo,
    modificar_vehiculo,
)

def handle_consultar_espacios_libres(garage):
    """Maneja la consulta de espacios libres"""
    print("\n1. Por piso\n2. Por tipo de vehículo\n3. Totales\n4. Volver")
    subop = input("Seleccione una de las opciones: ")
    
    if subop == "1":
        piso = pedir_piso(garage)
        libres = contar_espacios_libres([garage[piso]])
        print(f"Espacios libres en el piso {piso}: {libres}")
    elif subop == "2":
        print("\nTipos de vehículo:")
        print("1. Moto\n2. Auto\n3. Camioneta\n4. Bicicleta")
        tipo = pedir_tipo_vehiculo()
        libres = contar_espacios_libres_por_tipo(garage, tipo)
        print(f"Espacios libres para tipo {tipo}: {libres}")
    elif subop == "3":
        libres = contar_espacios_libres(garage)
        print(f"Espacios libres en todo el garage: {libres}")

def handle_consultar_vehiculos_estacionados(garage):
    """Maneja la consulta de vehículos estacionados"""
    print("\n1. Por tipo de vehículo\n2. Totales\n3. Volver")
    subop = input("Seleccione una de las opciones: ")
    
    if subop == "1":
        print("\nTipos de vehículo:")
        print("1. Moto\n2. Auto\n3. Camioneta\n4. Bicicleta")
        tipo = pedir_tipo_vehiculo()
        cantidad = contar_por_tipo_vehiculo(garage, tipo)
        tipos_nombres = {1: "Motos", 2: "Autos", 3: "Camionetas", 4: "Bicicletas"}
        print(f"Cantidad de {tipos_nombres[tipo]} estacionadas: {cantidad}")
    elif subop == "2":
        print("\n--- Vehículos estacionados por tipo ---")
        tipos = {1: "Motos", 2: "Autos", 3: "Camionetas", 4: "Bicicletas"}
        for tipo_num, tipo_nombre in tipos.items():
            cantidad = contar_por_tipo_vehiculo(garage, tipo_num)
            print(f"{tipo_nombre}: {cantidad}")

def handle_ingresar_vehiculo(garage):
    """Maneja el ingreso de vehículos"""
    registrar_entrada_auto(garage)

def handle_registrar_salida(garage):
    """Maneja la salida de vehículos"""
    patente = pedir_patente()
    if registrar_salida_vehiculo(garage, patente):
        print("Salida registrada correctamente.")
    else:
        print("Patente no encontrada.")

def handle_editar_vehiculo(garage):
    """Maneja la edición de vehículos"""
    patente = pedir_patente()
    nuevo_tipo = pedir_tipo_vehiculo()
    nueva_patente = input("Nueva patente (dejar vacío para no cambiar): ").strip().upper()
    if nueva_patente == "":
        nueva_patente = None
    if modificar_vehiculo(garage, patente, nuevo_tipo, nueva_patente):
        print("Vehículo modificado correctamente.")
    else:
        print("Patente no encontrada.")

def handle_mostrar_estado_garage(garage):
    """Maneja mostrar el estado del garage"""
    mostrar_estado_garage(garage)

def handle_buscar_vehiculo(garage):
    """Maneja la búsqueda de vehículos por patente"""
    patente = pedir_patente()
    pos = buscar_por_patente(garage, patente)
    if pos != (-1, -1):
        print(f"Vehículo encontrado en Piso {pos[0]}, Slot {pos[1]}")
    else:
        print("Vehículo no encontrado.")

def handle_estadisticas_rapidas(garage):
    """Maneja las estadísticas rápidas"""
    mostrar_estadisticas_rapidas(garage)