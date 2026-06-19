import json
import os
import re
from datetime import datetime

class GestorVentas:
    def __init__(self, ventas_cargadas=None):
        self.ventas = ventas_cargadas if ventas_cargadas is not None else []

    def validar_nombre_vendedor(self, mensaje):
        while True:
            nombre = input(mensaje).strip()
            if nombre == "" or nombre.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined']:
                print("Error: Nombre de vendedor no válido.")
                continue
            if len(nombre) < 3 or len(nombre) > 50:
                print("Error: El nombre del vendedor debe tener entre 3 y 50 caracteres.")
                continue
            patron_nombre = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$"
            if not re.fullmatch(patron_nombre, nombre):
                print("Error : El nombre del vendedor solo puede contener letras y espacios. No se permiten números ni símbolos.")
                continue
            return nombre

    def vender_producto(self, inventario):
        try:
            print("\n--- REGISTRAR VENTA MULTIPRODUCTO ---")
            if not inventario.productos:
                print("No hay productos registrados.")
                return

            vendedor = self.validar_nombre_vendedor("Nombre del vendedor: ")
            items_venta = []
            total_boleta = 0
            utilidad_boleta = 0

            while True:
                codigo = input("\nIngrese el código del producto: ").strip().upper()
                if codigo in ['NAN', 'INF', '-INF', 'INFINITY', '']:
                    print("Error: Código no válido.")
                    continue

                producto = next((p for p in inventario.productos if p['codigo'] == codigo), None)
                if not producto:
                    print("Error: Producto no encontrado.")
                elif producto['stock'] <= 0:
                    print(f"Error: El producto {producto['nombre']} no tiene stock disponible.")
                else:
                    while True:
                        entrada_cant = input(f"Cantidad a vender de '{producto['nombre']}' (Stock: {producto['stock']}): ").strip()
                        if entrada_cant.lower() in ['inf', '-inf', 'nan', 'infinity', '']:
                            print("Error: Entrada no válida.")
                            continue
                        try:
                            cantidad = int(entrada_cant)
                            if 0 < cantidad <= producto['stock']:
                                break
                            print("Error: Cantidad inválida o supera el stock.")
                        except ValueError:
                            print("Error: Ingrese un número entero válido.")

                    precio_v = producto['precio']
                    precio_c = producto.get('precio_compra', 0)
                    subtotal = quantity = cantidad * precio_v
                    subutilidad = (precio_v - precio_c) * cantidad

                    producto['stock'] -= cantidad

                    items_venta.append({
                        "codigo": producto['codigo'],
                        "nombre": producto['nombre'],
                        "cantidad": cantidad,
                        "subtotal": subtotal,
                        "subutilidad": subutilidad
                    })

                    total_boleta += subtotal
                    utilidad_boleta += subutilidad
                    print(f"-> Agregado: {producto['nombre']} x{cantidad} (S/. {subtotal:.2f})")

                while True:
                    continuar = input("\n¿Deseas agregar otro producto a esta misma venta? (s/n): ").strip().lower()
                    if continuar in ['s', 'n']:
                        break
                    print("Error: Opción inválida. Ingrese únicamente 's' para Sí o 'n' para No.")
                if continuar == 'n':
                    break

            if items_venta:
                print(f"\n=========================================")
                print(f" TOTAL A PAGAR POR EL CLIENTE: S/. {total_boleta:.2f}")
                print(f"=========================================")
                
                while True:
                    print("\nMétodo de pago: 1. Efectivo | 2. Yape | 3. Tarjeta")
                    op_pago = input("Seleccione una opción (1-3): ").strip()
                    if op_pago in ['1', '2', '3']:
                        break
                    print("Error: Opción inválida. Debe seleccionar 1, 2 o 3.")

                metodo_pago = "Efectivo"
                cod_pago = ""
                
                if op_pago == "2":
                    metodo_pago = "Yape"
                    while True:
                        cod_pago = input("Ingrese código de seguridad Yape (Exactamente 3 números): ").strip()
                        if cod_pago.isdigit() and len(cod_pago) == 3:
                            break
                        print("Error: El código de Yape debe tener exactamente 3 dígitos numéricos (Ejemplo: 457).")
                elif op_pago == "3":
                    metodo_pago = "Tarjeta"
                    cod_pago = ""

                nueva_venta = {
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "vendedor": vendedor,
                    "pago": metodo_pago,
                    "codigo_pago": cod_pago,
                    "productos_detalles": items_venta, 
                    "total": total_boleta,
                    "utilidad": utilidad_boleta
                }
                
                nueva_venta["codigo"] = items_venta[0]["codigo"]
                nueva_venta["nombre"] = items_venta[0]["nombre"] if len(items_venta) == 1 else f"{items_venta[0]['nombre']} y otros..."
                nueva_venta["cantidad"] = sum(item["cantidad"] for item in items_venta)

                self.ventas.append(nueva_venta)
                
                try:
                    ruta_clases = os.path.dirname(os.path.abspath(__file__))
                    ruta_libreria = os.path.dirname(ruta_clases)
                    ruta_json = os.path.join(ruta_libreria, "libreria_datos.json")

                    with open(ruta_json, "w", encoding="utf-8") as f:
                        datos_a_guardar = {
                            "productos": inventario.productos,
                            "ventas": self.ventas
                        }
                        json.dump(datos_a_guardar, f, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"\nError crítico al auto-guardar el archivo: {e}")

                print(f"¡Venta registrada con éxito! Total Boleta: S/. {total_boleta:.2f}")
            else:
                print("\nVenta cancelada (No se agregaron productos).")

        except KeyboardInterrupt:
            print("\n\n[PROCESO INTERRUMPIDO] Se presionó Ctrl + C. La venta actual fue cancelada y el stock no se afectará.")
            if 'items_venta' in locals() and items_venta:
                for item in items_venta:
                    prod = next((p for p in inventario.productos if p['codigo'] == item['codigo']), None)
                    if prod:
                        prod['stock'] += item['cantidad']
                print("-> El stock retenido ha sido devuelto al inventario con éxito.")

    def reporte_ventas(self, inventario):
        if not self.ventas:
            print("\nNo hay ventas registradas.")
            return

        while True:
            print("\n--- REPORTES DE VENTAS ---")
            print("1. Ver todas las ventas")
            print("2. Filtrar por categoría")
            print("3. Ver producto más vendido")
            print("4. Ver detalle de una venta específica")
            op = input("Seleccione una opción (1-4): ").strip()
            if op in ['1', '2', '3', '4']:
                break
            print("Error: Opción inválida. Seleccione un número entre 1 y 4.")

        lista = self.ventas
        
        if op == "2":
            cats = ["Cuadernos", "Papelería", "Arte y Manualidades", "Herramientas de Oficina", "Escritura", "Varios"]
            print("\nCategorías disponibles:")
            for i, cat in enumerate(cats, 1):
                print(f"{i}. {cat}")
            
            while True:
                sel = input("\nIngrese el número de la categoría: ").strip()
                if sel.lower() in ['inf', '-inf', 'nan', 'infinity', '']:
                    print("Error: Entrada inválida.")
                    continue
                if sel.isdigit() and 0 < int(sel) <= len(cats):
                    break
                print(f"Error: Debe ingresar un número entre 1 y {len(cats)}.")

            cat_elegida = cats[int(sel)-1].lower()
            cods = [p['codigo'] for p in inventario.productos if p.get('categoria', '').lower() == cat_elegida]
            
            lista = []
            for v in self.ventas:
                incluye_producto = False
                if "productos_detalles" in v:
                    for item in v["productos_detalles"]:
                        if item.get('codigo') in cods:
                            incluye_producto = True
                            break
                else:
                    if v.get('codigo') in cods:
                        incluye_producto = True
                if incluye_producto:
                    lista.append(v)
            
        elif op == "3":
            conteo_unidades = {}
            for v in self.ventas:
                if "productos_detalles" in v:
                    for item in v["productos_detalles"]:
                        n = item.get('nombre', 'Desconocido')
                        conteo_unidades[n] = conteo_unidades.get(n, 0) + item.get('cantidad', 0)
                else:
                    nombre = v.get('nombre', 'Desconocido')
                    cant = v.get('cantidad', 0)
                    conteo_unidades[nombre] = conteo_unidades.get(nombre, 0) + cant
            
            if conteo_unidades:
                producto_estrella = max(conteo_unidades, key=conteo_unidades.get)
                unidades_totales = conteo_unidades[producto_estrella]
                
                print("\n==================================================")
                print(f"PRODUCTO MÁS VENDIDO")
                print(f"Producto: {producto_estrella}")
                print(f"Total de unidades despachadas: {unidades_totales} uds.")
                print("==================================================")
            else:
                print("\nNo hay registros suficientes para calcular el más vendido.")
            return

        elif op == "4":
            while True:
                num_ingresado = input(f"\nIngrese el número de la venta que desea detallar (1-{len(self.ventas)}): ").strip()
                if num_ingresado.isdigit() and 0 < int(num_ingresado) <= len(self.ventas):
                    break
                print(f"Error: Ingrese un número válido en el rango de 1 a {len(self.ventas)}.")
            
            venta_sel = self.ventas[int(num_ingresado) - 1]
            
            print("\n==========================================================")
            print(f"DETALLE DE LA VENTA N° {num_ingresado}")
            print("==========================================================")
            print(f"Fecha/Hora:  {venta_sel.get('fecha', 'N/A')}")
            print(f"Vendedor:    {venta_sel.get('vendedor', 'N/A')}")
            print(f"Método Pago: {venta_sel.get('pago', 'Efectivo')} {f'({venta_sel.get('codigo_pago')})' if venta_sel.get('codigo_pago') else ''}")
            print("----------------------------------------------------------")
            print(f"{'COD.':<6} | {'PRODUCTO':<30} | {'CANT.':<5} | {'SUBTOTAL':<9}")
            print("----------------------------------------------------------")
            
            if "productos_detalles" in venta_sel:
                for item in venta_sel["productos_detalles"]:
                    print(f"{item.get('codigo', 'N/A'):<6} | {item.get('nombre', 'Desconocido'):<30} | {item.get('cantidad', 0):<5} | S/. {item.get('subtotal', 0):<5.2f}")
            else:
                print(f"{venta_sel.get('codigo', 'N/A'):<6} | {venta_sel.get('nombre', 'Desconocido'):<30} | {venta_sel.get('cantidad', 0):<5} | S/. {venta_sel.get('total', 0):<5.2f}")
                
            print("----------------------------------------------------------")
            print(f"TOTAL COMPRA:                               S/. {venta_sel.get('total', 0):.2f}")
            print(f"UTILIDAD:                                   S/. {venta_sel.get('utilidad', 0):.2f}")
            print("==========================================================")
            return

        print(f"\n{'N° VENTA':<9} | {'FECHA':<20} | {'COD.':<6} | {'PRODUCTO':<25} | {'CATEGORÍA':<18} | {'STOCK':<11} | {'CANT.':<5} | {'PAGO':<15} | {'TOTAL':<9} | {'UTILIDAD':<9}")
        print("-" * 163)
        
        ut_total = 0
        un_total = 0
        
        for num_v, v in enumerate(lista, 1):
            cant = v.get('cantidad', 0)
            un_total += cant
            
            ut = v.get('utilidad', 0)
            prod = next((p for p in inventario.productos if p['codigo'] == v['codigo']), None)
            if ut == 0 and prod:
                precio_c = prod.get('precio_compra', 0)
                precio_v = prod.get('precio', 0)
                if precio_v == 0 and cant > 0:
                    precio_v = v.get('total', 0) / cant
                ut = (precio_v - precio_c) * cant
                ut = max(0, ut)
            ut_total += ut
            
            stock_actual = prod.get('stock', 0) if prod else 0
            stock_inicial = stock_actual + cant
            str_stock = f"{stock_inicial}->{stock_actual}"
            
            metodo = v.get('pago', 'Efectivo')
            cod_pago = v.get('codigo_pago', v.get('Cod', ''))
            pago_formateado = f"{metodo} ({cod_pago})" if cod_pago and str(cod_pago).lower() != 'nan' and str(cod_pago).strip() else metodo

            nombre = v.get('nombre', 'Desconocido')
            if len(nombre) > 23:
                nombre = nombre[:20] + "..."
                
            categoria = prod.get('categoria', 'Sin Categoría') if prod else 'Sin Categoría'
            if len(categoria) > 16:
                categoria = categoria[:14] + ".."
                
            if len(pago_formateado) > 14:
                pago_formateado = pago_formateado[:12] + ".."

            texto_venta = f"Venta {num_v}"

            print(f"{texto_venta:<9} | {v.get('fecha', 'N/A'):<20} | {v.get('codigo', 'N/A'):<6} | {nombre:<25} | {categoria:<18} | {str_stock:<11} | {cant:<5} | {pago_formateado:<15} | S/. {v.get('total', 0):<5.2f} | S/. {ut:<5.2f}")
        
        print("-" * 163)
        print(f"TOTAL UNIDADES VENDIDAS: {un_total}")
        print(f"GANANCIA TOTAL (UTILIDAD): S/. {ut_total:.2f}")
        print("=" * 163)