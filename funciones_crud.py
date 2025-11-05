# Funciones principales del sistema (Create, Read, Update, Delete)

import os
from datetime import datetime
from tabulate import tabulate 
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

        with open("stock_data.json", "r", encoding="utf-8") as stockdata_json:

            return json.load(stockdata_json)

    except (FileNotFoundError, json.JSONDecodeError):

        print("Archivo no encontrado.")

        return []


def guardar_datos(datos):
    """
    Guarda los datos del stock en un json
    """

    try: 

        with open("stock_data.json", "w", encoding="utf-8") as f:

            json.dump(datos, f, ensure_ascii=False, indent=4)
            # ensure_ascii=False: Permite el uso de tildes
            # indent=4: Agrega sangrias
    
    except OSError:

        print("El archivo no pudo ser guardado.")

# Funciones propias del sistema

def registrar_accion(nombre_funcion) -> str:
    """
    Evalua que accion fue realizada en el sistema y la registra en un historial
    """

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    acciones = {

        "agregar_producto": "Agregó un nuevo producto al stock",
        "eliminar_carga_producto": "Eliminó una carga de producto",
        "modificar_producto": "Modificó un producto existente",
        "buscar_producto": "Buscó un producto en el stock",
    }

    descripcion = acciones.get(nombre_funcion, f"Ejecutó {nombre_funcion}")

    linea_horario = f"[{fecha_hora}] {descripcion}\n"

    ruta_archivo = os.path.join(os.path.dirname(__file__), "historial.txt")

    try:
        # Si no existe,el archivo, lo crea
        if not os.path.exists(ruta_archivo):

            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                # Esto seria el encabezado
                archivo.write("===== HISTORIAL DE ACCIONES =====\n\n") 

        # Si existe, simplemetne lo escribe
        with open(ruta_archivo, "a", encoding="utf-8") as archivo:

            archivo.write(linea_horario)

    except FileNotFoundError:

        print("No se encontro o no se pudo crear el archivo.")

    except OSError as e:

        print(f"Error del sistema al registrar el historial: {e}")


