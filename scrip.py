import json
import os
 
productos = []
ventas = []

def registrar_producto():
    
    print("\nREGISTRO DE PRODUCTO")
    nombre = input("Nombre del producto: ")
    if nombre == "":
        print("El nombre no puede estar vacío")
        return
    

    while True:
        try:
            codigo = input("Código: ")
            if codigo == "":
                print("El código no puede estar vacío")
                continue
            repetido = False
        except ValueError:
            print("Ingrese un código válido")
            continue
        for p in productos:
            if p['codigo'] == codigo:
                repetido = True
                break
        if repetido:
            print(" Error: Este código ya existe. Ingresa uno diferente.")
        else:
            break
 

    while True:
        try:
            precio = float(input("Precio: "))
            if precio <= 0:
                print("El precio debe ser mayor a 0")
            else:
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
    productos.append(producto)
    print("Producto registrado correctamente")
 

def mostrar_productos():
    print("\n=== LISTA DE PRODUCTOS (Ordenados) ===")
    if not productos:
        print("  No hay productos registrados")
        return

    lista_ordenada = sorted(productos, key=lambda x: x['codigo'])
    
    items_por_pagina = 10
    total_paginas = (len(lista_ordenada) + items_por_pagina - 1) // items_por_pagina
    
    for pagina_actual in range(1, total_paginas + 1):

        inicio = (pagina_actual - 1) * items_por_pagina
        fin = inicio + items_por_pagina
        pagina_productos = lista_ordenada[inicio:fin]
        
        print(f"\n Página {pagina_actual} de {total_paginas}")
        print(f"{'Código':<10} {'Nombre':<35} {'Stock':<10} {'Precio'}")
        print("-" * 65)
        
        for p in pagina_productos:
            aviso = "  BAJO" if p['stock'] < 50 else ""
            print(f"{p['codigo']:<10} {p['nombre']:<35} {p['stock']:<10} S/. {p['precio']:.2f}{aviso}")
        
        print("-" * 65)
        
        if pagina_actual < total_paginas:
            respuesta = input("Presiona ENTER para siguiente página o 'q' para salir: ").strip().lower()
            if respuesta == 'q':
                print(" Saliendo de la vista de productos.")
                break
        else:
            print("\n Fin de la lista.")
 
def buscar_producto():
    print("\n=== BUSCAR PRODUCTO ===")
    print("Opciones de búsqueda:")
    print("1. Por categoría (prefijo del código: P, H, A, C, E)")
    print("2. Por nombre (palabra clave)")
    
    opcion = input("Seleccione opción (1 ó 2): ").strip()
    
    if opcion == '1':
        prefijo = input("Ingrese el prefijo (Ej: P para Papeles, H para Herramientas): ").strip().upper()
        
        if not prefijo:
            print(" Ingrese un prefijo válido.")
            return

        encontrados = [p for p in productos if p['codigo'].startswith(prefijo)]
        
        if not encontrados:
            print(f"  No se encontraron productos con el prefijo '{prefijo}'.")
            return
            
        print(f"\n Resultados para '{prefijo}':")
        print("-" * 50)
        for p in encontrados:
            print(f"Código: {p['codigo']} | Nombre: {p['nombre']} | Stock: {p['stock']} | S/. {p['precio']:.2f}")
            
    elif opcion == '2':
        nombre_buscar = input("Ingrese parte del nombre: ").strip().lower()
        
        if not nombre_buscar:
            print(" Ingrese un nombre.")
            return

        encontrados = [p for p in productos if nombre_buscar in p['nombre'].lower()]
        
        if not encontrados:
            print("No se encontraron productos con ese nombre.")
            return
            
        print(f"\n Resultados para '{nombre_buscar}':")
        print("-" * 50)
        for p in encontrados:
            print(f"Código: {p['codigo']} | Nombre: {p['nombre']} | Stock: {p['stock']} | S/. {p['precio']:.2f}")
            
    else:
        print("Opción inválida. Volvemos al menú.")
 
 
def vender_producto():
    print("\nREGISTRAR VENTA")
    if len(productos) == 0:
        print("No hay productos disponibles")
        return
 
    codigo = input("Código del producto: ")
    producto_encontrado = None
 
    for producto in productos:
        if producto['codigo'] == codigo:
            producto_encontrado = producto
            break
 
    if producto_encontrado is None:
        print("Producto no encontrado")
        return
 
    print(f"Producto: {producto_encontrado['nombre']} - Stock disponible: {producto_encontrado['stock']}")
 
    while True:
        try:
            cantidad = int(input("Cantidad a vender: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor a 0")
            elif cantidad > producto_encontrado['stock']:
                print(f"Stock insuficiente. Disponible: {producto_encontrado['stock']}")
            else:
                break
        except ValueError:
            print("Ingrese un número válido")
 
    producto_encontrado['stock'] -= cantidad
    total = cantidad * producto_encontrado['precio']
 
    venta = {
        "codigo": producto_encontrado['codigo'],
        "nombre": producto_encontrado['nombre'],
        "cantidad": cantidad,
        "precio_unitario": producto_encontrado['precio'],
        "total": total
    }
    ventas.append(venta)
    print(f"Venta registrada. Total: S/. {total:.2f}")
 
 
def reporte_ventas():
    print("\nREPORTE DE VENTAS")
    if len(ventas) == 0:
        print("No hay ventas registradas")
    else:
        total_general = 0
        for i, venta in enumerate(ventas, 1):
            print(f"\nVenta #{i}")
            print(f"  Código: {venta['codigo']}")
            print(f"  Nombre: {venta['nombre']}")
            print(f"  Cantidad: {venta['cantidad']}")
            print(f"  Precio unitario: S/. {venta['precio_unitario']:.2f}")
            print(f"  Total: S/. {venta['total']:.2f}")
            total_general += venta['total']
        print(f"\nTotal general de ventas: S/. {total_general:.2f}")
 
 
def guardar_archivo():
    datos = {
        "productos": productos,
        "ventas": ventas
    }
    with open("libreria_datos.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("Datos guardados en 'libreria_datos.json'")
 
 
def cargar_archivo():
    global productos, ventas
    if os.path.exists("libreria_datos.json"):
        with open("libreria_datos.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
            productos = datos.get("productos", [])
            ventas = datos.get("ventas", [])
        print("Datos cargados correctamente")
 
 
def menu():
    cargar_archivo()
    while True:
        print("\n===== SISTEMA DE LIBRERÍA =====")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto")
        print("4. Vender producto")
        print("5. Reporte de ventas")
        print("6. Guardar y salir")
 
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Opción inválida")
            continue
 
        if opcion == 1:
            registrar_producto()
        elif opcion == 2:
            mostrar_productos()
        elif opcion == 3:
            buscar_producto()
        elif opcion == 4:
            vender_producto()
        elif opcion == 5:
            reporte_ventas()
        elif opcion == 6:
            guardar_archivo()
            print("Programa finalizado")
            break
        else:
            print("Opción inválida")
 
 
if __name__ == "__main__":
    menu()
