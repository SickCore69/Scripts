#!/usr/bin/env python3

import sys
import argparse
import signal
from termcolor import colored
import scapy.all as scapy
import subprocess


# Ctrl + c
def ctrl_c(sig, frame):
    print(colored(f"\n\n[!] Saliendo...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Función para aplicar tratamiento por cada paquete entrante. Recibe los paquetes de prn=
def process_dns_packet(packet):
    if packet.haslayer(scapy.DNSQR): # Filtrar únicamente paquetes que contengan la capa DNS Question Record
        domain = packet[scapy.DNSQR].qname.decode() # Capturar solo los dominios y aplicar un decode ya que se encuentran en formato bytes
        exclude_keywords = ["cloud", "bing", "static", "google"] # Lista negra para que no te incorpore los dominios en el set que hagan referencia a las palabras clave
        # Condicional que muestra solo los dominios que no estan en la lista negra
        if domain not in domains_seen and not any(keyword in domain for keyword in exclude_keywords):
            domains_seen.add(domain) # Agregar el dominio valido al conjunto 
            print(colored(f"\n[+ Dominio: {domain}]", 'green'))


def main():
    global domains_seen # Variable global 
    domains_seen = set() # Variable igualada a un conjunto para que no haya repetición de dominios
    interface = "ens33" 
    # iface=indicar la interfaz para la escucha, filter=filtrar por protocolo y puerto, prn=función que aplica tratamiento por cada paquete, store=0 no almacenar los paquetes en memoria
    print(colored(f"\n[i] Interceptando paquetes:\n", 'blue'))
    scapy.sniff(iface=interface, filter="udp and port 53", prn=process_dns_packet, store=0)


if __name__ == '__main__':
    main()
