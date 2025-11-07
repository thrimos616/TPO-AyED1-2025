# Funciones principales del sistema (Create, Read, Update, Delete)

import os
from datetime import datetime
from tabulate import tabulate 
import json

# Funciones genericas 

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def cargar_ventas():
    """Lee ventas.csv y devuelve una lista de diccionarios"""
    
    ventas = []
    
    try:
        with open("ventas.csv", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            
            if lineas:
                encabezado = lineas[0].strip().split(",")
                
                for linea in lineas[1:]:

                    if linea.strip():

                        valores = linea.strip().split(",")

                        if len(valores) == len(encabezado):

                            venta = dict(zip(encabezado, valores))
                            ventas.append(venta)
    
    except FileNotFoundError:

        print("Archivo no encontrado.")

        return ventas

    except Exception as e:

        print(f"Error al cargar ventas.csv: {e}")
    
    return ventas
   

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
            
            data = json.load(stockdata_json)
            
            return data

    except (FileNotFoundError, json.JSONDecodeError):

        print("Archivo no encontrado.")

        return {"stock": [], "umbrales": {}}

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
def agregar_stock(producto=None):
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
        input("\nENTER para volver al menú ")
        clear()
        return

    listar_productos()

    # Producto
    while True:

        try:

            if producto is None:

                id_producto = int(input("\nIngrese el ID del producto: "))

            else:

                id_producto=producto

            producto_seleccionado = None

            for x in productos:

                if int(x["id"]) == id_producto:
                    producto_seleccionado = x
                    break

            if producto_seleccionado is not None:

                tipo_producto = producto_seleccionado["nombre"]
                capacidad = producto_seleccionado["capacidad"]
                categoria = producto_seleccionado["categoria"]

                break

            else:
                clear()
                print("=========== AGREGAR STOCK ===========")
                listar_productos()

                print("\nID invalido, intente nuevamente.")

        except ValueError:
            clear()
            print("=========== AGREGAR STOCK ===========")
            listar_productos()

            print("\nValor invalido, solo se aceptan numeros.")

    clear()

    # Cantidad
    while True:

        try:
            print("=========== AGREGAR STOCK ===========")

            cantidad_unidades = int(input("Ingrese la cantidad a agregar: "))

            if cantidad_unidades > 0:
                break

            else:
                clear()
                print("Debe ingresar un numero mayor que 0.")
        except ValueError:
            clear()
            print("Valor invalido, solo se aceptan numeros.")

    clear()

    # Umbral
    if umbrales.get(tipo_producto) is None:  # Si no existe el umbral..

        while True:

            try:

                print("=========== AGREGAR STOCK ===========")

                valor = int(input(f"Ingrese el umbral minimo para {tipo_producto}: "))

                if valor > 0:

                    umbrales[tipo_producto] = valor
                    break

                else:
                    clear()
                    print("Debe ser mayor que 0.")

            except ValueError:
                clear()
                print("Valor invalido, solo se aceptan numeros enteros.")

    # Crear nueva carga
    nuevo_id_carga = max([x["id"] for x in stock], default=0) + 1

    nueva_carga = {
        "id": nuevo_id_carga,
        "tipo": tipo_producto,
        "capacidad": capacidad,
        "cantidad": cantidad_unidades,
        "categoria": categoria
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
        print("2. Agregar stock a otro producto")
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
    stock = stock_data.get("stock", [])  # Variable para acceder al stock
    productos = cargar_productos()  # Variable para acceder a los productos

    if not stock:
        print("===== No hay productos en stock =====")
        input("\nENTER para volver al menú")
        clear()
        return


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
                clear()
                print("=========== MODIFICAR STOCK ===========")
                listar_stock()

                print("\nID de la carga no encontrado.")

        except ValueError:
            clear()
            print("=========== MODIFICAR STOCK ===========")
            listar_stock()

            print("\nValor invalido, solo se aceptan numeros.")

    clear()

    while True:
        print("=========== MODIFICAR STOCK ===========")
        print("Selecciona lo que queres modificar...")
        print("1: Producto | 2: Cantidad de unidades\n")

        opcion = input("Seleccione una opcion (1 o 2): \n")
        clear()

        # Cambiar producto
        if opcion == "1":



            while True:

                try:
                    print("=========== MODIFICAR STOCK ===========")
                    listar_productos()

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
                    clear()
                    print("Valor invalido, solo se aceptan numeros.")
            break

        # Cambiar cantidad
        elif opcion == "2":

            while True:

                try:

                    print("=========== MODIFICAR STOCK ===========")

                    cantidad = int(input("Ingrese la nueva cantidad de unidades: "))

                    if cantidad >= 0:

                        carga["cantidad"] = cantidad
                        break

                    else:
                        clear()
                        print("La cantidad debe ser mayor o igual a 0")

                except ValueError:
                    clear()

                    print("Valor invalido, solo se aceptan numeros.")
            break

        else:
            clear()
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
        print("===========================================")
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

    stock_data = cargar_stock()  # Carga todo el json (productos y umbrales)
    stock = stock_data.get("stock", [])  # Variable para acceder a los productos

    if not stock:
        print("===== No hay productos cargados =====")
        input("\nENTER para volver al menú ")
        clear()
        return



    while True:

        try:
            print("=========== ELIMINAR CARGA STOCK ===========")
            listar_stock()
            id_stock = int(input("\nIngrese el ID de carga del producto a eliminar: "))
            break

        except ValueError:
            clear()
            print("Solo se aceptan numeros.")
            continue  # Si hubo error, lo vuelve a pedir el id

    carga = None

    for x in stock:

        if x["id"] == id_stock:
            carga = x

            break

    if carga is None:
        print("El ID de la carga no coincide con ningun producto.")
        input("\nENTER para volver al menú")
        clear()
        return



    confirmacion = 0
    while confirmacion not in ("1","2"):
        clear()
        print("=========== ELIMINAR CARGA STOCK ===========")
        confirmacion = input(
            f"La carga del producto que desea eliminar es '{carga['tipo']}', ID: '{id_stock}', con '{carga["cantidad"]}' unidades, es esto correcto? (1: Si | 2: No): ").strip()

    match confirmacion:

        case "1":

            # Elimina el producto y solo actualiza la parte del stock en el json
            stock.remove(carga)
            stock_data["stock"] = stock

        case "2":

            print("==== Eliminacion cancelada por el usuario ====")
            input("ENTER para volver al menú")
            clear()
            return

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
            return eliminar_stock()
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

def modificar_umbrales():

    stock_data = cargar_stock()
    umbrales = stock_data.get("umbrales", {})

    tipo_pintura = ["Látex Interior", "Látex Exterior", "Esmalte Sintético Brillante", "Esmalte Sintético Satinado",
                    "Barniz Marino", "Convertidor de Óxido", "Enduido Plástico Interior",
                    "Impermeabilizante para Techos", "Antihumedad"]


    indice=1

    print("============= MODIFICAR UMBRALES DE STOCK =============")
    print("Umbrales actuales:")
    print("=======================================================")
    for tipo, valor in umbrales.items():
        print(f"{indice}. {tipo}: {valor}")
        indice+=1
    print("=======================================================\n")

    while True:

        tipo_modificar = input("Ingrese el número del tipo de pintura a modificar su umbral(ENTER para salir): ").strip()

        try:
            if not tipo_modificar:
                clear()
                return
            else:
                tipo_modificar = tipo_pintura[int(tipo_modificar) - 1]
                break

        except ValueError:
            clear()
            indice=1
            print("============= MODIFICAR UMBRALES DE STOCK =============")
            print("Umbrales actuales:")
            print("=======================================================")
            for tipo, valor in umbrales.items():
                print(f"{indice}. {tipo}: {valor}")
                indice += 1
            print("=======================================================")
            print("Debe ingresar un número\n")



    clear()


    print("============= MODIFICAR UMBRALES DE STOCK =============")
    while True:
        try:

            nuevo_valor = int(input(f"Ingrese el nuevo umbral mínimo para '{tipo_modificar}': "))

            while nuevo_valor <= 0:
                print("Debe ingresar un número mayor que 0")
                nuevo_valor = int(input(f"Ingrese el nuevo umbral mínimo para '{tipo_modificar}': "))
            break

        except ValueError:
            clear()
            print("============= MODIFICAR UMBRALES DE STOCK =============")
            print("Debe ingresar un número")


    umbrales[tipo_modificar] = nuevo_valor
    stock_data["umbrales"] = umbrales
    guardar_stock(stock_data)

    clear()
    print("=========== UMBRAL MODIFICADO CORRECTAMENTE ===========")
    print(f"{tipo_modificar}: Nuevo umbral → {nuevo_valor}")

    print("============= MODIFICAR UMBRALES DE STOCK =============")
    while True:
        print("1. Volver al menú")
        print("2. Modificar otro producto")
        print("=======================================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        elif opcion == "2":
            clear()
            return modificar_umbrales()
        else:
            clear()
            print("=========== OPCIÓN INCORRECTA ===========")

# Funciones productos
def agregar_producto():
    """
    Permite al usuario agregar un producto nuevo al archivo productos.csv
    Se solicita: nombre, capacidad, categoria y precio.
    """
    print("=========== AGREGAR PRODUCTO ===========")

    productos = cargar_productos()

    categorias= ["Pintura","Protector","Preparación","Impermeabilizante"]

    # ID incremental
    if productos:
        nuevo_id = max(int(x["id"]) for x in productos) + 1
    else:
        nuevo_id = 1

    # Nombre 
    while True:
        
        nombre = input("\nIngrese el nombre del producto: ").strip().title()
        
        break

    clear()

    print("=========== AGREGAR PRODUCTO ===========")
    
    # Capacidad 
    capacidad = input("Ingrese la capacidad (1|5|10|20): ").strip()
    while capacidad not in ("1", "5", "10", "20"):
        clear()
        print("=========== AGREGAR PRODUCTO ===========")
        print("Opción incorrecta")
        capacidad = input("Ingrese la capacidad (1|5|10|20): ").strip()

    medida= input("Medida en Litros o Kilogramos (1: L | 2: kg): ").strip()
    while medida not in ("1", "2"):
        clear()
        print("=========== AGREGAR PRODUCTO ===========")
        print("Opción incorrecta")
        print(f"La capacidad ingresada es ({capacidad})")
        medida= input("Medida en Litros o Kilogramos (1: L | 2: kg): ").strip()
    if medida=="1":
        capacidad+="L"
    elif medida=="2":
        capacidad+="kg"

    clear()
    print("=========== AGREGAR PRODUCTO ===========")

    # Categoria 
    while True:
        # Muestra el listado de categorías
        for i, x in enumerate(categorias):
            print(f"{i + 1}: {x}")
        # Pide la categoría en número
        categoria = input("\nQue categoría es: ").strip()
        if categoria not in ("1", "2", "3", "4"):
            clear()
            print("=========== AGREGAR PRODUCTO ===========")
            print("Opción incorrecta\n")
        else:
            categoria = categorias[int(categoria) - 1].title()
            break

    clear()
    print("=========== AGREGAR PRODUCTO ===========")

    # Precio 
    while True:
        try:
            precio = int(input("Ingrese el precio del producto: "))
            if precio > 0:
                break
            else:
                clear()
                print("=========== AGREGAR PRODUCTO ===========")
                print("Debe ingresar un valor mayor que 0")
        except ValueError:
            clear()
            print("=========== AGREGAR PRODUCTO ===========")
            print("Valor invalido, solo se aceptan números enteros.")

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

    opcion = input("¿Desea agregar stock inicial a este producto? (1: Si | 2: No): ").lower()
    while opcion not in ("1","2"):
        clear()
        print(f"===== PRODUCTO AGREGADO =====")
        opcion = input(f"¿Desea agregar stock inicial al producto recién agregado ID: {nuevo_id}? (1: Si | 2: No): ").lower()

    if opcion=="1":
        clear()
        agregar_stock(nuevo_id)
        return

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
        input("\nENTER para volver al menú")
        clear()
        return

    listar_productos()

    while True:
        # Elegir producto
        try:
            id_eliminar = int(input("\nIngrese el ID del producto a eliminar: "))
            break
        except ValueError:
            print("Valor invalido, solo se aceptan numeros.")

    producto = None

    for x in productos:
        if int(x["id"]) == id_eliminar:
            producto = x
            break

    if not producto:
        print(f"No se encontro ningún producto con el ID {id_eliminar}")
        input("\nENTER para volver al menú")
        clear()
        return

    confirmacion = int(
        input(f"¿Desea eliminar el producto '{producto['nombre']}' ({producto['capacidad']})? (1: Si | 2: No): "))

    match confirmacion:
        case 1:

            # Eliminar producto del csv
            productos.remove(producto)
            
            # Elimina del stock y su umbral 
            stock_data = cargar_stock()
            stock = stock_data.get("stock", [])
            umbrales = stock_data.get("umbrales", {})
            
            # Eliminar sus cargas al stock
            stock_actualizado = [p for p in stock if p.get("tipo") != producto['nombre']]
            stock_data["stock"] = stock_actualizado
            
            # Eliminar al umbral (si existe)
            if producto['nombre'] in umbrales:
                del umbrales[producto['nombre']]
                stock_data["umbrales"] = umbrales

        case 2:
            print("==== Eliminacion cancelada ====")
            input("\nENTER para volver al menú")
            clear()
            return

    # Guarda todo
    guardar_stock(stock_data)
    guardar_productos(productos)
    registrar_accion("eliminar_producto")

    print(f"===== Producto '{producto['nombre']}' eliminado correctamente =====\n")
    print("Eliminado del catálogo de productos")
    print("Eliminado del stock")
    print("Eliminado de los umbrales")

    while True:
        print("\n1. Volver al menú")
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
        input("\nENTER para volver al menú")
        clear()
        return

    listar_productos()

    while True:

        # Elegir producto
        try:
            id_producto = int(input("\nIngrese el ID del producto a modificar: "))
            break

        except ValueError:
            clear()
            print("=========== MODIFICAR PRODUCTO ===========")
            listar_productos()
            print("Valor invalido, solo se aceptan numeros.")

    producto = None

    for x in productos:

        if int(x["id"]) == id_producto:
            producto = x
            break

    if not producto:
        print(f"No se encontro ningun producto con ID {id_producto}")
        input("ENTER para volver al menú")
        clear()
        return

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


def buscar_producto() -> None:
    """
    Permite buscar productos en el stock por: tipo de pintura y/o capacidad
    Muestra los productos que coincidan con la busqueda
    """
    # Carga los datos desde el archivo JSON de stock
    stock = cargar_productos()


    # Si no hay productos cargados, sale de la función
    if not stock:
        print("No hay productos cargados.")
        input("\nENTER para ir al menú")
        clear()
        return

    # Lista de tipos de pintura disponibles
    tipo_pintura = ["Látex Interior", "Látex Exterior", "Esmalte Sintético Brillante", "Esmalte Sintético Satinado", "Barniz Marino", "Convertidor de Óxido", "Enduido Plástico Interior", "Impermeabilizante para Techos", "Antihumedad"]

    #Lista de las categorías
    categorias = ["Pintura", "Protector", "Preparación", "Impermeabilizante"]

    # Opciones disponibles para filtrar (ID, tipo, capacidad, precio)
    criterios=["1","2","3","4","5","0"]

    # Guarda los filtros que ya se aplicaron
    criterios_usados=[]

    # Copia inicial de todos los productos
    resultados = stock[:]

    # Diccionario para mostrar los nombres en palabras de los filtros
    nombres_filtros = {
        "1": "ID",
        "2": "Tipo de pintura",
        "3": "Capacidad",
        "4": "Precio",
        "5": "Categoría"
    }

    # Textos reutilizables para mostrar
    textos={"header":"=========== BUSCAR PRODUCTOS ===========",
            "texto1":"Desea buscar por:\n1: ID\n2: Pintura\n3: Capacidad\n4: Precio\n5: Categoría \n0: Salir",
            "menu":"1. Volver al menú\n2. Hacer otra búsqueda",
            "separador":"==========================================="}

    # Controla el bucle principal
    salir=False

    # Bucle principal del menú de búsqueda
    while not salir:
        print(textos["header"])
        print(textos["texto1"])

        # Si se aplicaron filtros, los muestra
        if criterios_usados:
            filtros=[]
            for n in criterios_usados:
                filtros.append(nombres_filtros[n])
            print(f"Filtros usados: {', '.join(filtros)}")

        # Solicita el criterio de búsqueda
        criterio=input("Buscar por: ").strip()
        # Validación de la opción ingresada
        while criterio not in criterios:
            clear()
            print(textos["header"])
            print(textos["texto1"])
            if criterios_usados:
                print(f"Filtros usados: {", ".join(filtros)}")
            print("Opción incorrecta")
            criterio = input("Buscar por: ").strip()


        clear()

        # Si elige 0, vuelve al menú principal
        if criterio=="0":
            return

        print(textos["header"])

        # Si elige 1, Busca por id
        if criterio == "1":
            while True:
                try:
                    #Pide el id de carga y hace una lista con el resultado que encuentre
                    id_buscar = int(input("Ingrese el ID del producto: "))
                    resultados = [p for p in resultados if int(p["id"]) == id_buscar]
                    break
                except ValueError:
                    clear()
                    print(textos["header"])
                    print("El ID debe ser un número.")


        # Si elige 2, Busca por tipo de pintura
        elif criterio == "2":
            while True:
                # Muestra el listado de tipos de pintura
                for i,x in enumerate(tipo_pintura):
                    print(f"{i+1}: {x}")
                #Pide el tipo en número y válida si esta en los valores aceptados
                tipo_buscar = input("\nQue tipo de pintura es: ").strip()
                if tipo_buscar not in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                    clear()
                    print(textos["header"])
                    print("Opción incorrecta\n")
                else:
                    break

            #Pasa el número ingresado a el tipo expresado en palabras y hace una lista con los tipos que coincidan
            tipo_buscar = tipo_pintura[int(tipo_buscar) - 1].title()
            resultados = [p for p in resultados if p["nombre"] == tipo_buscar]


        # Si elige 3, Busca por capacidad
        elif criterio == "3":
            #Pide la capacidad y válida que este en los valores aceptados
            capacidad_buscar = input("Ingrese la capacidad (1|5|10|20): ").strip()
            while capacidad_buscar not in ("1","5","10","20"):
                clear()
                print(textos["header"])
                print("Opción incorrecta")
                capacidad_buscar = input("Ingrese la capacidad (1|5|10|20): ").strip()

            # Hace una lista con los valores que coincidan
            resultados = [p for p in resultados if p["capacidad"] == f"{capacidad_buscar}L" or p["capacidad"] == f"{capacidad_buscar}kg"]

        #Si elige 4, Busca por precio
        elif criterio == "4":
            while True:
                try:
                    #Pide el precio y hace una lista con los valores que coincidan
                    precio_buscar = int(input("Ingrese el precio: "))
                    resultados = [p for p in resultados if p["precio_unidad"] == precio_buscar]
                    break
                except ValueError:
                    clear()
                    print(textos["header"])
                    print("El precio debe ser un número")

        #Si elige 5, busca por categoría
        elif criterio == "5":
            while True:
                # Muestra el listado de categorías
                for i, x in enumerate(categorias):
                    print(f"{i + 1}: {x}")
                # Pide el tipo en número y válida si esta en los valores aceptados
                categoria = input("\nQue categoría es: ").strip()
                if categoria not in ("1", "2", "3", "4"):
                    clear()
                    print("=========== AGREGAR PRODUCTO ===========")
                    print("Opción incorrecta\n")
                else:
                    categoria = categorias[int(categoria) - 1].title()
                    resultados = [p for p in resultados if p["categoria"] == categoria]
                    break


        # Guarda el filtro usado y lo elimina de los filtros disponibles
        criterios_usados.append(criterio)
        criterios.remove(criterio)

        clear()

        if resultados:
            print("================================ RESULTADOS ================================")

            # Cantidad de resultados que muestra cada página
            mostrar = 5

            # Muestra los resultados en páginas de 5 en 5
            for i in range(0, len(resultados), mostrar):
                pagina = resultados[i:i + mostrar]
                print(tabulate(pagina, headers="keys", tablefmt="fancy_grid"))
                print(" " *20 + f"Mostrando {i+1}-{i+len(pagina)} de {len(resultados)} Resultados\n")

                #Si hay más de un resultado, permite agregar otro filtro, avanzar al menú, o avanzar de página en caso de que exista, si no también avanza al menú
                if len(resultados)>1:
                    seguir=input("Ingrese (1) para agregar otro filtro, (2) para continuar al menú, ENTER para continuar: ").strip()

                    # Si elige 1, vuelve a la búsqueda y permite aplicar otro filtro sobre los resultados actuales
                    if seguir == "1":
                        clear()
                        break

                    # Si elige 2, avanza al menú
                    elif seguir== "2":
                        clear()
                        salir = True
                        break

                    # Avanza ya sea a la siguiente página o a el menú
                    else:
                        clear()
                        # Si llega al final de los resultados, termina el bucle
                        if i+mostrar>=len(resultados):
                            salir = True
                        else:
                            print("================================ RESULTADOS ================================")

                # Si solo hay un resultado, solo permite avanzar al menú
                elif len(resultados)==1:
                    input("ENTER para continuar: ")
                    clear()
                    salir=True

        # Si no hay resultados o no hay más filtros para aplicar, avanza al menú
        elif not criterios or not resultados:
            print(textos["separador"])
            print("No se encontraron productos que coincidan con la búsqueda.")
            break

    # Registra la acción en el historial
    registrar_accion("buscar_producto")


    # Menú final
    print(textos["header"])
    while True:
        print(textos["menu"])
        print(textos["separador"])
        opcion = input("Seleccione una opción: ")

        # Si elige 1, vuelve al menú principal
        if opcion == "1":
            clear()
            return
        # Si elige 2, realiza otra búsqueda
        elif opcion == "2":
            clear()
            return buscar_producto()

        else:
            clear()
            print("=========== OPCIÓN INCORRECTA ===========")


def registrar_venta():
    """Registra una venta, actualiza el stock y guarda en ventas.csv (sin librería csv)."""

    print("=========== REGISTRAR VENTA ===========")

    # Importar módulos necesarios
    import json
    import os
    from datetime import datetime
    
    # Cargar datos necesarios
    stock_data = cargar_stock()
    stock = stock_data.get("stock", [])
    productos = cargar_productos()

    if not stock:
        print("No hay productos disponibles para vender.")
        input("Presione ENTER para volver al menú...")
        return

    # Mostrar productos disponibles en stock
    print("\n--- PRODUCTOS DISPONIBLES EN STOCK ---")
    for producto in stock:
        print(f"ID: {producto['id']} - {producto['tipo']} {producto['capacidad']} - Stock: {producto['cantidad']}")
    print("--------------------------------------")

    # --- Solicitar ID del producto ---
    while True:
        try:
            id_producto = int(input("\nIngrese el ID del producto vendido: ").strip())
            
            producto_stock = next((p for p in stock if int(p["id"]) == id_producto), None)
            if producto_stock is None:
                print("No se encontró un producto con ese ID en el stock.")
                continue
            
            cantidad_disponible = int(producto_stock.get("cantidad", 0))
            if cantidad_disponible <= 0:
                print("El producto no tiene stock disponible.")
                continue
                
            break
        except ValueError:
            print("Ingrese un número válido para el ID.")

    # --- Solicitar cantidad ---
    while True:
        try:
            cantidad_disponible = int(producto_stock.get("cantidad", 0))
            cantidad_vendida = int(input("Ingrese la cantidad vendida: ").strip())
            
            if cantidad_vendida <= 0:
                print("La cantidad debe ser mayor que cero.")
                continue
            if cantidad_vendida > cantidad_disponible:
                print(f"No hay suficiente stock disponible. Stock actual: {cantidad_disponible}")
                continue
            break
        except ValueError:
            print("Ingrese un número válido para la cantidad.")

    # --- Obtener datos del producto ---
    tipo_buscar = producto_stock.get("tipo", "Desconocido")
    capacidad_buscar = producto_stock.get("capacidad", "Sin categoría")
    
    # Buscar precio en la lista de productos cargada
    precio_unitario = 0.0
    categoria_encontrada = "Sin categoría"
    nombre_encontrado = tipo_buscar
    
    for producto in productos:
        # En productos.csv es "nombre", en stock es "tipo" - pero son el mismo dato
        if (producto.get("nombre", "") == tipo_buscar and 
            producto.get("capacidad", "") == capacidad_buscar):
            try:
                precio_unitario = float(producto.get("precio", 0))
                categoria_encontrada = producto.get("categoria", "Sin categoría")
                nombre_encontrado = producto.get("nombre", tipo_buscar)
                break
            except ValueError:
                continue

    # Si no se encontró precio, pedirlo manualmente
    if precio_unitario == 0:
        print(f"\nNo se encontró precio automáticamente para: {tipo_buscar} {capacidad_buscar}")
        while True:
            try:
                precio_input = input("Ingrese el precio unitario manualmente: $").strip()
                precio_unitario = float(precio_input)
                if precio_unitario <= 0:
                    print("El precio debe ser mayor que cero.")
                    continue
                break
            except ValueError:
                print("Ingrese un precio válido.")

    # --- Calcular total ---
    total_venta = round(precio_unitario * cantidad_vendida, 2)

    # --- Solicitar método de pago ---
    while True:
        metodo_pago = input("Método de pago (Efectivo/Tarjeta/Transferencia): ").strip().capitalize()
        if metodo_pago == "":
            metodo_pago = "No especificado"
            break
        elif metodo_pago in ["Efectivo", "Tarjeta", "Transferencia"]:
            break
        else:
            print("Método de pago no válido. Use: Efectivo, Tarjeta o Transferencia")

    # --- Actualizar stock ---
    producto_stock["cantidad"] = cantidad_disponible - cantidad_vendida

    try:
        with open("stock_data.json", "w", encoding="utf-8") as archivo:
            json.dump(stock_data, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al actualizar el stock: {e}")
        return

    # --- Generar ID autoincremental de venta ---
    id_venta = 1
    if os.path.exists("ventas.csv"):
        try:
            with open("ventas.csv", "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
                if len(lineas) > 1:
                    for i in range(len(lineas)-1, 0, -1):
                        if lineas[i].strip():
                            partes = lineas[i].strip().split(",")
                            if partes and partes[0].isdigit():
                                id_venta = int(partes[0]) + 1
                                break
        except Exception as e:
            print(f"Error al leer ventas.csv: {e}")

    # --- Crear registro de venta ---
    fecha_y_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    venta = [
        str(id_venta),
        fecha_y_hora,
        str(id_producto),
        nombre_encontrado,
        categoria_encontrada,
        str(cantidad_vendida),
        f"{precio_unitario:.2f}",
        f"{total_venta:.2f}",
        metodo_pago
    ]

    # --- Guardar o crear ventas.csv ---
    try:
        nuevo = not os.path.exists("ventas.csv")
        with open("ventas.csv", "a", encoding="utf-8") as archivo:
            if nuevo:
                archivo.write("id_venta,fecha_y_hora,id_producto,nombre_producto,categoria,cantidad,precio_unitario,total,metodo_pago\n")
            archivo.write(",".join(venta) + "\n")
    except Exception as e:
        print(f"Error al guardar la venta: {e}")
        return

    # --- Confirmación ---
    print("\n===== VENTA REGISTRADA CORRECTAMENTE =====")
    print(f"ID Venta: {id_venta}")
    print(f"Producto: {nombre_encontrado} {capacidad_buscar}")
    print(f"Categoría: {categoria_encontrada}")
    print(f"Cantidad: {cantidad_vendida}")
    print(f"Precio unitario: ${precio_unitario:.2f}")
    print(f"Total: ${total_venta:.2f}")
    print(f"Método de pago: {metodo_pago}")
    print("===========================================")
    
    while True:
        print("1. Volver al menú principal")
        print("2. Registrar otra venta")
        print("============================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        elif opcion == "2":
            clear()
            return registrar_venta()
        else:
            clear()
            print("=========== OPCIÓN INCORRECTA ===========")


def mostrar_stock_bajo() -> None:
    """
    Muestra todos los productos cuyo stock sea menor a un valor mínimo
    Sirve para identificar productos que deben reponerse
    """
    # Carga los datos desde el archivo JSON
    stock_data = cargar_stock()

    # Obtiene la lista de productos y los umbrales de stock mínimo
    stock = stock_data.get("stock", [])
    umbrales = stock_data.get("umbrales", {})


    if not stock:
        print("No hay productos cargados.")
        input("\nENTER para ir al menú")
        clear()
        return

    # Filtra los productos por su umbral minimo
    stock_bajo = [p for p in stock if p["cantidad"] <= umbrales[p["tipo"]]]

    # Cantidad de resultados que muestra cada página
    mostrar = 5

    # Muestra los resultados en páginas de 5 en 5
    for i in range(0, len(stock_bajo), mostrar):
        print("========================= PRODUCTOS CON STOCK BAJO =========================")
        pagina = stock_bajo[i:i + mostrar]
        print(tabulate(pagina, headers="keys", tablefmt="fancy_grid"))
        print(" " * 20 + f"Mostrando {i + 1}-{i + len(pagina)} de {len(stock_bajo)} Resultados\n")

        # Si hay más productos para mostrar
        if i+mostrar <= len(stock_bajo):
            seguir = input("Ingrese (1) para volver al menú, ENTER para ver más resultados: ").strip()

            # Si elige 1, vuelve al menú principal, si no, continúa
            if seguir == "1":
                clear()
                return
            else:
                clear()
        # Si llegó al final de los resultados, espera ENTER y vuelve al menú
        else:
            input("ENTER para ir al menú: ")
            clear()
            return


def mostrar_reportes():
    """
    Muestra los reportes de ventas por fecha
    """
    print("=========== REPORTES ===========")

    ventas = cargar_ventas()

    if not ventas:
        print("No hay ventas registradas para mostrar.")
        input("Presione ENTER para volver al menú...")
        return

    # Convertir los datos para tabulate
    tabla_datos = []
    for venta in ventas:
        fila = [
            venta.get('id_venta', ''),
            venta.get('fecha_y_hora', ''),
            venta.get('id_producto', ''),
            venta.get('nombre_producto', ''),
            venta.get('categoria', ''),
            venta.get('cantidad', ''),
            f"${venta.get('precio_unitario', '0')}",
            f"${venta.get('total', '0')}",
            venta.get('metodo_pago', '')
        ]
        tabla_datos.append(fila)

    # Definir encabezados 
    encabezados = [
        'ID Venta',
        'Fecha y Hora', 
        'ID Producto',
        'Nombre Producto',
        'Categoría',
        'Cantidad',
        'Precio Unitario',
        'Total',
        'Método Pago'
    ]

    print(tabulate(tabla_datos, headers=encabezados, tablefmt="grid"))

    while True:
        print("\n1. Volver al menú")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")


def exportar_stock_csv():
    """
    Exporta todos los datos del stock a un archivo CSV
    """
    print("=========== EXPORTAR STOCK A CSV ===========")
 

    try:
        # Cargar los datos del stock
        stock_data = cargar_stock()
        stock = stock_data.get("stock", [])
        
        if not stock:
            print("No hay datos de stock para exportar.")

        
        # Archivo exportado
        nombre_archivo = "stock_exportado.csv"
        
        # Crea y escribe el csv
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            # Escribir encabezado
            archivo.write("id,tipo,capacidad,cantidad\n")
            
            # Escribe cada producto
            for producto in stock:
                linea = f"{producto['id']},{producto['tipo']},{producto['capacidad']},{producto['cantidad']}\n"
                archivo.write(linea)
        
        print(f"Stock exportado correctamente a: {nombre_archivo}")
        print(f"Total de productos exportados: {len(stock)}")
        
    except Exception as e:

        print(f"Error al exportar el stock: {e}")
    
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