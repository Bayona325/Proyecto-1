from colorama import Fore, init, Style
import os
import json
import csv
import random
from tabulate import tabulate

init(autoreset=True)

def MostrarEstadisticas(estadisticas):
    tabla = []
    for aciertos, cantidad in estadisticas.items():
        tabla.append([f"{aciertos} aciertos", cantidad])
    print(tabulate(tabla, headers=["Aciertos", "Veces"], tablefmt="grid"))

def limpiarconsola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def escribirConsola(texto: str, color = Fore.WHITE):
    print(f"{color}{texto}")

def ENTERContinuar(mensaje: str = Fore.CYAN + "\nPresione ENTER para continuar:\n -> "):
    input(mensaje)

def CompraBoletos():
    boletos = []
    cantidad = int(input(Fore.MAGENTA + Style.BRIGHT + "¿Cuántos boletos desea comprar?: "))
    for i in range(cantidad):
        print(f"\nBoleto {len(boletos) + 1}:")
        boletos.append(EscogerNumeros())
    return boletos
    '''Ingresa los datos del comprador como ID, Nombre y Cantidad de dinero ingresado, 
    si el dinero es suficiente para un boleto lo compra.
    Aun asi se le pide la cantidad de boletos que quiere comprar y verifica si cumple con la cantidad de dinero requerida'''


def EscogerNumeros():
    numeros = []
    while len(numeros) < 6:
        try:
            num = int(input(Fore.BLUE + Style.BRIGHT + f"Ingrese el número {len(numeros) + 1} (1-49): " + Style.RESET_ALL))
            if num < 1 or num > 49:
                print(Fore.RED + Style.BRIGHT + "El número debe estar entre 1 y 49." + Style.RESET_ALL)
            elif num in numeros:
                print(Fore.YELLOW + Style.BRIGHT + "Número repetido. Intente de nuevo." + Style.RESET_ALL)
            else:
                numeros.append(num)
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "¡ERROR!\nIngrese un número válido." + Style.RESET_ALL)
    return numeros
'''Hay que tener en cuaenta de que un usuario puede escribir los mismos numeros que otro, 
por ello hay que verificar que no se repitan'''

#def verificarNum():
#    '''Verifica si los numeros ingresados por el usuario no estan repetidos con ningun otro boleto ya comprado,
#    y muestra cuales de los numeros estan en ese otro boleto'''
#    pass

def GuardarHistorial(boleto, ganadores, resultado):
    historial = {
        "boleto": boleto,
        "ganadores": ganadores,
        "aciertos": resultado[0],
        "premio": resultado[1]
    }
    with open("historial.json", "a") as file:
        json.dump(historial, file)
        file.write("\n")    
    '''Ve el historial de las compras del usuario, con datos como el numero de sus boletos comprados
    y cuales de esos numeros eran iguales al numero ganador marcados con color verde'''


def GenerarNumerosGanadores():
    return random.sample(range(1, 50), 6)    
'''Verifica la cantidad de numeros que sean iguales al numero ganador y
    da el premio segun la cantidad de numeros que concuerdan, guardando el analisis en el historial del usuario'''

def VerificarGanador(boleto, ganadores):
    aciertos = len(set(boleto) & set(ganadores))
    premios = {
        3: "Premio pequeño",
        4: "Premio mediano",
        5: "Premio grande",
        6: "Premio mayor"
    }
    return aciertos, premios.get(aciertos, "No ganó")

def SimularSorteos(cantidad: int):
    estadisticas = {i: 0 for i in range(7)}  # Contador de aciertos (0-6)
    for _ in range(cantidad):
        ganadores = GenerarNumerosGanadores()
        boleto = random.sample(range(1, 50), 6)
        aciertos = len(set(boleto) & set(ganadores))
        estadisticas[aciertos] += 1
    return estadisticas

