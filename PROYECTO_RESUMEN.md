# Proyecto: Descarga y Procesamiento de Datos Socioeconómicos

## Resumen del Proyecto

Este proyecto implementa un sistema unificado para descargar y procesar datos de múltiples fuentes públicas de variables socioeconómicas para todos los estados de México.

## Estructura del Proyecto

```
seguridadDesarrollo/
├── notebooks/
│   ├── download_data.py       # Script unificado de descarga
│   └── process_data.py        # Script unificado de procesamiento
├── data/
│   ├── raw/                   # Datos crudos descargados
│   │   ├── ied_raw.csv
│   │   ├── salario_raw.csv
│   │   ├── pea_raw.csv
│   │   ├── gasto_raw.csv
│   │   ├── remesas_raw.csv
│   │   └── metadata.txt       # Metadatos de descarga
│   ├── interim/              # Datos intermedios
│   │   └── gasto_detallado.csv
│   └── processed/            # Datos procesados (tidy)
│       ├── ied_procesado.csv
│       ├── salario_procesado.csv
│       ├── pea_procesado.csv
│       ├── gasto_procesado.csv
│       ├── remesas_procesado.csv
│       ├── datos_consolidados.csv
│       └── reporte_calidad.txt
├── references/
│   ├── diccionario_economia.md
│   └── diccionario_educacion_salud.md
├── requirements.txt
├── Makefile
├── README.md
└── .env.example
```

## Fuentes de Datos

### 1. DataMexico API (Economía)
- **URL**: http://www.economia.gob.mx/datamexico/
- **Datasets**:
  - Inversión Extranjera Directa (IED)
  - Salario Mensual (INEGI-ENOE)
  - Población Económicamente Activa (PEA)
  - Gasto Público Ejecutado
  - Remesas (BANXICO)

### 2. INEGI API (Educación y Salud)
- **URL**: https://www.inegi.org.mx/app/api/
- **API Key**: Configurada en .env
- **Indicadores**:
  - Tasa de analfabetismo
  - Grado promedio de escolaridad
  - Niveles educativos
  - Esperanza de vida
  - Mortalidad infantil

## Uso del Sistema

### 1. Configuración Inicial

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key (opcional)
cp .env.example .env
# Editar .env con tu API key
```

### 2. Descarga de Datos

```bash
# Opción 1: Usando Makefile
make download

# Opción 2: Script directo
python notebooks/download_data.py
```

**Salida**:
- Datos crudos en `data/raw/`
- Archivo de metadatos con fechas y fuentes

### 3. Procesamiento de Datos

```bash
# Opción 1: Usando Makefile
make process

# Opción 2: Script directo
python notebooks/process_data.py
```

**Salida**:
- Datos tidy en `data/processed/`
- Datos intermedios en `data/interim/`
- Reporte de calidad automático

### 4. Pipeline Completo

```bash
# Descarga + Procesamiento
make data
```

## Características Implementadas

### ✓ Script Unificado de Descarga
- Descarga de múltiples fuentes en un solo script
- Manejo de errores robusto
- Generación automática de metadatos
- Información detallada de progreso

### ✓ Script Unificado de Procesamiento
- Limpieza y transformación a formato tidy
- Validación automática de datos
- Detección de valores nulos y duplicados
- Agregación y consolidación de datasets
- Generación de reportes de calidad

### ✓ Metadatos y Documentación
- `metadata.txt`: Información sobre fuentes y fechas de descarga
- `reporte_calidad.txt`: Reporte automático de calidad de datos
- Diccionarios de datos detallados en `references/`

### ✓ Control de Calidad
Validaciones implementadas:
- Existencia de columnas requeridas
- Detección de valores nulos
- Detección de registros duplicados
- Validación de rangos (valores negativos, porcentajes)
- Validación de tipos de datos
- Coherencia temporal

### ✓ Makefile Actualizado
Comandos disponibles:
- `make download` - Descarga datos
- `make process` - Procesa datos
- `make data` - Pipeline completo
- `make requirements` - Instala dependencias
- `make help` - Muestra ayuda

### ✓ README Actualizado
Incluye:
- Instrucciones de configuración del entorno virtual
- Guía de ejecución de descarga y procesamiento
- Estructura de datos explicada
- Referencias a diccionarios de datos

## Formato de Datos

### Datos Tidy (Procesados)

Todos los datasets procesados siguen principios tidy:
- Cada variable es una columna
- Cada observación es una fila
- Cada tipo de unidad observacional es una tabla

Ejemplo (`ied_procesado.csv`):
```csv
Estado,Año,Trimestre,IED_millones_usd
Aguascalientes,1999,Q1,37.23
Aguascalientes,1999,Q2,30.15
...
```

### Dataset Consolidado

El archivo `datos_consolidados.csv` combina todos los indicadores trimestrales:
```csv
Estado,Año,Trimestre,IED_millones_usd,Salario_mensual_pesos,PEA_personas,Remesas_millones_usd,Gasto_ejecutado_pesos
Aguascalientes,2013,Q1,123.45,8500.00,550000,45.67,28482334983.0
...
```

## Reporte de Calidad

Ejemplo del reporte automático generado:

```
Archivo: ied_procesado.csv
  Registros totales: 3328
  Columnas: 4
  Columnas: Estado, Año, Trimestre, IED_millones_usd
  ✓ Sin valores nulos
  ✓ Sin duplicados
