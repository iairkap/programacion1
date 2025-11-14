import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from users.pass_logic import login
from users.users_garage import crear_archivo_users_garage, get_garage_data
from visual.menu_handlers import (
    handle_login, 
    handle_registro, 
    handle_seleccionar_garage, 
    handle_crear_garage,
    handle_actualizar_tipo_slots,
    handle_actualizar_tarifas,
    handle_mover_vehiculo,  
    handle_administrar_usuarios
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
    handle_imprimir_tarifas
)

from constantes.tarifa import guardar_precios_garage

from cache.json import leer_estado_garage, guardar_estado_garage
from colorama import Fore, Style
from auxiliares.consola import clear_screen

###Agregando comentario para que git detecte los cambios D:

def mostrar_menu_inicial():
    """Menú de inicio de sesión y registro"""
    print(Fore.GREEN + "\n=== BIENVENIDO A SLOTMASTER ===" + Style.RESET_ALL)
    print("\n1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir\n")

def mostrar_menu_garage(usuario):
    """Menú para seleccionar o crear garage"""
    print(Fore.GREEN+f"\n=== GESTIÓN DE GARAGES - {usuario['nombre']} ===" + Style.RESET_ALL)
    print("\n1. Seleccionar garage existente")
    print("2. Crear nuevo garage")
    
    
    if usuario.get("admin", False) == "True":
        print("3. Administrar usuarios")
        print("4. Cerrar sesión\n")
    else: 
        print("3. Cerrar sesión\n")

def mostrar_menu_principal(garage_name):
    """Menú principal del sistema"""

    opciones_menu_principal = [
    "Consultar espacios libres",
    "Consultar cantidad de vehículos estacionados",
    "Ingresar un vehículo",
    "Registrar salida de un vehículo",
    "Editar un vehículo",
    "Mostrar estado del garage",
    "Buscar vehículo por patente",
    "Estadísticas rápidas",
    "Actualizar tipo de slot",
    "Actualizar tarifas",
    "Imprimir tarifas",
    "Mover vehículo"
    ]
        
    print(Fore.GREEN + f"\n=== MENÚ PRINCIPAL - {garage_name['garage_name'].upper()} ===" + Style.RESET_ALL)
    for i, opcion in enumerate(opciones_menu_principal, start=1):
        print(f"{i}. {opcion}")
    print("\nc. Cambiar garage")
    print("x. Cerrar sesión")
    print("z. Salir\n")

def menu_inicial():
    """Gestiona el login y registro - retorna el usuario o None"""
    continuar = True
    usuario = None
    
    while continuar and not usuario:
        mostrar_menu_inicial()
        opcion = input("Seleccione una opción: \n")
        
        if opcion == "1":
            usuario = handle_login()
            if usuario:
                continuar = False
                
        elif opcion == "2":
            handle_registro()
                
        elif opcion == "3":
            print("¡Hasta luego!")
            continuar = False
            clear_screen()
        else:
            print(Fore.RED + "Opción inválida" + Style.RESET_ALL)
    
    return usuario

def menu_garage(usuario):
    """Gestiona la selección/creación de garages - retorna el garage seleccionado o None"""
    crear_archivo_users_garage()
    
    continuar = True
    garage_seleccionado = None
    tarifa = []  # ✅ INICIALIZAR AQUÍ
    admin = usuario.get('admin', False) == 'True'  # Verificar si el usuario es admin
    while continuar and not garage_seleccionado:
        mostrar_menu_garage(usuario)
        opcion = input("Seleccione una opción: \n")
        
        if opcion == "1":
            garage_seleccionado = handle_seleccionar_garage(usuario)
            if garage_seleccionado:
                tarifa = guardar_precios_garage(garage_seleccionado['garage_id'])
                continuar = False
                
        elif opcion == "2":
            garage_seleccionado = handle_crear_garage(usuario)
            if garage_seleccionado:
                tarifa = guardar_precios_garage(garage_seleccionado['garage_id'])  # ✅ AGREGAR AQUÍ TAMBIÉN
                continuar = False
        elif admin:
            if opcion == "3":
                handle_administrar_usuarios()
            elif opcion == "4":
                continuar = False  # Cerrar sesión
        elif opcion == "4":
            continuar = False  # Cerrar sesión
        else:
            print(Fore.RED + "Opción inválida" + Style.RESET_ALL)
    
    return garage_seleccionado, tarifa

