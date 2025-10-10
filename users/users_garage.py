#Archivo para crear garage, relacionarlos con usuarios y demas

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
                    "slots_per_floor": int(parts[5])
                }
                garages.append(garage)
        
        arch.close()
        
        if garages:
            return garages
        else:
            print("No se encontró un garage asociado a este usuario.")
            return None
            
    except FileNotFoundError:
        print("Archivo users-garage.csv no encontrado.")
        return None


def seleccionar_solo_un_garage(garages):
    "Se recibe como parametro una lista de garages, permitiendo al usuario seleccionar uno."
    if not garages:
        return None
    elif len(garages) == 1:
        return garages[0]
    else:
        print("Seleccione un garage:\n")
        for i, garage in enumerate(garages):
            print(f"{i + 1}. {garage['garage_name']} - {garage['address']}")
        seleccion = input("Ingrese el número del garage deseado: ")
        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(garages):
                return garages[seleccion - 1]
            else:
                print("Selección inválida.")
                return None
        except ValueError:
            print("Entrada no válida.")
            return None
        
        
        
def crear_archivo_users_garage():
    """Crea el archivo users-garage.csv si no existe, con encabezados."""
    try:
        with open("files/users-garage.csv", mode="x", encoding="utf-8") as arch:
            arch.write("garage_id,user_email,garage_name,address,floors,slots_per_floor\n")
            print("Archivo users-garage.csv creado exitosamente.")
    except FileExistsError:
        print("El archivo users-garage.csv ya existe.")
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
            
    except Exception as e:
        print(f"Error al asociar el garage: {e}")

def generate_garage_structure(floors, slots_per_floor):
    """Genera la estructura inicial del garage."""
    garage = []
    slot_id = 0
    for piso in range(floors):
        piso_slots = []
        for slot in range(slots_per_floor):
            slot_id += 1
            piso_slots.append({"slot_id": slot_id,"piso": piso, "posicion": slot, "tipo_slot": "","reservado_mensual": False,"ocupado": False, "patente":"", "hora_entrada": "", "tipo_vehiculo":""})
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


def crear_garage(garage_id, slots_per_floor, floors):
    """Crea un garage nuevo basado en el ID proporcionado."""
    try:
        estructura = generate_garage_structure(floors, slots_per_floor)
        # Encabezados coherentes con la estructura de cada slot
        headers = estructura[0][0].keys()
        rows = []
        for piso_slots in estructura:
            for slot in piso_slots:
                rows.append(slot.values())
        escribir_data_en_csv(f"files/garage-{garage_id}.csv", rows, headers=headers)
        print(f"Garage {garage_id} creado con {floors} pisos y {slots_per_floor} slots por piso.")
        return estructura
    except Exception as e:
        print(f"Error al crear el garage: {e}")
        return None

def actualizar_slot(garage_id, slot_id, nuevaData):
    """actualizar un slot en particular
    nuevaData es un diccionario con los campos a actualizar
    """
    try: 
        with open(f"files/garage-{garage_id}.csv", "r") as file:
            lineas = file.readlines()
        
        encabezado = lineas[0].strip().split(",")
        nuevas_lineas = [encabezado]
        
        for linea in lineas[1:]:
            datos = linea.strip().split(",")
            
            id_actual = datos[0]
            piso = datos[1]
            posicion = datos[2]
            tipo_slot = datos[3]
            reservado_mensual = datos[4]
            ocupado = datos[5]
            patente = datos[6]
            hora_entrada = datos[7]
            tipo_vehiculo = datos[8]
            
            # Si coincide el id, actualizamos
            if id_actual == str(slot_id):
                tipo_slot = str(nuevaData.get("tipo_slot", tipo_slot))
                reservado_mensual = str(nuevaData.get("reservado_mensual", reservado_mensual))
                ocupado = str(nuevaData.get("ocupado", ocupado))
                patente = str(nuevaData.get("patente", patente))
                hora_entrada = str(nuevaData.get("hora_entrada", hora_entrada))
                tipo_vehiculo = str(nuevaData.get("tipo_vehiculo", tipo_vehiculo))
            
            # Agregamos la fila (actualizada o no)
            nuevas_lineas.append([id_actual, piso, posicion, tipo_slot, reservado_mensual, ocupado, patente, hora_entrada, tipo_vehiculo])

        with open(f"files/garage-{garage_id}.csv", "w") as file:
            # Reescribir encabezado
            file.write(",".join(encabezado) + "\n")
            # Reescribir filas
            for fila in nuevas_lineas[1:]:
                file.write(",".join(fila) + "\n")
        
        print(f"Slot con id {slot_id} actualizado correctamente ✅")
    except FileNotFoundError:
        print(f"Archivo garage-{garage_id}.csv no encontrado.")
    except Exception as e:
        print(f"Error al actualizar el slot: {e}")
    
def actualizar_slots(garage_id, nuevaData):
    """actualizar varios slots a la vez
    nuevaData es una lista de diccionarios con los campos a actualizar
    i.e. [{"slot_id": 1, "ocupado": "True", "tipo_slot": 2}, {"slot_id": 2, "ocupado": "True"}]
    """
    try:
        for slotInfo in nuevaData:
            print(slotInfo)
            slot_id = slotInfo.get("slot_id")
            actualizar_slot(garage_id, slot_id, slotInfo)
    except Exception as e:
        print(f"Error al actualizar los slots: {e}")
       
def actualizar_garage(garage_id, data, bulk=False):
    """Actualiza la información de un garage en csv."""
    try: 
        if bulk:
            actualizar_slots(garage_id, data)
            return True
        else:
            actualizar_slot(garage_id, data.get("slot_id"), data)
        print(f"Garage con id {garage_id} actualizado correctamente ✅")
    except Exception as e:
        print(f"Error al actualizar el garage: {e}")
