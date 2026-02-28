import os
import pandas as pd
from pathlib import Path

class OutputCreator:

    def __init__(self, ruta_tablas, ruta_graficos) -> None:
        self.ruta_tablas = ruta_tablas
        self.ruta_graficos = ruta_graficos
        

    def guardar_csv(self, df, nombre_archivo) -> None:
        """
        Guarda un DataFrame como CSV solo si el archivo no existe en la ruta.
        DEBE AGREGAR .csv AL FINAL DEL NOMBRE
        """
        ruta_archivo = self.ruta_tablas / nombre_archivo
        # verificamr si la ruta ya existe
        if os.path.exists(ruta_archivo):
            print(f"El archivo ya existe en: {ruta_archivo}")
            print("Operación cancelada para evitar duplicados.")
        else:
            # Si no existe, se guarda
            try:
                df.to_csv(ruta_archivo, index=False)
                print(f"Archivo guardado exitosamente en: {ruta_archivo}")
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")