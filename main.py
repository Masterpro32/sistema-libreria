from clases_libreria import GestorArchivos, GestorInventario, GestorVentas

def menu():
    servicio_archivo = GestorArchivos()
    productos_guardados, ventas_guardadas = servicio_archivo.cargar_datos()

    inventario = GestorInventario(productos_guardados)
    caja = GestorVentas(ventas_guardadas)

    while True:
        print("\n===== SISTEMA DE LIBRERÍA =====")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Buscar producto")
        print("4. Vender producto")
        print("5. Reporte de ventas")
        print("6. Ver prefijos / categorías")  # <- NUEVA OPCIÓN
        print("7. Guardar y salir")
        
        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            inventario.registrar_producto()
        elif opcion == '2':
            inventario.mostrar_productos()
        elif opcion == '3':
            inventario.buscar_producto()
        elif opcion == '4':
            caja.registrar_venta(inventario.productos)
        elif opcion == '5':
            caja.mostrar_reporte()
        elif opcion == '6':  # <- LÓGICA DE LA NUEVA OPCIÓN
            print("\n=== PREFIJOS Y CATEGORÍAS VÁLIDAS ===")
            prefijos = inventario.obtener_prefijos_actuales()
            for letra, significado in sorted(prefijos.items()):
                print(f"  {letra} -> {significado}")
            print("-------------------------------------")
        elif opcion == '7':
            servicio_archivo.guardar_datos(inventario.productos, caja.ventas)
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()