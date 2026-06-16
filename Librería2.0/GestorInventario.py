import json
import os

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
        print("\n=== LISTA DE PRODUCTOS (Ordenados) ===")

        if not self.productos:
            print("No hay productos registrados")
            return

        lista_ordenada = sorted(
            self.productos,
            key=lambda x: x['codigo']
        )

        items_por_pagina = 10
        total_paginas = (len(lista_ordenada) + items_por_pagina - 1) // items_por_pagina
        pagina_actual = 1

        while True:
            inicio = (pagina_actual - 1) * items_por_pagina
            fin = inicio + items_por_pagina

            print(f"\nPágina {pagina_actual} de {total_paginas}")
            print(f"{'Código':<10} {'Nombre':<35} {'Stock':<10} {'Precio'}")
            print("-" * 65)

            for p in lista_ordenada[inicio:fin]:
                aviso = " BAJO" if p['stock'] < 50 else ""

                print(
                    f"{p['codigo']:<10} "
                    f"{p['nombre']:<35} "
                    f"{p['stock']:<10} "
                    f"S/. {p['precio']:.2f}{aviso}"
                )

            print("-" * 65)

            opciones = ['q']
            mensaje = "[q] Salir"

            if pagina_actual < total_paginas:
                opciones.append('s')
                mensaje += " | [s] Siguiente"

            if pagina_actual > 1:
                opciones.append('a')
                mensaje += " | [a] Anterior"

            if pagina_actual == total_paginas:
                opciones.append("")
                mensaje += " | [ENTER] Finalizar"

            respuesta = input(
                f"Opciones: {mensaje} -> "
            ).strip().lower()

            if respuesta not in opciones:
                print("Error: Opción incorrecta. Intente de nuevo.")
                continue

            if respuesta == 'q' or (
                respuesta == "" and pagina_actual == total_paginas
            ):
                break

            elif respuesta == 's':
                pagina_actual += 1

            elif respuesta == 'a':
                pagina_actual -= 1

    def buscar_producto(self):
        print("\nBUSCAR PRODUCTO")
        nombre_buscar = input("Ingrese nombre: ")
        for p in self.productos:
            if p['nombre'].lower() == nombre_buscar.lower():
                print(f"Producto encontrado:\n  Código: {p['codigo']}\n  Nombre: {p['nombre']}\n  Precio: S/. {p['precio']:.2f}\n  Stock: {p['stock']}")
                return
        print("Producto no encontrado")