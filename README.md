AVISO: Este readme esta claramente "GPTEADO", lo revise pero es posible que haya pasado algo por alto, gracias por leer el aviso 

# Sistema de Stock para Pinturería

##  Descripción del proyecto
Este proyecto consiste en un **sistema de gestión de stock** desarrollado en **Python**, diseñado para una **pinturería** que trabaja con distintos tipos y capacidades de pintura.  
El sistema permite realizar las operaciones básicas **CRUD** (Crear, Leer, Actualizar y Eliminar productos), además de registrar ventas, generar reportes y exportar los datos a un archivo CSV.

Todo el funcionamiento se realiza mediante una **interfaz por consola**, con una estructura modular que facilita su mantenimiento y ampliación.


## Funcionalidades principales

### 🔹 CRUD (Gestión del stock)
- **Agregar producto:** registra nuevos productos (tipo, capacidad, cantidad, precio).
- **Listar productos:** muestra todos los productos del stock en formato tabular.
- **Buscar producto:** permite buscar productos por tipo o capacidad.
- **Modificar producto:** actualiza cantidad o precio de productos existentes.
- **Eliminar producto:** elimina productos cargados en el csv.
- **Agregar stock:** agrega cargas de productos al stock guardadas en el JSON.
- **Eliminar stock:** elimina cargas de productos al stock guardadas en el JSON.
- **Modificar stock:** modifica los atributos (tipo, capacidad o unidades) de una carga de stock.

### 🔹 Funciones adicionales
- **Registrar venta:** descuenta del stock los productos vendidos y guarda la operación en un csv.
- **Mostrar stock bajo:** muestra productos con menos de una cantidad mínima definida (por ejemplo, 5 unidades).
- **Mostrar ventas:** muestra en una tabla todas las ventas y su fecha de realizacion.
- **Exportar a CSV:** crea un archivo con todo el stock actual, compatible con Excel o Google Sheets.

---

## Estructura del proyecto

sistema_stock_tpo/
│
├── main.py                # Menú principal y flujo general del sistema
├── funciones_crud.py      # Funciones CRUD y auxiliares
│
├── productos.csv          # Catálogo de productos (id, tipo, capacidad, precio_unidad)
├── stock_data.json        # Datos del stock y umbrales de reposición
├── ventas.csv             # Datos de las ventas realizadas 
└── historial.txt          # Registro de operaciones (ventas, altas, bajas, etc.)