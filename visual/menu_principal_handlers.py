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
from colorama import Back, Fore, Style
from auxiliares.consola import clear_screen
from constantes.tipos_vehiculos import enum_tipo_vehiculo


def handle_consultar_espacios_libres(garage, garage_data):
    """Maneja la consulta de espacios libres"""
    print("\n1. Por piso\n2. Por tipo de vehículo\n3. Totales\n4. Volver")
    subop = input(Fore.YELLOW + "\nSeleccione una de las opciones: " + Style.RESET_ALL)
    
    if subop == "1":
        piso = pedir_piso(garage_data) 
        
        libres = contar_espacios_libres([garage_data[piso]])
        print(Fore.GREEN + f"\nEspacios libres en el piso {piso}: {libres}" + Style.RESET_ALL)
        input('\nPresione cualquier tecla para continuar...')
        clear_screen()
    elif subop == "2":
        print("\nTipos de vehículo:")
        print("1. Moto\n2. Auto\n3. Camioneta\n4. Bicicleta")
        tipo = pedir_tipo_vehiculo()
        libres = contar_espacios_libres_por_tipo(garage_data, tipo)
        #Formatear tipo a texto
        
        tipos = enum_tipo_vehiculo()
        
        tipo_texto = [k for k, v in tipos.items() if v == tipo]
        print(Fore.GREEN + f"\nEspacios libres para tipo {tipo_texto[0] if tipo_texto else tipo}: {libres}" + Style.RESET_ALL)
        input('\nPresione cualquier tecla para continuar...')
        clear_screen()
        
    elif subop == "3":
        libres = contar_espacios_libres(garage_data)
        print(Fore.GREEN   + f"\nEspacios libres en todo el garage: {libres}" + Style.RESET_ALL)
        input('\nPresione cualquier tecla para continuar...')
        clear_screen()

def handle_consultar_vehiculos_estacionados(garage, garage_data):
    """Maneja la consulta de vehículos estacionados"""
    print("\n1. Por tipo de vehículo\n2. Totales\n3. Volver")
    subop = input(Fore.YELLOW+ "\nSeleccione una de las opciones: " + Style.RESET_ALL)
    
    if subop == "1":
        print("\nTipos de vehículo:")
        print("1. Moto\n2. Auto\n3. Camioneta\n4. Bicicleta")
        tipo = pedir_tipo_vehiculo()
        cantidad = contar_por_tipo_vehiculo(garage_data, tipo)
        tipos = enum_tipo_vehiculo()
        tipo_texto = [k for k, v in tipos.items() if v == tipo]
        print(Fore.GREEN + f"Cantidad de {tipo_texto[0] if tipo_texto else tipo} estacionadas: {cantidad}" + Style.RESET_ALL)
    
    elif subop == "2":
        print(Fore.GREEN + "\n--- Vehículos estacionados por tipo ---\n" + Style.RESET_ALL)
        tipos = enum_tipo_vehiculo()
        
        # tipos: {"moto": 1, "auto": 2, ...}
        for tipo_nombre, tipo_num in tipos.items():
            cantidad = contar_por_tipo_vehiculo(garage_data, tipo_num)
            print(Fore.GREEN + f"{tipo_nombre.capitalize()}: {cantidad}" + Style.RESET_ALL)
    input('\nPresione cualquier tecla para continuar...')
    clear_screen()


def handle_ingresar_vehiculo(garage, garage_data):
    """Maneja el ingreso de vehículos"""
    registrar_entrada_auto(garage_data)

def handle_registrar_salida(garage, garage_data):
    """Maneja la salida de vehículos"""
    patente = pedir_patente()
    if registrar_salida_vehiculo(garage_data, patente):
        print("Salida registrada correctamente.")
    else:
        print("Patente no encontrada.")

def handle_editar_vehiculo(garage, garage_data):
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

def handle_mostrar_estado_garage(garage, garage_data):
    """Maneja mostrar el estado del garage"""
    mostrar_estado_garage(garage_data)

def handle_buscar_vehiculo(garage, garage_data):
    """Maneja la búsqueda de vehículos por patente"""
    patente = pedir_patente()
    pos = buscar_por_patente(garage_data, patente)
    if pos != (-1, -1):
        print(f"Vehículo encontrado en Piso {pos[0]}, Slot {pos[1]}")
    else:
        print("Vehículo no encontrado.")

def handle_estadisticas_rapidas(garage, garage_data= None):
    """Maneja las estadísticas rápidas"""
    mostrar_estadisticas_rapidas(garage)