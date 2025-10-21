"""Módulo de precios para el garage.

Funciones principales:
- configurar_precios(): devuelve el diccionario de tarifas (docstring/help).
- leer_slots_csv(ruta): lee un CSV de slots y devuelve lista de dicts.
- calcular_tiempo(hora_entrada, hora_salida=None): devuelve horas float y dias int.
- calcular_tarifa_slot(slot, precios, hora_salida=None): calcula costo para un slot ocupado.
- calcular_costos_desde_csv(ruta_csv, precios=None): suma costos por tipo desde un CSV.

Este módulo no depende de datos de prueba (mockdata). Trabaja con los CSV
ubicados en la carpeta `files/` del proyecto.
"""

import csv
import math
from datetime import datetime
from typing import Dict, Tuple, List, Optional

DATE_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]


def configurar_precios() -> Dict[str, Dict[str, float]]:
    """Devuelve las tarifas por tipo de vehículo.

    La estructura devuelta es:
      {"auto": {"por_hora": 100.0, "por_dia": 1000.0}, ...}

    Puedes inspeccionar esta función con `help(garage.precios.configurar_precios)`
    para obtener esta documentación en runtime.
    """
    return {
        "auto": {"por_hora": 100.0, "por_dia": 1000.0},
        "moto": {"por_hora": 50.0, "por_dia": 500.0},
        "camion": {"por_hora": 200.0, "por_dia": 2000.0},
        "bici": {"por_hora": 20.0, "por_dia": 200.0},
        "otro": {"por_hora": 100.0, "por_dia": 1000.0},
    }


def _parse_bool(val) -> bool:
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    return str(val).strip().lower() in ("true", "1", "t", "yes", "y")


def leer_slots_csv(ruta: str) -> List[Dict[str, str]]:
    """Lee un CSV de slots y devuelve una lista de diccionarios.

    Espera columnas como: 'ocupado','hora_entrada','tipo_vehiculo' o 'tipo_slot'.
    Si el archivo no existe lanza FileNotFoundError.
    """
    with open(ruta, mode="r", encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        return [dict(fila) for fila in lector]


def _parse_datetime(s: str) -> datetime:
    """Intenta parsear una cadena en varios formatos definidos en DATE_FORMATS."""
    if s is None:
        raise ValueError("Valor de fecha es None")
    s = str(s).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    # si ninguno funcionó, intentar truncar segundos si hay punto decimal
    raise ValueError(f"Formato de fecha no reconocido: {s}")


def calcular_tiempo(hora_entrada: str, hora_salida: Optional[str] = None) -> Tuple[float, int]:
    """Devuelve (horas_float, dias_int) entre entrada y salida.

    - hora_entrada/hora_salida: strings con formato '%Y-%m-%d %H:%M:%S' o '%Y-%m-%d %H:%M'.
    - Si hora_salida es None usa datetime.now().
    - Dias = ceil(horas/24) si horas>0.
    """
    entrada_dt = _parse_datetime(hora_entrada)
    if hora_salida is None:
        salida_dt = datetime.now()
    else:
        salida_dt = _parse_datetime(hora_salida)

    if salida_dt < entrada_dt:
        raise ValueError("hora_salida debe ser posterior a hora_entrada")

    delta = salida_dt - entrada_dt
    horas = delta.total_seconds() / 3600.0
    dias = math.ceil(horas / 24.0) if horas > 0 else 0
    return horas, dias


_TIPO_MAP = {"1": "moto", "2": "auto", "3": "camion", "4": "bici"}


def _mapear_tipo(tipo_raw) -> str:
    """Mapea un valor bruto a la clave de tipo usada en las tarifas.

    Acepta números (int o string) y nombres ya escritos.
    """
    if tipo_raw is None:
        return "otro"
    if isinstance(tipo_raw, int):
        return _TIPO_MAP.get(str(tipo_raw), "otro")
    s = str(tipo_raw).strip()
    if s == "":
        return "otro"
    if s in ("auto", "moto", "camion", "bici", "otro"):
        return s
    return _TIPO_MAP.get(s, "otro")


def calcular_tarifa_slot(slot: Dict[str, str], precios: Optional[Dict[str, Dict[str, float]]] = None,
                         hora_salida: Optional[str] = None) -> float:
    """Calcula el costo para un slot (fila) leído desde el CSV.

    Reglas:
    - Si la duración <= 12 horas: se cobra por hora iniciada (ceil), mínimo 1 hora.
    - Si la duración > 12 horas: se cobra por día (ceil horas/24).

    slot: diccionario con al menos las claves 'ocupado' y 'hora_entrada', y
          'tipo_vehiculo' o 'tipo_slot'.
    precios: estructura devuelta por `configurar_precios()`.
    """
    if precios is None:
        precios = configurar_precios()

    ocupado = _parse_bool(slot.get("ocupado"))
    hora_entrada = slot.get("hora_entrada")
    if not ocupado or not hora_entrada:
        return 0.0

    tipo_raw = slot.get("tipo_vehiculo") or slot.get("tipo_slot")
    tipo = _mapear_tipo(tipo_raw)

    horas, dias = calcular_tiempo(hora_entrada, hora_salida)
    horas = max(0.0, horas)

    if horas <= 12:
        horas_cobradas = max(1, math.ceil(horas))
        costo = horas_cobradas * precios[tipo]["por_hora"]
    else:
        dias_cobrados = max(1, math.ceil(horas / 24.0))
        costo = dias_cobrados * precios[tipo]["por_dia"]

    return round(float(costo), 2)


def calcular_costos_desde_csv(ruta_csv: str, precios: Optional[Dict[str, Dict[str, float]]] = None,
                              hora_salida: Optional[str] = None) -> Dict[str, float]:
    """Lee el CSV y devuelve un diccionario con totales por tipo de vehículo.

    Devuelve: {'auto': total, 'moto': total, 'camion': total, 'bici': total, 'otro': total}
    """
    if precios is None:
        precios = configurar_precios()

    filas = leer_slots_csv(ruta_csv)
    totales = {k: 0.0 for k in precios.keys()}
    totales.setdefault("otro", 0.0)

    for fila in filas:
        try:
            costo = calcular_tarifa_slot(fila, precios, hora_salida)
        except Exception:
            # ignorar filas mal formadas y seguir
            continue
        tipo_raw = fila.get("tipo_vehiculo") or fila.get("tipo_slot")
        tipo = _mapear_tipo(tipo_raw)
        if tipo not in totales:
            totales["otro"] += costo
        else:
            totales[tipo] += costo

    return totales


if __name__ == "__main__":
    # Demo rápido cuando se ejecuta directamente
    ruta_demo = "files/garage-7.csv"
    print("Precios por defecto:", configurar_precios())
    try:
        resumen = calcular_costos_desde_csv(ruta_demo)
        print("Resumen de costos desde", ruta_demo)
        for t, v in resumen.items():
            print(f"  {t}: {v}")
    except FileNotFoundError:
        print("Archivo demo no encontrado:", ruta_demo)