menu =  Style.BRIGHT + f"""
--------------------------------------------------------
| ██╗░░░░░░█████╗░████████╗███████╗██████╗░██╗░█████╗░ |
| ██║░░░░░██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║██╔══██╗ |
| ██║░░░░░██║░░██║░░░██║░░░█████╗░░██████╔╝██║███████║ |
| ██║░░░░░██║░░██║░░░██║░░░██╔══╝░░██╔══██╗██║██╔══██║ |
| ███████╗╚█████╔╝░░░██║░░░███████╗██║░░██║██║██║░░██║ |
| ╚══════╝░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝╚═╝░░╚═╝ |
|______________________________________________________| 
|            |1. Compra de la boleta  |                |
|            |2. Boletos comprados    |                |
|            |3. Hacer sorteo         |                |
|            |4. Historial de sorteos |                |
|            |5. Simular sorteo       |                |
|            |6. Salir                |                |
--------------------------------------------------------
"""

while True:
    limpiarconsola()
    escribirConsola(menu, Fore.GREEN)
    opcion = input(Fore.MAGENTA + Style.BRIGHT + "Digite la opción que necesite:\n -> " + Style.RESET_ALL)
    if opcion == "1":
        boletos = CompraBoletos()
        ENTERContinuar()
    elif opcion == "2":
        ENTERContinuar()
    elif opcion == "3":
        ganadores = GenerarNumerosGanadores()
        print(Fore.GREEN + Style.BRIGHT + f"Números ganadores: {ganadores}")
        for boleto in boletos:
            resultado = VerificarGanador(boleto, ganadores)
            print(f"Boleto {boleto}: {resultado[0]} aciertos - {resultado[1]}")
            GuardarHistorial(boleto, ganadores, resultado)
        ENTERContinuar()
    elif opcion == "4":
        print(Fore.MAGENTA + Style.BRIGHT + "Historial de sorteos:")
        # Código para leer y mostrar el archivo JSON/CSV
        ENTERContinuar()
    elif opcion == "5":
        cantidad = int(input(Fore.MAGENTA + Style.BRIGHT + "Ingrese la cantidad de simulaciones que quiere hacer: \n -> "))
        SimularSorteos(cantidad)
        ENTERContinuar()
    elif opcion == "6":
        print("Saliendo del programa...")
        break
    else:
        print(Fore.RED + Style.BRIGHT + "\n¡SELECCIONE UNA OPCIÓN CORRECTA!")
        ENTERContinuar()

# Cosas a solucionar

# 1. En la compra de boletos, se debe hacer una comparación al final de todos los boletos vendidos hasta ahora
# En el caso de que exista un boleto que tenga todos los mismos numeros en el mismo orden, no se guarda en el historial de compra

# 2. A la hora de hacer el sorteo, solo se cuenta como acierto si el numero que es igual tiene la misma posicion que el numero ganador,
# Ejemplo: Si el primer numero gandor es 3, el primer numero del boleto tambien debe ser 3 para que cuente como un numero igual, el 3 no puede 
# ser un numero en la posicion 5 si en el boleto ganador estaba en la posicion 1

# 3. Toca hacer una funcion que permita ver los boletos comprados hasta ahora y a quien pertenencen

# 4. El simulador de sorteo no funciona correctamente.

# 5. Hacer que antes de realizar la compra, pregunte por los datos de la persona para identificar a quien pertenece el boleto,
# tambien saber cuanto dinero tiene y si no tiene el precio del boleto ($5) el boleto no puede ser comprado, y si pide varios boletos
# la cantidad de dinero debe ser coerente a la cantidad de estos, o bien el programa solo permita la compra de la cantidad de boletos 
# que se pueda permitir con el dinero ingresado.0

# 6. Despues de hacer el sorteo para saber el boleto ganador, se registra los boletos usados, 
# pero debe ser posible volver a usarlos despues del sorteo

# 7. Se necesita 2 archivos .json uno para saber cuales boletas estan en juego y otro para ver el historial de compras de los juegos pasados
