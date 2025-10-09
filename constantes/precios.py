""" 
Se lee los precios estipulados por el garage en el fine users-garage.csv -> se recibe por parametro el ID del garage 


"""


def listado_de_precios(garage_id):
    try:
        with open("files/users-garage.csv", mode="r", encoding="utf-8") as archivo:
            next(archivo)  # Saltar la primera línea (headers)
            for linea in archivo:
                datos = linea.strip().split(',')
                if datos[0] == str(garage_id):
                    return [
                           {"tipo_vehiculo": 1, "precio_hora": 50},  # Motos
                            {"tipo_vehiculo": 2, "precio_hora": 100}, # Autos
                            {"tipo_vehiculo": 3, "precio_hora": 150}, # Camionetas
                            {"tipo_vehiculo": 1, "precio_mensual": 1500},  # Motos
                            {"tipo_vehiculo": 2, "precio_mensual": 3000}, # Autos
                            {"tipo_vehiculo": 3, "precio_mensual": 4500}, # Camionetas
                    ]
        print(f"Error: No se encontró el garage con ID {garage_id}")
        return None
    except FileNotFoundError:
        print("Error: El archivo users-garage.csv no existe.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None