#Archivo para crear garage, relacionarlos con usuarios y demas
from auxiliares.consola import clear_screen
from cache.json import guardar_estado_garage, leer_estado_garage
import os
from constantes.tipos_vehiculos import enum_tipo_vehiculo
from colorama import Fore, Style


def mostrar_garages_asociados(email,show_all=False):
    """Mostramos todos los garages asociados al usuario"""
    if not email:
        return None
    
    try:
        arch = open("files/users-garage.csv", mode="r", encoding="utf-8")
        next(arch)  # Saltear la línea de encabezado
        cont = 0  # ✅ EMPEZAR EN 0
        
        print(Fore.CYAN + "\n=== GARAGES DISPONIBLES ===" + Style.RESET_ALL)
        
        for line in arch:
            parts = line.strip().split(",")
            if len(parts) < 6:
                continue
            
            # Solo procesar si el email coincide
            if parts[1] == email:
                cont += 1  # ✅ INCREMENTAR PRIMERO
                print(f"{cont}. {parts[2]}")  # ✅ LUEGO IMPRIMIR
            elif show_all:
                cont += 1
                print(f"{cont}. {parts[2]} (asociado a {parts[1]})")
        
        arch.close()
        
        if cont == 0:
            print(Fore.YELLOW + "No tienes garages asociados." + Style.RESET_ALL)
        
        return cont
    
    except FileNotFoundError:
        print("Archivo users-garage.csv no encontrado.")
        return 0

###Agregando comentario para que git detecte los cambios D:
def buscar_garage_asociado(email):
    """
    Busca el garage asociado a un usuario dado su email.
    Si me encuentra varios garages, se agregan a una lista que es retornada. 
    En caso de no encontrar ninguno, retorna None.
    
    """
    print(email)
  
    if not email:
        return None
    
    try:
        arch = open("files/users-garage.csv", mode="r", encoding="utf-8")
        next(arch)  # Saltear la línea de encabezado
        garages = []
        for line in arch:
            parts = line.strip().split(",")
            if len(parts) < 6:
                continue
            
            # Solo procesar si el email coincide
            if parts[1] == email:
                garage = {
                    "garage_id": parts[0],
                    "user_email": parts[1],
                    "garage_name": parts[2],
                    "address": parts[3],
                    "floors": int(parts[4]),
                    "slots_per_floor": int(parts[5]),
                
                }
                garages.append(garage)
        
        arch.close()
        
        if garages:
            return garages
        else:
            print(Fore.RED + "\nNo se encontró un garage asociado a este usuario.\n" + Style.RESET_ALL)
            return None
            
    except FileNotFoundError:
        print("Archivo users-garage.csv no encontrado.")
        return None


def seleccionar_solo_un_garage(email,cant_garages,admin = False):
    "Se recibe como parametro una lista de garages, permitiendo al usuario seleccionar uno."
    if not email:
        return None

    try:
        while True:
            try :
                numero_garage = int(input("Seleccione un garage: "))
                if 1 <= numero_garage <= cant_garages:
                    break
                print(Fore.RED + f"Ingrese un número entre 1 y {cant_garages}." + Style.RESET_ALL)
                
            except ValueError:
                print(Fore.RED + "Entrada inválida. Por favor, ingrese un número válido." + Style.RESET_ALL)

        with open("files/users-garage.csv", mode="r", encoding="utf-8") as arch:
            next(arch)  # Saltear la línea de encabezado
            garages = []
            count = 1
            for line in arch:
                parts = line.strip().split(",")
                if len(parts) < 6:
                    continue
                
                # Solo procesar si el email coincide
                if parts[1] == email or admin:
                    if count == numero_garage:
                        garage = {
                            "garage_id": parts[0],
                            "user_email": parts[1],
                            "garage_name": parts[2],
                            "address": parts[3],
                            "floors": int(parts[4]),
                            "slots_per_floor": int(parts[5])
                        }
                        arch.close()
                        return garage
                    else:
                        count += 1
            arch.close()
            return None

    except FileNotFoundError:
        print("Archivo users-garage.csv no encontrado.")
        return None
        
        
def crear_archivo_users_garage():
    """Crea el archivo users-garage.csv si no existe, con encabezados."""
    try:
        with open("files/users-garage.csv", mode="x", encoding="utf-8") as arch:
            arch.write("garage_id,user_email,garage_name,address,floors,slots_per_floor\n")
            print("Archivo users-garage.csv creado exitosamente.")
    except FileExistsError:
        # El archivo ya existe, no hacer nada
        pass
    return

