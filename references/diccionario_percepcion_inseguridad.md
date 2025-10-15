# Diccionario de Datos: Percepción de Inseguridad

## Archivo
`data/processed/percepcion_inseguridad_tidy.csv`

## Descripción General
Indicador de percepción de inseguridad por entidad federativa en México, basado en la Encuesta Nacional de Victimización y Percepción sobre Seguridad Pública (ENVIPE) del INEGI.

## Fuente de Datos
- **Organismo**: Instituto Nacional de Estadística y Geografía (INEGI)
- **Encuesta**: Encuesta Nacional de Victimización y Percepción sobre Seguridad Pública (ENVIPE)
- **Sistema**: Catálogo Nacional de Indicadores (CNI)
- **Clave del indicador**: 6204327085
- **URL**: https://www.inegi.org.mx/programas/envipe/

## Periodicidad
Anual

## Cobertura Temporal
2011 - 2025

## Cobertura Geográfica
- Nacional (total agregado)
- 32 entidades federativas de México

## Definiciones y Conceptos

### Percepción de Inseguridad
Número de personas de 18 años y más que perciben su entidad federativa como insegura, estimadas por cada 100,000 habitantes de ese grupo de edad.

Este indicador refleja la sensación subjetiva de inseguridad de la población adulta, independientemente de la incidencia delictiva real.

## Estructura del Dataset

### Formato
CSV (Comma-Separated Values)

### Codificación
UTF-8

### Número de Columnas
4

### Descripción de Columnas

| Columna  | Tipo de Dato | Descripción | Valores Posibles | Nulos Permitidos |
|----------|--------------|-------------|------------------|------------------|
| año      | Entero       | Año de la medición | 2011 - 2025 | No |
| valor    | Decimal      | Número de personas de 18+ años por cada 100,000 habitantes que perciben inseguridad | 0 - 100000 | No |
| entidad  | Texto        | Nombre de la entidad federativa o "Nacional" | Ver lista de entidades* | No |
| clave    | Texto        | Clave numérica de la entidad | "00" (Nacional), "01" - "32" (Estados) | No |

\* **Lista de entidades**: Nacional, Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila, Colima, Chiapas, Chihuahua, Ciudad de México, Durango, Guanajuato, Guerrero, Hidalgo, Jalisco, México, Michoacán, Morelos, Nayarit, Nuevo León, Oaxaca, Puebla, Querétaro, Quintana Roo, San Luis Potosí, Sinaloa, Sonora, Tabasco, Tamaulipas, Tlaxcala, Veracruz, Yucatán, Zacatecas.

## Calidad de Datos

### Validaciones Implementadas
1. ✓ Verificación de valores nulos
2. ✓ Verificación de rango de años (2011-2025)
3. ✓ Verificación de valores no negativos
4. ✓ Eliminación de duplicados
5. ✓ Ordenamiento por entidad y año

### Consideraciones de Calidad
- Todos los valores deben ser positivos (personas por cada 100,000)
- No debe haber duplicados para la misma combinación de entidad-año
- El valor "Nacional" es un agregado ponderado de todas las entidades

## Ejemplo de Datos

```csv
año,valor,entidad,clave
2011,45678.5,Nacional,00
2011,52341.2,Aguascalientes,01
2011,48923.7,Baja California,02
2012,47234.1,Nacional,00
2012,51023.4,Aguascalientes,01
```

## Usos Recomendados

1. **Análisis de tendencias temporales**: Evaluar cómo ha cambiado la percepción de inseguridad a lo largo del tiempo
2. **Comparaciones estatales**: Identificar estados con mayor o menor percepción de inseguridad
3. **Correlación con otros indicadores**: Comparar con incidencia delictiva real, desarrollo económico, etc.
4. **Mapas de calor**: Visualizar geográficamente la distribución de la percepción de inseguridad

## Limitaciones

- El indicador mide percepción subjetiva, no incidencia delictiva real
- Los datos dependen de la muestra de la ENVIPE
- Puede haber diferencias metodológicas entre años
- La percepción puede estar influida por cobertura mediática y otros factores sociales

## Notas Adicionales

- Los valores se expresan como tasa por cada 100,000 habitantes para facilitar comparaciones entre entidades con diferentes tamaños de población
- El grupo de edad considerado es población de 18 años y más
- Para análisis detallados, se recomienda consultar la metodología completa de ENVIPE en el sitio de INEGI

## Versión del Diccionario
1.0 - Octubre 2025

## Contacto
Para más información sobre los datos, consultar directamente con INEGI: https://www.inegi.org.mx/
