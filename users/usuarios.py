""" 
Creacion de usuario 
"""


def campo_no_vacio(msg, nombre_campo):
    while True:
        try:
            valor = input(msg)
            if valor.strip():
                return valor.strip()
            print(f"Error: El {nombre_campo} no puede estar vacío. Intente de nuevo.")
        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario.")
            return None
        
        
def email_valido():
    while True:
        try:
            email = input("Ingrese su email: ")
            if not email.strip():
                print("Error: El email no puede estar vacío. Intente de nuevo.")
                continue
            
            # Validar formato
            es_valido, mensaje = validacion_formato_email(email)
            if es_valido:
                return email.strip()
            print(f"Error en el email: {mensaje}. Intente nuevamente.")
        
        except KeyboardInterrupt:
            return None
    



def creacion_usuario():
    try:
        usuario = {}
        
        # Bucle while solo para confirmar contraseña
        #Validar datos que no esten vacios
        
        usuario['nombre'] = campo_no_vacio("Ingrese su nombre: ", "nombre")
        if usuario['nombre'] is None:
            return None
        usuario['apellido'] = campo_no_vacio("Ingrese su apellido: ", "apellido")
        if usuario['apellido'] is None:
            return None
        
        usuario['email'] = email_valido()
        if usuario['email'] is None:
            return None

        usuario['password'] = campo_no_vacio("Ingrese su contraseña: ", "contraseña")
        if usuario['password'] is None:
            return None

        while True:
            usuario['confirmar_password'] = input("Confirme su contraseña: ")
            if usuario['password'] == usuario['confirmar_password']:
                break
            print("Error: Las contraseñas no coinciden. Intente nuevamente.")
            
            
            validacion_email = validacion_formato_email(usuario['email'])
            if not validacion_email[0]:
                print(f"Error en el email: {validacion_email[1]}. Intente nuevamente.")
                usuario['email'] = input("Ingrese su email: ")
                continue
            if usuario['password'] == usuario['confirmar_password']:
                break
            else:
                print("Error: Las contraseñas no coinciden. Intente nuevamente.")
        
    except ValueError:
        print("Error: Entrada inválida. Intente de nuevo.")
        return None
    
    del usuario['confirmar_password']
    return usuario

def crear_archivo_users():
    """Crea el archivo users.csv con headers si no existe"""
    try:
        # Intenta abrir el archivo en modo lectura para ver si existe
        arch_test = open("files/users.csv", mode="r", encoding="utf-8")
        arch_test.close()
    except FileNotFoundError:
        # Si no existe, lo crea con los headers
        arch_users = open("files/users.csv", mode="w", encoding="utf-8")
        arch_users.write("nombre,apellido,email,password\n")
        arch_users.close()

# Crear archivo si no existe
crear_archivo_users()


def chequear_existencia_email(email):
    """Chequea si el email existe en el sistema
    retorna True si existe, else False"""
    try:
        arch_users = open("files/users.csv", mode="r", encoding="utf-8")
        next(arch_users)  # Saltar la primera linea (headers)
        
        for line in arch_users:
            nombre, apellido, user_email, user_password = line.strip().split(',')
            if user_email == email:
                arch_users.close()
                return True
        
        arch_users.close()
        return False
    
    except FileNotFoundError:
        print("Error: El archivo de usuarios no existe.")
        return False


    
    
    
def user_login():
    """Funcion para loguearse - retorna el usuario completo"""
    try:
        email = input("Ingrese su email: ")
        password = input("Ingrese su contraseña: ")
        
        arch_users = open("files/users.csv", mode="r", encoding="utf-8")
        next(arch_users)  # Saltar la primera linea (headers)
        
        for line in arch_users:
            nombre, apellido, user_email, user_password = line.strip().split(',')
            if user_email == email and user_password == password:
                arch_users.close()
                return {
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': user_email,
                    'password': user_password
                }
        
        print("Error: Email o contraseña incorrectos.")
        arch_users.close()
        return None
    
    except FileNotFoundError:
        print("Error: El archivo de usuarios no existe.")
        return None
        
def registrar_nuevo_usuario():
    """Función completa para registrar un nuevo usuario"""
    crear_archivo_users()
    usuario = creacion_usuario()
    
    if not usuario:
        print("No se pudo crear el usuario.")
        return False
    
    # Verificar si el email ya existe
    if chequear_existencia_email(usuario['email']):
        print("Error: El email ya existe en el sistema.")
        return False
    
    # Escribir el usuario al archivo
    try:
        arch_users = open("files/users.csv", mode="a", encoding="utf-8")
        arch_users.write(f"{usuario['nombre']},{usuario['apellido']},{usuario['email']},{usuario['password']}\n")
        arch_users.close()
        print("Usuario creado exitosamente:", usuario)
        return True
    except Exception as e:
        print(f"Error al guardar el usuario: {e}")
        return False
    
    
def validacion_formato_email(email):

    if email is None:
        return False, "Email nulo"
    email = email.strip()
    if email == "":
        return False, "Email vacío"

    # 1) exactamente una @
    if email.count("@") != 1:
        return False, "Debe contener exactamente una '@'"

    at = email.find("@")
    local = email[:at]
    dominio = email[at+1:]

    # 2) no vacíos
    if local == "" or dominio == "":
        return False, "Parte local o dominio vacíos"

    # 3) sin puntos consecutivos
    if email.find("..") != -1:
        return False, "No se permiten '..'"

    # ----- Validación de la parte local -----
    # reglas: letras, dígitos, . _ -, y no empieza/termina con '.'
    if local[0] == "." or local[-1] == ".":
        return False, "La parte local no puede empezar/terminar con '.'"
    for ch in local:
        if ch.isalpha() or ch.isdigit() or ch in "._-":
            pass
        else:
            return False, "Caracter inválido en la parte local"

    # ----- Validación del dominio -----
    # reglas: letras, dígitos, . -, al menos un '.', no empieza/termina con '.' ni '-'
    if dominio.find(".") == -1:
        return False, "El dominio debe contener al menos un '.'"
    if dominio[0] in ".-" or dominio[-1] in ".-":
        return False, "El dominio no puede empezar/terminar con '.' o '-'"
    if dominio.find("..") != -1:
        return False, "El dominio no puede tener '..'"

    for ch in dominio:
        if ch.isalpha() or ch.isdigit() or ch in ".-":
            pass
        else:
            return False, "Caracter inválido en el dominio"

    ultimo_punto = -1
    inicio_busqueda = 0
    while True:
        pos = dominio.find(".", inicio_busqueda)
        if pos == -1:
            break
        ultimo_punto = pos
        inicio_busqueda = pos + 1

    tld = dominio[ultimo_punto+1:]  # existe porque hay al menos un '.'
    if len(tld) < 2:
        return False, "El TLD debe tener al menos 2 caracteres"
    for ch in tld:
        if not ch.isalpha():
            return False, "El TLD debe tener solo letras"

    return True, "OK"
        