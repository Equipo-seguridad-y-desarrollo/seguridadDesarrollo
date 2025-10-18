# Diccionario de Datos - Variables Económicas

## Información General
- **Proyecto**: Seguridad y Desarrollo
- **Fuente**: DataMexico API (http://www.economia.gob.mx/datamexico/)
- **Última actualización**: 2025
- **Frecuencia de actualización**: Trimestral/Anual según el indicador

---

## 1. Inversión Extranjera Directa (IED)

**Archivo**: `data/processed/ied_procesado.csv`

### Descripción
Montos de inversión extranjera directa recibidos por cada estado de la república mexicana, 
organizados por trimestre. Los datos reflejan el flujo de capital extranjero invertido en 
empresas y proyectos dentro de cada entidad federativa.

### Columnas

| Columna | Tipo | Descripción | Valores Posibles |
|---------|------|-------------|------------------|
| Estado | String | Nombre del estado de la república | 32 estados de México |
| Año | Integer | Año del registro | 1999-2024 |
| Trimestre | String | Trimestre del año | Q1, Q2, Q3, Q4 |
| IED_millones_usd | Float | Monto de IED en millones de dólares USD | ≥ 0 |

### Reglas de Calidad
- No debe haber valores negativos en IED_millones_usd
- Cada combinación Estado-Año-Trimestre debe ser única
- No debe haber valores nulos en las columnas Estado, Año y Trimestre

### Notas
- Los valores están en millones de dólares estadounidenses (USD)
- Un valor alto indica mayor atracción de inversión extranjera
- Los datos provienen del registro oficial de IED reportado a la Secretaría de Economía

---

## 2. Salario Mensual

**Archivo**: `data/processed/salario_procesado.csv`

### Descripción
Salario mensual promedio por estado, calculado a partir de la Encuesta Nacional de 
Ocupación y Empleo (ENOE) del INEGI. Representa el ingreso mensual promedio de los 
trabajadores en cada entidad federativa.

### Columnas

| Columna | Tipo | Descripción | Valores Posibles |
|---------|------|-------------|------------------|
| Estado | String | Nombre del estado de la república | 32 estados de México |
| Año | Integer | Año del registro | 2005-2024 |
| Trimestre | String | Trimestre del año | Q1, Q2, Q3, Q4 |
| Salario_mensual_pesos | Float | Salario mensual promedio en pesos mexicanos | > 0 |

### Reglas de Calidad
- Los valores deben ser positivos
- El salario debe estar dentro de rangos razonables (>= salario mínimo mensual)
- Cada combinación Estado-Año-Trimestre debe ser única

### Notas
- Los valores están en pesos mexicanos (MXN)
- Fuente original: INEGI - ENOE
- Incluye todos los sectores económicos

---

## 3. Población Económicamente Activa (PEA)

**Archivo**: `data/processed/pea_procesado.csv`

### Descripción
Número de personas en edad de trabajar que están ocupadas o buscando empleo activamente 
en cada estado. Es un indicador clave del mercado laboral.

### Columnas

| Columna | Tipo | Descripción | Valores Posibles |
|---------|------|-------------|------------------|
| Estado | String | Nombre del estado de la república | 32 estados de México |
| Año | Integer | Año del registro | 2005-2024 |
| Trimestre | String | Trimestre del año | Q1, Q2, Q3, Q4 |
| PEA_personas | Integer | Número de personas en la PEA | > 0 |

### Reglas de Calidad
- Los valores deben ser enteros positivos
- La PEA no debe exceder la población total del estado
- Cada combinación Estado-Año-Trimestre debe ser única
- No debe haber cambios drásticos sin justificación entre trimestres consecutivos

### Notas
- Fuente original: INEGI - ENOE
- Incluye personas de 15 años y más
- Incluye población ocupada y desocupada que busca trabajo

---

## 4. Gasto Público Ejecutado

**Archivo**: `data/processed/gasto_procesado.csv`

### Descripción
Monto total del gasto público ejecutado por cada estado anualmente. Representa los recursos 
públicos efectivamente gastados (no solo presupuestados) en cada entidad federativa.

### Columnas

| Columna | Tipo | Descripción | Valores Posibles |
|---------|------|-------------|------------------|
| Estado | String | Nombre del estado de la república | 32 estados de México |
| Año | Integer | Año del registro | 2013-2023 |
| Gasto_ejecutado_pesos | Float | Gasto público total en pesos mexicanos | > 0 |

### Archivo Detallado
**Archivo**: `data/interim/gasto_detallado.csv`

Contiene el desglose por grupo funcional:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| Estado | String | Nombre del estado |
| Año | Integer | Año del registro |
| Grupo_Funcional | String | Categoría de gasto (educación, salud, etc.) |
| Gasto_ejecutado_pesos | Float | Gasto en pesos mexicanos |

### Reglas de Calidad
- Los valores deben ser positivos
- El gasto debe ser coherente con el tamaño y población del estado
- Cada combinación Estado-Año debe ser única en el archivo agregado

### Notas
- Los valores están en pesos mexicanos (MXN)
- Fuente: Transparencia Presupuestaria
- Los datos son anuales, no trimestrales

---

## 5. Remesas

**Archivo**: `data/processed/remesas_procesado.csv`

### Descripción
Monto de remesas internacionales recibidas por estado y trimestre. Las remesas son 
transferencias de dinero que los trabajadores mexicanos en el extranjero envían a sus 
familias en México.

### Columnas

| Columna | Tipo | Descripción | Valores Posibles |
|---------|------|-------------|------------------|
| Estado | String | Nombre del estado de la república | 32 estados de México |
| Año | Integer | Año del registro | 2003-2024 |
| Trimestre | String | Trimestre del año | Q1, Q2, Q3, Q4 |
| Remesas_millones_usd | Float | Monto de remesas en millones de dólares USD | ≥ 0 |

### Reglas de Calidad
- Los valores deben ser no negativos (pueden ser 0)
- Cada combinación Estado-Año-Trimestre debe ser única
- No debe haber valores nulos

### Notas
- Los valores están en millones de dólares estadounidenses (USD)
- Fuente original: Banco de México (BANXICO)
- Las remesas son un ingreso importante para muchas familias mexicanas

---

## 6. Dataset Consolidado

**Archivo**: `data/processed/datos_consolidados.csv`

### Descripción
Dataset que consolida todos los indicadores económicos trimestrales en un solo archivo, 
facilitando el análisis conjunto de múltiples variables.

### Columnas

| Columna | Tipo | Descripción |
|---------|------|-------------|
| Estado | String | Nombre del estado de la república |
| Año | Integer | Año del registro |
| Trimestre | String | Trimestre del año |
| IED_millones_usd | Float | Inversión Extranjera Directa |
| Salario_mensual_pesos | Float | Salario mensual promedio |
| PEA_personas | Integer | Población Económicamente Activa |
| Remesas_millones_usd | Float | Remesas recibidas |
| Gasto_ejecutado_pesos | Float | Gasto público (anual, repetido por trimestre) |

### Reglas de Calidad
- La combinación Estado-Año-Trimestre debe ser única
- Pueden existir valores nulos cuando un indicador no está disponible para ese periodo
- Todos los valores numéricos deben ser coherentes con sus datasets originales

### Notas
- Este archivo facilita análisis de correlación entre variables
- Algunos indicadores pueden tener valores nulos en ciertos periodos
- El gasto público es anual, por lo que se repite para todos los trimestres del mismo año

---

## Interpretación y Uso

### Indicadores Económicos Clave
1. **IED**: Mayor IED indica mayor confianza de inversionistas extranjeros
2. **Salario**: Salarios altos indican mejor calidad de vida y poder adquisitivo
3. **PEA**: PEA creciente indica mercado laboral activo
4. **Gasto Público**: Mayor gasto puede indicar más inversión en servicios públicos
5. **Remesas**: Altas remesas pueden indicar migración significativa

### Análisis Sugeridos
- Correlación entre IED y crecimiento económico estatal
- Relación entre salarios y costo de vida
- Impacto del gasto público en desarrollo social
- Dependencia económica de las remesas por estado

### Limitaciones
- Los datos están sujetos a revisiones por las fuentes oficiales
- Puede haber rezagos en la disponibilidad de datos recientes
- Los valores nominales no están ajustados por inflación
- Algunas series tienen periodos faltantes

---

## Referencias

- DataMexico: http://www.economia.gob.mx/datamexico/
- INEGI: https://www.inegi.org.mx/
- Banco de México: https://www.banxico.org.mx/
- Transparencia Presupuestaria: https://www.transparenciapresupuestaria.gob.mx/