```

## Diccionarios de Datos

### diccionario_economia.md
Documentación completa de:
- Inversión Extranjera Directa
- Salario Mensual
- Población Económicamente Activa
- Gasto Público
- Remesas
- Dataset Consolidado

Incluye:
- Descripción de variables
- Tipos de datos y rangos
- Reglas de calidad
- Interpretación y uso
- Limitaciones

### diccionario_educacion_salud.md
Documentación de indicadores INEGI:
- Indicadores educativos (analfabetismo, escolaridad, niveles)
- Indicadores de salud (esperanza de vida, mortalidad infantil)
- Metodología y fuentes

## Cumplimiento de Requerimientos

### ✓ Entorno Virtual
- Instrucciones en README
- Archivo `.env.example` para configuración

### ✓ Script de Descarga
- `notebooks/download_data.py`
- Descarga de 2+ fuentes diferentes
- Genera `metadata.txt` con:
  - Descripción de fuentes
  - Fechas de descarga
  - Enlaces a documentación
  - Explicación de naturaleza de datos

### ✓ Script de Procesamiento
- `notebooks/process_data.py`
- Transforma datos raw a tidy
- Selecciona información relevante
- Guarda en `data/processed/`
- Pasos intermedios en `data/interim/`

### ✓ Diccionarios de Datos
- Un diccionario por conjunto de datos
- Ubicados en `references/`
- Claramente indicados en README

### ✓ Control de Calidad
- Validaciones automáticas
- Reporte de calidad generado
- Reglas simples y obvias implementadas

### ✓ Documentación Makefile
- Método de descarga: `make download`
- Método de procesamiento: `make process`
- Pipeline completo: `make data`

### ✓ README Completo
- ✓ Inicialización de entorno virtual
- ✓ Ejecución de descarga
- ✓ Ejecución de procesamiento
- ✓ Estructura de datos
- ✓ Referencias a diccionarios

## Estadísticas de Datos Procesados

- **Estados**: 32 entidades federativas de México
- **Periodo IED**: 1999-2024
- **Periodo Salario/PEA**: 2010-2025
- **Periodo Gasto**: 2013-2023
- **Periodo Remesas**: 2013-2025
- **Registros totales consolidados**: 3,392
- **Variables en dataset consolidado**: 8

## Tecnologías Utilizadas

- **Python 3.12**: Lenguaje principal
- **pandas**: Manipulación de datos
- **requests**: Descarga de APIs
- **python-dotenv**: Configuración de variables de entorno
- **Makefile**: Automatización de tareas

## Notas Adicionales

1. Los archivos CSV grandes están en `.gitignore` para reducir tamaño del repositorio
2. Los archivos de metadatos y reportes se mantienen en git como evidencia
3. Los datos pueden regenerarse ejecutando el pipeline
4. La API de INEGI requiere una clave que debe configurarse en `.env`
5. Algunas fuentes pueden estar bloqueadas en entornos con restricciones de red

## Próximos Pasos Sugeridos

1. Agregar datos de seguridad (cuando estén disponibles)
2. Agregar datos de rezago educativo (CONEVAL)
3. Implementar análisis exploratorio de datos
4. Crear visualizaciones de tendencias
5. Calcular índices compuestos de desarrollo
