"""
API FastAPI para integración de análisis visual
Conecta Backend con módulo Python de visualización
Entrega gráficos en Base64 para React
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import json
from datetime import datetime
from pathlib import Path
import traceback
import logging

from visualizacion import VisualizadorDatos, crear_visualizador
from analisis import AnalizadorDatos
from reporte import GeneradorReportes

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="TDV Analytics API",
    description="API de análisis y visualización para Manifestation Journal",
    version="2.0.0"
)

# Configurar CORS para conectar con React y backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear instancias
visualizador = crear_visualizador()
analizador = AnalizadorDatos()
generador = GeneradorReportes()

# ===== RUTAS DE SALUD =====
@app.get("/")
def root():
    """Ruta raíz - Información de la API"""
    return {
        "message": "TDV Analytics API v2.0",
        "version": "2.0.0",
        "descripcion": "API de análisis y visualización de datos para Manifestation Journal",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "analisis": "/api/analytics/analizar",
            "frecuencia": "/api/analytics/graficar/frecuencia",
            "distribucion": "/api/analytics/graficar/distribucion",
            "tendencia": "/api/analytics/graficar/tendencia",
            "correlacion": "/api/analytics/graficar/correlacion",
            "reporte_completo": "/api/analytics/reporte"
        }
    }


@app.get("/health")
@app.get("/api/health")
def health():
    """Health check - Verifica que la API está funcionando"""
    return {
        "status": "healthy",
        "service": "TDV Analytics",
        "timestamp": datetime.now().isoformat()
    }


# ===== RUTAS DE ANÁLISIS =====
@app.post("/api/analytics/analizar")
async def analizar_datos(datos: dict):
    """
    Realizar análisis estadístico de datos
    
    Body: {
        "registros": [{...}, {...}]
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere campo 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        analizador.cargar_datos(dataframe=df)
        analizador.limpiar_datos()
        
        estadisticas = analizador.obtener_estadisticas_descriptivas()
        
        logger.info(f"Análisis completado: {len(df)} registros procesados")
        
        return {
            "success": True,
            "estadisticas": estadisticas,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en análisis: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== RUTAS DE GRÁFICOS =====

@app.post("/api/analytics/graficar/frecuencia")
async def graficar_frecuencia_endpoint(datos: dict):
    """
    Generar gráfico de frecuencia
    
    Body: {
        "registros": [{...}, {...}],
        "columna": "nombre_columna",
        "titulo": "Mi Título (opcional)",
        "top_n": 15
    }
    """
    try:
        if not datos.get("registros") or not datos.get("columna"):
            raise HTTPException(status_code=400, detail="Se requieren 'registros' y 'columna'")
        
        df = pd.DataFrame(datos["registros"])
        columna = datos.get("columna")
        titulo = datos.get("titulo", f"Análisis de Frecuencia: {columna}")
        top_n = datos.get("top_n", 15)
        
        resultado = visualizador.graficar_frecuencia(df, columna, titulo, top_n)
        
        logger.info(f"Gráfico de frecuencia generado para {columna}")
        
        return {
            "success": True,
            "grafico": resultado,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en gráfico de frecuencia: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/analytics/graficar/distribucion")
async def graficar_distribucion_endpoint(datos: dict):
    """
    Generar gráfico de distribución
    
    Body: {
        "registros": [{...}, {...}],
        "columna": "nombre_columna_numerica",
        "titulo": "Mi Título (opcional)"
    }
    """
    try:
        if not datos.get("registros") or not datos.get("columna"):
            raise HTTPException(status_code=400, detail="Se requieren 'registros' y 'columna'")
        
        df = pd.DataFrame(datos["registros"])
        columna = datos.get("columna")
        titulo = datos.get("titulo", f"Distribución: {columna}")
        
        resultado = visualizador.graficar_distribucion(df, columna, titulo)
        
        logger.info(f"Gráfico de distribución generado para {columna}")
        
        return {
            "success": True,
            "grafico": resultado,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en gráfico de distribución: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/analytics/graficar/tendencia")
async def graficar_tendencia_endpoint(datos: dict):
    """
    Generar gráfico de tendencia temporal
    
    Body: {
        "registros": [{...}, {...}],
        "fecha_columna": "createdAt",
        "valor_columna": "valor (opcional)",
        "titulo": "Mi Título (opcional)"
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requieren 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        fecha_columna = datos.get("fecha_columna", "createdAt")
        valor_columna = datos.get("valor_columna")
        titulo = datos.get("titulo", "Tendencia Temporal")
        
        resultado = visualizador.graficar_tendencia_temporal(df, fecha_columna, valor_columna, titulo)
        
        logger.info(f"Gráfico de tendencia generado")
        
        return {
            "success": True,
            "grafico": resultado,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en gráfico de tendencia: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/analytics/graficar/correlacion")
async def graficar_correlacion_endpoint(datos: dict):
    """
    Generar gráfico de correlación
    
    Body: {
        "registros": [{...}, {...}],
        "titulo": "Mi Título (opcional)"
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requieren 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        titulo = datos.get("titulo", "Matriz de Correlación")
        
        resultado = visualizador.graficar_correlacion(df, titulo)
        
        logger.info(f"Gráfico de correlación generado")
        
        return {
            "success": True,
            "grafico": resultado,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en gráfico de correlación: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/analytics/graficar/pastel")
async def graficar_pastel_endpoint(datos: dict):
    """
    Generar gráfico de pastel
    
    Body: {
        "registros": [{...}, {...}],
        "columna": "nombre_columna",
        "titulo": "Mi Título (opcional)",
        "top_n": 8
    }
    """
    try:
        if not datos.get("registros") or not datos.get("columna"):
            raise HTTPException(status_code=400, detail="Se requieren 'registros' y 'columna'")
        
        df = pd.DataFrame(datos["registros"])
        columna = datos.get("columna")
        titulo = datos.get("titulo", f"Distribución: {columna}")
        top_n = datos.get("top_n", 8)
        
        resultado = visualizador.graficar_pastel(df, columna, titulo, top_n)
        
        logger.info(f"Gráfico de pastel generado para {columna}")
        
        return {
            "success": True,
            "grafico": resultado,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en gráfico de pastel: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/analytics/graficar/comparacion")
async def graficar_comparacion_endpoint(datos: dict):
    """
    Generar gráfico de comparación entre grupos
    
    Body: {
        "registros": [{...}, {...}],
        "columna_y": "valor_numerico",
        "columna_x": "grupo",
        "titulo": "Mi Título (opcional)"
    }
    """
    try:
        if not datos.get("registros") or not datos.get("columna_y") or not datos.get("columna_x"):
            raise HTTPException(status_code=400, detail="Se requieren 'registros', 'columna_y' y 'columna_x'")
        
        df = pd.DataFrame(datos["registros"])
        columna_y = datos.get("columna_y")
        columna_x = datos.get("columna_x")
        titulo = datos.get("titulo", f"Comparación: {columna_y} por {columna_x}")
        
        resultado = visualizador.graficar_comparacion_grupos(df, columna_y, columna_x, titulo)
        
        logger.info(f"Gráfico de comparación generado")
        
        return {
            "success": True,
            "grafico": resultado,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en gráfico de comparación: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== RUTA DE REPORTE COMPLETO =====

@app.post("/api/analytics/reporte")
async def generar_reporte_endpoint(datos: dict):
    """
    Generar reporte completo con múltiples gráficos
    
    Body: {
        "registros": [{...}, {...}],
        "titulo": "Mi Reporte (opcional)"
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requieren 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        titulo = datos.get("titulo", "Reporte de Análisis Completo")
        
        # Procesar datos
        analizador.cargar_datos(dataframe=df)
        analizador.limpiar_datos()
        df_limpio = analizador.df
        
        # Generar reporte completo
        reporte = visualizador.generar_reporte_completo(df_limpio, titulo)
        
        logger.info(f"Reporte completo generado con {len(reporte['graficos'])} gráficos")
        
        return {
            "success": True,
            "reporte": reporte,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error en reporte: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== RUTA DE CARGA DE CSV =====

@app.post("/api/analytics/cargar-csv")
async def cargar_csv(file: UploadFile = File(...)):
    """
    Cargar y analizar archivo CSV
    """
    try:
        contenido = await file.read()
        df = pd.read_csv(io.StringIO(contenido.decode('utf-8')))
        
        analizador.cargar_datos(dataframe=df)
        analizador.limpiar_datos()
        
        estadisticas = analizador.obtener_estadisticas_descriptivas()
        
        logger.info(f"CSV cargado: {len(df)} registros")
        
        return {
            "success": True,
            "archivo": file.filename,
            "registros": len(df),
            "estadisticas": estadisticas,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error al cargar CSV: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# ===== RUTAS DE TENDENCIAS =====
@app.post("/tendencias")
async def analizar_tendencias(datos: dict):
    """
    Analizar tendencias temporales
    
    Body: {
        "registros": [{...}, {...}],
        "fecha_columna": "createdAt",
        "valor_columna": "campo_valor"
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        analizador.cargar_datos(dataframe=df)
        
        fecha_col = datos.get("fecha_columna", "createdAt")
        valor_col = datos.get("valor_columna")
        
        tendencias = analizador.analizar_tendencias(fecha_col, valor_col)
        
        return {
            "success": True,
            "tendencias": tendencias,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== RUTAS DE INFORMACIÓN =====
@app.post("/columnas-info")
async def info_columnas(datos: dict):
    """
    Obtener información sobre todas las columnas
    
    Body: {
        "registros": [{...}, {...}]
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        analizador.cargar_datos(dataframe=df)
        
        stats = analizador.obtener_estadisticas_descriptivas()
        
        return {
            "success": True,
            "columnas_info": stats["por_columna"],
            "total_columnas": stats["total_columnas"],
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
