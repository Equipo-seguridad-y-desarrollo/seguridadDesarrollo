# Diccionario de Datos - Educación y Salud

## Información General
- **Proyecto**: Seguridad y Desarrollo
- **Fuente**: INEGI - Instituto Nacional de Estadística y Geografía
- **API**: https://www.inegi.org.mx/app/api/
- **Última actualización**: 2025
- **Frecuencia de actualización**: Anual

---

## Dataset: Indicadores de Educación y Salud

**Archivo**: `data/processed/educacion_salud_procesado.csv`

### Descripción
Conjunto de indicadores socioeconómicos relacionados con educación y salud para cada 
estado de la república mexicana. Estos indicadores son oficiales y provienen del sistema 
de información estadística del INEGI.

---

## Indicadores de Educación

### 1. Tasa de Analfabetismo

**Código INEGI**: 6207019048

| Campo | Descripción |
|-------|-------------|
| **Definición** | Porcentaje de la población de 15 años y más que no sabe leer ni escribir |
| **Unidad** | Porcentaje (%) |
| **Rango** | 0 - 100 |
| **Interpretación** | Valores bajos indican mejor nivel educativo de la población |

**Reglas de Calidad**:
- Debe estar entre 0 y 100
- Valores decrecientes en el tiempo son esperables
- No debe haber incrementos significativos entre años consecutivos

---

### 2. Grado Promedio de Escolaridad

**Código INEGI**: 6207020032

| Campo | Descripción |
|-------|-------------|
| **Definición** | Número promedio de años de estudio de la población de 15 años y más |
| **Unidad** | Años |
| **Rango** | 0 - 20+ |
| **Interpretación** | Valores altos indican población mejor educada |

**Reglas de Calidad**:
- Debe ser un valor positivo
- Valores crecientes en el tiempo son esperables
- No debe haber decrementos significativos entre años consecutivos
- Típicamente entre 6 y 12 años en México

---

### 3. Porcentaje de Población con Educación Básica

**Código INEGI**: 6207020033

| Campo | Descripción |
|-------|-------------|
| **Definición** | Porcentaje de la población de 15 años y más con educación primaria o secundaria completa |
| **Unidad** | Porcentaje (%) |
| **Rango** | 0 - 100 |
| **Interpretación** | Valores altos indican mejor cobertura de educación básica |

**Niveles educativos incluidos**:
- Primaria completa (6 años)
- Secundaria completa (9 años de escolaridad total)

**Reglas de Calidad**:
- Debe estar entre 0 y 100
- Suma de porcentajes de todos los niveles no debe exceder 100
- Valores crecientes esperables

---

### 4. Porcentaje de Población con Educación Media Superior

**Código INEGI**: 6207020034

| Campo | Descripción |
|-------|-------------|
| **Definición** | Porcentaje de la población de 15 años y más con preparatoria o bachillerato completo |
| **Unidad** | Porcentaje (%) |
| **Rango** | 0 - 100 |
| **Interpretación** | Valores altos indican mejor acceso a educación media superior |

**Niveles educativos incluidos**:
- Preparatoria o bachillerato (12 años de escolaridad total)
- Educación técnica media superior

**Reglas de Calidad**:
- Debe estar entre 0 y 100
- Valores crecientes esperables
- Debe ser menor que el porcentaje con educación básica

---

### 5. Porcentaje de Población con Educación Superior

**Código INEGI**: 6207020035

| Campo | Descripción |
|-------|-------------|
| **Definición** | Porcentaje de la población de 15 años y más con estudios universitarios o posgrado |
| **Unidad** | Porcentaje (%) |
| **Rango** | 0 - 100 |
| **Interpretación** | Valores altos indican mayor acceso a educación superior |

**Niveles educativos incluidos**:
- Licenciatura o profesional
- Especialidad
- Maestría
- Doctorado

**Reglas de Calidad**:
- Debe estar entre 0 y 100
- Valores crecientes esperables
- Debe ser menor que el porcentaje con educación media superior

---

## Indicadores de Salud

### 6. Esperanza de Vida al Nacimiento

**Código INEGI**: 6207003986

| Campo | Descripción |
|-------|-------------|
| **Definición** | Número promedio de años que se espera que viva una persona desde su nacimiento |
| **Unidad** | Años |
| **Rango** | 40 - 90 |
| **Interpretación** | Valores altos indican mejores condiciones de salud y calidad de vida |

**Factores que influyen**:
- Acceso a servicios de salud
- Calidad de la alimentación
- Condiciones sanitarias
- Seguridad pública
- Nivel socioeconómico

