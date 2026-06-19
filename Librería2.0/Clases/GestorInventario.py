import json
import os
import re

class GestorInventario:
    def __init__(self, productos_cargados):
        self.productos = productos_cargados

    def registrar_producto(self):
        print("\nREGISTRO DE PRODUCTO")
        while True:
            nombre = input("Nombre del producto: ").strip()
            if nombre == "" or nombre.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none', 'false', 'true']:
                print("Error: Nombre inválido, vacío o palabra reservada no permitida.")
                continue
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
            codigo = input("Código (Debe ser de 4 caracteres, Ej: C001): ").strip().upper()
            if codigo == "" or codigo.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                print("Error: El código no puede estar vacío ni contener palabras reservadas.")
                continue
            if len(codigo) != 4:
                print("Error: El código debe tener EXACTAMENTE 4 caracteres (Ejemplo: C001).")
                continue
            primera_letra = codigo[0]
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
            
        while True:
            precio_input = input("Precio de venta (S/.): ").strip()
            if precio_input == "" or precio_input.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                print("Error: Entrada inválida.")
                continue
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
            if compra_input == "" or compra_input.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                print("Error: Entrada inválida.")
                continue
            if not re.match(r"^\d+(\.\d{1,2})?$", compra_input):
                print("Error: Formato inválido.")
                continue
            precio_compra = float(compra_input)
            if precio_compra >= precio:
                print("Error: El precio de compra debe ser menor al de venta.")
                continue
            break
            
        while True:
            stock_input = input("Stock Inicial: ").strip()
            if stock_input == "" or stock_input.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                print("Error: Entrada no válida.")
                continue
            try:
                stock = int(stock_input)
                if stock < 0:
                    print("Error: El stock inicial no puede ser negativo.")
                    continue
                break
            except ValueError:
                print("Error: Ingrese un número entero válido para el stock.")
                
        while True:
            stock_min_input = input("Definir Stock Mínimo de Alerta: ").strip()
            if stock_min_input == "" or stock_min_input.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                print("Error: Entrada no válida.")
                continue
            try:
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
            "precio_compra": precio_compra,
            "stock": stock,
            "stock_minimo": stock_minimo  
        }
        self.productos.append(producto)
        print(f"¡Producto '{nombre}' registrado correctamente con el código {codigo}!")

    def mostrar_productos(self):
        if not self.productos:
            print("\nEl inventario esta vacio. Registre productos primero.")
            return
        lista_ordenada = sorted(self.productos, key=lambda x: x['codigo'])
        items_for_pagina = 10
        total_paginas = (len(lista_ordenada) + items_for_pagina - 1) // items_for_pagina
        pagina_actual = 1
        while True:
            inicio = (pagina_actual - 1) * items_for_pagina
            fin = inicio + items_for_pagina
            print("\n==========================================================================")
            print(f"                    CATALOGO - PAGINA {pagina_actual} de {total_paginas}")
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
            if opcion not in opciones:
                print("Error: Opcion invalida.")
                continue
                
            if opcion == 'q':
                break
            elif opcion == 's' and pagina_actual < total_paginas:
                pagina_actual += 1
            elif opcion == 'a' and pagina_actual > 1:
                pagina_actual -= 1

    def buscar_producto(self):
        print("\nBUSCAR PRODUCTO")
        nombre_buscar = input("Ingrese el nombre del producto a buscar: ").strip().lower()
        if nombre_buscar == "" or nombre_buscar in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
            print("Error: Búsqueda inválida.")
            return
            
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