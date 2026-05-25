"""
Módulo de Visualización de Datos
Generación de gráficos con Matplotlib y Seaborn para análisis del Manifestation Journal
"""

import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI para servidor
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64
from pathlib import Path
from datetime import datetime
import io


# Configurar estilo de gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class VisualizadorDatos:
    """Clase para generar visualizaciones de datos del diario"""
    
    def __init__(self, output_dir='reportes'):
        """
        Inicializar el visualizador
        
        Args:
            output_dir (str): Directorio para guardar reportes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def graficar_frecuencia(self, dataframe, columna, titulo=None, top_n=15):
        """
        Generar gráfico de barras mostrando elementos más comunes
        Responde: ¿Cuáles son los elementos más frecuentes?
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            columna (str): Nombre de la columna a analizar
            titulo (str): Título del gráfico
            top_n (int): Top N elementos a mostrar
            
        Returns:
            dict: Contiene 'base64' (imagen en base64) y metadatos
        """
        try:
            if dataframe.empty:
                return {'base64': None, 'error': 'DataFrame vacío'}
            
            # Contar frecuencias
            frecuencias = dataframe[columna].value_counts().head(top_n)
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(12, 6))
            colores = plt.cm.Spectral(np.linspace(0, 1, len(frecuencias)))
            bars = ax.bar(range(len(frecuencias)), frecuencias.values, color=colores, edgecolor='black', alpha=0.8)
            
            # Configurar etiquetas
            ax.set_xlabel(columna, fontsize=12, fontweight='bold')
            ax.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
            ax.set_title(titulo or f'Análisis de Frecuencia: {columna}', fontsize=14, fontweight='bold', pad=20)
            ax.set_xticks(range(len(frecuencias)))
            ax.set_xticklabels(frecuencias.index, rotation=45, ha='right')
            
            # Añadir valores en las barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            resultado = self._guardar_grafico(fig, f'frecuencia_{columna}_{self.timestamp}')
            resultado['tipo'] = 'barras'
            resultado['columna'] = columna
            resultado['elementos'] = len(frecuencias)
            return resultado
            
        except Exception as e:
            print(f"Error en graficar_frecuencia: {str(e)}")
            return {'base64': None, 'error': str(e)}
    
    def graficar_tendencia_temporal(self, dataframe, fecha_columna='createdAt', 
                                   valor_columna=None, titulo=None):
        """
        Generar gráfico de tendencia temporal
        Responde: ¿Cuál es la tendencia a lo largo del tiempo?
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            fecha_columna (str): Nombre de la columna de fecha
            valor_columna (str): Nombre de la columna con valores (si es None, cuenta registros)
            titulo (str): Título del gráfico
            
        Returns:
            dict: Contiene 'base64' y metadatos
        """
        try:
            if dataframe.empty:
                return {'base64': None, 'error': 'DataFrame vacío'}
            
            # Convertir a datetime
            df_copy = dataframe.copy()
            df_copy[fecha_columna] = pd.to_datetime(df_copy[fecha_columna])
            df_copy = df_copy.sort_values(fecha_columna)
            
            # Agrupar por fecha
            if valor_columna and valor_columna in df_copy.columns:
                tendencia = df_copy.groupby(df_copy[fecha_columna].dt.date)[valor_columna].sum()
                label_y = valor_columna
            else:
                tendencia = df_copy.groupby(df_copy[fecha_columna].dt.date).size()
                label_y = 'Cantidad de Registros'
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.plot(tendencia.index, tendencia.values, marker='o', linestyle='-', 
                    color='#6B4C9A', linewidth=2.5, markersize=8)
            ax.fill_between(range(len(tendencia)), tendencia.values, alpha=0.3, color='#6B4C9A')
            
            # Configurar etiquetas
            ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
            ax.set_ylabel(label_y, fontsize=12, fontweight='bold')
            ax.set_title(titulo or 'Análisis de Tendencia Temporal', fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            resultado = self._guardar_grafico(fig, f'tendencia_{self.timestamp}')
            resultado['tipo'] = 'linea'
            resultado['fecha_columna'] = fecha_columna
            return resultado
            
        except Exception as e:
            print(f"Error en graficar_tendencia_temporal: {str(e)}")
            return {'base64': None, 'error': str(e)}
    
    def graficar_distribucion(self, dataframe, columna, titulo=None):
        """
        Generar gráfico de distribución (histograma)
        Responde: ¿Cómo se distribuyen los datos?
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            columna (str): Nombre de la columna numérica
            titulo (str): Título del gráfico
            
        Returns:
            dict: Contiene 'base64' y metadatos
        """
        try:
            if dataframe.empty:
                return {'base64': None, 'error': 'DataFrame vacío'}
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(12, 6))
            df_clean = dataframe[columna].dropna()
            
            n, bins, patches = ax.hist(df_clean, bins=25, color='#8B7BA8', edgecolor='black', alpha=0.7)
            
            # Colorear gradualmente las barras
            cm = plt.cm.Blues
            for i, patch in enumerate(patches):
                patch.set_facecolor(cm(0.4 + 0.6 * i / len(patches)))
            
            ax.set_xlabel(columna, fontsize=12, fontweight='bold')
            ax.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
            ax.set_title(titulo or f'Distribución de {columna}', fontsize=14, fontweight='bold', pad=20)
            
            # Añadir línea de media y mediana
            media = df_clean.mean()
            mediana = df_clean.median()
            ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.2f}')
            ax.axvline(mediana, color='green', linestyle='--', linewidth=2, label=f'Mediana: {mediana:.2f}')
            
            ax.legend(loc='upper right')
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            resultado = self._guardar_grafico(fig, f'distribucion_{columna}_{self.timestamp}')
            resultado['tipo'] = 'histograma'
            resultado['media'] = float(media)
            resultado['mediana'] = float(mediana)
            resultado['std'] = float(df_clean.std())
            return resultado
            
        except Exception as e:
            print(f"Error en graficar_distribucion: {str(e)}")
            return {'base64': None, 'error': str(e)}
    
    def graficar_correlacion(self, dataframe, titulo=None):
        """
        Generar mapa de calor de correlación
        Responde: ¿Cuáles variables están correlacionadas?
        
        Args:
            dataframe (pd.DataFrame): DataFrame con datos numéricos
            titulo (str): Título del gráfico
            
        Returns:
            dict: Contiene 'base64' y metadatos
        """
        try:
            if dataframe.empty:
                return {'base64': None, 'error': 'DataFrame vacío'}
            
            # Seleccionar solo columnas numéricas
            df_numeric = dataframe.select_dtypes(include=['number'])
            
            if df_numeric.empty or len(df_numeric.columns) < 2:
                return {'base64': None, 'error': 'No hay suficientes columnas numéricas'}
            
            # Calcular correlación
            correlacion = df_numeric.corr()
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(correlacion, annot=True, fmt='.2f', cmap='coolwarm', 
                       center=0, ax=ax, cbar_kws={'label': 'Correlación'},
                       vmin=-1, vmax=1, linewidths=1, linecolor='gray')
            ax.set_title(titulo or 'Matriz de Correlación', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            
            resultado = self._guardar_grafico(fig, f'correlacion_{self.timestamp}')
            resultado['tipo'] = 'heatmap'
            resultado['variables'] = len(correlacion)
            return resultado
            
        except Exception as e:
            print(f"Error en graficar_correlacion: {str(e)}")
            return {'base64': None, 'error': str(e)}
    
    def graficar_pastel(self, dataframe, columna, titulo=None, top_n=8):
        """
        Generar gráfico de pastel
        Responde: ¿Cuál es la proporción de cada elemento?
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            columna (str): Nombre de la columna a analizar
            titulo (str): Título del gráfico
            top_n (int): Top N elementos a mostrar
            
        Returns:
            dict: Contiene 'base64' y metadatos
        """
        try:
            if dataframe.empty:
                return {'base64': None, 'error': 'DataFrame vacío'}
            
            # Contar valores
            conteos = dataframe[columna].value_counts().head(top_n)
            otros = dataframe[columna].value_counts()[top_n:].sum()
            
            if otros > 0:
                conteos = pd.concat([conteos, pd.Series({'Otros': otros})])
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = plt.cm.Spectral(np.linspace(0, 1, len(conteos)))
            wedges, texts, autotexts = ax.pie(conteos.values, labels=conteos.index, 
                                               autopct='%1.1f%%', colors=colors,
                                               startangle=90, textprops={'fontsize': 10})
            
            # Mejorar formato
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(11)
            
            ax.set_title(titulo or f'Distribución de {columna}', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            
            resultado = self._guardar_grafico(fig, f'pastel_{columna}_{self.timestamp}')
            resultado['tipo'] = 'pastel'
            resultado['columna'] = columna
            return resultado
            
        except Exception as e:
            print(f"Error en graficar_pastel: {str(e)}")
            return {'base64': None, 'error': str(e)}
    
    def graficar_comparacion_grupos(self, dataframe, columna_y, columna_x, titulo=None):
        """
        Generar gráfico de comparación entre grupos
        Responde: ¿Cómo varían los valores según diferentes grupos?
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            columna_y (str): Columna con valores numéricos
            columna_x (str): Columna de agrupación
            titulo (str): Título del gráfico
            
        Returns:
            dict: Contiene 'base64' y metadatos
        """
        try:
            if dataframe.empty:
                return {'base64': None, 'error': 'DataFrame vacío'}
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            sns.boxplot(data=dataframe, x=columna_x, y=columna_y, ax=ax, palette='Set2')
            sns.stripplot(data=dataframe, x=columna_x, y=columna_y, ax=ax, 
                         color='black', alpha=0.4, size=5)
            
            ax.set_title(titulo or f'Comparación de {columna_y} por {columna_x}', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel(columna_x, fontsize=12, fontweight='bold')
            ax.set_ylabel(columna_y, fontsize=12, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            resultado = self._guardar_grafico(fig, f'comparacion_{self.timestamp}')
            resultado['tipo'] = 'boxplot'
            resultado['columna_x'] = columna_x
            resultado['columna_y'] = columna_y
            return resultado
            
        except Exception as e:
            print(f"Error en graficar_comparacion_grupos: {str(e)}")
            return {'base64': None, 'error': str(e)}
    
    def _guardar_grafico(self, fig, nombre_base):
        """
        Guardar gráfico en archivo y convertir a base64
        
        Args:
            fig: Figura de matplotlib
            nombre_base (str): Nombre base del archivo
            
        Returns:
            dict: Contiene 'base64' (string) y metadatos
        """
        try:
            # Guardar como PNG
            png_path = self.output_dir / f'{nombre_base}.png'
            fig.savefig(png_path, dpi=150, bbox_inches='tight', facecolor='white')
            
            # Convertir a base64
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            
            plt.close(fig)
            
            return {
                'base64': image_base64,
                'path': str(png_path),
                'nombre': f'{nombre_base}.png'
            }
        except Exception as e:
            plt.close(fig)
            return {'base64': None, 'path': None, 'error': str(e)}
    
    def generar_reporte_completo(self, dataframe, titulo_reporte='Reporte de Análisis'):
        """
        Generar reporte múltiple con varios gráficos
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            titulo_reporte (str): Título del reporte
            
        Returns:
            dict: Contiene información de todos los gráficos generados
        """
        reporte = {
            'titulo': titulo_reporte,
            'timestamp': datetime.now().isoformat(),
            'estadisticas': {
                'total_registros': len(dataframe),
                'total_columnas': len(dataframe.columns),
                'columnas': list(dataframe.columns)
            },
            'graficos': {}
        }
        
        # Generar gráficos para columnas categóricas
        for columna in dataframe.select_dtypes(include=['object']).columns[:3]:
            if dataframe[columna].nunique() <= 20:
                reporte['graficos'][f'frecuencia_{columna}'] = \
                    self.graficar_frecuencia(dataframe, columna)
                reporte['graficos'][f'pastel_{columna}'] = \
                    self.graficar_pastel(dataframe, columna)
        
        # Generar gráficos para columnas numéricas
        for columna in dataframe.select_dtypes(include=['number']).columns[:3]:
            if dataframe[columna].nunique() > 1:
                reporte['graficos'][f'distribucion_{columna}'] = \
                    self.graficar_distribucion(dataframe, columna)
        
        # Gráfico de correlación si hay múltiples numéricas
        if len(dataframe.select_dtypes(include=['number']).columns) >= 2:
            reporte['graficos']['correlacion'] = self.graficar_correlacion(dataframe)
        
        return reporte


def crear_visualizador():
    """Factory para crear instancia del visualizador"""
    return VisualizadorDatos()

