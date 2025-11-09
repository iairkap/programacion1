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
                

def get_slot_in_piso(piso, slot_id):
    slot_data = {}
    for slot in piso:
        if slot.get('id', 0) == slot_id:
            slot_data = slot
            break
    if not slot_data:
        print('Slot no encontrado')
    return slot_data
