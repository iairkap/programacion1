import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cache.json import guardar_estado_garage, leer_estado_garage
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
    print(Fore.GREEN + "\n=== CREAR NUEVO GARAGE ===" + Style.RESET_ALL)
    while True:
        try:
            nombre = input("Nombre del garage: ").strip()
            if not nombre:
                print(Fore.RED + "El nombre no puede estar vacío. Intente de nuevo." + Style.RESET_ALL)
                continue

            direccion = input("Dirección: ").strip()
            if not direccion:
                print(Fore.RED + "La dirección no puede estar vacía. Intente de nuevo." + Style.RESET_ALL)
                continue


            slots_per_floor = int(input("Ingrese la cantidad de slots por piso (mínimo 5): ").strip())
            
            if slots_per_floor < 5:
                print(Fore.RED + "La cantidad mínima de slots por piso es 5. Intente de nuevo." + Style.RESET_ALL)
                continue

        
            floors = int(input("Ingrese la cantidad de pisos (mínimo 1 - maximo 10): ").strip())

            if not (1 <= floors <= 10):
                print(Fore.RED + "La cantidad de pisos debe estar entre 1 y 10. Intente de nuevo." + Style.RESET_ALL)
                continue

            # todos los inputs son válidos -> salir del loop
            break

        except KeyboardInterrupt:
            print("\nCreación de garage cancelada por el usuario.")
            input("Presione cualquier tecla para continuar...")
            clear_screen()
            return None
        except ValueError:
            print(Fore.RED + "Entrada inválida. Por favor ingrese valores numéricos donde se requiera." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error en la entrada: {e}. Intente de nuevo." + Style.RESET_ALL)

    # crear el garage y obtener su id
    
    
    garage_id = crear_garage(usuario, nombre, direccion, slots_per_floor=slots_per_floor, floors=floors)
    if not garage_id:
        print(Fore.RED + "No se pudo crear el garage." + Style.RESET_ALL)
        input("Presione cualquier tecla para continuar...")
        clear_screen()
        return None

    # preguntar por configuración de tarifas (pasamos también el nombre para mensajes)
    configurar_tar = input(Fore.LIGHTYELLOW_EX + "¿Desea configurar tarifas para este garage ahora? (s/n): " + Style.RESET_ALL).strip().lower() == "s"
    if configurar_tar:
        agregar_tarifa(garage_id, garage_name=nombre)

    bulk = input(Fore.LIGHTYELLOW_EX + "\n¿Desea configurar los slots ahora? (s para sí): \n" + Style.RESET_ALL).strip().lower()
    if bulk == 's':
        print("Ejecutar la función de actualizar tipo de slots")

    input("Presione cualquier tecla para continuar...")
    clear_screen()
    return garage_id

def handle_actualizar_tarifas(garage, garage_data=None):
    """Maneja la actualización de tarifas del garage"""
    print("\n=== ACTUALIZAR TARIFAS DEL GARAGE ===")
    agregar_tarifa(garage['garage_id'], garage_name=garage['garage_name'])
    return garage


def agregar_tarifa(garage_id, garage_name=None):
    """Función independiente para agregar tarifas a files/tarifas.csv.
    Guarda valores numéricos: tipo (1/2/3), periodo_mensual (True/False)"""
    tipo_map = {"1": (1, "moto"), "2": (2, "auto"), "3": (3, "camioneta")}
    periodo_map = {"1": (False, "diario"), "2": (True, "mensual")}

    display_name = f" '{garage_name}'" if garage_name else f" id={garage_id}"
    print(f"\nConfigurar tarifas para el garage{display_name}. Escriba 'fin' para terminar.")
    
    while True:
        tipo_slot_in = input("Tipo (1 Moto, 2 Auto, 3 Camioneta/suv) o 'fin': ").strip().lower()
        if tipo_slot_in == "fin":
            break

        if tipo_slot_in not in tipo_map:
            print(Fore.RED + "Tipo inválido. Use 1/2/3." + Style.RESET_ALL)
            continue
        
        tipo_num, tipo_nombre = tipo_map[tipo_slot_in]

        periodo_in = input("Periodo (1: diario, 2: mensual): ").strip()
        if periodo_in not in periodo_map:
            print(Fore.RED + "Periodo inválido. Use 1 o 2." + Style.RESET_ALL)
            continue

        periodo_mensual, periodo_nombre = periodo_map[periodo_in]

        precio_str = input("Precio (número): ").strip()
        try:
            precio = float(precio_str)
            if precio < 0:
                raise ValueError
        except ValueError:
            print(Fore.RED + "Precio inválido. Ingrese un número mayor o igual a 0." + Style.RESET_ALL)
            continue

        descripcion = input("Descripción (opcional): ").strip()

        # Guardar con valores numéricos
        save_tarifa_to_csv(garage_id, tipo_num, periodo_mensual, precio, descripcion)
        print(Fore.GREEN + f"Tarifa guardada: {tipo_nombre}/{periodo_nombre} = {precio}" + Style.RESET_ALL)

    # fin de la configuración de tarifas
    input("Presione cualquier tecla para continuar...")
    clear_screen()
    return True




def save_tarifa_to_csv(garage_id, tipo_num, periodo_mensual, precio, descripcion=""):
    """Escribe o actualiza tarifa en CSV con valores numéricos.
    tipo_num: 1=moto, 2=auto, 3=camioneta
    periodo_mensual: True=mensual, False=diario
    
    Si ya existe tarifa para garage_id/tipo_num/periodo_mensual, la actualiza.
    Si no existe, la crea.
    """
    csv_path = "files/tarifas.csv"
    
    # Intentar leer archivo existente
    lineas_existentes = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            lineas_existentes = f.readlines()
    except FileNotFoundError:
        # Archivo no existe, se creará con header
        lineas_existentes = []
    
    # Procesar líneas
    lineas_nuevas = []
    tarifa_encontrada = False
    
    # Si hay líneas, mantener header
    if lineas_existentes:
        lineas_nuevas.append(lineas_existentes[0])  # Header
        
        # Procesar datos (desde línea 1 en adelante)
        for i in range(1, len(lineas_existentes)):
            linea = lineas_existentes[i].strip()
            if not linea:
                continue
            
            partes = linea.split(",")
            if len(partes) >= 3:
                garage_id_csv = partes[0]
                tipo_csv = partes[1]
                periodo_csv = partes[2]
                
                # Comparar si es la misma tarifa
                if (garage_id_csv == str(garage_id) and 
                    tipo_csv == str(tipo_num) and 
                    periodo_csv == str(periodo_mensual)):
                    # Actualizar línea
                    linea_nueva = f"{garage_id},{tipo_num},{periodo_mensual},{precio},{descripcion}\n"
                    lineas_nuevas.append(linea_nueva)
                    tarifa_encontrada = True
                else:
                    # Mantener línea original
                    lineas_nuevas.append(linea + "\n")
            else:
                lineas_nuevas.append(linea + "\n")
    
    # Si no se encontró, agregar nueva tarifa
    if not tarifa_encontrada:
        linea_nueva = f"{garage_id},{tipo_num},{periodo_mensual},{precio},{descripcion}\n"
        if not lineas_existentes:
            # Crear con header
            lineas_nuevas = [
                "garage_id,tipo,periodo_mensual,precio,moneda,descripcion\n",
                linea_nueva
            ]
        else:
            lineas_nuevas.append(linea_nueva)
    
    # Escribir archivo completo
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            f.writelines(lineas_nuevas)
    except Exception as e:
        print(Fore.RED + f"Error al guardar tarifa: {e}" + Style.RESET_ALL)
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
        # la tarifa ya se pudo haber configurado dentro de crear_nuevo_garage
        if garages:
            garage_nuevo = garages[-1]  # El último creado
            print(f"Garage '{garage_nuevo['garage_name']}' creado y seleccionado")
            return garage_nuevo
        input(Fore.LIGHTYELLOW_EX + "Presione cualquier tecla para continuar..." + Style.RESET_ALL)
        clear_screen()
    return None


def handle_actualizar_tipo_slots(garage, garage_data=None):
    """Maneja la actualización del tipo de slots en el garage"""
    print("\n=== ACTUALIZAR TIPO DE SLOTS ===")
    garage_id = garage['garage_id']
    bulk = input("¿Desea actualizar el tipo de varios slots a la vez? (s/n): ").lower() == 's'
    data = []
    archivo_editado = False
    if bulk:
        print("\nSe creara un csv en directorio actual llamado 'config_slots.csv' para actualizar los tipos de slots\n")
        ruta_csv = generar_csv_slots()
        if os.path.exists(ruta_csv):
            print(Fore.RED + f"Por favor, edite el archivo en: {os.path.abspath(ruta_csv)}" + Style.RESET_ALL)
            print("Una vez editado, guarde el archivo y vuelva aquí para continuar.")
            archivo_editado = input("\n¿Ha editado y guardado el archivo? (s/n): \n").lower() == 's'
        if archivo_editado:
            print(Fore.GREEN + f"\n{garage['garage_name']} ha sido actualizado con exito." + Style.RESET_ALL)
            print(Fore.GREEN + "\nContinuando con la actualización desde el archivo existente..."+ Style.RESET_ALL)
            input(Fore.YELLOW + "\nPresione cualquier tecla para continuar..."+ Style.RESET_ALL)
            clear_screen()
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
            data.append(crear_data_para_actualizar_slot(slot_id=slot_id, tipo_slot=tipo_slot))
            actualizar_slots(garage_id, data)
            print(f"Garage con id {garage_id} actualizado correctamente ✅")
        except Exception as e:
            print(f"Error al actualizar el garage: {e}")
    return garage


def handle_actualizar_slots(garage, garage_data=None):
    """Maneja la actualización de información de slots en el garage"""
    print("\n=== ACTUALIZAR INFORMACIÓN DE SLOTS ===")
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
            patente = input("Ingrese la patente del vehículo: ").strip()
            hora_entrada = input("Ingrese la hora de entrada (hs:min): ").strip()
            tipo_vehiculo = input("Ingrese el tipo de vehículo: ").strip()
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

