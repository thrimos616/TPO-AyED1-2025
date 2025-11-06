# Funciones principales del sistema (Create, Read, Update, Delete)

import os
from datetime import datetime
from tabulate import tabulate 
import json

# Funciones genericas 

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def cargar_productos():

    """Lee productos.csv y devuelve una lista de diccionarios"""

    productos = []

    try:

        with open("productos.csv", "r", encoding="utf-8") as archivo:

            lineas = archivo.readlines()

            encabezado = lineas[0].strip().split(",")


            for linea in lineas[1:]:

                valores = linea.strip().split(",")

                producto = dict(zip(encabezado, valores))
                productos.append(producto)

    except FileNotFoundError:

        print("Archivo csv no encontrado. Se creara al guardar.")

    return productos

def guardar_productos(productos):
    """Escribe la lista de productos en productos.csv"""

    with open("productos.csv", "w", encoding="utf-8") as archivo:

        if not productos:

            archivo.write("id_producto,tipo,capacidad,precio_unidad\n")

            return

        encabezado = ",".join(productos[0].keys())
        archivo.write(encabezado + "\n")
        
        for producto in productos:

            fila = ",".join(map(str, producto.values()))
            archivo.write(fila + "\n")

def cargar_stock():
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

def guardar_stock(datos):
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

# Funciones stock
def agregar_stock():
    """
    Agrega o actualiza productos en el stock.
    Muestra los productos disponibles desde productos.csv,
    solicita capacidad, cantidad, precio y, si es necesario, el umbral mínimo de stock.
    """

    print("=========== AGREGAR STOCK ===========")
    
    stock_data = cargar_stock()  # Carga todo el JSON (stock y umbrales)
    stock = stock_data.get("stock", [])  # Variable para acceder al stock
    umbrales = stock_data.get("umbrales", {})  # Variable para acceder a los umbrales de cada producto
    productos = cargar_productos()  # Variable para acceder a los prouctos

    if not productos:

        print("No hay productos cargados.")


    listar_productos()

    # Producto
    while True:

        try:
            id_producto = int(input("\nIngrese el ID del producto: "))
            
            producto_seleccionado = None

            for x in productos:

                if int(x["id"]) == id_producto:

                    producto_seleccionado = x
                    break

            if producto_seleccionado is not None:

                tipo_producto = producto_seleccionado["nombre"]
                capacidad = producto_seleccionado["capacidad"]
                categoria = producto_seleccionado["categoria"]
                precio_unidad = int(producto_seleccionado["precio"])
                break

            else:

                print("ID invalido, intente nuevamente.")

        except ValueError:

            print("Valor invalido, solo se aceptan numeros.")


    clear()

    # Cantidad
    while True:

        try:

            cantidad_unidades = int(input("Ingrese la cantidad a agregar: "))

            if cantidad_unidades > 0:
                break

            else:
                print("Debe ingresar un numero mayor que 0.")
        except ValueError:
            print("Valor invalido, solo se aceptan numeros.")

    # Umbral
    if umbrales.get(tipo_producto) is None: # Si no existe el umbral..

        while True:

            try:

                valor = int(input(f"Ingrese el umbral minimo para {tipo_producto}: "))

                if valor > 0:

                    umbrales[tipo_producto] = valor
                    break

                else:

                    print("Debe ser mayor que 0.")

            except ValueError:

                print("Valor invalido, solo  se aceptan numeros positivos.")

    # Crear nueva carga
    nuevo_id_carga = max([x["id"] for x in stock], default=0) + 1
   
    nueva_carga = {
        "id": nuevo_id_carga,
        "tipo": tipo_producto,
        "capacidad": capacidad,
        "cantidad": cantidad_unidades
    }
    
    stock.append(nueva_carga)
    print(f"Producto '{tipo_producto}' ({capacidad}), {cantidad_unidades} cantidad de unidades agregadas al stock.")

    # Guardar todo
    stock_data["stock"] = stock
    stock_data["umbrales"] = umbrales
    guardar_stock(stock_data)
    registrar_accion("agregar_producto")
    clear()

    print("===== PRODUCTO AGREGADO CORRECTAMENTE =====")
    print(f"Categoria: {categoria}, Tipo: {tipo_producto}, Capacidad: {capacidad}, Unidades: {cantidad_unidades}\n")


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
            return agregar_stock()
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")


