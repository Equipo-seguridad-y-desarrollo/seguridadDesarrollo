# 🇲🇽 Proyecto: Seguridad y Desarrollo en México# Seguridad y desarrollo



Análisis de la relación entre indicadores de seguridad y desarrollo económico-social en México.<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">

    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />

---</a>



## 🚀 Inicio RápidoAnálisis sobre el índice de desarrollo y seguridad por municipio



### Instalación Automática## 🚀 Inicio Rápido



**Windows (PowerShell)**:### Prerrequisitos

```powershell- Python 3.8 o superior

.\setup_env.ps1- pip (gestor de paquetes de Python)

python notebooks\descarga_datos_completa.py- Token de API de INEGI (para datos de seguridad)

```

### 1. Configuración del Entorno Virtual

**Linux/macOS**:

```bash#### En Windows (PowerShell):

chmod +x setup_env.sh```powershell

./setup_env.sh# Crear entorno virtual

python notebooks/descarga_datos_completa.pypython -m venv venv

```

# Activar entorno virtual

### Instalación Manual.\venv\Scripts\Activate.ps1



```bash# Si hay error de permisos, ejecutar primero:

# 1. Crear entorno virtualSet-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

python -m venv venv```



# 2. Activar entorno#### En Linux/Mac:

# Windows:```bash

.\venv\Scripts\Activate.ps1# Crear entorno virtual

# Linux/Mac:python3 -m venv venv

source venv/bin/activate

# Activar entorno virtual

# 3. Instalar dependenciassource venv/bin/activate

pip install -r requirements.txt```



# 4. Configurar token de INEGI (crear archivo .env)### 2. Instalar Dependencias

echo "INEGI_API_TOKEN=tu_token_aqui" > .env

```powershell

# 5. Descargar datos# Actualizar pip

python notebooks/descarga_datos_completa.pypython -m pip install --upgrade pip

```

# Instalar dependencias del proyecto

---pip install -r requirements.txt

```

## 📋 Requisitos

### 3. Descarga de Datos de Seguridad

- **Python**: 3.8 o superior

- **Token INEGI**: Gratuito desde https://www.inegi.org.mx/app/api/Los datos de seguridad se descargan desde dos fuentes oficiales:

- **Espacio en disco**: ~100 MB para datos descargados1. **INEGI**: Percepción de inseguridad (requiere token de API)

2. **SESNSP**: Incidencia delictiva estatal

---

#### Obtener Token de API de INEGI:

## 📦 Dependencias1. Visitar: https://www.inegi.org.mx/app/api/indicadores/

2. Registrarse o iniciar sesión

El proyecto usa **dependencias mínimas** por defecto (instalación en ~30-40 segundos):3. Copiar el token proporcionado

- `pandas` - Procesamiento de datos

- `numpy` - Operaciones numéricas  #### Ejecutar descarga:

- `requests` - Peticiones HTTP a APIs```powershell

- `python-dotenv` - Variables de entorno# Método 1: Pasar token directamente

python notebooks/datos_seguridad_mexico.py --token TU_TOKEN_AQUI

### Paquetes Opcionales

# Método 2: Usar archivo .env (recomendado)

Para análisis completo, instala según necesites:# 1. Crear archivo .env en la raíz del proyecto

```bash# 2. Agregar: INEGI_API_TOKEN=TU_TOKEN_AQUI

# Jupyter Notebooks# 3. Ejecutar:

pip install jupyter ipykernelpython notebooks/datos_seguridad_mexico.py

```

# Visualización

pip install matplotlib seaborn**Salidas generadas:**

- `data/raw/indicador_inseguridad_estados.csv` - Percepción de inseguridad por estado (2011-2025)

# Machine Learning- `data/raw/incidencia_delictiva_estatal_2015_2025.csv` - Incidencia delictiva estatal (2015-2025)

pip install scikit-learn scipy- `data/raw/log_descarga_seguridad.txt` - Log detallado con fechas, fuentes y descripción



# Excel### 4. Procesamiento de Datos

pip install openpyxl

```Transformar los datos raw a formato tidy y validar calidad:



---```powershell

python notebooks/procesar_datos_seguridad.py

## 📊 Datos Descargados```



El script `descarga_datos_completa.py` obtiene:**Salidas generadas:**

- `data/processed/percepcion_inseguridad_procesado.csv` - Dataset completo procesado

### 🔒 Seguridad- `data/processed/percepcion_inseguridad_estados.csv` - Solo estados (sin nacional)

- Percepción de inseguridad (INEGI)- `data/processed/incidencia_delictiva_procesado.csv` - Dataset de incidencia procesado

