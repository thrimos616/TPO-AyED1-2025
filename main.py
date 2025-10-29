import os
import tabulate
import json

stock=[]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def cargar_datos():
    """
    Carga los datos del stock desde un json
    Inicia la lista "stock" con los productos existentes
    """
    global stock
    try:
        with open("stock.json", "rt", encoding="utf-8") as stock_json:
                stock = json.load(stock_json)
    except (FileNotFoundError,OSError,json.JSONDecodeError):
        stock=[]


def guardar_datos():
    """
    Guarda los datos del stock en un json
    """
    global stock
    try:
        with open("stock.json", "wt", encoding="utf-8") as archivo:
            json.dump(stock, archivo, indent=2)
    except (PermissionError,TypeError,OSError) as e:
        print("Error",e)

def registrar_accion():
    """
    Evalua que accion fue realizada en el sistema y la registra en un historial
    """

    pass

def agregar_producto():
    """
    Agrega un nuevo producto al stock
    Se le solicita al usuario: tipo de pintura (satinada o brillante), capacidad de la lata (1lt, 5lts, 10lts o 20lts),
    la cantidad de ese producto y su precio por unidad
    """
    tipo_pintura=["Satinada","Brillante"]
    print("=========== AGREGAR PRODUCTO ===========")

    pintura=input("Que tipo de pintura es (1:Satinada, 2:Brillante): ").strip()
    while pintura not in ("1","2"):
        pintura = input("Que tipo de pintura es: ").strip()
    pintura= tipo_pintura[int(pintura)-1]


    capacidad=input("Capacidad de la lata en Lts (1,5,10 o 20): ").strip()
    while capacidad not in ("1","5","10","20"):
        capacidad=input("Capacidad de la lata: ").strip()
    capacidad=f"{int(capacidad)}L"


    while True:
        try:
            cantidad=int(input("Stock ingresado: "))
            while cantidad<0:
                print("No puede ser menor a 0")
                cantidad = int(input("Stock ingresado: "))
            break
        except ValueError:
            pass

    while True:
        try:
            precio=int(input("Precio: $"))
            while precio<=0:
                print("Debe ser mayor a 0")
                precio = int(input("Precio: $"))
            break
        except ValueError:
            pass


    nuevo_id = max([p["id"] for p in stock], default=0) + 1

    producto = {"id": nuevo_id, "tipo": pintura, "capacidad": capacidad, "cantidad": cantidad, "precio": precio}
    stock.append(producto)


    guardar_datos()
    clear()

    print("===== PRODUCTO AGREGADO CORRECTAMENTE =====")
    print(f"Producto ID: {nuevo_id}")
    print(f"Pintura:{pintura}, capacidad:{capacidad}, Stock:{cantidad}, Precio ${precio}\n")


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

def main():

    cargar_datos()

    while True:
        opciones = [
            ("1", "Agregar producto", agregar_producto),
            ("2", "Modificar producto", modificar_producto),
            ("3", "Eliminar producto", eliminar_producto),
            ("4", "Buscar producto", buscar_producto),
            ("5", "Listar productos con bajo stock", mostrar_stock_bajo),
            ("6", "Registrar ventas", registrar_venta),
            ("7", "Mostrar reportes", mostrar_reportes),
            ("8", "Exportar stock a csv", exportar_csv),
            ("0", "Salir", None)
        ]

        while True:
            print("===== SISTEMA DE STOCK - CENTRO PINTURERIAS =====")
            for clave, texto, funcion in opciones:
                print(f"{clave}. {texto}")
            print("===========================================")

            opcion = input("Seleccione una opción: ")
            clear()

            for clave, texto, funcion in opciones:
                if opcion == clave:
                    if clave == "0":
                        print("Saliendo del sistema...")
                        return
                    funcion()
                    break
            else:
                print("Opción inválida.")


if __name__ == "__main__":
    main()