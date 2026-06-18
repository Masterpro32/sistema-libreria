# Importamos nuestras clases desde los otros archivos
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
        print("5. Reporte de ventas")
        print("6. Guardar y salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Opción inválida")
            continue
        if opcion == 1:
            inventario.registrar_producto()
            archivos.guardar_datos(inventario.productos, caja.ventas)
        elif opcion == 2:
            inventario.mostrar_productos()
        elif opcion == 3:
            inventario.buscar_producto()
        elif opcion == 4:
            if caja.vender_producto(inventario): 
                archivos.guardar_datos(inventario.productos, caja.ventas)
                
        elif opcion == 5:
            caja.reporte_ventas()
        elif opcion == 6:
            archivos.guardar_datos(inventario.productos, caja.ventas)
            print("Programa finalizado")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()
