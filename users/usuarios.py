""" 
Creacion de usuario 
"""
garage_id = 0

def creacion_usuario():
    try:
        usuario = {}
        usuario['nombre'] = input("Ingrese su nombre: ")
        usuario['apellido'] = input("Ingrese su apellido: ")
        usuario['email'] = input("Ingrese su email: ")
        usuario['password'] = input("Ingrese su contraseña: ")
        
        # Bucle while solo para confirmar contraseña
        while True:
            usuario['confirmar_password'] = input("Confirme su contraseña: ")
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

usuario = creacion_usuario()

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

if usuario:
    arch_users = open("files/users.csv", mode="a", encoding="utf-8")
    #Hay que verificar si ya existe el email en el sistema
    if chequear_existencia_email(usuario['email']):
        print("Error: El email ya existe en el sistema.")
    else:
        arch_users.write(f"{usuario['nombre']},{usuario['apellido']},{usuario['email']},{usuario['password']}\n")
    arch_users.close()
    print("Usuario creado exitosamente:", usuario)
else:
    print("No se pudo crear el usuario.")
    
    
    
def user_login():
    """Funcion para loguearse"""
    try:
        email = input("Ingrese su email: ")
        password = input("Ingrese su contraseña: ")
        
        arch_users = open("files/users.csv", mode="r", encoding="utf-8")
        next(arch_users)  # Saltar la primera linea (headers)
        
        for line in arch_users:
            nombre, apellido, user_email, user_password = line.strip().split(',')
            if user_email == email and user_password == password:
                print(f"Bienvenido {nombre} {apellido}!")
                arch_users.close()
                return True
        
        print("Error: Email o contraseña incorrectos.")
        arch_users.close()
        return False
    
    except FileNotFoundError:
        print("Error: El archivo de usuarios no existe.")
        return False
        