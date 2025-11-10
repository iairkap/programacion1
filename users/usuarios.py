""" 
Creacion de usuario 
"""
from colorama import Fore, Style
from .pass_logic import login, UsuarioNoExisteError
from auxiliares.consola import clear_screen
import os

def mostrar_mensaje(msg, tipo="info"):
    colores = {
        "info": Fore.CYAN,
        "ok": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW
    }
    color = colores.get(tipo, Fore.WHITE)
    print(f"{color}{msg}{Style.RESET_ALL}")


def campo_no_vacio(msg, nombre_campo):
    while True:
        try:
            valor = input(msg)
            if valor.strip():
                return valor.strip()
            mostrar_mensaje(f"Error: El {nombre_campo} no puede estar vacío. Intente de nuevo.", "error")
        except KeyboardInterrupt:
            mostrar_mensaje("Operación cancelada por el usuario.", "warning")
            return None
        

def email_valido():
    while True:
        try:
            email = input("Ingrese su email: ")
            if not email.strip():
                mostrar_mensaje("Error: El email no puede estar vacío. Intente de nuevo.", "error")
                continue
            
            # Validar formato
            es_valido, mensaje = validacion_formato_email(email)
            if es_valido:
                return email.strip()
            mostrar_mensaje(f"Error en el email: {mensaje}. Intente nuevamente.", "error")
        
        except KeyboardInterrupt:
            mostrar_mensaje("Operación cancelada por el usuario.", "warning")
            return None
    


def creacion_usuario(mail):
    try:
        usuario = {}
        usuario['nombre'] = campo_no_vacio("Ingrese su nombre: ", "nombre")
        if usuario['nombre'] is None:
            return None
        usuario['apellido'] = campo_no_vacio("Ingrese su apellido: ", "apellido")
        if usuario['apellido'] is None:
            return None
        
        usuario['email'] = mail
        if usuario['email'] is None:
            return None
        
        usuario['admin'] = "False"
    except ValueError:
        mostrar_mensaje("Error: Entrada inválida. Intente de nuevo.", "error")
        return None
    
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
            nombre, apellido, user_email = line.strip().split(',')
            if user_email == email:
                arch_users.close()
                return True
        
        arch_users.close()
        return False
    
    except FileNotFoundError:
        mostrar_mensaje("Error: El archivo de usuarios no existe.", "error")
        return False


def user_login(email):
    """Funcion para loguearse - retorna el usuario completo"""
    try:
        # email = input("Ingrese su email: ")
        # password = input("Ingrese su contraseña: ")
        arch_users = open("files/users.csv", mode="r", encoding="utf-8")
        next(arch_users)  # Saltar la primera linea (headers)
        
        for line in arch_users:
            nombre, apellido, user_email,admin = line.strip().split(',')
            if user_email == email :
                arch_users.close()
                return {
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': user_email,
                    'admin': admin
                }
        nuevo_usuario = registrar_nuevo_usuario(email)
        if nuevo_usuario:
            print(Fore.GREEN + "Usuario registrado. Ahora puede iniciar sesión." + Style.RESET_ALL)
            clear_screen()
            return nuevo_usuario
        mostrar_mensaje("Error: Email o contraseña incorrectos.", "error")
        arch_users.close()
        return None
    
    except FileNotFoundError:
        mostrar_mensaje("Error: El archivo de usuarios no existe.", "error")
        return None
    except UsuarioNoExisteError as e:
        Print(e, "se cancelo la creacion del usuario ")
        return None
        
def registrar_nuevo_usuario(email):
    """Función completa para registrar un nuevo usuario"""
    crear_archivo_users()
    #chequear si existen usuarios previo para asignar admin 
    cantidad_usuarios = 0
    try:
        with open("files/users.csv", mode="r", encoding="utf-8") as arch_users:
            next(arch_users)  # Saltar header
            for _ in arch_users:
                cantidad_usuarios += 1
    except FileNotFoundError:
        cantidad_usuarios = 0
    
    usuario = creacion_usuario(email)
    if cantidad_usuarios == 0:#si es el primer usuario se logea como admin
        usuario['admin'] = "True"
        mostrar_mensaje("Este es el primer usuario registrado, se le ha asignado rol de administrador.", "ok")
    else:
        usuario['admin'] = "False"
    if not usuario:
        mostrar_mensaje("No se pudo crear el usuario.", "error")
        return False

    try:
        arch_users = open("files/users.csv", mode="a", encoding="utf-8")
        arch_users.write(f"{usuario['nombre']},{usuario['apellido']},{usuario['email']},{usuario['admin']}\n")
        arch_users.close()
        # mostrar_mensaje(f"Usuario creado exitosamente: {usuario}", "ok")
        return usuario
    except Exception as e:
        mostrar_mensaje(f"Error al guardar el usuario: {e}", "error")
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

