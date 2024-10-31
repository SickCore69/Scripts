#!/usr/bin/env python3

from termcolor import colored
import sys
import argparse
import signal # Control + c
import subprocess # Ejecutar comandos
from concurrent.futures import ThreadPoolExecutor # Incorporar hilos

# Identificar todos los equipos conectados a la misma red a través del protocolo ICMP

# Función para salir del programa presionando ctrl + c
def ctrl_c(sig, frame):
    print(colored(f"\n[!] Saliendo del programa...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)


# Panel de ayuda
def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta para descubrir hosts activos conectados a tu misma red (ICMP)")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de red a escanear")
    args = parser.parse_args()
    return args.target


def parse_target(target_str):
    target_str_splitted = target_str.split('.')
    first_three_octets = '.'.join(target_str_splitted[:3])

    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[:3]:
            start, end = target_str_splitted[3].split('-')
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end)+1)]
        else:
            return [target_str]
    else: 
        print(colored(f"\n[!] El formato de IP no es valido\n", 'red'))


def host_discovery(targets):
    try:
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)
        if ping.returncode == 0:
            print(colored(f"\n[i] La IP {target} está activa", 'green'))
    except subprocess.TimeoutExpired:
        pass


# La función main() recibe las demás funciones declaradas y las ejecuta
def main():
    # Almacenar el argumento en target_str para después cambiarlos a formato entero
    target_str = get_arguments()
    # parse_target almacena a target_str para convertirlo en un formato correcto y lo almacena en la variable target
    targets = parse_target(target_str)
    print(f"\n[+] Hosts activos en la red:\n")
    max_threads = 100
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(host_discovery, targets)


if __name__ == '__main__':
    main()
