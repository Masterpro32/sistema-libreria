# Importa json para leer y escribir datos en formato JSON.
import json
# Importa os para trabajar con rutas de archivos y carpetas del sistema.
import os
# Importa re para validar textos mediante expresiones regulares.
import re

# Define la clase encargada de gestionar los productos del inventario.
class GestorInventario:
    # Constructor que recibe la lista de productos cargados desde el archivo.
    def __init__(self, productos_cargados):
        # Guarda la lista de productos en el atributo principal del inventario.
        self.productos = productos_cargados

    # Define el método que registra un producto nuevo con todas sus validaciones.
    def registrar_producto(self):
        # Muestra el encabezado del módulo de registro de productos.
        print("\nREGISTRO DE PRODUCTO")
        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Solicita el nombre del producto y elimina espacios al inicio y al final.
            nombre = input("Nombre del producto: ").strip()
            # Valida que el nombre no esté vacío ni sea una palabra reservada o inválida.
            if nombre == "" or nombre.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none', 'false', 'true']:
                # Muestra un mensaje si el nombre del producto no cumple la validación inicial.
                print("Error: Nombre inválido, vacío o palabra reservada no permitida.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Valida que el nombre tenga una longitud razonable entre 3 y 60 caracteres.
            if len(nombre) < 3 or len(nombre) > 60:
                # Informa que el nombre no cumple con la longitud permitida.
                print("Error: El nombre debe tener entre 3 y 60 caracteres.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Comprueba si el nombre está formado únicamente por números.
            if nombre.isdigit():
                # Evita registrar productos cuyo nombre sea solamente numérico.
                print("Error: El nombre no puede ser solo números.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Verifica si el nombre contiene solamente símbolos, sin letras ni números.
            if all(not c.isalnum() and not c.isspace() for c in nombre):
                # Informa que un nombre formado solo por símbolos no es válido.
                print("Error: El nombre no puede contener solo símbolos.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Busca si ya existe otro producto con el mismo nombre, ignorando mayúsculas y minúsculas.
            if any(p['nombre'].lower() == nombre.lower() for p in self.productos):
                # Evita registrar productos duplicados con el mismo nombre.
                print("Error: Ya existe un producto con este mismo nombre.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Rompe el bucle principal y finaliza la ejecución de la función actual.
            break
            
        # Crea un diccionario con los prefijos permitidos y su categoría correspondiente.
        prefijos_validos = {
            # Asocia el prefijo C con la categoría Cuadernos.
            'C': 'Cuadernos',
            # Asocia el prefijo P con la categoría Papelería.
            'P': 'Papelería',
            # Asocia el prefijo A con la categoría Arte y Manualidades.
            'A': 'Arte y Manualidades',
            # Asocia el prefijo H con la categoría Herramientas de Oficina.
            'H': 'Herramientas de Oficina',
            # Asocia el prefijo E con la categoría Escritura.
            'E': 'Escritura',
            # Asocia el prefijo Ñ con la categoría Varios.
            'Ñ': 'Varios'
        # Línea necesaria para completar el funcionamiento del sistema.
        }
        
        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Muestra una tabla de ayuda con los prefijos permitidos.
            print("\n--- Prefijos permitidos y su significado ---")
            # Recorre cada prefijo y su significado para mostrarlos en pantalla.
            for letra, significado in prefijos_validos.items():
                # Imprime cada prefijo junto con la categoría que representa.
                print(f"  {letra} -> {significado}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("--------------------------------------------")
            # Solicita el código del producto, elimina espacios y lo convierte a mayúsculas.
            codigo = input("Código (Debe ser de 4 caracteres, Ej: C001): ").strip().upper()
            # Valida que el código no esté vacío ni use palabras reservadas.
            if codigo == "" or codigo.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                # Muestra error cuando el código ingresado no es válido.
                print("Error: El código no puede estar vacío ni contener palabras reservadas.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Verifica que el código tenga exactamente 4 caracteres.
            if len(codigo) != 4:
                # Informa el formato correcto del código cuando la longitud es incorrecta.
                print("Error: El código debe tener EXACTAMENTE 4 caracteres (Ejemplo: C001).")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Extrae la primera letra del código para identificar la categoría.
            primera_letra = codigo[0]
            # Comprueba que la primera letra pertenezca a los prefijos permitidos.
            if primera_letra not in prefijos_validos:
                # Indica que el prefijo ingresado no corresponde a ninguna categoría válida.
                print(f"Error: El prefijo '{primera_letra}' no es válido.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Valida que los tres últimos caracteres del código sean números.
            if not codigo[1:].isdigit():
                # Explica el formato correcto cuando el código no termina en tres números.
                print("Error: Después de la letra deben seguir exactamente 3 números (Ejemplo: C001).")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Revisa si ya existe un producto registrado con el mismo código.
            repetido = any(p['codigo'] == codigo for p in self.productos)
            # Comprueba el resultado de la búsqueda de código duplicado.
            if repetido:
                # Evita guardar un producto con un código repetido.
                print("Error: Este código ya existe.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Asigna automáticamente la categoría según la primera letra del código.
            categoria = prefijos_validos[primera_letra]
            # Rompe el bucle principal y finaliza la ejecución de la función actual.
            break
            
        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Solicita el precio de venta y elimina espacios innecesarios.
            precio_input = input("Precio de venta (S/.): ").strip()
            # Valida que el precio de venta no esté vacío ni contenga valores inválidos.
            if precio_input == "" or precio_input.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print("Error: Entrada inválida.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Define una expresión regular para permitir números positivos con máximo dos decimales.
            patron_precio = r"^\d+(\.\d{1,2})?$"
            # Verifica que el precio de venta cumpla el formato definido.
            if not re.match(patron_precio, precio_input):
                # Indica el formato correcto del precio de venta.
                print("Error: Formato inválido. Ingrese solo números positivos con máximo 2 decimales (Ej: 5.50).")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Convierte el precio de venta validado a número decimal.
            precio = float(precio_input)
            # Verifica que el precio no sea cero.
            if precio == 0:
                # Informa que el precio de venta debe ser mayor que cero.
                print("Error: El precio debe ser mayor a 0.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Rompe el bucle principal y finaliza la ejecución de la función actual.
            break
            
        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Solicita el precio de compra y elimina espacios.
            compra_input = input("Precio de compra (S/.): ").strip()
            # Valida que el precio de compra no esté vacío ni tenga valores inválidos.
            if compra_input == "" or compra_input.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print("Error: Entrada inválida.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Valida el formato del precio de compra con máximo dos decimales.
            if not re.match(r"^\d+(\.\d{1,2})?$", compra_input):
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print("Error: Formato inválido.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Convierte el precio de compra validado a número decimal.
            precio_compra = float(compra_input)
            # Comprueba que el precio de compra sea menor al precio de venta.
            if precio_compra >= precio:
                # Evita registrar productos sin margen de ganancia.
                print("Error: El precio de compra debe ser menor al de venta.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Rompe el bucle principal y finaliza la ejecución de la función actual.
            break
            
        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Solicita la cantidad inicial disponible del producto.
            stock_input = input("Stock Inicial: ").strip()
            # Valida que el stock inicial no esté vacío ni contenga palabras inválidas.
            if stock_input == "" or stock_input.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print("Error: Entrada no válida.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Inicia un bloque para intentar ejecutar código que podría generar errores.
            try:
                # Convierte el stock inicial a número entero.
                stock = int(stock_input)
                # Verifica que el stock inicial no sea negativo.
                if stock < 0:
                    # Informa que no se permiten cantidades negativas en el inventario.
                    print("Error: El stock inicial no puede ser negativo.")
                    # Regresa al inicio del bucle para volver a pedir una entrada válida.
                    continue
                # Rompe el bucle principal y finaliza la ejecución de la función actual.
                break
            # Captura el error cuando la entrada numérica no tiene el formato esperado.
            except ValueError:
                # Solicita un número entero válido para el stock inicial.
                print("Error: Ingrese un número entero válido para el stock.")
                
        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Solicita el stock mínimo que activará una alerta de bajo stock.
            stock_min_input = input("Definir Stock Mínimo de Alerta: ").strip()
            # Valida que el stock mínimo no esté vacío ni use valores inválidos.
            if stock_min_input == "" or stock_min_input.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print("Error: Entrada no válida.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Inicia un bloque para intentar ejecutar código que podría generar errores.
            try:
                # Convierte el stock mínimo a número entero.
                stock_minimo = int(stock_min_input)
                # Verifica que el stock mínimo sea al menos una unidad.
                if stock_minimo < 1:
                    # Informa que el mínimo de alerta no puede ser cero ni negativo.
                    print("Error: El stock mínimo de alerta debe ser de al menos 1 unidad.")
                    # Regresa al inicio del bucle para volver a pedir una entrada válida.
                    continue
                # Rompe el bucle principal y finaliza la ejecución de la función actual.
                break
            # Captura el error cuando la entrada numérica no tiene el formato esperado.
            except ValueError:
                # Solicita una entrada entera válida para el stock mínimo.
                print("Error: Ingrese un número entero válido para el stock mínimo.")
                
        # Crea el diccionario que almacenará todos los datos del producto nuevo.
        producto = {
            # Guarda el código único del producto.
            "codigo": codigo,
            # Guarda el nombre validado del producto.
            "nombre": nombre,
            # Guarda la categoría calculada según el prefijo del código.
            "categoria": categoria,
            # Guarda el precio de venta del producto.
            "precio": precio,
            # Guarda el costo de compra para calcular utilidad.
            "precio_compra": precio_compra,
            # Guarda la cantidad disponible en inventario.
            "stock": stock,
            # Guarda el límite mínimo para mostrar alerta de bajo stock.
            "stock_minimo": stock_minimo  
        # Línea necesaria para completar el funcionamiento del sistema.
        }
        # Agrega el producto nuevo a la lista principal del inventario.
        self.productos.append(producto)
        # Confirma que el producto fue registrado correctamente.
        print(f"¡Producto '{nombre}' registrado correctamente con el código {codigo}!")

    # Define el método que muestra el catálogo completo de productos.
    def mostrar_productos(self):
        # Comprueba si la lista de productos está vacía.
        if not self.productos:
            # Informa que no hay productos para mostrar.
            print("\nEl inventario esta vacio. Registre productos primero.")
            # Sale del método actual sin continuar ejecutando más instrucciones.
            return
        # Ordena los productos por código para mostrarlos de forma organizada.
        lista_ordenada = sorted(self.productos, key=lambda x: x['codigo'])
        # Define cuántos productos se mostrarán por cada página del catálogo.
        items_for_pagina = 10
        # Calcula el total de páginas necesarias para mostrar todos los productos.
        total_paginas = (len(lista_ordenada) + items_for_pagina - 1) // items_for_pagina
        # Inicia la visualización desde la primera página.
        pagina_actual = 1
        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Calcula el índice inicial de los productos de la página actual.
            inicio = (pagina_actual - 1) * items_for_pagina
            # Calcula el índice final de los productos de la página actual.
            fin = inicio + items_for_pagina
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("\n==========================================================================")
            # Muestra el número de página actual dentro del catálogo.
            print(f"                    CATALOGO - PAGINA {pagina_actual} de {total_paginas}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("==========================================================================")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print(f"{'CODIGO':<8} | {'NOMBRE':<35} | {'PRECIO':<10} | {'STOCK':<8} | {'ESTADO'}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("-" * 74)
            # Obtiene solamente los productos que corresponden a la página actual.
            productos_pagina = lista_ordenada[inicio:fin]
            # Recorre cada producto de la página actual para mostrarlo en pantalla.
            for p in productos_pagina:
                # Obtiene el código del producto actual.
                codigo = p['codigo']
                # Obtiene el nombre del producto actual.
                nombre = p['nombre']
                # Formatea el precio con dos decimales y símbolo de soles.
                precio = f"S/. {p['precio']:.2f}"
                # Obtiene el stock actual del producto.
                stock = p['stock']
                # Obtiene el stock mínimo; si no existe, usa 1 como valor predeterminado.
                stock_min = p.get('stock_minimo', 1)
                # Verifica si el producto ya no tiene unidades disponibles.
                if stock == 0:
                    # Marca el producto como sin stock.
                    estado = "[SIN STOCK]"
                # Verifica si el stock actual está en el nivel mínimo o por debajo.
                elif stock <= stock_min:
                    # Marca el producto como bajo stock e indica el mínimo configurado.
                    estado = f"[BAJO STOCK] (Min: {stock_min})"
                # Maneja cualquier opción que no coincida con las opciones permitidas.
                else:
                    # Marca el producto como disponible con stock suficiente.
                    estado = "[OK]"
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print(f"{codigo:<8} | {nombre:<35} | {precio:<10} | {stock:<8} | {estado}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("==========================================================================")
            # Define la opción base para salir de la vista del catálogo.
            opciones = ['q']
            # Prepara el texto de opciones que verá el usuario.
            mensaje = "[q] Salir"
            # Comprueba si existe una página siguiente.
            if pagina_actual < total_paginas:
                # Agrega la opción para avanzar a la siguiente página.
                opciones.append('s')
                # Añade al mensaje la opción de página siguiente.
                mensaje += " | [s] Siguiente"
            # Comprueba si existe una página anterior.
            if pagina_actual > 1:
                # Agrega la opción para regresar a la página anterior.
                opciones.append('a')
                # Añade al mensaje la opción de página anterior.
                mensaje += " | [a] Anterior"
                
            # Solicita la acción de navegación y normaliza la entrada.
            opcion = input(f"Opciones: {mensaje} -> ").strip().lower()
            # Valida que la opción ingresada sea una de las permitidas en esta página.
            if opcion not in opciones:
                # Informa que la opción de navegación no es válida.
                print("Error: Opcion invalida.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
                
            # Comprueba si el usuario desea salir del catálogo.
            if opcion == 'q':
                # Rompe el bucle principal y finaliza la ejecución de la función actual.
                break
            # Comprueba si el usuario desea avanzar y todavía hay páginas disponibles.
            elif opcion == 's' and pagina_actual < total_paginas:
                # Avanza una página en el catálogo.
                pagina_actual += 1
            # Comprueba si el usuario desea retroceder y no está en la primera página.
            elif opcion == 'a' and pagina_actual > 1:
                # Retrocede una página en el catálogo.
                pagina_actual -= 1

    # Define el método para buscar productos por coincidencia de nombre.
    def buscar_producto(self):
        # Muestra el encabezado del módulo de búsqueda.
        print("\nBUSCAR PRODUCTO")
        # Solicita el texto de búsqueda y lo convierte a minúsculas.
        nombre_buscar = input("Ingrese el nombre del producto a buscar: ").strip().lower()
        # Valida que la búsqueda no esté vacía ni sea un valor inválido.
        if nombre_buscar == "" or nombre_buscar in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined', 'none']:
            # Informa que la búsqueda ingresada no es válida.
            print("Error: Búsqueda inválida.")
            # Sale del método actual sin continuar ejecutando más instrucciones.
            return
            
        # Inicializa una bandera para saber si se encontró al menos un producto.
        encontrados = False
        # Recorre todos los productos del inventario.
        for p in self.productos:
            # Evalúa una condición para decidir si se ejecuta este bloque de código.
            if nombre_buscar in p['nombre'].lower():
                # Obtiene el stock mínimo; si no existe, usa 1 como valor predeterminado.
                stock_min = p.get('stock_minimo', 1)
                # Evalúa una condición para decidir si se ejecuta este bloque de código.
                if p['stock'] == 0:
                    # Marca el producto como sin stock.
                    estado = "[SIN STOCK]"
                # Evalúa una condición alternativa si las condiciones anteriores no se cumplieron.
                elif p['stock'] <= stock_min:
                    # Asigna o actualiza un valor que será usado más adelante en el programa.
                    estado = "[BAJO STOCK]"
                # Maneja cualquier opción que no coincida con las opciones permitidas.
                else:
                    # Marca el producto como disponible con stock suficiente.
                    estado = "[OK]"
                # Muestra el encabezado de un producto encontrado.
                print(f"\nProducto Encontrado:")
                # Muestra el código del producto encontrado.
                print(f"Codigo: {p['codigo']}")
                # Muestra el nombre del producto encontrado.
                print(f"Nombre: {p['nombre']}")
                # Muestra la categoría del producto, o un texto predeterminado si no existe.
                print(f"Categoria: {p.get('categoria', 'Sin Categoria')}")
                # Muestra el precio del producto con dos decimales.
                print(f"Precio: S/. {p['precio']:.2f}")
                # Muestra el stock actual junto con su estado.
                print(f"Stock Actual: {p['stock']} {estado}")
                # Marca que se encontró al menos un producto coincidente.
                encontrados = True
        # Comprueba si no hubo coincidencias después de recorrer todo el inventario.
        if not encontrados:
            # Informa que no existen productos con el nombre buscado.
            print("No se encontraron productos con ese nombre.")
