
# Diccionario de Datos

## Datos de educacion y salud

- **Archivo fuente**: `educacionysalud.csv`
- **Filas x columnas**: 479 x 10
- **Variables categóricas**: id_estado, estado

| Variable | Tipo | No. no nulos | No. nulos | Ejemplos | Rango numérico | Valores posibles | Descripción (inferida) | Unidades (inferidas) |
|---|---:|---:|---:|---|---|---|---|---|
| `id_estado` | category | 479 | 0 | 01, 02, 03, 04, 05 | [01, 32] |  | Identificador de entidad/estado |  |
| `estado` | category | 479 | 0 | Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila |  |  | Identificador de entidad/estado |  |
| `fecha` | int64 | 479 | 0 | 2000, 2005, 2010, 2015, 2020 | [1990, 2020] |  | Año de medición |  |
| `der_hab` | float64 | 128 | 351 | 523201.0, 758160.0, 930149.0 | [2.476260e+05, 1.126768e+07] |  | Número de derechohabientes registrados en todos los servicios de salud |  |
| `pob_bac` | float64 | 96 | 383 | 27312.0, 54559.0, 101806.0 | [1.733900e+04, 1.565560e+06] |  | Población con estudios de bachillerato|  |
| `pob_edbas` | float64 | 64 | 415 | 381110.0, 466984.0 | [1.663590e+05, 	5.971664e+06] |  | Población con educación básica|  |
| `pob_edsup` | float64 | 96 | 383 | 24581.0, 56558.0, 121483.0 | [1.305700e+04, 	1.628840e+06] |  | Población con estudios superiores|  |
| `pob_edsup` | float64 | 96 | 383 | 24581.0, 56558.0, 121483.0 | [1.305700e+04, 	1.628840e+06] |  | Población con estudios superiores|  |
| `porc_analf` | float64 | 447 | 32 | 32.1, 52.0, 67.3 | [1.475065, 86.900000 ] |  | Porcentaje de la población analfabeta|  |
| `porc_sined` | float64 | 64 | 415 | 3.078416, 2.311956 | [1.779600, 	14.553113] |  | Porcentaje de la población sin ninguna educación |  |
| `promedio_ed` | float64 | 160 | 319 | 32.1, 52.0, 67.3 | [5.400000, 11.482039] |  | Promedio de escolaridad |  |  |  |