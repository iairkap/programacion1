import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cache.json import  guardar_estado_garage, leer_estado_garage
from users.usuarios import user_login, registrar_nuevo_usuario
from users.users_garage import (
    buscar_garage_asociado,
    seleccionar_solo_un_garage,
    asociar_garage_a_usuario, 
    crear_archivo_users_garage, 
    crear_garage
)

from auxiliares.consola import clear_screen






def handle_login():
    """Maneja el login del usuario"""
    usuario = user_login()
    if usuario:
        print(f"¡Bienvenido {usuario['nombre']}!")
        input("Presione Enter para continuar...")
        clear_screen()
        return usuario
    else:
        print("Login fallido")
        input("Presione Enter para continuar...")
        clear_screen()
        return None

def handle_registro():
    """Maneja el registro de nuevo usuario"""
    if registrar_nuevo_usuario():
        print("Usuario registrado. Ahora puede iniciar sesión.")
        input("Presione Enter para continuar...")
        clear_screen()
        return True
    else:
        print("Error en el registro")
        input("Presione Enter para continuar...")
        clear_screen()
        
        return False



def crear_nuevo_garage(usuario):
    """Interfaz para crear un nuevo garage"""
    print("\n=== CREAR NUEVO GARAGE ===")
    
    #logica para preguntarle cuantos pisos y slots por piso
    while True:
        try:
            slots_per_floor = int(input("Ingrese la cantidad de slots por piso (mínimo 5): "))
            floors = int(input("Ingrese la cantidad de pisos (mínimo 1): "))
            if slots_per_floor >= 5 and floors >= 1:
                break
            else:
                print("Por favor, ingrese valores válidos.")
        except ValueError:
            print("Entrada inválida. Intente nuevamente.")

    garage_id = crear_garage(usuario, slots_per_floor=slots_per_floor, floors=floors)

    input("Presione cualquier tecla para continuar...")
    clear_screen()
    
    
    return garage_id

def handle_seleccionar_garage(usuario):
    """Maneja la selección de garage existente"""
    garages = buscar_garage_asociado(usuario['email'])
    if garages:
        garage_seleccionado = seleccionar_solo_un_garage(garages)
        if garage_seleccionado:
            print(f"Garage '{garage_seleccionado['garage_name']}' seleccionado")
            

            return garage_seleccionado
    else:
        print("No tiene garages asociados")
    input("Presione Enter para continuar...")
    clear_screen()
    return None

def handle_crear_garage(usuario):
    """Maneja la creación y selección de nuevo garage"""
    garage_id = crear_nuevo_garage(usuario)
    if garage_id:
        # Buscar el garage recién creado
        garages = buscar_garage_asociado(usuario['email'])
        if garages:
            garage_nuevo = garages[-1]  # El último creado
            print(f"Garage '{garage_nuevo['garage_name']}' creado y seleccionado")
            
            return garage_nuevo
        input("Presione Enter para continuar...")
        clear_screen()
    return None