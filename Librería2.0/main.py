# Importamos nuestras clases desde el otro archivo
from clases_libreria import GestorArchivos, GestorInventario, GestorVentas

def menu():
    # 1. Inicializamos el gestor de archivos y cargamos los datos previos
    archivos = GestorArchivos()
    productos_guardados, ventas_guardadas = archivos.cargar_datos()

    # 2. Instanciamos nuestras clases principales con los datos cargados
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
        elif opcion == 2:
            inventario.mostrar_productos()
        elif opcion == 3:
            inventario.buscar_producto()
        elif opcion == 4:
            caja.vender_producto(inventario) # Le pasamos el inventario para que verifique el stock
        elif opcion == 5:
            caja.reporte_ventas()
        elif opcion == 6:
            # Al salir, le pasamos las listas actualizadas al gestor de archivos
            archivos.guardar_datos(inventario.productos, caja.ventas)
            print("Programa finalizado")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()
 
