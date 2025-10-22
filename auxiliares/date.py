import time


def get_current_time_json():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def calculo_cantidad_de_horas(hora_entrada, hora_salida):
    "La funcion va a recibir dos strings con el formato 'YYYY-MM-DD HH:MM:SS'"
    formato = "%Y-%m-%d %H:%M:%S"
    tiempo_entrada = time.strptime(hora_entrada, formato)
    tiempo_salida = time.strptime(hora_salida, formato)
    segundos_entrada = time.mktime(tiempo_entrada)
    segundos_salida = time.mktime(tiempo_salida)
    diferencia_segundos = segundos_salida - segundos_entrada
    horas = diferencia_segundos / 3600
    return horas


def  fecha_json_to_readable(fecha_json):
    """Convierte una fecha en formato JSON a un formato legible 'DD/MM/YYYY HH:MM'"""
    struct_time = time.strptime(fecha_json, "%Y-%m-%d %H:%M:%S")
    return time.strftime("%d/%m/%Y %H:%M", struct_time)