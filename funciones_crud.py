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

        return {
        "productos": [],
        "umbrales": {
            "Látex Interior": 1,
            "Látex Exterior": 1,
            "Esmalte Sintético Brillante": 1,
            "Esmalte Sintético Satinado": 1,
            "Barniz Marino": 1,
            "Convertidor de Óxido": 1,
            "Enduido Plástico Interior": 1,
            "Impermeabilizante para Techos": 1,
            "Antihumedad": 1
        }
    }



def guardar_datos(datos):
    """
    Guarda los datos del stock en un json
    """

    try:

        with open("stock.json", "wt", encoding="utf-8") as f:

            json.dump(datos, f, ensure_ascii=False, indent=4)

    except (PermissionError,TypeError,OSError):

        print("El archivo no pudo ser guardado.")



def registrar_accion(nombre_funcion):
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

                # Si existe, simplemente lo escribe
        with open(ruta_archivo, "a", encoding="utf-8") as archivo:

            archivo.write(linea_horario)

    except FileNotFoundError:

        print("No se encontro o no se pudo crear el archivo.")

    except OSError as e:

        print(f"Error del sistema al registrar el historial: {e}")


def agregar_producto():
    """
    Agrega un nuevo producto al stock
    Se le solicita al usuario: tipo de pintura (satinada o brillante), capacidad de la lata (1lt, 5lts, 10lts o 20lts),
    la cantidad de ese producto y su precio por unidad
    """


    stock_data = cargar_datos()  # Carga todo el json (productos y umbrales)
    stock = stock_data.get("productos", [])  # Variable para acceder a los productos
    umbrales = stock_data.get("umbrales", {})  # Variable para acceder a los umbrales

    # Tipo de pintura
    while True:

        try:
            print("=========== AGREGAR PRODUCTO ===========")
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
            clear()
            print("El valor ingresado es incorrecto. Solo se aceptan valores numericos.")

    # Umbrales
    if umbrales.get(tipo_producto) is None:  # Si no existe el umbral del producto...

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
            print("=========== AGREGAR PRODUCTO ===========")
            print("1: 1L | 2: 5L | 3: 10L | 4: 20L\n")

            pintura_capacidad = int(input("Ingrese la capacidad de la lata: "))
            clear()

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
            clear()
            print("El valor ingresado es incorrecto. Solo se aceptan valores numericos.")

    # Cantidad stock ingresado
    while True:

        try:
            print("=========== AGREGAR PRODUCTO ===========")
            cantidad_unidades = int(input("Ingrese la cantidad de unidades: "))
            clear()

            if cantidad_unidades > 0:
                break

            else:

                print("Debe ingresar un numero mayor que 0.")

        except ValueError:
            clear()
            print("El valor ingresado es invalido. No se aceptan letras ni valores numericos negativos.")

    # Precio
    while True:

        try:
            print("=========== AGREGAR PRODUCTO ===========")
            precio_unidad = int(input("Ingrese el precio por unidad: "))
            clear()

            if precio_unidad > 0:
                break

            else:

                print("Debe ingresar un precio mayor que 0.")

        except ValueError:
            clear()
            print("El valor ingresado es invalido. No se aceptan letras ni valores numericos negativos.")

    # ID carga
    nuevo_id_carga = len(
        stock) + 1  # sisi, ya se, es muy holgazan de mi parte, y mariano es posible que haga algun comentario xd

    # Estructura producto en el json
    producto = {
        "id": id_tipo,
        "id_carga": nuevo_id_carga,
        "tipo": tipo_producto,
        "capacidad": capacidad,
        "cantidad": cantidad_unidades,
        "precio_unidad": precio_unidad
    }

    # Guarda todo
    stock.append(producto)  # La carga del producto
    stock_data["productos"] = stock  # El producto
    stock_data["umbrales"] = umbrales  # El umbral
    guardar_datos(stock_data)
    clear()

    print("===== PRODUCTO AGREGADO CORRECTAMENTE =====")
    print(
        f"Pintura: {tipo_producto}, Capacidad: {capacidad}, Unidades agregadas: {cantidad_unidades}, Precio por unidad: ${precio_unidad}\n")

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





def modificar_umbrales():

    stock_data = cargar_datos()
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
    guardar_datos(stock_data)

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








