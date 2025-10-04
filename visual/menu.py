from garage.garage_util import (
    contar_espacios_libres,
    buscar_por_patente,
    buscar_espacio_libre,
    contar_espacios_libres_por_tipo

)
from users.interaccion_usuario import (
    pedir_piso,
    pedir_patente,
    pedir_tipo_vehiculo,
    mostrar_estado_garage)
from main import (
    registrar_entrada_auto,
    contar_por_tipo_vehiculo,
    chequear_espacio_libre, registrar_salida_vehiculo,
    registrar_salida_vehiculo,
    modificar_vehiculo,
    mostrar_estadisticas_rapidas)

from users.usuarios import(
    creacion_usuario,
    crear_archivo_users,
    user_login
)

from garage.mockdata import GARAGE, COSTOS

garage = GARAGE


def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    
    print("1. Consultar espacios libres")
    print("2. Consultar cantidad de vehículos estacionados")
    print("3. Ingresar un vehículo")
    print("4. Registrar salida de un vehículo")
    print("5. Editar un vehículo")
    print("6. Mostrar estado del garage")
    print("7. Buscar vehículo por patente")
    print("8. Estadísticas rápidas")
    print("9. Crear usuario")
    print("10. Iniciar sesión")
    print("11. Salir")


def menu():
    while True:
        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n1. Por piso\n2. Por tipo de vehículo\n3. Totales\n4. Volver")
            subop = input("Seleccione una de las opciones: ")
            if subop == "1":
                piso = pedir_piso(garage)
                libres = contar_espacios_libres([garage[piso]])
                print(f"Espacios libres en el piso {piso}: {libres}")
            elif subop == "2":
                print("\nTipos de vehículo:")
                print("1. Moto\n2. Auto\n3. Camioneta\n4. Bicicleta")
                tipo = pedir_tipo_vehiculo()
                libres = contar_espacios_libres_por_tipo(garage, tipo)
                print(f"Espacios libres para tipo {tipo}: {libres}")
            elif subop == "3":
                libres = contar_espacios_libres(garage)
                print(f"Espacios libres en todo el garage: {libres}")

        elif opcion == "2":
            print("\n1. Por tipo de vehículo\n2. Totales\n3. Volver")
            subop = input("Seleccione una de las opciones: ")
            if subop == "1":
                print("\nTipos de vehículo:")
                print("1. Moto\n2. Auto\n3. Camioneta\n4. Bicicleta")
                tipo = pedir_tipo_vehiculo()
                cantidad = contar_por_tipo_vehiculo(garage, tipo)
                tipos_nombres = {1: "Motos", 2: "Autos",
                                 3: "Camionetas", 4: "Bicicletas"}
                print(
                    f"Cantidad de {tipos_nombres[tipo]} estacionadas: {cantidad}")
            elif subop == "2":
                print("\n--- Vehículos estacionados por tipo ---")
                tipos = {1: "Motos", 2: "Autos",
                         3: "Camionetas", 4: "Bicicletas"}
                for tipo_num, tipo_nombre in tipos.items():
                    cantidad = contar_por_tipo_vehiculo(garage, tipo_num)
                    print(f"{tipo_nombre}: {cantidad}")

        elif opcion == "3":
            registrar_entrada_auto(garage)

        elif opcion == "4":
            patente = pedir_patente()
            if registrar_salida_vehiculo(garage, patente):
                print("Salida registrada correctamente.")
            else:
                print("Patente no encontrada.")

        elif opcion == "5":
            patente = pedir_patente()
            nuevo_tipo = pedir_tipo_vehiculo()
            nueva_patente = input(
                "Nueva patente (dejar vacío para no cambiar): ").strip().upper()
            if nueva_patente == "":
                nueva_patente = None
            if modificar_vehiculo(garage, patente, nuevo_tipo, nueva_patente):
                print("Vehículo modificado correctamente.")
            else:
                print("Patente no encontrada.")

        elif opcion == "6":
            mostrar_estado_garage(garage)

        elif opcion == "7":
            patente = pedir_patente()
            pos = buscar_por_patente(garage, patente)
            if pos != (-1, -1):
                print(f"Vehículo encontrado en Piso {pos[0]}, Slot {pos[1]}")
            else:
                print("Vehículo no encontrado.")

        elif opcion == "8":
            mostrar_estadisticas_rapidas(garage)
        
        elif opcion == "9":
            crear_archivo_users()
            usuario = creacion_usuario()

            if usuario:
                arch_users = open("files/users.csv", mode="a", encoding="utf-8")
                arch_users.write(f"{usuario['nombre']},{usuario['apellido']},{usuario['email']},{usuario['password']}\n")
                arch_users.close()
                print("Usuario creado exitosamente:", usuario)
            else:
                print("No se pudo crear el usuario.")
        elif opcion == "10":
            user_login()
            if user_login():
                print("Login exitoso")
            else:
                print("Login fallido")
        elif opcion == "11":
            print("¡Hasta luego!")
            break
            
        
        else:
            print("Opción inválida. Intente de nuevo.")


menu()
