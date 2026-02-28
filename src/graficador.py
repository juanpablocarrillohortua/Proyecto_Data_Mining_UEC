import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
                         order: bool = True) -> None:
        
        #establecer tema

        sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#F8F9FA", "figure.facecolor": "#F8F9FA"})
        plt.rcParams['figure.figsize'] = (10, 5)


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