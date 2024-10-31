#!/usr/bin/env python3

import sys
import argparse
import signal
from termcolor import colored
import scapy.all as scapy

def ctrl_c(sig, frame):
    print(colored(f"\n[!] Saliendo del programa...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)


def get_arguments():
    parser = argparse.ArgumentParser(description="Escaneo de equipo por ARP")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host / IP range to scan")
    args = parser.parse_args() # Almacenar los paŕametros en args para después retornarlos
    return args.target # Retorno del parámetro target almacenado en args a la función main()

def scan(ip):
    scapy.arping(ip)


# main() recibe todas las demás funciones para que se ejecuten dentro de ella
def main():
    target = get_arguments()
    scan(target)
    
    

if __name__ == '__main__':
    main()
