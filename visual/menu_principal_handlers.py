import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

###Agregando comentario para que git detecte los cambios D:
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
)

from constantes.tarifa import print_tarifas

from colorama import Back, Fore, Style
from auxiliares.consola import clear_screen
from constantes.tipos_vehiculos import enum_tipo_vehiculo
from users.users_garage import actualizar_slot
from garage.slot_utils import tipos_de_slot_definidos, get_slot_in_piso

def handle_consultar_espacios_libres(garage, garage_data):
    """Maneja la consulta de espacios libres"""
    print("\n1. Por piso\n2. Por tipo de vehículo\n3. Totales\n4. Volver")
    subop = input(Fore.YELLOW + "\nSeleccione una de las opciones: " + Style.RESET_ALL)
    
    if subop == "1":
        piso = pedir_piso(garage_data) 
        
        libres = contar_espacios_libres([garage_data[piso]])
        print(Fore.GREEN + f"\nEspacios libres en el piso {piso}: {libres}" + Style.RESET_ALL)
        clear_screen()
    elif subop == "2":
        print("\nTipos de vehículo:")
        print("1. Moto\n2. Auto\n3. Camioneta\n")
        tipo = pedir_tipo_vehiculo()
        libres = contar_espacios_libres_por_tipo(garage_data, tipo)
        #Formatear tipo a texto
        
        tipos = enum_tipo_vehiculo()
        
        tipo_texto = [k for k, v in tipos.items() if v == tipo]
        print(Fore.GREEN + f"\nEspacios libres para tipo {tipo_texto[0] if tipo_texto else tipo}: {libres}" + Style.RESET_ALL)
        clear_screen()
        
    elif subop == "3":
        libres = contar_espacios_libres(garage_data)
        print(Fore.GREEN   + f"\nEspacios libres en todo el garage: {libres}" + Style.RESET_ALL)
        clear_screen()

def handle_consultar_vehiculos_estacionados(garage, garage_data):
    """Maneja la consulta de vehículos estacionados"""
    print("\n1. Por tipo de vehículo\n2. Totales\n3. Volver")
    subop = input(Fore.YELLOW+ "\nSeleccione una de las opciones: " + Style.RESET_ALL)
    
    if subop == "1":
        print("\nTipos de vehículo:")
        print("1. Moto\n2. Auto\n3. Camioneta")
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
    clear_screen()


def handle_ingresar_vehiculo(garage, garage_data):
    """Maneja el ingreso de vehículos"""
    if not tipos_de_slot_definidos(garage, garage_data):
        print(f"Debe definir tipos de slots en garage con id {garage.get('garage_id')} antes de ingresar vehiculos.🚩🚩🚩")
        clear_screen()
        return
    registrar_entrada_auto(garage_data)


def handle_registrar_salida(garage, garage_data, tarifa):
    """Maneja la salida de vehículos"""
    patente = pedir_patente()
    if registrar_salida_vehiculo(patente, tarifa):
        print("Salida registrada correctamente.")
    else:
        print("Patente no encontrada.")

def menu_editar_vehiculo():
    """Menu para editar vehiculo"""
    print(Fore.GREEN+ "\n=== MENU EDITAR VEHICULO ===" + Style.RESET_ALL)
    print("1. Editar patente")
    print("2. Editar tipo de vehiculo")
    print("3. Editar estadia")
    print("z. Volver atras")

    while True:
        opcion = input("Seleccione una opción: \n")
        if opcion == 'z':
            break
        if opcion not in ('1','2','3'):
            print("opcion invalida, intente de nuevo")
        return opcion

    
def handle_editar_vehiculo(garage, garage_data):
    """Maneja la edición de vehículos guardados"""
    opcion = menu_editar_vehiculo()
    if not opcion:
        return
    
    patente = pedir_patente()
    piso, slot = buscar_por_patente(garage_data, patente)
    if piso == -1 and slot ==-1:
        print(Fore.RED + 'Patente no encontrada en el garage' + Style.RESET_ALL)
        return
    nueva_patente = None
    nueva_estadia = None
    nuevo_tipo = None
    if opcion == '1':
        nueva_patente = pedir_patente()
    elif opcion == '2':
        nuevo_tipo = pedir_tipo_vehiculo()
    elif opcion == '3':
        while True:
            try:
                nueva_estadia_input = int(input("Ingrese la nueva estadía (1/mensual, 2/diaria): "))
                if nueva_estadia_input not in [1, 2]:
                    print("Valor invalido, intente otra vez")
                    continue
                else:
                    nueva_estadia = True if nueva_estadia_input == 1 else False
                    break
            except ValueError:
                print("Por favor ingrese 1 o 2")
                continue
    slot_data = get_slot_in_piso(garage_data[piso], slot)
    tipo_vehiculo = slot_data.get("tipo_vehiculo")
    nueva_patente = nueva_patente if nueva_patente else patente
    nuevo_tipo = nuevo_tipo if nuevo_tipo else tipo_vehiculo
    nueva_estadia = nueva_estadia if nueva_estadia is not None else slot_data.get("reservado_mensual")

    data = {"patente": nueva_patente, "tipo_vehiculo": nuevo_tipo, "reservado_mensual": nueva_estadia, 'piso': piso }
    if actualizar_slot(garage.get('garage_id'), slot, data):
        if nuevo_tipo != int(tipo_vehiculo):
            print(Fore.YELLOW + "SE EDITO EL TIPO DE VEHICULO. Use la opción 'Mover vehículo' del menú para moverlo a un slot acorde al nuevo tipo." + Style.RESET_ALL)
        print("Vehículo modificado correctamente.")
    return True

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
    mostrar_estadisticas_rapidas(garage_data)
    
    
def handle_imprimir_tarifas(tarifa):
    """Maneja la impresión de las tarifas del garage"""
    print_tarifas(tarifa)
    clear_screen()
    
