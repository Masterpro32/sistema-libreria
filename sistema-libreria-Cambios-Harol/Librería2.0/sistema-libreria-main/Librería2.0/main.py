# Importamos nuestras clases desde los otros archivos
# Importa la clase que se encarga de registrar ventas y generar reportes.
from Clases.GestorVentas import GestorVentas
# Importa la clase responsable de cargar y guardar la información en JSON.
from Clases.GestorArchivo import GestorArchivos
# Importa la clase que administra los productos del inventario.
from Clases.GestorInventario import GestorInventario

# Define la función principal que muestra el menú y conecta todos los módulos del sistema.
def menu():

    # Crea un objeto para manejar el archivo donde se guardan productos y ventas.
    archivos = GestorArchivos()
    # Carga desde el archivo JSON los productos y ventas guardados anteriormente.
    productos_guardados, ventas_guardadas = archivos.cargar_datos()
    # Crea el gestor de inventario usando los productos recuperados del archivo.
    inventario = GestorInventario(productos_guardados)
    # Crea el gestor de ventas usando el historial de ventas recuperado.
    caja = GestorVentas(ventas_guardadas)

    # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
    while True:
        # Muestra el título principal del menú del sistema.
        print("\n===== SISTEMA DE LIBRERÍA =====")
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("1. Registrar producto")
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("2. Mostrar productos")
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("3. Buscar producto")
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("4. Vender producto")
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("5. Reporte de ventas")
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("6. Guardar y salir")

        # Inicia un bloque para intentar ejecutar código que podría generar errores.
        try:
            # Solicita la opción del usuario y la convierte a número entero.
            opcion = int(input("Seleccione una opción: "))
        # Captura el error cuando la entrada numérica no tiene el formato esperado.
        except ValueError:
            # Informa al usuario que la opción ingresada no es válida.
            print("Opción inválida")
            # Regresa al inicio del bucle para volver a pedir una entrada válida.
            continue
        # Ejecuta la opción para registrar un producto nuevo.
        if opcion == 1:
            # Llama al método que pide y valida los datos del nuevo producto.
            inventario.registrar_producto()
            # Guarda en el archivo JSON el inventario y las ventas actualizadas.
            archivos.guardar_datos(inventario.productos, caja.ventas)
        # Ejecuta la opción para mostrar todos los productos registrados.
        elif opcion == 2:
            # Llama al método que lista los productos del inventario.
            inventario.mostrar_productos()
        # Ejecuta la opción para buscar un producto por nombre.
        elif opcion == 3:
            # Llama al método de búsqueda de productos dentro del inventario.
            inventario.buscar_producto()
        # Ejecuta la opción para registrar una venta.
        elif opcion == 4:
            # Intenta realizar una venta usando los productos disponibles en inventario.
            if caja.vender_producto(inventario): 
                # Guarda en el archivo JSON el inventario y las ventas actualizadas.
                archivos.guardar_datos(inventario.productos, caja.ventas)
                
        # Ejecuta la opción para revisar los reportes de ventas.
        elif opcion == 5:
            # Llama al reporte de ventas y le pasa el inventario para cruzar datos de productos.
            caja.reporte_ventas(inventario)
        # Ejecuta la opción para guardar los datos y cerrar el programa.
        elif opcion == 6:
            # Guarda en el archivo JSON el inventario y las ventas actualizadas.
            archivos.guardar_datos(inventario.productos, caja.ventas)
            # Muestra un mensaje indicando que el sistema terminó correctamente.
            print("Programa finalizado")
            # Rompe el bucle principal y finaliza la ejecución de la función actual.
            break
        # Maneja cualquier opción que no coincida con las opciones permitidas.
        else:
            # Informa al usuario que la opción ingresada no es válida.
            print("Opción inválida")
# Verifica que este archivo se esté ejecutando directamente y no importado como módulo.
if __name__ == "__main__":
    # Inicia el sistema llamando a la función principal del menú.
    menu()
