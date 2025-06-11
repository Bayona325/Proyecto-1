from colorama import Fore, init, Style
import os
import json
import random
from tabulate import tabulate

init(autoreset=True)

class ManejadorDeArchivos:
    @staticmethod
    def CargarboletosActivos():
        try:
            with open('boletosActivos.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def GuardarboletosActivos(boletos):
            with open('boletosActivos.json', 'w') as file:
                json.dump(boletos, file, indent=4)
        
    @staticmethod
    def CargarHistorial():
        try:
            with open('historial.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    @staticmethod
    def AgregarHistorial(registro):
        historial = ManejadorDeArchivos.CargarHistorial()
        historial.append(registro)
        with open('historial.json', 'w') as file:
            json.dump(historial, file, indent=4)

    @staticmethod
    def FormatearArchivos():
        boletos = ManejadorDeArchivos.CargarboletosActivos()
        ManejadorDeArchivos.GuardarboletosActivos(boletos)

        historial = ManejadorDeArchivos.CargarHistorial()
        with open('historial.json', 'w') as file:
            json.dump(historial, file, indent=4)

ManejadorDeArchivos.FormatearArchivos()
boletosActivos = ManejadorDeArchivos.CargarboletosActivos()

def MostrarEstadisticas(estadisticas):
    tabla = []
    for aciertos, cantidad in estadisticas.items():
        tabla.append([f"{aciertos} aciertos", cantidad])
    print(tabulate(tabla, headers=["aciertos", "Veces"], tablefmt="grid"))

def limpiarconsola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def escribirConsola(texto: str, color = Fore.WHITE):
    print(f"{color}{texto}")

def ENTERContinuar(mensaje: str = Fore.CYAN + Style.BRIGHT + "\nPresione ENTER para continuar:\n -> "):
    input(mensaje)

def EscogerNumeros():
    numeros = []
    while len(numeros) < 6:
        try:
            Num = int(input(Fore.BLUE + Style.BRIGHT + f"Ingrese el número {len(numeros) + 1} (1-49): " + Style.RESET_ALL))
            if Num < 1 or Num > 49:
                print(Fore.RED + Style.BRIGHT + "El número debe estar entre 1 y 49." + Style.RESET_ALL)
            elif Num in numeros:
                print(Fore.YELLOW + Style.BRIGHT + "Número repetido. Intente de nuevo." + Style.RESET_ALL)
            else:
                numeros.append(Num)
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "¡ERROR!\nIngrese un número válido." + Style.RESET_ALL)
    return numeros

def CargarHistorialCompleto():
    historial = ManejadorDeArchivos.CargarHistorial()
    return [item["boleto"] for item in historial] if historial else []

def Compraboletos():
    global boletosActivos
    Precioboleto = 5
    nombre = input("Ingrese su nombre: ")
    id = input("Ingrese su id: ")
    Dinero = float(input("Ingrese su dinero disponible (Cada boleto cuesta $5): $"))

    CantidadMAX = int(Dinero // Precioboleto)
    if CantidadMAX == 0:
        print(Fore.RED + Style.BRIGHT + "Dinero insuficiente. Se requiere $5 por boleto.")
        return []
    
    Cantidad = int(input(f"¿Cuántos boletos desea comprar? (Maximo {CantidadMAX}): "))
    Cantidad = min(Cantidad, CantidadMAX)

    boletos = []
    for i in range(Cantidad):
        while True:
            Nuevoboleto = EscogerNumeros()
            if any(Nuevoboleto == b["numeros"] for b in boletosActivos + CargarHistorialCompleto()):
                print(Fore.RED + Style.BRIGHT + "¡Esta combinación ya existe! Escoja números diferentes.")
            elif Nuevoboleto in [b["numeros"] for b in boletos]:
                print(Fore.RED + Style.BRIGHT + "¡Este boleto ya lo compraste!")
            else:
                boletos.append({
                    "nombre": nombre,
                    "id": id,
                    "numeros": Nuevoboleto,
                    "dinero_gastado": Precioboleto
                })
                break
    return boletos

def GuardarHistorial(boleto, ganadores, resultado):
    historial = {
        "boleto": boleto,
        "ganadores": ganadores,
        "aciertos": resultado[0],
        "premio": resultado[1]
    }
    with open('historial.json', 'a') as file:
        json.dump(historial, file)
        file.write("\n")

def MostrarHistorial():
    historial = ManejadorDeArchivos.CargarHistorial()
    if not historial:
        print(Fore.YELLOW + Style.BRIGHT + "No hay historial de sorteos por el momento")
        return
    
    tabla = []
    for item in historial:
        tabla.append([
            item["boleto"]["nombre"],
            item["boleto"]["id"],
            item["boleto"]["numeros"],
            item["ganadores"],
            item["resultado"][0],
            item["resultado"][1],
            "Sí" if item["boleto"].get("participado", False) else "No"
        ])

    print(tabulate(
        tabla,
        headers=["nombre", "id", "boleto", "ganadores", "aciertos", "premio", "Participo"],
        tablefmt="grid"
    ))

def GenerarNumsGanadores():
    return random.sample(range(1, 50), 6)

def VerificarGanador(boleto, ganadores):
    aciertos = 0
    for i in range(6):
        if boleto[i] == ganadores[i]:
            aciertos += 1
    Premios = {
        3: "premio pequeño",
        4: "premio mediano",
        5: "premio grande",
        6: "premio mayor"
    }
    return aciertos, Premios.get(aciertos, "No ganó")

def SimularSorteos():
    global boletosActivos

    #Mostrar los usuarios con boletos comprados
    Usuarios = {b['id']: b['nombre'] for b in boletosActivos}
    if not Usuarios:
        print(Fore.RED + Style.BRIGHT + "No hay boletos comprados para simular")
        return None
    
    print(Fore.CYAN + Style.BRIGHT + "\nUsuarios disponibles:")
    for id, nombre in Usuarios.items():
        print(f"id: {id} - nombre: {nombre}")
    
    #Seleccion de Usuario
    id = input("\nIngrese el id del usuario: ")
    boletosUsuario = [b for b in boletosActivos if b['id'] == id]

    if not boletosUsuario:
        print(Fore.RED + Style.BRIGHT + "No se encontraron boletos para este usuario.")
        return None
    
    #Mostrar boletos del usuario
    print(Fore.CYAN + Style.BRIGHT + "\nboletos disponibles para simulación:")
    for i, boleto in enumerate(boletosUsuario, 1):
        print(f"{i}. Números: {boleto['numeros']}")

    #Seleccionar boleto
    try:
        Seleccion = int(input("\nSeleccione el número de boleto a simular: ")) - 1
        boletoSeleccionado = boletosUsuario[Seleccion]
    except (ValueError, IndexError):
        print(Fore.RED + Style.BRIGHT + "Seleccion invalida")
        return None
    
    #Cantidad de simulaciones
    try:
        Cantidad = int(input("Ingrese la cantidad de simulaciones: "))
        if Cantidad <= 0:
            raise ValueError
    except ValueError:
        print(Fore.RED + Style.BRIGHT + "Debe ingresar un numero positivo")
        return None
    
    #Realizar Simulaciones
    Estadisticas = {i: 0 for i in range(7)}    # Contador de aciertos (0-6)
    Numeroboleto = boletoSeleccionado['numeros']

    print(Fore.CYAN + Style.BRIGHT + f"\nSimulando {Cantidad} sorteos para el boleto: {Numeroboleto}")

    for i in range(Cantidad):
        ganadores = GenerarNumsGanadores()
        aciertos = len(set(Numeroboleto) & set(ganadores))
        Estadisticas[aciertos] += 1
    
    return Estadisticas

def RealizarSorteo(boletos):
    global boletosActivos
    ganadores = GenerarNumsGanadores()
    print(Fore.CYAN + Style.BRIGHT + "\nNúmeros ganadores:", ganadores)

    for boleto in boletos:
        boleto['participado'] = True
        resultado = VerificarGanador(boleto['numeros'], ganadores)
        ManejadorDeArchivos.AgregarHistorial({
            "boleto": boleto,
            "ganadores": ganadores,
            "resultado": resultado
        })

        if resultado[0] >= 3:
            print(Fore.GREEN + Style.BRIGHT + f"\n¡boleto ganador!")
            print(f"Dueño: {boleto['nombre']} (id: {boleto['id']})")
            print(F"numeros: {boleto['numeros']}")
            print(f"aciertos: {resultado[0]} - {resultado[1]}")

    ManejadorDeArchivos.GuardarboletosActivos(boletosActivos)
    print(Fore.GREEN + Style.BRIGHT + "\n¡Sorteo completado! Los boletos siguen disponibles para consulta.")

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
|            |2. boletos comprados    |                |
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
        Nuevosboletos = Compraboletos()
        if Nuevosboletos:
            boletosActivos.extend(Nuevosboletos)
            ManejadorDeArchivos.GuardarboletosActivos(boletosActivos)
            print(Fore.GREEN + Style.BRIGHT + "boletos comprados exitosamente.")
        ENTERContinuar()

    elif opcion == "2":
        if not boletosActivos:
            print(Fore.YELLOW + Style.BRIGHT + "No hay boletos comprados.")
        else:
            tabla = []
            for b in boletosActivos:
                Estado = "Participo" if b.get("participado", False) else "Disponible"
                tabla.append([b["nombre"], b["id"], b["numeros"], Estado])

            print(tabulate(
                tabla,
                headers=["nombre", "id", "numeros", "Estado"],
                tablefmt="grid"
            ))
        ENTERContinuar()

    elif opcion == "3":
        if not boletosActivos:
            print(Fore.RED + Style.BRIGHT + "No hay boletos para sortear.")
        else:
            RealizarSorteo(boletosActivos)
        ENTERContinuar()

    elif opcion == "4":
        MostrarHistorial()
        ENTERContinuar()

    elif opcion == "5":
        Estadisticas = SimularSorteos()
        if Estadisticas is not None:
            MostrarEstadisticas(Estadisticas)
        ENTERContinuar()

    elif opcion == "6":
        ManejadorDeArchivos.GuardarboletosActivos(boletosActivos)
        print("Estas saliendo del programa....")
        print("Has salido correctamente")
        break

    else:
        print("\n¡SELECCIONE UNA OPCION CORRECTA!")
        ENTERContinuar()
        
