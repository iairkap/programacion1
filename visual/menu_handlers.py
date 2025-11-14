import sys
import os
###Agregando comentario para que git detecte los cambios D:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from users.pass_logic import login
from users.usuarios import (
    user_login,
    registrar_nuevo_usuario,
    chequear_existencia_email,
    asignar_admin,
    eliminar_admin
)
from users.users_garage import (
    buscar_garage_asociado,
    seleccionar_solo_un_garage,
    crear_garage,
    actualizar_slots,
    generar_csv_slots,
    crear_data_para_actualizar_slot,
    crear_data_para_actualizar_tipo_slots,
    mostrar_garages_asociados,
    )
from auxiliares.consola import clear_screen
from colorama import Fore, Style
from garage.garage_util import buscar_por_patente
from users.interaccion_usuario import pedir_patente
from garage.slot_utils import validacion_slots_ok, buscar_piso_por_slot_id, get_slot_in_piso, buscar_slots_por_tipo, tipos_de_slot_definidos, slot_ocupado
from menu_principal_handlers import handle_mostrar_estado_garage

def handle_login():
    """Maneja el login del usuario"""
    try:
        email, password = login()
        usuario = user_login(email)
        if usuario:
            print(Fore.GREEN + f"\n\n¡Bienvenido {usuario['nombre']}!" + Style.RESET_ALL)
            clear_screen()
            return usuario
        else:
            print("Login fallido")
            clear_screen()
            return None
    except Exception as e:
        print(Fore.RED + f"Error durante el login. {e}" + Style.RESET_ALL)
        clear_screen()
        return None 

def handle_registro():
    """Maneja el registro de nuevo usuario"""
    email,password = login(crear_usuario=True)
    if chequear_existencia_email(email):
        user_login(email)
        clear_screen()
        return 
    elif registrar_nuevo_usuario(email):
        print(Fore.GREEN + "Usuario registrado. Ahora puede iniciar sesión." + Style.RESET_ALL)
        clear_screen()
        return True
    else:
        print(Fore.RED + "Error en el registro" + Style.RESET_ALL)
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


            slots_per_floor = int(input("Ingrese la cantidad de slots por piso (mínimo 5 - maximo 25): ").strip())
            
            if not (5 <= slots_per_floor <= 25):
                print(Fore.RED + "La cantidad mínima de slots por piso es 5, el maximo es de 25. Intente de nuevo." + Style.RESET_ALL)
                continue

        
            floors = int(input("Ingrese la cantidad de pisos (mínimo 1 - maximo 10): ").strip())

            if not (1 <= floors <= 10):
                print(Fore.RED + "La cantidad de pisos debe estar entre 1 y 10. Intente de nuevo." + Style.RESET_ALL)
                continue

            # todos los inputs son válidos -> salir del loop
            break

        except KeyboardInterrupt:
            print("\nCreación de garage cancelada por el usuario.")
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
        clear_screen()
        return None

    # preguntar por configuración de tarifas (pasamos también el nombre para mensajes)
    configurar_tar = input(Fore.LIGHTYELLOW_EX + "¿Desea configurar tarifas para este garage ahora? (s/n): " + Style.RESET_ALL).strip().lower() == "s"
    if configurar_tar:
        agregar_tarifa(garage_id, garage_name=nombre)

    # Preguntar por configuración de slots
    configurar_slots = input(Fore.LIGHTYELLOW_EX + "\n¿Desea configurar los slots ahora? (s/n): \n" + Style.RESET_ALL).strip().lower() == "s"
    if configurar_slots:
        # Crear objeto garage temporal para pasar a la función
        garage_temp = {
            'garage_id': garage_id,
            'garage_name': nombre,
            'floors': floors,
            'slots_per_floor': slots_per_floor
        }
        configurar_slots_bulk(garage_temp)

    clear_screen()
    return garage_id

def handle_actualizar_tarifas(garage, garage_data=None):
    """Maneja la actualización de tarifas del garage"""
    print(Fore.GREEN + "\n=== ACTUALIZAR TARIFAS DEL GARAGE ===" + Style.RESET_ALL)
    agregar_tarifa(garage['garage_id'], garage_name=garage['garage_name'])
    return garage


