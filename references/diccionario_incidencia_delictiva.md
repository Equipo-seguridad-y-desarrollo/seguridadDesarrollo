# Diccionario de Datos: Incidencia Delictiva Estatal

## Archivos

### Principal (Formato Tidy)
`data/processed/incidencia_delictiva_tidy.csv`

### Resumen Anual
`data/processed/incidencia_delictiva_resumen_anual.csv`

### Intermedio
`data/interim/incidencia_delictiva_interim.csv`

## Descripción General
Hechos delictivos registrados en averiguaciones previas y carpetas de investigación iniciadas por las procuradurías y fiscalías estatales de México. Contiene información detallada sobre delitos del fuero común desagregados por tipo, entidad federativa y periodo temporal.

## Fuente de Datos
- **Organismo**: Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP)
- **Programa**: Incidencia Delictiva del Fuero Común - Nueva Metodología
- **URL de descarga**: https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/
- **URL de referencia**: https://www.gob.mx/sesnsp/acciones-y-programas/incidencia-delictiva-del-fuero-comun-nueva-metodologia

## Periodicidad
Mensual (publicación aproximadamente el día 20 de cada mes con datos del mes anterior)

## Cobertura Temporal
Enero 2015 - Agosto 2025 (corte vigente)

## Cobertura Geográfica
32 entidades federativas de México

## Definiciones y Conceptos

### Incidencia Delictiva
Número de hechos delictivos registrados en averiguaciones previas iniciadas o carpetas de investigación, reportados por las Procuradurías Generales de Justicia y Fiscalías Generales de las entidades federativas.

### Fuero Común
Delitos que son competencia de las autoridades estatales y municipales (en contraste con el fuero federal).

### Bien Jurídico Afectado
Categorización de los delitos según el derecho o bien que se protege legalmente (ej: vida, patrimonio, libertad, etc.).

## Estructura del Dataset

### Archivo Principal (Tidy): incidencia_delictiva_tidy.csv

#### Formato
CSV (Comma-Separated Values)

#### Codificación
UTF-8

#### Descripción de Columnas

| Columna | Tipo de Dato | Descripción | Valores Posibles | Nulos Permitidos |
|---------|--------------|-------------|------------------|------------------|
| año | Entero | Año del registro | 2015 - 2025 | No* |
| clave_entidad | Texto/Entero | Clave numérica de la entidad federativa | 1 - 32 | No* |
| entidad | Texto | Nombre completo de la entidad federativa | Ver lista de estados** | No |
| bien_juridico | Texto | Categoría del bien jurídico afectado | Ver categorías*** | No* |
| tipo_delito | Texto | Tipo específico de delito | Variable según bien jurídico | No* |
| subtipo_delito | Texto | Subtipo o especificación del delito | Variable según tipo | No* |
| modalidad | Texto | Modalidad en que se cometió el delito | Variable según subtipo | No* |
| mes | Texto | Nombre del mes | Enero - Diciembre | No |
| num_delitos | Entero | Número de delitos registrados | 0 - n | No |

\* Nota: Dependiendo de la estructura original del archivo, algunas columnas pueden variar. La estructura exacta se valida durante el procesamiento.

\*\* **Estados**: Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila, Colima, Chiapas, Chihuahua, Ciudad de México, Durango, Guanajuato, Guerrero, Hidalgo, Jalisco, México, Michoacán, Morelos, Nayarit, Nuevo León, Oaxaca, Puebla, Querétaro, Quintana Roo, San Luis Potosí, Sinaloa, Sonora, Tabasco, Tamaulipas, Tlaxcala, Veracruz, Yucatán, Zacatecas.

\*\*\* **Bienes Jurídicos Principales** (ejemplos):
- La vida y la integridad corporal
- La libertad personal
- La libertad y la seguridad sexual
- El patrimonio
- La familia
- La sociedad
- Otros bienes jurídicos afectados

### Archivo Resumen Anual: incidencia_delictiva_resumen_anual.csv

#### Descripción de Columnas

| Columna | Tipo de Dato | Descripción | Valores Posibles | Nulos Permitidos |
|---------|--------------|-------------|------------------|------------------|
| año | Entero | Año del registro | 2015 - 2025 | No |
| entidad | Texto | Nombre de la entidad federativa | Ver lista de estados | No |
| total_delitos | Entero | Total de delitos en el año para la entidad | 0 - n | No |

