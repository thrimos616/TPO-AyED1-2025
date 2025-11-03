import os
import tabulate
import json
from datetime import datetime
import csv



def clear():
    os.system("cls" if os.name == "nt" else "clear")

def cargar_datos():
    """
    Carga los datos del stock desde un json
    Inicia la lista "stock" con los productos existentes
    """
    try:

        with open("stock.json", "rt", encoding="utf-8") as stock_json:

                return json.load(stock_json)

    except (FileNotFoundError,OSError,json.JSONDecodeError):

        print("Archivo no encontrado.")

        return []


def guardar_datos(datos):
    """
    Guarda los datos del stock en un json
    """

    try:

        with open("stock.json", "wt", encoding="utf-8") as f:

            json.dump(datos, f, ensure_ascii=False, indent=4)

    except (PermissionError,TypeError,OSError):

        print("El archivo no pudo ser guardado.")



def registrar_accion(accion, detalle):
    """
    Evalua que accion fue realizada en el sistema y la registra en un historial
    """
    fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    linea = f"[{fecha}] {accion}: {detalle}\n"
    try:
        with open("log.txt", "at", encoding="utf-8") as log:
            log.write(linea)
    except Exception as e:
        print("Error al escribir log:", e)



def agregar_producto():
    """
    Agrega un nuevo producto al stock
    Se le solicita al usuario: tipo de pintura (satinada o brillante), capacidad de la lata (1lt, 5lts, 10lts o 20lts),
    la cantidad de ese producto y su precio por unidad
    """
    stock=cargar_datos()

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
            umbral=int(input("Umbral de stock bajo: "))
            while umbral<=0:
                print("Debe ser mayor a 0")
                umbral=int(input("Umbral de stock bajo: "))
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

    producto = {"id": nuevo_id, "tipo": pintura, "capacidad": capacidad, "cantidad": cantidad, "precio": precio, "Umbral de stock":umbral}
    stock.append(producto)


    stock=guardar_datos(stock)
    clear()

    print("===== PRODUCTO AGREGADO CORRECTAMENTE =====")
    print(f"Producto ID: {nuevo_id}")
    print(f"Pintura:{pintura}\nCapacidad:{capacidad}\nStock:{cantidad}\nUmbral:{umbral}\nPrecio ${precio}")

    print("===========================================")
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

    stock = cargar_datos()

    try:

        id_producto = int(input("Ingrese el ID del producto a modificar: "))

    except ValueError:

        print("Solo se aceptan numeros")

    producto = None

    for x in stock:  # x seria el diccionario, osea cada producto por individual

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

            case _:  # Funciona como un else

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

        id_producto = int(input("Ingrese el ID del producto a eliminar: "))

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
    pass











