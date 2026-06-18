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
                
                # Validamos que la raíz sea un diccionario
                if not isinstance(datos, dict):
                    print("Advertencia: El archivo JSON está corrupto o mal formado. Se cargará vacío.")
                    return [], []
                
                productos_crudos = datos.get("productos", [])
                ventas_crudas = datos.get("ventas", [])
                
                if not isinstance(productos_crudos, list) or not isinstance(ventas_crudas, list):
                    return [], []

                # --- VALIDACIÓN DE PRODUCTOS ---
                productos_validados = []
                for p in productos_crudos:
                    # Comprobamos que sea diccionario y tenga las claves mínimas
                    if isinstance(p, dict) and all(k in p for k in ('codigo', 'nombre', 'precio', 'stock')):
                        try:
                            # Forzamos los tipos correctos para evitar errores matemáticos
                            p['precio'] = float(p['precio'])
                            p['stock'] = int(p['stock'])
                            productos_validados.append(p)
                        except (ValueError, TypeError):
                            print(f"Advertencia: Producto {p.get('codigo', 'Desconocido')} ignorado por datos inválidos.")
                            continue 

                # --- VALIDACIÓN DE VENTAS ---
                ventas_validadas = [v for v in ventas_crudas if isinstance(v, dict)]

                return productos_validados, ventas_validadas

        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"\n[!] Error crítico al leer la base de datos: {e}")
            print("El sistema iniciará con el inventario vacío por seguridad.")
            return [], []
        except Exception as e:
            print(f"\n[!] Error inesperado en archivos: {e}")
            return [], []

    def guardar_datos(self, productos, ventas):
        try:
            datos = {"productos": productos, "ventas": ventas}
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            print(f"Datos guardados correctamente en '{self.archivo}'")
            return True
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
            return False
