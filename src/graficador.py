import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pathlib import Path
import scipy.stats as stats

# --- CONSTANTES DE ESTILO EDITORIAL ---
_COLOR_TITULO    = '#34495e'
_COLOR_SUBTITULO = '#7f8c8d'
_COLOR_EJES      = '#555555'
_COLOR_GRILLA    = '#f8f9f9'
_COLOR_PRINCIPAL = '#4C72B0'
_COLOR_ACENTO    = '#ec7063'


def _aplicar_estilo_editorial():
    """Aplica la configuración base de estilo editorial a todos los gráficos."""
    sns.set_theme(style="white")
    plt.rcParams['font.family'] = 'sans-serif'


def _configurar_ejes(ax,
                     titulo: str,
                     subtitulo: str = None,
                     etiqueta_x: str = None,
                     etiqueta_y: str = None):
    """
    Aplica el estilo editorial estándar a un eje:
    título alineado a la izquierda, subtítulo itálico,
    grilla sutil y despine total.
    """
    # Título principal alineado a la izquierda
    ax.set_title(titulo, loc='left', fontweight='bold',
                 fontsize=16, color=_COLOR_TITULO, pad=12)

    # Subtítulo/descripción en itálica justo debajo del título
    if subtitulo:
        ax.text(0, 1.01, subtitulo,
                transform=ax.transAxes,
                fontsize=11, color=_COLOR_SUBTITULO, style='italic')

    # Etiquetas de ejes
    if etiqueta_x:
        ax.set_xlabel(etiqueta_x, fontsize=11, color=_COLOR_EJES)
    if etiqueta_y:
        ax.set_ylabel(etiqueta_y, fontsize=11, color=_COLOR_EJES)

    # Grilla sutil de fondo
    ax.grid(color=_COLOR_GRILLA, linestyle='-', linewidth=1, zorder=0)

    # Limpieza visual total (sin bordes)
    sns.despine(ax=ax, left=True, bottom=True)