- Incidencia delictiva (SESNSP)- `data/interim/incidencia_delictiva_completa.csv` - Versión intermedia normalizada

- `data/processed/reporte_procesamiento.txt` - Reporte de validación y estadísticas

### 📚 Educación y Salud

- Indicadores educativos (INEGI)### 5. Exploración de Datos (Opcional)

- Indicadores de salud (INEGI)

Notebooks disponibles para análisis exploratorio:

### 💰 Economía

- Inversión Extranjera Directa (Secretaría de Economía)```powershell

- Salarios promedio (DataMexico)# Iniciar Jupyter

- Población Económicamente Activa (DataMexico)jupyter notebook

- Gasto público (DataMexico)

- Remesas (DataMexico)# Abrir en el navegador:

# - notebooks/1.0-exploracion_datos_seguridad.ipynb (Exploración inicial)

### 📈 Desigualdad# - notebooks/2.0-procesamiento_datos_seguridad.ipynb (Pruebas de transformación)

- Coeficiente de Gini (CONEVAL)```



**Total**: ~410,000 registros | ~55 MB## 📊 Diccionarios de Datos



---Los diccionarios completos se encuentran en `references/`:

- `diccionario_datos_seguridad.md` - Documentación completa de datasets de seguridad

## 📁 Estructura del Proyecto- Describe estructura de datos raw y procesados

- Incluye validaciones de calidad y reglas de negocio

```

.## 📁 Estructura del Proyecto

├── README.md                          # Este archivo

├── setup_env.ps1                      # Setup automático (Windows)## 📁 Estructura del Proyecto

├── setup_env.sh                       # Setup automático (Linux/Mac)

├── requirements.txt                   # Dependencias mínimas```

├── .env                               # Token INEGI (crear este archivo)├── LICENSE            <- Open-source license if one is chosen

│├── Makefile           <- Makefile with convenience commands like `make data` or `make train`

├── notebooks/                         # Scripts y notebooks├── README.md          <- The top-level README for developers using this project.

│   ├── descarga_datos_completa.py     # ⭐ Script principal de descarga├── data

│   ├── 1_*.py                         # Scripts de descarga individuales│   ├── external       <- Data from third party sources.

│   ├── 2_*.py                         # Scripts de procesamiento│   ├── interim        <- Intermediate data that has been transformed.

│   └── *.ipynb                        # Notebooks de análisis│   │   └── incidencia_delictiva_completa.csv

││   ├── processed      <- The final, canonical data sets for modeling.

├── data/                              # Datos del proyecto│   │   ├── percepcion_inseguridad_procesado.csv

│   ├── raw/                           # Datos crudos descargados│   │   ├── percepcion_inseguridad_estados.csv

│   ├── interim/                       # Datos intermedios│   │   ├── incidencia_delictiva_procesado.csv

│   └── processed/                     # Datos procesados y limpios│   │   └── reporte_procesamiento.txt

││   └── raw            <- The original, immutable data dump.

├── references/                        # Documentación de referencia│       ├── indicador_inseguridad_estados.csv

│   ├── diccionario_*.md               # Diccionarios de datos│       ├── incidencia_delictiva_estatal_2015_2025.csv

│   └── *.txt                          # Convenciones y fuentes│       └── log_descarga_seguridad.txt

││

└── docs/                              # Documentación adicional├── docs               <- A default mkdocs project; see www.mkdocs.org for details

```│

├── models             <- Trained and serialized models, model predictions, or model summaries

---│

├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),

## 🔑 Configuración del Token INEGI│                         the creator's initials, and a short `-` delimited description, e.g.

│                         `1.0-jqp-initial-data-exploration`.

1. Registrarse en: https://www.inegi.org.mx/app/api/│   ├── 1.0-exploracion_datos_seguridad.ipynb

2. Obtener token (gratuito)│   ├── 2.0-procesamiento_datos_seguridad.ipynb

3. Crear archivo `.env` en la raíz del proyecto:│   ├── datos_seguridad_mexico.py       <- Script de descarga

   ```│   └── procesar_datos_seguridad.py     <- Script de procesamiento

   INEGI_API_TOKEN=tu_token_aqui│

   ```├── pyproject.toml     <- Project configuration file with package metadata for 

│                         Seguridad y desarrollo and configuration for tools like black

---│

├── references         <- Data dictionaries, manuals, and all other explanatory materials.

## 📖 Uso│   └── diccionario_datos_seguridad.md  <- Diccionario completo de datos de seguridad

│

### Descargar Todos los Datos├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.

```bash│   └── figures        <- Generated graphics and figures to be used in reporting

python notebooks/descarga_datos_completa.py│

