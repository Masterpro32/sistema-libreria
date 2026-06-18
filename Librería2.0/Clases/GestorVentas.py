import json
from datetime import datetime
from collections import Counter

class GestorVentas:
    def __init__(self, ventas_cargadas):
        self.ventas = ventas_cargadas

    def validar_nombre_vendedor(self, prompt):
        while True:
            nombre = input(prompt).strip()
            if (nombre.replace(" ", "").isalpha()) and len(nombre) >= 3:
                return nombre
            print("Error: El nombre debe tener mínimo 3 letras y no contener números.")

    def vender_producto(self, inventario):
        print("\n--- REGISTRAR VENTA ---")
        if not inventario.productos:
            print("No hay productos registrados.")
            return

        codigo = input("Ingrese el código del producto: ").strip().upper()
        producto = next((p for p in inventario.productos if p['codigo'] == codigo), None)
        
        if not producto or producto['stock'] <= 0:
            print("Error: Producto no encontrado o sin stock.")
            return

        while True:
            try:
                cantidad = int(input(f"Cantidad a vender (Stock: {producto['stock']}): "))
                if 0 < cantidad <= producto['stock']:
                    break
                print("Error: Cantidad inválida.")
            except ValueError:
                print("Error: Ingrese un número entero.")

        vendedor = self.validar_nombre_vendedor("Nombre del vendedor: ")
        
        precio_c = producto.get('precio_compra', 0)
        total = cantidad * producto['precio']
        utilidad = (producto['precio'] - precio_c) * cantidad
        venta = {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "vendedor": vendedor,
            "codigo": producto['codigo'],
            "nombre": producto['nombre'],
            "cantidad": cantidad,
            "total": total,
            "utilidad": utilidad
        }
        producto['stock'] -= cantidad
        self.ventas.append(venta)
        print(f"¡Venta realizada! Utilidad: S/. {utilidad:.2f}")

    def reporte_ventas(self, inventario):
        if not self.ventas:
            print("\nNo hay ventas registradas.")
            return

        print("\n--- REPORTES DE VENTAS ---")
        print("1. Ver todas las ventas")
        print("2. Filtrar por categoría")
        print("3. Ver producto más vendido")
        op = input("Seleccione una opción: ")

        lista = self.ventas
        if op == "2":
            cats = sorted(list(set(p.get('categoria', 'Sin Categoria') for p in inventario.productos)))
            print("\nCategorías disponibles:")
            for i, cat in enumerate(cats, 1):
                print(f"{i}. {cat}")
            
            sel = input("\nIngrese el número de la categoría: ").strip()
            if sel.isdigit() and 0 < int(sel) <= len(cats):
                cat_elegida = cats[int(sel)-1].lower()
                if cat_elegida == "sin categoria":
                    cods = [p['codigo'] for p in inventario.productos if 'categoria' not in p or not p.get('categoria')]
                else:
                    cods = [p['codigo'] for p in inventario.productos if p.get('categoria', '').lower() == cat_elegida]
                
                lista = [v for v in self.ventas if v.get('codigo') in cods]
            else:
                print("Opción inválida.")
                return
        elif op == "3":
            nombres = [v['nombre'] for v in self.ventas]
            mas_vendido = Counter(nombres).most_common(1)
            if mas_vendido:
                print(f"\nProducto estrella: {mas_vendido[0][0]} ({mas_vendido[0][1]} unidades)")
            return
        elif op != "1":
            print("Opción inválida.")
            return

        print(f"\n{'FECHA':<20} | {'PRODUCTO':<35} | {'CANT.':<6} | {'TOTAL':<11} | {'UTILIDAD':<8}")
        print("-" * 80)
        
        ut_total = 0
        un_total = 0
        for v in lista:
            cant = v.get('cantidad', 0)
            ut = v.get('utilidad', 0)
            un_total += cant
            ut_total += ut
            print(f"{v.get('fecha', 'N/A'):<20} | {v.get('nombre', 'Desconocido'):<35} | {cant:<6} | S/. {v.get('total', 0):<6.2f} | S/. {ut:<6.2f}")
        
        print("-" * 80)
        print(f"TOTAL UNIDADES VENDIDAS: {un_total}")
        print(f"GANANCIA TOTAL (UTILIDAD): S/. {ut_total:.2f}")
        print("=" * 80)