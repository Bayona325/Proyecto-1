from colorama import Fore, init, Style
import os
import json
import random
from tabulate import tabulate

init(autoreset=True)

class ManejadorArchivos:
    @staticmethod
    def cargar_boletos_activos():
        try:
            with open('boletos_activos.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def guardar_boletos_activos(boletos):
        with open('boletos_activos.json', 'w') as file:
            json.dump(boletos, file, indent=4)

    @staticmethod
    def cargar_historial():
        try:
            with open('historial.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def agregar_al_historial(registro):
        historial = ManejadorArchivos.cargar_historial()
        historial.append(registro)
        with open('historial.json', 'w') as file:
            json.dump(historial, file, indent=4)

    @staticmethod
    def formatear_archivos():
        # Asegurar formato consistente en todos los archivos
        boletos = ManejadorArchivos.cargar_boletos_activos()
        ManejadorArchivos.guardar_boletos_activos(boletos)
        
        historial = ManejadorArchivos.cargar_historial()
        with open('historial.json', 'w') as file:
            json.dump(historial, file, indent=4)

# Inicialización global
ManejadorArchivos.formatear_archivos()
boletos_activos = ManejadorArchivos.cargar_boletos_activos()

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
    global boletos_activos
    precio_boleto = 5
    nombre = input("Ingrese su nombre: ")
    id_usuario = input("Ingrese su ID: ")
    dinero = float(input("Ingrese su dinero disponible: $"))
    
    cantidad_max = int(dinero // precio_boleto)
    if cantidad_max == 0:
        print(Fore.RED + "Dinero insuficiente. Se requiere $5 por boleto.")
        return []
    
    cantidad = int(input(f"¿Cuántos boletos desea comprar? (Máximo {cantidad_max}): "))
    cantidad = min(cantidad, cantidad_max)
    
    boletos = []
    for _ in range(cantidad):
        while True:
            nuevo_boleto = EscogerNumeros()
            # Verificar contra todos los boletos existentes (activos e historial)
            if any(nuevo_boleto == b["numeros"] for b in boletos_activos + cargar_historial_completo()):
                print(Fore.RED + "¡Esta combinación ya existe! Elija números diferentes.")
            elif nuevo_boleto in [b["numeros"] for b in boletos]:
                print(Fore.RED + "¡Boleto duplicado en esta compra!")
            else:
                boletos.append({
                    "nombre": nombre,
                    "id": id_usuario,
                    "numeros": nuevo_boleto,
                    "dinero_gastado": precio_boleto
                })
                break
    return boletos

def cargar_historial_completo():
    historial = ManejadorArchivos.cargar_historial()
    return [item["boleto"] for item in historial] if historial else []

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

def MostrarHistorial():
    historial = ManejadorArchivos.cargar_historial()
    if not historial:
        print(Fore.YELLOW + "No hay historial de sorteos disponible.")
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
        headers=["Nombre", "ID", "Boleto", "Ganadores", "Aciertos", "Premio", "Participó"],
        tablefmt="grid"
    ))

def GenerarNumerosGanadores():
    return random.sample(range(1, 50), 6)    

def VerificarGanador(boleto, ganadores):
    aciertos = 0
    for i in range(6):
        if boleto[i] == ganadores[i]:
            aciertos += 1
    premios = {
        3: "Premio pequeño",
        4: "Premio mediano",
        5: "Premio grande",
        6: "Premio mayor"
    }
    return aciertos, premios.get(aciertos, "No ganó")

def SimularSorteos():
    global boletos_activos
    
    # Mostrar usuarios con boletos disponibles
    usuarios = {b['id']: b['nombre'] for b in boletos_activos}
    if not usuarios:
        print(Fore.RED + "No hay boletos comprados para simular.")
        return None
    
    print(Fore.CYAN + "\nUsuarios disponibles:")
    for id_usuario, nombre in usuarios.items():
        print(f"ID: {id_usuario} - Nombre: {nombre}")
    
    # Seleccionar usuario
    id_usuario = input("\nIngrese el ID del usuario: ")
    boletos_usuario = [b for b in boletos_activos if b['id'] == id_usuario]
    
    if not boletos_usuario:
        print(Fore.RED + "No se encontraron boletos para este usuario.")
        return None
    
    # Mostrar boletos del usuario
    print(Fore.CYAN + "\nBoletos disponibles para simulación:")
    for i, boleto in enumerate(boletos_usuario, 1):
        print(f"{i}. Números: {boleto['numeros']}")
    
    # Seleccionar boleto
    try:
        seleccion = int(input("\nSeleccione el número de boleto a simular: ")) - 1
        boleto_seleccionado = boletos_usuario[seleccion]
    except (ValueError, IndexError):
        print(Fore.RED + "Selección inválida.")
        return None
    
    # Cantidad de simulaciones
    try:
        cantidad = int(input("Ingrese la cantidad de simulaciones: "))
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        print(Fore.RED + "Debe ingresar un número positivo.")
        return None
    
    # Realizar simulaciones
    estadisticas = {i: 0 for i in range(7)}  # Contador de aciertos (0-6)
    numeros_boleto = boleto_seleccionado['numeros']
    
    print(Fore.CYAN + f"\nSimulando {cantidad} sorteos para el boleto: {numeros_boleto}")
    
    for _ in range(cantidad):
        ganadores = GenerarNumerosGanadores()
        aciertos = len(set(numeros_boleto) & set(ganadores))
        estadisticas[aciertos] += 1
    
    return estadisticas

def RealizarSorteo(boletos):
    global boletos_activos
    ganadores = GenerarNumerosGanadores()
    print(Fore.CYAN + "\nNúmeros ganadores:", ganadores)
    
    for boleto in boletos:
        # Agregar campo 'participado' al boleto
        boleto['participado'] = True
        resultado = VerificarGanador(boleto["numeros"], ganadores)
        ManejadorArchivos.agregar_al_historial({
            "boleto": boleto,
            "ganadores": ganadores,
            "resultado": resultado
        })
        
        if resultado[0] >= 3:
            print(Fore.GREEN + f"\n¡Boleto ganador!")
            print(f"Dueño: {boleto['nombre']} (ID: {boleto['id']})")
            print(f"Números: {boleto['numeros']}")
            print(f"Aciertos: {resultado[0]} - {resultado[1]}")
    
    # Actualizar boletos activos (marcando participación pero sin eliminarlos)
    ManejadorArchivos.guardar_boletos_activos(boletos_activos)
    print(Fore.GREEN + "\n¡Sorteo completado! Los boletos siguen disponibles para consulta.")

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
        nuevos_boletos = CompraBoletos()
        if nuevos_boletos:
            boletos_activos.extend(nuevos_boletos)
            ManejadorArchivos.guardar_boletos_activos(boletos_activos)
            print(Fore.GREEN + "Boletos comprados exitosamente.")
        ENTERContinuar()
    
    elif opcion == "2":
        if not boletos_activos:
            print(Fore.YELLOW + "No hay boletos comprados.")
        else:
            tabla = []
            for b in boletos_activos:
                estado = "Participó" if b.get("participado", False) else "Disponible"
                tabla.append([b["nombre"], b["id"], b["numeros"], estado])
            
            print(tabulate(
                tabla,
                headers=["Nombre", "ID", "Números", "Estado"],
                tablefmt="grid"
            ))
        ENTERContinuar()
    
    elif opcion == "3":
        if not boletos_activos:
            print(Fore.RED + "No hay boletos para sortear.")
        else:
            RealizarSorteo(boletos_activos)
        ENTERContinuar()
    
    elif opcion == "4":
        MostrarHistorial()
        ENTERContinuar()
    
    elif opcion == "5":
        estadisticas = SimularSorteos()
        if estadisticas is not None:
            MostrarEstadisticas(estadisticas)
        ENTERContinuar()
    
    elif opcion == "6":
        # Guardar los boletos activos antes de salir usando ManejadorArchivos
        ManejadorArchivos.guardar_boletos_activos(boletos_activos)
        print("Saliendo del programa...")
        break
    
    else:
        print(Fore.RED + Style.BRIGHT + "\n¡SELECCIONE UNA OPCIÓN CORRECTA!")
        ENTERContinuar()
        