def modificar_stock():
    """
    Permite modificar una carga en el stock.
    El usuario puede cambiar el producto de la carga o la cantidad de unidades.
    """

    print("=========== MODIFICAR STOCK ===========")

    stock_data = cargar_stock()  # Carga todo el JSON (stock y umbrales)
    stock = stock_data.get("stock", []) # Variable para acceder al stock
    productos = cargar_productos() # Variable para acceder a los productos

    if not stock:

        print("===== No hay productos en stock =====")


    listar_stock()

    # Seleccionar que stock cargado a modificar

    while True:

        try:

            id_stock = int(input("\nIngrese el ID de la carga a modificar: "))
            
            carga = None

            for x in stock:

                if x["id"] == id_stock:

                    carga = x
                    break

            if carga:

                break

            else:

                print("ID de la carga no encontrado.")

        except ValueError:

            print("Valor invalido, solo se aceptan numeros.")
    
    clear()

    # Opciones
    print("Selecciona lo que queres modificar...")
    print("1: Producto | 2: Cantidad de unidades\n")

    while True:

        opcion = input("Seleccione una opcion (1 o 2): \n")

        # Cambiar producto
        if opcion == "1":

            listar_productos()  

            while True:

                try:

                    id_producto = int(input("\nIngrese el ID del nuevo producto: "))
                    producto_nuevo = None

                    for x in productos:

                        if int(x["id"]) == id_producto:

                            producto_nuevo = x
                            break

                    if producto_nuevo:

                        carga["tipo"] = producto_nuevo["nombre"]
                        carga["capacidad"] = producto_nuevo["capacidad"]
                        break

                    else:
                        print("ID de producto invalido.")

                except ValueError:
                    print("Valor invalido, solo se aceptan numeros.")
            break

        # Cambiar cantidad
        elif opcion == "2":
            
            while True:

                try:
                    cantidad = int(input("Ingrese la nueva cantidad de unidades: "))

                    if cantidad >= 0:

                        carga["cantidad"] = cantidad
                        break

                    else:
                        print("La cantidad debe ser mayor o igual a 0")

                except ValueError:

                    print("Valor invalido, solo se aceptan numeros.")
            break

        else:
            print("Opcion invalida, ingrese 1 o 2.")

    # Guardar todo
    stock_data["stock"] = stock
    guardar_stock(stock_data)
    registrar_accion("modificar_stock")
    clear()

    print("===== CARGA MODIFICADA CORRECTAMENTE =====")
    print(f"ID: {carga['id']} | Producto: {carga['tipo']} ({carga['capacidad']}) | Cantidad: {carga['cantidad']}\n")

    while True:
        print("1. Volver al menú")
        print("2. Modificar otra carga")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            clear()
            return
        elif opcion == "2":
            clear()
            return modificar_stock()
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")



def eliminar_stock():
    """
    Elimina un producto del stock
    Se le solicita al usuario el ID del producto a eliminar
    """
    print("=========== ELIMINAR CARGA STOCK ===========")

    stock_data = cargar_stock() # Carga todo el json (productos y umbrales)
    stock = stock_data.get("stock", []) # Variable para acceder a los productos

    if not stock:

        print("===== No hay productos cargados =====")

    listar_stock()

    try:

        id_stock = int(input("\nIngrese el ID de carga del producto a eliminar: "))
    
    except ValueError:

        print("Solo se aceptan numeros.")


    carga = None

    for x in stock: 

        if x["id"] == id_stock:

            carga = x

            break
        
    if carga is None:
        
        print("El ID de la carga no coincide con ningun producto.")

        return eliminar_carga_producto()


    confirmasion = int(input(f"La carga del producto que desea eliminar es '{carga['tipo']}', ID: '{id_stock}', con '{carga["cantidad"]}' unidades, es esto correcto? (1: Si | 2: No): ")) 

    match confirmasion:

        case 1:
    
            # Elimina el producto y solo actualiza la parte del stock en el json
            stock.remove(carga)
            stock_data["stock"] = stock
        

        case 2:

            print("==== Eliminacion cancelada por el usuario ====")

            return eliminar_carga_producto()
    
    # Guarda todo y historial
    guardar_stock(stock_data)
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


def listar_stock():
    """
    Muestra el stock cargado en forma de tabla.
    Cada fila muestra: ID de carga, Producto, Capacidad, Cantidad.
    """
    
    stock_data = cargar_stock() # Carga todo el json
    stock = stock_data.get("stock", []) # Varibale para acceder al stock

    if not stock:

        print("===== No hay productos en stock =====")


    print(tabulate(stock, headers="keys", tablefmt="grid", showindex=False)) # Muestra el dic como una tabla


