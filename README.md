# Seguridad y desarrollo

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Análisis sobre el índice de desarrollo y seguridad por municipio

## Configuración del Entorno Virtual

Este proyecto utiliza un entorno virtual de Python para gestionar las dependencias. Sigue estos pasos para configurarlo:

### 1. Crear el entorno virtual

```bash
# Opción 1: Usando venv (recomendado)
python3 -m venv venv

# Opción 2: Usando virtualenv
virtualenv venv

# Opción 3: Usando Makefile
make create_environment
```

### 2. Activar el entorno virtual

```bash
# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
# Opción 1: Usando pip directamente
pip install -r requirements.txt

# Opción 2: Usando Makefile
make requirements
```

### 4. Verificar instalación

```bash
python --version  # Debe mostrar Python 3.12.x
pip list          # Debe mostrar todas las dependencias instaladas
```

## Descarga y Procesamiento de Datos

Este proyecto descarga y procesa datos de múltiples fuentes públicas de variables socioeconómicas para todos los estados de México.

### Fuentes de Datos

1. **Economía** (DataMexico API)
   - Inversión Extranjera Directa (IED)
   - Salario Mensual
   - Población Económicamente Activa (PEA)
   - Gasto Público Ejecutado
   - Remesas

2. **Educación y Salud** (INEGI API)
   - Tasa de analfabetismo
   - Grado promedio de escolaridad
   - Niveles educativos
   - Esperanza de vida
   - Mortalidad infantil

### Configuración de API Key

Para descargar datos del INEGI, necesitas configurar la API Key:

```bash
# Crear archivo .env en la raíz del proyecto
echo "INEGI_API_KEY=32805429-135c-9311-70c1-0b963c6f8317" > .env
```

### Ejecución de la Descarga de Datos

```bash
# Opción 1: Usando Makefile (recomendado)
make download

# Opción 2: Ejecutando el script directamente
python notebooks/download_data.py
```

**Salida:**
- Los datos crudos se guardan en: `data/raw/`
- Se genera un archivo de metadatos: `data/raw/metadata.txt`
- El archivo de metadatos contiene:
  - Fechas de descarga
  - Descripción de las fuentes
  - Enlaces a la documentación

### Ejecución del Procesamiento de Datos

```bash
# Opción 1: Usando Makefile (recomendado)
make process

# Opción 2: Ejecutando el script directamente
python notebooks/process_data.py
```

**Salida:**
- Datos procesados (tidy): `data/processed/`
- Datos intermedios: `data/interim/`
- Reporte de calidad: `data/processed/reporte_calidad.txt`

### Pipeline Completo (Descarga + Procesamiento)

```bash
# Ejecuta descarga y procesamiento en secuencia
make data
```

## Estructura de Datos

### Datos Crudos (`data/raw/`)
- `ied_raw.csv` - Inversión Extranjera Directa
- `salario_raw.csv` - Salario Mensual
- `pea_raw.csv` - Población Económicamente Activa
- `gasto_raw.csv` - Gasto Público
- `remesas_raw.csv` - Remesas
- `inegi_educacion_salud_raw.csv` - Indicadores INEGI
- `metadata.txt` - Metadatos de descarga

### Datos Procesados (`data/processed/`)
- `ied_procesado.csv` - IED en formato tidy
- `salario_procesado.csv` - Salarios en formato tidy
- `pea_procesado.csv` - PEA en formato tidy
- `gasto_procesado.csv` - Gasto agregado por estado
- `remesas_procesado.csv` - Remesas en formato tidy
- `educacion_salud_procesado.csv` - Indicadores de educación y salud
- `datos_consolidados.csv` - Todos los indicadores consolidados
- `reporte_calidad.txt` - Reporte de calidad de datos

### Datos Intermedios (`data/interim/`)
- `gasto_detallado.csv` - Gasto público por grupo funcional

## Diccionarios de Datos

Los diccionarios de datos se encuentran en el directorio `references/`:

- `diccionario_economia.md` - Variables económicas (IED, salarios, PEA, gasto, remesas)
- `diccionario_educacion_salud.md` - Indicadores de educación y salud

Cada diccionario contiene:
- Descripción de cada variable
- Tipo de dato y rangos válidos
- Reglas de calidad
- Interpretación y uso
- Fuentes y referencias

## Control de Calidad de Datos

El sistema implementa múltiples niveles de validación:

### Validaciones Automáticas
1. **Existencia de columnas requeridas**
2. **Detección de valores nulos**
3. **Detección de duplicados**
4. **Validación de rangos** (valores negativos, porcentajes)
5. **Validación de tipos de datos**

### Reporte de Calidad
Después de procesar los datos, se genera automáticamente un reporte de calidad:
```bash
cat data/processed/reporte_calidad.txt
```

## Comandos Útiles

```bash
# Ver ayuda de comandos disponibles
make help

# Limpiar archivos compilados de Python
make clean

# Formatear código
make format

# Verificar estilo de código
make lint

# Desactivar entorno virtual
deactivate
```

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

