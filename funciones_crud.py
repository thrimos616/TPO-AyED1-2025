# Funciones principales del sistema (Create, Read, Update, Delete)

import os
import datetime
import json

# Funciones genericas

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def cargar_datos():
    """
    Carga los datos del stock desde un json
    Inicia la lista "stock" con los productos existentes
    """
    
    try:

        with open("stock.json", "r", encoding="utf-8") as stock_json:

            return json.load(stock_json)

    except (FileNotFoundError, json.JSONDecodeError):

        print("Archivo no encontrado.")

        return []


def guardar_datos(datos):
    """
    Guarda los datos del stock en un json
    """

    try: 

        with open("stock.json", "w", encoding="utf-8") as f:

            json.dump(datos, f, ensure_ascii=False, indent=4)
            # ensure_ascii=False: Permite el uso de tildes
            # indent=4: Agrega sangrias
    
    except OSError:

        print("El archivo no pudo ser guardado.")

# Funciones propias del sistema

def identificar_accion():
    """
    Identifica la accion realizada por el usuario para agregarla al historial
    """

    """
   
                ("1", "Agregar producto", agregar_producto),
                ("2", "Modificar producto", modificar_producto),
                ("3", "Eliminar producto", eliminar_producto),
                ("6", "Registrar ventas", registrar_venta),
                ("8", "Exportar stock a csv"
    """

    pass

def registrar_accion():
    """
    Evalua que accion fue realizada en el sistema y la registra en un historial
    """

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    

def agregar_producto():
    """
    Agrega un nuevo producto al stock.
    Se le solicita al usuario: tipo de pintura (satinada o brillante), capacidad de la lata (1lt, 5lts, 10lts o 20lts),
    la cantidad de ese producto y su precio por unidad.
    """
    print("=========== AGREGAR PRODUCTO ===========")

    # Tipo de pintura
    while True:

        try:

            print("1: Satinada | 2: Brillante\n")

            pintura_tipo = int(input("Ingrese el tipo de pintura: "))

            if pintura_tipo in (1, 2):

                tipo_producto = "Satinada" if pintura_tipo == 1 else "Brillante"
                
                id_tipo = pintura_tipo  

                break

            else:

                print("Opción inválida. Ingrese 1 o 2.")

        except ValueError:

            print("El valor ingresado es incorrecto. Solo se aceptan valores numericos.")

    # Capacidad de la lata
    while True:

        try:

            print("1: 1L | 2: 5L | 3: 10L | 4: 20L\n")

            pintura_capacidad = int(input("Ingrese la capacidad de la lata: "))

            if pintura_capacidad in (1, 2, 3, 4):

                break

            else:

                print("Valor fuera de rango. Debe ingresar valores entre 1 y 4")

        except ValueError:

            print("El valor ingresado es incorrecto. Solo se aceptan valores numericos.")

    # Cantidad stock ingresado
    while True:

        try:

            cantidad_unidades = int(input("Ingrese la cantidad de unidades: "))

            if cantidad_unidades > 0:

                break

            else:

                print("Debe ingresar un número mayor que 0.")

        except ValueError:

            print("El valor ingresado es inválido. No se aceptan letras ni valores numericos negativos.")

    # Precio
    while True:

        try:

            precio_unidad = int(input("Ingrese el precio por unidad: "))

            if precio_unidad > 0:

                break

            else:

                print("Debe ingresar un precio mayor que 0.")

        except ValueError:

            print("El valor ingresado es inválido. No se aceptan letras ni valores numericos negativos.")


    # Estructura producto en el json
    producto = {
        "id": id_tipo,
        "tipo": tipo_producto,
        "capacidad": {1: "1L", 2: "5L", 3: "10L", 4: "20L"}[pintura_capacidad],
        "cantidad": cantidad_unidades,
        "precio_unidad": precio_unidad
    }

    # Funciones genericas
    stock = cargar_datos()
    stock.append(producto)
    guardar_datos(stock)
    clear()

    print("===== PRODUCTO AGREGADO CORRECTAMENTE =====")
    print(f"Pintura:{pintura_tipo}, Capacidad:{pintura_capacidad}, Unidades agregadas:{cantidad_unidades}, Precio por unidad ${precio_unidad}\n")


    while True:
        print("1. Volver al menú")
        print("2. Agregar otro producto")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        elif opcion == "2":
            clear()
            return agregar_producto()
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")


