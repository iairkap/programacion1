
from garage_util import (
    contar_espacios_libres,
    buscar_por_patente,
    buscar_espacio_libre,
    contar_espacios_libres_por_tipo
)
from interaccion_usuario import pedir_piso, pedir_patente, pedir_tipo_vehiculo

from main import garage

def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Consultar espacios libres")
    print("2. Consultar cantidad de vehículos estacionados")
    print("3. Ingresar un vehículo")
    print("4. Registrar salida de un vehículo")
    print("5. Reubicar un vehículo")
    print("6. Mostrar estado del garage")
    print("7. Buscar vehículo por patente")
    print("8. Estadísticas rápidas")
    print("9. Salir")
    
def menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
#! agregar validacion aca para el ingreso de opciones, pedir por parametro el num max de opciones

        if opcion == "1":
            print("\n1. Por piso\n2. Por tipo de vehículo\n3. Totales\n4. Volver")
            subop = input("Seleccione una de las opciones: ")
            if subop == "1":
                piso = pedir_piso(garage)
                libres = contar_espacios_libres([garage[piso]])
                print(f"Espacios libres en el piso {piso}: {libres}")
            elif subop == "2":
                tipo = pedir_tipo_vehiculo()
                libres = contar_esapcios_libres_por_tipo(garage, tipo)
                print(f"Espacios libres para tipo {tipo}: {libres}")
            elif subop == "3":
                libres = contar_espacios_libres(garage)
                print(f"Espacios libres en todo el garage: {libres}")
            elif subop == "4":
                continue

        elif opcion == "2":
            print("\n1. Por tipo de vehículo\n2. Totales\n3. Volver")
            subop = input("Seleccione una de las opciones: ")
            if subop == "1":
                tipo = pedir_tipo_vehiculo()
                cantidad = contar_esapcios_libres_por_tipo(garage, tipo)
                print(f"Cantidad de vehículos tipo {tipo}: {cantidad}")
            elif subop == "2":
                for tipo in range(1, 4):
                    cantidad = contar_esapcios_libres_por_tipo(garage, tipo)
                    print(f"Tipo {tipo}: {cantidad}")
            elif subop == "3":
                continue

        elif opcion == "3":
            ingresar_auto_matriz(garage)

        elif opcion == "4":
            patente = pedir_patente()
            print("Funcionalidad de salida de vehículo no implementada.")

        elif opcion == "5":
            patente = pedir_patente()
            print("Funcionalidad de reubicación no implementada.")

        elif opcion == "6":
            print("Funcionalidad de mostrar estado no implementada.")

        elif opcion == "7":
            patente = pedir_patente()
            pos = buscar_por_patente(garage, patente)
            if pos != (-1, -1):
                print(f"Vehículo encontrado en Piso {pos[0]}, Slot {pos[1]}")
            else:
                print("Vehículo no encontrado.")

        elif opcion == "8":
            print("Funcionalidad de estadísticas no implementada.")

        elif opcion == "9":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intente de nuevo.")
            
menu()

#notas:
# mostrar los tipos de veiculos en el menu
# validar entradas de menu
#hacer todo en un try para que no rompa
