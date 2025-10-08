import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from users.users_garage import crear_archivo_users_garage
from visual.menu_handlers import (
    handle_login, 
    handle_registro, 
    handle_seleccionar_garage, 
    handle_crear_garage
)
from visual.menu_principal_handlers import (
    handle_consultar_espacios_libres,
    handle_consultar_vehiculos_estacionados,
    handle_ingresar_vehiculo,
    handle_registrar_salida,
    handle_editar_vehiculo,
    handle_mostrar_estado_garage,
    handle_buscar_vehiculo,
    handle_estadisticas_rapidas
)
from garage.mockdata import GARAGE

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

def mostrar_menu_principal(garage_actual):
    """Menú principal del sistema"""
    print(f"\n=== MENÚ PRINCIPAL - {garage_actual['garage_name']} ===")
    print("1. Consultar espacios libres")
    print("2. Consultar cantidad de vehículos estacionados")
    print("3. Ingresar un vehículo")
    print("4. Registrar salida de un vehículo")
    print("5. Editar un vehículo")
    print("6. Mostrar estado del garage")
    print("7. Buscar vehículo por patente")
    print("8. Estadísticas rápidas")
    print("9. Cambiar garage")
    print("10. Cerrar sesión")
    print("11. Salir")

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
            print("Opción inválida")
    
    return usuario

def menu_garage(usuario):
    """Gestiona la selección/creación de garages - retorna el garage seleccionado o None"""
    crear_archivo_users_garage()
    
    continuar = True
    garage_seleccionado = None
    
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
            print("Opción inválida")
    
    return garage_seleccionado

def menu_principal(garage_actual):
    """Menú principal del sistema - retorna acción a realizar"""
    garage = GARAGE  # Usar el garage mock por ahora
    
    continuar = True
    accion = None
    
    while continuar and not accion:
        mostrar_menu_principal(garage_actual)
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            handle_consultar_espacios_libres(garage)

        elif opcion == "2":
            handle_consultar_vehiculos_estacionados(garage)

        elif opcion == "3":
            handle_ingresar_vehiculo(garage)

        elif opcion == "4":
            handle_registrar_salida(garage)

        elif opcion == "5":
            handle_editar_vehiculo(garage)

        elif opcion == "6":
            handle_mostrar_estado_garage(garage)

        elif opcion == "7":
            handle_buscar_vehiculo(garage)

        elif opcion == "8":
            handle_estadisticas_rapidas(garage)
            
        elif opcion == "9":
            accion = "cambiar_garage"
            continuar = False
            
        elif opcion == "10":
            accion = "cerrar_sesion"
            continuar = False
            
        elif opcion == "11":
            accion = "salir"
            continuar = False
            
        else:
            print("Opción inválida. Intente de nuevo.")
    
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
            garage_actual = menu_garage(usuario_actual)
            if not garage_actual:
                session_active = False
                continue
                
            # 3. Menú principal
            menu_activo = True
            while menu_activo and session_active:
                resultado = menu_principal(garage_actual)
                
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