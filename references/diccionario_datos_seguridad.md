# Diccionario de Datos - Indicadores de Seguridad México

## Dataset 1: Indicador de Percepción de Inseguridad por Entidad Federativa

### Información General
- **Nombre del archivo**: `indicador_inseguridad_estados.csv`
- **Fuente**: Instituto Nacional de Estadística y Geografía (INEGI) - API de Indicadores
- **Encuesta**: Encuesta Nacional de Victimización y Percepción sobre Seguridad Pública (ENVIPE) / Censo Nacional de Impartición de Justicia (CNI)
- **Periodicidad**: Anual
- **Cobertura temporal**: 2011-2025
- **Cobertura geográfica**: Nacional y 32 entidades federativas
- **Unidad de medida**: Personas de 18 años y más por cada 100,000 habitantes del mismo grupo de edad
- **Clave del indicador**: 6204327085

### Descripción
Este dataset contiene el número estimado de personas de 18 años y más que perciben su entidad federativa como insegura, expresado como una tasa por cada 100,000 habitantes de ese grupo de edad. Los datos provienen de la ENVIPE y representan la percepción subjetiva de inseguridad de la población adulta.

### Variables

| Campo | Nombre | Tipo de dato | Descripción | Valores posibles | Observaciones |
|-------|--------|--------------|-------------|------------------|---------------|
| año | Año | Integer | Año de referencia de la medición | 2011-2025 | Valores anuales consecutivos |
| valor | Valor del indicador | Float | Número de personas de 18+ años que perciben inseguridad por cada 100,000 habitantes del mismo grupo | 0.00 - 100,000.00 | Valores nulos pueden indicar falta de datos para ese año/entidad |
| entidad | Entidad federativa | String | Nombre completo de la entidad federativa o "Nacional" | Ver catálogo de entidades | 33 valores únicos (32 estados + Nacional) |
| clave | Clave de entidad | String | Código numérico de identificación de la entidad | "00"-"32" | "00" = Nacional, "01"-"32" = Estados según catálogo INEGI |

### Catálogo de Entidades Federativas

| Clave | Entidad |
|-------|---------|
| 00 | Nacional |
| 01 | Aguascalientes |
| 02 | Baja California |
| 03 | Baja California Sur |
| 04 | Campeche |
| 05 | Coahuila |
| 06 | Colima |
| 07 | Chiapas |
| 08 | Chihuahua |
| 09 | Ciudad de México |
| 10 | Durango |
| 11 | Guanajuato |
| 12 | Guerrero |
| 13 | Hidalgo |
| 14 | Jalisco |
| 15 | México |
| 16 | Michoacán |
| 17 | Morelos |
| 18 | Nayarit |
| 19 | Nuevo León |
| 20 | Oaxaca |
| 21 | Puebla |
| 22 | Querétaro |
| 23 | Quintana Roo |
| 24 | San Luis Potosí |
| 25 | Sinaloa |
| 26 | Sonora |
| 27 | Tabasco |
| 28 | Tamaulipas |
| 29 | Tlaxcala |
| 30 | Veracruz |
| 31 | Yucatán |
| 32 | Zacatecas |

---

## Dataset 2: Incidencia Delictiva Estatal

### Información General
- **Nombre del archivo**: `incidencia_delictiva_estatal_2015_2025.csv`
- **Fuente**: Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP) - Datos Abiertos
- **URL origen**: https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_ago25.csv
- **Periodicidad**: Mensual
- **Cobertura temporal**: Enero 2015 - Agosto 2025
- **Cobertura geográfica**: Nacional y 32 entidades federativas
- **Unidad de medida**: Hechos delictivos (conteos absolutos)

### Descripción
Este dataset contiene los registros oficiales de hechos delictivos ocurridos en México, desagregados por entidad federativa, tipo de delito y mes. Los datos son reportados por las procuradurías y fiscalías estatales al SESNSP y representan los delitos del fuero común y federal registrados oficialmente.

### Variables Esperadas

*Nota: La estructura exacta puede variar, pero típicamente incluye las siguientes variables basadas en la estructura estándar del SESNSP:*

| Campo | Nombre | Tipo de dato | Descripción | Valores posibles | Observaciones |
|-------|--------|--------------|-------------|------------------|---------------|
| año | Año | Integer | Año de ocurrencia del delito | 2015-2025 | Valores anuales |
| mes | Mes | Integer/String | Mes de ocurrencia del delito | 1-12 o nombres de meses | Formato puede variar |
| entidad | Entidad federativa | String | Nombre de la entidad federativa | 32 entidades + posibles agregados | Puede usar nombres completos o abreviados |
| tipo_delito | Tipo de delito | String | Categoría del delito | Ver clasificación SESNSP | Múltiples categorías según clasificación oficial |
| subtipo_delito | Subtipo de delito | String | Subcategoría específica del delito | Varía según tipo principal | Mayor detalle de la clasificación |
| total | Total de casos | Integer | Número de hechos delictivos registrados | 0 - N | Conteos absolutos mensuales |

