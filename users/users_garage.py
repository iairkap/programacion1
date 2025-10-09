#Archivo para crear garage, relacionarlos con usuarios y demas

def buscar_garage_asociado(email):
    """Busca el garage asociado a un usuario dado su email."""
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
    "si el user tiene varios garages, le permite seleccionar uno"
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
      # Estructura del slot: [slot_id, piso, pos, tipo_slot, reservado_mensual, ocupado, patente, hora_entrada, tipo_vehiculo_estacionado]
            piso_slots.append([slot_id, piso, slot, "", False, False, "", "", ""])
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

    ### Agregar check para el id ###
    try:
        estructura = generate_garage_structure(floors, slots_per_floor)
        # Encabezados coherentes con la estructura de cada slot
        headers = [
            "slot_id",
            "floor",
            "pos",
            "tipo_slot",
            "reservado_mensual",
            "ocupado",
            "patente",
            "hora_entrada",
            "tipo_vehiculo_estacionado"
        ]

        rows = []
        for piso_slots in estructura:
            for slot in piso_slots:
                rows.append(slot)
        escribir_data_en_csv(f"files/garage-{garage_id}.csv", rows, headers=headers)
        print(f"Garage {garage_id} creado con {floors} pisos y {slots_per_floor} slots por piso.")
        return estructura
    except Exception as e:
        print(f"Error al crear el garage: {e}")
        return None

def actualizar_slot_por_tipo(estructura, slot_id, tipo_slot ):
    """actualizar el tipo de slot en la estructura"""
    for piso in estructura:
        for slot in piso:
            if slot[0] == slot_id:
                slot[3] = tipo_slot
                return True

def actualizar_slots_por_tipo(estructura, garage_id, tipo_slot, cantidad):
    """actualizar matriz y escribir en el archivo"""
    #### A terminar ####
    if cantidad <= 0:
        print("Cantidad debe ser mayor que 0")
        return False
    try: 
        for piso in estructura:
            pass
    except Exception as e:
        print(f"Error al actualizar slots: {e}")
        return False
    
def actualizar_slot_en_csv(estructura, garage_id, bulk= False):
    """escribe la estructura actualizada en el archivo correspondiente"""
    ### A terminar ###
    pass