def buscar_producto():
    """
    Permite buscar productos en el stock por: tipo de pintura y/o capacidad
    Muestra los productos que coincidan con la busqueda
    """
    stock = cargar_datos()

    if not stock:
        print("No hay productos cargados.")
        return

    tipo_pintura = ["Satinada", "Brillante"]
    criterios=["1","2","3","4","0"]
    criterios_usados=[]
    nombres_filtros = {
        "1": "ID",
        "2": "Tipo de pintura",
        "3": "Capacidad",
        "4": "Precio"
    }

    textos={"header":"=========== BUSCAR PRODUCTOS ===========",
            "texto1":"¿Desea buscar por ID(Ingrese 1), pintura(2), por capacidad(3) o precio(4)? (0 Para salir)",
            "menu":"1. Volver al menú\n2. Hacer otra búsqueda",
            "separador":"==========================================="}

    resultados = stock[:]
    salir=False

    while not salir:
        print(textos["header"])
        print(textos["texto1"])

        if criterios_usados:
            filtros=[]
            for n in criterios_usados:
                filtros.append(nombres_filtros[n])
            print(f"Filtros usados: {', '.join(filtros)}")

        criterio=input("Buscar por: ").strip()
        while criterio not in criterios:
            clear()
            print(textos["header"])
            print(textos["texto1"])
            if criterios_usados:
                print(f"Filtros usados: {", ".join(filtros)}")
            print("Opción incorrecta\n")
            criterio = input("Buscar por: ").strip()


        clear()

        if criterio=="0":
            return

        print(textos["header"])

        if criterio == "1":
            while True:
                try:
                    id_buscar = int(input("Ingrese el ID del producto: "))
                    resultados = [p for p in resultados if p["id"] == id_buscar]
                    break
                except ValueError:
                    print("El ID debe ser un número.")


        elif criterio == "2":
            tipo_buscar = input("Que tipo de pintura es (1:Satinada, 2:Brillante): ").strip()
            while tipo_buscar not in ("1", "2"):
                tipo_buscar = input("Que tipo de pintura es: ").strip()
            tipo_buscar = tipo_pintura[int(tipo_buscar) - 1].capitalize()
            resultados = [p for p in resultados if p["tipo"] == tipo_buscar]


        elif criterio == "3":
            capacidad_buscar = input("Ingrese la capacidad (1|5|10|20): ").strip()
            while capacidad_buscar not in ("1","5","10","20"):
                capacidad_buscar = input("Ingrese la capacidad (1|5|10|20): ").strip()
            resultados = [p for p in resultados if p["capacidad"] == f"{capacidad_buscar}L"]


        elif criterio == "4":
            while True:
                try:
                    precio_buscar = int(input("Ingrese el precio: "))
                    resultados = [p for p in resultados if p["precio"] == precio_buscar]
                    break
                except ValueError:
                    print("El precio debe ser un número")

        criterios_usados.append(criterio)
        criterios.remove(criterio)

        clear()

        if resultados:
            print("================================ RESULTADOS ================================")
            paso = 5
            for i in range(0, len(resultados), paso):
                pagina = resultados[i:i + paso]
                print(tabulate.tabulate(pagina, headers="keys", tablefmt="fancy_grid"))
                print(" " *20 + f"Mostrando {i+1}-{i+len(pagina)} de {len(resultados)} Resultados\n")

                if len(resultados)>1:
                    seguir=input("Ingrese (1) para agregar otro filtro, (2) para continuar al menú, ENTER para continuar: ").strip().title()
                    if seguir == "1":
                        clear()
                        break
                    elif seguir== "2":
                        clear()
                        salir = True
                        break
                    else:
                        clear()

                        if i+paso>=len(resultados):
                            salir=True
                        else:
                            print("================================ RESULTADOS ================================")


                elif len(resultados)==1:
                    input("ENTER para continuar: ")
                    clear()
                    salir=True

        elif not criterios or not resultados:
            print(textos["separador"])
            print("No se encontraron productos que coincidan con la búsqueda.")
            break

    filtros_log = []
    for n in criterios_usados:
        filtros_log.append(nombres_filtros[n])

    detalle = f"Criterios: {', '.join(filtros_log)} | Resultados: {len(resultados)}"
    registrar_accion("Búsqueda de producto", detalle)

    print(textos["header"])
    while True:
        print(textos["menu"])
        print(textos["separador"])
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clear()
            return
        elif opcion == "2":
            clear()
            return buscar_producto()
        else:
            clear()
            print("=========== OPCIÓN INCORRECTA ===========")








def registrar_venta():
    """
    Registra una venta de un producto solicitando: ID del producto, cantidad vendida
    Se descuenta del stock y se registra en el historial
    """
    pass




def mostrar_stock_bajo():
    """
    Muestra todos los productos cuyo stock sea menor a un valor mínimo
    Sirve para identificar productos que deben reponerse
    """
    stock = cargar_datos()

    if not stock:
        print("No hay productos cargados.")
        return


    stock_bajo = [p for p in stock if p["cantidad"] <= p["Umbral de stock"]]

    if stock_bajo:
        registrar_accion("Consulta de stock bajo", f"{len(stock_bajo)} productos con stock bajo")

        paso = 5
        for i in range(0, len(stock_bajo), paso):
            print("========================= PRODUCTOS CON STOCK BAJO =========================")
            pagina = stock_bajo[i:i + paso]
            print(tabulate.tabulate(pagina, headers="keys", tablefmt="fancy_grid"))
            print(" " * 20 + f"Mostrando {i + 1}-{i + len(pagina)} de {len(stock_bajo)} Resultados\n")

            if i+paso <= len(stock_bajo):
                seguir = input("Ingrese (1) para volver al menú, ENTER para ver más resultados: ").strip().title()

                if seguir == "1":
                    clear()
                    return
                else:
                    clear()

            else:
                input("ENTER para ir al menú: ")
                clear()
                return

    else:
        registrar_accion("Consulta de stock bajo", "Sin productos con stock bajo")





def mostrar_reportes():
    """
    Muestra los reportes de ventas por fecha
    """
    pass


def exportar_csv():
    """
    Exporta todos los datos del stock a un archivo CSV
    """
    pass