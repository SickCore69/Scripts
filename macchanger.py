#!/usr/bin/anv python3

import argparse
import re
import subprocess # Ejecutar comandos a nivel de sistema
from termcolor import colored

# Función para mostrar el panel de ayuda. -h mostrar panel
def get_arguments():
    # Instancia de clase que obtiene los argumentos de utiliza el script
    parser = argparse.ArgumentParser(description="Herramienta para cambiar de MAC Address en una interfaz de red")
    # Método para agregar los parámetros a utilizar
    # -i e -- interface son los parámetros a usar, dest es donde se almacenará el contenido de -i y required significa que es necesario ingresar el parámetro para que funcione el script
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Nombre de la interfaz de red")
    parser.add_argument("-m", "--mac", required=True, dest="mac_address", help="Nueva MAC Address a signar a la interfaz de red")
    return parser.parse_args() # Retornar los argumentos para que los reciba la función main()

# Función para validar el contenido de los parámetros
def is_valid_input(interface, mac_address):
    # Regex que indica que el 1er caracter empieza por una e, el 2do caracter pueder una n o una t, el 3ro puede ser una s o una h y por último se valida que haya uno o dos digitos
    is_valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$', interface)
    is_valid_mac_address = re.match('^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$', mac_address)
    # Retorno los matches y si ambos son verdaderos entra en el condicional is_valid_input y te cambia la MAC Address
    return is_valid_interface and is_valid_mac_address

# Función que te cambia la MAC Address
def change_mac_address(interface, mac_address):
    # Condicional que valida si los parámetros se proporcionaron correctamente
    if is_valid_input(interface, mac_address):
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address])
        subprocess.run(["ifconfig", interface, "up"])
        print(colored(f"\n[+] La MAC Address ha sido cambiada: {mac_address}\n", 'green'))
    else:
        print(colored(f"\n[!] Datos incorrectos\n", 'red'))


def main (): # Carga las funciones para correr
    args = get_arguments()
    # Llamada a la función encargada de cambiar la MAC Address. Debe recibir los parámetros interface y mac_address
    change_mac_address(args.interface, args.mac_address)



if __name__ == '__main__': # Inicio del programa
    main()
