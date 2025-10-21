import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from users.users_garage import crear_archivo_users_garage, leer_garage_desde_csv
from visual.menu_handlers import (
    handle_login, 
    handle_registro, 
    handle_seleccionar_garage, 
    handle_crear_garage,
    handle_actualizar_tipo_slots,
    handle_actualizar_slots
)
from visual.menu_principal_handlers import (
    handle_consultar_espacios_libres,
    handle_consultar_vehiculos_estacionados,
    handle_ingresar_vehiculo,
    handle_registrar_salida,
    handle_editar_vehiculo,
    handle_mostrar_estado_garage,
    handle_buscar_vehiculo,
    handle_estadisticas_rapidas,
)

from cache.json import leer_estado_garage, guardar_estado_garage
from colorama import Fore, Style

def mostrar_menu_inicial():
    """Menú de inicio de sesión y registro"""
    print("\n=== BIENVENIDO A SLOTMASTER ===")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")

def mostrar_menu_garage(usuario):
    """Menú para seleccionar o crear garage"""
    print(f"\n=== GESTIÓN DE GARAGES - {usuario['nombre']} ===")
    print("1. Seleccionar garage existente")
    print("2. Crear nuevo garage")
    print("3. Cerrar sesión")

def mostrar_menu_principal(garage_name):
    """Menú principal del sistema"""
    print(f"\n=== MENÚ PRINCIPAL - {garage_name} ===")
    print("1. Consultar espacios libres")
    print("2. Consultar cantidad de vehículos estacionados")
    print("3. Ingresar un vehículo")
    print("4. Registrar salida de un vehículo")
    print("5. Editar un vehículo")
    print("6. Mostrar estado del garage")
    print("7. Buscar vehículo por patente")
    print("8. Estadísticas rápidas")
    print("9. Actualizar tipo de slot")
    print("10. Actualizar info de slots")
    print("c. Cambiar garage")
    print("x. Cerrar sesión")
    print("z. Salir")

def menu_inicial():
    """Gestiona el login y registro - retorna el usuario o None"""
    continuar = True
    usuario = None
    
    while continuar and not usuario:
        mostrar_menu_inicial()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            usuario = handle_login()
            if usuario:
                continuar = False
                
        elif opcion == "2":
            handle_registro()
                
        elif opcion == "3":
            print("¡Hasta luego!")
            continuar = False
            
        else:
            print(Fore.RED + "Opción inválida" + Style.RESET_ALL)
    
    return usuario

def menu_garage(usuario):
    """Gestiona la selección/creación de garages - retorna el garage seleccionado o None"""
    crear_archivo_users_garage()
    
    continuar = True
    garage_seleccionado = None #users-garage actual
    
    while continuar and not garage_seleccionado:
        mostrar_menu_garage(usuario)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            garage_seleccionado = handle_seleccionar_garage(usuario)
            if garage_seleccionado:
                continuar = False
                
        elif opcion == "2":
            garage_seleccionado = handle_crear_garage(usuario)
            if garage_seleccionado:
                continuar = False
                    
        elif opcion == "3":
            continuar = False  # Cerrar sesión
            
        else:
            print(Fore.RED + "Opción inválida" + Style.RESET_ALL)
    
    return garage_seleccionado

def menu_principal(garage_actual, garageName):
    """Menú principal del sistema - retorna acción a realizar""" 
    continuar = True
    accion = None

    # Lista indexada desde 0 → por eso usamos un desplazamiento (-1)
    # Agregar nuevos handlers aquí según se vayan creando
    handlers = [
        handle_consultar_espacios_libres,
        handle_consultar_vehiculos_estacionados,
        handle_ingresar_vehiculo,
        handle_registrar_salida,
        handle_editar_vehiculo,
        handle_mostrar_estado_garage,
        handle_buscar_vehiculo,
        handle_estadisticas_rapidas,
        handle_actualizar_tipo_slots,
        handle_actualizar_slots
    ]

    # Acciones especiales (no ejecutan función)
    acciones_especiales = {
        "c": "cambiar_garage",
        "x": "cerrar_sesion",
        "z": "salir",
    }
    try: 
        while continuar and not accion:
            mostrar_menu_principal(garageName)
            opcion = input("Seleccione una opción: ")

            if opcion.isdigit():
                indice = int(opcion) - 1  # la lista empieza en 0 y el menú en 1
                if 0 <= indice < len(handlers):
                    handlers[indice](garage_actual)
                    continue

            if opcion in acciones_especiales:
                accion = acciones_especiales[opcion]
                continuar = False
            else:
                print(Fore.RED + "Opción inválida. Intente de nuevo." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}" + Style.RESET_ALL)
    return accion



def main():
    """Función principal que coordina todo el flujo"""
    programa_activo = True
    
    while programa_activo:
        # 1. Login/Registro
        usuario_actual = menu_inicial()
        if not usuario_actual:
            programa_activo = False
            continue
            
        # 2. Selección/Creación de garage
        session_active = True
        while session_active and programa_activo:
            garage_actual_obj = menu_garage(usuario_actual)
            garage_from_csv = leer_garage_desde_csv(garage_actual_obj['garage_id'])
            if not garage_actual_obj:
                session_active = False
                continue
 
            
            # 3. Menú principal
            menu_activo = True
            while menu_activo and session_active:
                resultado = menu_principal(garage_actual_obj, garage_actual_obj['garage_name'])
                
                if resultado == "cambiar_garage":
                    menu_activo = False
                elif resultado == "cerrar_sesion":
                    session_active = False
                    menu_activo = False
                elif resultado == "salir":
                    print("¡Hasta luego!")
                    programa_activo = False
                    session_active = False
                    menu_activo = False

if __name__ == "__main__":
    main()