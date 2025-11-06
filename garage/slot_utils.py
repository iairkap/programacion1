import datetime
from colorama import Fore, Style


def tipo_slot():
    while True:
        entrada = input(Fore.LIGHTYELLOW_EX +
            "\nQue tipo de vehiculo ingreso: \n 1. Moto \n 2. Auto \n 3. Suv - Camioneta \n " + Style.RESET_ALL).strip().lower()

        try:
            tipo_slot = int(entrada)
            if tipo_slot in [1, 2, 3]:
                return tipo_slot
            else:
                print("Error: Opcion no valida")
                continue
        except ValueError:
            if entrada in ["moto", "1"]:
                return 1
            elif entrada in ["auto", "2"]:
                return 2
            elif entrada in ["suv", "camioneta", "suv-camioneta", "suv - camioneta", "3"]:
                return 3
            else:
                print(
                    "Error: Ingrese un numero (1-3) o el tipo de vehiculo (moto/auto/suv-camioneta)")
                

def obtener_slot_por_id(garage, slot_id):
    """Obtiene slot por ID - NUEVA función auxiliar"""
    # Busca en todos los pisos y slots
    for piso in garage:
        for slot in piso:
            # Compara con slot["id"] que es el ID del slot
            if slot["id"] == slot_id:
                return slot
    return None

def buscar_piso_por_slot_id(slot_id, garage):
    """
    Calcula a qué piso pertenece un slot según su número y cantidad de slots por piso.
    """
    slots_por_piso = garage.get("slots_per_floor")
    if slot_id <= 0:
        return None  # IDs negativos o 0 no son válidos
    piso = ((slot_id - 1) // slots_por_piso)
    return piso

def validacion_slots_ok(data, garage):
    """Valida que la cantidad de slots a actualizar coincida con la configuración del garage,
    y detecta pisos con más o menos slots de los esperados.
    """
    slots_per_floor = garage.get("slots_per_floor", 0)
    floors = garage.get("floors", 0)
    total_slots = floors * slots_per_floor
    data_len = len(data)

    if not data:
        print("❌ No se recibieron datos para actualizar.")
        return False

    pisos_count = {}
    for slot in data:
        piso = slot.get('piso')
        if piso is None:
            continue
        if piso is None or piso < 0 or piso > floors:
            print(f"⚠️ Piso inválido detectado: {piso}")
            errores = True
            continue
        pisos_count[piso] = pisos_count.get(piso, 0) + 1

    if data_len < total_slots:
        print(f"⚠️ Estás modificando menos slots que los totales ({data_len}/{total_slots}).")
    elif data_len > total_slots:
        print(f"❌ Estás intentando modificar más slots ({data_len}) de los existentes ({total_slots}).")
    else:
        print("✅ La cantidad total de slots a actualizar es correcta.")
    
    continuar= True
    if data_len != total_slots:
        continuar = input("¿Desea continuar con la actualización? (s/n): ").strip().lower() == 's'
    if not continuar:
        return False

    print("\n📊 Revisión por piso:")
    errores = False
    for piso in range(0, floors):
        count = pisos_count.get(piso, 0)
        if count < slots_per_floor:
            print(f"  Piso {piso}: {count}/{slots_per_floor} → faltan {slots_per_floor - count}")
        elif count > slots_per_floor:
            print(f"  Piso {piso}: {count}/{slots_per_floor} → sobran {count - slots_per_floor}")
        else:
            print(f"  Piso {piso}: {count}/{slots_per_floor} ✅ correcto")
    return not errores

def tipos_de_slot_definidos(garage, garage_data):
    """Retorna True si todos los slots ya tienen tipo, else False"""
    total_slots = garage.get('floors', 0) * garage.get('slots_per_floor', 0)
    return total_slots > 0 and all(slot.get('tipo_slot') for data in garage_data for slot in data)