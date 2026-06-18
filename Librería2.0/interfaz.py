# interfaz.py

import tkinter as tk
from tkinter import ttk, messagebox

from Clases.GestorVentas import GestorVentas
from Clases.GestorArchivo import GestorArchivos
from Clases.GestorInventario import GestorInventario


class VentanaPrincipal:
    def __init__(self):
        self.archivos = GestorArchivos()

        productos_guardados, ventas_guardadas = self.archivos.cargar_datos()

        self.inventario = GestorInventario(productos_guardados)
        self.caja = GestorVentas(ventas_guardadas)

        self.root = tk.Tk()
        self.root.title("Librería Machuca - Sistema de Gestión")
        self.root.geometry("1200x900")

        self.crear_menu()

    def ejecutar(self):
        self.root.mainloop()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ======================
    # MENÚ PRINCIPAL
    # ======================
    def crear_menu(self):
        self.limpiar_pantalla()

        tk.Label(
            self.root,
            text="LIBRERÍA MACHUCA",
            font=("Arial", 35, "bold")
        ).pack(pady=20)
        tk.Button(self.root, text="Registrar Producto", width=60, height=3, bg="#607D8B", fg="white", font=("Comic Sans", 15, "bold"), command=self.crear_registro).pack(pady=5)
        tk.Button(self.root, text="Mostrar Productos", width=60, height=3, bg="#607D8B", fg="white", font=("Comic Sans", 15, "bold"), command=self.crear_productos).pack(pady=5)
        tk.Button(self.root, text="Buscar Producto", width=60, height=3, bg="#607D8B", fg="white", font=("Comic Sans", 15, "bold"), command=self.crear_busqueda).pack(pady=5)
        tk.Button(self.root, text="Vender Producto", width=60, height=3, bg="#607D8B", fg="white", font=("Comic Sans", 15, "bold"), command=self.crear_ventas).pack(pady=5)
        tk.Button(self.root, text="Reporte de Ventas", width=60, height=3, bg="#607D8B", fg="white", font=("Comic Sans", 15, "bold"), command=self.crear_reporte).pack(pady=5)
        tk.Button(self.root, text="Guardar y Salir", width=60, height=3, bg="#607D8B", fg="white", font=("Comic Sans", 15, "bold"), command=self.salir).pack(pady=20)

    # ======================
    # REGISTRO
    # ======================
    def crear_registro(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text="REGISTRAR PRODUCTO", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.root, text="Nombre").pack()
        entry_nombre = tk.Entry(self.root)
        entry_nombre.pack()

        tk.Label(self.root, text="Prefijos válidos").pack(pady=10)
        tk.Label(
            self.root,
            text="C→Cuadernos | P→Papelería | A→Arte | H→Oficina | E→Escritura | Ñ→Varios"
        ).pack()

        tk.Label(self.root, text="Código (Ej: E011)").pack()
        entry_codigo = tk.Entry(self.root)
        entry_codigo.pack()

        tk.Label(self.root, text="Precio").pack()
        entry_precio = tk.Entry(self.root)
        entry_precio.pack()

        tk.Label(self.root, text="Stock").pack()
        entry_stock = tk.Entry(self.root)
        entry_stock.pack()

        def registrar():
            exito, mensaje = self.inventario.registrar_producto_gui(
                entry_nombre.get(),
                entry_codigo.get(),
                entry_precio.get(),
                entry_stock.get()
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.crear_menu()
            else:
                messagebox.showerror("Error", mensaje)

        tk.Button(self.root, text="Registrar", command=registrar).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.crear_menu).pack()

    # ======================
    # MOSTRAR PRODUCTOS
    # ======================
    def crear_productos(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text="LISTA DE PRODUCTOS", font=("Arial", 18, "bold")).pack(pady=10)

        tree = ttk.Treeview(
            self.root,
            columns=("codigo", "nombre", "precio", "stock"),
            show="headings"
        )

        tree.heading("codigo", text="Código")
        tree.heading("nombre", text="Nombre")
        tree.heading("precio", text="Precio")
        tree.heading("stock", text="Stock")

        for p in self.inventario.obtener_productos():
            tree.insert("", tk.END, values=(
                p["codigo"],
                p["nombre"],
                f"S/. {p['precio']:.2f}",
                p["stock"]
            ))

        tree.pack(fill="both", expand=True)
        tk.Button(self.root, text="Volver", command=self.crear_menu).pack(pady=10)

    # ======================
    # BUSCAR PRODUCTO
    # ======================
    def crear_busqueda(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text="BUSCAR PRODUCTO", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.root, text="Nombre").pack()
        entry = tk.Entry(self.root)
        entry.pack()

        resultado = tk.Label(self.root, text="")
        resultado.pack(pady=20)

        def buscar():
            producto = self.inventario.buscar_producto_gui(entry.get())

            if producto:
                resultado.config(
                    text=f"Código: {producto['codigo']}\n"
                         f"Nombre: {producto['nombre']}\n"
                         f"Precio: S/. {producto['precio']:.2f}\n"
                         f"Stock: {producto['stock']}"
                )
            else:
                resultado.config(text="Producto no encontrado")

        tk.Button(self.root, text="Buscar", command=buscar).pack()
        tk.Button(self.root, text="Volver", command=self.crear_menu).pack(pady=10)

    # ======================
    # VENDER PRODUCTO
    # ======================
    def crear_ventas(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text="REGISTRAR VENTA", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.root, text="Código").pack()
        entry_codigo = tk.Entry(self.root)
        entry_codigo.pack()

        tk.Label(self.root, text="Cantidad").pack()
        entry_cantidad = tk.Entry(self.root)
        entry_cantidad.pack()

        def vender():
            exito, mensaje = self.caja.vender_producto_gui(
                self.inventario,
                entry_codigo.get(),
                entry_cantidad.get()
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.crear_menu()
            else:
                messagebox.showerror("Error", mensaje)

        tk.Button(self.root, text="Vender", command=vender).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.crear_menu).pack()

    # ======================
    # REPORTE
    # ======================
    def crear_reporte(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text="REPORTE DE VENTAS", font=("Arial", 18, "bold")).pack(pady=10)

        tree = ttk.Treeview(
            self.root,
            columns=("codigo", "nombre", "cantidad", "precio", "total"),
            show="headings"
        )

        tree.heading("codigo", text="Código")
        tree.heading("nombre", text="Nombre")
        tree.heading("cantidad", text="Cantidad")
        tree.heading("precio", text="Precio")
        tree.heading("total", text="Total")

        for venta in self.caja.obtener_ventas():
            tree.insert("", tk.END, values=(
                venta["codigo"],
                venta["nombre"],
                venta["cantidad"],
                f"S/. {venta['precio_unitario']:.2f}",
                f"S/. {venta['total']:.2f}"
            ))

        tree.pack(fill="both", expand=True)
        tk.Button(self.root, text="Volver", command=self.crear_menu).pack(pady=10)

    def salir(self):
        self.archivos.guardar_datos(
            self.inventario.productos,
            self.caja.ventas
        )
        self.root.destroy()