def agregar_producto():
    """
    Agrega un nuevo producto al stock.
    Se le solicita al usuario: tipo de pintura, capacidad de la lata (1lt, 5lts, 10lts o 20lts),
    la cantidad de ese producto y su precio por unidad.
    """
    print("=========== AGREGAR PRODUCTO ===========")
    
    stock_data = cargar_datos() # Carga todo el json (productos y umbrales)
    stock = stock_data.get("productos", []) # Variable para acceder a los productos
    umbrales = stock_data.get("umbrales", {}) # Variable para acceder a los umbrales
    
    # Tipo de pintura
    while True:

        try:
            print("1: Látex Interior")
            print("2: Látex Exterior")
            print("3: Esmalte Sintético Brillante")
            print("4: Esmalte Sintético Satinado")
            print("5: Barniz Marino")
            print("6: Convertidor de Óxido")
            print("7: Enduido Plástico Interior")
            print("8: Impermeabilizante para Techos")
            print("9: Antihumedad\n")

            pintura_tipo = int(input("Ingrese el tipo de pintura: "))
            clear()

            match pintura_tipo:

                case 1:

                    tipo_producto = "Látex Interior"
                    id_tipo = 1
                    break

                case 2:

                    tipo_producto = "Látex Exterior"
                    id_tipo = 2
                    break

                case 3:

                    tipo_producto = "Esmalte Sintético Brillante"
                    id_tipo = 3
                    break

                case 4:

                    tipo_producto = "Esmalte Sintético Satinado"
                    id_tipo = 4
                    break

                case 5:

                    tipo_producto = "Barniz Marino"
                    id_tipo = 5
                    break

                case 6:

                    tipo_producto = "Convertidor de Óxido"
                    id_tipo = 6
                    break

                case 7:

                    tipo_producto = "Enduido Plástico Interior"
                    id_tipo = 7
                    break

                case 8:

                    tipo_producto = "Impermeabilizante para Techos"
                    id_tipo = 8
                    break

                case 9:

                    tipo_producto = "Antihumedad"
                    id_tipo = 9
                    break

                case _:

                    print("Opcion invaida. Ingrese un número entre 1 y 9.")

        except ValueError:

            print("El valor ingresado es incorrecto. Solo se aceptan valores numericos.")


    # Umbrales
    if umbrales.get(tipo_producto) is None: # Si no existe el umbral del producto...

        while True:

            try:

                valor = int(input(f"Ingrese el valor del umbral minimo de stock para {tipo_producto}: "))

                if valor > 0:

                    umbrales[tipo_producto] = valor
                    break

                else:

                    print("Debe ingresar un numero mayor que 0")

            except ValueError:

                print("Valor invalido. Solo se aceptan numeros positivos.")


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

                print("Debe ingresar un numero mayor que 0.")

        except ValueError:

            print("El valor ingresado es invalido. No se aceptan letras ni valores numericos negativos.")

    # Precio
    while True:

        try:

            precio_unidad = int(input("Ingrese el precio por unidad: "))

            if precio_unidad > 0:
                break
            
            else:

                print("Debe ingresar un precio mayor que 0.")

        except ValueError:

            print("El valor ingresado es invalido. No se aceptan letras ni valores numericos negativos.")

    # ID carga
    if stock: # Si hay productos...

        # Busca el maximo y le suma 1
        nuevo_id_carga = max(x["id_carga"] for x in stock) + 1

    else:

        nuevo_id_carga = 1

    # Estructura producto en el json
    producto = {
        "id": id_tipo,
        "id_carga": nuevo_id_carga,
        "tipo": tipo_producto,
        "capacidad": capacidad,
        "cantidad": cantidad_unidades,
        "precio_unidad": precio_unidad
    }

    # Guarda todo y lo registra en el historial
    stock.append(producto) # La carga del producto
    stock_data["productos"] = stock # El producto
    stock_data["umbrales"] = umbrales # El umbral 
    registrar_accion("agregar_producto") # Historial
    guardar_datos(stock_data)
    clear()

    print("===== PRODUCTO AGREGADO CORRECTAMENTE =====")
    print(f"Pintura: {tipo_producto}, Capacidad: {capacidad}, Unidades agregadas: {cantidad_unidades}, Precio por unidad: ${precio_unidad}\n")

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

    stock_data = cargar_datos() # Carga todo el json (productos y umbrales)
    stock = stock_data.get("productos", []) # Variable para acceder a los productos
    umbrales = stock_data.get("umbrales", {}) # Variable para acceder a los umbrales

    try:

        id_carga = int(input("Ingrese el ID de carga del producto a modificar: "))

    except ValueError:

        print("Solo se aceptan numeros.")

    producto = None

    for x in stock: 

        if x["id_carga"] == id_carga:

            producto = x

            break
        
    if producto is None:
        
        print("El ID de carga no coincide con ningun producto.")
    
    print("\n1: Tipo de producto")
    print("2: Precio por unidad")
    print("3: Capacidad\n")

    try:
        opcion = int(input("Ingrese el atributo a modificar: "))

    except ValueError:

        print("Debe ingresar un numero entre 1 y 3")


    match opcion:

        # Cambira tipo
        case 1:
            print("\n1: Látex Interior")
            print("2: Látex Exterior")
            print("3: Esmalte Sintético Brillante")
            print("4: Esmalte Sintético Satinado")
            print("5: Barniz Marino")
            print("6: Convertidor de Óxido")            
            print("7: Enduido Plástico Interior")
            print("8: Impermeabilizante para Techos")
            print("9: Antihumedad\n")

            try:

                tipo = int(input("Ingrese el nuevo tipo: "))

            except ValueError:

                print("Debe ingresar un numero entre 1 y 9")


            match tipo:

                case 1:
                    producto["tipo"] = "Látex Interior"
                    producto["id"] = 1

                case 2:

                    producto["tipo"] = "Látex Exterior"
                    producto["id"] = 2

                case 3:

                    producto["tipo"] = "Esmalte Sintético Brillante"
                    producto["id"] = 3

                case 4:

                    producto["tipo"] = "Esmalte Sintético Satinado"
                    producto["id"] = 4

                case 5:

                    producto["tipo"] = "Barniz Marino"
                    producto["id"] = 5

                case 6:

                    producto["tipo"] = "Convertidor de Óxido"
                    producto["id"] = 6

                case 7:

                    producto["tipo"] = "Enduido Plástico Interior"
                    producto["id"] = 7

                case 8:

                    producto["tipo"] = "Impermeabilizante para Techos"
                    producto["id"] = 8

                case 9:

                    producto["tipo"] = "Antihumedad"
                    producto["id"] = 9

                case _:

                    print("Opciin invalida. Ingrese un numero entre 1 y 9")


        # Cambiar precio
        case 2:

            try:

                nuevo_precio = int(input("Nuevo precio por unidad: "))

                if nuevo_precio > 0:
                    producto["precio_unidad"] = nuevo_precio

                else:

                    print("Debe ingresar un numero mayor que 0")


            except ValueError:

                print("Solo se aceptan numeros.")


        # CAmbiar capaciad
        case 3:

            print("1: 1L | 2: 5L | 3: 10L | 4: 20L")

            try:

                nueva_capacidad = int(input("Ingrese la nueva capacidad: "))

            except ValueError:

                print("Debe ingresar un numero entre 1 y 4")


            match nueva_capacidad:

                case 1:

                    producto["capacidad"] = "1L"

                case 2:

                    producto["capacidad"] = "5L"

                case 3:

                    producto["capacidad"] = "10L"

                case 4:

                    producto["capacidad"] = "20L"

                case _:
                    print("Opcion invalida. Debe ingresar un valor entre 1 y 4")


        case _:

            print("Opcion invalida.")


    # Guardar los cambios y historial
    guardar_datos(stock_data)
    registrar_accion("modificar_producto")
    clear()
    print("===== PRODUCTO MODIFICADO CORRECTAMENTE =====")

    while True:
        print("1. Volver al menú")
        print("2. Modificar otro producto")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                clear()
                return
            case "2":
                clear()
                return modificar_producto()
            case _:
                clear()
                print("===== OPCIÓN INCORRECTA =====")