## Calidad de Datos

### Validaciones Implementadas
1. ✓ Conversión de valores no numéricos a NaN
2. ✓ Eliminación de registros con valores nulos en num_delitos
3. ✓ Verificación y corrección de valores negativos (convertidos a 0)
4. ✓ Conversión de num_delitos a tipo entero
5. ✓ Ordenamiento consistente de registros

### Transformaciones Aplicadas
1. **Normalización de nombres de columnas**: Estandarización de nombres para facilitar el procesamiento
2. **Formato ancho a largo (wide to long)**: Conversión de columnas mensuales a filas individuales
3. **Limpieza de valores**: Eliminación de espacios y caracteres especiales
4. **Agregación**: Creación de resumen anual por entidad

### Consideraciones de Calidad
- Los datos provienen de reportes oficiales de procuradurías y fiscalías
- Puede haber retrasos en la actualización de cifras de meses recientes
- Los cambios metodológicos en 2015 hacen que los datos anteriores no sean directamente comparables
- No todos los delitos se denuncian (cifra negra)

## Ejemplo de Datos

### Formato Tidy
```csv
año,clave_entidad,entidad,bien_juridico,tipo_delito,subtipo_delito,modalidad,mes,num_delitos
2015,9,Ciudad de México,El patrimonio,Robo,Robo de vehículo,Con violencia,Enero,3245
2015,9,Ciudad de México,El patrimonio,Robo,Robo de vehículo,Con violencia,Febrero,3187
2015,9,Ciudad de México,El patrimonio,Robo,Robo de vehículo,Sin violencia,Enero,5432
```

### Formato Resumen
```csv
año,entidad,total_delitos
2015,Ciudad de México,523456
2015,Jalisco,312789
2016,Ciudad de México,498234
```

## Usos Recomendados

1. **Análisis de tendencias delictivas**: Evaluar la evolución temporal de diferentes tipos de delitos
2. **Comparaciones estatales**: Identificar estados con mayor o menor incidencia delictiva
3. **Análisis por tipo de delito**: Estudiar patrones específicos de criminalidad
4. **Estacionalidad**: Identificar patrones mensuales o estacionales en la incidencia delictiva
5. **Mapas de calor**: Visualizar geográficamente la distribución de delitos
6. **Correlaciones**: Relacionar con indicadores socioeconómicos y de percepción de seguridad

## Limitaciones

1. **Cifra negra**: No todos los delitos se denuncian, por lo que las cifras oficiales subestiman la incidencia real
2. **Cambios metodológicos**: La metodología cambió en 2015, limitando la comparabilidad con años anteriores
3. **Heterogeneidad en el registro**: Pueden existir diferencias en los criterios de registro entre entidades
4. **Rezago en actualización**: Los datos más recientes pueden estar sujetos a actualizaciones posteriores
5. **Fuero federal no incluido**: Solo contempla delitos del fuero común, excluyendo delitos federales
6. **Datos agregados**: No incluye información sobre ubicación específica dentro de cada estado

## Notas Adicionales

### Tipos de Delitos Principales (ejemplos)
- **Vida e integridad corporal**: Homicidio doloso, homicidio culposo, feminicidio, lesiones
- **Libertad personal**: Secuestro, tráfico de menores, otros delitos contra la libertad personal
- **Libertad y seguridad sexual**: Abuso sexual, acoso sexual, hostigamiento sexual, violación, violación equiparada
- **Patrimonio**: Robo (vehículos, casas, negocios, transeúntes), fraude, abuso de confianza, extorsión, daño a la propiedad
- **Familia**: Violencia familiar, violencia de género, incumplimiento de obligaciones familiares
- **Sociedad**: Corrupción de menores, trata de personas, narcomenudeo

### Modalidades Comunes
- Con violencia / Sin violencia
- Simple / Agravado
- En vía pública / En domicilio / En negocio
- A transeúnte / A repartidor / A conductor

## Referencias Metodológicas

Para información detallada sobre la metodología de recopilación y clasificación:
- Guía metodológica del SESNSP
- Catálogo Nacional de Incidencia Delictiva
- Código Penal de cada entidad federativa

## Versión del Diccionario
1.0 - Octubre 2025

## Contacto
Para más información sobre los datos, consultar directamente con SESNSP: https://www.gob.mx/sesnsp
