from funciones_crud import *

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

