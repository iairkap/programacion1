import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from garage.garage_util import (
    contar_espacios_libres,
    buscar_por_patente,
    buscar_espacio_libre,
    contar_espacios_libres_por_tipo
)
from users.interaccion_usuario import (
    pedir_piso,
    pedir_patente,
    pedir_tipo_vehiculo,
    mostrar_estado_garage)
from main import (
    registrar_entrada_auto,
    contar_por_tipo_vehiculo,
    chequear_espacio_libre, 
    registrar_salida_vehiculo,
    modificar_vehiculo,
    mostrar_estadisticas_rapidas)

from users.usuarios import(
    user_login,
    registrar_nuevo_usuario
)

from users.users_garage import (
    buscar_garage_asociado,
    seleccionar_solo_un_garage,
    crear_archivo_users_garage,
    asociar_garage_a_usuario
)

from garage.mockdata import GARAGE, COSTOS

# Variables globales para el usuario y garage seleccionado
usuario_actual = None
garage_actual = None

def mostrar_menu_inicial():
    """Menú de inicio de sesión y registro"""
    print("\n=== BIENVENIDO A SLOTMASTER ===")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")

def mostrar_menu_garage():
    """Menú para seleccionar o crear garage"""
    print(f"\n=== GESTIÓN DE GARAGES - {usuario_actual['nombre']} ===")
    print("1. Seleccionar garage existente")
    print("2. Crear nuevo garage")
    print("3. Cerrar sesión")

def mostrar_menu_principal():
    """Menú principal del sistema (el actual)"""
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
    """Gestiona el login y registro"""
    global usuario_actual
    
    while True:
        mostrar_menu_inicial()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            usuario_actual = user_login()
            if usuario_actual:
                print(f"¡Bienvenido {usuario_actual['nombre']}!")
                return True
            else:
                print("Login fallido")
                
        elif opcion == "2":
            if registrar_nuevo_usuario():
                print("Usuario registrado. Ahora puede iniciar sesión.")
            else:
                print("Error en el registro")
                
        elif opcion == "3":
            print("¡Hasta luego!")
            return False
            
        else:
            print("Opción inválida")

def crear_nuevo_garage():
    """Interfaz para crear un nuevo garage"""
    print("\n=== CREAR NUEVO GARAGE ===")
    nombre = input("Nombre del garage: ")
    direccion = input("Dirección: ")
    
    while True:
        try:
            pisos = int(input("Cantidad de pisos: "))
            if pisos > 0:
                break
            else:
                print("Debe ser mayor a 0")
        except ValueError:
            print("Ingrese un número válido")
    
    while True:
        try:
            slots_por_piso = int(input("Slots por piso: "))
            if slots_por_piso > 0:
                break
            else:
                print("Debe ser mayor a 0")
        except ValueError:
            print("Ingrese un número válido")
    
    asociar_garage_a_usuario(
        usuario_actual['email'], 
        nombre, 
        direccion, 
        pisos, 
        slots_por_piso
    )
    return True

def menu_garage():
    """Gestiona la selección/creación de garages"""
    global garage_actual
    
    crear_archivo_users_garage()
    
    while True:
        mostrar_menu_garage()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            garages = buscar_garage_asociado(usuario_actual['email'])
            if garages:
                garage_actual = seleccionar_solo_un_garage(garages)
                if garage_actual:
                    print(f"Garage '{garage_actual['garage_name']}' seleccionado")
                    return True
            else:
                print("No tiene garages asociados")
                
        elif opcion == "2":
            if crear_nuevo_garage():
                # Buscar el garage recién creado
                garages = buscar_garage_asociado(usuario_actual['email'])
                if garages:
                    garage_actual = garages[-1]  # El último creado
                    print(f"Garage '{garage_actual['garage_name']}' creado y seleccionado")
                    return True
                    
        elif opcion == "3":
            return False
            
        else:
            print("Opción inválida")

def menu_principal():
    """Menú principal del sistema (lógica actual)"""
    garage = GARAGE  # Usar el garage mock por ahora
    
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
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

        elif opcion == "2":
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

        elif opcion == "3":
            registrar_entrada_auto(garage)

        elif opcion == "4":
            patente = pedir_patente()
            if registrar_salida_vehiculo(garage, patente):
                print("Salida registrada correctamente.")
            else:
                print("Patente no encontrada.")

        elif opcion == "5":
            patente = pedir_patente()
            nuevo_tipo = pedir_tipo_vehiculo()
            nueva_patente = input("Nueva patente (dejar vacío para no cambiar): ").strip().upper()
            if nueva_patente == "":
                nueva_patente = None
            if modificar_vehiculo(garage, patente, nuevo_tipo, nueva_patente):
                print("Vehículo modificado correctamente.")
            else:
                print("Patente no encontrada.")

        elif opcion == "6":
            mostrar_estado_garage(garage)

        elif opcion == "7":
            patente = pedir_patente()
            pos = buscar_por_patente(garage, patente)
            if pos != (-1, -1):
                print(f"Vehículo encontrado en Piso {pos[0]}, Slot {pos[1]}")
            else:
                print("Vehículo no encontrado.")

        elif opcion == "8":
            mostrar_estadisticas_rapidas(garage)
            
        elif opcion == "9":
            return "cambiar_garage"
            
        elif opcion == "10":
            return "cerrar_sesion"
            
        elif opcion == "11":
            return "salir"
            
        else:
            print("Opción inválida. Intente de nuevo.")

def main():
    """Función principal que coordina todo el flujo"""
    while True:
        # 1. Login/Registro
        if not menu_inicial():
            break
            
        # 2. Selección/Creación de garage
        session_active = True
        while session_active:
            if not menu_garage():
                session_active = False
                continue
                
            # 3. Menú principal
            while True:
                resultado = menu_principal()
                
                if resultado == "cambiar_garage":
                    break  # Volver al menú de garages
                elif resultado == "cerrar_sesion":
                    session_active = False
                    break  # Volver al login
                elif resultado == "salir":
                    print("¡Hasta luego!")
                    return

if __name__ == "__main__":
    main()