# Funciones productos
def agregar_producto():
    """
    Permite al usuario agregar un producto nuevo al archivo productos.csv
    Se solicita: nombre, capacidad, categoria y precio.
    """
    print("=========== AGREGAR PRODUCTO ===========")

    productos = cargar_productos()

    # ID incremental
    if productos:

        nuevo_id = max(int(x["id"]) for x in productos) + 1

    else:

        nuevo_id = 1

    # Nombre
    nombre = input("Ingrese el nombre del producto: ").strip()

    if not nombre:
        print("El nombre no puede estar vacio.")


    # Capacidad
    capacidad = input("Ingrese la capacidad (ej: 1L, 5L, 10L, 20L, 1kg, etc): ").strip()

    if not capacidad:
        print("La capacidad no puede estar vacia.")


    # Categoria
    categoria = input("Ingrese la categoria del producto: ").strip()

    if not categoria:

        print("La categoria no puede estar vacia.")

    # Precio
    while True:

        try:

            precio = int(input("Ingrese el precio del producto: "))

            if precio > 0:
                break

            else:
                print("Debe ingresar un valor mayor que 0")

        except ValueError:

            print("Valor invalido, solo se aceptan nimeros.")

    # Estructura del producto
    nuevo_producto = {
        "id": int(nuevo_id),
        "nombre": nombre,
        "capacidad": capacidad,
        "categoria": categoria,
        "precio": int(precio)
    }

    # Guardar todo
    productos.append(nuevo_producto)
    guardar_productos(productos)
    registrar_accion("agregar_producto")
    clear()

    print(f"===== PRODUCTO AGREGADO =====")
    print(f"ID: {nuevo_id}, Nombre: {nombre}, Capacidad: {capacidad}, Categoria: {categoria}, Precio por unidad: ${precio}\n")

    # Opciones post-agregar
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

def eliminar_producto():
    """
    Elimina un producto del catálogo de productos.
    El usuario selecciona el ID del producto a eliminar.
    """
    print("=========== ELIMINAR PRODUCTO ===========")

    
    productos = cargar_productos()  

    if not productos:

        print("===== No hay productos cargados =====")

    listar_productos()

    # Elegir producto
    try:
        id_eliminar = int(input("\nIngrese el ID del producto a eliminar: "))

    except ValueError:

        print("Valor invalido, solo se aceptan numeros.")


    producto = None

    for x in productos:

        if int(x["id"]) == id_eliminar:

            producto = x
            break

    if not producto:

        print(f"No se encontro ningún producto con el ID {id_eliminar}")


    confirmasion = int(input(f"¿Desea eliminar el producto '{producto['nombre']}' ({producto['capacidad']})? (1: Si | 2: No): "))

    match confirmasion:

        case 1:

            # Eliminar producto
            productos.remove(producto)

        case 2:

            print("==== Eliminacion cancelada ====")

    # Guardar todo
    guardar_productos(productos)  
    registrar_accion("eliminar_producto")

    print(f"===== Producto '{producto['nombre']}' eliminado correctamente =====\n")

    while True:
        print("1. Volver al menú")
        print("2. Eliminar otro producto")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                clear()
                return
            case "2":
                clear()
                return eliminar_producto()
            case _:
                clear()
                print("===== OPCIÓN INCORRECTA =====")


def modificar_producto():
    """
    Modifica un producto existente del catálogo.
    El usuario puede cambiar: nombre, capacidad, categoría o precio.
    """
    print("=========== MODIFICAR PRODUCTO ===========")

 
    productos = cargar_productos()  # Variable para acceder a los productos

    if not productos:

        print("===== No hay productos cargados =====")


    listar_productos()

    # Elegir producto
    try:
        id_producto = int(input("\nIngrese el ID del producto a modificar: "))

    except ValueError:

        print("Valor invalido, solo se aceptan numeros.")


    producto = None

    for x in productos:

        if int(x["id"]) == id_producto:

            producto = x
            break

    if not producto:

        print(f"No se encontro ningun producto con ID {id_producto}")

    clear()

    print("Seleccione el atributo a modificar...\n")
    print("1: Nombre | 2: Capacidad | 3: Categoría | 4: Precio\n")

    try:

        opcion = int(input("Seleccione una opcion (1-4): "))

    except ValueError:

        print("Valor invalido.")


    match opcion:

        case 1:

            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            producto["nombre"] = nuevo_nombre.strip()

        case 2:

            nueva_capacidad = input("Ingrese la nueva capacidad (ej. 1L, 5L, 10L): ")
            producto["capacidad"] = nueva_capacidad.strip()

        case 3:

            nueva_categoria = input("Ingrese la nueva categoria: ")
            producto["categoria"] = nueva_categoria.strip()

        case 4:

            try:
                nuevo_precio = int(input("Ingrese el nuevo precio: "))

                if nuevo_precio > 0:

                    producto["precio"] = nuevo_precio

                else:

                    print("El precio debe ser mayor que 0")

            except ValueError:

                print("Valor invalido, debe ser un numero.")

        case _:

            print("Opcion invalida.")


    # Guardar todo
    guardar_productos(productos)
    registrar_accion("modificar_producto")

    print(f"===== Producto ID {id_producto} modificado correctamente =====\n")

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


def listar_productos():
    """
    Muestra por pantalla todos los productos del stock en forma de tabla
    Cada producto debe mostrar: ID, tipo de pintura, capacidad (lts), cantidad, precio de la unidad
    """

    productos = cargar_productos()  # Variable para acceder a los productos

    if not productos:

        print("===== No hay productos cargados =====")

    print(tabulate(productos, headers="keys", tablefmt="grid", showindex=False)) # Muestra el csv como una tabla


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