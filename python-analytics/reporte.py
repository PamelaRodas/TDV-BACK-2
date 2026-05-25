"""
Generador de Reportes
Crea reportes visuales en Base64 para integración con React/Frontend
Se conecta con el backend Spring Boot para sincronización de datos
"""

import json
import base64
from io import BytesIO
from datetime import datetime
from pathlib import Path
import pandas as pd
import logging
from visualizacion import VisualizadorDatos, crear_visualizador
from analisis import AnalizadorDatos

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeneradorReportes:
    """Clase para generar reportes visuales e interactivos"""
    
    def __init__(self, output_dir='reportes'):
        """
        Inicializar generador de reportes
        
        Args:
            output_dir (str): Directorio para guardar reportes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.visualizador = crear_visualizador()
        self.analizador = AnalizadorDatos()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"GeneradorReportes inicializado en {output_dir}")
    
    def procesar_datos_para_frontend(self, datos_json=None, archivo_csv=None):
        """
        Procesar datos y generar salida completa para frontend
        Incluye análisis estadísticos y gráficos en Base64
        
        Args:
            datos_json (dict o str): Datos en formato JSON o ruta al archivo
            archivo_csv (str): Ruta a archivo CSV
            
        Returns:
            dict: Datos procesados listos para enviar al frontend (modelo Headless/Pull)
        """
        try:
            # Cargar datos
            if datos_json:
                if isinstance(datos_json, str):
                    with open(datos_json, 'r') as f:
                        datos = json.load(f)
                else:
                    datos = datos_json
                df = pd.DataFrame(datos)
            elif archivo_csv:
                df = pd.read_csv(archivo_csv)
            else:
                raise ValueError('Debe proporcionar datos_json o archivo_csv')
            
            logger.info(f"Procesando {len(df)} registros para reporte")
            
            # Limpiar datos
            self.analizador.cargar_datos(dataframe=df)
            self.analizador.limpiar_datos()
            df_limpio = self.analizador.df
            
            # Generar análisis estadísticos
            estadisticas = self.analizador.obtener_estadisticas_descriptivas()
            
            # Generar gráficos
            graficos = {}
            
            # Frecuencias de columnas categóricas (máx 5)
            for columna in df_limpio.select_dtypes(include=['object']).columns[:5]:
                try:
                    if df_limpio[columna].nunique() <= 15:
                        resultado = self.visualizador.graficar_frecuencia(
                            df_limpio, columna, f'Análisis: {columna}'
                        )
                        if resultado.get('base64'):
                            graficos[f'frecuencia_{columna}'] = {
                                'tipo': 'barras',
                                'imagen_base64': resultado['base64'],
                                'descripcion': f'Frecuencia de {columna}',
                                'columna': columna
                            }
                except Exception as e:
                    logger.warning(f"Error generando gráfico para {columna}: {str(e)}")
            
            # Distribuciones de columnas numéricas (máx 3)
            for columna in df_limpio.select_dtypes(include=['number']).columns[:3]:
                try:
                    resultado = self.visualizador.graficar_distribucion(
                        df_limpio, columna, f'Distribución: {columna}'
                    )
                    if resultado.get('base64'):
                        graficos[f'distribucion_{columna}'] = {
                            'tipo': 'histograma',
                            'imagen_base64': resultado['base64'],
                            'descripcion': f'Distribución de {columna}',
                            'media': resultado.get('media'),
                            'mediana': resultado.get('mediana'),
                            'std': resultado.get('std')
                        }
                except Exception as e:
                    logger.warning(f"Error generando distribución para {columna}: {str(e)}")
            
            # Correlación si hay variables numéricas
            if len(df_limpio.select_dtypes(include=['number']).columns) >= 2:
                try:
                    resultado = self.visualizador.graficar_correlacion(df_limpio)
                    if resultado.get('base64'):
                        graficos['correlacion'] = {
                            'tipo': 'heatmap',
                            'imagen_base64': resultado['base64'],
                            'descripcion': 'Matriz de correlación entre variables'
                        }
                except Exception as e:
                    logger.warning(f"Error generando correlación: {str(e)}")
            
            # Gráficos de pastel para categóricas (máx 3)
            for columna in df_limpio.select_dtypes(include=['object']).columns[:3]:
                try:
                    if df_limpio[columna].nunique() <= 10:
                        resultado = self.visualizador.graficar_pastel(df_limpio, columna)
                        if resultado.get('base64'):
                            graficos[f'pastel_{columna}'] = {
                                'tipo': 'pastel',
                                'imagen_base64': resultado['base64'],
                                'descripcion': f'Proporciones de {columna}',
                                'columna': columna
                            }
                except Exception as e:
                    logger.warning(f"Error generando pastel para {columna}: {str(e)}")
            
            # Construir respuesta
            respuesta = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'estadisticas': estadisticas,
                'graficos': graficos,
                'resumen': {
                    'total_registros': len(df_limpio),
                    'total_graficos': len(graficos),
                    'tipos_graficos': list(set([g.get('tipo') for g in graficos.values()]))
                }
            }
            
            logger.info(f"Reporte generado exitosamente con {len(graficos)} gráficos")
            return respuesta
            
        except Exception as e:
            logger.error(f"Error procesando datos: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def generar_reporte_json_completo(self, dataframe, nombre_reporte='reporte'):
        """
        Generar un reporte completo en JSON con todos los análisis
        
        Args:
            dataframe (pd.DataFrame): DataFrame a analizar
            nombre_reporte (str): Nombre del reporte
            
        Returns:
            dict: Reporte completo con estadísticas y gráficos
        """
        try:
            logger.info(f"Generando reporte JSON: {nombre_reporte}")
            
            # Análisis
            self.analizador.cargar_datos(dataframe=dataframe)
            self.analizador.limpiar_datos()
            estadisticas = self.analizador.obtener_estadisticas_descriptivas()
            
            # Generar gráficos
            reporte_viz = self.visualizador.generar_reporte_completo(dataframe, nombre_reporte)
            
            # Combinar
            reporte_final = {
                'nombre': nombre_reporte,
                'timestamp': datetime.now().isoformat(),
                'estadisticas': estadisticas,
                'graficos': reporte_viz.get('graficos', {})
            }
            
            return reporte_final
        except Exception as e:
            logger.error(f"Error generando reporte JSON: {str(e)}")
            return {'error': str(e)}
        
        # Preparar respuesta para frontend
        reporte_frontend = {
            'id': f'reporte_{self.timestamp}',
            'fecha_generacion': datetime.now().isoformat(),
            'estadisticas': {
                'resumen': {
                    'total_registros': estadisticas['total_registros'],
                    'total_columnas': estadisticas['total_columnas'],
                    'duplicados': estadisticas['duplicados'],
                    'memoria_mb': round(estadisticas['memoria_uso_mb'], 2)
                },
                'por_columna': estadisticas['por_columna']
            },
            'graficos': graficos,
            'metadata': {
                'version': '1.0',
                'formato': 'base64-png',
                'compatibilidad': ['react', 'vue', 'angular']
            }
        }
        
        return reporte_frontend
    
    def generar_reporte_json_con_graficos(self, df, nombre_reporte='reporte'):
        """
        Generar reporte JSON con todas las gráficas codificadas en base64
        
        Args:
            df (pd.DataFrame): DataFrame a reportar
            nombre_reporte (str): Nombre del reporte
            
        Returns:
            dict: Reporte completo con gráficos
        """
        self.analizador.cargar_datos(dataframe=df)
        
        reporte = {
            'nombre': nombre_reporte,
            'fecha': datetime.now().isoformat(),
            'analisis': self.analizador.obtener_resumen(),
            'graficos_base64': {},
            'urls_archivos': {}
        }
        
        # Generar y codificar gráficos
        for columna in df.select_dtypes(include=['object']).columns[:3]:
            if df[columna].nunique() <= 15:
                resultado = self.visualizador.graficar_frecuencia(df, columna)
                if resultado.get('base64'):
                    reporte['graficos_base64'][f'freq_{columna}'] = resultado['base64']
                if resultado.get('path'):
                    reporte['urls_archivos'][f'freq_{columna}'] = resultado['path']
        
        for columna in df.select_dtypes(include=['number']).columns[:2]:
            resultado = self.visualizador.graficar_distribucion(df, columna)
            if resultado.get('base64'):
                reporte['graficos_base64'][f'dist_{columna}'] = resultado['base64']
            if resultado.get('path'):
                reporte['urls_archivos'][f'dist_{columna}'] = resultado['path']
        
        return reporte
    
    def crear_respuesta_api(self, datos, titulo='Análisis Visual'):
        """
        Crear respuesta formatada para API REST
        
        Args:
            datos (dict o pd.DataFrame): Datos a procesar
            titulo (str): Título del reporte
            
        Returns:
            dict: Respuesta formateada para API
        """
        if isinstance(datos, pd.DataFrame):
            df = datos
        else:
            df = pd.DataFrame(datos)
        
        reporte = self.procesar_datos_para_frontend(datos=df.to_dict('records'))
        
        respuesta_api = {
            'success': True,
            'message': 'Reporte generado exitosamente',
            'data': {
                'reporte': reporte,
                'timestamp': datetime.now().isoformat(),
                'estadisticas_generales': {
                    'total_registros_procesados': len(df),
                    'graficos_generados': len(reporte['graficos']),
                    'tiempo_procesamiento': 'calculado en frontend'
                }
            },
            'meta': {
                'version': '1.0',
                'formato': 'JSON + Base64-PNG',
                'compresion': 'none'
            }
        }
        
        return respuesta_api
    
    def exportar_como_html_interactivo(self, datos, nombre_archivo='reporte.html'):
        """
        Exportar reporte como HTML con gráficos incrustados
        
        Args:
            datos (dict o pd.DataFrame): Datos a procesar
            nombre_archivo (str): Nombre del archivo HTML
            
        Returns:
            str: Ruta del archivo creado
        """
        if isinstance(datos, pd.DataFrame):
            df = datos
        else:
            df = pd.DataFrame(datos)
        
        reporte = self.procesar_datos_para_frontend(datos=df.to_dict('records'))
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{reporte.get('id', 'Reporte')}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .stat-card h3 {{
                    margin: 0 0 10px 0;
                    color: #667eea;
                    font-size: 14px;
                    font-weight: 600;
                }}
                .stat-card .value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #333;
                }}
                .graficos-container {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                    gap: 20px;
                }}
                .grafico {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                .grafico h3 {{
                    margin-top: 0;
                    color: #333;
                }}
                .grafico img {{
                    width: 100%;
                    height: auto;
                }}
                .footer {{
                    text-align: center;
                    color: #666;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Reporte de Análisis Visual</h1>
                <p>Generado el: {reporte['fecha_generacion']}</p>
            </div>
            
            <div class="stats-grid">
        """
        
        # Agregar estadísticas
        stats = reporte['estadisticas']['resumen']
        for key, value in stats.items():
            html_content += f"""
                <div class="stat-card">
                    <h3>{key.replace('_', ' ').title()}</h3>
                    <div class="value">{value}</div>
                </div>
            """
        
        html_content += """
            </div>
            
            <h2>📈 Gráficos</h2>
            <div class="graficos-container">
        """
        
        # Agregar gráficos
        for nombre_grafico, datos_grafico in reporte['graficos'].items():
            if datos_grafico.get('imagen_base64'):
                html_content += f"""
                <div class="grafico">
                    <h3>{datos_grafico.get('descripcion', nombre_grafico)}</h3>
                    <img src="data:image/png;base64,{datos_grafico['imagen_base64']}" 
                         alt="{nombre_grafico}">
                </div>
                """
        
        html_content += """
            </div>
            
            <div class="footer">
                <p>Reporte generado automáticamente | Manifestation Journal Analytics</p>
            </div>
        </body>
        </html>
        """
        
        archivo_path = self.output_dir / nombre_archivo
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(archivo_path)


def crear_generador():
    """Factory para crear instancia del generador de reportes"""
    return GeneradorReportes()