def menu_principal(garage_actual, tarifa):
    """Menú principal del sistema - retorna acción a realizar"""
    #SUBO MI GARAGE ACTUAL AL JSON PARA QUE SEA ACCESIBLE DESDE CUALQUIER PARTE DEL PROYECTO
    guardar_estado_garage(garage_actual)    
    
    
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
        handle_actualizar_tarifas,
        handle_imprimir_tarifas,
        handle_mover_vehiculo
    ]
    
    # Acciones especiales (no ejecutan función)
    acciones_especiales = {
        "c": "cambiar_garage",
        "x": "cerrar_sesion",
        "z": "salir",
    }

    try: 
        while continuar and not accion:

            mostrar_menu_principal(garage_actual)
            garage_data = get_garage_data(garage_actual['garage_id'])
            opcion = input("Seleccione una opción: \n")

            if opcion.isdigit():
                indice = int(opcion) - 1  # la lista empieza en 0 y el menú en 1
                if 0 <= indice < len(handlers):
                    if indice == 3:  # Opción 4: registrar salida
                        handlers[indice](garage_actual, garage_data, tarifa)
                    elif indice == 9:  # Opción 10: actualizar tarifas
                        handlers[indice](garage_actual, tarifa)
                        tarifa = guardar_precios_garage(garage_actual['garage_id'])
                        
                    elif indice == 10:  # Opción 11: imprimir tarifas
                        handlers[indice](tarifa)
                    else:
                        handlers[indice](garage_actual, garage_data)
                    continue
            if opcion in acciones_especiales:
                accion = acciones_especiales[opcion]
                continuar = False
            else:
                print(Fore.RED + "Opción inválida. Intente de nuevo." + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.RED + "\nOperación cancelada por el usuario." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}" + Style.RESET_ALL)
    return accion


def main():
    """Función principal que coordina todo el flujo"""

    while True: 
        try:
            programa_activo = True

            while programa_activo:
               
                usuario_actual = menu_inicial()
                if not usuario_actual:
                    programa_activo = False
                    continue

             
                session_active = True
                while session_active and programa_activo:
                    (garage_actual, tarifa) = menu_garage(usuario_actual)
                    guardar_estado_garage(garage_actual)

                    if not garage_actual:
                        session_active = False
                        continue

             
                    menu_activo = True
                    while menu_activo and session_active:
                        resultado = menu_principal(garage_actual, tarifa)
                        tarifa = guardar_precios_garage(garage_actual['garage_id'])

                        if resultado == "cambiar_garage":
                            menu_activo = False
                            clear_screen()

                        elif resultado == "cerrar_sesion":
                            session_active = False
                            menu_activo = False
                            clear_screen()

                        elif resultado == "salir":
                            print("¡Hasta luego!")
                            programa_activo = False
                            session_active = False
                            menu_activo = False
                            clear_screen()

            
            break

        except KeyboardInterrupt:
            print(Fore.RED + "\n\n⚠️ Ejecución cancelada por el usuario (Ctrl + C)." + Style.RESET_ALL)
            print("Saliendo de la aplicación...")
            break

        except Exception as e:
            print(Fore.RED + "\n❌ Ocurrió un error inesperado:" + Style.RESET_ALL)
            print(str(e))
            print("\n¿Qué deseas hacer?")
            print("1) Reintentar")
            print("2) Salir")

            opcion = input("> ").strip()
            if opcion == "1":
                print("\n🔄 Reiniciando la aplicación...\n")
                continue   
            else:
                print("\n👋 Saliendo debido al error inesperado...")
                break


if __name__ == "__main__":
    main()
