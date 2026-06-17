import json
import os

class GestorArchivos:
    def __init__(self, nombre_archivo="libreria_datos.json"):
        self.archivo = nombre_archivo

    def cargar_datos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                # Retorna los productos y ventas (o listas vacías si no existen)
                return datos.get("productos", []), datos.get("ventas", [])
        return [], []

    def guardar_datos(self, productos, ventas):
        datos = {
            "productos": productos,
            "ventas": ventas
        }
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        print(f"Datos guardados en '{self.archivo}'")