def mostrar_usuarios_admin(admin = False):
    """mostrar los usuarios que son admin o no son admin dependiendo del parametro"""
    print("\n=== LISTA DE USUARIOS DISPONIBLES ===")
    with open("files/users.csv", mode="r", encoding="utf-8") as arch_users:
        next(arch_users)  # Saltar la primera linea (headers)
        count = 0
        for linea in arch_users:
            nombre, apellido, user_email,admin_user = linea.strip().split(',')
            if (admin and admin_user == "True") or (not admin and admin_user == "False"):
                count += 1
                print(f"{count}- {nombre} {apellido} ({user_email})")
                
    return count

    
def asignar_admin():
    while True:
        try:
            print("\n=== ASIGNAR ADMINISTRADOR ===")
            cantidad_usuarios_disp = mostrar_usuarios_admin(admin=False)
            if cantidad_usuarios_disp == 0:
                print(Fore.YELLOW + "No hay usuarios disponibles para asignar como admin." + Style.RESET_ALL)
                return 0

            indice = input("Seleccione el número del usuario a asignar como admin (o 'q' para salir): ")
            if indice.lower() == 'q':
                clear_screen()
                return 0
            if not indice.isdigit() or int(indice) < 1 or int(indice) > cantidad_usuarios_disp:
                print(Fore.RED + "Opción inválida. Intente de nuevo." + Style.RESET_ALL)
                continue

            indice = int(indice)
            temp_file = "files/temp_users.csv"

            with open("files/users.csv", "r", encoding="utf-8") as original, \
                 open(temp_file, "w", encoding="utf-8") as temp:
                header = next(original)
                temp.write(header)
                contador_visibles = 0
                for linea in original:
                    nombre, apellido, user_email, admin_user = linea.strip().split(',')
                    if admin_user == "False":
                        contador_visibles += 1
                        if contador_visibles == indice:
                            temp.write(f"{nombre},{apellido},{user_email},True\n")
                            continue
                    temp.write(linea)

            os.replace(temp_file, "files/users.csv")
            print(Fore.GREEN + "Usuario asignado como administrador correctamente." + Style.RESET_ALL)
            return 1

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nOperación cancelada por el usuario." + Style.RESET_ALL)
            return 0


def eliminar_admin():
    while True:
        try:
            print("\n=== ELIMINAR ADMINISTRADOR ===")
            cantidad_usuarios_disp = mostrar_usuarios_admin(admin=True)
            if cantidad_usuarios_disp == 0:
                print(Fore.YELLOW + "No hay administradores disponibles para eliminar." + Style.RESET_ALL)
                return 0
            if cantidad_usuarios_disp == 1:
                print(Fore.RED + "No se puede eliminar el único administrador restante." + Style.RESET_ALL)
                return 0
            indice = input("Seleccione el número del administrador a eliminar (o 'q' para salir): ")
            if indice.lower() == 'q':
                clear_screen()
                return 0
            if not indice.isdigit() or int(indice) < 1 or int(indice) > cantidad_usuarios_disp:
                print(Fore.RED + "Opción inválida. Intente de nuevo." + Style.RESET_ALL)
                continue

            indice = int(indice)
            temp_file = "files/temp_users.csv"

            with open("files/users.csv", "r", encoding="utf-8") as original, \
                 open(temp_file, "w", encoding="utf-8") as temp:
                header = next(original)
                temp.write(header)
                contador_visibles = 0
                for linea in original:
                    nombre, apellido, user_email, admin_user = linea.strip().split(',')
                    if admin_user == "True":
                        contador_visibles += 1
                        if contador_visibles == indice:
                            temp.write(f"{nombre},{apellido},{user_email},False\n")
                            continue
                    temp.write(linea)

            os.replace(temp_file, "files/users.csv")
            print(Fore.GREEN + "Administrador eliminado correctamente." + Style.RESET_ALL)
            return 1

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nOperación cancelada por el usuario." + Style.RESET_ALL)
            return 0