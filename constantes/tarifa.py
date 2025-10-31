"""Función para guardar en memoria las tarifas actualizadas cuando se obtiene el garage_id.
Las tarifas se encuentran almacenadas en el csv tarifas.csv
Header del csv: garage_id,tipo,periodo_mensual,precio,moneda
"""


def guardar_precios_garage(garage_id):
    """Obtiene todas las tarifas de un garage desde el CSV.
    Retorna lista de diccionarios con las tarifas."""
    tarifas_actualizadas = []
    
    try:
        with open('files/tarifas.csv', 'r', encoding='utf-8') as file:
            # Leer todas las líneas
            lineas = file.readlines()
    except FileNotFoundError:
        return tarifas_actualizadas
    
    if not lineas:
        return tarifas_actualizadas
    
    # Extraer header (primera línea)
    header = lineas[0].strip().split(',')
    
    # Procesar datos (desde línea 1 en adelante)
    for i in range(1, len(lineas)):
        linea = lineas[i].strip()
        if not linea:
            continue
        
        valores = linea.split(',')
        if len(valores) == len(header):
            # Crear diccionario con header como claves
            fila = dict(zip(header, valores))
            
            # Comparar garage_id
            if fila.get('garage_id') == str(garage_id):
                tarifas_actualizadas.append(fila)
    
    return tarifas_actualizadas


#Tengo que hacer una funcion que dado una tarifa y un tipo de vehiculo me devuelva el precio
def obtener_precio_tipo_periodo(tarifas, tipo_vehiculo, periodo_mensual):
    """Obtiene el precio de una tarifa específica para un tipo de vehículo y periodo mensual.
    Retorna el precio si se encuentra, de lo contrario retorna None."""
    for tarifa in tarifas:
        if (tarifa.get('tipo') == str(tipo_vehiculo) and 
            tarifa.get('periodo_mensual') == str(periodo_mensual)):
            return tarifa.get('precio')
    return None