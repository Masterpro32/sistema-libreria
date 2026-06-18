import json
import os
from datetime import datetime

class GestorVentas:
    def __init__(self, ventas_cargadas):
        self.ventas = ventas_cargadas

    def validar_nombre_vendedor(self, prompt):
        while True:
            nombre = input(prompt).strip()
            # Valida solo letras y espacios, mínimo 3 caracteres
            if (nombre.replace(" ", "").isalpha()) and len(nombre) >= 3:
                return nombre
            print("Error: El nombre debe tener mínimo 3 letras y no contener números ni símbolos.")

    def vender_producto(self, inventario):
        print("\n--- REGISTRAR VENTA ---")
        if not inventario.productos:
            print("No hay productos registrados.")
            return
        codigo = input("Ingrese el código del producto (ej. C001): ").strip().upper()
        if len(codigo) != 4 or not (codigo[0].isalpha() and codigo[1:].isdigit()):
            print("Error: El código debe tener 1 letra y 3 números.")
            return
        producto = next((p for p in inventario.productos if p['codigo'] == codigo), None)
        if not producto:
            print("Error: Producto no encontrado.")
            return
        if producto['stock'] <= 0:
            print("Error: El producto está agotado.")
            return
        print(f"Producto: {producto['nombre']} | Stock: {producto['stock']}")  
        while True:
            try:
                cantidad = int(input("Cantidad a vender: "))
                if cantidad <= 0:
                    print("Error: La cantidad debe ser mayor a 0.")
                elif cantidad > producto['stock']:
                    print(f"Error: Stock insuficiente. Disponible: {producto['stock']}")
                else:
                    break
            except ValueError:
                print("Error: Ingrese un número entero válido.")
        # 1. Validar nombre del vendedor
        vendedor = self.validar_nombre_vendedor("Ingrese nombre del vendedor: ")

        # 2. Validar medio de pago
        while True:
            print("\nMedios de pago disponibles: 1. Efectivo, 2. Tarjeta, 3. Yape")
            opcion_pago = input("Seleccione (1-3): ").strip()
            
            if opcion_pago == "1":
                medio_pago = "Efectivo"
                break
            elif opcion_pago == "2":
                medio_pago = "Tarjeta"
                break
            elif opcion_pago == "3":
                # Bucle interno solo para el código de Yape
                while True:
                    codigo_yape = input("Ingrese código de seguridad de 3 dígitos: ").strip()
                    if codigo_yape.isdigit() and len(codigo_yape) == 3:
                        medio_pago = f"Yape (Cod: {codigo_yape})"
                        break # Rompe el bucle de Yape
                    else:
                        print("Error: El código debe ser de exactamente 3 números.")
                break # Rompe el bucle de selección de pago general
            else:
                print("Opción inválida. Por favor, elija 1, 2 o 3.")
        
        stock_anterior = producto['stock']
        producto['stock'] -= cantidad
        stock_nuevo = producto['stock']
        total = cantidad * producto['precio']
        
        venta = {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "vendedor": vendedor,
            "codigo": producto['codigo'],
            "nombre": producto['nombre'],
            "cantidad": cantidad,
            "stock_anterior": stock_anterior,
            "stock_nuevo": stock_nuevo,
            "precio_unitario": producto['precio'],
            "total": total,
            "medio_pago": medio_pago
        }
        
        self.ventas.append(venta)
        print(f"¡Venta realizada! Total: S/. {total:.2f}")
        return True

    def reporte_ventas(self):
        print("\n" + "="*80)
        print(f"{'REPORTE DETALLADO DE VENTAS':^80}")
        print("="*80)
        
        if not self.ventas:
            print("No hay ventas registradas.")
            return
            
        for i, v in enumerate(self.ventas, 1):
            nombre_vendedor = v.get('vendedor', 'N/A')
            pago = v.get('medio_pago', 'No especificado')
            
            print(f"Venta #{i} | {v['fecha']} | Vendedor: {nombre_vendedor}")
            print(f"  Producto: {v['nombre']} (Cod: {v['codigo']})")
            print(f"  Stock: {v['stock_anterior']} -> {v['stock_nuevo']} | Cant: {v['cantidad']}")
            print(f"  Pago: {pago} | Total: S/. {v['total']:.2f}")
            print("-" * 40) 
        total_general = sum(v['total'] for v in self.ventas)
        print(f"\nTOTAL GENERAL ACUMULADO: S/. {total_general:.2f}")
        print("="*80)