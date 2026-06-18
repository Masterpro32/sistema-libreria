import json
import os

class GestorArchivos:
    def __init__(self, nombre_archivo="libreria_datos.json"):
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        self.archivo = os.path.join(carpeta_actual, "..", nombre_archivo)

    def cargar_datos(self):
        if not os.path.exists(self.archivo):
            return [], []
            
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if not isinstance(datos, dict):
                    return [], []
                productos = datos.get("productos", [])
                ventas = datos.get("ventas", [])
                if not isinstance(productos, list) or not isinstance(ventas, list):
                    return [], []
                return productos, ventas
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            return [], []
        except Exception:
            return [], []

    def guardar_datos(self, productos, ventas):
        try:
            datos = {"productos": productos, "ventas": ventas}
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            print(f"Datos guardados correctamente en '{self.archivo}'")
            return True
        except Exception:
            return False