def agregar_tarifa(garage_id, garage_name=None):
    """Función mejorada para actualizar tarifas con vista previa y confirmación"""
    from constantes.tarifa import guardar_precios_garage
    
    # Obtener tarifas actuales (retorna lista de listas)
    tarifas_lista = guardar_precios_garage(garage_id)
    
    # Convertir a diccionario {(tipo, periodo_mensual): precio}
    tarifas_actuales = {}
    for tarifa in tarifas_lista:
        if len(tarifa) >= 4:
            try:
                tipo = int(tarifa[1])
                periodo_mensual = tarifa[2] == "True"
                precio = float(tarifa[3])
                tarifas_actuales[(tipo, periodo_mensual)] = precio
            except (ValueError, IndexError):
                continue
    
    display_name = f"'{garage_name}'" if garage_name else f"ID {garage_id}"
    print(f"\n{Fore.CYAN}Garage: {display_name}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    
    # Mostrar tarifas actuales
    print(f"\n{Fore.CYAN}TARIFAS ACTUALES:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
    print(f"{'VEHÍCULO':<20} {'DIARIO':<20} {'MENSUAL':<20}")
    print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
    
    # Mostrar moto
    moto_d = tarifas_actuales.get((1, False), 0)
    moto_m = tarifas_actuales.get((1, True), 0)
    print(f"{'Moto':<20} ${moto_d:<19.2f} ${moto_m:<19.2f}")
    
    # Mostrar auto
    auto_d = tarifas_actuales.get((2, False), 0)
    auto_m = tarifas_actuales.get((2, True), 0)
    print(f"{'Auto':<20} ${auto_d:<19.2f} ${auto_m:<19.2f}")
    
    # Mostrar camioneta
    cam_d = tarifas_actuales.get((3, False), 0)
    cam_m = tarifas_actuales.get((3, True), 0)
    print(f"{'Camioneta/SUV':<20} ${cam_d:<19.2f} ${cam_m:<19.2f}")
    print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}\n")
    
    # Estructura para las nuevas tarifas
    nuevas_tarifas = []
    tipo_nombres = {1: "Moto", 2: "Auto", 3: "Camioneta/SUV"}
    periodo_nombres = {False: "Diario", True: "Mensual"}
    
    print(f"{Fore.GREEN}Ingrese las nuevas tarifas (presione ENTER para mantener actual):{Style.RESET_ALL}\n")
    
    # Pedir tarifas para cada tipo y periodo
    for tipo_num in [1, 2, 3]:
        for periodo_mensual in [False, True]:
            tipo_nombre = tipo_nombres[tipo_num]
            periodo_nombre = periodo_nombres[periodo_mensual]
            actual = tarifas_actuales.get((tipo_num, periodo_mensual), 0)
            
            while True:
                precio_str = input(f"{tipo_nombre} {periodo_nombre} (actual: ${actual:.2f}): $").strip()
                
                # Si presiona ENTER, mantener valor actual
                if precio_str == "":
                    nuevas_tarifas.append((tipo_num, periodo_mensual, actual))
                    break
                
                # Validar precio
                try:
                    precio = float(precio_str)
                    if precio < 0:
                        print(Fore.RED + "  ❌ El precio no puede ser negativo" + Style.RESET_ALL)
                        continue
                    nuevas_tarifas.append((tipo_num, periodo_mensual, precio))
                    break
                except ValueError:
                    print(Fore.RED + "  ❌ Ingrese un número válido" + Style.RESET_ALL)
    
    # Mostrar resumen de cambios
    print(f"\n{Fore.CYAN}RESUMEN DE CAMBIOS:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
    hay_cambios = False
    
    for tipo_num, periodo_mensual, precio_nuevo in nuevas_tarifas:
        precio_actual = tarifas_actuales.get((tipo_num, periodo_mensual), 0)
        if precio_nuevo != precio_actual:
            hay_cambios = True
            tipo_nombre = tipo_nombres[tipo_num]
            periodo_nombre = periodo_nombres[periodo_mensual]
            print(f"{tipo_nombre} {periodo_nombre}: ${precio_actual:.2f} → {Fore.GREEN}${precio_nuevo:.2f}{Style.RESET_ALL}")
    
    if not hay_cambios:
        print(f"{Fore.YELLOW}No hay cambios para guardar{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
        clear_screen()
        return True
    
    print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
    
    # Confirmar cambios
    while True:
        confirmacion = input(f"\n{Fore.YELLOW}¿Guardar cambios? (s/n): {Style.RESET_ALL}").strip().lower()
        if confirmacion in ['s', 'si', 'yes', 'y']:
            # Guardar todas las tarifas
            for tipo_num, periodo_mensual, precio in nuevas_tarifas:
                save_tarifa_to_csv(garage_id, tipo_num, periodo_mensual, precio)
            print(f"\n{Fore.GREEN}✅ Tarifas actualizadas exitosamente{Style.RESET_ALL}")
            clear_screen()
            return True
        elif confirmacion in ['n', 'no']:
            print(f"{Fore.RED}❌ Cambios cancelados{Style.RESET_ALL}")
            clear_screen()
            return False
        else:
            print(Fore.RED + "Responda 's' o 'n'" + Style.RESET_ALL)


def save_tarifa_to_csv(garage_id, tipo_num, periodo_mensual, precio):
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
                    linea_nueva = f"{garage_id},{tipo_num},{periodo_mensual},{precio}\n"
                    lineas_nuevas.append(linea_nueva)
                    tarifa_encontrada = True
                else:
                    # Mantener línea original
                    lineas_nuevas.append(linea + "\n")
            else:
                lineas_nuevas.append(linea + "\n")
    
    # Si no se encontró, agregar nueva tarifa
    if not tarifa_encontrada:
        linea_nueva = f"{garage_id},{tipo_num},{periodo_mensual},{precio}\n"
        if not lineas_existentes:
            # Crear con header
            lineas_nuevas = [
                "garage_id,tipo,periodo_mensual,precio\n",
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
    admin = usuario.get("admin", False) == "True"
    if admin:
        cant_garages_asociados = mostrar_garages_asociados(usuario["email"], show_all=True)
    else: 
        cant_garages_asociados = mostrar_garages_asociados(usuario["email"])
    if cant_garages_asociados != 0:
        garage_seleccionado = seleccionar_solo_un_garage(usuario["email"], cant_garages_asociados,admin=admin)
        if garage_seleccionado:
            print(Fore.GREEN + f"Garage '{garage_seleccionado['garage_name']}' seleccionado" + Style.RESET_ALL)
            clear_screen()
            return garage_seleccionado
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
        clear_screen()
    return None


def handle_actualizar_tipo_slot(garage_data, garage):
    data = []
    garage_id = garage.get('garage_id', 0)

    print("Actualización de un solo slot")

    while True:
        slot_input = input(
            "Ingrese el ID del slot a actualizar (o 'v' para ver slots disponibles | 's' para salir): "
        ).strip().lower()

        if slot_input == "s":
            return

        if slot_input == "v":
            print("\n📌 Slots disponibles:")
            handle_mostrar_estado_garage(garage, garage_data)
            print("")
            continue

        try:
            slot_id = int(slot_input)
        except ValueError:
            print("❌ Debe ingresar un número válido, 'v' o 's'. Intente de nuevo.")
            continue

        if slot_ocupado(garage_data, slot_id):
            print(Fore.YELLOW +
                  "⚠️ El slot está ocupado. Solo puede actualizar el tipo si está vacío."
                  + Style.RESET_ALL)
            return
        else:
            break

    while True:
        tipo_slot = input("Ingrese el nuevo tipo de slot (moto/auto/camioneta | 's' para salir): ").strip().lower()

        if tipo_slot == "s":
            return

        if tipo_slot not in ('moto', 'auto', 'camioneta'):
            print("❌ El tipo de slot es inválido. Intente nuevamente.")
        else:
            break

    piso = buscar_piso_por_slot_id(slot_id, garage)

    try:
        print(f"\nActualizando tipo de slot para el garage '{garage['garage_name']}'...")

        data.append(
            crear_data_para_actualizar_slot(
                slot_id=slot_id,
                tipo_slot=tipo_slot,
                piso=piso
            )
        )

        actualizar_slots(garage_id, data)

        print(f"Garage con ID {garage_id} actualizado correctamente ✅")

    except Exception as e:
        print(f"❌ Error al actualizar el garage: {e}")

def handle_actualizar_tipo_slots(garage, garage_data=None):
    """Maneja la actualización del tipo de slots en el garage"""
    print("\n=== ACTUALIZAR TIPO DE SLOTS ===")
    garage_id = garage['garage_id']
    data = []
    archivo_editado = False
    tipos_slots = tipos_de_slot_definidos(garage, garage_data)
    bulk = input("¿Desea actualizar el tipo de varios slots a la vez? (s/n): ").lower() == 's'
    if bulk and not tipos_slots:
        print("\nSe creara un csv en directorio actual llamado 'config_slots.csv' para actualizar los tipos de slots\n")
        ruta_csv = generar_csv_slots(garage)
        if os.path.exists(ruta_csv):
            print(Fore.RED + f"Por favor, edite el archivo en: {os.path.abspath(ruta_csv)}" + Style.RESET_ALL)
            print("Una vez editado, guarde el archivo y vuelva aquí para continuar.")
            archivo_editado = input("\n¿Ha editado y guardado el archivo? (s/n): \n").lower() == 's'
        if archivo_editado:
            data = crear_data_para_actualizar_tipo_slots(ruta_csv, garage)
            if validacion_slots_ok(data, garage):
                actualizar_slots(garage_id, data)
                print(Fore.GREEN + f"\n{garage['garage_name']} ha sido actualizado con exito." + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "Actualizacion postergada" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Actualización postergada. Por favor, edite el archivo y vuelva a intentarlo." + Style.RESET_ALL )
            return garage
    elif bulk and tipos_slots:
        print(Fore.RED + "LOS TIPOS DE SLOTS YA HAN SIDO DEFINIDOS EN BULK, no se pueden definir de este formato, actualice uno por uno" + Style.RESET_ALL)
    else:
        handle_actualizar_tipo_slot(garage_data, garage)
    return garage


def configurar_slots_bulk(garage):
    """Lógica para configurar múltiples slots mediante CSV"""
    garage_id = garage['garage_id']
    garage_name = garage['garage_name']
    
    print("\nSe creará un csv en directorio actual llamado 'config_slots.csv' para actualizar los tipos de slots\n")
    ruta_csv = generar_csv_slots(garage)
    
    if ruta_csv and os.path.exists(ruta_csv):
        print(Fore.RED + f"Por favor, edite el archivo en: {os.path.abspath(ruta_csv)}" + Style.RESET_ALL)
        print("Una vez editado, guarde el archivo y vuelva aquí para continuar.")
        archivo_editado = input("\n¿Ha editado y guardado el archivo? (s/n): \n").lower() == 's'
        
        if archivo_editado:
            data = crear_data_para_actualizar_tipo_slots(ruta_csv, garage)
            actualizar_slots(garage_id, data)
            print(Fore.GREEN + f"\n{garage_name} ha sido actualizado con éxito." + Style.RESET_ALL)
        else:
            print("Actualización postergada. Por favor, edite el archivo y vuelva a intentarlo.")
    else:
        print(Fore.RED + "No se pudo generar el archivo CSV. Operación cancelada." + Style.RESET_ALL)

def mover_vehiculo(patente, garage_data, tipo_vehiculo, data, garage, piso):
    pisos_slots_por_tipo = buscar_slots_por_tipo(garage_data, tipo_vehiculo)
    slots_por_tipo = [slot for sub in pisos_slots_por_tipo.values() for slot in sub]
    while True:
        if not slots_por_tipo:
            print("No hay mas lugares disponibles para este tipo de vehiculo.")
            raise Exception("No hay lugar")
        print(f"Lugares disponibles: {pisos_slots_por_tipo}/n")
        nuevo_slot_id = int(input(f"Ingrese el ID del nuevo slot debe coincidir con {slots_por_tipo}: "))
        if nuevo_slot_id < 1 or nuevo_slot_id not in slots_por_tipo:
            print(Fore.RED + f"El ID del slot debe estar entre {slots_por_tipo}." + Style.RESET_ALL)
        else:
            break
    nuevo_piso = buscar_piso_por_slot_id(nuevo_slot_id, garage)
    old_slot_id = data.get("id")
    hora_entrada = data.get('hora_entrada')
    
    print(f"Moviendo vehículo con patente {patente} al slot {nuevo_slot_id}...")
    data_actualizada = [{"slot_id": old_slot_id, "piso": piso, "ocupado": False, "patente": "", "hora_entrada": "", "tipo_vehiculo": 0}, {"slot_id": nuevo_slot_id, "piso": nuevo_piso, "ocupado": True, "patente": patente, "hora_entrada": hora_entrada, "tipo_vehiculo": tipo_vehiculo}]
    actualizar_slots(garage['garage_id'],  data_actualizada)
    print(Fore.GREEN + f"Vehículo con patente {patente} movido al slot {nuevo_slot_id} correctamente." + Style.RESET_ALL)


def handle_mover_vehiculo(garage, garage_data=None):
    """Maneja el movimiento de un vehículo dentro del garage"""
    print("\n=== MOVER VEHÍCULO ===")
    
    # Validar que garage_data no sea None
    if garage_data is None:
        print(Fore.RED + "Error: No se pudo cargar la información del garage" + Style.RESET_ALL)
        clear_screen()
        return garage
    
    try:
        # 1. Pedir patente y buscar vehículo
        patente = pedir_patente()
        piso_actual, slot_id_actual = buscar_por_patente(garage_data, patente)
        
        if piso_actual == -1 and slot_id_actual == -1:
            print(Fore.RED + "Vehículo no encontrado en el garage" + Style.RESET_ALL)
            clear_screen()
            return False
        
        # 2. Obtener datos del vehículo actual
        slot_actual = None
        for piso in garage_data:
            for slot in piso:
                if slot.get('piso') == piso_actual and slot.get('id') == slot_id_actual:
                    slot_actual = slot
                    break
            if slot_actual:
                break
        
        if not slot_actual:
            print(Fore.RED + "Error: No se pudo obtener información del slot" + Style.RESET_ALL)
            clear_screen()
            return False
        
        tipo_slot_vehiculo = slot_actual.get('tipo_slot')
        hora_entrada = slot_actual.get('hora_entrada')
        tipo_vehiculo = slot_actual.get('tipo_vehiculo')
        reservado_mensual = slot_actual.get('reservado_mensual')
        
        # 3. Buscar slots disponibles del mismo tipo
        slots_disponibles = []
        for piso in garage_data:
            for slot in piso:
                # Slot debe ser del mismo tipo, estar libre, y no ser el slot actual
                if (slot.get('tipo_slot') == tipo_slot_vehiculo and 
                    not slot.get('ocupado') and 
                    slot.get('id') != slot_id_actual):
                    slots_disponibles.append({
                        'id': slot.get('id'),
                        'piso': slot.get('piso')
                    })
        
        # 4. Verificar si hay slots disponibles
        if not slots_disponibles:
            print(Fore.RED + f"No hay slots disponibles del mismo tipo (tipo {tipo_slot_vehiculo})" + Style.RESET_ALL)
            clear_screen()
            return False
        
        # 5. Mostrar slots disponibles
        print(Fore.GREEN + f"\nSlots disponibles para mover el vehículo (tipo {tipo_slot_vehiculo}):" + Style.RESET_ALL)
        for slot_disp in slots_disponibles:
            print(f"  - Slot ID: {slot_disp['id']}, Piso: {slot_disp['piso']}")
        
        # 6. Pedir al usuario que elija un slot
        ids_disponibles = [s['id'] for s in slots_disponibles]
        while True:
            try:
                nuevo_slot_id = int(input(Fore.YELLOW + f"\nIngrese el ID del nuevo slot {ids_disponibles}: " + Style.RESET_ALL))
                if nuevo_slot_id not in ids_disponibles:
                    print(Fore.RED + f"ID inválido. Debe ser uno de: {ids_disponibles}" + Style.RESET_ALL)
                    continue
                break
            except ValueError:
                print(Fore.RED + "Por favor ingrese un número válido" + Style.RESET_ALL)
        
        # 7. Obtener piso del nuevo slot
        nuevo_piso = None
        for slot_disp in slots_disponibles:
            if slot_disp['id'] == nuevo_slot_id:
                nuevo_piso = slot_disp['piso']
                break
        
        # 8. Mover el vehículo (liberar slot actual y ocupar nuevo slot)
        print(f"\nMoviendo vehículo con patente {patente} al slot {nuevo_slot_id} (piso {nuevo_piso})...")
        
        data_actualizada = [
            # Liberar slot actual
            {
                "slot_id": slot_id_actual, 
                "piso": piso_actual, 
                "ocupado": False, 
                "patente": "", 
                "hora_entrada": "", 
                "tipo_vehiculo": 0
            },
            # Ocupar nuevo slot
            {
                "slot_id": nuevo_slot_id, 
                "piso": nuevo_piso, 
                "ocupado": True, 
                "patente": patente, 
                "hora_entrada": hora_entrada, 
                "tipo_vehiculo": tipo_vehiculo,
                "reservado_mensual": reservado_mensual
            }
        ]
        
        actualizar_slots(garage['garage_id'], data_actualizada)
        print(Fore.GREEN + f"✅ Vehículo movido exitosamente al slot {nuevo_slot_id} (piso {nuevo_piso})" + Style.RESET_ALL)
        clear_screen()
        
    except Exception as e:
        print(Fore.RED + f"Error al mover el vehículo: {e}" + Style.RESET_ALL)
        import traceback
        traceback.print_exc()
        clear_screen()
    
    return garage

def handle_administrar_usuarios():
    """Maneja la administración de usuarios del garage"""
    print("\n=== ADMINISTRAR USUARIOS DEL GARAGE ===")
    try:
        
        while True:
            print("1- Asignar admin a un usuario")
            print("2- Quitar admin a un usuario")
            print("3- Volver al menú principal")
            
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "1":
                asignar_admin()
                clear_screen()
            elif opcion == "2":
                eliminar_admin()
                clear_screen()
            elif opcion == "3":
                clear_screen()
                break
            else:
                print(Fore.RED + "Opción inválida. Intente de nuevo." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error al administrar usuarios: {e}" + Style.RESET_ALL)
    
