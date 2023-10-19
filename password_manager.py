import json
import os
import getpass
from cryptography.fernet import Fernet

# Nombre del archivo para almacenar las contraseñas cifradas
PASSWORD_FILE = "passwords.json"

def load_key():
    try:
        return open("key.key", "rb").read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
cipher_suite = Fernet(key)

# Verifica si el archivo de contraseñas existe y lo carga
if os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, 'rb') as file:
        encrypted_passwords = file.read()
        decrypted_passwords = cipher_suite.decrypt(encrypted_passwords)
        passwords = json.loads(decrypted_passwords.decode())
else:
    passwords = {}

def save_passwords():
    encrypted_passwords = cipher_suite.encrypt(json.dumps(passwords).encode())
    with open(PASSWORD_FILE, 'wb') as file:
        file.write(encrypted_passwords)

def display_menu():
    print("Gestor de Contraseñas")
    print("1. Mostrar contraseñas")
    print("2. Agregar una contraseña")
    print("3. Eliminar una contraseña")
    print("4. Salir")

while True:
    display_menu()
    choice = input("Seleccione una opción: ")

    if choice == "1":
        for site, password in passwords.items():
            print(f"Sitio: {site}, Contraseña: {password}")
    elif choice == "2":
        site = input("Ingrese el nombre del sitio: ")
        password = getpass.getpass("Ingrese la contraseña: ")
        passwords[site] = password
        save_passwords()
        print("Contraseña guardada con éxito.")
    elif choice == "3":
        site = input("Ingrese el nombre del sitio cuya contraseña desea eliminar: ")
        if site in passwords:
            del passwords[site]
            save_passwords()
            print("Contraseña eliminada con éxito.")
        else:
            print("El sitio no existe en la base de datos.")
    elif choice == "4":
        print("Saliendo del gestor de contraseñas.")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