def obtener_siguiente_garage_id():
    """Obtiene el siguiente ID de garage disponible."""
    try:
        with open("files/users-garage.csv", mode="r", encoding="utf-8") as arch:
            next(arch)  # Saltar header
            max_id = 0
            for line in arch:
                parts = line.strip().split(",")
                if parts and parts[0].isdigit():
                    max_id = max(max_id, int(parts[0]))
            return max_id + 1
    except FileNotFoundError:
        return 1  # Primer garage

def asociar_garage_a_usuario(user_email, garage_name, address, floors, slots_per_floor):
    """Asocia un garage a un usuario escribi endo en users-garage.csv."""
    try:
        garage_id = obtener_siguiente_garage_id()
        
        with open("files/users-garage.csv", mode="a", encoding="utf-8") as arch:
            arch.write(f"{garage_id},{user_email},{garage_name},{address},{floors},{slots_per_floor}\n")
            print(f"Garage '{garage_name}' asociado al usuario '{user_email}' exitosamente.")
            return garage_id        
    except Exception as e:
        print(f"Error al asociar el garage: {e}")

def generate_garage_structure(floors, slots_per_floor):
    """Genera la estructura inicial del garage. """
    garage = []
    slot_id = 0
    for piso in range(floors):
        piso_slots = []
        for _ in range(slots_per_floor):
            slot_id += 1
            piso_slots.append({"slot_id": slot_id,"piso": piso, "tipo_slot": "","reservado_mensual": False,"ocupado": False, "patente":"", "hora_entrada": "", "tipo_vehiculo":""})
        garage.append(piso_slots)
    return garage

def _escape_csv_field(value):
    """Escapa un campo para CSV: dobla comillas y encierra en comillas si hay comas / saltos de línea."""
    s = "" if value is None else str(value)
    if any(c in s for c in ('"', ',', '\n', '\r')):
        s = '"' + s.replace('"', '""') + '"'
    return s

def escribir_data_en_csv(file_path, data, headers=None):
    """Escribe una lista de listas en file_path como CSV sin usar el módulo csv.
    headers: lista opcional de nombres de columna."""
    try:
        with open(file_path, mode="w", encoding="utf-8") as f:
            if headers:
                f.write(",".join(_escape_csv_field(h) for h in headers) + "\n")
            for row in data:
                f.write(",".join(_escape_csv_field(cell) for cell in row) + "\n")
    except Exception as e:
        print(f"Error al escribir CSV {file_path}: {e}")
        raise


def crear_garage(usuario, nombre, direccion, slots_per_floor=10, floors=2):
    """Crea un garage nuevo basado en el ID proporcionado."""
    try: 
        garage_id = asociar_garage_a_usuario(
            usuario['email'],
            nombre,
            direccion,
            floors if floors else 2,
            slots_per_floor if slots_per_floor else 10
        )
        estructura = generate_garage_structure(floors, slots_per_floor)
        # Encabezados coherentes con la estructura de cada slot
        headers = estructura[0][0].keys()
        rows = []
        for piso_slots in estructura:
            for slot in piso_slots:
                rows.append(slot.values())
        escribir_data_en_csv(f"files/garage-{garage_id}.csv", rows, headers=headers)
        print(Fore.GREEN + f"Garage {nombre} creado con {floors} pisos y {slots_per_floor} slots por piso." + Style.RESET_ALL)
        return garage_id
    except Exception as e:
        print(f"Error al crear el garage: {e}")
        return 
def crear_data_para_actualizar_slot(slot_id, tipo_slot=None, piso=None, reservado_mensual=None, ocupado=None, patente=None, hora_entrada=None, tipo_vehiculo=None):
    """Crea un diccionario con los datos a actualizar para un slot."""
    data = {"slot_id": slot_id}
    if tipo_slot is not None:
        data["tipo_slot"] =  enum_tipo_vehiculo()[tipo_slot.lower()]
    if piso is not None:
        data["piso"] = piso
    if reservado_mensual is not None:
        data["reservado_mensual"] = reservado_mensual
    if ocupado is not None:
        data["ocupado"] = ocupado
    if patente is not None:
        data["patente"] = patente
    if hora_entrada is not None:
        data["hora_entrada"] = hora_entrada
    if tipo_vehiculo is not None:
        data["tipo_vehiculo"] = tipo_vehiculo
    return data