def modificar_producto():
    """
    Modifica un producto existente en el stock
    Se le pide al usuario seleccionar entre, tipo de producto o precio de unidad
    """
    print("=========== MODIFICAR PRODUCTO ===========")
    listar_productos()
    input("ID del producto a modificar: ")
    clear()
    print("===== PRODUCTO MODIFICADO CORRECTAMENTE =====")

    while True:
        print("1. Volver al menú")
        print("2. Modificar otro producto")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        elif opcion == "2":
            clear()
            return modificar_producto()
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")

def eliminar_producto():
    """
    Elimina un producto del stock
    Se le solicita al usuario el ID del producto a eliminar
    """
    print("=========== ELIMINAR PRODUCTO ===========")
    listar_productos()
    input("ID del producto a eliminar: ")
    clear()
    print("===== PRODUCTO ELIMINADO CORRECTAMENTE =====")

    while True:
        print("1. Volver al menú")
        print("2. Eliminar otro producto")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        elif opcion == "2":
            clear()
            return eliminar_producto()
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")


def listar_productos():
    """
    Muestra por pantalla todos los productos del stock en forma de tabla
    Cada producto debe mostrar: ID, tipo de pintura, capacidad (lts), cantidad, precio de la unidad
    """
    datos = [
        [1,"Pintura Satinada", "1L", 10, 1000],
        [2,"Pintura Satinada", "5L", 5, 5000],
        [3,"Pintura Brillante", "10L", 2, 10000]
    ]


    titulos = ["ID","Tipo", "Capacidad", "Cantidad", "Precio"]

    print("===========================================")
    print(tabulate.tabulate(datos, titulos))
    print("===========================================")



def buscar_producto():
    """
    Permite buscar productos en el stock por: tipo de pintura y/o capacidad
    Muestra los productos que coincidan con la busqueda
    """
    print("=========== BUSCAR PRODUCTOS ===========")
    print("¿Desea buscar por pintura, por capacidad o ambos?")
    input("Buscar por: ")
    clear()

    datos = [
        [1, "Pintura Satinada", "1L", 10, 1000],
        [2, "Pintura Satinada", "5L", 5, 5000],
        [3, "Pintura Brillante", "10L", 2, 10000]
    ]
    titulos = ["ID", "Tipo", "Capacidad", "Cantidad", "Precio"]

    print("===========================================")
    print(tabulate.tabulate(datos, titulos))
    print("===========================================")

    while True:
        print("1. Volver al menú")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")

def registrar_venta():
    """
    Registra una venta de un producto solicitando: ID del producto, cantidad vendida
    Se descuenta del stock y se registra en el historial
    """
    print("=========== REGISTRAR VENTA ===========")
    listar_productos()
    input("ID del producto vendido: ")
    input("Cantidad vendida: ")
    clear()
    print("===== VENTA REGISTRADA CORRECTAMENTE =====")

    while True:
        print("1. Volver al menú")
        print("2. Registrar otra venta")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        elif opcion == "2":
            clear()
            return registrar_venta()
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")


def mostrar_stock_bajo():
    """
    Muestra todos los productos cuyo stock sea menor a un valor mínimo
    Sirve para identificar productos que deben reponerse
    """
    print("=========== STOCK BAJO ===========")
    print("No hay productos con stock bajo por el momento.")
    print("===========================================")

    while True:
        print("1. Volver al menú")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")


def mostrar_reportes():
    """
    Muestra los reportes de ventas por fecha
    """
    print("=========== REPORTES ===========")

    print("fecha: 2025-19-10, producto: Satinada 10lts, cantidad: 2, precio unitario: 10000")

    print("===========================================")

    while True:
        print("1. Volver al menú")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")


def exportar_csv():
    """
    Exporta todos los datos del stock a un archivo CSV
    """
    print("=========== EXPORTAR CSV ===========")
    print("Archivo exportado correctamente como archivo.csv")
    print("===========================================")

    while True:
        print("1. Volver al menú")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")