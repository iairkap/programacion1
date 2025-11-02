"""Función para guardar en memoria las tarifas actualizadas cuando se obtiene el garage_id.
Las tarifas se encuentran almacenadas en el csv tarifas.csv
Header del csv: garage_id,tipo,periodo_mensual,precio,moneda,descripcion
"""
from constantes.tipos_vehiculos import obtener_nombre_vehiculo
from colorama import Fore, Style
from auxiliares.consola  import clear_screen


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

def print_tarifas(tarifas):
    """Imprime las tarifas en formato de tabla con colores."""
    if not tarifas:
        print(Fore.YELLOW + "No hay tarifas disponibles para este garage." + Style.RESET_ALL)
        return
    
    print(Fore.CYAN + "\n" + "="*70 + Style.RESET_ALL)
    print(Fore.CYAN + "TARIFAS DEL GARAGE" + Style.RESET_ALL)
    print(Fore.CYAN + "="*70 + Style.RESET_ALL)
    
    # Encabezados
    print(Fore.LIGHTWHITE_EX + f"{'Tipo':<15} {'Período':<15} {'Precio':<15} {'Moneda':<10}" + Style.RESET_ALL)
    print(Fore.CYAN + "-"*70 + Style.RESET_ALL)
    
    # Datos
    for tarifa in tarifas:
        # Validar que tenga al menos: garage_id, tipo, periodo, precio
        if len(tarifa) < 4:
            continue
        
        try:
            tipo_numero = int(tarifa[1])
            tipo = obtener_nombre_vehiculo(tipo_numero)
            
            periodo = "Mensual" if tarifa[2] == "True" else "Diario"
            precio = tarifa[3]
            moneda = tarifa[4] if len(tarifa) > 4 else "ARS"
            
            # Colorear según tipo
            if tipo == "moto":
                color = Fore.GREEN
            elif tipo == "auto":
                color = Fore.YELLOW
            elif tipo == "camioneta":
                color = Fore.RED
            else:
                color = Fore.WHITE
            
            print(color + f"{tipo.capitalize():<15} {periodo:<15} ${precio:<14} {moneda:<10}" + Style.RESET_ALL)
        
        except (ValueError, IndexError):
            continue
    
    print(Fore.CYAN + "="*70 + Style.RESET_ALL)
    print()