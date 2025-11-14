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
    """Imprime las tarifas en formato de tabla mejorado."""
    if not tarifas:
        print(Fore.YELLOW + "No hay tarifas disponibles para este garage." + Style.RESET_ALL)
        return
    
    print(f"\n{Fore.CYAN}TARIFAS DEL GARAGE{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{'VEHÍCULO':<20} {'DIARIO':<20} {'MENSUAL':<20}")
    print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
    
    # Organizar tarifas por tipo
    tarifas_por_tipo = {1: {}, 2: {}, 3: {}}  # moto, auto, camioneta
    
    for tarifa in tarifas:
        if len(tarifa) < 4:
            continue
        try:
            tipo_numero = int(tarifa[1])
            periodo_mensual = tarifa[2] == "True"
            precio = float(tarifa[3])
            
            if tipo_numero in tarifas_por_tipo:
                tarifas_por_tipo[tipo_numero][periodo_mensual] = precio
        except (ValueError, IndexError):
            continue
    
    # Imprimir moto
    tipo_nombre = Fore.GREEN + "Moto" + Style.RESET_ALL
    diario = tarifas_por_tipo[1].get(False, 0)
    mensual = tarifas_por_tipo[1].get(True, 0)
    print(f"{tipo_nombre:<29} ${diario:<19.2f} ${mensual:<19.2f}")
    
    # Imprimir auto
    tipo_nombre = Fore.YELLOW + "Auto" + Style.RESET_ALL
    diario = tarifas_por_tipo[2].get(False, 0)
    mensual = tarifas_por_tipo[2].get(True, 0)
    print(f"{tipo_nombre:<29} ${diario:<19.2f} ${mensual:<19.2f}")
    
    # Imprimir camioneta
    tipo_nombre = Fore.RED + "Camioneta/SUV" + Style.RESET_ALL
    diario = tarifas_por_tipo[3].get(False, 0)
    mensual = tarifas_por_tipo[3].get(True, 0)
    print(f"{tipo_nombre:<29} ${diario:<19.2f} ${mensual:<19.2f}")
    
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")