import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path


class Graficador:

    def __init__(self, ruta_guardado):
        self.ruta_guardado = ruta_guardado

    def barplot_discreto(self, 
                         data_frame:pd.DataFrame, 
                         var: str, 
                         titulo: str, 
                         etiqueta_x: str, 
                         etiqueta_y: str = False, 
                         count_label: bool = True,
                         paleta: str = "pastel",
                         order: bool = True,
                         rotacion: int = False) -> None:
        
        """Generar un Barplot para variables discretas"""
        
        #establecer tema

        sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#F8F9FA", "figure.facecolor": "#F8F9FA"})

        self.figura_actual, ax = plt.subplots(figsize=(10, 5))


        # Crear el gráfico de frecuencias (Countplot)
        if order:
            # Ordenar los datos por valor de frecuencia
            order = data_frame[var].value_counts().index

            ax = sns.countplot(
                data=data_frame, 
                x=var, 
                order=order,
                palette=paleta, # color
                hue=var,     # Asignamos hue para control de color
                legend=False
            )
        else:
            ax = sns.countplot(
                data=data_frame, 
                x=var, 
                palette=paleta, # color
                hue=var,     # Asignamos hue para control de color
                legend=False
            )

        # Configuracion titulos y aspecto general
        sns.despine(left=True) 

        ax.set_title(titulo, fontsize=18, pad=25, weight='bold', color='#2C3E50')

        ax.set_xlabel(etiqueta_x, fontsize=12, labelpad=15, color='#34495E')

        if etiqueta_y:
          ax.set_ylabel(etiqueta_y, fontsize=12, labelpad=15, color='#34495E')
        else:  
            ax.set_ylabel("Cantidad", fontsize=12, labelpad=15, color='#34495E')

        #rotacion del eje x
        if rotacion:
            ax.tick_params(axis='x', rotation=rotacion) 

            plt.setp(ax.get_xticklabels(), ha="center", va="top")

        # Añadir etiquetas de datos sobre las barras (Data Labels) solo si es True
        if count_label:
            for p in ax.patches:
                ax.annotate(f'{int(p.get_height())}', 
                            (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha = 'center', va = 'center', 
                            xytext = (0, 9), 
                            textcoords = 'offset points',
                            fontsize=11, fontweight='bold', color='#2C3E50')

        plt.tight_layout()
        plt.show()

    def guardar_grafico(self, nombre_archivo: str, dpi: int = 300, sobrescribir: bool = False):
            
            """
            Guarda la figura actual. 
            Verifica si el archivo ya existe antes de proceder.
            """

            if self.figura_actual is None:
                print("Error: No hay ningún gráfico generado para guardar.")
                return

            # Asegurar que tenga extensión
            if not nombre_archivo.endswith(('.png', '.jpg', '.pdf', '.svg')):
                nombre_archivo += '.png'

            # Crear carpeta si no existe
            if not os.path.exists(self.ruta_guardado):
                os.makedirs(self.ruta_guardado)
                print(f"Carpeta creada: {self.ruta_guardado}")

            ruta_completa = self.ruta_guardado / nombre_archivo

            # Revisar si ya existe
            if os.path.exists(ruta_completa) and not sobrescribir:
                print(f"El archivo '{nombre_archivo}' ya existe en '{self.ruta_guardado}'.")
                print("Usa 'sobrescribir=True' si deseas reemplazarlo.")
            else:
                self.figura_actual.savefig(ruta_completa, dpi=dpi, bbox_inches='tight')
                print(f"Gráfico guardado exitosamente en: {ruta_completa}")