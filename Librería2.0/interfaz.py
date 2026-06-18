# interfaz.py

import tkinter as tk
from tkinter import messagebox

from Clases.GestorVentas import GestorVentas
from Clases.GestorArchivo import GestorArchivos
from Clases.GestorInventario import GestorInventario


class VentanaPrincipal:

    def __init__(self):

        archivos = GestorArchivos()

        productos, ventas = archivos.cargar_datos()

        self.archivos = archivos
        self.inventario = GestorInventario(productos)
        self.caja = GestorVentas(ventas)

        self.root = tk.Tk()
        self.root.title("Sistema de Librería")
        self.root.geometry("1200x800")

        titulo = tk.Label(
            self.root,
            text="SISTEMA DE LIBRERÍA",
            font=("Arial", 40, "bold")
        )

        titulo.pack(pady=20)

        tk.Button(
            self.root,
            text="Registrar Producto",
            width=100,
            height=6,
            bg="#4CAF50",
            fg="white",
            command=self.registrar_producto
        ).pack(pady=5)               

        tk.Button(
            self.root,
            text="Mostrar Productos",
            width=100,
            height=6,
            bg="#4CAF50",
            fg="white",
            command=self.mostrar_productos
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Buscar Producto",
            width=100,
            height=6,
            bg="#4CAF50",
            fg="white",
            command=self.buscar_producto
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Registrar Venta",
            width=100,
            height=6,
            bg="#4CAF50",
            fg="white",
            command=self.registrar_venta
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Reporte de Ventas",
            width=100,
            height=6,
            bg="#4CAF50",
            fg="white",
            command=self.reporte_ventas
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Guardar y Salir",
            width=100,
            height=6,
            bg="#4CAF50",
            fg="white",
            command=self.salir
        ).pack(pady=15)

    def registrar_producto(self):
        messagebox.showinfo(
            "Info",
            "Aquí irá la ventana de registro"
        )

    def mostrar_productos(self):
        messagebox.showinfo(
            "Info",
            "Aquí irá la lista de productos"
        )

    def buscar_producto(self):
        messagebox.showinfo(
            "Info",
            "Aquí irá la búsqueda"
        )

    def registrar_venta(self):
        messagebox.showinfo(
            "Info",
            "Aquí irá la venta"
        )

    def reporte_ventas(self):
        messagebox.showinfo(
            "Info",
            "Aquí irá el reporte"
        )

    def salir(self):

        self.archivos.guardar_datos(
            self.inventario.productos,
            self.caja.ventas
        )

        self.root.destroy()

    def ejecutar(self):
        self.root.mainloop()