```├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.

│                         generated with `pip freeze > requirements.txt`

### Procesar Datos│

```bash├── setup.cfg          <- Configuration file for flake8

python notebooks/2_variables_economicas_procesar_datos_formateados.py│

```└── Seguridad y desarrollo   <- Source code for use in this project.

    │

### Análisis en Jupyter    ├── __init__.py             <- Makes Seguridad y desarrollo a Python module

```bash    │

jupyter notebook notebooks/EDA_variables_economicas.ipynb    ├── config.py               <- Store useful variables and configuration

```    │

    ├── dataset.py              <- Scripts to download or generate data

---    │

    ├── features.py             <- Code to create features for modeling

## 🛠️ Solución de Problemas    │

    ├── modeling                

### Error: "No module named 'pandas'"    │   ├── __init__.py 

```bash    │   ├── predict.py          <- Code to run model inference with trained models          

pip install -r requirements.txt    │   └── train.py            <- Code to train models

```    │

    └── plots.py                <- Code to create visualizations

### Error: "INEGI_API_TOKEN not found"```

Crea el archivo `.env` con tu token de INEGI.

## 🔧 Flujo de Trabajo de Datos

### Error de compatibilidad NumPy/Pandas

```bash### Pipeline de Datos de Seguridad

pip uninstall -y numpy pandas

pip install "numpy<2.0" "pandas>=2.0,<2.3"1. **Descarga (Raw)**: `datos_seguridad_mexico.py`

```   - ⬇️  Descarga desde APIs oficiales (INEGI, SESNSP)

   - 💾 Guarda en `data/raw/`

### Activar entorno virtual   - 📝 Genera log con metadata completa

```bash

# Windows2. **Procesamiento (Interim → Processed)**: `procesar_datos_seguridad.py`

.\venv\Scripts\Activate.ps1   - 🧹 Limpia y normaliza datos

   - ✅ Valida calidad (nulos, duplicados, rangos)

# Linux/Mac   - ➕ Agrega columnas calculadas

source venv/bin/activate   - 💾 Guarda en `data/processed/` y `data/interim/`

```   - 📊 Genera reporte de validación



---3. **Exploración y Análisis**: Notebooks

   - 🔍 Exploración visual

## 📚 Diccionarios de Datos   - 📈 Análisis estadístico

   - 🧪 Pruebas de transformaciones

Ver archivos en `references/`:

- `diccionario_datos_seguridad.md` - Variables de seguridad### Validaciones de Calidad Implementadas

- `diccionario_datos_economia.md` - Variables económicas

- `diccionario_datos_educacionysalud.md` - Variables sociales- ✅ **Valores nulos**: Verificación en columnas críticas

- `diccionario_desigualdad.md` - Indicadores de desigualdad- ✅ **Tipos de datos**: Conversión y validación automática

- ✅ **Rangos válidos**: Detección de valores atípicos

---- ✅ **Duplicados**: Identificación por claves únicas

- ✅ **Completitud temporal**: Series de tiempo completas por entidad

## 🤝 Contribuir

## 🧰 Scripts Principales

1. Fork el proyecto

2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)### Scripts de Datos de Seguridad

3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)

4. Push a la rama (`git push origin feature/AmazingFeature`)| Script | Ubicación | Descripción | Uso |

5. Abre un Pull Request|--------|-----------|-------------|-----|

| `datos_seguridad_mexico.py` | `notebooks/` | Descarga de datos de INEGI y SESNSP | `python notebooks/datos_seguridad_mexico.py --token TOKEN` |

---| `procesar_datos_seguridad.py` | `notebooks/` | Procesamiento y validación de datos | `python notebooks/procesar_datos_seguridad.py` |



## 📄 Licencia### Notebooks



Este proyecto está bajo la licencia especificada en el archivo `LICENSE`.| Notebook | Descripción |

|----------|-------------|

---| `1.0-exploracion_datos_seguridad.ipynb` | Exploración inicial y visualizaciones |

| `2.0-procesamiento_datos_seguridad.ipynb` | Pruebas de transformaciones |

## 👥 Equipo

## 📚 Fuentes de Datos

Equipo-seguridad-y-desarrollo

### Datos de Seguridad

---

1. **Percepción de Inseguridad**

## 📞 Contacto   - **Fuente**: INEGI - ENVIPE

   - **Período**: 2011-2025

Para preguntas o sugerencias, abre un issue en el repositorio.   - **Cobertura**: Nacional y 32 estados

   - **Actualización**: Anual

---   - **API**: https://www.inegi.org.mx/app/api/indicadores/



**¡Gracias por usar este proyecto!** 🎉2. **Incidencia Delictiva**

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

