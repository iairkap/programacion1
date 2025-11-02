from colorama import Fore, Style
from constantes.tipos_vehiculos import obtener_nombre_vehiculo
from auxiliares.consola import clear_screen

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
    
def es_subscripcion_mensual(patente):
    """Chequea si la subscripcion es mensual o diaria"""
    info_patentes = acceder_a_info_de_patentes()
    for info in info_patentes:
        if patente in info:
            return info[3] 

def mostrar_estado_garage(garage):
    print(Fore.GREEN + "\n--- ESTADO DEL GARAGE ---" + Style.RESET_ALL)
    
    #para el tipo_vehiculo estacionado no quiero imprimir el numero sino el texto del def enum_tipo_vehiculo
    
    imprimir_piso = lambda idx, piso: (
        print(f"\nPiso {idx}:"),
        [print(
            f"  Slot {slot['id']}: {'Ocupado' if slot['ocupado'] else 'Libre'} | Patente: {slot['patente'] if slot['ocupado'] else '-'} | Tipo: {obtener_nombre_vehiculo(slot['tipo_vehiculo']) if slot['ocupado'] else '-'}"
        ) for slot in piso]
    )
    for idx in range(len(garage)):
        imprimir_piso(idx, garage[idx])
    clear_screen()
    

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
                
            print("Volve a intentarlo") #####Arreglar esto

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
            
            
            
            
