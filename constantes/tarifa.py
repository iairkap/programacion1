"""Función para guardar en memoria las tarifas actualizadas cuando se obtiene el garage_id.
Las tarifas se encuentran almacenadas en el csv tarifas.csv
Header del csv: garage_id,tipo,periodo_mensual,precio,moneda,descripcion
"""


def guardar_precios_garage(garage_id):
    """Obtiene todas las tarifas de un garage desde el CSV.
    Retorna lista de listas con las tarifas: [garage_id, tipo, periodo_mensual, precio, moneda, descripcion]"""
    tarifas_actualizadas = []
    
    try:
        with open('files/tarifas.csv', 'r', encoding='utf-8') as file:
            lineas = file.readlines()
    except FileNotFoundError:
        return tarifas_actualizadas
    
    if not lineas:
        return tarifas_actualizadas
    
    # Saltar header (línea 0)
    for i in range(1, len(lineas)):
        linea = lineas[i].strip()
        if not linea:
            continue
        
        valores = linea.split(',')
        if len(valores) >= 4:  # Mínimo: garage_id, tipo, periodo_mensual, precio
            garage_id_csv = valores[0]
            
            # Comparar garage_id
            if garage_id_csv == str(garage_id):
                tarifas_actualizadas.append(valores)
    
    return tarifas_actualizadas


def obtener_precio_tipo_periodo(tarifas, tipo_vehiculo, periodo_mensual):
    """Obtiene el precio de una tarifa específica para un tipo de vehículo y periodo.
    
    tarifas: lista de listas [[garage_id, tipo, periodo_mensual, precio, ...], ...]
    tipo_vehiculo: número (1=moto, 2=auto, 3=camioneta)
    periodo_mensual: booleano (True=mensual, False=diario)
    
    Retorna: precio (string) o None si no encuentra
    """
    periodo_str = "True" if periodo_mensual else "False"
    
    for tarifa in tarifas:
        if len(tarifa) >= 4:
            tarifa_tipo = tarifa[1]
            tarifa_periodo = tarifa[2]
            tarifa_precio = tarifa[3]
            
            # Comparar tipo y período
            if tarifa_tipo == str(tipo_vehiculo) and tarifa_periodo == periodo_str:
                try:
                    return float(tarifa_precio)
                except ValueError:
                    return None
    
    return None