### Clasificación Típica de Delitos (SESNSP)

**Delitos de Alto Impacto:**
- Homicidio doloso
- Homicidio culposo
- Feminicidio
- Secuestro
- Extorsión
- Robo (múltiples modalidades)
- Violencia familiar
- Violación
- Trata de personas
- Narcomenudeo

**Modalidades de Robo:**
- Robo a casa habitación
- Robo a negocio
- Robo de vehículo
- Robo a transeúnte
- Robo en transporte público
- Robo a institución bancaria
- Robo de autopartes
- Otros robos

### Consideraciones Metodológicas

#### Dataset 1 (Percepción de Inseguridad)
- **Cifra obscura**: Este indicador mide percepción, no incidencia real
- **Muestreo**: Basado en encuestas probabilísticas representativas
- **Población objetivo**: Solo personas de 18 años y más
- **Comparabilidad**: Los cambios metodológicos pueden afectar la comparabilidad temporal

#### Dataset 2 (Incidencia Delictiva)
- **Cifra obscura**: Solo incluye delitos denunciados y registrados oficialmente
- **Clasificación**: Puede haber cambios en criterios de clasificación entre años
- **Reportes**: Depende de la capacidad institucional de cada entidad
- **Actualización**: Los datos más recientes pueden ser preliminares

### Notas de Calidad de Datos

1. **Valores faltantes**: Pueden indicar falta de información o problemas en el reporte
2. **Inconsistencias temporales**: Verificar discontinuidades que puedan indicar cambios metodológicos
3. **Outliers**: Valores extremos pueden requerir validación con fuentes adicionales
4. **Agregación**: El dato nacional no siempre es la suma exacta de las entidades por redondeos

### Metadatos de Proceso

- **Fecha de extracción**: Determinar según fecha de ejecución del script
- **Token API INEGI**: 32805429-135c-9311-70c1-0b963c6f8317
- **Método de acceso**: API REST (INEGI) y descarga directa CSV (SESNSP)
- **Transformaciones aplicadas**: Conversión de tipos de datos, renombrado de columnas
- **Control de calidad**: Validación de tipos numéricos con manejo de errores

### Uso Recomendado

- **Análisis temporal**: Evaluar tendencias anuales y estacionales
- **Comparación regional**: Ranking y clustering de entidades
- **Correlación**: Relacionar percepción con incidencia real
- **Visualización**: Series de tiempo, mapas coropléticos, gráficos de barras
- **Modelado**: Variables independientes para modelos predictivos de seguridad pública

---

## DATASETS PROCESADOS

## Dataset 3: Percepción de Inseguridad - Procesado

### Información General
- **Nombre del archivo**: `percepcion_inseguridad_procesado.csv`
- **Ubicación**: `data/processed/`
- **Fuente original**: `data/raw/indicador_inseguridad_estados.csv`
- **Transformaciones aplicadas**: 
  - Normalización de nombres de columnas
  - Conversión de tipos de datos
  - Agregación de columnas calculadas
  - Validación de calidad
  - Ordenamiento por entidad y año

### Descripción
Dataset procesado y limpio listo para análisis, con columnas adicionales calculadas para facilitar el análisis y clasificación de niveles de percepción.

### Variables

| Campo | Nombre | Tipo de dato | Descripción | Valores posibles | Observaciones |
|-------|--------|--------------|-------------|------------------|---------------|
| año | Año | Integer | Año de referencia de la medición | 2011-2025 | Valores anuales consecutivos |
| valor | Valor del indicador | Float | Número de personas de 18+ años que perciben inseguridad por cada 100,000 habitantes | 0.00 - 100,000.00 | Validado en rango [0, 100000] |
| entidad | Entidad federativa | String | Nombre completo de la entidad federativa o "Nacional" | 33 valores únicos | Incluye nacional y 32 estados |
| cve_entidad | Clave de entidad | String | Código numérico de identificación con formato de 2 dígitos | "00"-"32" | Formato normalizado con ceros a la izquierda |
| nivel_percepcion | Nivel de percepción | Category | Clasificación del nivel de percepción de inseguridad | Bajo, Medio, Alto, Muy Alto | Bajo: 0-50k, Medio: 50k-70k, Alto: 70k-85k, Muy Alto: 85k-100k |
| es_nacional | Es nacional | Boolean | Indica si el registro corresponde al nivel nacional | True, False | True cuando entidad="Nacional" |

### Reglas de Clasificación

**Nivel de Percepción (nivel_percepcion):**
- **Bajo**: 0 - 50,000 personas por cada 100,000
- **Medio**: 50,001 - 70,000 personas por cada 100,000
- **Alto**: 70,001 - 85,000 personas por cada 100,000
- **Muy Alto**: 85,001 - 100,000 personas por cada 100,000

### Validaciones de Calidad Aplicadas

