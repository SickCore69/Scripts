#!/bin/bash

function ctrl_c(){
    echo -e "\n\n[!] Saliendo...\n"
    tput cnorm;    # Recuperar el cursor al hacer ctrl + c.
    exit 1    # Salir con un código de estado no exitoso.
}

tput civis    # Ocultar el cursor durante la ejecución del script.

# Ctrl+C
trap ctrl_c SIGINT

for i in $(seq 1 254); do 
    timeout 1 bash -c "ping -c 1 10.10.0.$i" &> /dev/null && echo "[+] Host 10.10.0.$i - Activo." &
done
wait    # Esperar a que finalicen los hilos
tput cnorm			# Recuperar el cursor al finálizar el script.
