#!/usr/bin/env python3

import sys
import socket # Establecer conexiones por medio de sockets
from termcolor import colored # Agregar colores al script pip3 install termcolor
import argparse
import signal

# Función para salir del programa hacientro ctrl + c
def ctrl_c(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Panel de ayuda
def get_arguments():
    parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
    parser.add_argument("-t", "--target", required=True, dest="target", help="Victim target to scan (Ex: -t 198.162.10.34)")
    parser.add_argument("-p", "--port", required=True, dest="port", help="Port range to scan (Ex: -p 1-65535)")
    options = parser.parse_args()

    if options.target is None or options.port is None:
        parser.print_help()
        sys.exit(1)

    return options.target, options.port

# Socket
def create_socket():
    s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    s.settimeout(1) # Establecer un tiempo de 1 seg en cada petición
    return s # Retornas el socket creado

def port_scanner(port, host, s):
    try:
        s.connect((host, port)) 
        print(colored(f"\n[+] El puerto {port} está abierto", 'green'))
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        s.close()

def main():
    target, ports_str = get_arguments() 	
    if '-' in port:
        ports = port.split('-')
        for port in range(int(ports[0]), int(ports[1])):
            s = create_socket()
            port_scanner(port, target, s)

    elif ',' in port:
        ports = port.split(',')
        for port in ports:
            s = create_socket()
            port_scanner(int(port), target, s)

if __name__ == '__main__':
    main()
