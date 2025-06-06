import os
import json
import csv
import random

def limpiarconsola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def ENTERContinuar(mensaje: str = "\nPresione ENTER para continuar:\n -> "):
    input(mensaje)

def CompraBoletos():
    '''Ingresa los datos del comprador como ID, Nombre y Cantidad de dinero ingresado, 
    si el dinero es suficiente para un boleto lo compra.
    Aun asi se le pide la cantidad de boletos que quiere comprar y verifica si cumple con la cantidad de dinero requerida'''
    pass

def EscogerNumeros():
    print("Escriba los numeros que deseas en tu boleta, recuerda que solo debes escribir un numero del 1-49:")
    Nume1 = int(input("Primer Numero: "))
    Nume2 = int(input("Segundo Numero: "))
    Nume3 = int(input("Tercer Numero: "))
    Nume4 = int(input("Cuarto Numero: "))
    Nume5 = int(input("Quinto Numero: "))
    Nume6 = int(input("Sexto Numero: "))
'''Hay que tener en cuaenta de que un usuario puede escribir los mismos numeros que otro, por ello hay que verificar que no se repitan'''

def verificarNum():
    '''Verifica si los numeros ingresados por el usuario no estan repetidos con ningun otro boleto'''
    pass

def VerHistorial():
    '''Ve el historial de las compras del usuario, con datos como el numero de sus boletos comprados
    y cuales de esos numeros eran iguales al numero ganador'''
    pass

def VerificarGanador():
    '''Verifica la cantidad de numeros que sean iguales al numero ganador y
    da el premio segun la cantidad de numeros que concuerdan, guardando el analisis en el historial del usuario'''
    pass

def Random():
    Num1 = random.randint(1, 49)
    Num2 = random.randint(1, 49)
    Num3 = random.randint(1, 49)
    Num4 = random.randint(1, 49)
    Num5 = random.randint(1, 49)
    Num6 = random.randint(1, 49)
    print("La boleta ganadora es:")
    print(f'-{Num1}---{Num2}---{Num3}---{Num4}---{Num5}---{Num6}-')

menu = """
--------------------------------------------------------
| ██╗░░░░░░█████╗░████████╗███████╗██████╗░██╗░█████╗░ |
| ██║░░░░░██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║██╔══██╗ |
| ██║░░░░░██║░░██║░░░██║░░░█████╗░░██████╔╝██║███████║ |
| ██║░░░░░██║░░██║░░░██║░░░██╔══╝░░██╔══██╗██║██╔══██║ |
| ███████╗╚█████╔╝░░░██║░░░███████╗██║░░██║██║██║░░██║ |
| ╚══════╝░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝╚═╝░░╚═╝ |
|______________________________________________________| 
|            |1. Compra de la boleta  |                |
|            |2. Hacer sorteo         |                |
|            |3. Historial de sorteos |                |
|            |4. Salir                |                |
--------------------------------------------------------
"""

while True:
    limpiarconsola()
    print(menu)
    opcion = input("Digite la opcion que necesite:\n -> ")
    if opcion == "1":
        ENTERContinuar()
    elif opcion == "2":
        ENTERContinuar()
    elif opcion == "3":
        ENTERContinuar()
    elif opcion == "4":
        print("Estas saliendo del programa....")
        print("Has salido correctamente")
        break
    else:
        print("\n¡SELECCIONE UNA OPCION CORRECTA!")
        ENTERContinuar()