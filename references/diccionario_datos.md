<<<<<<< HEAD
# Diccionario de Datos

## Datos de educacion y salud

- **Archivo fuente**: `educacionysalud.csv`
- **Filas x columnas**: 479 x 10
- **Variables categóricas**: id_estado, estado
=======
# Diccionario de Datos – Variables Económicas

## salario mensual promedio por entidad federativa trimestral

- **Archivo fuente**: `salario_raw.csv`
- **Filas x columnas**: 1919 x 6
- **Variables categóricas**: State
>>>>>>> origin/jose

### Variables

| Variable | Tipo | No. no nulos | No. nulos | Ejemplos | Rango numérico | Valores posibles | Descripción (inferida) | Unidades (inferidas) |
|---|---:|---:|---:|---|---|---|---|---|
<<<<<<< HEAD
| `id_estado` | object | 479 | 0 | 01, 02, 03, 04, 05 | [01, 32] |  | Identificador de entidad/estado |  |
| `estado` | object | 479 | 0 | Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila |  |  | Identificador de entidad/estado |  |
| `fecha` | object | 479 | 0 | 2000, 2005, 2010, 2015, 2020 | [1990, 2020] |  | Año de medición |  |
| `der_hab` | float64 | 128 | 351 | 523201.0, 758160.0, 930149.0 | [2.476260e+05, 1.126768e+07] |  | Número de derechohabientes registrados en todos los servicios de salud |  |
| `pob_bac` | float64 | 96 | 383 | 27312.0, 54559.0, 101806.0 | [1.733900e+04, 1.565560e+06] |  | Población con estudios de bachillerato|  |
| `pob_edbas` | float64 | 64 | 415 | 381110.0, 466984.0 | [1.663590e+05, 	5.971664e+06] |  | Población con educación básica|  |
| `pob_edsup` | float64 | 96 | 383 | 24581.0, 56558.0, 121483.0 | [1.305700e+04, 	1.628840e+06] |  | Población con estudios superiores|  |
| `pob_edsup` | float64 | 96 | 383 | 24581.0, 56558.0, 121483.0 | [1.305700e+04, 	1.628840e+06] |  | Población con estudios superiores|  |
| `porc_analf` | float64 | 447 | 32 | 32.1, 52.0, 67.3 | [1.475065, 86.900000 ] |  | Porcentaje de la población analfabeta|  |
| `porc_sined` | float64 | 64 | 415 | 3.078416, 2.311956 | [1.779600, 	14.553113] |  | Porcentaje de la población sin ninguna educación |  |
| `promedio_ed` | float64 | 160 | 319 | 32.1, 52.0, 67.3 | [5.400000, 11.482039] |  | Promedio de escolaridad |  |  |  |
=======
| `State ID` | int64 | 1919 | 0 | 1, 2, 3, 4, 5 | [1, 32] |  | Identificador de entidad/estado/municipio/región. |  |
| `State` | object | 1919 | 0 | Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila |  |  | Identificador de entidad/estado/municipio/región. |  |
| `Quarter ID` | int64 | 1919 | 0 | 20101, 20102, 20103, 20104, 20111 | [2.01e+04, 2.025e+04] |  | Identificador o clave de referencia. |  |
| `Quarter` | object | 1919 | 0 | 2010-Q1, 2010-Q2, 2010-Q3, 2010-Q4, 2011-Q1 |  |  | Trimestre calendario. |  |
| `Monthly Wage` | float64 | 1919 | 0 | 3489.895832122564, 3248.439951488845, 3185.0299909298205, 3181.3475999012835, 32 | [2033, 1.234e+04] |  | Mes calendario. |  |
| `Workforce` | int64 | 1919 | 0 | 447374, 469995, 471876, 457877, 455823 | [2.806e+05, 8.191e+06] |  |  |  |

## remesas por entidad federativa trimestral

- **Archivo fuente**: `remesas_raw.csv`
- **Filas x columnas**: 1600 x 3
- **Variables categóricas**: State

### Variables

| Variable | Tipo | No. no nulos | No. nulos | Ejemplos | Rango numérico | Valores posibles | Descripción (inferida) | Unidades (inferidas) |
|---|---:|---:|---:|---|---|---|---|---|
| `State` | object | 1600 | 0 | Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila |  |  | Identificador de entidad/estado/municipio/región. |  |
| `Quarter` | object | 1600 | 0 | 2013-Q1, 2013-Q2, 2013-Q3, 2013-Q4, 2014-Q1 |  |  | Trimestre calendario. |  |
| `Remittance Amount` | int64 | 1600 | 0 | 70935871, 84477649, 80581209, 80801368, 79194217 | [1.017e+07, 1.52e+09] |  | Remesas monto. |  |

