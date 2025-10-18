# Seguridad y desarrollo

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Análisis sobre el índice de desarrollo y seguridad por entidad federativa (estado) de México

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

### 3. Descarga y procesamiento de datos

Los datos se descargan desde las siguientes fuentes oficiales:
1. **INEGI**: Percepción de inseguridad, indicadores de educación y número de derechohabientes (requiere token de API)
2. **SESNSP**: Incidencia delictiva estatal
3. **Plataforma de Datos Abiertos México – Secretaría de Economía**: Indicadores económicos
4. **CONEVAL**: GINI - indicador de desigualdad

#### Obtener Token de API de INEGI:
1. Visitar: https://www.inegi.org.mx/app/api/indicadores/
2. Registrarse o iniciar sesión
3. Copiar el token proporcionado 

#### Ejecutar script:
```powershell

python main.py

# Es necesario que el token esté definido en el archivo .env local para que el script funcione adecuadamente

```

**Salidas generadas de datos crudos:**
- `data/raw/indicador_inseguridad_estados.csv` - Percepción de inseguridad por estado (2011-2025)
- `data/raw/incidencia_delictiva_estatal_2015_2025.csv` - Incidencia delictiva estatal (2015-2025)
- `data/raw/educacionysalud_raw.csv` - Indicadores de educación y derechohabientes por estado (1990 - 2020)
- `data/raw/gasto_raw.csv` - Gasto público por entidad federativa anual
- `data/raw/ied_raw.csv` - Inversión extranjera directa por entidad federativa trimestral
- `data/raw/coeficiente_gini_desigualdad.csv` - Indicador de desigualdad por entidad federativa (Coeficiente GINI)
- `data/raw/pea_raw.csv` - Población economicamente activa por entidad federativa trimestral
- `data/raw/remesas_raw.csv` - Remesad por entidad federativa trimestral
- `data/raw/salario_raw.csv` - Salario mensual promedio por entidad federativa trimestral
- `data/raw/log_descarga_economia.csv` - Log detallado con fechas, fuentes y descripción de datos de economía
- `data/raw/log_desigualdad_gini.csv` - Log detallado con fechas, fuentes y descripción de datos de desigualdad
- `data/raw/log_descarga_seguridad.txt` - Log detallado con fechas, fuentes y descripción de datos de seguridad
- `references/registro_fuentes_educacionysalud.txt` - Log detallado con fechas, fuentes y descripción de datos de educación y salud



**Salidas generadas de procesamiento de datos:**
- `data/processed/datos_unificados_2015_2020.csv` - Dataset completo procesado


### 5. Exploración de Datos (Opcional)

Notebooks disponibles para análisis exploratorio:

```powershell
# Iniciar Jupyter
jupyter notebook

# Abrir en el navegador:
# Datos de seguridad
# - notebooks/1.0-exploracion_datos_seguridad.ipynb 
# - notebooks/2.0-procesamiento_datos_seguridad.ipynb

# Datos de educación y salud
# - notebooks/1.0-eot-importacion_inegi_edu.ipynb
# - notebooks/2.0-eot-procesar_datos_edu.ipynb

# Datos de desigualdad
# - rezago_social.ipynb

# Datos de economía
# - notebooks/EDA_variables_economicas.ipynb
# - notebooks/Datos_Proyecto.ipynb
```

## 📊 Diccionarios de Datos

Los diccionarios completos se encuentran en `references/`:
- `diccionario_datos_seguridad.md` - Documentación completa de datasets de seguridad
- `diccionario_datos_economia.md` - Documentación completa de datasets de economía
- `diccionario_datos_educacionysalud.md` - Documentación completa de datasets de educación y salud
- `diccionario_desigualdad.md` - Documentación completa de datasets de desigualdad
- Describe estructura de datos raw y procesados
- Incluye validaciones de calidad y reglas de negocio

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

1. **Descarga (Raw)**: 
   - ⬇️  Descarga desde APIs oficiales (INEGI, SESNSP)
   - 💾 Guarda en `data/raw/`
   - 📝 Genera log con metadata completa

2. **Procesamiento (Interim → Processed)**: 
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
| `importacion_inegi_edu.py` | `notebooks/` | Descarga de datos de INEGI de educación | `python notebooks/importacion_inegi_edu.py --token TOKEN` |
| `procesado_inegi_edu.py` | `notebooks/` | Procesamiento y validación de datos | `python notebooks/procesado_inegi_edu.py` |
| `1_variables_economicas_descarga_datos_crudos.py` | `notebooks/` | Descarga de datos de economía | `python notebooks/1_variables_economicas_descarga_datos_crudos.py` |
| `2_variables_economicas_procesar_datos_formateados.py` | `notebooks/` | Procesamiento y validación de datos | `python notebooks/2_variables_economicas_procesar_datos_formateados.py` |
| `descarga_datos_rezago.py` | `notebooks/` | Descarga de datos de desigualdad | `python notebooks/descarga_datos_rezago.py ` |
| `procesar_datos_rezago.py.py` | `notebooks/` | Procesamiento y validación de datos | `python notebooks/procesar_datos_rezago.py.py` |

### Notebooks

| Notebook | Descripción |
|----------|-------------|
| `1.0-exploracion_datos_seguridad.ipynb` | Exploración inicial y visualizaciones |
| `2.0-procesamiento_datos_seguridad.ipynb` | Pruebas de transformaciones |


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

