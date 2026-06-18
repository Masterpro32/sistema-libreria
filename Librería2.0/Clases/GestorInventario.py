import json
import os

class GestorInventario:
    def __init__(self, productos_cargados):
        self.productos = productos_cargados

    def registrar_producto(self):
        print("\nREGISTRO DE PRODUCTO")
        while True:
            nombre = input("Nombre del producto: ").strip()
            if len(nombre) < 3 or len(nombre) > 60:
                print("Error: El nombre debe tener entre 3 y 60 caracteres.")
                continue
            if nombre.isdigit():
                print("Error: El nombre no puede ser solo números.")
                continue
            if all(not c.isalnum() and not c.isspace() for c in nombre):
                print("Error: El nombre no puede contener solo símbolos.")
                continue
            if any(p['nombre'].lower() == nombre.lower() for p in self.productos):
                print("Error: Ya existe un producto con este mismo nombre.")
                continue
            break
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
            codigo = input("Código (Debe ser de 4 caracteres, Ej: C001): ").strip()
            if codigo == "":
                print("El código no puede estar vacío")
                continue
            if len(codigo) != 4:
                print("Error: El código debe tener EXACTAMENTE 4 caracteres (Ejemplo: C001).")
                continue
            primera_letra = codigo[0]
            if not primera_letra.isupper():
                print("Error: La primera letra debe ser MAYÚSCULA obligatoriamente (Ejemplo: C001).")
                continue
            if primera_letra not in prefijos_validos:
                print(f"Error: El prefijo '{primera_letra}' no es válido.")
                continue
            if not codigo[1:].isdigit():
                print("Error: Después de la letra deben seguir exactamente 3 números (Ejemplo: C001).")
                continue
            repetido = any(p['codigo'] == codigo for p in self.productos)
            if repetido:
                print("Error: Este código ya existe.")
                continue
            categoria = prefijos_validos[primera_letra]
            break
        import re
        while True:
            precio_input = input("Precio de venta (S/.): ").strip()
            patron_precio = r"^\d+(\.\d{1,2})?$"
            if not re.match(patron_precio, precio_input):
                print("Error: Formato inválido. Ingrese solo números positivos con máximo 2 decimales (Ej: 5.50).")
                continue
            precio = float(precio_input)
            if precio == 0:
                print("Error: El precio debe ser mayor a 0.")
                continue
            break
        while True:
            compra_input = input("Precio de compra (S/.): ").strip()
            if not re.match(r"^\d+(\.\d{1,2})?$", compra_input):
                print("Formato inválido.")
                continue
            precio_compra = float(compra_input)
            if precio_compra >= precio:
                print("Error: El precio de compra debe ser menor al de venta.")
                continue
            break
        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "precio_compra": precio_compra, # NUEVO CAMPO
            "stock": stock,
            "stock_minimo": stock_minimo  
        }
        while True:
            try:
                stock_input = input("Stock Inicial: ").strip()
                stock = int(stock_input)
                if stock < 0:
                    print("Error: El stock inicial no puede ser negativo.")
                    continue
                break
            except ValueError:
                print("Error: Ingrese un número entero válido para el stock.")
        while True:
            try:
                stock_min_input = input("Definir Stock Mínimo de Alerta: ").strip()
                stock_minimo = int(stock_min_input)
                if stock_minimo < 1:
                    print("Error: El stock mínimo de alerta debe ser de al menos 1 unidad.")
                    continue
                break
            except ValueError:
                print("Error: Ingrese un número entero válido para el stock mínimo.")
        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "stock": stock,
            "stock_minimo": stock_minimo  
        }
        self.productos.append(producto)
        print(f"¡Producto '{nombre}' registrado correctamente con el código {codigo}!")

    def mostrar_productos(self):
        if not self.productos:
            print("\nEl inventario esta vacio. Registre productos primero.")
            return
        lista_ordenada = sorted(
            self.productos,
            key=lambda x: x['codigo']
        )
        items_for_pagina = 10
        total_paginas = (len(lista_ordenada) + items_for_pagina - 1) // items_for_pagina
        pagina_actual = 1
        while True:
            inicio = (pagina_actual - 1) * items_for_pagina
            fin = inicio + items_for_pagina
            print("\n==========================================================================")
            print(f"                       CATALOGO - PAGINA {pagina_actual} de {total_paginas}")
            print("==========================================================================")
            print(f"{'CODIGO':<8} | {'NOMBRE':<35} | {'PRECIO':<10} | {'STOCK':<8} | {'ESTADO'}")
            print("-" * 74)
            productos_pagina = lista_ordenada[inicio:fin]
            for p in productos_pagina:
                codigo = p['codigo']
                nombre = p['nombre']
                precio = f"S/. {p['precio']:.2f}"
                stock = p['stock']
                stock_min = p.get('stock_minimo', 1)
                if stock == 0:
                    estado = "[SIN STOCK]"
                elif stock <= stock_min:
                    estado = f"[BAJO STOCK] (Min: {stock_min})"
                else:
                    estado = "[OK]"
                print(f"{codigo:<8} | {nombre:<35} | {precio:<10} | {stock:<8} | {estado}")
            print("==========================================================================")
            opciones = ['q']
            mensaje = "[q] Salir"
            if pagina_actual < total_paginas:
                opciones.append('s')
                mensaje += " | [s] Siguiente"
            if pagina_actual > 1:
                opciones.append('a')
                mensaje += " | [a] Anterior"
            opcion = input(f"Opciones: {mensaje} -> ").strip().lower()
            if opcion == 'q':
                break
            elif opcion == 's' and pagina_actual < total_paginas:
                pagina_actual += 1
            elif opcion == 'a' and pagina_actual > 1:
                pagina_actual -= 1
            else:
                print("Opcion invalida.")

    def buscar_producto(self):
        print("\nBUSCAR PRODUCTO")
        nombre_buscar = input("Ingrese el nombre del producto a buscar: ").strip().lower()
        encontrados = False
        for p in self.productos:
            if nombre_buscar in p['nombre'].lower():
                stock_min = p.get('stock_minimo', 1)
                if p['stock'] == 0:
                    estado = "[SIN STOCK]"
                elif p['stock'] <= stock_min:
                    estado = "[BAJO STOCK]"
                else:
                    estado = "[OK]"
                print(f"\nProducto Encontrado:")
                print(f"Codigo: {p['codigo']}")
                print(f"Nombre: {p['nombre']}")
                print(f"Categoria: {p.get('categoria', 'Sin Categoria')}")
                print(f"Precio: S/. {p['precio']:.2f}")
                print(f"Stock Actual: {p['stock']} {estado}")
                encontrados = True
        if not encontrados:
            print("No se encontraron productos con ese nombre.")

    def buscar_producto(self):
        print("\nBUSCAR PRODUCTO")
        nombre_buscar = input("Ingrese el nombre del producto a buscar: ").strip().lower()
        encontrados = False
        for p in self.productos:
            if nombre_buscar in p['nombre'].lower():
                stock_min = p.get('stock_minimo', 1)
                if p['stock'] == 0:
                    estado = "[SIN STOCK]"
                elif p['stock'] <= stock_min:
                    estado = "[BAJO STOCK]"
                else:
                    estado = "[OK]" 
                print(f"\nProducto Encontrado:")
                print(f"Codigo: {p['codigo']}")
                print(f"Nombre: {p['nombre']}")
                print(f"Categoria: {p.get('categoria', 'Sin Categoria')}")
                print(f"Precio: S/. {p['precio']:.2f}")
                print(f"Stock Actual: {p['stock']} {estado}")
                encontrados = True     
        if not encontrados:
            print("No se encontraron productos con ese nombre.")
            
    def reponer_stock(self):
        print("\n--- REPONER STOCK ---")
        if not self.productos:
            print("El inventario está vacío. Registre productos primero.")
            return

        codigo = input("Ingrese el código del producto a reponer: ").strip().upper()
        
        # Buscamos el producto
        producto = next((p for p in self.productos if p['codigo'] == codigo), None)
        
        if not producto:
            print("Error: No se encontró ningún producto con ese código.")
            return
            
        print(f"\nProducto encontrado: {producto['nombre']}")
        print(f"Stock actual: {producto['stock']}")
        
        while True:
            try:
                cantidad = int(input("Ingrese la cantidad a añadir al inventario: "))
                if cantidad > 0:
                    producto['stock'] += cantidad
                    print(f"¡Éxito! El nuevo stock de '{producto['nombre']}' es de {producto['stock']} unidades.")
                    break
                else:
                    print("Error: La cantidad a reponer debe ser mayor a 0.")
            except ValueError:
                print("Error: Por favor, ingrese un número entero válido.")
