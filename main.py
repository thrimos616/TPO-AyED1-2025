from funciones_crud import *

def main():

    while True:
        opciones = [
            ("1", "Agregar stock", agregar_stock),
            ("2", "Modificar stock", modificar_stock),
            ("3", "Eliminar stock", eliminar_stock),
            ("4", "Agregar producto", agregar_producto),
            ("5", "Eliminar producto", eliminar_producto),
            ("6", "Modificar producto", modificar_producto),
            ("7", "Buscar producto", buscar_producto),
            ("8", "Listar productos con bajo stock", mostrar_stock_bajo),
            ("9", "Registrar ventas", registrar_venta),
            ("10", "Mostrar reportes", mostrar_reportes),
            ("11", "Exportar stock a csv", exportar_stock_csv),
            ("12", "Modificar Umbrales", modificar_umbrales),
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