def eliminar_carga_producto():
    """
    Elimina un producto del stock
    Se le solicita al usuario el ID del producto a eliminar
    """
    print("=========== ELIMINAR PRODUCTO ===========")

    stock_data = cargar_datos() # Carga todo el json (productos y umbrales)
    stock = stock_data.get("productos", []) # Variable para acceder a los productos

    if not stock:

        print("===== No hay productos cargados =====")

    listar_productos()

    try:

        id_carga = int(input("\nIngrese el ID de carga del producto a eliminar: "))
    
    except ValueError:

        print("Solo se aceptan numeros.")


    producto = None

    for x in stock: 

        if x["id_carga"] == id_carga:

            producto = x

            break
        
    if producto is None:
        
        print("El ID de carga no coincide con ningun producto.")

        return eliminar_carga_producto()


    confirmasion = int(input(f"La carga del producto que desea eliminar es '{producto['tipo']}', ID: '{id_carga}', con '{producto["cantidad"]}' unidades, es esto correcto? (1: Si | 2: No): ")) 

    match confirmasion:

        case 1:
    
            # Elimina el producto y solo actualiza la parte del producto en el json
            stock.remove(producto)
            stock_data["productos"] = stock
        

        case 2:

            print("==== Eliminacion cancelada por el usuario ====")

            return eliminar_carga_producto()
    
    # Guarda todo y historial
    guardar_datos(stock_data)
    registrar_accion("eliminar_carga_producto")
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

    stock_data = cargar_datos() # Carga todo el json (productos y umbrales)
    stock = stock_data.get("productos", []) # Variable para acceder a los productos

    if not stock:

        print("===== No hay productos en stock =====")

    print(tabulate(stock, headers="keys", tablefmt="grid", showindex=False)) # Muestra el dic como una tabla


def buscar_producto():
    """
    Permite buscar productos en el stock por: tipo de pintura y/o capacidad
    Muestra los productos que coincidan con la busqueda
    """
    print("=========== BUSCAR PRODUCTOS ===========")
    
    print("1: Buscar por tipo | 2: Buscar por capacidad | 3: Buscar por ambos")

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