## poblacion economicamente activa por entidad federativa trimestral

- **Archivo fuente**: `pea_raw.csv`
- **Filas x columnas**: 1919 x 5
- **Variables categóricas**: State

### Variables

| Variable | Tipo | No. no nulos | No. nulos | Ejemplos | Rango numérico | Valores posibles | Descripción (inferida) | Unidades (inferidas) |
|---|---:|---:|---:|---|---|---|---|---|
| `State ID` | int64 | 1919 | 0 | 1, 2, 3, 4, 5 | [1, 32] |  | Identificador de entidad/estado/municipio/región. |  |
| `State` | object | 1919 | 0 | Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila |  |  | Identificador de entidad/estado/municipio/región. |  |
| `Quarter ID` | int64 | 1919 | 0 | 20101, 20102, 20103, 20104, 20111 | [2.01e+04, 2.025e+04] |  | Identificador o clave de referencia. |  |
| `Quarter` | object | 1919 | 0 | 2010-Q1, 2010-Q2, 2010-Q3, 2010-Q4, 2011-Q1 |  |  | Trimestre calendario. |  |
| `Workforce` | int64 | 1919 | 0 | 483288, 502204, 504363, 491955, 485158 | [2.994e+05, 8.491e+06] |  |  |  |

## inversion extranjera directa por entidad federativa trimestral

- **Archivo fuente**: `ied_raw.csv`
- **Filas x columnas**: 3328 x 5
- **Variables categóricas**: State

### Variables

| Variable | Tipo | No. no nulos | No. nulos | Ejemplos | Rango numérico | Valores posibles | Descripción (inferida) | Unidades (inferidas) |
|---|---:|---:|---:|---|---|---|---|---|
| `Quarter ID` | int64 | 3328 | 0 | 19991, 19992, 19993, 19994, 20001 | [1.999e+04, 2.024e+04] |  | Identificador o clave de referencia. |  |
| `Quarter` | object | 3328 | 0 | 1999-Q1, 1999-Q2, 1999-Q3, 1999-Q4, 2000-Q1 |  |  | Trimestre calendario. |  |
| `State ID` | int64 | 3328 | 0 | 1, 2, 3, 4, 5 | [1, 32] |  | Identificador de entidad/estado/municipio/región. |  |
| `State` | object | 3328 | 0 | Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila |  |  | Identificador de entidad/estado/municipio/región. |  |
| `Investment` | float64 | 3328 | 0 | 37.22750520706177, 30.149538099765778, 715.2237231731415, 36.24531817436218, 207 | [-1585, 1.381e+04] |  |  |  |

## gasto publico por entidad federativa anual

- **Archivo fuente**: `gasto_raw.csv`
- **Filas x columnas**: 1479 x 6
- **Posibles columnas temporales**: Year
- **Posibles variables categóricas**: State, Functional Group

### Variables

| Variable | Tipo | No. no nulos | No. nulos | Ejemplos | Rango numérico | Valores posibles | Descripción (inferida) | Unidades (inferidas) |
|---|---:|---:|---:|---|---|---|---|---|
| `State ID` | int64 | 1479 | 0 | 1, 2, 3, 4, 5 | [1, 35] |  | Identificador de entidad/estado/municipio/región. |  |
| `State` | object | 1479 | 0 | Aguascalientes, Baja California, Baja California Sur, Campeche, Coahuila |  |  | Identificador de entidad/estado/municipio/región. |  |
| `Functional Group ID` | int64 | 1479 | 0 | 1, 2, 3, 4 | [1, 4] | 1, 2, 3, 4 | Identificador o clave de referencia. |  |
| `Functional Group` | object | 1479 | 0 | Gobierno, Desarrollo Social, Desarrollo Económico, Otras no Clasificadas en Func |  | Gobierno, Desarrollo Social, Desarrollo Económico, Otras no Clasificadas en Func |  |  |
| `Amount Executed` | float64 | 1479 | 0 | 2597413637.38, 18276017602.18, 1687886421.1499996, 5921017322.0, 3469177983.86 | [0, 2.338e+12] |  |  |  |
| `Year` | int64 | 1479 | 0 | 2013, 2014, 2015, 2016, 2017 | [2013, 2023] | 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | Año calendario. |  |


>>>>>>> origin/jose
