import json

def guardar_estado_garage(garage: list, filename: str = "cache.json") -> None:
    """
    Guarda el estado actual del garage en un archivo JSON.
    Sobrescribe siempre el archivo existente.
    
    garage: lista de pisos, cada uno con lista de diccionarios de slots
    filename: nombre del archivo donde se guarda (por defecto 'cache.json')
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(garage, f, indent=4, ensure_ascii=False)
        print(f"Estado del garage guardado en {filename}")
    except Exception as e:
        print(f"No se pudo guardar el estado del garage: {e}")


def leer_estado_garage(filename: str = "cache.json") -> list | None:
    """
    Lee el estado del garage desde un archivo JSON.
    Devuelve la lista de pisos con slots, o None si falla.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Archivo {filename} está dañado o no es un JSON válido.")
        return None
    except Exception as e:
        print(f"Error al leer el estado del garage: {e}")
        return None