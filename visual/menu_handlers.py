import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from users.usuarios import user_login, registrar_nuevo_usuario
from users.users_garage import (
    buscar_garage_asociado,
    seleccionar_solo_un_garage,
    asociar_garage_a_usuario, 
    crear_archivo_users_garage, 
    crear_garage
)

def handle_login():
    """Maneja el login del usuario"""
    usuario = user_login()
    if usuario:
        print(f"¡Bienvenido {usuario['nombre']}!")
        return usuario
    else:
        print("Login fallido")
        return None

def handle_registro():
    """Maneja el registro de nuevo usuario"""
    if registrar_nuevo_usuario():
        print("Usuario registrado. Ahora puede iniciar sesión.")
        return True
    else:
        print("Error en el registro")
        return False

def crear_nuevo_garage(usuario):
    """Interfaz para crear un nuevo garage"""
    print("\n=== CREAR NUEVO GARAGE ===")
    #Por ahora me lo esta agregando sen  el file users-garage.csv
    garage = crear_garage(usuario)
    
    
    return garage

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
    return None

def handle_crear_garage(usuario):
    """Maneja la creación y selección de nuevo garage"""
    if crear_nuevo_garage(usuario):
        # Buscar el garage recién creado
        garages = buscar_garage_asociado(usuario['email'])
        if garages:
            garage_nuevo = garages[-1]  # El último creado
            print(f"Garage '{garage_nuevo['garage_name']}' creado y seleccionado")
            return garage_nuevo
    return None