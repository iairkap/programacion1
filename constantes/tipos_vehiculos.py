def enum_tipo_vehiculo():
    return {
        "moto": 1 ,
        "auto": 2,
        "camioneta": 3,
    }
    
    
def obtener_nombre_vehiculo(tipo_numero):
    """Convierte número de tipo a nombre. Retorna nombre o '-' si no existe."""
    tipos = enum_tipo_vehiculo()
    
    # Invertir: buscar número en valores
    for nombre, numero in tipos.items():
        if numero == tipo_numero:
            return nombre.capitalize()
    
    return "-"