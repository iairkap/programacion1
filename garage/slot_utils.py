import datetime

def tipo_slot():
    while True:
        entrada = input(
            "Que tipo de vehiculo ingreso: \n 1. Moto \n 2. Auto \n 3. Suv - Camioneta \n ").strip().lower()

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
            # Compara con slot[0] que es el ID del slot
            if slot[0] == slot_id:
                return slot
    return None


def actualizar_slot(patente, tipo_de_vehículo, piso, fila, columna, garage=GARAGE ):
    """Actualiza el slot con la nueva informacion"""
    slot = garage[piso][fila][columna]
    slot[1] = patente
    slot[3] = False
    slot[5] = datetime.datetime.now()
    slot[6] = tipo_de_vehículo
    print(f"Slot actualizado: {slot}")
    return True 