def modificar_producto():
    """
    Modifica un producto existente en el stock
    Se le pide al usuario seleccionar entre, tipo de producto o precio de unidad
    """
    print("=========== MODIFICAR PRODUCTO ===========")

    listar_productos()

    stock_data = cargar_datos()  # Carga todo el json (productos y umbrales)
    stock = stock_data.get("productos", [])  # Variable para acceder a los productos
    umbrales = stock_data.get("umbrales", {})  # Variable para acceder a los umbrales

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

    # Guardar los cambios
    guardar_datos(stock_data)
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

    stock_data = cargar_datos()  # Carga todo el json (productos y umbrales)
    stock = stock_data.get("productos", [])  # Variable para acceder a los productos

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

    confirmacion = int(input(
        f"La carga del producto que desea eliminar es '{producto['tipo']}', ID: '{id_carga}', con '{producto["cantidad"]}' unidades, es esto correcto? (1: Si | 2: No): "))

    match confirmacion:

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
            return eliminar_carga_producto()
        else:
            clear()
            print("===== OPCIÓN INCORRECTA =====")


def listar_productos():
    """
    Muestra por pantalla todos los productos del stock en forma de tabla
    Cada producto debe mostrar: ID, tipo de pintura, capacidad (lts), cantidad, precio de la unidad
    """
    stock_data = cargar_datos()  # Carga todo el json (productos y umbrales)
    stock = stock_data.get("productos", [])  # Variable para acceder a los productos

    if not stock:
        print("===== No hay productos en stock =====")

    print(tabulate.tabulate(stock, headers="keys", tablefmt="grid", showindex=False))  # Muestra el dic como una tabla











def buscar_producto() -> None:
    """
    Permite buscar productos en el stock por: tipo de pintura y/o capacidad
    Muestra los productos que coincidan con la busqueda
    """
    # Carga los datos desde el archivo JSON de stock
    stock_data = cargar_datos()
    stock = stock_data.get("productos", [])

    # Si no hay productos cargados, sale de la función
    if not stock:
        print("No hay productos cargados.")
        return

    # Lista de tipos de pintura disponibles
    tipo_pintura = ["Látex Interior", "Látex Exterior", "Esmalte Sintético Brillante", "Esmalte Sintético Satinado", "Barniz Marino", "Convertidor de Óxido", "Enduido Plástico Interior", "Impermeabilizante para Techos", "Antihumedad"]

    # Opciones disponibles para filtrar (ID, tipo, capacidad, precio)
    criterios=["1","2","3","4","0"]

    # Guarda los filtros que ya se aplicaron
    criterios_usados=[]

    # Copia inicial de todos los productos
    resultados = stock[:]

    # Diccionario para mostrar los nombres en palabras de los filtros
    nombres_filtros = {
        "1": "ID",
        "2": "Tipo de pintura",
        "3": "Capacidad",
        "4": "Precio"
    }

    # Textos reutilizables para mostrar
    textos={"header":"=========== BUSCAR PRODUCTOS ===========",
            "texto1":"¿Desea buscar por ID(Ingrese 1), pintura(2), por capacidad(3) o precio(4)? (0 Para salir)",
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
                    resultados = [p for p in resultados if p["id_carga"] == id_buscar]
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
            tipo_buscar = tipo_pintura[int(tipo_buscar) - 1].capitalize()
            resultados = [p for p in resultados if p["tipo"] == tipo_buscar]


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
            resultados = [p for p in resultados if p["capacidad"] == f"{capacidad_buscar}L"]

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
                print(tabulate.tabulate(pagina, headers="keys", tablefmt="fancy_grid"))
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








def mostrar_stock_bajo() -> None:
    """
    Muestra todos los productos cuyo stock sea menor a un valor mínimo
    Sirve para identificar productos que deben reponerse
    """
    # Carga los datos desde el archivo JSON
    stock_data = cargar_datos()

    # Obtiene la lista de productos y los umbrales de stock mínimo
    stock = stock_data.get("productos", [])
    umbrales = stock_data.get("umbrales", {})

    # Si no hay productos cargados, sale de la función
    if not stock:
        print("No hay productos cargados.")
        return

    # Filtra los productos que su stock actual sea menor o igual al umbral definido por tipo
    stock_bajo = [p for p in stock if p["cantidad"] <= umbrales[p["tipo"]]]

    # Cantidad de resultados que muestra cada página
    mostrar = 5

    # Muestra los resultados en páginas de 5 en 5
    for i in range(0, len(stock_bajo), mostrar):
        print("========================= PRODUCTOS CON STOCK BAJO =========================")
        pagina = stock_bajo[i:i + mostrar]
        print(tabulate.tabulate(pagina, headers="keys", tablefmt="fancy_grid"))
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






def registrar_venta():
    """
    Registra una venta de un producto solicitando: ID del producto, cantidad vendida
    Se descuenta del stock y se registra en el historial
    """

    pass

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