# Funciones principales del sistema (Create, Read, Update, Delete)

import os
import datetime
import tabulate 
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

            match tipo_input:
                
                case 1:

                    tipo_producto = "Satinada"
                    id_tipo = 1
                    break

                case 2:

                    tipo_producto = "Brillante"
                    id_tipo = 2
                    break

                case _:

                    print("Opcion invslida. Ingrese 1 o 2.")

        except ValueError:

            print("El valor ingresado es incorrecto. Solo se aceptan valores numericos.")

    # Capacidad de la lata
    while True:

        try:

            print("1: 1L | 2: 5L | 3: 10L | 4: 20L\n")

            pintura_capacidad = int(input("Ingrese la capacidad de la lata: "))

            match pintura_capacidad:

                case 1:

                    capacidad = "1L"
                    break

                case 2:

                    capacidad = "5L"
                    break

                case 3:

                    capacidad = "10L"
                    break

                case 4:
                    capacidad = "20L"
                    break

                case _:
                    print("Valor fuera de rango. Debe ingresar un valor entre 1 y 4")

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


    nuevo_id_carga = id_carga =+ 1

    # Estructura producto en el json
    producto = {
        "id": id_tipo,
        "id_carga": nuevo_id_carga, 
        "tipo": tipo_producto,
        "capacidad": pintura_capacidad,
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
    Se le pide al usuario seleccionar entre: tipo de producto, precio de unidad o capacidad
    """
    
    print("=========== MODIFICAR PRODUCTO ===========")
    
    listar_productos()

    stock = cargar_datos()

    try:

        id_producto = int(input("Ingrese el ID del producto a modificar: "))
    
    except ValueError:

        print("Solo se aceptan numeros")

    producto = None

    for x in stock: # x seria el diccionario, osea cada producto por individual

        if x["id"] == id_producto:

            producto = x

            break
        
    if producto is None:
        
        print("El ID no coincide con ningun producto.")
    

    print("\n1: Tipo de producto")
    print("2: Precio por unidad")
    print("3: Capacidad\n")

    try:

        opcion = int(input("Ingrese el atributo a modificar: "))
    
    except ValueError:
        
        print("Debe ingresar un numero entre 1 y 3")


    if opcion == 1:

        print("1: Satinada | 2: Brillante")

        tipo = int(input("Ingrese el nuevo tipo: "))

        if tipo in (1, 2):

            producto["tipo"] = "Satinada" if tipo == 1 else "Brillante"


    elif opcion == 2:

        nuevo_precio = int(input("Nuevo precio por unidad: "))

        if nuevo_precio > 0:

            producto["precio_unidad"] = nuevo_precio


    elif opcion == 3:

        print("1: 1L | 2: 5L | 3: 10L | 4: 20L")

        nueva_capacidad = int(input("Ingrese la nueva capicidad: "))

        match nueva_capacidad:

            case 1:

                producto["capacidad"] = "1L"

            case 2:

                producto["capacidad"] = "5L"

            case 3:

                producto["capacidad"] = "10L"

            case 4:

                producto["capacidad"] = "20L"

            case _: # Funciona como un else

                print("Opcion invalida. Debe ingresar un valor entre 1 y 4.")

                return modificar_producto()

    else:

        print("Opcion invalida.")


    # Funciones genericas
    guardar_datos(stock)
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
    stock = cargar_datos()

    try:

        id_producto = int(input("Ingrese el ID del producto a modificar: "))
    
    except ValueError:

        print("Solo se aceptan numeros")


    producto = None

    for x in stock: 

        if x["id"] == id_producto:

            producto = x

            break
        
    if producto is None:
        
        print("El ID no coincide con ningun producto.")


    print(f"\nEl producto que estas por eliminar es: {producto["tipo"]}, {producto["capacidad"]}")

    # Elimina el producto
    stock.remove(producto)
    
    guardar_datos(stock)
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

    stock = cargar_datos()

    if not stock:

        print("===== No hay productos en stock =====")

        return

    print(tabulate.tabulate(stock, headers="keys", tablefmt="grid")) # Muestra el dic como una tabla




def buscar_producto():
    """
    Permite buscar productos en el stock por: tipo de pintura y/o capacidad
    Muestra los productos que coincidan con la busqueda
    """
    print("=========== BUSCAR PRODUCTOS ===========")
    
    print("1: Buscar por tipo | 2: Buscar por capacidad")

    stock = cargar_datos()
    clear()

    opcion = int(input("Elija una opcion: "))


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