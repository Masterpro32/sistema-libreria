import json
import os
 
productos = []
ventas = []
 
 
def registrar_producto():
    print("\nREGISTRO DE PRODUCTO")
    while True:
        codigo = input("Código: ")
        repetido = False
        for p in productos:
            if p['codigo'] == codigo:
                repetido = True
                break
        
        if repetido:
            print(" Error: Este código ya existe. Ingresa uno diferente.")
        else:
            break
    nombre = input("Nombre del producto: ")
 
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
    print("\nLISTA DE PRODUCTOS")
    if len(productos) == 0:
        print("No hay productos registrados")
    else:
        for producto in productos:
            print("---------------------")
            print(f"Código: {producto['codigo']}")
            print(f"Nombre: {producto['nombre']}")
            print(f"Precio: S/. {producto['precio']:.2f}")
            print(f"Stock: {producto['stock']}")
    print("---------------------")
 
 
def buscar_producto():
    print("\nBUSCAR PRODUCTO")
    nombre_buscar = input("Ingrese nombre: ")
    encontrado = False
    for producto in productos:
        if producto['nombre'].lower() == nombre_buscar.lower():
            print("Producto encontrado:")
            print(f"  Código: {producto['codigo']}")
            print(f"  Nombre: {producto['nombre']}")
            print(f"  Precio: S/. {producto['precio']:.2f}")
            print(f"  Stock: {producto['stock']}")
            encontrado = True
    if not encontrado:
        print("Producto no encontrado")
 
 
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
 
