from colorama import Fore, Style


def pedir_piso(garage):
    while True:
        try:
            piso = int(input(f"Ingrese el piso que desea consultar entre 0 y {len(garage)-1}: "))
            if piso < 0 or piso > len(garage) or len(garage) == 0:
                print("El piso ingresado no es válido. Intente nuevamente.")
            else:
                return piso            
        except Exception as e:
            print(e)

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
    

def es_subscripcion_mensual(patente):
    """Chequea si la subscripcion es mensual o diaria"""
    info_patentes = acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
            return info[3] 


def mostrar_estado_garage(garage):
    print(Fore.GREEN + "\n--- ESTADO DEL GARAGE ---" + Style.RESET_ALL)
    imprimir_piso = lambda idx, piso: (
        print(f"\nPiso {idx}:"),
        [print(
            f"  Slot {slot['id']}: {'Ocupado' if slot['ocupado'] else 'Libre'} | Patente: {slot['patente'] if slot['ocupado'] else '-'} | Tipo: {slot['tipo_vehiculo_estacionado'] if slot['ocupado'] else '-'}"
        ) for slot in piso]
    )
    for idx in range(len(garage)):
        imprimir_piso(idx, garage[idx])
    input(Fore.YELLOW + '\nPresione cualquier tecla para continuar...' + Style.RESET_ALL) 

def pedir_patente():
    # estructura de patente 
    # NUEVA = AB123CD
    # VIEJA = ABC123
    while True:
        try:
            patente = input(Fore.YELLOW + "\nIngrese la patente:" + Style.RESET_ALL).strip().upper()
            digitos = len(patente)
            if digitos != 6 and digitos != 7:
                print(Fore.RED + "\nLas nuevas patentes tienen 7 digitos y las antiguas 6\n" + Style.RESET_ALL)
            elif digitos == 6 :
                if patente[:3].isalpha() and patente[3:].isdigit():
                    return patente
            elif digitos == 7 :
                if patente[:2].isalpha() and patente[2:5].isdigit() and patente[5:].isalpha():
                    return patente
            else: 
                print(Fore.RED + "La patente no tiene el formato correcto ej: AB123CD o ABC123" + Style.RESET_ALL)
                
            print("Volve a intentarlo")

        except Exception as e:
            print(e)
    
def pedir_tipo_vehiculo():
    return pedir_num_natural(min = 1, max = 4)
    
def pedir_num_natural(max,mensaje_personalizado = "\nIngresa el tipo de vehiculo (1/Moto. 2/Auto. 3/Camioneta ): ",min = 0):
    while True:
        try:
            num = int(input(mensaje_personalizado))
            if num < min or num > max:
                print(f"\nEl numero ingresado tiene que ser un numero valido, entre {min} y {max}")
            else: return num
        except ValueError:
            print("\nPor favor ingresa un numero")
        except Exception as e : 
            print(e)
            
            
            
            
