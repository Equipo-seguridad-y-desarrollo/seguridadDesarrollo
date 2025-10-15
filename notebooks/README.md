# Notebooks

Este directorio contiene notebooks de exploración y scripts de procesamiento de datos.

## 📓 Notebooks de Exploración

### 1.0-exploracion_datos_seguridad.ipynb
**Descripción**: Exploración inicial de datos de seguridad descargados.
- Carga y visualización de datos raw
- Análisis estadístico descriptivo
- Detección de valores atípicos
- Verificación de completitud de datos
- Visualizaciones exploratorias

**Cuándo usar**: Después de descargar datos raw para entender su estructura y calidad.

### 2.0-procesamiento_datos_seguridad.ipynb
**Descripción**: Pruebas de transformaciones antes de implementarlas en scripts.
- Transformaciones de datos raw a tidy
- Validaciones de calidad
- Creación de variables derivadas
- Pruebas de agregaciones

**Cuándo usar**: Para experimentar con transformaciones antes de automatizarlas.

## 🐍 Scripts de Datos

### datos_seguridad_mexico.py
**Descripción**: Script para descarga automática de datos de seguridad desde fuentes oficiales.

**Fuentes de datos**:
1. **INEGI - Percepción de Inseguridad** (ENVIPE)
   - API: Banco de Indicadores INEGI
   - Requiere: Token de API
   - Período: 2011-2025
   - Cobertura: Nacional + 32 estados

2. **SESNSP - Incidencia Delictiva Estatal**
   - Descarga directa (CSV)
   - Período: 2015-2025
   - Actualización: Mensual

**Uso**:
```bash
# Opción 1: Pasar token como argumento
python datos_seguridad_mexico.py --token TU_TOKEN_AQUI

# Opción 2: Configurar en .env (recomendado)
# 1. Copiar .env.example a .env
# 2. Editar .env y agregar tu token
# 3. Ejecutar:
python datos_seguridad_mexico.py
```

**Salidas**:
- `data/raw/indicador_inseguridad_estados.csv` - Percepción de inseguridad
- `data/raw/incidencia_delictiva_estatal_2015_2025.csv` - Incidencia delictiva
- `data/raw/log_descarga_seguridad.txt` - Log completo con metadata

**Log de descarga incluye**:
- Fecha y hora de descarga
- Descripción de cada fuente
- URLs y enlaces a documentación
- Periodicidad y cobertura temporal
- Cobertura geográfica
- Número de registros descargados
- Estado de descarga (exitoso/error)

### procesar_datos_seguridad.py
**Descripción**: Script para procesar datos raw a formato tidy con validaciones de calidad.

**Transformaciones aplicadas**:
1. **Percepción de Inseguridad**:
   - Normalización de nombres de columnas
   - Conversión de tipos de datos
   - Creación de variable `nivel_percepcion` (Bajo, Medio, Alto, Muy Alto)
   - Creación de indicador `es_nacional`
   - Ordenamiento por entidad y año

2. **Incidencia Delictiva**:
   - Normalización de nombres de columnas
   - Detección automática de estructura
   - Guardado en formato intermedio para análisis posterior

**Validaciones de calidad**:
- ✅ Valores nulos en columnas críticas
- ✅ Tipos de datos correctos
- ✅ Valores en rangos esperados
- ✅ Detección de duplicados
- ✅ Completitud temporal por entidad

**Uso**:
```bash
python procesar_datos_seguridad.py
```

**Requisitos previos**: Haber ejecutado `datos_seguridad_mexico.py`

**Salidas**:
- `data/processed/percepcion_inseguridad_procesado.csv` - Dataset completo
- `data/processed/percepcion_inseguridad_estados.csv` - Solo estados (sin nacional)
- `data/processed/incidencia_delictiva_procesado.csv` - Dataset procesado
- `data/interim/incidencia_delictiva_completa.csv` - Versión intermedia
- `data/processed/reporte_procesamiento.txt` - Reporte detallado

## 🔄 Flujo de Trabajo Recomendado

### Para nuevos datos de seguridad:

1. **Descarga** (Primera vez o actualización):
   ```bash
   python datos_seguridad_mexico.py --token TU_TOKEN
   ```

2. **Exploración** (Opcional pero recomendado):
   - Abrir `1.0-exploracion_datos_seguridad.ipynb`
   - Ejecutar todas las celdas
   - Revisar visualizaciones y estadísticas

3. **Procesamiento**:
   ```bash
   python procesar_datos_seguridad.py
   ```

4. **Validación**:
   - Revisar `data/processed/reporte_procesamiento.txt`
   - Verificar que no haya errores críticos
   - Revisar advertencias si las hay

5. **Análisis** (Según necesidad):
   - Usar datos de `data/processed/` para análisis
   - Crear nuevos notebooks numerados secuencialmente
   - Documentar hallazgos y conclusiones

## 📝 Convención de Nombres

Los notebooks siguen la convención:
```
<número>.<versión>-<iniciales>-<descripción-corta>.ipynb
```

Ejemplo:
- `1.0-exploracion_datos_seguridad.ipynb`
- `2.0-procesamiento_datos_seguridad.ipynb`
- `3.0-jdoe-analisis-correlacion.ipynb` (nuevo análisis por John Doe)

## 🔧 Dependencias

Todas las dependencias están en `requirements.txt`:
- `pandas` - Manipulación de datos
- `numpy` - Cálculos numéricos
- `matplotlib`, `seaborn` - Visualizaciones
- `requests` - Descargas HTTP
- `python-dotenv` - Manejo de variables de entorno

## 📚 Referencias

- Diccionario de datos: `references/diccionario_datos_seguridad.md`
- Documentación INEGI API: https://www.inegi.org.mx/app/api/indicadores/
- Datos SESNSP: https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva - Scripts de Recopilación de Datos

Este directorio contiene scripts y notebooks para la recopilación y análisis de datos de seguridad en México.

## Script: datos_seguridad_mexico.py

Script para descargar datos de seguridad desde fuentes oficiales mexicanas.

### Datos que descarga:

1. **Indicador de percepción de inseguridad** (INEGI/ENVIPE)
   - Periodicidad: Anual
   - Cobertura: 2011-2025
   - Geografía: Nacional y por entidad federativa
   - Unidad: Personas de 18+ años por cada 100,000 que perciben inseguridad

2. **Incidencia delictiva estatal** (SESNSP)
   - Periodicidad: Mensual
   - Cobertura: Enero 2015 - Agosto 2025
   - Geografía: Por entidad federativa
   - Unidad: Hechos delictivos (conteos mensuales)

### Configuración:

1. Copiar el archivo `.env.example` de la raíz del proyecto a `.env`:
   ```bash
   cp ../.env.example ../.env
   ```

2. Obtener un token de API de INEGI:
   - Visitar: https://www.inegi.org.mx/app/api/
   - Solicitar un token de desarrollador
   - Copiar el token obtenido

3. Editar el archivo `.env` y configurar el token:
   ```
   INEGI_API_TOKEN=tu_token_aqui
   ```

### Uso:

```bash
cd notebooks
python datos_seguridad_mexico.py
```

### Archivos generados:

- `indicador_inseguridad_estados.csv`: Percepción de inseguridad por estado
- `incidencia_delictiva_estatal_2015_2025.csv`: Incidencia delictiva mensual

### Requisitos:

- Python 3.8+
- requests
- pandas
- python-dotenv

Instalar dependencias desde la raíz del proyecto:
```bash
pip install -r requirements.txt
```
