# 📊 TDV Analytics - Módulo de Visualización v2.0

## 📝 Descripción

Módulo avanzado de **análisis de datos y visualización** para **Manifestation Journal**. Genera gráficos interactivos en **Base64** para integración con React y se conecta con el backend **Spring Boot** (H2).

### 🎯 Características Principales

- ✅ **Análisis Estadístico Completo**: Media, mediana, desviación estándar, correlaciones
- ✅ **Visualización de Datos**: 7+ tipos de gráficos (barras, líneas, pastel, dispersión, etc.)
- ✅ **Generación en Base64**: Imágenes listas para React sin necesidad de archivos
- ✅ **API RESTful**: FastAPI con CORS para integración frontend
- ✅ **Limpieza Automática**: Manejo de valores nulos, duplicados y outliers
- ✅ **Reportes Completos**: Análisis múltiple en una sola solicitud
- ✅ **Integración con Spring Boot**: Sincronización automática con backend Java/H2

---

## 📊 Tipos de Gráficos Disponibles

| Tipo | Nombre | Uso | Endpoint |
|------|--------|-----|----------|
| Barras | `graficar_frecuencia()` | ¿Cuáles elementos son más comunes? | `/graficar/frecuencia` |
| Línea | `graficar_tendencia_temporal()` | ¿Cuál es la tendencia en el tiempo? | `/graficar/tendencia` |
| Histograma | `graficar_distribucion()` | ¿Cómo se distribuyen los datos? | `/graficar/distribucion` |
| Pastel | `graficar_pastel()` | ¿Cuál es la proporción? | `/graficar/pastel` |
| Heatmap | `graficar_correlacion()` | ¿Qué variables están relacionadas? | `/graficar/correlacion` |
| Box Plot | `graficar_comparacion_grupos()` | ¿Cómo se comparan los grupos? | `/graficar/comparacion` |

---

## 🚀 Instalación y Configuración

### 1️⃣ Prerequisitos

- Python 3.8+
- pip (gestor de paquetes)
- Backend Node.js/Spring Boot ejecutándose

### 2️⃣ Instalación

```bash
# Navegar al directorio
cd python-analytics

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Dependencias

Las dependencias están en `requirements.txt`:

```
pandas>=2.2.0              # Manipulación de datos
matplotlib>=3.8.0          # Generación de gráficos
seaborn>=0.13.0           # Gráficos estadísticos
fastapi>=0.109.0          # Framework API
uvicorn>=0.27.0           # Servidor ASGI
python-multipart>=0.0.6   # Carga de archivos
scipy>=1.12.0             # Cálculos científicos
numpy>=1.26.0             # Arrays y matrices
```

---

## 💻 Uso de la API

### Iniciar Servidor

```bash
# Activar entorno virtual
venv\Scripts\activate

# Iniciar API
python -m uvicorn api:app --reload --port 8000
```

**Acceso:**
- 🌐 Documentación interactiva: http://localhost:8000/docs
- 🌐 ReDoc: http://localhost:8000/redoc

### Ejemplos de Solicitudes

#### 1️⃣ Gráfico de Frecuencia

```bash
curl -X POST http://localhost:8000/api/analytics/graficar/frecuencia \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"tipo": "Calma", "fecha": "2024-01-01"},
      {"tipo": "Equilibrio", "fecha": "2024-01-02"},
      {"tipo": "Calma", "fecha": "2024-01-03"}
    ],
    "columna": "tipo",
    "titulo": "Tipos de Contenido Más Populares"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "grafico": {
    "base64": "iVBORw0KGgoAAAANSUhEUgA...",
    "tipo": "barras",
    "columna": "tipo",
    "elementos": 2
  }
}
```

#### 2️⃣ Gráfico de Tendencia Temporal

```bash
curl -X POST http://localhost:8000/api/analytics/graficar/tendencia \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"createdAt": "2024-01-01", "valor": 5},
      {"createdAt": "2024-01-02", "valor": 8},
      {"createdAt": "2024-01-03", "valor": 12}
    ],
    "fecha_columna": "createdAt",
    "titulo": "Evolución de Entradas del Diario"
  }'
