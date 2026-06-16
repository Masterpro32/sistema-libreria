import json
import os

class GestorVentas:
    def __init__(self, ventas_cargadas):
        self.ventas = ventas_cargadas

    # Le pasamos el objeto 'inventario' para que GestorVentas pueda modificar el stock
    def vender_producto(self, inventario):
        print("\nREGISTRAR VENTA")
        if not inventario.productos:
            print("No hay productos disponibles")
            return

        codigo = input("Código del producto: ")
        producto_encontrado = next((p for p in inventario.productos if p['codigo'] == codigo), None)

        if not producto_encontrado:
            print("Producto no encontrado")
            return

        print(f"Producto: {producto_encontrado['nombre']} - Stock disponible: {producto_encontrado['stock']}")

        while True:
            try:
                cantidad = int(input("Cantidad a vender: "))
                if cantidad <= 0: print("La cantidad debe ser mayor a 0")
                elif cantidad > producto_encontrado['stock']: print(f"Stock insuficiente. Disponible: {producto_encontrado['stock']}")
                else: break
            except ValueError:
                print("Ingrese un número válido")

        # Modificamos el stock en el inventario
        producto_encontrado['stock'] -= cantidad
        total = cantidad * producto_encontrado['precio']

        venta = {
            "codigo": producto_encontrado['codigo'],
            "nombre": producto_encontrado['nombre'],
            "cantidad": cantidad,
            "precio_unitario": producto_encontrado['precio'],
            "total": total
        }
        self.ventas.append(venta)
        print(f"Venta registrada. Total: S/. {total:.2f}")

    def reporte_ventas(self):
        print("\nREPORTE DE VENTAS")
        if not self.ventas:
            print("No hay ventas registradas")
            return
            
        total_general = sum(v['total'] for v in self.ventas)
        for i, v in enumerate(self.ventas, 1):
            print(f"\nVenta #{i}\n  Código: {v['codigo']}\n  Nombre: {v['nombre']}\n  Cantidad: {v['cantidad']}\n  Precio: S/. {v['precio_unitario']:.2f}\n  Total: S/. {v['total']:.2f}")
        print(f"\nTotal general de ventas: S/. {total_general:.2f}")
