import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path
import scipy.stats as stats


class Graficador:

    def __init__(self, ruta_guardado):
        self.ruta_guardado = ruta_guardado

    @staticmethod
    def calcular_porcentaje_atipicos(data:pd.DataFrame ,var: str, screen=True):
    
        q1 = data[var].quantile(0.25)
        q3 = data[var].quantile(0.75)
        iqr = q3 - q1

        
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        
        outliers_mask = (data[var] < limite_inferior) | (data[var] > limite_superior)

        
        porcentaje_outliers = outliers_mask.mean() * 100 # .mean() sobre booleanos da la proporción (0 a 1)

        if screen:
            print(f"--- Análisis de: {var} ---")
            print(f"Límite Inferior: {limite_inferior:.4f}")
            print(f"Límite Superior: {limite_superior:.4f}")
            print(f"Porcentaje de atípicos: {porcentaje_outliers:.2f}%")
            print("-" * 30)
        return porcentaje_outliers

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

    def graficos_continuos(self, 
                           df: pd.DataFrame, 
                           var: str) -> None:
        """Genera un resumen grafico completo para las variables continuas"""
        # 1. Preparación de datos y estadísticos
        data = df[var]
        media = data.mean()
        mediana = data.median()
        moda = data.mode()[0]

        # 2. Configurar la cuadrícula (1 fila, 3 columnas)
        self.figura_actual, axes = plt.subplots(1, 3, figsize=(18, 5))
        sns.set_theme(style="darkgrid")

        # --- GRÁFICO 1: HISTOGRAMA ---
        sns.histplot(data, kde=True, color="#4C72B0", element="step", alpha=0.4, ax=axes[0], bins="fd")
        axes[0].axvline(media, color='red', linestyle='--', label=f'Media: {media:.2f}')
        axes[0].axvline(mediana, color='green', linestyle='-', label=f'Mediana: {mediana:.2f}')
        axes[0].axvline(moda, color='orange', linestyle=':', label=f'Moda: {moda:.2f}')
        axes[0].set_title('Histograma y Tendencia Central')
        axes[0].legend()

        # --- GRÁFICO 2: BOXPLOT ---
        sns.boxplot(y=data, ax=axes[1], color="#9b59b6", width=0.3)
        axes[1].set_title('Boxplot (Detección de Outliers)')
        # punto para la media en el boxplot
        axes[1].plot(0, media, marker='D', color='red', label='Media') 

        # --- GRÁFICO 3: QQ-PLOT ---
        # stats.probplot dibuja el gráfico sobre el eje que le pasemos
        stats.probplot(data, dist="norm", plot=axes[2])
        axes[2].get_lines()[0].set_markerfacecolor('#4C72B0') # Color de los puntos
        axes[2].get_lines()[1].set_color('red')               # Color de la línea de ajuste
        axes[2].set_title('QQ-Plot (Ajuste a Normal)')

        # Ajuste final de diseño
        self.figura_actual.suptitle(f'Análisis de la Variable: {var}', 
                             fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        sns.despine()
        plt.show()

    def scatter_plot(self, 
                     data: pd.DataFrame, 
                     x:str, 
                     y:str,
                     x_title: str = None,
                     y_title: str = None,
                     main_title: str = None) -> None:

        """Generar un grafico de puntos para observar la relacion entre 2 variables"""

        sns.set_theme(style="darkgrid", palette="muted")

        # Crear el gráfico
        self.figura_actual, ax = plt.subplots(figsize=(10, 6))
        sns.regplot(
            data=data, 
            x=data[x], 
            y=data[y],
            scatter_kws={'alpha':0.5, 's':60}, # Transparencia y tamaño de puntos
            line_kws={'color':'red', 'lw':2}   # Estilo de la línea de ajuste
        )

        # Personalizar etiquetas y título
        ax.set_title(main_title or f'Relación entre {x} y {y}', fontsize=16, fontweight='bold', y=1.02)
        ax.set_xlabel(x_title or x, fontsize=12)
        ax.set_ylabel(y_title or y, fontsize=12)

        # Quitar los bordes superior y derecho para un look más limpio
        sns.despine()

        plt.show()
    
    def box_plot_para_atipicos(self, data: pd.DataFrame , var: str) -> None:

        porcentaje = Graficador.calcular_porcentaje_atipicos(data, var, screen=False)
    
        sns.set_theme(style="darkgrid", context="notebook")

        # 2. Crear la figura y el eje usando subplots
        # Esto reemplaza a plt.figure() y permite gestionar mejor el layout
        self.figura_actual, ax = plt.subplots(figsize=(10, 6), dpi=100)

        # 3. Crear el Boxplot vinculándolo al eje 'ax'
        sns.boxplot(
            data=data,
            y=var,
            color='#3376BD',
            width=0.4,           
            linewidth=1.5,
            fliersize=5,         
            showmeans=True,
            meanprops={
                "marker":"o", 
                "markerfacecolor":"white", 
                "markeredgecolor":"black", 
                "markersize":"7"
            },
            ax=ax                
        )

        texto_info = f'Porcentaje de Outliers: {porcentaje:.2f}%'
        
        ax.text(
            0.95, 0.95,                  # Posición (X, Y) relativa al eje
            texto_info, 
            transform=ax.transAxes,      # Indica que use coordenadas 0-1 del recuadro
            fontsize=12,
            verticalalignment='top', 
            horizontalalignment='right',
            fontweight='bold',
            bbox=dict(                   # Propiedades del recuadro
                boxstyle='round,pad=0.5', 
                facecolor='white', 
                edgecolor="#FFFFFF", 
                alpha=0.8
            )
        )

        # 4. Personalización sobre el objeto 'ax'
        ax.set_title(f'Detección de outliers para {var}', fontsize=18, pad=20, fontweight='bold')

        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.xaxis.grid(False)

        sns.despine(ax=ax, left=True, bottom=True)

        plt.tight_layout()
        plt.show()