```

#### 3️⃣ Gráfico de Distribución

```bash
curl -X POST http://localhost:8000/api/analytics/graficar/distribucion \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"duracion": 15},
      {"duracion": 20},
      {"duracion": 25}
    ],
    "columna": "duracion",
    "titulo": "Distribución de Duración de Sesiones"
  }'
```

#### 4️⃣ Reporte Completo

```bash
curl -X POST http://localhost:8000/api/analytics/reporte \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"tipo": "Calma", "duracion": 15, "fecha": "2024-01-01"},
      {"tipo": "Equilibrio", "duracion": 20, "fecha": "2024-01-02"}
    ],
    "titulo": "Reporte Mensual de Actividad"
  }'
```

---

## 🔗 Integración con React

### Componente React para Mostrar Gráficos

```jsx
import React, { useState, useEffect } from 'react';

export function ReporteVisual() {
  const [graficos, setGraficos] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/analytics/reporte', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        registros: [
          { tipo: 'Calma', duracion: 15 },
          { tipo: 'Equilibrio', duracion: 20 }
        ]
      })
    })
      .then(res => res.json())
      .then(data => {
        setGraficos(data.reporte.graficos);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando gráficos...</p>;

  return (
    <div className="graficos">
      {Object.entries(graficos).map(([key, grafico]) => (
        <div key={key} className="grafico">
          <h3>{grafico.descripcion}</h3>
          <img 
            src={`data:image/png;base64,${grafico.base64}`} 
            alt={grafico.descripcion}
          />
        </div>
      ))}
    </div>
  );
}
```

---

## 🔄 Integración con Backend Spring Boot

### Flujo de Datos

```
React Frontend
    ↓
Python Analytics API (puerto 8000)
    ↓
Backend Spring Boot (puerto 5000) + H2
    ↓
Base de Datos H2
```

### Endpoints del Backend para Sincronización

1. **GET** `/api/diary` - Obtener entradas del diario
2. **POST** `/api/analytics/reporte` - Generar reporte
3. **GET** `/api/analytics/graficos/{tipo}` - Obtener gráficos específicos

---

## 📋 Resultados y Hallazgos Clave

### Preguntas que Responden los Gráficos

- ❓ **¿Cuál es el contenido más popular?** → Gráfico de Frecuencia
- ❓ **¿Ha cambiado el uso con el tiempo?** → Gráfico de Tendencia Temporal
- ❓ **¿Cómo se distribuyen las sesiones?** → Histograma de Distribución
- ❓ **¿Qué proporciones tiene cada tipo?** → Gráfico de Pastel
- ❓ **¿Hay correlación entre variables?** → Heatmap de Correlación
- ❓ **¿Cómo se comparan diferentes grupos?** → Box Plot

### Ejemplo de Análisis

**Dataset:** 1000 registros de usuarios (enero-marzo 2024)

- **60%** interacciones: Contenido "Calma"
- **25%** interacciones: Contenido "Equilibrio"
- **15%** interacciones: Otras categorías
- **Pico horario:** 6:00-9:00 AM
- **Tendencia:** +15% semanal en "Espacios Sagrados"

---

## 🐍 Ejemplo Programático

### Uso Directo en Python

```python
import pandas as pd
from visualizacion import crear_visualizador
from analisis import AnalizadorDatos

# Crear datos
datos = {
    'tipo': ['Calma', 'Equilibrio', 'Calma', 'Energía'],
    'duracion': [15, 20, 18, 25],
    'fecha': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']
}
df = pd.DataFrame(datos)

# Analizar
analizador = AnalizadorDatos()
analizador.cargar_datos(dataframe=df)
analizador.limpiar_datos()

# Visualizar
viz = crear_visualizador()

# Gráfico de frecuencia
result_freq = viz.graficar_frecuencia(df, 'tipo', titulo='Tipos de Contenido')
print(f"Gráfico guardado: {result_freq['path']}")

# Gráfico de distribución
result_dist = viz.graficar_distribucion(df, 'duracion')
print(f"Base64: {result_dist['base64'][:50]}...")

# Reporte completo
reporte = viz.generar_reporte_completo(df, 'Mi Reporte')
print(f"Total gráficos: {len(reporte['graficos'])}")
```

---

## 📁 Estructura Actualizada

```
python-analytics/
├── __init__.py                  # Módulo principal
├── analisis.py                  # Análisis estadístico
├── visualizacion.py             # ✨ Visualización mejorada v2.0
├── reporte.py                   # ✨ Reportes para Frontend
├── api.py                       # ✨ API mejorada con más endpoints
├── ejemplo.py                   # Ejemplos de uso
├── requirements.txt             # Dependencias
├── README.md                    # Este archivo
└── reportes/                    # Gráficos generados
    ├── frecuencia_*.png
    ├── distribucion_*.png
    ├── correlacion_*.png
    └── tendencia_*.png
```

---

## 🔄 GitFlow y Rama Feature

### Crear Rama Feature

```bash
# Crear rama desde develop
git checkout develop
git pull origin develop
git checkout -b feature/reporte-visual

# Hacer cambios...
git add .
git commit -m "feat: agregar visualización de gráficos en Base64"

# Push a feature
git push origin feature/reporte-visual

# Crear Pull Request en GitHub
# Esperar revisión y merge a develop
```

---

## 🐛 Resolución de Problemas

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | Activar venv: `venv\Scripts\activate` |
| Puerto 8000 ocupado | `python -m uvicorn api:app --port 8001` |
| Error matplotlib | `pip install --upgrade matplotlib` |
| CORS error en React | Ya configurado, verificar URL del backend |

---

## 📚 Documentación

- **API Swagger:** http://localhost:8000/docs
- **Análisis Detallado:** Ver archivo `analisis.py`
- **Ejemplos:** Ver archivo `ejemplo.py`

---

## 📦 Entregables (Momento 3)

✅ Módulo `visualizacion.py` - 6+ funciones de gráficos
✅ Generador de reportes con Base64
✅ API FastAPI mejorada con múltiples endpoints
✅ Integración con React (componentes de ejemplo)
✅ Rama feature y Pull Request
✅ Documentación completa
✅ Conexión con Spring Boot/H2

---

## 👨‍💻 Autor

**TDV Project** - Manifestation Journal Analytics Module
**Versión:** 2.0.0
**Última actualización:** Enero 2024
- Python 3.8+
- pip

### Pasos

1. **Navegar al directorio**
```bash
cd python-analytics
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Opción 1: Ejecutar Ejemplos

```bash
python ejemplo.py
```

Esto generará:
- Análisis de datos
- 4 gráficos diferentes
- Reporte HTML interactivo
- Detección de outliers

### Opción 2: Usar como Librería

```python
from analisis import crear_analizador
from visualizacion import crear_visualizador
from reporte import crear_generador
import pandas as pd

# Cargar datos
df = pd.read_csv('datos.csv')

# Análisis
analizador = crear_analizador()
analizador.cargar_datos(dataframe=df)
analizador.limpiar_datos()
stats = analizador.obtener_estadisticas_descriptivas()

# Visualización
visualizador = crear_visualizador()
resultado = visualizador.graficar_frecuencia(df, 'columna')

# Reporte
generador = crear_generador()
reporte = generador.crear_respuesta_api(df, 'Mi Análisis')
```

### Opción 3: Ejecutar API

```bash
python -m uvicorn api:app --reload --port 8000
```

API disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

## 🔌 Endpoints de la API

### POST `/analizar`
Analizar datos en formato JSON

```bash
curl -X POST "http://localhost:8000/analizar" \
  -H "Content-Type: application/json" \
  -d '{"registros": [{"nombre": "John", "edad": 30}, {"nombre": "Jane", "edad": 25}]}'
```

### POST `/graficar`
Generar un gráfico específico

```bash
curl -X POST "http://localhost:8000/graficar" \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [...],
    "tipo": "frecuencia",
    "columna": "categoria",
    "titulo": "Mi Gráfico"
  }'
```

**Tipos disponibles:** `frecuencia`, `distribucion`, `correlacion`, `pastel`, `box`, `tendencia`

### POST `/reporte`
Generar reporte completo

```bash
curl -X POST "http://localhost:8000/reporte" \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [...],
    "titulo": "Análisis Visual",
    "formato": "json"
  }'
```

### POST `/cargar-csv`
Cargar y analizar archivo CSV

```bash
curl -X POST "http://localhost:8000/cargar-csv" \
  -F "file=@datos.csv"
```

### POST `/outliers`
Detectar valores atípicos

```bash
curl -X POST "http://localhost:8000/outliers" \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [...],
    "columna": "precio",
    "metodo": "iqr"
  }'
```

### POST `/tendencias`
Analizar tendencias temporales

```bash
curl -X POST "http://localhost:8000/tendencias" \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [...],
    "fecha_columna": "createdAt",
    "valor_columna": "puntuacion"
  }'
```

## 🎨 Respuesta de Gráficos

Todos los gráficos se devuelven en Base64-PNG:

```json
{
  "success": true,
  "grafico": {
    "tipo": "frecuencia",
    "imagen_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAA...",
    "nombre": "frecuencia_categoria_20231122_143022.png"
  }
}
```

**Para usar en React/JavaScript:**
```javascript
const imagenSrc = `data:image/png;base64,${respuesta.grafico.imagen_base64}`;
<img src={imagenSrc} alt="Gráfico" />
```

## 📊 Ejemplos de Análisis

### Análisis de Diario Personal

```python
from reporte import crear_generador

datos_diario = [
    {"fecha": "2024-01-01", "categoria": "Manifestación", "estado": "completado", "puntuacion": 8},
    {"fecha": "2024-01-02", "categoria": "Gratitud", "estado": "completado", "puntuacion": 9},
    # ...
]

generador = crear_generador()
reporte = generador.crear_respuesta_api(datos_diario, "Análisis de Enero")
```

### Gráfico de Tendencia Semanal

```python
from visualizacion import crear_visualizador
import pandas as pd

visualizador = crear_visualizador()
df = pd.DataFrame(datos)
resultado = visualizador.graficar_tendencia_temporal(
    df, 
    fecha_columna='createdAt',
    valor_columna=None,  # Contar registros
    titulo='Registros por Día'
)
```

## 🔄 Integración con Backend Node.js

El módulo está diseñado para funcionar con el backend Express.js:

1. **Backend Node.js** (`puerto 5000`): Maneja autenticación y datos de usuarios
2. **API Python** (`puerto 8000`): Procesa análisis y gráficos
3. **Frontend React** (TDV-BACK-2): Consume ambas APIs

**Flujo:**
```
React → Node.js API (datos) → Python API (análisis) → Gráficos Base64 → React
```

## 🔐 Seguridad

- CORS habilitado (personalizar en producción)
- Validación de entrada en todos los endpoints
- Manejo de errores con traceback
- Datos procesados en memoria (no persistencia)

## 📝 Notas Importantes

- Los gráficos se generan en formato PNG y se codifican en Base64
- Los archivos también se guardan en el directorio `reportes/`
- El módulo maneja automáticamente valores nulos y duplicados
- Soporta análisis con múltiples tipos de datos (numéricos, categóricos, fechas)

## 🆘 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install -r requirements.txt
```

### Error de CORS
Asegurate de que ambas APIs (Node.js y Python) estén ejecutándose:
- Node.js: `http://localhost:5000`
- Python: `http://localhost:8000`

### Gráficos no se generan
Verifica que el directorio `reportes/` exista:
```bash
mkdir reportes
```

## 📚 Documentación Completa

Para más información sobre cada módulo, revisa los comentarios en:
- `analisis.py`: Análisis estadístico
- `visualizacion.py`: Generación de gráficos
- `reporte.py`: Reportes e integración
- `api.py`: Endpoints REST

## 🤝 Contribuciones

Sugerencias y mejoras bienvenidas.

## 📄 Licencia

MIT
