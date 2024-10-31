#!/bin/bash

function ctrl_c(){
	echo -e "\n\n[!] Saliendo...\n"
	tput cnorm; exit 1
}

# Ctrl+C
trap ctrl_c SIGINT

old_process=$(ps -eo user,command)

tput civis # Ocultar el cursor

while true; do
	new_process=$(ps -eo user,command)
	diff <(echo "$old_process") <(echo "$new_process") | grep "[\>\<]" | grep -vE "command|kworker|procmon"  #Aplicar una diferencia entre la variable old_process y new_process
	old_process=$new_process    # Actualizar la variable old_process con el contenido de new_process para que la diferencia aplicada no sea infinita.
done

tput cnorm
