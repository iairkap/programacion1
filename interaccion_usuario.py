def pedir_piso(garage):
    return pedir_num_natural(max =len(garage))

def acceder_a_info_de_patentes(GARAGE):
    """Accede a los datos guardados de las patentes
    retorna la info de todas la petentes en el sistema"""
    datos = []
    for d in GARAGE:
        for pisos in d:
            datos.append(pisos)
    return datos

def chequear_existencia_patente(patente):
    """Chequea si la patente existe en el sistema
    retorna True si existe, else False"""
    info_patentes = acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
                return True
    return False



def buscar_patente(patente):
    info_patentes= acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
            return info


def calcular_costo_de_estadia(patente, hora_salida):
    info_patente = buscar_patente(patente)
    costo = 0
    if not info_patente:
        return "Patente no registrada"
    tipo_de_slot = info_patente[-1]
    if not es_subscripcion_mensual(patente):
        min_entrada = info_patente[-2].split(" ")[1].replace(":", "")
        min_transcurridos = int(hora_salida.replace(":", "")) - int(min_entrada)
        horas_transcurridas = min_transcurridos / 60
        print(f"Horas transcurridas: {horas_transcurridas}")
        costo = COSTOS[tipo_de_slot][0] * horas_transcurridas
    else:
        costo = COSTOS[tipo_de_slot][1] ### Debemos agregar la {ultima fecha de pago??? 
    return costo
    


#creo que esta la hice jp
# def chequear_espacio_libre(garage = GARAGE):
#     """Chequea si hay espacio libre en el estacionamiento"""
#     for piso_idx, piso in enumerate(garage):
#         if len(piso) < 12:
#             fila = piso[-1][0] + 1
#             return (piso_idx, fila) ##Falta retornar algun dato mas??



def es_subscripcion_mensual(patente):
    """Chequea si la subscripcion es mensual o diaria"""
    info_patentes = acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
            return info[3] 


def pedir_patente():
    # estructura de patente 
    # NUEVA = AB123CD
    # VIEJA = ABC123
    while True:
        try:
            patente = input("ingrese la patente:")
            digitos = len(patente)
            if digitos != 6 and digitos != 7:
                print("las nuevas patentes tienen 7 digitos y las antiguas 6")
            elif digitos == 6 :
                if patente[:3].isalpha() and patente[3:].isdigit():
                    return patente
            elif digitos == 7 :
                if patente[:2].isalpha() and patente[2:5].isdigit() and patente[5:].isalpha():
                    return patente
            else: 
                print("la patente no tiene le formato correcto ej: AB123CD o ABC123")
                
            print("volve a intentarlo")

        except Exception as e:
            print(e)
    



def pedir_tipo_vehiculo():
    return pedir_num_natural(min = 1, max = 4)


    
def pedir_num_natural(max,min = 0):
    while True:
        try:
            num = int(input("ingresa el numero"))
            if num < min or num > max:
                print(f"el nuero ingresado tiene que ser un num valido, entre {min} y {max}")
            else: return num
        except ValueError:
            print("por favor ingresa un numero")
        except Exception as e : 
            print(e)