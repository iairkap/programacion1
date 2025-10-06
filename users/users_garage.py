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
    """Asocia un garage a un usuario escribiendo en users-garage.csv."""
    try:
        garage_id = obtener_siguiente_garage_id()
        
        with open("files/users-garage.csv", mode="a", encoding="utf-8") as arch:
            arch.write(f"{garage_id},{user_email},{garage_name},{address},{floors},{slots_per_floor}\n")
            print(f"Garage '{garage_name}' asociado al usuario '{user_email}' exitosamente.")
            
    except Exception as e:
        print(f"Error al asociar el garage: {e}")

print(buscar_garage_asociado("user@example.com"))
