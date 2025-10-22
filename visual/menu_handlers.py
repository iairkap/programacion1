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
    crear_garage,
    actualizar_slot,
    actualizar_slots,
    generar_csv_slots,
    crear_data_para_actualizar_slot,
    crear_data_para_actualizar_tipo_slots,
)

from auxiliares.consola import clear_screen
from colorama import Fore, Style







def handle_login():
    """Maneja el login del usuario"""
    usuario = user_login()
    if usuario:
        print(Fore.GREEN + f"\n\n¡Bienvenido {usuario['nombre']}!" + Style.RESET_ALL)
        input(Fore.LIGHTYELLOW_EX + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        clear_screen()
        return usuario
    else:
        print("Login fallido")
        input(Fore.LIGHTYELLOW_EX + "Presione cualquier tecla para continuar..." + Style.RESET_ALL)
        clear_screen()
        return None

def handle_registro():
    """Maneja el registro de nuevo usuario"""
    if registrar_nuevo_usuario():
        print("Usuario registrado. Ahora puede iniciar sesión.")
        input(Fore.LIGHTYELLOW_EX + "Presione cualquier tecla para continuar..." + Style.RESET_ALL)
        clear_screen()
        return True
    else:
        print("Error en el registro")
        input(Fore.LIGHTYELLOW_EX + "Presione cualquier tecla para continuar..." + Style.RESET_ALL)
        clear_screen()
        
        return False



def crear_nuevo_garage(usuario):
    """Interfaz para crear un nuevo garage"""
    print("\n=== CREAR NUEVO GARAGE ===")
    
    #logica para preguntarle cuantos pisos y slots por piso
    while True:
        try:
            nombre = input("Nombre del garage: ").strip()
            if not nombre:
                break
                print("El nombre no puede estar vacío. Intente de nuevo.")
            direccion = input("Dirección: ").strip()
            if not direccion:
                break
                print("La dirección no puede estar vacía. Intente de nuevo.")
            slots_per_floor = int(input("Ingrese la cantidad de slots por piso (mínimo 5): "))
            floors = int(input("Ingrese la cantidad de pisos (mínimo 1): "))
            if slots_per_floor >= 5 and floors >= 1:
                break
            else:
                print("Por favor, ingrese valores válidos.")

        except KeyboardInterrupt:
            print("\nCreación de garage cancelada por el usuario.")
            input("Presione cualquier tecla para continuar...")
            clear_screen()
            return None
    garage_id = crear_garage(usuario,nombre, direccion, slots_per_floor=slots_per_floor, floors=floors)

    input("Presione cualquier tecla para continuar...")
    clear_screen()
    return garage_id

def handle_seleccionar_garage(usuario):
    """Maneja la selección de garage existente"""
    garages = buscar_garage_asociado(usuario['email'])
    if garages:
        garage_seleccionado = seleccionar_solo_un_garage(garages)
        if garage_seleccionado:
            print(Fore.GREEN + f"Garage '{garage_seleccionado['garage_name']}' seleccionado" + Style.RESET_ALL)
            clear_screen()
            return garage_seleccionado
    else:
        print(Fore.RED + "No tiene garages asociados" + Style.RESET_ALL)
    input(Fore.LIGHTYELLOW_EX + "Presione cualquier tecla para continuar..." + Style.RESET_ALL)
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
        input(Fore.LIGHTYELLOW_EX + "Presione cualquier tecla para continuar..." + Style.RESET_ALL)
        clear_screen()
    return None

def handle_actualizar_tipo_slots(garage, garage_data= None):
    """Maneja la actualización del tipo de slots en el garage"""
    print("\n=== ACTUALIZAR TIPO DE SLOTS ===")
    garage_id = garage['garage_id']
    bulk = input("¿Desea actualizar el tipo de varios slots a la vez? (s/n): ").lower() == 's'
    data = []
    archivo_editado = False
    if bulk:
        print("Se creara un csv en directorio actual llamado 'config_slots.csv' para actualizar los tipos de slots")
        ruta_csv = generar_csv_slots()
        if os.path.exists(ruta_csv):
            print(f"Por favor, edite el archivo en: {os.path.abspath(ruta_csv)}")
            print("Una vez editado, guarde el archivo y vuelva aquí para continuar.")
            archivo_editado = input("¿Ha editado y guardado el archivo? (s/n): ").lower() == 's'
        if archivo_editado:
            print("Continuando con la actualización desde el archivo existente...")
            data = crear_data_para_actualizar_tipo_slots(ruta_csv)
            actualizar_slots(garage_id, data)
        else:
            print("Actualización postergada. Por favor, edite el archivo y vuelva a intentarlo.")
            return garage
    else:
        print("Actualización de un solo slot")
        slot_id = int(input("Ingrese el ID del slot a actualizar: "))
        tipo_slot = input("Ingrese el nuevo tipo de slot para actualizar: ")
        try:
            print(f"Actualizando tipo de slot para el garage '{garage['garage_name']}'...")
            data.append(crear_data_para_actualizar_slot( slot_id=slot_id, tipo_slot=tipo_slot))
            actualizar_slots(garage_id, data)
            print(f"Garage con id {garage_id} actualizado correctamente ✅")
        except Exception as e:
            print(f"Error al actualizar el garage: {e}")
    return garage

def handle_actualizar_slots(garage, garage_data = None):
    """Maneja la actualización de información de slots en el garage"""
    print("\n=== ACTUALIZAR INFORMACIÓN DE SLOTS ===")
    # Aquí se implementaría la lógica para actualizar los slots
    data = []
    garage_id = garage['garage_id']
    seguir_actualizando = True
    print(f"Actualizando slots para el garage '{garage['garage_name']}'...")
    try:
        while seguir_actualizando:
            slot_id = input("Ingrese el ID del slot a actualizar (o 'q' para salir): ")
            if slot_id.lower() == 'q':
                break
            ocupado = input("¿El slot está ocupado? (s/n): ").lower() == 's'
            reservado_mensual = input("¿El slot es reservado mensual? (s/n): ").lower() == 's'
            patente = input("Ingrese la patente del vehículo: ")   
            hora_entrada= input("Ingrese la hora de entrada (hs:min): ")## Actualizar con datetime.today() si se puede
            tipo_vehiculo= input("Ingrese el tipo de vehículo: ")
            data_slot = crear_data_para_actualizar_slot(
                slot_id=slot_id,
                ocupado=ocupado,
                reservado_mensual=reservado_mensual if reservado_mensual in ['s', 'n'] else None,
                patente=patente if patente else None,
                hora_entrada=hora_entrada if hora_entrada else None,
                tipo_vehiculo=tipo_vehiculo if tipo_vehiculo else None)
            data.append(data_slot)
            seguir_actualizando = input("¿Desea actualizar otro slot? (s/n): ").lower() == 's'
        actualizar_slots(garage_id, data)
        print(f"Slot {slot_id} actualizado correctamente.")   
    except Exception as e:
        print(f"Error al actualizar el garage: {e}")
    return garage

# def handle_actualizar_garage(usuario):
#     """Maneja la actualizacion de los datos del garage"""
#     garages = buscar_garage_asociado(usuario['email'])
#     if garages:
#         garage_seleccionado = seleccionar_solo_un_garage(garages)
#         if garage_seleccionado:
#             print(f"Garage cambiado a '{garage_seleccionado['garage_name']}'")
#             return garage_seleccionado
#     else:
#         print("No tiene garages asociados")
#     return None