1. **Valores nulos**: Verificación en columnas críticas (año, valor, entidad, cve_entidad)
2. **Tipos de datos**: Validación de tipos correctos para cada columna
3. **Rango de valores**: Verificación que 'valor' esté entre 0 y 100,000
4. **Duplicados**: Detección de registros duplicados por (año, cve_entidad)
5. **Completitud temporal**: Verificación de datos para todos los años esperados (2011-2025) por entidad

---

## Dataset 4: Percepción de Inseguridad por Estados (sin nacional)

### Información General
- **Nombre del archivo**: `percepcion_inseguridad_estados.csv`
- **Ubicación**: `data/processed/`
- **Descripción**: Versión del dataset procesado que excluye el registro nacional, contiene únicamente los 32 estados
- **Uso recomendado**: Análisis comparativos entre estados, mapas coropléticos, análisis regionales

### Variables
Mismas variables que `percepcion_inseguridad_procesado.csv`, excepto que:
- No incluye registros donde `entidad = "Nacional"`
- El campo `es_nacional` siempre es `False`
- Total de registros: 32 estados × ~15 años = ~480 registros

---

## Dataset 5: Incidencia Delictiva - Completa (Intermedio)

### Información General
- **Nombre del archivo**: `incidencia_delictiva_completa.csv`
- **Ubicación**: `data/interim/`
- **Fuente original**: `data/raw/incidencia_delictiva_estatal_2015_2025.csv`
- **Estado**: Intermedio - Columnas normalizadas pero sin agregaciones mayores
- **Transformaciones aplicadas**:
  - Normalización de nombres de columnas (minúsculas, guiones bajos)
  - Codificación UTF-8 asegurada

### Descripción
Dataset intermedio que contiene la estructura completa de incidencia delictiva con nombres de columnas normalizados. La estructura exacta depende del archivo fuente del SESNSP, pero típicamente incluye:

### Estructura Esperada (sujeta a variación)

**Columnas de identificación:**
- Año, mes, entidad federativa
- Tipo de delito, subtipo de delito
- Modalidad del delito

**Columnas de conteo:**
- Total de casos por categoría
- Desagregaciones por tipo específico de delito

**Nota**: Este dataset se mantiene en formato intermedio debido a su estructura compleja y variable. Para análisis específicos, se recomienda crear scripts de transformación ad-hoc según las necesidades del proyecto.

---

## METADATOS DE PROCESAMIENTO

### Scripts de Procesamiento

1. **datos_seguridad_mexico.py**
   - **Ubicación**: `notebooks/`
   - **Función**: Descarga de datos raw desde fuentes originales
   - **Salidas**: Archivos en `data/raw/` + log de descarga
   - **Uso**: `python datos_seguridad_mexico.py --token TU_TOKEN_AQUI`

2. **procesar_datos_seguridad.py**
   - **Ubicación**: `notebooks/`
   - **Función**: Transformación de datos raw a procesados
   - **Salidas**: Archivos en `data/processed/` y `data/interim/`
   - **Uso**: `python procesar_datos_seguridad.py`
   - **Genera**: Reporte de procesamiento y validaciones

### Notebooks de Exploración

1. **1.0-exploracion_datos_seguridad.ipynb**
   - Exploración inicial de datos raw
   - Visualizaciones exploratorias
   - Análisis de calidad preliminar

2. **2.0-procesamiento_datos_seguridad.ipynb**
   - Pruebas de transformaciones
   - Desarrollo de validaciones
   - Prototipado antes de scripts

### Control de Calidad

**Reglas de calidad implementadas:**

1. **Valores nulos**:
   - ERROR si >10% de nulos en columnas críticas
   - ADVERTENCIA si <10% de nulos

2. **Tipos de datos**:
   - Verificación de tipos numéricos y string
   - Conversión automática con manejo de errores

3. **Rangos válidos**:
   - Percepción: [0, 100000]
   - Años: [2011, 2025] para percepción, [2015, 2025] para delictiva

4. **Duplicados**:
   - Detección por claves únicas (año + entidad)
   - Reporte en validación

5. **Completitud temporal**:
   - Verificación de serie completa por entidad
   - Identificación de años faltantes

### Archivos Generados en Procesamiento

**data/processed/**
- `percepcion_inseguridad_procesado.csv` - Dataset completo procesado
- `percepcion_inseguridad_estados.csv` - Solo estados (sin nacional)
- `incidencia_delictiva_procesado.csv` - Dataset agregado (si estructura lo permite)
- `reporte_procesamiento.txt` - Reporte detallado del procesamiento

**data/interim/**
- `incidencia_delictiva_completa.csv` - Dataset intermedio normalizado

**data/raw/**
- `log_descarga_seguridad.txt` - Log detallado de descarga con metadata

---

## CHANGELOG

### Versión 2.0 (Octubre 2025)
- Agregados datasets procesados
- Implementadas validaciones de calidad
- Creados scripts de descarga y procesamiento automatizados
- Agregada columna `nivel_percepcion` calculada
- Normalización de nombres de columnas
- Documentación de flujo de procesamiento

### Versión 1.0 (Inicial)
- Documentación de datasets raw
- Definición de estructura básica
- Catálogo de entidades federativas