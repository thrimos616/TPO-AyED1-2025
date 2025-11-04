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
- **Eliminar producto:** elimina productos del stock.

### 🔹 Funciones adicionales
- **Registrar venta:** descuenta del stock los productos vendidos y guarda la operación.
- **Mostrar stock bajo:** muestra productos con menos de una cantidad mínima definida (por ejemplo, 5 unidades).
- **Mostrar reportes:** genera estadísticas del stock (valor total, productos más o menos disponibles, etc.).
- **Exportar a CSV:** crea un archivo con todo el stock actual, compatible con Excel o Google Sheets.

---

## Estructura del proyecto

sistema_stock_tpo/
│
├── main.py # Menú principal y flujo general del sistema
├── crud.py # Funciones CRUD (gestión básica del stock)
│
├── stock_data.json # Base de datos del stock (productos)
└── historial.txt # Registro de acciones realizadas


