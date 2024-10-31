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
    arp_packet = scapy.ARP(pdst=ip) # Crear el paquete ARP que será enviado a la IP indicada
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_packet/arp_packet # Unir ambos paquetes para ser enviados
    answered, unanswered = scapy.srp(arp_packet, timeout=1, verbose=False) # Envio de paquetes separando las respuestas
    response = answered.summary()

# main() recibe todas las demás funciones para que se ejecuten dentro de ella
def main():
    target = get_arguments()
    scan(target)
