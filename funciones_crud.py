# Funciones principales del sistema (Create, Read, Update, Delete)

import json
import tabulate
import datetime

def cargar_datos():
    """
    Carga los datos del stock desde un json
    Inicia la lista "stock" con los productos existentes
    """

    pass

def guardar_datos():
    """
    Guarda los datos del stock en un json
    """

    pass

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

    pass

def modificar_producto():
    """
    Modifica un producto existente en el stock
    Se le pide al usuario seleccionar entre, tipo de producto o precio de unidad
    """

def eliminar_producto():
    """
    Elimina un producto del stock
    Se le solicita al usuario el ID del producto a eliminar
    """
    pass

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
    pass