**Reglas de Calidad**:
- Debe estar entre 60 y 85 años típicamente en México
- Valores crecientes en el tiempo son esperables
- No debe haber decrementos significativos excepto en situaciones extraordinarias

---

### 7. Tasa de Mortalidad Infantil

**Código INEGI**: 6207004772

| Campo | Descripción |
|-------|-------------|
| **Definición** | Número de defunciones de menores de un año por cada 1,000 nacidos vivos |
| **Unidad** | Por cada 1,000 nacidos vivos |
| **Rango** | 0 - 100 |
| **Interpretación** | Valores bajos indican mejores condiciones de salud infantil |

**Factores que influyen**:
- Acceso a atención prenatal
- Calidad de servicios de salud maternoinfantil
- Nivel socioeconómico de las familias
- Acceso a agua potable y saneamiento

**Reglas de Calidad**:
- Debe ser un valor positivo
- Valores decrecientes en el tiempo son esperables
- Típicamente entre 8 y 20 en México
- No debe haber incrementos significativos sin causa justificada

---

## Estructura del Archivo Procesado

### Columnas

| Columna | Tipo | Descripción | Valores Posibles |
|---------|------|-------------|------------------|
| Estado | String | Nombre del estado de la república | 32 estados de México |
| Periodo | String | Año del registro | 2000-2024 |
| Tasa de analfabetismo | Float | % de población analfabeta | 0-100 |
| Grado promedio de escolaridad | Float | Años promedio de estudio | 0-20 |
| Porcentaje de población con educación básica | Float | % con primaria/secundaria | 0-100 |
| Porcentaje de población con educación media superior | Float | % con preparatoria | 0-100 |
| Porcentaje de población con educación superior | Float | % con universidad | 0-100 |
| Esperanza de vida al nacimiento | Float | Años de esperanza de vida | 60-85 |
| Tasa de mortalidad infantil | Float | Muertes por 1,000 nacidos | 0-100 |

---

## Reglas de Calidad General

### Validaciones Básicas
1. No debe haber valores negativos en ningún indicador
2. Los porcentajes deben estar entre 0 y 100
3. La esperanza de vida debe estar entre 60 y 90 años
4. No debe haber valores nulos para Estado y Periodo

### Validaciones de Coherencia
1. La suma de porcentajes de niveles educativos puede superar 100% (no son mutuamente excluyentes)
2. El grado promedio de escolaridad debe ser coherente con los porcentajes de población por nivel
3. Estados con mayor educación típicamente tienen mayor esperanza de vida

### Validaciones Temporales
1. Los indicadores educativos deben mostrar tendencia creciente
2. La tasa de mortalidad infantil debe mostrar tendencia decreciente
3. La esperanza de vida debe mostrar tendencia creciente o estable

---

## Interpretación y Uso

### Análisis de Desarrollo Social
Los indicadores de educación y salud son fundamentales para:
- Medir el desarrollo humano de cada estado
- Identificar brechas regionales
- Evaluar políticas públicas
- Priorizar inversiones en desarrollo social

### Relaciones Esperadas
- **Educación ↑ → Esperanza de vida ↑**
- **Educación ↑ → Mortalidad infantil ↓**
- **Analfabetismo ↓ → Desarrollo económico ↑**

### Indicadores Compuestos
Estos datos se pueden utilizar para calcular:
- Índice de Desarrollo Humano (IDH)
- Índice de Rezago Social
- Índice de Marginación

---

## Limitaciones

1. **Temporalidad**: Los datos pueden tener rezagos de 1-2 años
2. **Cobertura**: No todos los indicadores están disponibles para todos los años
3. **Granularidad**: Los datos son a nivel estatal, no municipal
4. **Metodología**: Cambios metodológicos pueden afectar la comparabilidad temporal

---

## Referencias

### Fuentes Oficiales
- INEGI - Instituto Nacional de Estadística y Geografía: https://www.inegi.org.mx/
- API de Indicadores INEGI: https://www.inegi.org.mx/app/api/indicadores/
- Banco de Información Económica (BIE): https://www.inegi.org.mx/app/indicadores/

### Metodología
- Encuesta Nacional de Ocupación y Empleo (ENOE)
- Censo de Población y Vivienda
- Encuesta Intercensal
- Estadísticas Vitales de Mortalidad
- Estadísticas Vitales de Natalidad

### Documentación Adicional
- Glosario de términos: https://www.inegi.org.mx/app/glosario/
- Metadatos de indicadores: Incluidos en las respuestas de la API