class Graficador:
    """Compendio de gráficas con estilo editorial para uso en notebooks."""

    def __init__(self, ruta_guardado):
        """Cree la instancia con la ruta donde desee guardar los gráficos."""
        self.ruta_guardado = Path(ruta_guardado)
        self.figura_actual = None

    # ------------------------------------------------------------------ #
    #  MÉTODOS AUXILIARES                                                  #
    # ------------------------------------------------------------------ #

    @staticmethod
    def calcular_porcentaje_atipicos(data: pd.DataFrame, var: str, screen=True):
        """Calcula y muestra el porcentaje de valores atípicos por IQR."""
        q1  = data[var].quantile(0.25)
        q3  = data[var].quantile(0.75)
        iqr = q3 - q1

        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        outliers_mask       = (data[var] < limite_inferior) | (data[var] > limite_superior)
        porcentaje_outliers = outliers_mask.mean() * 100

        if screen:
            print(f"--- Análisis de: {var} ---")
            print(f"Límite Inferior: {limite_inferior:.4f}")
            print(f"Límite Superior: {limite_superior:.4f}")
            print(f"Porcentaje de atípicos: {porcentaje_outliers:.2f}%")
            print("-" * 30)

        return porcentaje_outliers

    def guardar_grafico(self, nombre_archivo: str, dpi: int = 300, sobrescribir: bool = False):
        """Guarda la figura actual. Verifica si el archivo ya existe."""
        if self.figura_actual is None:
            print("Error: No hay ningún gráfico generado para guardar.")
            return

        if not nombre_archivo.endswith(('.png', '.jpg', '.pdf', '.svg')):
            nombre_archivo += '.png'

        self.ruta_guardado.mkdir(parents=True, exist_ok=True)
        ruta_completa = self.ruta_guardado / nombre_archivo

        if ruta_completa.exists() and not sobrescribir:
            print(f"El archivo '{nombre_archivo}' ya existe en '{self.ruta_guardado}'.")
            print("Usa 'sobrescribir=True' si deseas reemplazarlo.")
        else:
            self.figura_actual.savefig(ruta_completa, dpi=dpi, bbox_inches='tight')
            print(f"Gráfico guardado exitosamente en: {ruta_completa}")

    # ------------------------------------------------------------------ #
    #  GRÁFICOS                                                            #
    # ------------------------------------------------------------------ #

    def barplot_discreto(self,
                         data_frame: pd.DataFrame,
                         var: str,
                         titulo: str,
                         etiqueta_x: str,
                         etiqueta_y: str = None,
                         subtitulo: str = None,
                         count_label: bool = True,
                         paleta: str = "pastel",
                         order: bool = True,
                         rotacion: int = None) -> None:
        """Genera un Barplot para variables discretas con estilo editorial."""

        _aplicar_estilo_editorial()
        self.figura_actual, ax = plt.subplots(figsize=(10, 5))

        orden = data_frame[var].value_counts().index if order else None

        sns.countplot(
            data=data_frame,
            x=var,
            order=orden,
            palette=paleta,
            hue=var,
            legend=False,
            ax=ax,
            zorder=2
        )

        # Etiquetas de conteo sobre las barras
        if count_label:
            for p in ax.patches:
                ax.annotate(
                    f'{int(p.get_height())}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9), textcoords='offset points',
                    fontsize=11, fontweight='bold', color=_COLOR_TITULO,
                    zorder=3
                )

        # Rotación del eje x
        if rotacion:
            ax.tick_params(axis='x', rotation=rotacion)
            plt.setp(ax.get_xticklabels(), ha="center", va="top")

        _configurar_ejes(
            ax,
            titulo=titulo,
            subtitulo=subtitulo,
            etiqueta_x=etiqueta_x,
            etiqueta_y=etiqueta_y or "Cantidad"
        )

        plt.tight_layout()
        plt.show()

    def graficos_continuos(self, df: pd.DataFrame, var: str) -> None:
        """Genera un resumen gráfico completo para variables continuas."""

        _aplicar_estilo_editorial()

        data    = df[var]
        media   = data.mean()
        mediana = data.median()
        moda    = data.mode()[0]

        self.figura_actual, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Título editorial a nivel de figura
        self.figura_actual.text(
            0.04, 1.02,
            f"Análisis de la variable: {var}",
            fontsize=20, fontweight='bold', color=_COLOR_TITULO
        )
        self.figura_actual.text(
            0.04, 0.97,
            "Distribución, dispersión y ajuste a la normalidad",
            fontsize=13, color=_COLOR_SUBTITULO, style='italic'
        )

        # --- HISTOGRAMA ---
        sns.histplot(data, kde=True, color=_COLOR_PRINCIPAL,
                     element="step", alpha=0.4, ax=axes[0], bins="fd", zorder=2)
        axes[0].axvline(media,   color='#e74c3c', linestyle='--', lw=1.5, label=f'Media: {media:.2f}')
        axes[0].axvline(mediana, color='#27ae60', linestyle='-',  lw=1.5, label=f'Mediana: {mediana:.2f}')
        axes[0].axvline(moda,    color='#f39c12', linestyle=':',  lw=1.5, label=f'Moda: {moda:.2f}')
        axes[0].legend(frameon=False, fontsize=10)
        _configurar_ejes(axes[0], titulo="Histograma", subtitulo="Distribución y tendencia central")

        # --- BOXPLOT ---
        sns.boxplot(y=data, ax=axes[1], color=_COLOR_PRINCIPAL,
                    width=0.3, linewidth=1.5, fliersize=5, zorder=2)
        axes[1].plot(0, media, marker='D', color='#e74c3c',
                     markersize=8, label='Media', zorder=3)
        axes[1].legend(frameon=False, fontsize=10)
        _configurar_ejes(axes[1], titulo="Boxplot", subtitulo="Detección de outliers")

        # --- QQ-PLOT ---
        stats.probplot(data, dist="norm", plot=axes[2])
        axes[2].get_lines()[0].set(markerfacecolor=_COLOR_PRINCIPAL,
                                    markeredgecolor='white', markersize=5, alpha=0.6)
        axes[2].get_lines()[1].set(color='#e74c3c', lw=2)
        _configurar_ejes(axes[2], titulo="QQ-Plot", subtitulo="Ajuste a la distribución normal")

        plt.subplots_adjust(top=0.88, wspace=0.28, left=0.06, right=0.97, bottom=0.10)
        plt.show()

    def scatter_plot(self,
                     data: pd.DataFrame,
                     x: str,
                     y: str,
                     x_title: str = None,
                     y_title: str = None,
                     main_title: str = None,
                     subtitulo: str = None) -> None:
        """Genera un gráfico de dispersión para observar la relación entre 2 variables."""

        _aplicar_estilo_editorial()
        self.figura_actual, ax = plt.subplots(figsize=(10, 6))

        sns.regplot(
            data=data,
            x=x,
            y=y,
            ax=ax,
            scatter_kws={
                'alpha': 0.6,
                's': 70,
                'color': _COLOR_PRINCIPAL,
                'edgecolors': 'white',
                'linewidths': 0.6,
                'zorder': 2
            },
            line_kws={'color': '#e74c3c', 'lw': 2}
        )

        _configurar_ejes(
            ax,
            titulo=main_title or f'Relación entre {x} y {y}',
            subtitulo=subtitulo or "Línea de tendencia con intervalo de confianza al 95%",
            etiqueta_x=x_title or x,
            etiqueta_y=y_title or y
        )

        plt.tight_layout()
        plt.show()

    def box_plot_para_atipicos(self, data: pd.DataFrame, var: str) -> None:
        """Boxplot con anotación del porcentaje de valores atípicos."""

        porcentaje = Graficador.calcular_porcentaje_atipicos(data, var, screen=False)

        _aplicar_estilo_editorial()
        self.figura_actual, ax = plt.subplots(figsize=(10, 6), dpi=100)

        sns.boxplot(
            data=data,
            y=var,
            color=_COLOR_PRINCIPAL,
            width=0.4,
            linewidth=1.5,
            fliersize=5,
            showmeans=True,
            meanprops={
                "marker": "o",
                "markerfacecolor": "white",
                "markeredgecolor": "#2c3e50",
                "markersize": 7
            },
            ax=ax,
            zorder=2
        )

        # Anotación de porcentaje de outliers (estilo editorial)
        ax.text(
            0.97, 0.97,
            f'Outliers: {porcentaje:.2f}%',
            transform=ax.transAxes,
            fontsize=12, fontweight='bold',
            color=_COLOR_TITULO,
            verticalalignment='top',
            horizontalalignment='right',
            style='italic',
            bbox=dict(
                boxstyle='round,pad=0.5',
                facecolor='white',
                edgecolor=_COLOR_GRILLA,
                alpha=0.9
            )
        )

        _configurar_ejes(
            ax,
            titulo=f'Detección de outliers — {var}',
            subtitulo="Método intercuartílico (IQR × 1.5) · ◆ indica la media"
        )

        plt.tight_layout()
        plt.show()
