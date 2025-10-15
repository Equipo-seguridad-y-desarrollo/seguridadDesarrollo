# Seguridad y desarrollo

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Análisis sobre el índice de desarrollo y seguridad por municipio

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Token de API de INEGI (para datos de seguridad)

### 1. Configuración del Entorno Virtual

#### En Windows (PowerShell):
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### En Linux/Mac:
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

### 2. Instalar Dependencias

```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### 3. Descarga de Datos de Seguridad

Los datos de seguridad se descargan desde dos fuentes oficiales:
1. **INEGI**: Percepción de inseguridad (requiere token de API)
2. **SESNSP**: Incidencia delictiva estatal

#### Obtener Token de API de INEGI:
1. Visitar: https://www.inegi.org.mx/app/api/indicadores/
2. Registrarse o iniciar sesión
3. Copiar el token proporcionado

#### Ejecutar descarga:
```powershell
# Método 1: Pasar token directamente
python notebooks/datos_seguridad_mexico.py --token TU_TOKEN_AQUI

# Método 2: Usar archivo .env (recomendado)
# 1. Crear archivo .env en la raíz del proyecto
# 2. Agregar: INEGI_API_TOKEN=TU_TOKEN_AQUI
# 3. Ejecutar:
python notebooks/datos_seguridad_mexico.py
```

**Salidas generadas:**
- `data/raw/indicador_inseguridad_estados.csv` - Percepción de inseguridad por estado (2011-2025)
- `data/raw/incidencia_delictiva_estatal_2015_2025.csv` - Incidencia delictiva estatal (2015-2025)
- `data/raw/log_descarga_seguridad.txt` - Log detallado con fechas, fuentes y descripción

### 4. Procesamiento de Datos

Transformar los datos raw a formato tidy y validar calidad:

```powershell
python notebooks/procesar_datos_seguridad.py
```

**Salidas generadas:**
- `data/processed/percepcion_inseguridad_procesado.csv` - Dataset completo procesado
- `data/processed/percepcion_inseguridad_estados.csv` - Solo estados (sin nacional)
- `data/processed/incidencia_delictiva_procesado.csv` - Dataset de incidencia procesado
- `data/interim/incidencia_delictiva_completa.csv` - Versión intermedia normalizada
- `data/processed/reporte_procesamiento.txt` - Reporte de validación y estadísticas

### 5. Exploración de Datos (Opcional)

Notebooks disponibles para análisis exploratorio:

```powershell
# Iniciar Jupyter
jupyter notebook

# Abrir en el navegador:
# - notebooks/1.0-exploracion_datos_seguridad.ipynb (Exploración inicial)
# - notebooks/2.0-procesamiento_datos_seguridad.ipynb (Pruebas de transformación)
```

## 📊 Diccionarios de Datos

Los diccionarios completos se encuentran en `references/`:
- `diccionario_datos_seguridad.md` - Documentación completa de datasets de seguridad
- Describe estructura de datos raw y procesados
- Incluye validaciones de calidad y reglas de negocio

## 📁 Estructura del Proyecto

## 📁 Estructura del Proyecto

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   │   └── incidencia_delictiva_completa.csv
│   ├── processed      <- The final, canonical data sets for modeling.
│   │   ├── percepcion_inseguridad_procesado.csv
│   │   ├── percepcion_inseguridad_estados.csv
│   │   ├── incidencia_delictiva_procesado.csv
│   │   └── reporte_procesamiento.txt
│   └── raw            <- The original, immutable data dump.
│       ├── indicador_inseguridad_estados.csv
│       ├── incidencia_delictiva_estatal_2015_2025.csv
│       └── log_descarga_seguridad.txt
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│   ├── 1.0-exploracion_datos_seguridad.ipynb
│   ├── 2.0-procesamiento_datos_seguridad.ipynb
│   ├── datos_seguridad_mexico.py       <- Script de descarga
│   └── procesar_datos_seguridad.py     <- Script de procesamiento
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         Seguridad y desarrollo and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│   └── diccionario_datos_seguridad.md  <- Diccionario completo de datos de seguridad
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── Seguridad y desarrollo   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes Seguridad y desarrollo a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

## 🔧 Flujo de Trabajo de Datos

### Pipeline de Datos de Seguridad

1. **Descarga (Raw)**: `datos_seguridad_mexico.py`
   - ⬇️  Descarga desde APIs oficiales (INEGI, SESNSP)
   - 💾 Guarda en `data/raw/`
   - 📝 Genera log con metadata completa

2. **Procesamiento (Interim → Processed)**: `procesar_datos_seguridad.py`
   - 🧹 Limpia y normaliza datos
   - ✅ Valida calidad (nulos, duplicados, rangos)
   - ➕ Agrega columnas calculadas
   - 💾 Guarda en `data/processed/` y `data/interim/`
   - 📊 Genera reporte de validación

3. **Exploración y Análisis**: Notebooks
   - 🔍 Exploración visual
   - 📈 Análisis estadístico
   - 🧪 Pruebas de transformaciones

### Validaciones de Calidad Implementadas

- ✅ **Valores nulos**: Verificación en columnas críticas
- ✅ **Tipos de datos**: Conversión y validación automática
- ✅ **Rangos válidos**: Detección de valores atípicos
- ✅ **Duplicados**: Identificación por claves únicas
- ✅ **Completitud temporal**: Series de tiempo completas por entidad

## 🧰 Scripts Principales

### Scripts de Datos de Seguridad

| Script | Ubicación | Descripción | Uso |
|--------|-----------|-------------|-----|
| `datos_seguridad_mexico.py` | `notebooks/` | Descarga de datos de INEGI y SESNSP | `python notebooks/datos_seguridad_mexico.py --token TOKEN` |
| `procesar_datos_seguridad.py` | `notebooks/` | Procesamiento y validación de datos | `python notebooks/procesar_datos_seguridad.py` |

### Notebooks

| Notebook | Descripción |
|----------|-------------|
| `1.0-exploracion_datos_seguridad.ipynb` | Exploración inicial y visualizaciones |
| `2.0-procesamiento_datos_seguridad.ipynb` | Pruebas de transformaciones |

## 📚 Fuentes de Datos

### Datos de Seguridad

1. **Percepción de Inseguridad**
   - **Fuente**: INEGI - ENVIPE
   - **Período**: 2011-2025
   - **Cobertura**: Nacional y 32 estados
   - **Actualización**: Anual
   - **API**: https://www.inegi.org.mx/app/api/indicadores/

2. **Incidencia Delictiva**
   - **Fuente**: SESNSP (Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública)
   - **Período**: 2015-2025
   - **Cobertura**: 32 estados
   - **Actualización**: Mensual
   - **URL**: https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Crea un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📞 Soporte

Para preguntas o problemas:
- Revisar documentación en `references/`
- Revisar logs de descarga y procesamiento en `data/raw/` y `data/processed/`
- Abrir un issue en el repositorio

## 📝 Licencia

Ver archivo `LICENSE` para detalles.

--------

