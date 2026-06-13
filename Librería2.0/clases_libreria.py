import json
import os

class GestorArchivos:
    def __init__(self, nombre_archivo="libreria_datos.json"):
        self.archivo = nombre_archivo

    def cargar_datos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                # Retorna los productos y ventas (o listas vacías si no existen)
                return datos.get("productos", []), datos.get("ventas", [])
        return [], []

    def guardar_datos(self, productos, ventas):
        datos = {
            "productos": productos,
            "ventas": ventas
        }
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        print(f"Datos guardados en '{self.archivo}'")


class GestorInventario:
    def __init__(self, productos_cargados):
        self.productos = productos_cargados

    def registrar_producto(self):
        print("\nREGISTRO DE PRODUCTO")

        nombre = input("Nombre del producto: ").strip()

        if nombre == "":
            print("El nombre no puede estar vacío")
            return

        prefijos_validos = {
            'C': 'Cuadernos',
            'P': 'Papelería',
            'A': 'Arte y Manualidades',
            'H': 'Herramientas de Oficina',
            'E': 'Escritura',
            'Ñ': 'Varios'
        }

        while True:
            print("\n--- Prefijos permitidos y su significado ---")

            for letra, significado in prefijos_validos.items():
                print(f"  {letra} -> {significado}")

            print("--------------------------------------------")

            codigo = input(
                "Código (Ej: E011, C009): "
            ).strip().upper()

            if codigo == "":
                print("El código no puede estar vacío")
                continue

            primera_letra = codigo[0]

            if primera_letra not in prefijos_validos:
                print(
                    f"\nError: El prefijo '{primera_letra}' no es válido."
                )
                continue

            if len(codigo) < 2 or not codigo[1:].isdigit():
                print(
                    "Error: El código debe tener una letra seguida de números (Ej: E011)"
                )
                continue

            repetido = any(
                p['codigo'] == codigo
                for p in self.productos
            )

            if repetido:
                print("Error: Este código ya existe.")
                continue

            break

        while True:
            try:
                precio_input = input("Precio: ").strip()
                precio = float(precio_input)

                if precio <= 0:
                    print("El precio debe ser mayor a 0")
                    continue

                if "." in precio_input:
                    decimales = precio_input.split(".")[1]

                    if len(decimales) > 2:
                        print(
                            "Error: El precio solo puede tener máximo 2 decimales"
                        )
                        continue

                break

            except ValueError:
                print("Ingrese un número válido")

        while True:
            try:
                stock = int(input("Stock: "))

                if stock < 0:
                    print("El stock no puede ser negativo")
                else:
                    break

            except ValueError:
                print("Ingrese un número válido")

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "stock": stock
        }

        self.productos.append(producto)

        print(f"¡Producto '{nombre}' registrado correctamente con el código {codigo}!")
    def mostrar_productos(self):
        print("\nLISTA DE PRODUCTOS")
        if not self.productos:
            print("No hay productos registrados")
            return
        
        for p in self.productos:
            print("---------------------")
            print(f"Código: {p['codigo']}\nNombre: {p['nombre']}\nPrecio: S/. {p['precio']:.2f}\nStock: {p['stock']}")
        print("---------------------")

    def buscar_producto(self):
        print("\nBUSCAR PRODUCTO")
        nombre_buscar = input("Ingrese nombre: ")
        for p in self.productos:
            if p['nombre'].lower() == nombre_buscar.lower():
                print(f"Producto encontrado:\n  Código: {p['codigo']}\n  Nombre: {p['nombre']}\n  Precio: S/. {p['precio']:.2f}\n  Stock: {p['stock']}")
                return
        print("Producto no encontrado")


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
