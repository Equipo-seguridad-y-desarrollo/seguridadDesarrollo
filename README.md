# Seguridad y desarrollo

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Analisis sobre el indice de desarrollo y seguridad por municipio

## Configuración del Entorno

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Inicializar el Entorno Virtual

1. **Crear el entorno virtual:**
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual:**
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

### Configurar Variables de Entorno

1. **Copiar el archivo de ejemplo:**
   ```bash
   cp .env.example .env
   ```

2. **Editar el archivo `.env`** y configurar tu token de API de INEGI:
   ```
   INEGI_API_TOKEN=tu_token_aqui
   ```
   
   Para obtener un token de INEGI:
   - Visita: https://www.inegi.org.mx/app/api/
   - Regístrate y solicita un token de desarrollador

## Descarga y Procesamiento de Datos

### Paso 1: Descargar Datos de Seguridad

El script `datos_seguridad_mexico.py` descarga datos de dos fuentes principales:
- Indicador de percepción de inseguridad (INEGI/ENVIPE) 2011-2025
- Incidencia delictiva estatal (SESNSP) 2015-2025

**Ejecutar la descarga:**
```bash
python notebooks/datos_seguridad_mexico.py
```

**Archivos generados en `./data/raw/`:**
- `indicador_inseguridad_estados.csv` - Datos de percepción de inseguridad
- `incidencia_delictiva_estatal_2015_2025.csv` - Datos de incidencia delictiva
- `fuentes_datos_seguridad.txt` - Descripción de las fuentes y metadatos

### Paso 2: Procesar Datos a Formato Tidy

El script `procesar_datos_seguridad.py` transforma los datos crudos en conjuntos de datos tidy con validaciones de calidad.

**Ejecutar el procesamiento:**
```bash
python notebooks/procesar_datos_seguridad.py
```

**Archivos generados:**

En `./data/processed/`:
- `percepcion_inseguridad_tidy.csv` - Datos tidy de percepción de inseguridad
- `incidencia_delictiva_tidy.csv` - Datos tidy de incidencia delictiva (formato largo)
- `incidencia_delictiva_resumen_anual.csv` - Resumen anual agregado por entidad

En `./data/interim/`:
- `incidencia_delictiva_interim.csv` - Datos intermedios con nombres de columnas estandarizados

### Validaciones de Calidad Aplicadas

El script de procesamiento implementa las siguientes validaciones:

1. **Verificación de valores nulos** - Identifica y elimina registros con datos faltantes
2. **Verificación de rangos** - Valida que los años estén en los rangos esperados
3. **Verificación de valores no negativos** - Asegura que los conteos sean positivos
4. **Eliminación de duplicados** - Remueve registros duplicados
5. **Estandarización de tipos de datos** - Convierte valores a los tipos apropiados
6. **Ordenamiento consistente** - Ordena los datos de manera lógica

### Diccionarios de Datos

Los diccionarios de datos detallados están disponibles en `./references/`:

- `diccionario_percepcion_inseguridad.md` - Especificación completa del dataset de percepción de inseguridad
- `diccionario_incidencia_delictiva.md` - Especificación completa del dataset de incidencia delictiva

Estos archivos contienen:
- Descripción de cada columna
- Tipos de datos y rangos válidos
- Definiciones y conceptos
- Fuentes originales
- Limitaciones y consideraciones de calidad
- Ejemplos de uso

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         Seguridad y desarrollo and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
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

--------