def actualizar_slot( garage_id, slot_id, nuevaData):
    """actualizar un slot en particular
    nuevaData es un diccionario con los campos a actualizar
    {
        'slot_id': 3,
        'piso': 0,
        'ocupado': True,
        'hora_entrada': '2025-10-31 13:40:55',
        'tipo_slot': 2,
        'patente': 'FAB144',
        "tipo_vehiculo": 2
        
        }
    
    """

    try: 
        with open(f"files/garage-{garage_id}.csv", "r") as file:
            lineas = file.readlines()

        encabezado = lineas[0].strip().split(",")
        nuevas_lineas = [encabezado]

        for linea in lineas[1:]:
            datos = linea.strip().split(",")

            id_actual, piso, tipo_slot, reservado_mensual, ocupado, patente, hora_entrada, tipo_vehiculo = datos[0:]

            if id_actual == str(slot_id) and str(nuevaData.get("piso")) == datos[1]:
                piso = datos[1]
                tipo_slot = str(nuevaData.get("tipo_slot", tipo_slot))
                reservado_mensual = str(nuevaData.get("reservado_mensual", reservado_mensual))
                ocupado = str(nuevaData.get("ocupado", ocupado))
                patente = str(nuevaData.get("patente", patente))
                hora_entrada = str(nuevaData.get("hora_entrada", hora_entrada))
                tipo_vehiculo = str(nuevaData.get("tipo_vehiculo", tipo_vehiculo))

            # Agregamos la fila (actualizada o no)
            nuevas_lineas.append([id_actual, piso, tipo_slot, reservado_mensual, ocupado, patente, hora_entrada, tipo_vehiculo])

        with open(f"files/garage-{garage_id}.csv", "w") as file:
            # Reescribir encabezado
            file.write(",".join(encabezado) + "\n")
            # Reescribir filas
            for fila in nuevas_lineas[1:]:
                file.write(",".join(fila) + "\n")
        return True
    except FileNotFoundError:
        print(f"Archivo garage-{garage_id}.csv no encontrado.")
    except Exception as e:
        print(f"Error al actualizar el slot: {e}")


def generar_csv_slots(garage):
    """
    Crea un archivo CSV si no existe en la ruta
    ~/Documents/data/config_slots.csv para que el usuario edite
    los tipos de slot y sus cantidades. Si ya existe, no lo modifica.
    """
    try:
        ruta_base = os.path.expanduser('~')
        ruta_data = os.path.join(ruta_base, "Documents", "data")
        _id = garage.get('garage_id', 0)
        os.makedirs(ruta_data, exist_ok=True)
        ruta_csv = os.path.join(ruta_data, f"config_slots_{_id}.csv")

        if not os.path.exists(ruta_csv):
            with open(ruta_csv, "w", encoding='utf-8') as file:
                file.write("tipo_de_slot,cantidad,piso\n")
                for piso in range(garage.get('floors')):
                    file.write(f"auto,0,{piso}\n")
                    file.write(f"moto,0,0{piso}\n")
                    file.write(f"camioneta,0,{piso}\n")
            print(Fore.GREEN + f"✅ Archivo de configuración CREADO en: {os.path.abspath(ruta_csv)}" + Style.RESET_ALL) 
        else:
            print(Fore.YELLOW + f"ℹ️ El archivo de configuración YA EXISTE en: {os.path.abspath(ruta_csv)}" + Style.RESET_ALL)

        print("Editá este archivo para indicar las cantidades de cada tipo de slot.")
        print("Una vez editado, guardalo y ejecuta la actualización de tipos de slots nuevamente.")
        return ruta_csv
    except Exception as e:
        print(Fore.RED + f"❌ Ocurrió un error al intentar gestionar el archivo CSV: {e}" + Style.RESET_ALL)
        print("Asegurate de que tu usuario tenga permisos para escribir en la carpeta 'Documents'.")

def leer_config_slots(ruta_csv=None):
    """
    Lee el archivo config_slots.csv y devuelve un diccionario
    con tipo_de_slot -> cantidad.
    """
    if os.path.exists(ruta_csv):
        config = {}
        with open(ruta_csv, "r", encoding="utf-8") as f:
            lineas = f.read().strip().split("\n")

        for linea in lineas[1:]:
            if not linea.strip():
                continue
            partes = linea.split(",")
            if len(partes) != 2:
                continue

            tipo = partes[0].strip()
            cantidad_str = partes[1].strip()

            if cantidad_str.isdigit():
                config[tipo] = int(cantidad_str)
        return config

