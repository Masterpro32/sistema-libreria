# Importa json para leer y escribir datos en formato JSON.
import json
# Importa os para trabajar con rutas de archivos y carpetas del sistema.
import os

# Define la clase encargada de administrar la carga y guardado de datos.
class GestorArchivos:
    # Constructor que recibe el nombre del archivo JSON donde se guardará la información.
    def __init__(self, nombre_archivo="libreria_datos.json"):
        # Obtiene la ruta absoluta de la carpeta donde se encuentra este archivo Python.
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta del archivo JSON ubicado una carpeta arriba de la carpeta actual.
        self.archivo = os.path.join(carpeta_actual, "..", nombre_archivo)

    # Define el método que carga productos y ventas desde el archivo JSON.
    def cargar_datos(self):
        # Verifica si el archivo JSON todavía no existe.
        if not os.path.exists(self.archivo):
            # Devuelve listas vacías para productos y ventas cuando no hay datos válidos.
            return [], []
            
        # Inicia un bloque para intentar ejecutar código que podría generar errores.
        try:
            # Abre el archivo JSON en modo lectura usando codificación UTF-8.
            with open(self.archivo, "r", encoding="utf-8") as f:
                # Convierte el contenido JSON del archivo en una estructura de Python.
                datos = json.load(f)
                # Verifica que el contenido principal del JSON sea un diccionario.
                if not isinstance(datos, dict):
                    # Devuelve listas vacías para productos y ventas cuando no hay datos válidos.
                    return [], []
                # Obtiene la lista de productos guardados; si no existe, usa una lista vacía.
                productos = datos.get("productos", [])
                # Obtiene la lista de ventas guardadas; si no existe, usa una lista vacía.
                ventas = datos.get("ventas", [])
                # Comprueba que productos y ventas sean listas válidas antes de usarlas.
                if not isinstance(productos, list) or not isinstance(ventas, list):
                    # Devuelve listas vacías para productos y ventas cuando no hay datos válidos.
                    return [], []
                # Devuelve las listas cargadas para que el sistema continúe con esos datos.
                return productos, ventas
        # Controla errores esperados relacionados con archivo faltante, JSON dañado o datos incorrectos.
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            # Devuelve listas vacías para productos y ventas cuando no hay datos válidos.
            return [], []
        # Captura cualquier otro error inesperado para evitar que el programa se cierre abruptamente.
        except Exception:
            # Devuelve listas vacías para productos y ventas cuando no hay datos válidos.
            return [], []

    # Define el método encargado de guardar productos y ventas en el archivo JSON.
    def guardar_datos(self, productos, ventas):
        # Inicia un bloque para intentar ejecutar código que podría generar errores.
        try:
            # Agrupa productos y ventas en un solo diccionario antes de guardarlos.
            datos = {"productos": productos, "ventas": ventas}
            # Abre el archivo JSON en modo escritura para reemplazarlo con los datos actuales.
            with open(self.archivo, "w", encoding="utf-8") as f:
                # Guarda el diccionario en formato JSON con tildes permitidas y sangría de 4 espacios.
                json.dump(datos, f, ensure_ascii=False, indent=4)
            # Confirma en pantalla que los datos fueron guardados correctamente.
            print(f"Datos guardados correctamente en '{self.archivo}'")
            # Devuelve True para indicar que el guardado fue exitoso.
            return True
        # Captura cualquier otro error inesperado para evitar que el programa se cierre abruptamente.
        except Exception:
            # Devuelve False cuando ocurre un error al guardar.
            return False
