# Diccionario de Datos: Coeficiente de GINI por Estado (2010–2022)

## 1. Descripción General

Este conjunto de datos contiene los valores del **Coeficiente de GINI** estimados para las **entidades federativas de México** durante el período comprendido entre **2010 y 2022**.  

El **Coeficiente de GINI** es una medida estadística utilizada para representar la **distribución del ingreso o la riqueza dentro de una población**, y por tanto, su nivel de desigualdad.  
- Un valor de **0** indica **igualdad perfecta** (todos los individuos tienen el mismo ingreso).  
- Un valor de **1** representa **desigualdad total** (una sola persona concentra todo el ingreso).  

Los datos fueron obtenidos a través de la **plataforma de Datos Abiertos de México**, específicamente desde el portal de la **Secretaría de Economía**, en la sección de indicadores socioeconómicos.  

---

## 2. Información del Archivo

- **Archivo fuente:** `gini_desigualdad_procesado.csv`  
- **Ubicación:** `/data/raw/`  
- **Origen de datos:** [https://www.economia.gob.mx/datamexico/es/about/infoapi)  
- **Periodo de cobertura:** 2010–2022  
- **Filas x columnas:** 224 filas × 4 columnas  
- **Posibles columnas temporales:** `anio`  
- **Posibles variables categóricas:** `estado`

---

## 3. Estructura de Variables

| Variable     | Descripción                                                                                                         | Tipo de dato |
|---------------|---------------------------------------------------------------------------------------------------------------------|---------------|
| `anio`        | Año en que se registró el valor del coeficiente de GINI.                                                           | Entero        |
| `id_estado`   | Identificador numérico oficial de la entidad federativa, de acuerdo con el catálogo del INEGI.                     | Entero        |
| `estado`      | Nombre de la entidad federativa o estado de la República Mexicana.                                                 | Texto         |
| `gini`        | Valor del coeficiente de GINI correspondiente a la entidad y año. Se expresa como número decimal entre 0 y 1.      | Flotante      |

---

## 4. Consideraciones Metodológicas

- Los valores provienen de estimaciones oficiales y pueden haber sido ajustados por métodos de interpolación estadística para garantizar consistencia temporal.  
- La información es útil para **análisis de desigualdad económica**, **estudios de desarrollo social** y **evaluaciones de políticas públicas**.  
- Los nombres de las entidades federativas están normalizados según los códigos oficiales del **INEGI**.  

---

## 5. Fuentes y Referencias

- **Plataforma de Datos Abiertos México – Secretaría de Economía:**  
  [https://www.economia.gob.mx/datamexico/es/vizbuilder)  
- **Instituto Nacional de Estadística y Geografía (INEGI):** Catálogo de entidades federativas.  
- **CONEVAL:** Indicadores de pobreza y distribución del ingreso.  

---

