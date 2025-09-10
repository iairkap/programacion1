def pedir_piso(garage):
    return pedir_num_natural(max =len(garage))





        


def mostrar_estado_garage(garage):
    print("\n--- ESTADO DEL GARAGE ---")
    imprimir_piso = lambda idx, piso: (
        print(f"\nPiso {idx}:"),
        [print(
            f"  Slot {slot[0]}: {'Ocupado' if slot[3] else 'Libre'} | Patente: {slot[1] if slot[3] else '-'} | Tipo: {slot[6] if slot[3] else '-'}"
        ) for slot in piso]
    )
    for idx in range(len(garage)):
        imprimir_piso(idx, garage[idx])

def pedir_patente():
    # estructura de patente 
    # NUEVA = AB123CD
    # VIEJA = ABC123

    while True:
        try:
            patente = input("ingrese la patente:").strip().upper()
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
            num = int(input("ingresa el numero: "))
            if num < min or num > max:
                print(f"el nuero ingresado tiene que ser un num valido, entre {min} y {max}")
            else: return num
        except ValueError:
            print("por favor ingresa un numero")
        except Exception as e : 
            print(e)