def crear_data_para_actualizar_tipo_slots(ruta_csv,  garage):
    """Crea una lista de diccionarios con los datos a actualizar para varios slots.
    """
    slots_por_piso = garage.get('slots_per_floor', 0)
    pisos_totales = garage.get('floors', 0)

    try:
        slots = []
        slot_id = 0
        pisos_slots = {}

        with open(ruta_csv, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        encabezado = True
        for linea in lineas:
            linea = linea.strip()
            if not linea or encabezado:
                encabezado = False
                continue

            partes = linea.split(",")
            if len(partes) != 3:
                print(Fore.YELLOW + f"⚠️ Línea con formato incorrecto: {linea}" + Style.RESET_ALL)
                continue

            tipo_str, cantidad_str, piso_str = partes
            try:
                piso = int(piso_str)
                tipo = tipo_str.lower().strip()
                cantidad = int(cantidad_str)
            except ValueError:
                print(Fore.YELLOW + f"⚠️ Error al convertir valores en línea: {linea}" + Style.RESET_ALL)
                continue

            tipo_slot = enum_tipo_vehiculo().get(tipo)
            if tipo_slot is None:
                print(Fore.YELLOW + f"⚠️ Tipo desconocido: {tipo}" + Style.RESET_ALL)
                continue

            if piso not in pisos_slots:
                pisos_slots[piso] = 0

            for _ in range(cantidad):
                if pisos_slots[piso] >= slots_por_piso:
                    print(Fore.YELLOW + f"⚠️ Piso {piso} alcanzó el máximo de {slots_por_piso} slots. Ignorando los extra." + Style.RESET_ALL)
                    break

                slot_id += 1
                slots.append({
                    "slot_id": slot_id,
                    "tipo_slot": tipo_slot,
                    "piso": piso
                })
                pisos_slots[piso] += 1

        for piso in range(0, pisos_totales):
            count = pisos_slots.get(piso, 0)
            if count < slots_por_piso:
                print(Fore.YELLOW + f"⚠️ Piso {piso} tiene solo {count}/{slots_por_piso} slots definidos." + Style.RESET_ALL)
        return slots

    except Exception as e:
        print(Fore.RED + f"\nError al actualizar slots: {e}\n" + Style.RESET_ALL)
        return []
    
def get_garage_data(garage_id):
    """Lee la estructura del garage desde CSV y retorna lista de pisos con slots."""
    garage = []
    try:
        with open(f"files/garage-{garage_id}.csv", "r") as file:
            lineas = file.readlines()

        if not lineas:
            return garage

        # Saltar encabezado (línea 0)
        for linea in lineas[1:]:
            datos = linea.strip().split(",")
            
            if len(datos) < 8:
                continue
            
            # Obtener piso para crear estructura
            piso_csv = int(datos[1]) if len(datos) > 1 else 0

            # Crear pisos vacíos si es necesario
            while len(garage) <= piso_csv:
                garage.append([])

            # Crear slot con conversión de tipos
            slot = {
                "id": int(datos[0]) if len(datos) > 0 and datos[0].isdigit() else 0,
                "piso": int(datos[1]) if len(datos) > 2 and datos[1].isdigit() else 0,
                "tipo_slot": int(datos[2]) if len(datos) > 3 and datos[2].isdigit() else 0,
                "reservado_mensual": datos[3].lower() == "true" if len(datos) > 4 else False,
                "ocupado": datos[4].lower() == "true" if len(datos) > 5 else False,
                "patente": datos[5].strip() if len(datos) > 6 else "",
                "hora_entrada": datos[6].strip() if len(datos) > 7 else None,
                "tipo_vehiculo": int(datos[7]) if datos[7] and len(datos) >= 8 else 0,
            }
           
            garage[piso_csv].append(slot)

        return garage

    except FileNotFoundError:
        print(f"Archivo garage-{garage_id}.csv no encontrado.")
        return garage
    except Exception as e:
        print(f"Error al obtener datos del garage: {e}")
        return garage


def actualizar_slots(garage_id, nuevaData):
    """actualizar varios slots a la vez
    nuevaData es una lista de diccionarios con los campos a actualizar
    i.e. [{"slot_id": 1, "ocupado": "True", "tipo_slot": 2}, {"slot_id": 2, "ocupado": "True"}]
    """
    try:
        for slotInfo in nuevaData:
            slot_id = slotInfo.get("slot_id")
            actualizar_slot(garage_id, slot_id, slotInfo)
    except Exception as e:
        print(Fore.RED + f"Error al actualizar los slots: {e}" + Style.RESET_ALL)
       
def actualizar_garage(garage_id, data, bulk=False):
     """Actualiza la información de un garage en csv."""
     try: 
         if bulk:
             actualizar_slots(garage_id, data)
             print( Fore.GREEN + f"Garage con id {garage_id} actualizado correctamente ✅" + Style.RESET_ALL)
             return True
         else:
             actualizar_slot(garage_id, data.get("slot_id"), data)
         print(Fore.GREEN + f"Garage con id {garage_id} actualizado correctamente ✅" + Style.RESET_ALL)
         return True
     except Exception as e:
         print(Fore.RED + f"Error al actualizar el garage: {e}" + Style.RESET_ALL)
        
