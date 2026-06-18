from Clases.GestorVentas import GestorVentas
from Clases.GestorArchivo import GestorArchivos
from Clases.GestorInventario import GestorInventario

def menu():

    archivos = GestorArchivos()
    productos_guardados, ventas_guardadas = archivos.cargar_datos()
    inventario = GestorInventario(productos_guardados)
    caja = GestorVentas(ventas_guardadas)

    while True:
        print("\n===== SISTEMA DE LIBRERÍA =====")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto")
        print("4. Vender producto")
        print("5. Reponer stock")           # Nueva opción de stock
        print("6. Reporte de ventas")
        print("7. Guardar datos")           # Guarda sin cerrar el sistema
        print("8. Guardar y salir")         # Cierra el sistema

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Opción inválida. Ingrese un número.")
            continue
            
        if opcion == 1:
            inventario.registrar_producto()
            archivos.guardar_datos(inventario.productos, caja.ventas)
        elif opcion == 2:
            inventario.mostrar_productos()
        elif opcion == 3:
            inventario.buscar_producto()
        elif opcion == 4:
            # En tu GestorVentas, la función no retorna True/False por defecto en tu versión. 
            # Si no retorna nada, simplemente lo ejecutamos y guardamos por seguridad.
            caja.vender_producto(inventario)
            archivos.guardar_datos(inventario.productos, caja.ventas)
        elif opcion == 5:
            inventario.reponer_stock()
            archivos.guardar_datos(inventario.productos, caja.ventas)
        elif opcion == 6:
            caja.reporte_ventas(inventario)
        elif opcion == 7:
            archivos.guardar_datos(inventario.productos, caja.ventas)
        elif opcion == 8:
            archivos.guardar_datos(inventario.productos, caja.ventas)
            print("Programa finalizado. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Seleccione un número del 1 al 8.")

if __name__ == "__main__":
    menu()
