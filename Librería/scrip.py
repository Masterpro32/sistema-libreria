# Sistema de Librería
import json
import os
 
libros = []
ventas = []
 
 
def registrar_libro():
    print("\nREGISTRO DE LIBROS")
    codigo = input("Código: ")
    nombre = input("Nombre del libro: ")
 
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
 
    libro = {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "stock": stock
    }
    libros.append(libro)
    print("Libro registrado correctamente")
 
 
def mostrar_libros():
    print("\nLISTA DE LIBROS")
    if len(libros) == 0:
        print("No hay libros registrados")
    else:
        for libro in libros:
            print("---------------------")
            print(f"Código: {libro['codigo']}")
            print(f"Nombre: {libro['nombre']}")
            print(f"Precio: S/. {libro['precio']:.2f}")
            print(f"Stock: {libro['stock']}")
    print("---------------------")
 
 
def buscar_libro():
    print("\nBUSCAR LIBRO")
    nombre_buscar = input("Ingrese nombre: ")
    encontrado = False
    for libro in libros:
        if libro['nombre'].lower() == nombre_buscar.lower():
            print("Libro encontrado:")
            print(f"  Código: {libro['codigo']}")
            print(f"  Nombre: {libro['nombre']}")
            print(f"  Precio: S/. {libro['precio']:.2f}")
            print(f"  Stock: {libro['stock']}")
            encontrado = True
    if not encontrado:
        print("Libro no encontrado")
 
 
def vender_libro():
    print("\nREGISTRAR VENTA")
    if len(libros) == 0:
        print("No hay libros disponibles")
        return
 
    codigo = input("Código del libro: ")
    libro_encontrado = None
 
    for libro in libros:
        if libro['codigo'] == codigo:
            libro_encontrado = libro
            break
 
    if libro_encontrado is None:
        print("Libro no encontrado")
        return
 
    print(f"Libro: {libro_encontrado['nombre']} - Stock disponible: {libro_encontrado['stock']}")
 
    while True:
        try:
            cantidad = int(input("Cantidad a vender: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor a 0")
            elif cantidad > libro_encontrado['stock']:
                print(f"Stock insuficiente. Disponible: {libro_encontrado['stock']}")
            else:
                break
        except ValueError:
            print("Ingrese un número válido")
 
    libro_encontrado['stock'] -= cantidad
    total = cantidad * libro_encontrado['precio']
 
    venta = {
        "codigo": libro_encontrado['codigo'],
        "nombre": libro_encontrado['nombre'],
        "cantidad": cantidad,
        "precio_unitario": libro_encontrado['precio'],
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
        "libros": libros,
        "ventas": ventas
    }
    with open("libreria_datos.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("Datos guardados en 'libreria_datos.json'")
 
 
def cargar_archivo():
    global libros, ventas
    if os.path.exists("libreria_datos.json"):
        with open("libreria_datos.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
            libros = datos.get("libros", [])
            ventas = datos.get("ventas", [])
        print("Datos cargados correctamente")
 
 
def menu():
    cargar_archivo()
    while True:
        print("\n===== SISTEMA DE LIBRERÍA =====")
        print("1. Registrar libro")
        print("2. Mostrar libros")
        print("3. Buscar libro")
        print("4. Vender libro")
        print("5. Reporte de ventas")
        print("6. Guardar y salir")
 
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Opción inválida")
            continue
 
        if opcion == 1:
            registrar_libro()
        elif opcion == 2:
            mostrar_libros()
        elif opcion == 3:
            buscar_libro()
        elif opcion == 4:
            vender_libro()
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