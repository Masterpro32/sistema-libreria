import json
import os

class GestorArchivos:
    def __init__(self, nombre_archivo="libreria_datos.json"):
        # Localiza la carpeta exacta donde vive este script y amarra el JSON ahí
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        self.archivo = os.path.join(carpeta_actual, nombre_archivo)

    def cargar_datos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("productos", []), datos.get("ventas", [])
        return [], []

    def guardar_datos(self, productos, ventas):
        datos = {
            "productos": productos,
            "ventas": ventas
        }
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        print(f"Datos guardados correctamente.")


class GestorInventario:
    def __init__(self, productos_cargados):
        self.productos = productos_cargados
        self.categorias_base = {
            'C': 'Cuadernos',
            'P': 'Papelería',
            'A': 'Arte y Manualidades',
            'H': 'Herramientas de Oficina',
            'E': 'Escritura'
        }

    def obtener_prefijos_actuales(self):
        prefijos = self.categorias_base.copy()
        for p in self.productos:
            if p.get('codigo'):
                letra = p['codigo'][0].upper()
                if letra not in prefijos:
                    prefijos[letra] = f"Categoría {letra}"
        return prefijos

    def registrar_producto(self):
        print("\n=== REGISTRO DE PRODUCTO ===")
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            return

        while True:
            prefijos_validos = self.obtener_prefijos_actuales()
            print("\nPrefijos válidos:")
            for letra, significado in sorted(prefijos_validos.items()):
                print(f"  {letra} -> {significado}")
            
            codigo = input("\nCódigo (Ej: E011): ").strip().upper()
            if not codigo:
                print("El código no puede estar vacío.")
                continue

            primera_letra = codigo[0]
            if primera_letra not in prefijos_validos:
                print(f"Se detectó un prefijo nuevo: '{primera_letra}'")
                nombre_cat = input(f"Nombre para la categoría '{primera_letra}': ").strip()
                self.categorias_base[primera_letra] = nombre_cat if nombre_cat else f"Categoría {primera_letra}"

            if len(codigo) < 2 or not codigo[1:].isdigit():
                print("Error: Debe ser una letra seguida de números.")
                continue

            if any(p['codigo'] == codigo for p in self.productos):
                print("Error: Este código ya existe.")
                continue
            break

        while True:
            try:
                precio = float(input("Precio: S/. "))
                if precio <= 0:
                    print("El precio debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("Ingrese un número válido.")

        while True:
            try:
                stock = int(input("Stock: "))
                if stock < 0:
                    print("El stock no puede ser negativo.")
                    continue
                break
            except ValueError:
                print("Ingrese un número entero válido.")

        self.productos.append({
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "stock": stock
        })
        print(f"¡{nombre} registrado con éxito!")

    def mostrar_productos(self):
        print("\n=== INVENTARIO DE PRODUCTOS ===")
        if not self.productos:
            print("No hay productos registrados.")
            return

        lista_ordenada = sorted(self.productos, key=lambda x: x['codigo'])
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
                aviso = " (BAJO)" if p['stock'] < 50 else ""
                print(f"{p['codigo']:<10} {p['nombre']:<35} {p['stock']:<10} S/. {p['precio']:.2f}{aviso}")

            print("-" * 65)
            mensaje = "[q] Salir"
            opciones = ['q']

            if pagina_actual < total_paginas:
                opciones.append('s')
                mensaje += " | [s] Siguiente"
            if pagina_actual > 1:
                opciones.append('a')
                mensaje += " | [a] Anterior"

            respuesta = input(f"Opciones: {mensaje} -> ").strip().lower()
            if respuesta == 'q':
                break
            elif respuesta == 's' and 's' in opciones:
                pagina_actual += 1
            elif respuesta == 'a' and 'a' in opciones:
                pagina_actual -= 1

    def buscar_producto(self):
        print("\n=== BUSCAR PRODUCTO ===")
        print("1. Por nombre")
        print("2. Por categoría (Letra)")
        op = input("Opción: ").strip()

        if op == '1':
            txt = input("Texto a buscar: ").strip().lower()
            encontrados = [p for p in self.productos if txt in p['nombre'].lower()]
            if not encontrados:
                print("No se encontraron coincidencias.")
                return
            for p in encontrados:
                print(f"[{p['codigo']}] {p['nombre']} - Stock: {p['stock']} - S/. {p['precio']:.2f}")
        elif op == '2':
            letra = input("Letra de la categoría: ").strip().upper()
            encontrados = [p for p in self.productos if p['codigo'].startswith(letra)]
            if not encontrados:
                print(f"No hay productos con el prefijo {letra}")
                return
            for p in encontrados:
                print(f"[{p['codigo']}] {p['nombre']} - Stock: {p['stock']} - S/. {p['precio']:.2f}")


class GestorVentas:
    def __init__(self, ventas_cargadas):
        self.ventas = ventas_cargadas

    def registrar_venta(self, inventario):
        print("\n=== REGISTRAR VENTA ===")
        codigo = input("Código del producto a vender: ").strip().upper()
        prod = next((p for p in inventario if p['codigo'] == codigo), None)
        
        if not prod:
            print("Producto no encontrado.")
            return

        try:
            cant = int(input(f"Cantidad (Disponible: {prod['stock']}): "))
            if cant <= 0 or cant > prod['stock']:
                print("Cantidad inválida o stock insuficiente.")
                return
        except ValueError:
            print("Número inválido.")
            return

        prod['stock'] -= cant
        total = cant * prod['precio']
        self.ventas.append({
            "codigo": codigo,
            "nombre": prod['nombre'],
            "cantidad": cant,
            "total": total
        })
        print(f"Venta realizada. Total: S/. {total:.2f}")

    def mostrar_reporte(self):
        print("\n=== REPORTE DE VENTAS ===")
        if not self.ventas:
            print("No se han realizado ventas.")
            return
        total_general = 0
        for v in self.ventas:
            print(f"Prod: {v['nombre']} | Cant: {v['cantidad']} | Total: S/. {v['total']:.2f}")
            total_general += v['total']
        print(f"Total Recaudado: S/. {total_general:.2f}")